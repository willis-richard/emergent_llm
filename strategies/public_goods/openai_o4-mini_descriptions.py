"""
Strategy descriptions for PublicGoodsDescription.

Generated with:
- Provider: OpenAI
- Model: o4-mini
"""


description_COOPERATIVE_1 = '''
Below is a simple “Grim‐Trigger + Endgame‐Defect” strategy.  It is fully cooperative as long as everyone has cooperated so far, but (1) punishes any one defection by defecting forever after, and (2) defects in the very last round (no future to protect).  This is a deterministic, memory-one strategy augmented with one Boolean flag:

––––––––––––––––––––––––––––––––––––––  
Strategy name: Grim–Trigger with Endgame-Defect  

State variable:  
 punish ← false   // has any defection been seen so far?  

At the start (before round 1):  
 punish ← false  

For each round t = 1,2,…,r do:  
 if t = r then  
  // Last round has no future; defect to protect against free-riding  
  play D  
 else if punish = true then  
  // Once we’ve seen any defection, we defect forever after  
  play D  
 else if t = 1 then  
  // First move: establish cooperation  
  play C  
 else  
  // t ∈ {2,…,r−1}, punish=false  
  if in round t–1 any player j played D then  
   punish ← true  
   play D         // trigger punishment  
  else  
   play C         // continue cooperating  
  end if  
 end if  

––––––––––––––––––––––––––––––––––––––  
Explanation of key points:

1.  First round (t=1): we play C to lead by example.  
2.  Rounds 2 to r–1:  
   –  If nobody has defected so far (punish=false) and the immediately previous round was all C’s, continue cooperating.  
   –  If in the last round someone defected, set punish=true and defect this round.  From that moment on punish=true forever, so we defect in every remaining round.  
3.  Last round (t=r): irrespective of history we defect, since there is no future round in which to enforce cooperation.  
4.  forever defection after the first observed defection is the “Grim trigger.”  It enforces cooperation by threatening permanent exclusion of benefits if any player ever deviates.  

Properties:  
•  Incentive to cooperate from round 1 through r–1 is high, because as long as everyone remains C no one ever suffers the permanent punishment and the group enjoys the efficient all-C payoff.  
•  Last‐round defection is standard endgame logic in a finite horizon.  
•  The strategy is entirely deterministic, easy to implement, and robust in tournaments of independent strategies.
'''

description_COOPERATIVE_2 = '''
Below is a single‐strategy “recipe” for a cooperative entrant in the r–round N-player public‐goods tournament.  It is a variant of Tit-for-Tat (TFT) with a short punishment phase and majority‐rule forgiveness.  It (a) starts by cooperating, (b) punishes only when a majority defected last round, (c) forgives after a fixed number of defections, and (d) uses the same rule even in the last round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Parameters you choose once before play:  
   • τ (cooperation threshold) = 0.5       (we require ≥50% cooperators in prior round)  
   • M (punishment length) = 2            (number of rounds to defect after a “bad” round)

2.  Internal state:  
   • punish_counter ← 0

3.  Round-by-round decision rule (for t = 1,2,…,r):  
   if t == 1 then  
     play C  
     continue to next round  
   end if  

   if punish_counter > 0 then  
     play D  
     punish_counter ← punish_counter – 1  
     continue to next round  
   end if  

   let c_prev = number of cooperators observed in round t–1  
   let frac_prev = c_prev / n  

   if frac_prev ≥ τ then  
     play C  
   else  
     play D  
     punish_counter ← M  
   end if  

   (No special override for the last round—just apply the same rule.)

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of why this is “cooperative”:  
1. First move cooperates, signaling willingness to build the public good.  
2. It punishes only if fewer than half the group cooperated in the prior round—so it never over‐rewards single missteps.  
3. Punishment is limited to M=2 rounds, then it resumes cooperation, allowing for recovery.  
4. By using a simple majority threshold, it aligns its choice with the group’s recent behavior and does not try to out‐guess individual identities.  
5. Because it forgives, entire‐group cooperation can become stable.  

Edge‐cases:  
• First round: automatic C, since there is no history.  
• Rounds with an active punish_counter: automatic D until the counter runs out.  
• Last round: treated exactly the same as other rounds—no special “defect for final gain” override—so if the group has been mostly cooperating, it will still play C, reinforcing a cooperative stance even when there is no future.
'''

description_COOPERATIVE_3 = '''
Below is a simple, fully‐deterministic “Public‐Goods Tit-for-Tat” (PG-TFT) strategy.  It is designed to sustain full cooperation whenever possible, to punish defections by denying the public good in the very next round, and to forgive as soon as the group re-establishes full cooperation.  

1.  Data structures and parameters  
   •  n: number of players  
   •  r: total number of rounds  
   •  history[t][i]: action of player i in round t (C or D)  

2.  High-level description  
   –  Round 1: cooperate.  
   –  For every subsequent round t=2…r:  
        •  If in t–1 every player cooperated, then cooperate;  
        •  Otherwise defect.  
   –  By construction, if all players ever return to full-C in some round, PG-TFT will immediately revert to C and stay there as long as nobody defects.  

3.  Pseudocode  

  initialize:  
    for i in 1…n: history[0][i] ←––  (no round 0)  

  for t in 1…r:  
    if t == 1:  
      my_action ← C  
    else:  
      // count cooperators in previous round  
      coop_count ← 0  
      for j in 1…n:  
        if history[t-1][j] == C:  
          coop_count ← coop_count + 1  
      end for  

      if coop_count == n:  
        my_action ← C         // full cooperation last round ⇒ cooperate  
      else:  
        my_action ← D         // at least one defector ⇒ punish by defecting  
      end if  
    end if  

    // (record your action; simultaneously the others do likewise)  
    history[t][me] ← my_action  
    // play my_action in round t  
  end for  

4.  Why this is cooperative  
   •  It unconditionally starts with C.  
   •  It never punishes longer than one round: as soon as all players again play C, PG-TFT immediately resumes cooperation.  
   •  It sustains the Pareto‐optimal all‐C path if no one deviates.  
   •  It handles the last round identically to all others, so if all have cooperated throughout, PG-TFT will even cooperate in round r (exploiting the “shadow of the future” built into everyone playing PG-TFT).  

5.  Edge cases  
   –  First round (t=1): no history ⇒ cooperate by rule.  
   –  Last round (t=r): the same threshold rule applies; if full-C at t–1, cooperate at r.  
   –  One lone defection triggers exactly one round of collective punishment, then full cooperation is restored automatically if the group repairs itself.
'''

description_COOPERATIVE_4 = '''
Below is a single‐strategy proposal—a forgiving “trigger‐and‐forgive” rule—that (i) seeks full cooperation, (ii) punishes any defection with exactly one round of defection, then (iii) immediately returns to cooperation, and (iv) starts with cooperation.  It does not rely on any off-path beliefs or signals beyond the observable history, and it treats all opponents symmetrically.  

––––––––––––––––––––––––––––––––––––––––  
Name: Forgiving Trigger Strategy (FT)

Intuition:  
•  Always start by cooperating.  
•  If someone defects, punish by defecting exactly one round.  
•  After that one‐round punishment, forgive unconditionally and return to cooperation.  
•  Repeat this “punish once, then forgive” cycle whenever a new defection appears.  

State variables:  
  in_punish  ∈ {false, true}  ← whether we are in the one‐round punishment phase  

Decision rule for round t:  
  if t = 1 then  
    play C  
  else if in_punish = true then  
    play D  
    in_punish ← false        // punishment phase ends here  
  else if any player j chose D in round t–1 then  
    play D                    // trigger punishment  
    in_punish ← true  
  else  
    play C  

Edge cases:  
•  First round (t=1): no history ⇒ cooperate.  
•  Any time we are in a punishment phase (in_punish=true) we defect exactly once, then clear the flag.  No further checks on what happened in the punishment round itself (so we don’t end up punishing ourselves).  
•  If another defection occurs in the round immediately following our punishment, we will punish again for one round, then forgive, and so on.  
•  Last round (t=r): the same rule applies—if we are in punishment, we defect; otherwise we cooperate—even though there is no future, we choose C to maximize group payoff.  

Pseudocode  

  initialize  
    in_punish ← false  

  for t in 1…r do  
    if t = 1 then  
      a_t ← C  
    else if in_punish = true then  
      a_t ← D  
      in_punish ← false  
    else  
      // inspect last round’s actions  
      let defect_occurred ← (∃ j ∈ {1…n}: action_j,t−1 = D)  
      if defect_occurred then  
        a_t ← D  
        in_punish ← true  
      else  
        a_t ← C  
      end if  
    end if  

    play a_t  
  end for  

Why this fosters cooperation:  
1.  Mutual cooperation in round 1 yields higher payoffs than mass defection (k/n·n = k > 1).  
2.  As long as no one defects, all continue to cooperate indefinitely—maximizing payoffs each round.  
3.  The moment any single defection appears, every cooperator immediately retaliates by defecting exactly one round—imposing a short, sharp cost on the defector and all punishers (but no more).  
4.  Forgiveness after one round prevents endless retaliation cycles and allows the group to re-establish full cooperation if the lone defector returns to C.  
5.  Because punishment is only one round, the cost of deviating is less than the gain from realigning with cooperators; this makes return to cooperation attractive.  
6.  By cooperating in the final round (unless we are in the middle of a one‐round punishment), we preserve a cooperative reputation to the end.  

This strategy thus (i) avoids being “suckered” by pure cooperators, (ii) deters persistent defectors, and (iii) quickly forgives isolated mistakes—maximizing overall group payoffs in a repeated public goods setting.
'''

description_COOPERATIVE_5 = '''
Below is a single‐strategy proposal, which we’ll call “Generous One–Round Punisher.”  It is designed to sustain cooperation most of the way through the r rounds, to punish any defection quickly, and to forgive thereafter.  It also handles the unravelling pressure in the very last round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Intuition  
  • Start by cooperating.  
  • If anyone defects, punish by defecting for exactly one full round.  
  • After that one‐round punishment, “forgive” and return to cooperation (unless there is a new defection).  
  • In the very last round, defect (standard backward‐induction exit).  
  This simple trigger–punishment–forgiveness rule is enough to deter one‐shot deviations while keeping the group locked in mutual cooperation for r–1 rounds.  

2. Parameters & State  
  Let n, r, k be given.  
  Choose punishment length L = 1.  
  Maintain one state variable:  
    pun_remain ∈ {0,1}  (how many more rounds we must defect to complete punishment)  

3. Full Decision Rule (per round t = 1…r)  
  
  If t == 1:  
    play C  
    set pun_remain ← 0  
    return  

  If t == r:                    ← last round  
    play D  
    return  

  If pun_remain > 0:            ← we are in the middle of punishing  
    play D  
    pun_remain ← pun_remain – 1  
    return  

  Otherwise (pun_remain = 0 and 1 < t < r):  
    look at round t–1 history:  
      let defect_count ← number of players who played D in round t–1  
    if defect_count > 0:        ← someone defected last round  
      play D                   ← begin one‐round punishment  
      pun_remain ← L           ← schedule exactly L=1 future defects  
    else                        ← full cooperation last round  
      play C  
    return  

4. Pseudocode  

  initialize pun_remain ← 0

  for t in 1…r do
    if t == 1 then
      action[t] ← C
      pun_remain ← 0
      continue
    end if

    if t == r then
      action[t] ← D
      continue
    end if

    if pun_remain > 0 then
      action[t] ← D
      pun_remain ← pun_remain – 1
      continue
    end if

    // No active punishment, not first or last round
    let defect_count ← count of D’s in round (t–1)
    if defect_count > 0 then
      action[t] ← D       // trigger punishment
      pun_remain ← 1      // punish exactly one more round
    else
      action[t] ← C       // continue cooperation
    end if
  end for

5. Why this is cooperative  
  • You begin by cooperating, so you never risk being the first defector.  
  • Any single defection by any player is punished exactly one round—enough to make defection costly but not so long that the group collapses.  
  • After that one‐round punishment, you immediately return to cooperation (“forgiveness”).  
  • You only defect in the very final round (t = r), as compelled by backward induction.  
  • Against other cooperative‐minded strategies of this form, you will almost always see full cooperation for rounds 1 through r–1, yielding each player payoff ≈ k each round (the social optimum).  

6. Edge Cases  
  • If two players defect simultaneously in round t, each sees defect_count>0 in t and punishes in t+1; these cross‐punishments resolve in one round and then cooperation resumes.  
  • If a defection occurs in round r–1, you will punish in round r—but since you also want to defect in round r anyway, the two criteria coincide.  
  • If everyone uses this rule, defect_count will always be 0 after round 1, so the group stays in C–C–C… until the last round, then all defect.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This “Generous One–Round Punisher” is easy to implement, rewards full cooperation, responds swiftly to any defection, and forgives immediately so you avoid locked‐in mutual punishment.
'''

description_COOPERATIVE_6 = '''
Below is a self–contained “cooperative” strategy for the finite, simultaneous‐move N-player public goods game.  It (a) starts by cooperating, (b) punishes any observed defection by one round of mutual defection, then forgives and returns to cooperation, and (c) always defects in the very last round (to guard against end‐game exploitation).  In tournament play this gives a high incentive to stay jointly cooperative, but does not allow one single defection to collapse cooperation forever.

---

Name: Forgiving‐Trigger Cooperation (FTC)

Parameters (internal to FTC):  
- retaliation_length L = 1  (punish defectors for exactly one round)  
- endgame_rounds E = 1       (defect in the final E rounds)

State variable:  
  punish_turns_remaining (integer ≥ 0), initially 0.

Decision rule at round t (1≤t≤r):
1. If t > r – E  then  
     play Defect  // last E rounds we always defect  
2. Else if t = 1 then  
     play Cooperate   
3. Else if punish_turns_remaining > 0 then  
     play Defect  
     punish_turns_remaining ← punish_turns_remaining – 1  
4. Else  // t in 2..r–E and not currently punishing  
     if (in round t–1 at least one player j≠i chose D) then  
         // someone defected last round  
         punish_turns_remaining ← L  
         play Defect  
     else  
         play Cooperate

Pseudocode:

  initialize punish_turns_remaining ← 0  
  for t in 1..r do  
    if t > r – E then  
      action_t ← D  
      continue  
    if t = 1 then  
      action_t ← C  
      continue  
    if punish_turns_remaining > 0 then  
      action_t ← D  
      punish_turns_remaining ← punish_turns_remaining – 1  
      continue  
    // otherwise inspect last round  
    let defections_last = count of players j with action_{t−1} = D  
    if defections_last ≥ 1 then  
      punish_turns_remaining ← L  
      action_t ← D  
    else  
      action_t ← C  
  end for

Discussion of key points:

1. First round (t = 1): we cooperate unconditionally.  
2. Monitoring: we observe the full vector of actions each previous round (public info).  
3. Punishment: as soon as we see any defection in round t–1, we defect in round t.  That one–round “punishment” suffices to lower a defector’s extra gain by k/n × (number of cooperators), creating a disincentive to deviate.  
4. Forgiveness: after exactly L = 1 round of punishment, we reset punish_turns_remaining to 0 and go back to cooperating (provided no new defections are observed).  This avoids “death spiral” of permanent mutual defection.  
5. End‐game (t > r–1): we defect in the very last round to avoid being exploited by other strategies that know we will cooperate there.  All rational strategies do defect in the last round of a finite game, so we conform to that logic.  

Why this is cooperative:  
- If everyone plays FTC, no one ever defects (no trigger is ever pulled), so all r–1 early rounds are full‐cooperate, yielding maximal group payoff.  
- A single opportunistic defection is immediately punished for one round and then cooperation resumes.  The cost of that one‐round punishment can outweigh the short‐run defector’s gain if k is not too large, deterring unilateral defection.  
- By not punishing forever, the strategy restores cooperation quickly and maintains high average payoff over r rounds.  
- By defecting only in the last round, we protect ourselves from “end‐game” sucker-payoffs without undermining early cooperation.

This simple “forgiving‐trigger” strikes a balance between deterrence of free‐riding and rapid restoration of cooperation, making it well suited for a tournament of independent cooperator‐seeker strategies.
'''

description_COOPERATIVE_7 = '''
Here is a simple, fully‐specified “conditional‐cooperator” strategy that (i) starts out fully cooperative, (ii) continues to cooperate whenever the group in the immediately preceding round produced a high enough public­‐good return to make cooperation worthwhile, (iii) defects otherwise, and (iv) defects on the very last round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Benefit‐Proportional Conditional Cooperator (BPCC)  

Intuition  
•  In each intermediate round, you look back at how many people cooperated last time.  
•  If that number was at least the break-even level (so that your share of the public good last round would have been ≥1 had you cooperated), you keep cooperating.  
•  If it was below break-even, you switch to defection.  
•  You start out cooperating and you defect on the very last round (standard endgame logic).  

Parameters you know:  
  n = number of players  
  k = project multiplier (1 < k < n)  
  r = total rounds  

Precompute:  
  threshold = ceil(n / k)  
    •  This is the smallest integer c  such that (k/n)·c ≥ 1.  
    •  Equivalently, if at least “threshold” players cooperated last round, then a cooperator would have gotten ≥ 1 from the public good alone.  

Pseudocode  

```
function BPCC_Action(t, history):
  # history is a list of past joint‐action profiles, each entry e.g.
  #   history[t’] = [a1, a2, …, a_n] with a_i in {C,D}

  if t == 1:
    return C             # always start by cooperating

  if t == r:
    return D             # endgame defect

  # otherwise 1 < t < r: look at last round’s contributions
  last_profile = history[t-1]               # index as desired
  c_prev = count_C(last_profile)            # number of C’s in round t−1

  if c_prev ≥ threshold:
    return C         # group produced enough; continue cooperating
  else:
    return D         # group failed break‐even; defect this round
```

Explanation of key steps  
1. threshold = ceil(n/k)  
   – If exactly c_prev players cooperated last round, then anyone playing C would have earned  
     π_C = 0 + (k/n)·c_prev.  
   – We require π_C ≥ 1 ↔ (k/n)·c_prev ≥ 1 ↔ c_prev ≥ n/k.  
   – Hence we set threshold = ⌈n/k⌉ to capture “cooperation was, at least, not loss‐making.”  

2. Round 1: cooperate unconditionally.  
   – This gives us the best shot at jump‐starting mutual cooperation.  

3. Rounds 2 … r−1: conditional.  
   – If the previous round was “at or above break–even,” we trust the group to keep it up and we cooperate.  
   – If it fell below break–even, we defect to punish/withdraw our contribution.  

4. Round r: defect.  
   – There is no future in which our defection could be punished, so standard backward‐induction recommends defection.  

Why this is cooperative  
•  When all players use BPCC and start by cooperating, c_prev = n each time, which is ≥ threshold, so everyone will keep cooperating through round (r−1).  
•  If any individual unilaterally defects early, as long as the group that remains still meets c_prev ≥ threshold, everybody forgives and continues cooperating.  
•  Only if enough players defect in one round to push c_prev below threshold do all BPCC players switch to defection in the next round—this punishes severe breakdowns but tolerates small lapses.  
•  Because BPCC players immediately resume cooperation once c_prev bounces back to ≥ threshold, accidental or sporadic defections do not lock the group into permanent mutual defection.  

Edge‐case summary  
•  First round: C (no history).  
•  Last round: D (endgame defection).  
•  Between: compare c_prev to ⌈n/k⌉ and cooperate if and only if c_prev ≥ ⌈n/k⌉.  

This strategy is easy to implement, transparent to opponents, and in head‐to‐head or tournament play tends to sustain high levels of cooperation while punishing only sufficiently large breakdowns—and it never forgives endgame defection.
'''

description_COOPERATIVE_8 = '''
Below is a simple, fully decentralized “tit-for-tat with one-round punishment and end-game defection” strategy. It (1) starts by cooperating, (2) cooperates whenever everyone did in the previous round, (3) punishes any defection by defecting exactly once, then forgives, and (4) defects in the known last round (since no future punishment is possible).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: TFT-1P-END  

Parameters:  
• n ≥2 players, r rounds, k∈(1,n) (as specified)  
• P = 1 (punishment length)  

State variable (local to you):  
• punish_counter ← 0 (remaining rounds in “punish” mode)  

Decision rule for each round t = 1…r:  
1. If t = 1:  
     play C  
2. Else if t = r:  
     // Last round: no future leverage ⇒ defect  
     play D  
3. Else if punish_counter > 0:  
     // Punishment in progress  
     play D  
     punish_counter ← punish_counter − 1  
4. Else (punish_counter = 0 and 1 < t < r):  
     Let coop_prev ← number of cooperators in round t−1 (including your own past action).  
     If coop_prev = n:  
         // Everyone cooperated last round ⇒ reward with cooperation  
         play C  
     Else:  
         // At least one defector ⇒ trigger one-round punishment  
         punish_counter ← P  
         play D  

Pseudocode summary:  
```
initialize punish_counter = 0

for t in 1..r do
  if t == 1 then
    action ← C

  else if t == r then
    action ← D

  else if punish_counter > 0 then
    action ← D
    punish_counter ← punish_counter - 1

  else
    coop_prev = count_cooperators_in_round(t-1)
    if coop_prev == n then
      action ← C
    else
      punish_counter ← 1
      action ← D
    end if
  end if

  play(action)
end for
```

Explanation of how it meets your three requirements:

1. Specify decision rules  
   – Round 1: always cooperate; gives a clear signal of willingness.  
   – Intermediate rounds:  
     • If everyone cooperated last round → cooperate.  
     • If you are in a “punishment” window → defect this round only.  
     • If you are free to react and saw any defection last round → defect this round, entering a one-round punishment.  
   – Round r: always defect (standard backward-induction endgame).

2. Handle edge cases  
   – First round has no history → default to C.  
   – Last round has no continuation → default to D to avoid being exploited.  
   – Punishment never spills beyond one round, so after punishing you automatically revert to cooperation if others have returned to C.

3. Be cooperative  
   – You always reward full cooperation immediately by cooperating.  
   – You never punish more than one round, so a single slip or noise won’t lead to permanent breakdown.  
   – You only defect in the last round (when cooperation is futile for self-interest) and when punishing a recent defection.  
   – Against fellow cooperators (who also use TFT-1P-END or any strategy that returns to C after one punishment), this yields unanimous cooperation each round 2…r−1.

This strategy is simple, transparent, retaliatory enough to deter free-riding, yet forgiving so that cooperation can be quickly restored.
'''

description_COOPERATIVE_9 = '''
Below is a single, self‐contained “conditional cooperation” strategy for the n-player, r-round public-goods game.  It is cooperative by default, punishes defections in a simple way, forgives quickly, and handles first and last rounds explicitly.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: Forgiving Tit-for-Tat with Endgame Adjustment  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

1. Overview  
   - Cooperate (C) in round 1.  
   - In each intermediate round, if you are currently “in punishment mode,” defect (D); otherwise cooperate, unless someone defected in the immediately preceding round, in which case enter punishment mode and defect.  
   - Punishment mode lasts exactly one round (a single “tit-for-tat” retaliation), then you return to cooperation.  
   - In the final round you defect (standard endgame logic).  

2. Why this is cooperative  
   - You start by trusting everyone.  
   - You only punish when you observe free‐riding, and you punish just long enough to deter it (one round), then you resume cooperation.  
   - By defecting only in the last round, you do not undermine the incentives for cooperation earlier in the game.  

3. Detailed decision rules  
   Let t = current round (1 ≤ t ≤ r).  
   Maintain a state variable punishCounter ∈ {0,1}, initialized to 0.  

   At the start of round t:  
   1) If t == 1:  
         action ← C  
   2) Else if t == r:  
         action ← D  
   3) Else if punishCounter > 0:  
         action ← D  
         punishCounter ← punishCounter − 1  
   4) Else (punishCounter == 0 and 1 < t < r):  
         If “any player (including yourself) chose D in round t−1” then  
           punishCounter ← 1  
           action ← D  
         Else  
           action ← C  

   After all actions in round t are revealed, update punishCounter as above before moving to t+1.  

4. Pseudocode  

   initialize punishCounter ← 0  

   for t in 1..r do  
     if t == 1 then  
       play C  
     else if t == r then  
       play D  
     else if punishCounter > 0 then  
       play D  
       punishCounter ← punishCounter − 1  
     else  
       if (∃ j such that opponent j’s action in round t−1 was D) then  
         punishCounter ← 1  
         play D  
       else  
         play C  
       end if  
     end if  

     observe all players’ actions this round  
     -- (no additional state update needed here; punishCounter is already set)  
   end for  

5. Edge‐case discussion  
   • First round (t=1):  We have no history, so we cooperate to signal willingness.  
   • Intermediate rounds (1<t<r):  We punish any defection from the previous round exactly once, then we forgive.  If everyone cooperated last round, we continue to cooperate.  
   • Last round (t=r):  We defect—there are no future rounds, so no benefit in cooperating (standard end‐game rationality).  

6. Expected behavior in a tournament  
   • If all players adopt this strategy, then for rounds 1 through r−1 everyone will cooperate (because no one ever defects), and in round r everyone defects.  Total payoff per player = (r−1)×(k)×(n/n) + 1 = (r−1)×k + 1.  
   • If someone ever defects prematurely, our strategy punishes them in the next round, but then quickly returns to cooperation, thereby sustaining high cooperation while discouraging repeated free‐riding.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This single‐round‐punishment TFT variant is simple to implement, extremely cooperative, yet enforces accountability for non‐cooperators.
'''

description_COOPERATIVE_10 = '''
Below is a simple, fully‐specified “collective Tit-for-Tat” style strategy that (1) always starts by cooperating, (2) punishes any defection by defecting exactly one round, then (3) immediately returns to cooperation if the group re-cooperates.  It is easy to implement, transparent to opponents, and fosters high welfare by keeping punishments short and forgiveness swift.

---

Name:  Collective Tit-for-Tat (C-TFT)

Decision rules  
1. Round 1: play C.  
2. For each round t = 2,…,r:  
   • If in round t − 1 **every** player contributed (i.e. all played C), then play C.  
   • Otherwise (at least one D in t − 1), play D.  

No other bookkeeping is needed.  Cooperation is only withheld for exactly one round after any defection, after which you revert to cooperation whenever the group does.

Edge‐case handling  
• First round: cooperate unconditionally to signal your willingness.  
• Last round (t = r): apply the same rule.  If everyone cooperated in round r−1, you cooperate in r; otherwise you defect.  (This may admit cooperation in the final round if you’ve built a cooperative track record.)  
• Multiple defections: even if many players defect in round t−1, you still punish only one round.  

Pseudocode  
```
Input: history H of past actions, where H[t−1][j] ∈ {C,D} for each player j
for t in 1..r:
   if t == 1:
      play C
   else:
      // check if last round was all‐cooperate
      if ∀j ∈ {1..n}: H[t−1][j] == C:
         play C
      else:
         play D
```

Why this is cooperative  
– You always start by cooperating.  
– You cooperate whenever the group cooperates, so you never “hold out” longer than necessary.  
– You punish defection immediately but only briefly (one round), preventing cascades of mutual defection.  
– By forgiving as soon as the group returns to all‐C, you create a stable reward for sustained cooperation.  

This strategy is easy to understand, cannot be exploited by long‐term “trembling,” and supports high average payoffs in the repeated public‐goods setting.
'''

description_COOPERATIVE_11 = '''
Below is a single‐agent decision rule (“you” below means this strategy) that (i) tries to sustain full cooperation, (ii) punishes defections just enough to deter free-riding, (iii) forgives so that cooperation can be re-established, and (iv) handles first‐ and last‐round edge cases.  

Name: Forgiving Trigger (FT)  

Parameters:  
  • r = total rounds  
  • n, k as given (strategy does not need to know k beyond that cooperation is socially beneficial)  

State variable:  
  “mode” ∈ {COOP, PUNISH}  
    – COOP: you intend to cooperate next round  
    – PUNISH: you intend to defect next round as a one‐round punishment  

Initialization (before round 1):  
  mode ← COOP  

Decision rule for round t:  
  if t == 1 then  
    play C  
    continue to next round  
  end if  

  if t == r then  
    /* Last round: no future to enforce cooperation */  
    play D  
    end strategy  
  end if  

  /* t in {2,…,r–1} */  
  if mode == COOP then  
    /* Check for any defection by others in last round */  
    if ∃ j ≠ you : action_j(t–1) == D then  
      mode ← PUNISH  
      play D      /* punish once */  
    else  
      play C      /* all cooperated last round → continue cooperating */  
    end if  

  else /* mode == PUNISH */  
    /* You are in punishment mode: use this round to send the “we saw a defection” message */  
    play D        
    /* Now check if punishees stopped defecting in last round */  
    if ∀ j ≠ you : action_j(t–1) == C then  
      mode ← COOP   /* everyone cooperated last round → forgive */  
    else  
      /* At least one player still defected last round → stay in PUNISH */  
      mode ← PUNISH  
    end if  
  end if  

End of decision rule.  

Explanation:  
1. First round you cooperate to signal willingness.  
2. Rounds 2 through r–1:  
   – In COOP mode you contribute unless you observed any defection in the immediately preceding round, in which case you switch to PUNISH mode and defect once.  
   – In PUNISH mode you defect for one round as a penalty. After punishing, if everyone else cooperated in the last round, you forgive (return to COOP); otherwise you continue to punish.  
3. In the very last round (t = r) you defect, since there is no future round in which to enforce cooperation (“end‐game”).  

Why this works as a cooperative strategy:  
• It unconditionally cooperates with cooperators.  
• It punishes defection quickly (at most one round of suffering), but then forgives as soon as cooperation is restored, preventing endless mutual punishment.  
• The threat of a one‐round defection penalty makes free‐riding less attractive: a defector loses the future stream of cooperation from you unless she returns to cooperation immediately.  
• By defecting in the very last round you avoid being exploited when there is no future to enforce cooperation.  

Pseudocode summary:  
```
mode = COOP
for t in 1..r:
  if t == 1:
    action[t] = C
  else if t == r:
    action[t] = D
  else if mode == COOP:
    if any opponent played D in round t-1:
      action[t] = D
      mode = PUNISH
    else:
      action[t] = C
  else:  # mode == PUNISH
    action[t] = D
    if all opponents played C in round t-1:
      mode = COOP
    else:
      mode = PUNISH
```
This strategy is simple, transparent, and fosters high levels of cooperation in a tournament of unknown opponents.
'''

description_COOPERATIVE_12 = '''
Below is a simple “N‐player Tit‐for‐Tat with Last‐Round Defection” strategy.  It is designed to sustain full cooperation throughout most of the r-rounds by rewarding perfect group cooperation and punishing any defection—yet it avoids being suckered in the last round, where backward induction predicts universal defection.

1.  State variables:
    •   last_round_all_cooperated?  (Boolean)  
         – true if in the previous round every player chose C;  
         – false otherwise.  
    •   current_round t ∈ {1,…,r}.

2.  Initialization (before round 1):
    last_round_all_cooperated? ← true  
    t ← 1

3.  Decision rule for each round t:
    if t == r then
        // Last round: defect to avoid being exploited
        play D
    else if t == 1 then
        // First move: signal cooperation
        play C
    else
        // Rounds 2 through r−1: mirror the group’s last move
        if last_round_all_cooperated? == true then
            play C
        else
            play D
    end if

4.  After observing all n actions in round t:
    last_round_all_cooperated? ← (number_of_C  == n)

5.  Increment round counter:
    t ← t + 1  
    Repeat step 3 until t > r.

— — — — — — — — — — — — — — — — — —

Explanation of why this is cooperative:

•   Incentive to cooperate early and mid-game  
    – By starting with C and cooperating whenever everyone cooperated in the previous round, you create a positive reward loop: as long as the group stays fully cooperative, you keep cooperating, yielding the group payoff of k·n/n = k each round (each player earns k).

•   Simple, transparent punishment  
    – The moment any player defects, “last_round_all_cooperated?” flips to false, and you defect exactly once in the next round.  This single-round punishment is enough to make unilateral defection unprofitable in expectation, yet it is not so harsh that a single “one-off” mistake dooms the whole future.

•   Forgiving  
    – After punishing for one round, if the group returns to full cooperation you do too.  This prevents endless mutual defection spirals.

•   Last‐round defection  
    – Standard backward induction dictates that in a finite repeated public‐goods game everyone defects in the last round.  To avoid being exploited in round r, you defect there.

Pseudocode  

```
initialize:
    last_round_all_cooperated? = true
    t = 1

while t ≤ r:
    if t == r:
        action = D
    else if t == 1:
        action = C
    else:
        if last_round_all_cooperated?:
            action = C
        else:
            action = D
    end if

    // submit action, observe all players’ actions
    observe actions_j for j=1…n
    count_C = # of j with actions_j == C
    last_round_all_cooperated? = (count_C == n)

    t = t + 1
end while
```

This strategy is easy to implement, clearly communicates your willingness to cooperate, enforces accountability for defection, and avoids last‐round exploitation—thus fostering high levels of cooperation over the course of the tournament.
'''

description_COOPERATIVE_13 = '''
Below is a single‐strategy proposal—“Threshold‐Punish‐&‐Forgive”—that (1) starts by cooperating, (2) punishes defection lightly, (3) forgives quickly, and (4) defects in the final round (since there is no future to sustain). The key idea is to maintain full cooperation whenever possible, but to respond to multi-player breakdowns with a brief sanction so that defectors learn that mass defection is not profitable.

1.  Overview of decision rules  
    •  Round 1: Cooperate.  
    •  Rounds 2…(r−1):  
       –  If you are in a “punishment window,” defect.  
       –  Otherwise look at the previous round’s total cooperators C_prev:  
          •  If C_prev ≥ n − 1 (i.e. at most one defector), continue to cooperate.  
          •  If C_prev < n − 1 (i.e. two or more defectors),  play D and trigger a 1‐round punishment window.  
    •  Round r (last round): Defect.  
    •  Punishment window length is 1 round.  After that you automatically forgive.

2.  Rationale  
    –  By cooperating when almost everybody cooperated (C_prev≥ n−1), you sustain maximum public‐good provision.  
    –  By punishing when there was widespread defection (C_prev< n−1), you make defection collectively unprofitable.  
    –  By limiting punishment to a single round, you allow the group to quickly return to full cooperation.  
    –  Defecting in the last round is individually optimal given no future reputation benefit.

3.  Edge cases  
    –  First round has no history ⇒ play C.  
    –  Last round has no future ⇒ play D.  
    –  If multiple mass‐defections occur in a row, you will re‐trigger punishment each time.  
    –  This strategy needs only the count of cooperators in the immediately preceding round.

4.  Pseudocode  

    Parameters:  
      n            # number of players  
      r            # total rounds (>1)  
      PUNISH_LEN=1 # length of punishment window  

    State variables (initialize before round 1):  
      punish_until = 0   # last round index up to which we defect  

    For t in 1..r do:  
      if t == 1 then  
        action ← C  
      else if t == r then  
        action ← D  
      else  
        if t ≤ punish_until then                # we are punishing  
          action ← D  
        else                                    # in normal mode  
          C_prev ← number of cooperators in round t−1  
          if C_prev ≥ n − 1 then                # almost full cooperation last round  
            action ← C  
          else                                  # too many defectors last round  
            action ← D  
            punish_until ← t + PUNISH_LEN      # trigger one‐round punishment  
          end if  
        end if  
      end if  

      “Play action in round t.”  

5.  Discussion  
    –  If every other player also plays this strategy, the path is:  
        Round 1: All C ⇒ full cooperation.  
        Rounds 2…r−1: C_prev=n ⇒ keep playing C ⇒ full cooperation forever until last round.  
        Round r: All defect (D).  
    –  Suppose one or two players stray and defect in round t. Then in t+1 your strategy defects (punishment). If they return to cooperating in t+1, you see C_prev≥n−1 in round t+1 and forgive in round t+2.  
    –  This “tit-for-mass‐defection” rule punishes only when defection is widespread, punishes only 1 round, and immediately rewards any return to cooperation.  
    –  The final‐round defection is standard for finite‐horizon games and gives you the one‐off advantage when no future rounds remain.

This strategy is simple, transparent, and strongly pro-cooperation: it sustains full group contributions whenever possible and applies minimal but credible punishment to deter multi-player breakdowns.
'''

description_COOPERATIVE_14 = '''
Below is a simple “Grim‐with‐Endgame” strategy that (i) sustains full cooperation as long as nobody ever defects, (ii) punishes any defection by defecting thereafter, and (iii) anticipates the one‐shot defection in the very last round.

1. Intuition  
   - Rounds 1 through r–1: “Cooperate unless someone has ever defected before; if they have, defect forever.”  
   - Round r: defect (standard end‐game result).  
   This gives a large “stick” (many future rounds of lost cooperation) to deter early defection, yet accepts that rational players will defect in the known final round.

2. Decision Rules  
   Maintain a Boolean flag `any_defection_so_far` (initially false).  
   For each round t = 1,2,…,r:  
     if t == r:  
       play D  
     else if any_defection_so_far == false:  
       play C  
     else:  
       play D  

   After actions in round t become public, if any player chose D in round t, set  
     any_defection_so_far ← true.

3. Edge‐Cases  
   • First round (t=1): `any_defection_so_far` is false ⇒ you play C.  
   • If someone defects in round r−1, you will still defect in r (but you would anyway).  
   • Once `any_defection_so_far` flips to true—even if that happens late—you defect for all remaining t<r (punishment is short if late, long if early).  
   • Round r is always D.  

4. Why it’s cooperative  
   • If no one ever defects in 1…r−1, everyone earns  
         π_i,t = (k/n)·n = k  
     each of those rounds, which exceeds the “always­‐defect” stream (1 each).  
   • Any single defection in round t < r triggers up to (r−1 − t) rounds of lost k‐payoffs for the defector (since you and all “grim” players will defect thereafter), making early defection unprofitable when k>1.  
   • In the subgame starting at any t<r, the threat of perpetual defection is credible, since it costs you only the remaining cooperation you were already planning (round r would be D in any case).

5. Pseudocode

```
initialize:
  any_defection_so_far ← false

for t in 1…r do
  if t == r then
    action ← D
  else if any_defection_so_far == false then
    action ← C
  else
    action ← D
  end if

  submit(action)

  // AFTER simultaneous play, observe all n actions this round
  if (any player’s action == D) then
    any_defection_so_far ← true
  end if
end for
```

Summary  
• Cooperate in every round 1 through r−1 so long as no defection has ever occurred.  
• Defect forever after the first observed defection.  
• Defect in the known final round.  
This maximally sustains cooperation across the bulk of the game, deters free‐riding early on, and acknowledges the inevitable defection in a finitely repeated public‐goods context.
'''

description_COOPERATIVE_15 = '''
Below is a single‐strategy recipe that (1) starts fully cooperative, (2) punishes defections but forgives quickly, and (3) handles both the first and last round.  It requires no special coordination beyond observing the previous round’s play.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
STRATEGY “Generous Trigger with Finite Punishment”  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

State variables (for each player i):  
• pun_counter (integer ≥ 0), initially 0  
• last_actions (vector of length n), the observed actions in t–1  

Parameters you choose once:  
• P = 1    ← punishment length in rounds  
• T = n–1  ← threshold of cooperators needed to stay in cooperation  

Decision rule for round t = 1…r:  
1. if t == 1  
     ai,t ← C  
   else if t == r  
     ai,t ← D        # Last‐round defection (standard endgame play)  
   else if pun_counter > 0  
     ai,t ← D  
     pun_counter ← pun_counter – 1  
   else  
     countC ← number of C’s in last_actions  
     if countC ≥ T  
       ai,t ← C       # “Enough” cooperators last round → cooperate  
     else  
       # someone defected, trigger punishment  
       pun_counter ← P  
       ai,t ← D  

After all players reveal actions in round t, update:  
• last_actions ← observed profile in t  
• (pun_counter already decremented or reset above)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Why this works cooperatively  
1. First round: everyone who follows this plays C, so it “tries” for full‐group cooperation from the outset.  
2. Trigger‐and‐punish: if you see fewer than n–1 cooperators in the previous round, you defect for P rounds (P=1 here)—that punishes any defector quickly.  
3. Finite punishment: after P rounds you “forgive” and resume cooperation, so you don’t lock yourself into permanent defection (avoids endless mutual punishment).  
4. Threshold T = n–1: you require only a single defection to punish, but tolerate “rumor” of one mistake in case of asynchronous observation.  You could set T=n if you want zero tolerance.  
5. Last round: you defect, since in a finitely repeated game backward induction predicts universal defection in round r anyway.  

Edge cases handled  
• First round (t=1): always C.  
• “Off‐by‐one” defection: since T=n–1, if exactly one player defects you still punish, but only for one round (P=1) and then return to cooperation.  
• Multiple simultaneous defectors: you punish exactly the same (P rounds).  If the group repeatedly defects, you will continue to defect until you observe a “mostly cooperative” round.  
• Last round (t=r): always D.  

Discussion & tuning  
– Raising P makes the punishment harsher (longer) but risks dragging out needless defection.  P=1 or 2 is usually enough to deter freeloaders.  
– Lowering T (e.g. T = ⌈0.8 n⌉) makes you more forgiving in the face of multiple defectors, which can help restart cooperation in noisy environments.  
– If you anticipate truly rational opponents who know backward‐induction, you could try to “smooth” the endgame by cooperating in r–1 if you saw full cooperation in r–2; but most simple strategies will still defect in the last two rounds.  

This recipe strikes a balance: it is unmistakably cooperative when the group is cooperating, it punishes any defection quickly, but it forgives almost immediately so that the group can return to mutual cooperation.
'''

description_COOPERATIVE_16 = '''
Below is a single‐strategy (no tags, no side channels) that (a) starts out fully cooperative, (b) punishes only when the group defects beyond a small tolerance, (c) forgives quickly so cooperation can rebuild, and (d) defects in the very last round to guard against end‐game exploitation.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: Forgiving Threshold Tit-for-Tat (FTFTT)  

Parameters you can tune  
• f_max = 1           ← maximum number of defectors tolerated in the previous round  
• T_punish = 1        ← number of full punishment rounds after intolerable defection  

State variables (reset at start of match)  
• punishment_rounds_left ← 0  

Pseudocode  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Inputs each round t:  
  • t (current round index, 1 ≤ t ≤ r)  
  • history of all players’ actions in rounds 1…t-1  

Action ← C or D  

if t == 1 then  
  # First‐round: lead with cooperation  
  Action ← C  

else if t == r then  
  # Last‐round: defect to avoid being exploited in the final move  
  Action ← D  

else if punishment_rounds_left > 0 then  
  # We are in a punishment phase  
  Action ← D  
  punishment_rounds_left ← punishment_rounds_left − 1  

else  
  # Normal decision mode  
  Let D_prev = number of defectors in round (t − 1)  
  if D_prev ≤ f_max then  
    # Group was sufficiently cooperative last round → cooperate  
    Action ← C  
  else  
    # Too many defectors last round → trigger punishment  
    punishment_rounds_left ← T_punish  
    Action ← D  
  end if  
end if  

Return Action  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

How it works  
1. First round: unconditional cooperate to signal willingness.  
2. Middle rounds (2 … r−1):  
   – If we are currently “punishing,” we defect until the punishment counter runs out.  
   – Otherwise we count how many defectors appeared last round.  
     • If defections ≤ f_max (e.g. only one defector), we forgive and cooperate.  
     • If defections > f_max, we defect for T_punish rounds, then revert to cooperation.  
3. Last round: we defect (standard end-game logic) so that opponents cannot exploit us in t = r.  

Edge cases  
– If the very first round is mis‐coordinated (an opponent defects), we will punish only in round 2, then return to cooperation in round 3.  
– If toward the very end we enter punishment, we still obey “last round defect,” which may shorten the punishment phase, but this is consistent with backward‐induction in the last stage.  
– If the entire group always cooperates, we will cooperate in every round except the last, maximizing joint surplus.  

Cooperative mindset  
• We only defect in response to significant group defection, and even then only briefly.  
• By tolerating up to f_max defectors, we avoid over‐reacting to single mistakes.  
• Quick forgiveness prevents endless cycles of retaliation, allowing cooperation to be restored.
'''

description_COOPERATIVE_17 = '''
Below is a single‐strategy proposal – “Generous Group Tit-for-Tat with Endgame Conditioning” – that aims to sustain cooperation, punish lone defectors briefly, forgive quickly, and guard against last‐round exploitation.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Intuition  
  • Promote full‐group cooperation whenever possible (the socially efficient outcome).  
  • If anyone defects, issue only a single‐round punishment (defect yourself once), then immediately return to cooperation (“forgiving”).  
  • In the very last round, defect only if you have ever been exploited; otherwise cooperate to reward a spotless history.  

2. Parameters  
  • n = number of players  
  • r = total rounds  
  • P = 1 (length of punishment in rounds)  

3. State variables (for your agent)  
  • pun_count ∈ {0,1}: how many remaining punishment rounds you must defect  
  • spotless_history ∈ {True,False}: remains True only if all past rounds were unanimous C  

4. Full‐round pseudocode  

Initialize:  
  pun_count ← 0  
  spotless_history ← True  

For each round t = 1,2,…,r do:  
  if t == 1 then  
    action ← C  
  else if pun_count > 0 then               # we are in punishment mode  
    action ← D  
    pun_count ← pun_count − 1  
  else if t == r then                       # last round  
    if spotless_history then action ← C    # reward a perfect run  
    else                   action ← D      # guard against exploitation  
  else                                       # normal middle rounds  
    if all n players chose C in round t−1 then  
      action ← C                            # full‐group cooperation continues  
    else                                     # someone defected last round  
      action ← D                            # single‐round punishment  
      pun_count ← P                         # schedule exactly P further defects  

  # Update spotless_history based on what everyone did in this round  
  if (anyone’s action this round == D) then spotless_history ← False  

  Play(action)  

End for  

5. Explanation of key points  
  1. First round: cooperate unconditionally to signal goodwill.  
  2. Middle rounds (2…r−1):  
     – If everyone cooperated last round ⇒ cooperate.  
     – If a defection occurred ⇒ defect yourself this round (punishment), then revert.  
  3. Punishment is capped at P=1 round ⇒ you do not get stuck in a death‐spiral.  
  4. spotless_history tracks whether you have ever seen a defection.  
  5. Final round (t=r): defect if anyone has ever defected (to avoid being last‐round–exploited), else cooperate to honor a flawless run.  

6. Cooperative Mindset  
  – You only punish when (and for as long as) someone has defected in the immediately preceding round.  
  – You forgive immediately afterward, restoring full cooperation if your punishment seems to have worked.  
  – You reward a completely cooperative sequence with cooperation even in the last round.  

This strategy yields high average payoffs when matched against other conditional cooperators, deters persistent exploitation, but does not allow a single mistake to poison the entire remainder of the game.
'''

description_COOPERATIVE_18 = '''
Below is a single‐parameter “Threshold-Reciprocal” strategy that (i) starts by cooperating, (ii) retaliates when contributions fall below the level needed for net social benefit, (iii) forgives immediately as soon as others return to cooperation, and (iv) defects in the very last round (since there is no future to protect).

———  
Name: Threshold-Reciprocal Strategy (TRS)  
Parameter:  
 T ← ceil(n/k)   // minimum number of cooperators needed so that k·T/n ≥ 1  
Rounds: t = 1,2,…,r  

Decision Rule for player i at round t:  
1. If t = 1:  
 Action ← C  
2. Else if t = r:  
 Action ← D  
3. Else (1 < t < r):  
 Let c_last ← total number of cooperators observed in round t–1  
 If c_last ≥ T then  
  Action ← C  
 Else  
  Action ← D  

Rationale:  
• T = ceil(n/k) is the smallest group contribution level at which everyone’s share of the public good, (k/n)·T, is ≥1.  Below that threshold, the group return on any one contribution does not even cover the private cost of giving up the endowment.  Thus if others cooperated enough in the last round, you resume cooperating; if not, you withhold cooperation for one round.  
• Punishment is only one round long, immediately forgiven if the threshold is met next round.  
• First‐round cooperation “tests the waters” and invites initial mutual cooperation.  
• Last‐round defection is standard backward‐induction: there is no future to enforce cooperation, so defect.

Pseudocode  
----------  
Input: n (players), k, r (rounds)  
Compute T ← ceil(n/k)  
history ← empty list of past action–profiles  

for t in 1…r do  
 if t == 1 then  
  play C  
 elif t == r then  
  play D  
 else  
  // inspect last round’s total cooperators  
  let last_profile = history[t–2] // zero‐based index  
  c_last = number of C’s in last_profile  
  if c_last ≥ T then  
   play C  
  else  
   play D  
 end if  
 end if  

 // Observe all players’ actions this round and append to history  
 observe profile_t  
 history.append(profile_t)  
end for  

———  
Discussion of properties  
1. Cooperative-minded: TRS immediately rewards sufficiently large cooperation blocs by cooperating next round.  
2. Retaliatory: It punishes a collapse of cooperation (c_last < T) with one round of defection.  
3. Forgiving: As soon as others restore at least T cooperators, TRS switches back to cooperation.  
4. Robust to “lone deviators”: A single defection (or a few) that does not drop c_last below T is absorbed without triggering punishment.  
5. Edge cases:  
 – First round: C (invites cooperation)  
 – Last round: D (no continuation value)  
 – Single‐round punishment only, avoids lock‐in of permanent defection  

TRS therefore fosters high levels of cooperation among similarly inclined opponents, punishes brief breakdowns just enough to deter exploitation, and always returns to cooperation quickly if the group as a whole does.
'''

description_COOPERATIVE_19 = '''
Here is a fully specified cooperative strategy, which we’ll call “Limited-Punishment Tit-for-Tat” (LPTFT).  It combines an initial willingness to cooperate, a mild groupwise “punishment” when defections occur, forgiveness after a short punishment, and a last‐round defection to respect backward induction.

1.  Parameters you choose up front:  
    • punishment_length L (e.g. 2 rounds)  
    • cooperation_threshold m* = n (i.e. insist on full cooperation last round before you will cooperate again)  

2.  State variables (maintained between rounds):  
    • timer (integer ≥ 0), initially 0  
    • last_round_contributors m_prev (integer, undefined until after round 1)  

3.  Decision rules:  
   Round t = 1:  
     – Play C.  
   Rounds t = 2 … r–1:  
     – If timer > 0:  
         • Play D, then decrement timer ← timer – 1.  
         • After observing this round’s contributions m, if m = n, you may reset timer ← 0 (early forgiveness).  
     – Else (timer = 0):  
         • If m_prev = n (i.e. everyone cooperated last round), play C.  
         • Otherwise (somebody defected last round), play D and set timer ← L.  
   Round t = r (the final round):  
     – Play D.  (No future to enforce cooperation.)  

4.  History tracking: at the end of each round t you record m_prev ← total number of cooperators in round t.

5.  Rationale & edge‐case handling:  
   • First round: unqualified cooperation to signal willingness.  
   • Defection‐detection: as soon as any player defects, you “punish” by defecting for L rounds.  
   • Forgiveness: if during your punishment everyone else suddenly returns to full cooperation, you cut the punishment short.  
   • Return to cooperation: after punishment_timer expires, you cooperate again—but only if the last observed round was full cooperation.  
   • Final round defection: ensures you do not leave yourself exploitable on the last move.  

Pseudocode  
-----------  
```
initialize:
  timer = 0
  m_prev = undefined

for t in 1…r:
  if t == 1:
    action = C
  else if t == r:
    action = D
  else if timer > 0:
    action = D
    timer = timer – 1
  else:
    if m_prev == n:
      action = C
    else:
      action = D
      timer = L

  play action
  observe m = number of C’s this round
  if timer > 0 and m == n:
    // everyone cooperated despite punishment → forgive immediately
    timer = 0
  m_prev = m
end for
```

Notes on parameters:  
– L should be small (1–3) so you don’t “over-punish” a single mistake.  
– The threshold m* = n makes you require unanimous cooperation before re-cooperating; you can soften this by setting m* = n–1 if you wish.  

This strategy is firmly cooperative (it starts by cooperating and is quick to forgive), yet it defends against free‐riders by a short, predictable punishment phase. On the last round it defects in line with backward induction.
'''

description_COOPERATIVE_20 = '''
Below is a single‐strategy “template” you can drop into an N‐player public‐goods tournament.  It is a trigger‐style strategy with limited punishment and forgiveness.  It (i) starts by cooperating, (ii) cooperates as long as everyone cooperated last round, and (iii) if it ever observes a defection, it defects for a fixed punishment length L, then forgives and attempts cooperation again.  In this way it (a) rewards mutual cooperation, (b) punishes deviations, and (c) does not get stuck in permanent all‐defect (unless opponents continuously defect).

1.  Parameters you can tune  
   •  L = punishment length (integer ≥1).  A typical choice is L≈r/2 or L=r (the “grim” limit).  
   •  α = cooperation threshold (we choose α=1, i.e. require all n cooperated).  

2.  State variables  
   •  punish_remain ∈ {0,1,…,L}: how many more rounds of punishment are left.  
   •  ever_defected (bool): have we ever seen a defector?  (Optional—only for bookkeeping or statistics.)

3.  Initialization (before round 1)  
   punish_remain ← 0  
   ever_defected ← false  

4.  Decision rule (for each round t = 1…r)  
   Let coop_prev = number of cooperators observed in the immediately preceding round (for t=1 define coop_prev := n).  
   Let rounds_left = r – t + 1.  

   if t==1 then  
     Action ← C  
   else if punish_remain > 0 then  
     // we are in the middle of a punishment phase  
     Action ← D  
     punish_remain ← punish_remain – 1  
   else  
     // not punishing, so decide whether to cooperate or re‐enter punishment  
     if coop_prev ≥ α·n then  
       // “all cooperated last time,” return to cooperation  
       Action ← C  
     else  
       // someone defected last round → punish  
       ever_defected ← true  
       // only punish as many rounds as remain  
       punish_remain ← min(L, rounds_left)  
       Action ← D  
     end if  
   end if  

   // (Optional) override in the very last round  
   if t==r and punish_remain==0 and coop_prev≥α·n then  
     // if we never punished in this last round, go ahead and cooperate  
     Action ← C  
   end if  

5.  Why this is cooperative  
   •  First round you cooperate—and so will everyone else who uses the same logic.  
   •  As long as “everyone cooperated last round,” you keep cooperating.  That supports the socially efficient all-C outcome.  
   •  A single defection triggers a finite punishment cycle of length L; this deters free-riding because you lose the benefit of L future cooperative rounds.  
   •  After punishment you forgive and return to cooperation—so a single mistake does not doom the rest of the game.  

6.  Edge cases  
   •  First round: coop_prev is artificially set to n so you cooperate.  
   •  Last round (t=r): if you are not already in punishment, you still cooperate provided the previous round was full‐cooperate—this maximizes total group payoff at the end.  If you are in punishment, you defect (since that is your commitment).  
   •  If L exceeds the number of rounds left, you simply punish for the remainder of the game.  

7.  Pseudocode summary  

  function DecideAction(t, history) -> {C, D}  
    coop_prev ← (t==1 ? n : countCooperators(history[t–1]))  
    rounds_left ← r – t + 1  
    if t==1 then  
      return C  
    if punish_remain > 0 then  
      punish_remain ← punish_remain – 1  
      return D  
    if coop_prev ≥ α·n then  
      // full cooperation last round  
      return C  
    else  
      // trigger punishment  
      ever_defected ← true  
      punish_remain ← min(L, rounds_left)  
      return D  
    end if  
  end function  

Choose α=1 (require unanimous cooperate) for the strongest incentive, or α<1 (e.g. α=(n–1)/n) if you wish to tolerate a lone “noise” defection.  Likewise, tuning L trades off speed of recovery vs. strength of deterrence.  With this “Conditional‐Cooperate‐&‐Punish” strategy you sustain mutual cooperation when possible but punish and then forgive deviations—embodying a genuinely cooperative mindset.
'''

description_COOPERATIVE_21 = '''
Below is a fully specified “cooperative‐minded” strategy for the repeated n-person public-goods game.  In spirit it is an N‐player generalization of Pavlov (win-stay/lose-shift), with a one‐round “punish‐but-forgive” rule, plus rational defection in the very last round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Overview  
   •  First round: cooperate (C) to signal goodwill.  
   •  Rounds 2 through (r–1):  
       –  If your previous move yielded at least as much payoff as you would have gotten by switching, repeat it (“win‐stay”).  
       –  Otherwise, switch your previous move (“lose‐shift”).  
     This punishes defectors for one round only and then forgives if cooperation returns.  
   •  Last round (t = r): defect (D).  In a known finite horizon, defection is dominant in the final stage.  

2.  Notation  
   let t = current round (1 ≤ t ≤ r)  
   let a_i[t] ∈ {C,D} = your action in round t  
   let H[t] = total number of cooperators in round t (observable at the end of t)  
   let π_i[t] = your realized payoff at the end of t = (1 – c_i[t]) + (k/n)·H[t], where c_i[t]=1 if a_i[t]=C, else 0  

3.  Pseudocode  

   initialize  
     prev_action ← C      // for round 1  
     prev_H ← n           // pretend everyone “cooperated” before round 1  

   for t in 1 to r:  
     if t == 1 then  
       a_i[t] ← C  
     else if t == r then  
       // last‐round rational defection  
       a_i[t] ← D  
     else  
       // compute actual payoff last round  
       if prev_action == C then  
         c_prev ← 1  
       else  
         c_prev ← 0  
       π_prev ← (1 – c_prev) + (k/n) * prev_H  

       // compute hypothetical payoff from switching last round  
       if prev_action == C then  
         // if you had defected instead  
         alt ← 1 + (k/n) * (prev_H – 1)  
       else  
         // if you had cooperated instead  
         alt ← 0 + (k/n) * (prev_H + 1)  

       // win-stay/lose-shift rule  
       if π_prev ≥ alt then  
         a_i[t] ← prev_action      // stay with what worked  
       else  
         a_i[t] ← (prev_action == C ? D : C)  // switch  

     // end if t logic

     // after all actions are chosen and round t is played, observe H[t]  
     prev_action ← a_i[t]  
     prev_H ← H[t]  

   end for  

4.  How this fosters cooperation  
   • “Win‐Stay” means that if cooperating last round earned you as much or more than defecting would have, you keep cooperating.  Likewise for defection.  
   • “Lose‐Shift” ensures that if you or others defect in a way that lowers your payoff, you switch and thus punish—but only for one round.  If your punishment round is sufficiently pro‐cooperative, you revert to cooperation immediately.  
   • By defecting only one round in response to a loss, this strategy reconciles quickly and re-establishes full cooperation when all players return to good behavior.  
   • Defecting in the very last round protects you from end-game exploitation in a finite-horizon setting.  

5.  Edge cases  
   • r = 2:  
       – t=1: cooperate  
       – t=2: defect (by “last‐round” rule)  
   • r = 3:  
       – t=1: C  
       – t=2: (apply Pavlov vs. t=1 payoff)  
       – t=3: D  
   • If everyone cooperates for many rounds, you will stay at C indefinitely (until t = r).  
   • If the group collapses to all-D at any point, you will (by Pavlov) eventually switch back to C once defection stops being rewarding.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

This strategy is  
   – Nice (never the first to defect),  
   – Provocable (punishes defection promptly),  
   – Forgiving (only one round of punishment),  
   – Non-exploitable in the last round (defects when rational).  

That combination has a strong track record of sustaining high cooperation in multiplayer public-goods tournaments.
'''

description_COOPERATIVE_22 = '''
Below is a single‐strategy proposal—called “Proportional Punishment Trigger (PPT)”—that (i) starts fully cooperative, (ii) punishes defectors in proportion to how many defected, and (iii) then returns to cooperation.  It requires keeping track of only one integer (the remaining punishment rounds).

––––––––––––––––––––––––––––––––––––––––––––  
1. State variables  
   • t : current round (1…r)  
   • punish_cnt : integer ≥ 0, number of rounds left in punishment phase  

Initialize at t = 1:  
   punish_cnt ← 0  

––––––––––––––––––––––––––––––––––––––––––––  
2. Decision rule for round t  

if t = r then  
 → Last round: play D  
else if t = 1 then  
 → First round: play C  
else if punish_cnt > 0 then  
 // We are currently punishing  
 play D  
 punish_cnt ← punish_cnt − 1  
else  
 // No active punishment; check last round’s cooperation  
 let coop_prev = Σ₁ⁿ c_j at round t−1  
 if coop_prev = n then  
  // Everyone cooperated last round → reward by cooperating  
  play C  
 else  
  // Some defectors last round → punish them proportionally  
  let defectors = n − coop_prev  
  // Schedule that many punishment rounds (including this one)  
  punish_cnt ← defectors − 1  
  play D  

After action, increment t ← t + 1.  

––––––––––––––––––––––––––––––––––––––––––––  
3. Intuition & cooperative alignment  
• We start fully cooperative to signal good will.  
• If even one player defects, we “punish” by defecting for exactly as many rounds as there were defectors.  
• Once punishment is complete, we forgive and return to cooperation—this keeps the cycle short and focuses on restoring full cooperation.  
• In the last round (t = r), we defect (standard backward‐induction rationale), so earlier punishments can still be carried out if they overlap the final round.  
• Because punishments scale automatically with the size of the breach, defectors know any deviation is met by sufficient, but not endless, retaliation.  
• If all players follow PPT, they quickly learn that any defection costs them proportional future payoff, so the unique stable path is full cooperation every round except the inevitable last‐round defection.  

––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode summary  

```
initialize punish_cnt ← 0
for t in 1…r:
  if t = r:
    action ← D
  else if t = 1:
    action ← C
  else if punish_cnt > 0:
    action ← D
    punish_cnt ← punish_cnt − 1
  else:
    coop_prev ← number of C’s in round t−1
    if coop_prev = n:
      action ← C
    else:
      defectors ← n − coop_prev
      punish_cnt ← defectors − 1
      action ← D
  play(action)
```

––––––––––––––––––––––––––––––––––––––––––––  
This strategy is simple, clearly cooperative in spirit, enforces accountability, and quickly re‐establishes full cooperation after any defection.
'''

description_COOPERATIVE_23 = '''
Below is a single‐player decision‐rule—a “conditional cooperator with one‐round punishment and end‐game defection.”  It is designed to (1) reward full cooperation, (2) punish defections just long enough to deter them, (3) forgive so cooperation can resume, and (4) avoid exploitation in the known final round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
STRATEGY NAME  
   Forgiving Trigger with End‐Game Defection  

OVERVIEW  
   • Start by cooperating.  
   • In each intermediate round (t = 2 … r–1), cooperate if everyone cooperated last round; if anyone defected last round, defect exactly one round in response, then return to cooperation.  
   • In the final round (t = r), always defect.  

PARAMETERS  
   r  = total number of rounds (known)  
   n  = number of players  
   c_j,t ∈ {0,1} = contribution of player j in round t  

STATE VARIABLES  
   punish = 0 or 1  
     punish = 1 means “I am in my one‐round punishment phase.”  
   punish_counter = 0 or 1  
     counts how many punishment rounds remain.  

PSEUDOCODE  

   initialize:  
     punish ← 0  
     punish_counter ← 0  

   for each round t = 1 to r do:  
     
     if t == 1 then  
       action ← C      # first‐round cooperation  
     
     else if t == r then  
       action ← D      # defect in the final round to avoid exploitation  
     
     else  
       if punish == 1 then  
         # I am punishing for a single round  
         action ← D  
         punish_counter ← punish_counter − 1  
         if punish_counter == 0 then  
           punish ← 0    # end punishment, return to cooperative mode  
         end if  
       
       else  
         # Normal mode: check last round’s group behavior  
         total_coop_last ← Σ_{j=1..n} c_j,(t−1)  
         if total_coop_last == n then  
           action ← C    # everyone cooperated last round → reward with C  
         else  
           # at least one defector last round → punish next round  
           punish ← 1  
           punish_counter ← 1  
           action ← D  
         end if  
       end if  
     end if  
     
     play action in round t  
     observe all contributions c_j,t and payoffs  
   end for  

RATIONALE  

1. First Round  
   • Cooperate unconditionally to signal willingness to build the public good.  

2. Intermediate Rounds (2 ≤ t ≤ r−1)  
   • If the entire group cooperated last round, I continue cooperating—this rewards mutual cooperation with the highest group payoff.  
   • If even one player defected, I defect exactly once in response—this lowers the defector’s return enough to make unilateral defection costly, but I do not punish indefinitely.  
   • After that single punishment round, I “forgive” and return to cooperation. This prevents breakdown of cooperation due to noise or accidental defection.  

3. Final Round (t = r)  
   • There is no future in which to punish, so cooperation cannot be enforced. I defect to avoid being exploited in the last round.  

COOPERATIVE MINDSET  
   • Rewards full‐group cooperation (by always cooperating after an all-C round).  
   • Discourages free-riding with a calibrated, one-round penalty.  
   • Forgives promptly so cooperation can re-emerge after mistakes.  
   • Avoids being “suckered” in the known last round by defecting when there is no future.  

This strategy balances strong incentives for mutual cooperation with limited, forgiving punishment—qualities known to sustain high levels of contributions in finitely repeated public‐goods settings.
'''

description_COOPERATIVE_24 = '''
Below is a lightweight “majority‐reciprocity with brief punishment and forgiveness” strategy.  It is designed to (1) start out fully cooperative, (2) reward rounds in which at least a majority of the group cooperated, (3) punish any round in which fewer than a majority cooperated by defecting exactly one round, then forgive, and (4) defect in the last round (since no future remains to sustain cooperation).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: Majority-Reciprocator  
Parameters 
  • n = number of players  
  • r = total rounds  
  • threshold = ⌈n/2⌉ (majority threshold)  
  • pun_duration = 1 (length of punishment)  

State variables  
  • punishing (bool), initially false  
  • pun_timer (int), initially 0  

Decision rules by round t=1…r  
  1. If t == 1:  
       play C  
       continue  
  2. Else if t == r:  
       play D    ← defection in last round  
       continue  
  3. Else (1 < t < r):  
     a. If punishing == true:  
          play D  
          pun_timer ← pun_timer + 1  
          if pun_timer ≥ pun_duration:  
            punishing ← false  
          end  
     b. Else (not punishing):  
          let total_prev = number of cooperators in round t–1  
          if total_prev ≥ threshold:  
            play C         ← reward majority cooperation  
          else:  
            play D         ← punish sub-majority  
            punishing ← true  
            pun_timer ← 0  
          end  
     end  

Pseudocode  
```
initialize punishing = false
initialize pun_timer  = 0
threshold = ceil(n/2)
pun_duration = 1

for t in 1..r:
  if t == 1:
    action[t] = C
    continue

  if t == r:
    action[t] = D
    continue

  # intermediate rounds
  if punishing:
    action[t] = D
    pun_timer += 1
    if pun_timer >= pun_duration:
      punishing = false
  else:
    total_prev = sum_{j=1..n} c_j(t-1)  # how many cooperated last round
    if total_prev >= threshold:
      action[t] = C
    else:
      action[t] = D
      punishing = true
      pun_timer = 0
```

Explanation of key features  
1. First-round cooperation “builds goodwill.”  
2. Reward: if at least a simple majority cooperated last round, we continue cooperating.  
3. Punishment: one round of defection if fewer than a majority cooperated—enough to deter free‐riding but quick to forgive.  
4. Last‐round defection is standard in finite‐horizon repeated games.  

This strategy is fully deterministic, transparent, and aims to sustain high‐payoff cooperation through simple majority‐based reciprocity with minimal punishment.
'''

description_COOPERATIVE_25 = '''
Below is a single‐strategy proposal—“Forgiving Trigger” adapted to the N‐player public‐goods game—that (i) punishes free riders, (ii) quickly forgives small lapses, and (iii) sustains cooperation when possible.  You can tune its two parameters (tolerance T and punishment length M) to your taste; suggested defaults are T=1, M=1.

----------------------------------------------------------------------
1.  Intuition  
   - Start nice (cooperate).  
   - If everyone cooperated last round, keep cooperating.  
   - If a few defected, punish them by defecting for a short, fixed number of rounds.  
   - After punishment, immediately return to cooperation (“forgiving”).  
   - If many defect at once (beyond your tolerance), go into “grim” mode and defect forever.  
   - Works for r>1 and gracefully handles the first and last rounds.  

2.  Parameters  
   • T = tolerance threshold (max # of defectors you’ll forgive)  
   • M = punishment length (how many rounds you defect after a tolerated defection)  
   Suggested: T=1, M=1.  

3.  State variables  
   • pun_counter: integer ≥0, rounds of punishment still to serve  
   • grim: boolean, once true you defect every remaining round  

4.  Strategy pseudocode  

   initialize:  
     pun_counter ← 0  
     grim ← false  

   for t in 1…r do  
     if grim == true then  
       play D  # permanent defection  
       continue  

     if t == 1 then  
       play C  
       continue  

     # t ≥ 2  
     if pun_counter > 0 then  
       play D  
       pun_counter ← pun_counter – 1  
       continue  
     end if  

     # No punishment currently in force  
     let d_prev = number of defectors in round t–1  
     if d_prev == 0 then  
       play C  
     else if d_prev ≤ T then  
       # small lapse—punish briefly  
       pun_counter ← M – 1   # we will defect this round plus M–1 more  
       play D  
     else  
       # too many defectors → grim trigger  
       grim ← true  
       play D  
     end if  
   end for  

----------------------------------------------------------------------  
5.  Explanation of edge cases  
   – First round: we have no history, so we “signal” cooperation by playing C.  
   – When pun_counter>0: we defect exactly the prescribed number of rounds, then automatically revert.  
   – Grim trigger: if at any point the group’s last round had more than T defectors, we never trust the group again.  
   – Last round (t=r): no special‐case needed—your rules already cover it.  If the group has shown itself perfectly cooperative (d_prev=0) and you have no pending punishment, you will cooperate, thereby squeezing any last‐round benefit k/n×#C’s out of the public good.  If you have a pending punishment or are in grim mode, you defect as specified.  

6.  Why is this cooperative?  
   • You begin by cooperating and return to cooperation immediately after punishing minor lapses.  
   • You do not hold infinite grudges for occasional mistakes (forgiveness).  
   • You only resort to permanent defection if the group signals mass defection (beyond your tolerance).  
   • You never exploit cooperators unilaterally—your defections are always tied to observed defection.  

7.  How to tune T and M?  
   • T=1, M=1 is a minimal “tit‐for‐tat” style: you punish a single defector with one round of defection.  
   • Increase M if you think one round of punishment is too weak.  
   • Increase T if you wish to tolerate small coordinated mistakes.  

This strategy conforms to all the specification’s requirements, is easy to implement, and—by combining niceness, punishment, and forgiveness—supports sustained cooperation in a finite N‐player repeated public‐goods game.
'''

description_COOPERATIVE_26 = '''
Below is a simple “conditional‐cooperator” strategy for the n‐player repeated public‐goods game.  It combines a tit‐for‐tat‐style rule at the group level with a one‐round punishment, is fully cooperative when everyone cooperates, punishes any defection, then quickly forgives—and defects in the final round (since no future remains to enforce cooperation).

1.  State variables  
   •  punish_flag ∈ {false, true}, initially false  

2.  Parameters (you may tune these if you like)  
   •  PUNISH_LENGTH = 1    ← how many rounds to defect in punishment phase  

3.  Decision rule (executed each round t = 1…r):  
```
if t == 1:
    # First round: give the benefit of the doubt
    play C
    punish_flag ← false
    punishment_timer ← 0

else if t == r:
    # Last round: defect (no future to punish)
    play D

else if punishment_timer > 0:
    # We are in punishment mode
    play D
    punishment_timer ← punishment_timer - 1
    if punishment_timer == 0:
        punish_flag ← false

else:
    # Normal operation: look at the previous round’s cooperation level
    let coop_count ← number of players (including yourself) who chose C in round t-1

    if coop_count == n:
        # Everybody cooperated last round ⇒ resume/continue cooperation
        play C
    else:
        # At least one defector last round ⇒ punish for exactly PUNISH_LENGTH rounds
        play D
        punish_flag ← true
        punishment_timer ← PUNISH_LENGTH
```

4.  Explanation of key points  
•  “coop_count == n” means everyone (including you) played C in the last round. Only in that case do you cooperate.  
•  As soon as you see any defection, you switch to D for one round (PUNISH_LENGTH=1), then reset and give cooperation another chance.  
•  In round 1 you cooperate unconditionally to signal willingness.  
•  In the final round, you defect because there is no future round in which to impose or receive punishment.  

5.  Why this is “cooperative”  
•  It starts by cooperating.  
•  It fully rewards periods of unanimous cooperation by continuing to cooperate.  
•  It punishes defections, discouraging free‐riding.  
•  Punishment is brief (one round) so the group can quickly return to the high‐payoff cooperative outcome.  
•  It only defects on the very last round when backward‐induction logic would predict defection anyway.  

This strategy is simple to implement, uses only public history, rewards cooperation, punishes defection, and forgives rapidly—thereby sustaining a high level of group cooperation over r − 1 rounds.
'''

description_COOPERATIVE_27 = '''
Below is a self-contained, n-player extension of “Tit-for-Tat” that (1) starts by cooperating, (2) punishes when the group as a whole falls below a cooperation‐threshold, (3) forgives automatically if a majority has already returned to cooperation, and (4) defects in the known last round (the one‐shot defect incentive).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: Generous‐Majority Tit-for-Tat (GM‐TFT)

Parameters (common knowledge):  
• n = number of players (≥ 2)  
• r = total rounds (> 1)  
• k = multiplication factor (1 < k < n)  

Auxiliary constant:  
• T = ⌊n/2⌋ + 1    (strict majority of n)  

Notation:  
• t = current round index, t ∈ {1,…,r}  
• history[t − 1] = the full record of all players’ moves in the previous round  
• coop_prev = number of players who played C in round t − 1  

Decision rule for player i in round t:

1. If t == 1 then  
     play C   (open by cooperating)  
2. Else if t == r then  
     play D   (defect in the last round)  
3. Else  
     let coop_prev = count of C’s in history[t − 1]  
     if coop_prev ≥ T then  
         play C   (majority cooperated last round → cooperate)  
     else  
         play D   (majority defected last round → punish)  

That’s it.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  

```
function decide_action(t, history):
    # Input:
    #   t       : current round (1..r)
    #   history : list of past rounds' moves; history[t-1] is list of n moves
    # Output: 'C' or 'D'
    
    if t == 1:
        return 'C'
    if t == r:
        return 'D'
    
    # count cooperators in the immediately preceding round
    coop_prev = 0
    for move in history[t-1]:
        if move == 'C':
            coop_prev += 1
    
    # T = floor(n/2) + 1  (majority threshold)
    if coop_prev >= T:
        return 'C'
    else:
        return 'D'
```

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Intuition & Cooperative Mindset  
• By opening with C we signal willingness to build the public good.  
• We punish only when a majority of the group has chosen to defect, thereby making the punishment credible—but we do not over‐punish defections by a small minority.  
• Forgiveness is built in: as soon as a majority cooperates in the prior round, we immediately return to C.  
• In the final round we defect (the one‐shot incentive is unavoidable), but until then we sustain cooperation whenever a majority sustains it.  

This strategy is simple to implement, conditions only on the aggregate history (not on hidden communication), and supports high levels of cooperation against similarly generous strategies while still punishing persistent defection.
'''

description_COOPERATIVE_28 = '''
Below is a single‐agent strategy (“Firm‐but‐Fair Trigger”) that aims to sustain cooperation in an n-player repeated public-goods game with r rounds and multiplier k.  It combines an initial cooperative stance, a simple trigger to punish defections, automatic defection in the last round (to avoid end‐game exploitation), and a one‐round “forgiveness” that lets the group recover once it has fully re‐cooperated.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Informal description  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  First round: Cooperate.  
2.  Thereafter (round t = 2, …, r):  
   a.  If t = r (the very last round), defect.  
   b.  Else if in the previous round all players cooperated (i.e. total_cooperators = n), “forgive” and cooperate.  
   c.  Else if we are currently in “good standing” (no active punishment) and last round saw ≥ (n−1) cooperators, cooperate.  
   d.  Otherwise (one or more defections by others), enter punishment mode: defect for exactly one round, then return to good standing.  
3.  This keeps cooperation stable so long as everyone else returns to full cooperation; a single defection triggers only one round of punishment rather than permanent grim trigger.  
4.  By defecting in the last round, we avoid being suckered when no future retaliation is possible.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
2.  Pseudocode  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Parameters:  
 n    number of players  
 r    total rounds  
State variables:  
 punish_mode  ∈ {true,false}, initially false  
 punish_timer ∈ ℕ, initially 0  

At the start of each round t:  
 Inputs: history H of previous rounds’ contributions  
 Let prev_coops = number of cooperators in round t−1 (0 if t=1)  

Decision rule:  
 if t == 1 then  
  action ← “C”  
 else if t == r then  
  # Last‐round defection to avoid end‐game loss  
  action ← “D”  
 else if punish_mode == true then  
  # We are in a punishment‐for‐one‐round state  
  action ← “D”  
  punish_timer ← punish_timer + 1  
  if punish_timer ≥ 1 then  
   # Exit punishment after exactly one round  
   punish_mode ← false  
   punish_timer ← 0  
 else  
  # Good standing: decide based on last round’s level of cooperation  
  if prev_coops ≥ n − 1 then  
   # Almost everyone cooperated → cooperate  
   action ← “C”  
  else  
   # Someone defected → trigger one‐round punishment next round  
   action ← “D”  
   punish_mode ← true  
return action  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
3.  Explanation of key features  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
•  Initial cooperation builds trust.  
•  Defecting in the last round prevents exploitation when no retaliation is possible.  
•  The “n−1” threshold means we only forgive if the group is essentially unanimous, so a single defector is immediately punished.  
•  Punishment lasts exactly one round, then we return to cooperation if the group has re‐cooperated fully.  
•  This is “firm” (punishes defection) but also “fair”/“generous” (allows quick return to cooperation).  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
4.  Handling edge cases  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
•  r=2: Then t=1 → C; t=2 → D.  We get mutual cooperation once and avoid one‐round exploitation.  
•  r=3: t=1→C; t=2→depends on round‐1 history; t=3→D.  
•  If all players adopt this same rule, any accidental defection in round t will be punished in t+1 and then full cooperation resumes in t+2 (unless t+2 is the last).  
•  If others never re‐cooperate, we will defect every round after the first defection sees us penalize them once and then we keep being in punish_mode each time prev_coops < n−1.  

This strategy therefore (i) maximizes group payoff by sustaining cooperation, (ii) retaliates promptly against free‐riders, (iii) forgives after one round so minor mistakes don’t lead to endless breakdown, and (iv) avoids last‐round exploitation.
'''

description_COOPERATIVE_29 = '''
Below is a single‐strategy proposal, “Collective Tit-for-Tat with Finite Punishment and End-game Defense,” that tries to sustain cooperation for as long as possible while protecting itself against exploitation at the end.  It meets all three requirements:

 1.   Specify decision rules  
 2.   Handle edge cases (first round, last round, accidental slip)  
 3.   Be “cooperative” (reward full cooperation, punish defection only briefly, then forgive)

­  
────────────────────────────────────────────────────  
STRATEGY: Collective Tit-for-Tat with Finite Punishment and End-game Defense  

Parameters you may tune:  
•   G = punishment length (in rounds) after observing defection (we suggest G = 1)  
•   E = number of final rounds in which we always defect to avoid end-game exploitation (we suggest E = 1 or 2)  

State variables (persist across rounds):  
•   punish_until = 0   // round index up to which we are currently punishing  

At the start of the game, set punish_until ← 0.  

For each round t = 1, 2, …, r do the following:

 1.  If t > r – E then  
       play D  
     {We refuse to be suckers in the final E rounds.}  

 2.  Else if t = 1 then  
       play C  
     {We open with cooperation.}  

 3.  Else if t ≤ punish_until then  
       play D  
     {We are in a punishment window.}  

 4.  Else  { t > 1, not in endgame, not in punishment }  
       Let m = number of players who played C in round t–1.  
       If m = n then  
         play C  
       Else  
         play D  
         punish_until ← t + G  
         {We saw at least one defector last round; we punish for the next G rounds.}  

────────────────────────────────────────────────────  
Explanation of key features  

1.  “Open‐with‐C” (round 1):  Signals cooperative intent.  
2.  “Collective TFT”:  We only cooperate when we saw unanimous cooperation last round.  A single defector triggers punishment.  
3.  “Finite punishment” (G rounds):  After any defection, we defect for G rounds, then forgive and are ready to resume cooperation if the group does.  This prevents endless downward spirals due to one‐off mistakes.  
4.  “End‐game defense” (last E rounds):  In the final E rounds we always defect, because in a known finite horizon the incentive to defect is overwhelming.  By defecting ourselves we avoid being the only cooperator in the very last rounds.  
5.  “Pseudocode‐ready” for tournament entry.  

You can tweak G and E for more or less forgiveness or a longer end‐game hedge.  With G=1 and E=1 this strategy:

•   Cooperates immediately  
•   Continues to cooperate so long as the group does  
•   Votes D for exactly one round in response to any round with a defection  
•   Forgives after that one‐round punishment  
•   Defects unconditionally in the very last round  

This is widely known to foster high levels of cooperation against many independent strategies, yet protects you from being exploited in the known final rounds.
'''

description_COOPERATIVE_30 = '''
Below is a single‐strategy proposal—call it “One‐Period Punishment with Endgame Defection”—that strives for group cooperation, punishes defection once, then forgives, and handles first and last rounds explicitly.

1.  Overview  
   • Cooperate by default.  
   • If you observe any defection by anyone in round t–1, defect in round t (a single‐round punishment), then immediately return to cooperation.  
   • In the final round, defect (since no future rounds remain to enforce cooperation).  

2.  State Variables  
   last_defect_round ← 0  
     – Stores the most recent round index in which one or more players defected.  

3.  Strategy Pseudocode  

  initialize last_defect_round ← 0  

  for t in 1 … r do  
    if t = 1 then  
      action[t] ← C                        # Round 1: start cooperatively  
    else if t = r then  
      action[t] ← D                        # Last round: defect (no future enforcement)  
    else if t = last_defect_round + 1 then  
      action[t] ← D                        # Punish exactly one period after any defection  
    else  
      action[t] ← C                        # Otherwise, cooperate  

    # (After everyone plays in round t, update the history:)  
    if (# of cooperators in round t) < n then  
      last_defect_round ← t               # Record the round of the latest defection  
    end if  
  end for  

4.  Decision Rules Explained  
  – First round (t=1): Cooperate unconditionally to signal willingness.  
  – Rounds 2 … r–1:  
     • If you are in your one‐round punishment window (t = last_defect_round+1), defect.  
     • Else cooperate.  
  – Last round (t=r): Defect, since no future rounds remain in which you can punish.  

5.  Edge Cases  
  – Multiple defections in a row: You punish only once per defection “event.” If defection spills into your punishment round (so total cooperators < n again), last_defect_round is updated, and you punish once more in the following round—still only one round at a time.  
  – Immediate re‐cooperation: After your punishment round, you return to cooperation unless defections recur.  
  – Final round defections: Since you defect in round r by design, any defection in r–1 simply leads you to defect in r—which is your prescribed move regardless.  

6.  Why It’s Cooperative  
  • By default you cooperate, earning high group payoffs when others do the same.  
  • Punishing only one round tempers exploitation but is light enough to allow rapid reconciliation.  
  • Forgiveness after a single punishment prevents endless retaliation loops.  
  • The strategy deters persistent defection (since each defection triggers an immediate cost to the group) yet continually offers a return path to full cooperation.
'''

description_COOPERATIVE_31 = '''
Here is a simple, fully‐specified “cooperative” strategy we call  
Finite‐Punishment Conditional Cooperator (FPCC).  Its goal is to sustain full‐group cooperation whenever possible, but to impose just enough punishment on free‐riders to deter them.

1.  State variables (per player i)  
    •  punish_timer ← 0    (counts down punishment rounds)  
    •  ever_defected ← false  

2.  Parameters (you can tune these in the tournament)  
    •  p = 2      (punish length in rounds when a defection is observed)  
    •  m = 1      (end‐phase “mercy” window: if we reach last m rounds with zero defection ever, we still cooperate)  

3.  Decision rule at round t (1 ≤ t ≤ r)  
   a.  If t = 1:  
         play C  

   b.  Else if punish_timer > 0:  
         play D  
         punish_timer ← punish_timer − 1  

   c.  Else if t > r − m  (i.e. in the final m rounds):  
         if ever_defected = false  
             play C  
         else  
             play D  

   d.  Else  (normal, non‐punishment, non‐endgame round):  
         look at last round’s actions of all players  
         if every player cooperated in t−1:  
             play C  
         else  
             // someone defected last round  
             ever_defected ← true  
             punish_timer ← p  
             play D  

4.  Bookkeeping (after observing the other n−1 actions this round):  
    if in the current round any player j played D, set ever_defected ← true.  

— — — — — — — —

Explanations / Rationale  
1.  First‐round cooperation “tests the waters.”  
2.  Any defection in round t−1 triggers a fixed‐length punishment of p rounds.  This gives a clear, credible deterrent without “defect forever” (grim‐trigger) harshness.  
3.  After the p‐round punishment ends, we return to cooperation, giving the group a chance to re‐establish full cooperation.  
4.  In the final m rounds, if we’ve never seen a defection to that point, we continue to cooperate (a small “endgame mercy”).  Otherwise, with no future to enforce cooperation, we defect to avoid being exploited.  
5.  ever_defected flag simply lets us know if we are “clean” or “tainted” for endgame decision.  

Pseudocode sketch  
----------------  
initialize punish_timer ← 0  
initialize ever_defected ← false  

for t in 1..r:  
    if t == 1:  
        action ← C  

    else if punish_timer > 0:  
        action ← D  
        punish_timer ← punish_timer − 1  

    else if t > r − m:  
        if ever_defected == false:  
            action ← C  
        else:  
            action ← D  

    else:  
        if (no defections observed in round t−1):  
            action ← C  
        else:  
            ever_defected ← true  
            punish_timer ← p  
            action ← D  

    play(action)  
    observe all players’ actions this round  
    if any observed action == D:  
        ever_defected ← true  

endfor  

Trade‐offs & tuning  
•  p controls how severely we punish.  Larger p makes defection less attractive but risks dragging down payoffs if there was a single mistake.  
•  m controls how “merciful” we are in the very last rounds.  With m=0 we would defect immediately in round r if ever_defected==true; with m>1 we allow a small window of late cooperation if the history was clean.  
•  In setting p and m you balance deterrence (strength of threat) versus vulnerability to noise or accidental defection.  

This strategy is clearly “cooperative”: it starts by cooperating, only defects to punish observed free‐riding, immediately forgives after p rounds, and only switches to permanent defection in the true endgame once it can no longer influence future behavior.
'''

description_COOPERATIVE_32 = '''
Below is a single‐strategy “forgiving trigger” approach that generalizes tit-for-tat to the n-player public‐goods game.  It (1) starts by cooperating, (2) rewards full mutual cooperation, (3) delivers a one-round punishment if anyone defects, then immediately forgives, and (4) defects in the last round to avoid end‐game exploitation.  This strategy is simple, transparent, and highly cooperative.

1.  Intuition  
   - We want to sustain full cooperation because it maximizes group payoff each round (everybody gets k).  
   - If someone defects, we briefly punish by defecting once—enough to deter one-off free‐riding—then we return to cooperation.  
   - In the final round (round r), standard backward‐induction says to defect, since there is no future to preserve.  

2.  Decision rules  
   Let t = current round (1 ≤ t ≤ r).  Let last_allC = true if in round t–1 every player chose C; false otherwise.  We also keep a one–round flag just_punished that tracks whether our previous move was that punishment.

   Pseudocode:  
     initialize  
       just_punished ← false  

     for t from 1 to r do  
       if t == 1 then  
         action_t ← C        # Round 1: always cooperate  
         just_punished ← false  

       else if t == r then  
         action_t ← D        # Last round: defect  

       else if just_punished then  
         action_t ← C        # Forgive after punishing one round  
         just_punished ← false  

       else if last_allC then  
         action_t ← C        # Reward full cooperation last round  

       else  
         action_t ← D        # Punish defectors  
         just_punished ← true  

       end if  

       # At the end of round t:  
       #   1) observe all players’ moves this round, set last_allC = (# of C’s == n)  
       #   2) proceed to next round  
     end for  

3.  Handling edge cases  
   • First round: no history ⇒ cooperate.  
   • Punishment is exactly one round, then automatic return to cooperation—this avoids endless cycles of retaliation.  
   • Last round (t = r): defect, because there is no future benefit from sustaining cooperation.  

4.  Why this is cooperative  
   – It always seeks full cooperation at the group level.  
   – It never “grimly” punishes forever; it punishes just enough to discourage one‐shot defections.  
   – It is transparent and easy for others to detect and respond to, which promotes stable mutual cooperation.  
   – Against fellow cooperators it achieves the maximum group payoff each round; against defectors it quickly recovers cooperation once the poor behavior has been penalized.
'''

description_COOPERATIVE_33 = '''
Below is a concise description of a simple, robust “forgiving‐Tit-for-Tat” style strategy for the n-player repeated public‐goods game.  It (a) starts by cooperating, (b) punishes any defection but only for one round, then forgives, and (c) defects in the very last round (the standard end‐game “unravelling” move).

1.  State variables  
    •  t: current round, t=1,…,r  
    •  PunishRoundsRemaining (integer ≥0), initialized to 0  

2.  Parameter  
    •  r = total number of rounds  

3.  Decision rule at the start of each round t:  
    if t == r then  
      play D   # last-round defection  
    else if t == 1 then  
      play C   # open with cooperation  
    else if PunishRoundsRemaining > 0 then  
      play D  
      PunishRoundsRemaining ← PunishRoundsRemaining − 1  
    else  
      look at last round’s contributions  
      if “any player defected in round t–1” then  
        # trigger exactly one round of punishment  
        play D  
        PunishRoundsRemaining ← 0    # we already punish this round  
      else  
        play C  

4.  Updating after observing round t actions (for logging only)  
    After all actions in round t are revealed, you may record  
      LastRoundHadDefection ← (∑_i c_i[t] < n)  
    but the code above already captures that via your PunishRoundsRemaining logic.  

5.  Explanation & properties  
  •  First‐round cooperation signals your willingness to build the public good.  
  •  If everyone cooperated in round t–1, you cooperate again in t.  
  •  If you ever observe a defector in t–1, you defect exactly in round t as punishment, then return to cooperation.  
  •  The single‐round punishment prevents endless mutual defection and restores full cooperation quickly.  
  •  In round r you defect (standard backward-induction endgame defect).  

6.  Edge cases handled  
  •  t=1: cooperates by definition.  
  •  t=r: defects irrespective of history.  
  •  Single‐round punish ensures you never “over‐punish” or get trapped in mutual defection.  
  •  If a defection occurs at t=r–1, you punish at t=r–1+1=r, but the rule “t==r → D” already enforces your defection.  

7.  Pseudocode summary  
```
Initialize PunishRoundsRemaining ← 0

for t in 1…r do
  if t == r:
    action ← D
  else if t == 1:
    action ← C
  else if PunishRoundsRemaining > 0:
    action ← D
    PunishRoundsRemaining ← PunishRoundsRemaining − 1
  else 
    if any opponent played D in round t−1 then
      action ← D
      # punish exactly one round
      PunishRoundsRemaining ← 0
    else
      action ← C
  end if

  execute action; observe all players’ moves this round
  # (for bookkeeping) record whether any D occurred this round
end for
```  

This strategy is cooperative—it seeks and quickly restores full‐group cooperation—and simple enough to implement in a tournament against unknown opponents.
'''

description_COOPERATIVE_34 = '''
Below is a simple yet robust “tit-for-tat with finite punishment” strategy for the repeated n-player public-goods game.  It is designed to:

•	Discourage unilateral defection by punishing it  
•	Forgive after a short, pre-specified punishment phase so cooperation can resume  
•	Work without any off-path signalling or communication  
•	Be easy to implement in pseudocode  

################################################################################  
1.  STRATEGY OVERVIEW  
################################################################################  

1.1  Intuition  
–  Start by cooperating.  
–  If in the previous round at least one player defected, punish the entire group by defecting for the next P rounds.  
–  After P rounds of punishment, give cooperation another chance.  
–  Repeat: every time you observe defection, trigger a new P-round punishment.  

This “finite punishment” rule makes defection unattractive (because it costs you P lower payoffs) but does not turn into an endless grim-trigger.  It thus supports high cooperation rates without permanently locking the group into mutual defection.  

1.2  Choice of P  
–  P is a small integer ≥1.  Typical choices are P=1 or 2.  
–  P=1 reduces to pure tit-for-tat (punish one round).  
–  P=2 gives a slightly stronger deterrent at the cost of a longer disruption.  

You can tune P based on how severely you wish to punish defections.  

################################################################################  
2.  DECISION RULES  
################################################################################  

Let r be the total number of rounds.  
Let P be your punishment length (e.g. P=2).  

State variables (kept from round to round):  
– punish_until  (integer round index up to which you must defect)  

Initialize:  
– punish_until ← 0  

For each round t = 1,2,…,r do:  
  if t = 1 then  
    play C  // always cooperate in the first round  
  else if t ≤ punish_until then  
    play D  // still punishing  
  else  
    if “there was at least one D by someone in round (t–1)” then  
      // trigger a new punishment  
      punish_until ← min(r, t + P – 1)  
      play D  
    else  
      // previous round was all-C, so resume cooperation  
      play C  
    end if  
  end if  

################################################################################  
3.  HANDLING EDGE CASES  
################################################################################  

3.1  First round (t=1)  
– Action: C.  You have no history, so begin cooperatively.  

3.2  Overlapping punishments  
– If you observe new defections while already in a punishment phase, you extend punish_until.  
  Example: P=2, a defection in round 3 sets punish_until=4; if you see another defection in 4, you reset punish_until=5.  

3.3  Last round (t=r)  
– The same rule applies.  If you are still in a punishment window, you defect; otherwise your action depends on whether round r–1 was all-C.  
– This may mean you still punish in the final round—but that is a conscious choice to maintain credibility of your punishments.  

3.4  No-communication, no-coordination  
– You only condition on the publicly observable history of cooperators vs. defectors.  
– No extra assumptions about side-agreements or off-path signalling.  

################################################################################  
4.  WHY THIS STRATEGY IS COOPERATIVE  
################################################################################  

•	It begins with full cooperation.  
•	It immediately punishes defections, making unilateral defection unprofitable over the long run.  
•	It forgives after a finite P rounds, allowing the group to return to mutual cooperation even if mistakes or brief attacks occur.  
•	It is transparent and symmetric: every player using this strategy will stabilize on all-C if no one defects.  

Over many repetitions, rational opponents learn that defection merely invites a short downturn in payoffs, whereas cooperation maximizes collective and individual returns.  

################################################################################  
5.  PSEUDOCODE SUMMARY  
################################################################################  

Parameters:  
 r  ← total rounds  
 P  ← punishment length (e.g. 2)  

State:  
 punish_until ← 0  

For t in 1…r:  
 if t == 1:  
  action ← C  
 else if t ≤ punish_until:  
  action ← D  
 else:  
  if any player chose D in round t–1:  
   punish_until ← min(r, t + P – 1)  
   action ← D  
  else:  
   action ← C  
  end if  
 end if  

Return action for round t  

################################################################################  

This “finite‐punishment tit-for-tat” is simple to implement, robust against one‐shot or repeated deviations, and highly promotes sustained cooperation in the public‐goods setting.
'''

description_COOPERATIVE_35 = '''
Below is a self-contained, easy-to-implement “N-Player Tit-for-Tat” style strategy with a one-round punishment and clear edge-case rules.  It is fully cooperative (it starts by cooperating, resumes cooperation after forgiving a single defection) but protects itself against persistent free-riding.    

## 1. High-Level Description  
1. First round: always cooperate.  
2. In rounds 2 through r–1:  
   – If in the immediately preceding round every player cooperated, then cooperate.  
   – Otherwise (i.e. you saw at least one defection last round), punish by defecting this round.  
   – After punishing for one round, automatically resume cooperation unless you again see defection.  
3. Last round (round r): defect (standard backward-induction exploitation of the one-shot game).  

This rule set:  
• Is fully symmetric (you treat everybody’s defection alike).  
• Forgives after a single punishment round so it does not lock into permanent defection.  
• Strongly rewards unanimous cooperation.  
• Defects in the last round to avoid being exploited when there is no future.  

## 2. Pseudocode  

Let history[t][i] ∈ {C, D} be player i’s action in round t (once observed).  
Initialize:  
 state.punish = false  

For each round t = 1 … r do  
 if t == 1 then  
  action ← C                    # Start by cooperating  
 elif t == r then  
  action ← D                    # Last-round defection  
 else  
  if state.punish == true then  
   # Punishment round  
   action ← D                  
   state.punish ← false        # Forgive after one round  
  else  
   # Look at what happened in round t–1  
   let prev = {history[t–1][j] for j=1…n}  
   if ∀j ∈ 1…n: prev[j] == C then  
    action ← C                # Everyone cooperated last round  
   else  
    action ← D                # Punish this round  
    state.punish ← true       # Flag one-round punishment  
   end if  
  end if  
 end if  

 # Play action; afterward record it in history[t][you]  

end for  

## 3. How It Fulfills the Requirements  
1. Decision rule is fully specified for every t: first, middle, and last round.  
2. Cooperates initially to signal goodwill.  
3. Only defects in the middle game when it has observed free-riding, and then only for one round (minimum necessary punishment).  
4. Always defects in the terminal round to avoid the sucker’s payoff when there is no future.  
5. By forgiving after one round, it allows the group to re-establish full cooperation quickly.  

This strategy is easy to code, needs only the last round’s action profile, and balances strong cooperation with self-protection.
'''

description_COOPERATIVE_36 = '''
Below is a single‐strategy description—called “Forgiving Trigger with End-Game Defection”—that meets all your requirements.  It starts fully cooperative, punishes any defection for exactly one round, then forgives, and in the final round defects (to avoid the unavoidable end-game incentive to free‐ride).

1.  Data structures / state  
    •  punishing : Boolean flag (initially false)  
    •  last_contributions : integer in [0..n] (number of C’s in the previous round; undefined in round 1)  

2.  Parameters  
    •  L = 1   (length of punishment in rounds)  
    •  r       (total number of rounds)  
    •  n       (number of players)  

3.  Decision rule (pseudocode)  
```
for round t = 1 to r:
    if t == 1:
        action ← C                     # Always start by cooperating
    else if t == r:
        action ← D                     # End‐game defection
    else if punishing == true:
        action ← D
        punishing ← false             # Punish exactly one round, then reset
    else:
        # t in {2, …, r-1} and not currently punishing
        if last_contributions == n:
            action ← C                # Everyone cooperated last round ⇒ reward with C
        else:
            action ← D                # Someone defected last round ⇒ punish now
            punishing ← true         # Set flag so that next round is punishment as well
    end if

    play action
    observe contributions of all players this round ⇒ last_contributions
end for
```

4.  Explanation of key points  
  •  First round:  By playing C initially, we demonstrate goodwill.  
  •  Punishment:  The moment we see fewer than n contributions (i.e. at least one defection), we defect immediately and set `punishing=true`.  That means one more round of defection follows (because in the next iteration `punishing==true`), for a total punishment of exactly L=1 round beyond the immediate defection.  
  •  Forgiveness:  After that single extra defection round, we reset `punishing=false` and return to cooperation as soon as we again observe full cooperation among the group.  
  •  End‐game:  In round t=r we defect unconditionally.  This is the standard backward‐induction pull in finitely repeated games.  

5.  Why it is cooperative  
  •  It never throws away cooperation unless provoked by an observed defection.  
  •  Punishment is brief—only one extra round—limiting the damage to overall group payoff.  
  •  By forgiving after punishment, it restores trust and supports the potential for sustained high contributions.  
  •  Yet it still enforces accountability, deterring free‐riders.  

This strategy thus balances strong cooperation, clear deterrence of defection, limited collateral damage, and the inevitable last‐round defection.
'''

description_COOPERATIVE_37 = '''
Below is a simple, fully‐specified “cooperative” strategy for the n‐player repeated public‐goods game.  It is in the spirit of Tit-for-Tat extended to many players, but with a one‐round punishment and automatic forgiveness so that cooperation can be re-established even after mistakes or occasional defection.

1.  High‐Level Description  
    •  Start by cooperating.  
    •  Cooperate as long as everyone cooperated in the previous round.  
    •  If you observe any defection by any player in round t–1, punish by defecting exactly once in round t, then automatically return to cooperation in round t+1.  
    •  Always defect in the very last round (round r), since backward induction dictates no future punishment is possible.  

   This strategy is  
    –  Cooperative: it rewards full cooperation immediately,  
    –  Retaliatory: it punishes any defection,  
    –  Forgiving: punishment lasts exactly one round, so cooperation can resume,  
    –  Robust: it never locks into permanent defection after an error,  
    –  Time‐consistent: it defects in the final round when no threat of future punishment exists.

2.  Pseudocode

    Parameters known to the strategy: n, r.  
    Observe in each round t the vector of actions a^(t–1) = (c_1,…,c_n) from the previous round.

    State variable:
       punish_flag ∈ {false, true}  
       Initially: punish_flag ← false

    For t from 1 to r do
      if t == 1 then
        // First round: unconditionally cooperate
        action_i ← C
        punish_flag ← false
      else if t == r then
        // Last round: defect (no future retaliation possible)
        action_i ← D
        // punish_flag doesn’t matter any more
      else
        if punish_flag == true then
          // We are in our one‐round punishment
          action_i ← D
          punish_flag ← false        // reset punish
        else
          // Check whether anyone defected last round
          let num_cooperators = Σ_{j=1..n} c_j^(t–1)
          if num_cooperators < n then
            // At least one defection observed
            action_i ← D
            punish_flag ← true         // trigger one‐round punishment
          else
            // Everyone cooperated last round
            action_i ← C
            // punish_flag remains false
          end if
        end if
      end if

      play action_i in round t
    end for

3.  Explanation of Key Features

  •  “First‐move cooperate” sends a clear signal of willingness to build the public good.  
  •  “One‐round punishment” (punish_flag) ensures that any defection by any player is met with immediate retaliation, making defection unprofitable in expectation.  
  •  “Automatic forgiveness” after exactly one round prevents eternal breakdown of cooperation due to noise or a single mistake.  
  •  “Defect in the last round” is necessary under standard finite-horizon reasoning: without a future threat, cooperation cannot be enforced, so you switch to the short‐term best reply.  

4.  Handling Edge Cases

  –  If two or more players defect simultaneously, you still punish only one round.  
  –  If multiple defections occur in consecutive rounds, you punish each by a single D in the next round, but you never punish more than one round per observed defection.  
  –  If you or others accidentally “mis‐click” a C when you meant D (or vice versa), the one‐round punishment/forgiveness mechanism allows recovery.  
  –  If r=2, the algorithm cooperates in round 1 and defects in round 2 (the only viable threat‐based enforcement).  

5.  Why This Is Cooperative

  –  It achieves mutual cooperation in all rounds t=1,…,r–1 whenever no one defects.  
  –  The expected payoff per round for full cooperation is (k/n)·n = k > 1, exceeding the guaranteed 1 from full defection.  
  –  By punishing deviations just enough to deter them, it steers the group to sustain the superior cooperative equilibrium in all but the last round.
'''

description_COOPERATIVE_38 = '''
Below is a fully specified “forgiving‐trigger” strategy.  It is cooperative, starts by contributing, punishes any defection with exactly one round of defection, then immediately returns to cooperation.  In the final round it defects (end‐game) to protect itself from exploitation.

1. State variables  
   punish_count ← 0   // how many more rounds we must punish

2. Parameter  
   MAX_PUNISH ← 1     // length of punishment for any defection

3. Pseudocode  
   for t in 1…r do  
     if t == 1 then  
       play C    // round 1: always cooperate  
     else if t == r then  
       play D    // final round: defect (standard end‐game logic)  
     else  
       if punish_count > 0 then  
         play D  
         punish_count ← punish_count – 1  
       else  
         // inspect last round’s history  
         let defectors ← number of players j with action D in round t–1  
         if defectors > 0 then  
           // someone defected last round → punish for next MAX_PUNISH rounds  
           punish_count ← MAX_PUNISH  
           play D  
         else  
           // no defection last round → cooperate  
           play C  
         end if  
       end if  
     end if  
   end for

4. Explanation of decision rules  
 • First round: play C to signal full cooperation.  
 • Rounds 2…r–1:  
   – If in “punishment mode” (punish_count>0), keep defecting until punish_count runs out.  
   – Otherwise, look at round t–1:  
     • If nobody defected then cooperate.  
     • If any defection occurred then defect this round and set punish_count=MAX_PUNISH (one round).  
 • Last round (t=r): always defect to avoid being exploited in the known end‐game.

5. Why this is cooperative  
 – It starts by cooperating.  
 – It only punishes actual defections (no “preemptive” defections).  
 – It forgives immediately after one round of punishment, restoring cooperation if opponents return to C.  
 – It avoids the “death spiral” of grim–trigger while still deterring free‐riding.  

6. Edge cases  
 – Single defection in early play triggers exactly one round of defection, then returns to full cooperation.  
 – Multiple players defecting in the same round still only cost them one round of collective punishment.  
 – In the final round, defecting is optimal once cooperation can no longer be enforced in future play.
'''

description_COOPERATIVE_39 = '''
Below is a single‐strategy proposal we’ll call “Group-Tit-for-Tat with Last-Round Defection.”  It is simple, provably cooperative (it steadily rewards full cooperation), punishes defections promptly, then forgives, and handles first and last rounds explicitly.

1. State variables  
   • last_outcomes[t–1]: the set of actions {C or D} chosen by all n players in the previous round  
   • r: total number of rounds  
   • t: index of the current round (1…r)  

2. Decision rules  

   Round 1 (t = 1):  
     – No history to observe → play C (Cooperate).  
   
   Intermediate rounds (1 < t < r):  
     – If in the immediately preceding round every player cooperated (|last_outcomes[t–1]| = {C}):  
         play C.  
     – Otherwise (at least one defection seen in t–1):  
         play D (Defect) to punish free-rider(s), but only for this one round.  
         On the next round, you will check history again and forgive if full cooperation returned.  
   
   Last round (t = r):  
     – Defection is a dominant strategy—no future punishments are possible—so play D.  

3. Why this is cooperative  
   – It always opens with cooperation.  
   – It rewards full cooperation by continuing to cooperate.  
   – A single defection by any player triggers exactly one round of group-wide punishment and then immediate forgiveness if everyone subsequently returns to C.  
   – Because punishments are neither too harsh (they last only one round) nor too lenient (they occur at all),-minded opponents learn that sustained cooperation maximizes payoffs.  
   – It defects in the last round only because there is no future incentive structure; this is the only time it departs from cooperation.  

4. Pseudocode  

   initialize t = 1  
   for t in 1…r do  
     if t = 1 then  
       action_i[t] ← C  
     else if t = r then  
       action_i[t] ← D  
     else  
       if ∀­j : last_outcomes[t–1][j] = C then  
         action_i[t] ← C  
       else  
         action_i[t] ← D  
       end if  
     end if  
     play action_i[t]  
     observe last_outcomes[t] (everybody’s actions)  
   end for  

5. Extensions & edge cases  
   – If two or more players punctuate cooperation by defecting repeatedly, this strategy will retaliate each time (one defection → one round of D).  If defectors persist, you will continue to defect until you observe a clean slate.  
   – In a purely cooperative group, this settles into perpetual C until the final round.  
   – If opponents happen to cooperate even in the last round, you miss the extra payoff from mutual C, but you avoid exploitation risk—it’s the price of rationality in a finitely repeated game.  

This strategy balances an unambiguous cooperative stance with a clear, bounded punishment that encourages opponents to return quickly to mutual cooperation.
'''

description_COOPERATIVE_40 = '''
Below is a single‐strategy design that (i) “tries” to sustain full cooperation, (ii) punishes defections just long enough to discourage free‐riding, (iii) never punishes cooperators indefinitely (forgives), and (iv) recognizes that in a finite‐horizon game the very last round must be defection.

1. Informal description  
   a. Round 1: Cooperate.  
   b. Rounds 2…r−1:  
      – If in the preceding round everyone cooperated, cooperate.  
      – If you observed at least one defection in the preceding round, defect for exactly one round (punishment), then return to cooperation if the last round’s contributions are again full.  
   c. Round r (last round): Defect.  
   This is a “one‐round punishment” version of Tit-for-Tat with occasional forgiveness and a terminal defection.

2. Why it is cooperative  
   – It starts by cooperating.  
   – It only defects to punish observed defection—and then forgives after one round if others return to cooperating.  
   – By punishing, it makes unilateral defection costly, sustaining cooperation when opponents value future payoffs.  
   – It defects in the last round only because backward induction makes cooperation there non‐credible.

3. Pseudocode  
   ```
   strategy PublicGoodsOneRoundPunish(n, k, r):
     // State variable
     punish_remaining ← 0

     for t from 1 to r do
       if t == 1 then
         action[t] ← C
       else if t == r then
         // Last‐round defection is inevitable in finite horizon
         action[t] ← D
       else if punish_remaining > 0 then
         // We are in a punishment phase
         action[t] ← D
         punish_remaining ← punish_remaining - 1
       else
         // Examine last round’s contributions
         coopers_last ← number of C's in history at round t-1
         if coopers_last == n then
           // Everyone cooperated last round → cooperate
           action[t] ← C
         else
           // Someone defected → trigger one‐round punishment
           action[t] ← D
           punish_remaining ← 1
         end if
       end if
     end for

     return action[1..r]
   ```

4. Edge‐case handling  
   – First round: no history → cooperate to signal goodwill.  
   – Punishment length is exactly one round, so you never get stuck in endless retaliation if the group returns to cooperating.  
   – Last round r: guaranteed defection to avoid being exploited by backward induction.  

5. Expected behavior  
   – If all players adopt this, they will produce full cooperation every round 1…r−1 and switch to mutual defection in round r.  
   – If a single player defects in round t<r, all others defect in t+1 (punishment), then resume cooperation from t+2 onward if no further defections occur.  
   – Cooperators never suffer unending punishment, so genuine cooperators recover quickly.  

This strategy is simple, clear, and aligns incentives toward mutual cooperation while respecting the unavoidable end‐game defection.
'''

description_COOPERATIVE_41 = '''
Below is a single‐agent strategy (“Collective Tit-for-Tat with Limited Punishment and End-Game Defection”) that seeks to sustain full cooperation most of the way, punishes free-riders just enough to deter them, then returns to cooperation, and finally defects in the last round to capture any unilateral gain at the very end.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Intuition  
   • We begin by cooperating.  
   • Whenever anyone defects, we defect exactly one round as “punishment” and then immediately forgive—this keeps punishments short and avoids spirals of mutual defection.  
   • If the previous round saw unanimous cooperation, we cooperate again.  
   • In the known final round (t = r), we defect to exploit any last-round cooperators.  

This “one-shot punishment + quick forgiveness” fosters and stabilizes cooperation against a wide class of strategies—so long as others know that a lone defection will trigger an immediate but brief group response.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
2. Pseudocode  

Let r = total rounds, t = current round (1 ≤ t ≤ r).  
Maintain a single integer state variable PunishTimer, initially 0.  
Maintain access to history of contributions so you can check, for any past round s, whether any player defected (i.e. Σ_j c_j < n).

For each round t do:

  if t == 1 then  
    action ← C  
    PunishTimer ← 0  

  else if t == r then  
    /* Final‐round defection to capture extra private payoff */  
    action ← D  

  else  
    if PunishTimer > 0 then  
      /* We are in punishment mode */  
      action ← D  
      PunishTimer ← PunishTimer − 1  

    else  
      /* No active punishment—check last round */  
      let coop_last = (number of cooperators in round t−1)  
      if coop_last == n then  
        /* Everyone cooperated last round — resume cooperation */  
        action ← C  
      else  
        /* Someone defected last round — punish exactly one round */  
        action ← D  
        PunishTimer ← 1  
      end if  
    end if  
  end if  

Submit action.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
3. Explanation of Key Cases  

• First round (t=1): Cooperate unconditionally to signal willingness.  
• Normal rounds (1 < t < r):  
  – If we are “in punishment” (PunishTimer>0), we defect once then decrement the timer.  
  – Otherwise we look back one round:  
     • If *everyone* cooperated → we cooperate.  
     • If *anyone* defected → we defect this round and set PunishTimer=1 so that next round we return to cooperation.  
• Last round (t=r): Defect no matter what, to extract the extra private payoff when others might still cooperate.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
4. Why This Is Cooperative  

– It rewards full‐cooperation by continuing to cooperate whenever history is “clean.”  
– It deters single defections by imposing a guaranteed one‐round group defection—enough to make defection costly when averaged over many rounds.  
– It never escalates punishments beyond one round, so trust can be re-established quickly.  
– It is fully deterministic, transparent, and uses only publicly observable history—no hidden moves or randomization needed.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
5. Possible Variations / Tuning  

– PunishTimer ← k for k>1 if you wish harsher punishment.  
– One could choose to *not* defect in the final round (t=r) if your goal is purely maximal group payoff at the expense of personal gain—but standard PD logic leads us to defect.  
– You can generalize the rule “someone defected → punish” to “fewer than T cooperators → punish” if you want to target mass defection differently.  

This strategy strikes a balance between strong deterrence of free-riding and rapid forgiveness, thereby sustaining high cooperation rates throughout the repeated public goods provision.
'''

description_COOPERATIVE_42 = '''
Below is a simple, transparent “multi‐player Tit-for-Tat with one‐shot punishment and forgiveness” that (i) starts by cooperating, (ii) punishes any defection by any player for exactly one round, (iii) then immediately returns to cooperation, and (iv) defects in the final round (since no future to protect).  It requires no secret signals or pre-coordination—only the public history of contributions.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy “1-Round Punish-and-Forgive TFT”  
State: none beyond remembering your own last move (C or D).

Pseudocode (for player i):  
  initialize nothing special  

  for t = 1…r:  
    if t == 1:  
      action_i(t) = C  
      continue  

    if t == r:  
      action_i(t) = D        # final‐round defection (no future)  
      continue  

    # otherwise 1 < t < r  
    let total_C = Σ_{j=1 to n} c_j(t–1)   # count of cooperators in last round  
    if total_C == n:  
      # full cooperation last round → stay cooperative  
      action_i(t) = C  
    else:  
      # someone defected last round  
      if c_i(t–1) == 1:  
        # you were “suckered” (you cooperated but others didn’t) → punish once  
        action_i(t) = D  
      else:  
        # you defected last round (you already punished) → forgive and return to C  
        action_i(t) = C  

End for  

Description of key pieces:  
1. First round (t=1): Cooperate.  
2. Full-cooperation trigger: If everyone contributed in the previous round, keep cooperating.  
3. One-shot punishment: If you contributed but at least one other player defected last round, defect this round (a one‐round response).  
4. Immediate forgiveness: If you defected last round (i.e. you already carried out the punishment), switch back to cooperation.  
5. Last round (t=r): Defect—there is no future, so no incentive to cooperate.  

Why this is cooperative:  
- It rewards unanimous cooperation by always returning to C.  
- It punishes defection only long enough to be noticed (exactly one round), minimizing wasted rounds.  
- It never punishes more severely or longer than necessary, which helps restore trust quickly.  
- By cooperating whenever possible (except the last‐round inevitable defection), it sustains high contributions against any strategy that reciprocates cooperation.  

Edge cases handled:  
- r=2: You play C in round 1, then (inevitably) D in round 2.  
- Near the end (t=r–1): You still apply the same rule—if round r–2 was all C, you cooperate in r–1; otherwise you punish once; and then round r you defect.  
- Multiple simultaneous defectors: Any defection by any player triggers the same one‐round retaliation by you (if you were cooperating), no matter how many defected.  

This strategy is easy to implement, transparent to opponents (they can read off your rules from the history), and strongly promotes mutual cooperation in the early and middle rounds, while keeping punishments short enough to allow rapid recovery.
'''

description_COOPERATIVE_43 = '''
Below is a simple, fully specified “reciprocal‐cooperator” that (i) starts by cooperating, (ii) punishes any defection by defecting for a short, fixed window, then (iii) forgives and returns to cooperation, and (iv) always defects in the last round (the known end‐game).

───────────────────────────────────────────────────────────────────  
1.  “Reciprocal Cooperator with 1‐Round Punishment”  
───────────────────────────────────────────────────────────────────  

PARAMETERS (you may tune L, the punishment length):  
•  L = 1   (length of punishment after observing any defection)  

STATE VARIABLES:  
•  punish_timer ← 0   (counts down remaining punishment rounds)  

ALGORITHM (for player i):  
For each round t = 1,2,…,r:  
  if t = 1 then  
    // First round: build trust  
    play C (c_i = 1)  
  
  else if t = r then  
    // Last round: backward‐induce defection  
    play D (c_i = 0)  

  else if punish_timer > 0 then  
    // We are in the middle of a punishment phase  
    play D (c_i = 0)  
    punish_timer ← punish_timer – 1  

  else  
    // We're “in good standing” and not in the last round  
    let total_cooperators_last ← Σ_j c_j^(t–1)  
    if total_cooperators_last = n then  
      // Everyone cooperated last time → reward with cooperation  
      play C (c_i = 1)  
    else  
      // Someone defected last time → punish for L rounds  
      play D (c_i = 0)  
      punish_timer ← L  



───────────────────────────────────────────────────────────────────  
2.  Explanation of Decision Rules  
───────────────────────────────────────────────────────────────────  
•  First round (t=1): cooperate.  
•  Intermediate rounds (2 ≤ t ≤ r–1):  
   –  If we’re currently punishing (punish_timer>0), continue to defect until the timer expires.  
   –  Otherwise, look at the previous round’s aggregate contributions:  
      •  If everyone cooperated last round, cooperate.  
      •  If at least one defection occurred, defect now and set punish_timer = L (punish the group for L rounds).  
•  Last round (t=r): defect unconditionally (standard end‐game defection).  

───────────────────────────────────────────────────────────────────  
3.  Handling Edge Cases  
───────────────────────────────────────────────────────────────────  
–  If a defection occurs during a punishment phase, we do not extend the punishment further (this avoids runaway escalation).  
–  If a punishment phase overlaps into the final round, the rule “defect in last round” takes precedence.  
–  If r is very small (e.g. r=2 or 3), punish_timer may never fully be used—but even one round of guaranteed punishment deters single‐round gains from defection.  

───────────────────────────────────────────────────────────────────  
4.  Why This Is Cooperative  
───────────────────────────────────────────────────────────────────  
•  It starts by offering cooperation unconditionally—building trust.  
•  It only defects in direct response to observed defection, so it rewards cooperators and punishes free‐riders.  
•  Punishment is finite and brief (L=1), so accidental or sporadic mistakes don’t spiral into permanent mutual defection.  
•  By forgiving quickly, it re‐establishes full cooperation when others return to contributing.  
•  The final‐round defection is unavoidable (common‐knowledge end‐game), but up to t=r–1 it sustains cooperation whenever possible.  

This strategy has all the hallmarks of a successful cooperative rule in public‐goods tournaments: it is clear, retaliatory yet forgiving, and it internalizes the known end‐game in a minimal way.
'''

description_COOPERATIVE_44 = '''
Below is a simple, fully-specified “n-player Tit-for-Tat” (nTFT) strategy that (i) is maximally cooperative when everyone reciprocates, (ii) punishes defections immediately, (iii) handles the first and last rounds, and (iv) uses no outside conventions or signals beyond the public history of moves.

1.  Intuition  
    •  Begin by cooperating.  
    •  In every interior round, cooperate if and only if *everyone* cooperated last round.  
    •  If any defection occurred in the previous round, defect this round.  
    •  In the very last round, defect (standard backward‐induction to avoid being exploited).  

2.  Decision rules  

    Let t = current round (1 ≤ t ≤ r), and let history[t−1] = list of all players’ actions in round t−1.

    •  If t = 1:  
       – Play C.  
    •  Else if t = r (the last round):  
       – Play D.  
    •  Else (2 ≤ t ≤ r−1):  
       – If ∀ j ∈ {1…n}: history[t−1][j] = C, then play C.  
       – Otherwise (at least one D last round), play D.  

3.  Pseudocode  

    ```  
    function decide_action(t, history, n, r):
        // history is a 2D array: history[s][j] ∈ {C,D}, for rounds s < t, players j=1…n

        if t == 1:
            return C

        if t == r:
            return D

        // Check last round's actions
        last_round = history[t-1]    
        for j in 1..n:
            if last_round[j] == D:
                return D
        // if we reach here, everyone played C last round
        return C
    ```

4.  Why it is cooperative  
    – When *all* players adopt this strategy:  
      • Round 1 → everyone plays C  
      • Rounds 2…(r−1) → since everyone cooperated previously, they all keep playing C  
      → yields (r−1) consecutive full‐cooperation rounds  
      • Round r → all defect (avoiding last‐round exploitation)  
    – Against a single deviator who defects in some round t₀ < r:  
      • Round t₀ → deviator earns higher payoff that round  
      • Round t₀+1 → our strategy defects (punishing the group)  
      • From t₀+1 onward (except last round), it will continue defecting because unanimity was broken  
      → deviator is punished in every subsequent interior round.  

5.  Edge-case handling  
    – First round (t = 1): no history → start cooperatively.  
    – Last round (t = r): standard one‐shot best response is D → we defect to avoid unilateral exploitation.  
    – Any round after a defection → immediate punishment, simple memory (only last round).  

This n-player Tit-for-Tat is easy to implement, uses only the public history of moves, and both fosters mutual cooperation and deters free‐riding.
'''

description_COOPERATIVE_45 = '''
Here is a simple, fully‐specified “cooperative” strategy for the repeated N-player public-goods game.  It is a direct generalization of Tit-for-Tat to the N-player setting, with one‐period punishment of any defection, and automatic defection in the last round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy Name  
  CONDITIONAL COOPERATOR (CC)

Parameters  
  n  = number of players  
  r  = total rounds (r > 1)  
  k  = multiplication factor (1 < k < n)

State Variables  
  We only need to remember what the others did in the immediately preceding round.  
    prev_others_defected  ← False  
      (True if in the last round at least one *other* player defected)

Action Rule pseudocode for player i  
  for t in 1…r do:
  
    if t == 1 then  
      // No history yet – start by cooperating  
      play C  
      
    else if t == r then  
      // Last round: defect (no future to punish us)  
      play D  
      
    else  
      if prev_others_defected == True then  
        // Punish everyone one round for any past defection  
        play D  
      else  
        // Otherwise, keep cooperating  
        play C  
      end if  
    end if
    
    
    // Now observe everyone’s choices this round  
    // Let c_j(t) = 1 if player j cooperated in round t, 0 if j defected  
    let defect_count_others = number of players j ≠ i for which c_j(t) = 0
    
    // Prepare state for next round  
    prev_others_defected = (defect_count_others > 0)
    
  end for

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of the Rules  

1. First Round (t=1):  
   We open with cooperation to signal our willingness to build the public good.  

2. “Tit-for-Tat” Punishment (Rounds 2 through r–1):  
   – If *any* other player defected in the immediately preceding round, we defect this round—this is our one‐turn punishment.  
   – As soon as every other player cooperates in a round, we resume cooperation in the following round.  
   This rule rewards a return to full cooperation quickly, but ensures defectors pay a short, sharp penalty.  

3. Last Round (t=r):  
   Because there is no future in which to punish us, defection strictly dominates cooperation in the final shot—so we defect.  
   (We assume other rational strategies will do likewise.)

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Why this is “Cooperative”  

•   It starts by cooperating.  
•   It only ever defects to punish *others’* defections, not because of miscoordination.  
•   It forgives after exactly one round of punishment, allowing the group to re-establish full cooperation quickly.  
•   It exploits defectors but never over‐punishes—limiting the damage to overall welfare.  

Over repeated play against other conditional cooperators, this strategy will sustain full cooperation for nearly all rounds (except the last), yielding each player close to the social‐optimum payoff of k every round. If an opponent defects, they are disciplined immediately, then brought back into the cooperative fold.
'''

description_COOPERATIVE_46 = '''
Below is a simple, fully‐specified “conditional cooperation with one‐round punishment” strategy.  It is designed to sustain high levels of contribution, punish defection just enough to deter it, then quickly return to the cooperative equilibrium.  It requires no off‐path signals or conventions beyond observing last round’s contributions.

––––––––––––––––––––––––––––––––––––––––––––––––––––  
STRATEGY NAME  
  “1‐Round Punish‐and‐Forgive”  

PARAMETERS  
  r                total number of rounds (r > 1)  
  n                number of players (n ≥ 2)  
  k                multiplication factor (1 < k < n)  
  P = 1            punishment length (in rounds)  

INTERNAL STATE  
  punish_remaining ∈ {0,1}   // how many rounds of punishment remain  

INITIALIZATION (before round 1)  
  punish_remaining ← 0  

DECISION RULE (at the start of each round t = 1,…,r):  
  1. If t = 1:  
       – Action ← C  
       – (No punishment possible yet)  

  2. Else if punish_remaining > 0:  
       – Action ← D  
       – punish_remaining ← punish_remaining − 1  
         (If that brings punish_remaining to 0, we will revert to normal cooperation next round.)  

  3. Else (punish_remaining = 0 and t ≥ 2):  
       – Let defectors_prev = number of players who chose D in round t–1.  
       – If defectors_prev > 0:  
           • Enter punishment phase:  
             punish_remaining ← P  
           • Action ← D  
         Else (defectors_prev = 0):  
           • Action ← C  

  4. Last‐round override (optional, but maximizes total payoff in final round):  
       – If t = r and punish_remaining = 0 then Action ← C  
         (If punish_remaining > 0 you still carry out the punishment.)  

––––––––––––––––––––––––––––––––––––––––––––––––––––  
EXPLANATION & RATIONALE  
1. First round you cooperate unconditionally.  
2. As long as no one has defected in the very last round, you keep cooperating—thus supporting full contributions.  
3. The moment you observe any defection, you retaliate by defecting for exactly one round (P = 1).  
4. After that one‐round punishment, you “forgive” and return to cooperation, giving everyone a fresh start.  
5. In the final round, if you are not in the middle of punishment, you can safely cooperate (no future rounds to exploit), squeezing out the last bit of group surplus.  

PROPERTIES  
• Incentive‐compatible punishment: a one‐round defection for a one‐round gain makes defection unprofitable if players care even slightly about future payoffs.  
• Fast forgiveness: punishing only one round means you don’t lock yourself (or the group) into permanent defection.  
• No exotic assumptions: you only use the publicly observed history of contributions.  

This strategy is easy to implement, clearly cooperative, and robust against isolated defections while avoiding the downward spiral of permanent defection.
'''

description_COOPERATIVE_47 = '''
Below is a simple, transparent “Tit-for-Tat” style rule, adapted to the n-player public-goods game, that (1) begins by cooperating, (2) punishes any observed defection by defecting for exactly one round, then forgives, and (3) cooperates on the very last round if—and only if—no defection has ever been observed.  This strategy is easy to implement, robust against persistent free-riding, and clearly signals a cooperative mindset.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: One-Round-Punishment Tit-for-Tat (ORP-TFT)  

State variables (per player i):  
• punishing (bool), initially false  
• ever_defected (bool), initially false  

For each round t = 1, 2, …, r do:  

1.  Decide action a_i,t  
    if t == 1 then  
      a_i,t ← C  
    else if t == r then  
      // Last-round override: only cooperate if we’ve never seen any defection  
      if ever_defected == false then  
        a_i,t ← C  
      else  
        a_i,t ← D  
      end  
    else  
      // Intermediate rounds  
      if punishing == true then  
        a_i,t ← D  
      else  
        a_i,t ← C  
      end  
    end  

2.  Play a_i,t simultaneously with others; observe all A_t = (a_1,t,…,a_n,t).  

3.  Update memory:  
    let others_defected = (∃ j ≠ i such that a_j,t == D)  
    if others_defected == true then  
      ever_defected ← true        // record that someone has defected at least once  
      if punishing == false then  
        punishing ← true          // enter one-round punishment  
      end  
    else  
      // if we were punishing last round, we have now completed it  
      if punishing == true then  
        punishing ← false  
      end  
    end  

Repeat to next round.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of key points:

1.  First round (t=1): Cooperate unconditionally to signal willingness to build the public good.

2.  Intermediate rounds (1 < t < r):  
   – If in the immediately preceding round you saw at least one defection by any player, set punishing=true and defect this round; that sends a clear message that “I will not tolerate free-riding.”  
   – After defecting once (the punishment), you reset punishing=false, and on the next round you return to cooperation—hoping that the group will have “learned” to contribute.

3.  Last round (t=r):  
   – Backward induction says there is no future punishment, so cooperators are exploitable.  To preserve a cooperative mindset, we override the normal rule: we only cooperate in the final round if no one in the entire history ever defected (ever_defected==false).  Otherwise we defect, since there is no way to enforce future compliance.

4.  ever_defected flag ensures that once the group has permanently broken down (someone defected even in the first round), we do not waste further resources on contributions that will be exploited without hope of sustained cooperation.

Why this is cooperative:
• It rewards full cooperation with continued cooperation.  
• It imposes the minimal necessary punishment (one round) on any defection.  
• It forgives swiftly, allowing the group to rebuild full cooperation if the defector returns to contributing.  
• It cooperates in the last round—but only if the group never betrayed mutual trust—thus preserving group payoffs when it is safe to do so.

This strategy is simple to implement, transparent to other LLM opponents, and aligns with the goal of sustaining high levels of public goods provision over r rounds.
'''

description_COOPERATIVE_48 = '''
Below is a fully‐specified “grim‐trigger” style strategy lifted to the n‐player public‐goods context.  It is simple, easy to implement, clearly cooperative (it seeks full contribution from everyone), punishes any unilateral defection by permanently reverting to defection (so deterrence is maximal), and it handles the first and last rounds explicitly.

1.     Variables & notation  
   •  n, r, k  — game parameters passed in.  
   •  history[t]  — the vector of contributions in round t (c₁,…,cₙ), where cᵢ=1 if player i played C, 0 if D.  
   •  totalContrib[t] = Σᵢ history[t][i]  

2.     Outline of the rule  
   A.  Round 1: cooperate.  
   B.  Rounds 2…(r–1):  
       –  If nobody has defected in any previous round, play C.  
       –  Otherwise (if at least one round in the past had totalContrib < n), play D.  
   C.  Round r (the last round): always defect.  

3.     Why it is cooperative  
   –  As long as every player (including yourself) has cooperated in all earlier rounds, you continue to cooperate, so it supports sustained full‐group cooperation.  
   –  The one‐shot “grim” punishment is severe enough to deter a unilateral defection: the moment any player breaks the all‐C equilibrium, everyone switches to D for the remainder (so the defector loses the future cooperative surplus).  
   –  No side channels or secret coordination needed—the strategy uses only the publicly observed contributions.  

4.     Pseudocode  
```
function decideMove(round t, history, n, r):
    # First‐round full‐cooperate
    if t == 1:
        return "C"
    # Last‐round always defect
    if t == r:
        return "D"
    # Check whether any defection has occurred in rounds 1..t-1
    for s in 1 .. (t-1):
        if sum(history[s]) < n:
            # A defection happened at round s; trigger permanent defection
            return "D"
    # No defection so far => cooperate
    return "C"
```

5.     Edge cases  
–  If two or more players simultaneously deviate, the same trigger activates; punishment does not single out individuals (public‐goods games cannot fine only the defectors), but the threat of losing all future cooperative surplus deters large‐scale collapse.  
–  If you (your own algorithm) accidentally defect in round 1 (e.g. due to a bug), you’ll punish yourself as well—this is a known drawback of grim‐trigger but can be remedied by a “finite‐length punishment” variant if desired.  
–  No coordination on round r is possible: backward induction says defect, so the strategy defecting in round r is internally consistent.  

6.     Possible variants / discussion  
If your tournament faces “noisy” play or you want to allow a single‐round slip without permanent collapse, you can soften the trigger (“punish for m rounds, then return to cooperation”).  But the pure grim‐trigger above is the simplest strategy that  
(a) fully cooperates whenever possible,  
(b) punishes any defection severely,  
(c) is deterministic and uses only public history,  
(d) explicitly handles first and last rounds.
'''

description_COOPERATIVE_49 = '''
Below is a single‐strategy proposal, called “Grim‐Trigger Public Goods” (GTPG), that (a) aims for full cooperation up to the last round, (b) punishes any defection by switching to defection forever, and (c) makes clear exceptions for round 1 and the last round.  Despite its simplicity, Grim‐Trigger is one of the most robust ways to sustain cooperation in a finitely repeated public‐goods game when you cannot communicate or coordinate sophisticated protocols.

1. Strategy overview  
   • We start by cooperating.  
   • We continue to cooperate in each subsequent round so long as no one has ever defected in any earlier round.  
   • The moment we observe a defection by anyone (including ourselves), we switch to defect forever after (punishment phase).  
   • In the very last round, we cooperate only if there has never been any defection—otherwise we defect (we cannot punish beyond the end).  

2. Pseudocode  
```
Parameters:
  n = number of players
  r = total number of rounds
  History = sequence of observed contribution‐vectors per past round
            (each vector is length n of 0/1’s; 1=C, 0=D)

State variable:
  triggered = false    // has any defection been observed so far?

For each round t = 1,2,…,r:
  // Update trigger flag based on history from round t–1
  If t > 1:
    Let last_contributions = History[t–1]    // a list of 0/1’s
    If min(last_contributions) == 0:
      triggered = true

  // Decision rule
  If t == r:
    // Last‐round rule
    If triggered == false:
      play C
    Else
      play D
  Else
    // Rounds 1 through r–1
    If triggered == false:
      play C
    Else
      play D

  // After choosing, the action (0/1) will be added to History[t]
End For
```

3. Explanation of decision rules  
  – Round 1: “triggered” is still false, so we play C (cooperate).  
– Rounds 2 to r–1:  
   • If we have never seen a defection, we keep cooperating.  
   • As soon as any player defects in any prior round, we set `triggered = true` and from that round onward we always defect.  
– Round r (final):  
   • If full cooperation has prevailed up to round r–1 (`triggered == false`), we cooperate one last time—rewarding the group for perfect play.  
   • Otherwise, we defect, because there is no future in which to punish or to restore cooperation.  

4. Cooperative mindset and rationale  
– By cooperating every round unless someone defects first, we send a clear, simple “let’s all cooperate” signal.  
– The grim trigger (permanent defection after any defection) creates a strong deterrent: any single defection destroys the possibility of future cooperative surplus.  
– Rewarding perfect cooperation with one final C in round r gives co‐players an extra incentive to keep cooperating right up to the end.  
– This strategy never attempts complex belief‐tracking or side‐payments; it only requires observing who cooperates/defects.  

5. Handling edge cases  
– If r = 2, we cooperate in round 1. If everyone cooperated, we cooperate in round 2; otherwise we defect in round 2.  
– If some opponent always defects, we’ll cooperate in round 1 and then defect from round 2 on—minimizing our losses.  
– If everyone uses the same Grim‐Trigger logic, full cooperation is sustained for rounds 1 through r – 1, and a final bonus cooperation occurs in round r.  

GTPG is easy to implement, transparent in its incentives, and widely known to support near‐optimal cooperation against a broad class of selfish opponents in finitely repeated public‐goods settings.
'''

description_COOPERATIVE_50 = '''
Below is a simple “conditional‐cooperator” strategy that (i) starts out fully cooperative, (ii) uses the previous round’s cooperation level as its guide, (iii) punishes mild deviations only one round long, and (iv) returns to cooperation as soon as the group re-coordinates.  It works for any n ≥ 2, r > 1 and 1 < k < n.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Strategy intuition  
   •  We want to sustain full‐group cooperation (everyone plays C) by only defecting when there is a shortfall of cooperators.  
   •  We punish deviations for exactly one round, then we give the group another chance.  
   •  This is a form of generalized “tit for tat” or “win–stay, lose–shift” in the n-player setting.  

2.  Parameters and threshold  
   Let  
     n = number of players  
     r = total rounds  
   Define a cooperation threshold T = ceil((n + 1)/2).  
   –– Intuition: if at least half (rounded up) cooperated last round, it is safe to cooperate.  

3.  Decision rule (per round t = 1…r)  

   If t = 1:  
     Play C.    // we always open with cooperation  

   Else (t > 1):  
     Let m = number of players (including yourself) who contributed C in round t–1.  
     If m ≥ T:  
       Play C.  // group is sufficiently cooperative, continue cooperating  
     Else:  
       Play D.  // insufficient cooperation last round, deliver a one‐shot punishment  

   End  

4.  Edge cases  

   •  Last round (t = r):  
     We apply exactly the same rule.  
     – We do not “unwind” to guaranteed defection on the last move; instead we remain consistent and cooperate if m ≥ T, defect otherwise.  

   •  Recovering from punishment:  
     Since our punishment is only one round long, if the group re-coordinates in round t, you immediately resume cooperation in round t+1.  

   •  No exogenous noise handling:  
     This strategy assumes actions are observed without noise.  Even a single lapse by one player triggers only one round of punishment.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  

  Input:  n, r  
  T ← ceil((n + 1)/2)  

  history ← empty list of length r  // will record each round’s C/D for all players  

  for t in 1…r:  
    if t == 1:  
      my_action ← C  
    else:  
      // count how many cooperated last round  
      m ← count of C’s in history[t−1]  
      if m ≥ T:  
        my_action ← C  
      else:  
        my_action ← D  
    end  

    submit(my_action)  
    observe full profile a_1,…,a_n this round  
    history[t] ← (a_1,…,a_n)  

  end  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Why this is cooperative  
  •  If everyone uses it, in round 1 all C ⇒ m=n≥T ⇒ round 2 all C ⇒ … ⇒ full cooperation every round.  
  •  A single defection in round t–1 causes one round of group‐wide D in round t, but the next round (t+1) cooperation can resume as soon as the group m≥T again.  
  •  This strategy never punishes forever, it never “grinds” the group back to permanent defection; it is forgiving after exactly one round.  
  •  It never requires communication or complex coordination—only simple counting of cooperators.
'''

description_COOPERATIVE_51 = '''
Below is a single‐strategy proposal—call it “Generous Collective TFT with Endgame Defection.”  It is easy to implement, is maximally cooperative when the group is cooperating, punishes defections just enough to deter free‐riding, forgives occasional slip‐ups, and handles first‐ and last‐round edge cases.

1.  Strategy outline  
    •  Name: Generous Collective Tit-for-Tat with Endgame Defection  
    •  Intuition:  
       –  Start by cooperating.  
       –  In each non-terminal round, look at how many cooperators there were last round.  
       –  If nearly everyone (n or n–1 players) cooperated, cooperate again.  
          This “forgives” up to one stray defection.  
       –  Otherwise defect this round (a mild punishment).  
       –  In the last round, defect (standard endgame play).  

2.  Decision rules in detail  
    Let t ∈ {1,2,…,r} be the current round; let m_{t–1}=∑_{j=1}^n c_j(t–1) be the number of cooperators in the previous round.  

    Round t = 1:  
       Play C.  

    Rounds t = 2,3,…,r–1 (interior rounds):  
       If m_{t–1} ≥ n–1 then  
          Play C  
       Else  
          Play D  

    Round t = r (last round):  
       Play D  

3.  Why it’s cooperative  
    •  As long as the group is near‐fully cooperating (at most one defector), you continue cooperating.  
    •  A single defection by a co‐player is forgiven: you still cooperate unless two or more defect.  
    •  If defection becomes “contagious” (≥2 players defect), you defect once as a warning.  
    •  After that one “punishment” defect, if the others return to full cooperation, you immediately go back to C.  

4.  Edge-case handling  
    – First round: no history ⇒ choose C to signal willingness to cooperate.  
    – Last round: finite-horizon logic ⇒ defect (all rational players will defect in the final stage; cooperating there is purely altruistic but cannot be sustained).  
    – Single stray defection (e.g. noise or experimentation) ⇒ forgiven automatically in the next round, so the chain of cooperation is not broken by accident.  
    – Multiple defectors in one round ⇒ a single‐round “punishment” by defecting once; if the group then returns to near-full cooperation, you forgive and resume.  

5.  Pseudocode  

    function my_action(t, history):  
        Input:  
           t        – current round index (1…r)  
           history  – list of past action profiles [(c_1, …, c_n) at each τ < t]  
        Output:  
           “C” or “D”  

        if t == 1:  
            return “C”  

        if t == r:  
            return “D”  

        // interior rounds  
        let last_profile = history[t–2]  
        let m = sum_{j=1..n} last_profile[j]  // number of C’s last round  

        if m >= n – 1:  
            // everyone or everyone but one cooperated  
            return “C”  
        else:  
            // two or more defectors last round ⇒ mild punishment  
            return “D”  

End of strategy. When played against other “nice” or “conditional-cooperator” strategies it quickly settles on full cooperation, tolerates up to one defection per round, and does not collapse into all-D except in the unavoidable last stage.
'''

description_COOPERATIVE_52 = '''
Below is a fully specified, state‐based strategy that (i) tries to sustain full cooperation, (ii) punishes any defection by defecting exactly one round, then immediately forgives, and (iii) handles first and last rounds explicitly.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
STRATEGY NAME  
One‐Round Punish & Forgive (ORPF)

PARAMETERS  
n   – number of players (≥2)  
r   – total number of rounds (>1)  

STATE VARIABLES  
punish_timer ∈ {0,1}  
  – counts remaining punishment rounds (0 = no punishment pending)

INTERNAL OBSERVABLE  
last_C_count  
  – number of players who cooperated in the immediately preceding round  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
HIGH‐LEVEL IDEA  
1. Round 1: Cooperate unconditionally.  
2. Thereafter, if we are “in punishment” (punish_timer=1), defect this round, decrement punish_timer to 0, then revert to full cooperation mode.  
3. If we are not punishing (punish_timer=0):  
   – If everyone cooperated last round (last_C_count == n), cooperate again.  
   – Otherwise (at least one defector last round), set punish_timer=1, defect this round.  
4. In the final round (t=r), if punish_timer=0 we still cooperate (we do _not_ carry out a backward‐induction defection), but if punish_timer=1 we defect as a part of punishing.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
PSEUDOCODE  

initialize:  
  punish_timer ← 0  

for each round t from 1 to r do  
  if t == 1 then  
    action ← C  
  else if punish_timer > 0 then  
    # We are serving our one‐round punishment  
    action ← D  
    punish_timer ← punish_timer – 1  
  else if t == r then  
    # Last round and no punishment pending  
    action ← C  
  else  
    # No punishment pending, not first or last round  
    if last_C_count == n then  
      action ← C        # everyone cooperated last round, stay cooperative  
    else  
      action ← D        # punish defectors  
      punish_timer ← 1  # schedule exactly one round of punishment  
    end if  
  end if  

  play action  
  observe opponents’ actions  
  last_C_count ← number of C’s in this round (including yourself)  
end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
EXPLANATION & PROPERTIES  

1. Cooperativeness  
   – As long as _everybody_ cooperates, ORPF will keep cooperating, maximizing the group‐level public good.  
   – Even in the final round, if there is never been a defection to punish, ORPF cooperates.  

2. Deterrence of Defection  
   – The moment any player defects (last_C_count < n), ORPF switches to defection for exactly one round.  
   – Since the punishment is group‐wide in that round, the lone defector foregoes its share of the public good during punishment.  

3. Forgiveness  
   – Punishment lasts exactly one round, after which ORPF immediately returns to cooperation—this avoids permanent breakdowns due to noise or single mistakes.  

4. Handling Edge Cases  
   – First round: C (build initial trust).  
   – Last round: if no punishment is pending, C (to continue maximally cooperative play), else D (to serve the punishment).  

5. Implementation Notes  
   – Only one integer state variable (punish_timer) is needed.  
   – Complexity is O(1) per round.  
   – Requires observing the total number of cooperators each round (which is standard in the public‐goods setting).  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
ORPF strikes a balance between strong deterrence (any defection triggers a cost to the defector) and quick reconciliation (forgiveness next round), fostering sustained high cooperation in repeated public‐goods play.
'''

description_COOPERATIVE_53 = '''
Below is a simple “trigger‐and‐forgive” strategy that (1) starts fully cooperative, (2) punishes any defection by defecting for a small fixed number of rounds, then (3) returns to cooperation, and (4) always cooperates in the last round to maximize the group payoff.  It requires only one round of memory plus a small counter.

––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: Forgiving Trigger  
Parameters:  
 M = number of punishment rounds (we suggest M=2)  

State variables (maintained across rounds):  
 punish_count ∈ {0,1,…,M}  ← how many punishment rounds remain  

Initialization (before round 1):  
 punish_count ← 0  

For each round t = 1…r do:  
 if t = 1 then  
  Action ← C // always start by cooperating  
 else if t = r then  
  Action ← C // always cooperate in last round  
 else if punish_count > 0 then  
  // we are in punishment mode  
  Action ← D  
  punish_count ← punish_count − 1  
 else  
  // no punishment currently scheduled  
  if any player j defected in round t−1 then  
   // trigger punishment  
   punish_count ← M−1   // we will play D this round plus M−1 more  
   Action ← D  
  else  
   // everyone cooperated last round ⇒ resume cooperation  
   Action ← C  
  end if  
 end if  

End for  

––––––––––––––––––––––––––––––––––––––––––––  
Explanation of key points:

1.  First round cooperation  
    We unconditionally play C in round 1 to signal willingness to cooperate.

2.  Trigger & finite punishment  
    The first time we see a defection (any D by any other) we defect for M consecutive rounds (including the round in which we detected the defection).  This punishes defectors but does not lock us into permanent retaliation.

3.  Forgiveness  
    After M defections we return to cooperation, giving the group a chance to re‐establish full cooperation.

4.  Last‐round override  
    Because no future punishment is possible, we override any remaining punish_count in round r and play C.  This maximizes the total group payoff (and our own payoff) in the final round.

5.  Choice of M  
    Setting M=1 reduces to a one‐round “Tit‐for‐Tat‐style” response.  Larger M enforce harsher punishment.  We recommend M=2 or 3 to make defection unprofitable yet still allow a quick return to full cooperation.

This strategy is fully specified, requires only 1–round memory plus a small counter, and ensures that mutual cooperation is both stable and efficient.
'''

description_COOPERATIVE_54 = '''
Below is a single “conditional‐cooperate” strategy that (i) starts by cooperating, (ii) punishes any defection by a one–round reciprocal defection, (iii) then immediately forgives, and (iv) in the very last round defects (since no future remains).  This simple strategy is easy to implement, fosters high levels of cooperation, and handles the finite horizon.

1. Variables  
   • P : punishment counter (integer ≥ 0), initially P ← 0  
   • r : total number of rounds  
   • t : current round index, 1 ≤ t ≤ r  

2. Decision rule for round t  
   if t = r then  
     – play D  (last‐round defection)  
   else if t = 1 then  
     – play C  (always start by cooperating)  
   else if P > 0 then  
     – play D  
     – P ← P − 1  
   else  
     – look at last round’s total contributions S = Σ_j c_j^(t−1)  
       • if S < n (i.e. at least one defector) then  
           • play D  
           • P ← 1   (punish exactly one round)  
         else  
           • play C  

3. Pseudocode  

  initialize P ← 0  
  for t in 1…r do  
    if t = r then  
      action ← D  
    else if t = 1 then  
      action ← C  
    else if P > 0 then  
      action ← D  
      P ← P − 1  
    else  
      let S ← number of cooperators in round t−1  
      if S < n then  
        action ← D  
        P ← 1  
      else  
        action ← C  
    end  
    play action in round t  
  end  

4. Explanation and properties  
• First round: we cooperate unconditionally to signal goodwill.  
• “Tit‐for‐one‐lag” punishment: any time someone defects (S < n), we defect exactly once in the next round (P=1), then return to cooperation.  This punishes defectors but swiftly forgives, avoiding long vendettas.  
• Last round (t=r): we defect, since after r there is no future in which punishments or rewards can be imposed.  
• By defecting only one round per observed defection, we minimize lost cooperative surplus.  At the same time, no one can exploit us repeatedly without suffering immediate retaliation.  
• Against like‐minded cooperators, S will always equal n (no one ever defects), so we enjoy full cooperation (π_i = k each round except the last, where π_i = 1).  
• If one or more players stray, they immediately incur a one‐round retaliation, which stabilizes full‐cooperation equilibria for large enough k (folk theorem logic).  

This strategy (sometimes called “Forgiving Tit‐for‐Tat with final‐round defection”) is simple, transparent, and provably cooperative in repeated public‐goods settings. It neither over‐punishes nor allows sustained exploitation, and it explicitly handles the finite horizon.
'''

description_COOPERATIVE_55 = '''
Below is a single‐parameter “conditional‐cooperation” strategy that (a) starts by cooperating, (b) punishes only when group cooperation last round was too low to make cooperation payoff‐worthwhile, (c) forgives as soon as the group recovers, and (d) defects in the very last round to avoid end‐game exploitation.  It requires only knowing n, k, r, and the total contributions in the previous round:

––––––––––––––––––––––––––––––––––––  
Strategy: Threshold‐Based Conditional Cooperation  
––––––––––––––––––––––––––––––––––––  

Parameters computed once at the start:  
 T ← ceil(n / k)  
  • This is the minimum number of contributors in the previous round needed so that a cooperator’s public‐good share ≥ 1.  
  • Since k > 1, 1 ≤ T ≤ n.

Decision rule for player i on round t (1 ≤ t ≤ r):

1. If t == 1  
 Action ← C  // Always start by cooperating

2. Else if t == r  
 Action ← D  // Last‐round defection (no future to reward cooperation)

3. Else  
 Let S ← total contributions (number of C’s) in round t − 1  
 If S ≥ T  
  Action ← C  // Previous round yielded enough public good—cooperate  
 Else  
  Action ← D  // Previous round fell short—defect (punish)

––––––––––––––––––––––––––––––––––––  
Pseudocode Version  
––––––––––––––––––––––––––––––––––––  

```
initialize(n, k, r):
    T ← ceil(n / k)

decide_action(t, history):
    if t == 1:
        return "C"
    if t == r:
        return "D"
    // extract last round’s contributions
    S ← sum_{j=1..n} [history[t-1].action_j == "C" ? 1 : 0]
    if S ≥ T:
        return "C"
    else:
        return "D"
```

––––––––––––––––––––––––––––––––––––  
Why this is cooperative  
––––––––––––––––––––––––––––––––––––  
• By cooperating on round 1, it signals willingness to build the public good.  
• It punishes only when the group’s cooperation last round was so low that even a cooperator’s share would fall below the private defection payoff (1).  
• Punishment lasts exactly one round; if the group rebounds (S ≥ T), it immediately returns to cooperation, which helps restore mutual cooperation quickly.  
• It defects in the last round, avoiding exploitation when no future rounds remain to enforce reciprocity.  

This rule uses no hidden coordination, communicates only via actions, and balances firmness against defectors with prompt forgiveness—qualities known to sustain high cooperation in finitely repeated public‐goods settings.
'''

description_COOPERATIVE_56 = '''
Below is a single‐strategy proposal—call it “N-TFT+End-Defect”—which generalizes tit-for-tat to n players, adds limited punishment and handles the end‐game.  

1.  Overview of States and Variables  
    •  state ∈ {Cooperate, Punish}  
    •  punish_counter ∈ ℕ (initially 0)  
    •  P = 1  (length of punishment phase)  

2.  High-Level Description  
    •  We begin in the Cooperate state, play C.  
    •  As long as everyone cooperated last round, remain cooperative.  
    •  If we detect any defection by anyone, enter a Punish subphase of length P: play D for the next P rounds, then return to Cooperate.  
    •  In the very last round (t = r), defect (the one‐shot Nash).  

3.  Why it’s Cooperative  
    •  Rewards full cooperation by continuing to cooperate.  
    •  Punishes defections just long enough (P=1) to deter free‐riding.  
    •  Forgives after punishment, allowing cooperation to restart.  

4.  Pseudocode  

```
Inputs:
  n    – number of players
  r    – total rounds
  history – list of past rounds; each entry is a list of n actions {C,D}

Initialize:
  state = "Cooperate"
  punish_counter = 0

Function decide_move(t, history):
  # 1) Last‐round defection handling / punishment logic
  if punish_counter > 0:
    # we are in a punishment subphase
    punish_counter -= 1
    my_move = D
  else:
    # not currently punishing
    if t == 1:
      # first round: start cooperatively
      my_move = C
    elif t == r:
      # last round: one‐shot Nash defect
      my_move = D
    else:
      # rounds 2 … r−1: inspect previous round
      last_round = history[t-2]      # zero‐based index
      if any(a == D for a in last_round):
        # somebody defected → enter punishment
        punish_counter = P  # will punish for next P rounds
        my_move = D
      else:
        # full cooperation last round → cooperate
        my_move = C

  return my_move
```

5.  Edge Cases  
  •  First round (t=1): no history → cooperate.  
  •  Last round (t=r): defect regardless of history (standard finite‐horizon logic).  
  •  Single defection by any player in round t triggers exactly P=1 rounds of universal defection in t+1, then resets.  

6.  Parameter Choices & Extensions  
  •  Punishment length P=1 is minimal but sufficient to deter isolated defections. You can increase P if you expect more severe opportunism.  
  •  This strategy never locks into permanent defection—it always forgives after P rounds—so it sustains cooperation if opponents are likewise responsive.  

By construction it is (i) cooperative when others are, (ii) punishes free‐riding but (iii) returns to cooperation, and (iv) handles both the beginning (optimism) and the end (one‐shot defection) of the finite horizon.
'''

description_COOPERATIVE_57 = '''
Below is a full description of a simple, “forgiving‐trigger” strategy that (1) starts by cooperating, (2) rewards unanimous cooperation, (3) punishes any defection by the group for a short, fixed number of rounds, then forgives, and (4) defects in the very last round to avoid end‐game exploitation.

—–  
Name: Forgiving Group‐Trigger (FGT)  

State variables (per player):  
• punishment_timer ∈ {0,1,2,…}, initially 0  
• last_all_coop ∈ {true,false}, initially true  

Parameters (you choose once at start):  
• P = 2 // length of group punishment  

Decision rule at round t (1 ≤ t ≤ r):  
1. If t == 1:  
     play “C”  
2. Else If t == r:  
     play “D” // last‐round defection to avoid being exploited  
3. Else if punishment_timer > 0:  
     play “D”  
     punishment_timer ← punishment_timer − 1  
4. Else (punishment_timer == 0):  
     if last_all_coop == true:  
         play “C”  
     else:  
         // Someone defected last round ⇒ enter punishment  
         punishment_timer ← P  
         play “D”  

After observing all players’ moves in round t, update:  
last_all_coop ← true if and only if every player chose C in round t  

—–  
Explanation of the logic:  
1. First round cooperates unconditionally to invite mutual cooperation.  
2. If everyone cooperated in the immediately preceding round, remain in “cooperative mode” and play C again.  
3. At the first sign of any defection by anyone, switch to “punishment mode” for exactly P rounds (here P=2), during which you defect every round.  
4. After P rounds of punishment you “forgive” by resetting punishment_timer to 0 and return to cooperative mode (i.e. you again require unanimous cooperation to continue).  
5. In the very last round (t=r) you defect—no future rounds remain in which to reward cooperation, so defection is the dominant action.  

Why this is cooperative:  
• It fully rewards a string of unanimous contributions with ongoing cooperation.  
• It punishes any defection by the group, so deters free‐riding.  
• Punishment is limited (P rounds) and followed by full forgiveness, preventing permanent mutual defection.  
• Defection in the final round is standard in finite repeated games to avoid being exploited.  

This strategy is simple, transparent, and aligns incentives around collective contributions while still guarding against repeated exploitation.
'''

description_COOPERATIVE_58 = '''
Below is a single‐player “recipe” you can submit to the tournament.  It is a straightforward, cooperative‐minded, N-player generalization of Tit-for-Tat with limited forgiveness and a one-round punishment.  It obeys the public‐goods payoffs, punishes defectors, but quickly returns to cooperation if the group does.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: N-TFT-F (N-player Tit-for-Tat with Forgiveness)  

Parameters (you may embed these in your code or hard-code):  
• n         = number of players  
• r         = total rounds  
• f_count   = forgiveness count = 1   (allow up to one defection last round)  
• L         = punishment length   = 1   (punish defectors one full round)  

State variables (maintained between rounds):  
• punishment_timer  (integer, initially 0)  

Decision rule for round t:  
1. If t == 1:  
     – Action = Cooperate (C).  
2. Else if t == r:  
     – Action = Defect (D).  
     (Standard backward-induction step: last round is a one-shot game.)  
3. Else if punishment_timer > 0:  
     – Action = D  
     – Decrease punishment_timer by one (punishment_timer ← punishment_timer – 1).  
4. Else:  look at how many cooperated in round t–1:  
     let coop_prev = number of players j with c_j = 1 in round t–1.  
     let def_prev  = n – coop_prev.  
     a) If def_prev ≤ f_count  (i.e. at most one defector last round):  
          Action = C  (forgive up to f_count defections).  
     b) Otherwise (more than f_count defectors):  
          Action = D  
          punishment_timer ← L  

Rationale:  
– We start by cooperating to signal goodwill.  
– In each interior round we cooperate so long as the group as a whole was “almost” fully cooperative last turn.  
– If f_count+1 or more players defect, we punish by defecting for L=1 rounds, then return to cooperation.  
– On the very last round we defect (since no future to punish us).  

Pseudocode  
-----------  
   // GLOBAL STATE  
   punishment_timer ← 0  

   function choose_action(t, history):  
     if t == 1:  
       return C  

     if t == r:  
       return D  

     if punishment_timer > 0:  
       punishment_timer ← punishment_timer – 1  
       return D  

     // otherwise inspect last round  
     coop_prev ← count of C’s in history[t–1]  
     def_prev  ← n – coop_prev  

     if def_prev ≤ f_count:  
       return C  
     else:  
       punishment_timer ← L  
       return D  

Edge cases  
----------  
– Rounds 1 and r are hard-wired.  On round 1 you always cooperate.  On the final round you always defect.  
– punishment_timer ensures you carry out exactly L rounds of defection as a punishment.  L=1 means “one‐round tit‐for‐tat.”  
– f_count=1 forgives up to one stray defection by the group, to recover cooperation quickly.  

Why this is cooperative  
------------------------  
• It rewards full or nearly full cooperation by returning C as soon as you see at most one defection.  
• It punishes larger breakdowns of cooperation, deterring mass defection.  
• It never parties defects indefinitely—after L rounds it again gives the group a chance.  
• It establishes a simple, transparent rule that other conditional cooperators can easily learn and reciprocate.
'''

description_COOPERATIVE_59 = '''
Below is a single‐strategy proposal—call it “Threshold Reciprocal with One‐Period Punishment (TR‐OPP)”—that tries to sustain cooperation for as many rounds as possible, but still defects in the last round.  It is fully specified, handles edge cases, is forgiving (only one‐period punishment), and aligns with the cooperative mindset whenever it is worthwhile.

1.  Precompute a cooperation threshold L:  
   •  In a one‐shot public goods game, you prefer to cooperate over defect if  
      (k/n)·(number of cooperators) > 1.  
   •  Thus set  
        L = floor(n/k) + 1  
      so that if at least L players cooperated last round, then cooperating this round yields a higher immediate payoff than defecting.

2.  Strategy overview  
   •  Start by cooperating.  
   •  On each round t=2,…,r−1 compare last‐round cooperators to the threshold L:  
       –  If last round’s total cooperators ≥ L, play C.  
       –  Otherwise, play D for exactly one round (the “punishment”), then revert to C.  
   •  In the final round t = r, always play D (no future to protect).  

3.  Pseudocode  

   let L = floor(n / k) + 1  
   let punishing = false    # flag: are we now in the one‐round punishment?  

   for t in 1…r do  
     if t == 1 then  
       action[t] = C          # no history yet, give cooperation a chance  
     else if t == r then  
       action[t] = D          # last round: defect  
     else  
       if punishing == true then  
         # we are carrying out a one‐round punishment  
         action[t] = D  
         punishing = false    # reset punishment flag after one round  
       else  
         let m = number_of_cooperators_in_round(t−1)  
         if m >= L then  
           action[t] = C  
         else  
           action[t] = D      # trigger a one‐round punishment  
           punishing = true  
         end if  
       end if  
     end if  
   end for  

4.  Explanation of components  

   1.  First round (t=1):  
       – We cooperate, hoping to signal willingness to build the public good.  

   2.  Rounds t=2,…,r−1:  
       – We check whether last round’s cooperation level m was high enough (m ≥ L) so that immediate payoffs reward cooperation.  
       – If it was, we “reward” by cooperating.  
       – If it was below threshold, we impose exactly one round of punishment by defecting, then revert to cooperation.  This avoids endless mutual defection (over‐harsh trigger), and is forgiving.  

   3.  Last round (t=r):  
       – Since there is no future, we defect (standard end‐game logic).  

5.  Edge‐case handling  

   •  If r=2:  
     – t=1: we cooperate.  
     – t=2 (last): we defect.  

   •  If floor(n/k)+1 = 1 (i.e. k≥n):  
     – L=1, so any positive cooperation last round triggers C.  If nobody cooperates, we still punish once then resume C.  

   •  No unbounded penalties:  
     – The “punishing” flag ensures only one round of defection per shortfall, limiting collateral damage.  

6.  Why this is cooperative  

   – We begin with cooperation.  
   – We only defect when last round’s group cooperation was too low to make cooperating immediately payoff‐dominant, and even then we punish for only one round.  
   – After that single punishment we revert to cooperation—so long as the group returns above the profitability threshold.  
   – By defecting only when rationally forced and for only one round, we sustain high‐levels of cooperation while protecting ourselves against persistent free‐riders.  
   – In the terminal round, we defect (standard backward‐induction), but by then we have extracted cooperation in all prior rounds.
'''

description_COOPERATIVE_60 = '''
Below is a simple “trigger‐and‐forgive” strategy that (i) starts out fully cooperative, (ii) punishes any round in which at least one player defects by defecting exactly one round, and then (iii) returns to cooperation as soon as full cooperation is observed.  In the very last round, since there is no future to protect, it defects (to maximize its own one‐shot gain).  

1. State variables  
   • punish_flag (boolean), initially false  
   • last_coop_count (integer), undefined until after Round 1  

2. High-level decision rules  
   – Round 1: Cooperate.  
   – Rounds 2 … r−1:  
       • If punish_flag==true, then Defect this round (punishment), and reset punish_flag←false.  
       • Else (punish_flag==false):  
            – If in the previous round everyone cooperated (last_coop_count==n), Cooperate.  
            – Otherwise (at least one defector last round), Defect this round and set punish_flag←true.  
   – Round r (the last round): Defect (no future rounds to enforce cooperation).  

3. Pseudocode  

  initialize:  
    punish_flag ← false  

  for t in 1…r do  
    if t == 1 then  
      action_t ← C                        # always start by cooperating  
    else if t == r then  
      action_t ← D                        # last‐round defection  
    else if punish_flag == true then  
      action_t ← D                        # carry out one‐round punishment  
      punish_flag ← false  
    else                              
      if last_coop_count == n then       # full cooperation last round?  
        action_t ← C  
      else                               # saw at least one defection last round  
        action_t ← D  
        punish_flag ← true               # schedule one‐round punishment next turn  
      end if  
    end if  

    play action_t  
    observe coop_count_t = number of cooperators in round t  
    last_coop_count ← coop_count_t  

  end for  

4. Explanation of key points  
  • Cooperate whenever the entire group cooperated in the immediately preceding round.  
  • If anyone defects, punish exactly one round (by defecting yourself), then—if full cooperation ever re‐appears—immediately return to cooperating.  
  • First round must be cooperative to signal willingness.  
  • Last round you defect (the dominant one‐shot move), but by that point you will have preserved cooperation in all earlier rounds with any reciprocators.  

5. Behavior in common scenarios  
  – All cooperators (“All-C” opponents): You will cooperate rounds 1…r−1 and then defect in r.  Group payoff is maximal until the last round.  
  – Single accidental defector in round t: You punish in t+1, but if everyone then returns to C in t+1, you resume cooperation in t+2.  
  – Persistent defectors: You cooperate once, see defection, then defect every remaining non‐final round (since you never observe full cooperation again), preventing them from profiting off you.  

This strategy is “cooperative” (it maintains full cooperation whenever possible), “punishes” defectors swiftly but only briefly, and “forgives” as soon as the group restores cooperation.
'''

description_COOPERATIVE_61 = '''
Below is one example of a cooperative, conditional‐cooperation strategy for the N-player repeated public-goods game.  It combines three ingredients:

 1. Start by cooperating.  
 2. Reward cooperation and punish defections “just enough” (one round of punishment), then forgive.  
 3. In the very last round, defect (no future to sustain cooperation).  

You can tune the punishment length or endgame cutoff to your taste, but this particular variant (“1-round punish, then forgive”) has proven robust in tournaments.

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
Cooperative Strategy: “Forgiving Tit-for-Tat for Public Goods”

Parameters you may choose up front:
  • punish_length = 1    (number of rounds to punish after seeing any defection)  
  • endgame_cutoff = 1   (number of last rounds in which we defect)  

State variables (kept from round to round):
  • pun_remaining ← 0    (rounds of punishment still to go)  

Pseudocode for player i in round t (1 ≤ t ≤ r):

  if t > r – endgame_cutoff then
    // In the last ‘endgame_cutoff’ rounds there is no future incentive
    action ← D

  else if t = 1 then
    // First round: start by cooperating
    action ← C

  else if pun_remaining > 0 then
    // We are currently punishing
    action ← D
    pun_remaining ← pun_remaining – 1

  else
    // Look at what everyone did last round
    let total_cooperators_prev = Σ_{j=1..n} c_j(t–1)

    if total_cooperators_prev = n then
      // Everyone cooperated last round → reward with cooperation
      action ← C
    else
      // At least one defector last round → trigger punishment
      pun_remaining ← punish_length
      action ← D
    end if
  end if

// End of round t.  Observe actions c_j(t), payoffs π_j(t), then go to next t.
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Explanation:

1.  First round we cooperate unconditionally, signaling goodwill.  
2.  As long as everyone cooperated in the immediately preceding round, we keep cooperating.  
3.  If we detect any defection in the last round (i.e. total_cooperators < n), we defect for exactly one round (punishment), then reset to cooperating.  
4.  In the final round (t = r), we defect—there is no future to leverage, so we switch to the one‐shot Nash play.  

Why this works cooperatively:

–  It only punishes for a minimal length (one round) so that a single mistake by one opponent does not trigger endless mutual defection.  
–  It rewards full cooperation immediately, sustaining high contribution levels.  
–  The final‐round defection is necessary to avoid being strictly dominated in the last stage.  

Tuning notes:

–  punish_length can be increased (more severe punishment) if opponents are slow to re‐cooperate, but too large punishments can collapse cooperation.  
–  endgame_cutoff can be set >1 if you expect opponents to start “end‐game” defection early; this can blunt the backward‐induction cascade.  
–  You may also randomize in the last few rounds (e.g. occasionally cooperate) to create uncertainty about the exact end, but the simple version above suffices in many tournaments.
'''

description_COOPERATIVE_62 = '''
Below is a simple, fully specified “cooperative” strategy for the n‐player public‐goods game.  It is a direct generalization of Tit-for-Tat to n players, with a one‐round “punishment” window and a last‐round defection.  It (1) starts by cooperating, (2) defects for exactly one round whenever anyone defects, (3) otherwise cooperates, and (4) defects in the final round (to guard against backward induction).  This scheme (often called a “forgiving trigger”) rewards full cooperation, punishes defection just long enough to discourage it, then quickly returns to cooperation.

––––––––––––––––––––––––––––––––––––––  
Strategy name: N-TFT-1 (n-player Tit-for-Tat with 1-round Punishment and Final‐Round Defect)  
Parameters:  
  n ≥ 2 (number of players)  
  r > 1 (number of rounds)  

State variables:  
  last_actions[1..n]  – the action profile observed in the previous round  
  punish_counter      – integer, how many more rounds to punish (init 0)  

Action set:  C = Cooperate, D = Defect  

Pseudocode outline:

```
initialize:
  punish_counter ← 0

for t from 1 to r do
  if t == 1 then
    my_action ← C
  else if t == r then
    my_action ← D
  else if punish_counter > 0 then
    // still in punishment mode
    my_action ← D
    punish_counter ← punish_counter – 1
  else
    // not in punishment mode; look at last round
    total_cooperators ← sum(last_actions[j] == C for j=1..n)
    if total_cooperators == n then
      // everybody cooperated last round → resume cooperation
      my_action ← C
    else
      // at least one defection → punish for one round
      my_action ← D
      punish_counter ← 1
    end if
  end if

  play my_action
  observe all players’ actions into last_actions[1..n]
end for
```

Explanation of the rules:

1. First round (t=1): always cooperate (to signal willingness).  
2. Intermediate rounds (2 ≤ t < r):  
   a. If we are still punishing (punish_counter>0), defect and decrement the counter by one.  
   b. Otherwise, check whether everyone in the previous round cooperated.  
      – If yes, cooperate.  
      – If no one cooperated (i.e. at least one defector), defect, set punish_counter=1 to punish for exactly one round, then return to “nice” mode.  
3. Last round (t=r): defect (standard backward‐induction endgame move).  

Why this is cooperative:  
– It fully cooperates whenever the group is fully cooperating, maximizing the public‐good bonus k/n·n = k each round.  
– It punishes unilateral or partial defection, so uncooperative strategies get a one‐round penalty in which our payoff is higher only if we defect against cooperators.  
– It is forgiving: after exactly one round of mutual defection, it returns to cooperation.  
– It defects in the final round to prevent exploitation by “sucker” cooperations when no future punishment is possible.  

This strategy encourages sustained group cooperation against defectors, never punishes forever (so cooperation can be reestablished), and handles both the first‐round startup and the last‐round endgame cleanly.
'''

description_COOPERATIVE_63 = '''
Below is a fully specified, cooperative‐minded strategy for the n-player repeated public-goods game.  It is a straightforward “collective tit-for-tat with one-round punishment and forgiveness,” combined with the inevitable last-round defection.  It achieves full cooperation whenever no one has just defected, punishes any observed defection for exactly one round, then forgives and returns to cooperation.  

1.  Data structures / variables  
   •   punished_last_round  (Boolean), initially false  

2.  Decision rules by round t  
   If t = 1 (first round):  
     action ← C  
   Else if t = r (last round):  
     action ← D  
   Else if punished_last_round = true:  
     // We just punished in this round – now forgive  
     action ← C  
     punished_last_round ← false  
   Else if (in round t–1) at least one player defected:  
     // Trigger a one‐round punishment  
     action ← D  
     punished_last_round ← true  
   Else  
     // Everyone cooperated last round → resume cooperation  
     action ← C  

3.  Explanation / rationale  
   •   First round: Cooperate to signal goodwill.  
   •   Ongoing rounds (t=2…r–1):  
     –  If nobody defected on the previous move, play C and build mutual trust.  
     –  If you observe any defection in the previous round, you defect exactly once.  
     –  After that one‐round punishment, you immediately return to cooperation (forgiveness).  
   •   Last round: Defect.  Backward induction implies that cooperation cannot be enforced here, so you secure the safe private payoff.  

4.  Properties  
   –  Cooperative: As long as the group remains fully cooperative, you continue to cooperate every round (except the last).  
   –  Retaliatory: A single defection by anyone leads to exactly one round of mutual defection, which lowers the defector’s payoff and deters future free-riding.  
   –  Forgiving: You never punish forever. After one-round retaliation, you resume cooperation, keeping the door open for rebuilding trust.  
   –  Simple to implement from public history (you only need to know if there was any defection last round and track a one‐round punishment flag).  

Pseudocode  

```
initialize punished_last_round ← false

for t in 1…r do
  if t = 1 then
    action[t] ← C

  else if t = r then
    action[t] ← D     // Last‐round defection

  else if punished_last_round = true then
    action[t] ← C
    punished_last_round ← false

  else
    // Examine last round’s contributions:
    if (total_contributors at t–1) < n then
      // Someone defected last round
      action[t] ← D
      punished_last_round ← true
    else
      // Unanimous cooperation last round
      action[t] ← C
    end if
  end if
end for
```

This strategy maximizes the chance of sustaining full cooperation in early rounds, imposes swift and finite punishment on deviators, and avoids getting locked into endless vendettas.  In the tournament you will reap the high group‐payoff equilibrium whenever other strategies are similarly cooperative, yet you remain protected against persistent free-riders.
'''

description_COOPERATIVE_64 = '''
Below is a single‐strategy description—“Limited Trigger with End‐Game Defection”—that (i) starts out fully cooperative, (ii) punishes any defection for a short, fixed number of rounds, (iii) then forgives and returns to cooperation, and (iv) defects in the final round to avoid being exploited in the last move.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
STRATEGY: “LIMITED TRIGGER WITH END-GAME DEFECTION”  
Parameters you must know:  
• n = number of players  
• r = total rounds (>1)  
• k = multiplication factor (1<k<n)  
• P = punishment length (we choose P=1 for simplicity; you may tune to P≥1)  

Memory/State variables:  
• punish_counter ← 0        // how many more rounds we will punish  
• last_round_defected? ← FALSE  

Decision rule at the start of each round t = 1,…,r:  
1. If t = r (the final round):  
     play D  
     (Rationale: in a one‐shot game defection strictly dominates cooperation.)  

2. Else if punish_counter > 0:  
     play D  
     punish_counter ← punish_counter − 1  
     (We are in the midst of punishing a previous defection.)  

3. Else if t = 1:  
     play C  
     (We “never defect first.”)  

4. Else (t ∈ {2,…,r−1} and punish_counter = 0):  
     • Observe total_contributions in round t−1:  
         Σ c_j,t−1  (how many cooperated last round)  
     • If Σ c_j,t−1 < n  (i.e. at least one defector last round):  
           punish_counter ← P  
           play D  
       Else (everyone cooperated last round):  
           play C  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
EXPLANATION / PROPERTIES  
1. “Never defect first”: starts round 1 with C.  
2. “Retaliate just enough”: upon seeing any defection, we defect for P consecutive rounds.  
3. “Forgiving”: after P punished rounds, we resume cooperation (so occasional mistakes don’t spiral into permanent defection).  
4. “End-game defection”: in round r we defect to protect against last‐round free‐riding.  
5. “Mutual cooperation” is a stable path: if all use this strategy, everyone plays C in rounds 1…r−1 and D in round r, yielding payoffs of (k) each round (except 1 in the last) rather than collapsing to full defection.  
6. “Punishment deters unilateral defection”: a single defector in round t reaps a one‐round gain but then suffers P rounds of mutual defection; if P and the parameters (n,k) are chosen so that the future loss outweighs the one‐shot gain, defection is disincentivized.  

PSEUDOCODE  
----------  
initialize punish_counter ← 0  
for t in 1..r:  
    if t == r:  
        action ← D  
    else if punish_counter > 0:  
        action ← D  
        punish_counter ← punish_counter − 1  
    else if t == 1:  
        action ← C  
    else:  
        observe total_C ← Σ_j c_j at round (t−1)  
        if total_C < n:  
            punish_counter ← P  
            action ← D  
        else:  
            action ← C  
    end  
    play action  
end  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy is simple, transparent, fosters cooperation, punishes deviation briefly, then forgives—and avoids the last‐round sucker problem.
'''

description_COOPERATIVE_65 = '''
Below is a single‐strategy policy (pseudocode plus verbal description) that tries to sustain near‐full cooperation in the N-player public‐goods game, punishes defection for a short fixed window, then forgives and returns to cooperation.  It also protects you against end‐game exploitation.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
VERBAL DESCRIPTION  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Parameters you choose once at the start:  
• P (integer ≥1): length of punishment (in rounds) following any observed defection.  
• t_safe (integer ≥1): number of last rounds in which you simply defect (to avoid being exploited at the very end).  

State variables you carry from one round to the next:  
• punishing_count (initially 0): how many more rounds you will defect to punish.  

Decision rule at round t (1 ≤ t ≤ r):  
1.  If t ≤ t_safe:  
      play D.  
2.  Else if t = 1 (and t_safe = 0):  
      play C.  
3.  Else if punishing_count > 0:  
      play D; decrement punishing_count by 1.  
4.  Else (not punishing, t not in “safe” end window, and t > 1):  
    • Look at last round’s actions of all n players.  
    • If everybody cooperated last round, play C.  
    • Otherwise (at least one defection observed),  
         – set punishing_count ← P–1  
         – play D (this is the first of P punishment rounds).  

Key properties:  
• You start by cooperating (unless you’ve elected t_safe ≥1, in which case you simply defect the last t_safe rounds).  
• You only defect to punish observed deviation, and you punish for exactly P rounds, then forgive and return to cooperation.  
• You ignore “mistakes” by forgiving after P rounds—this avoids endless mutual retaliation.  
• Rounds t in [r − t_safe + 1, …, r] are always defections, so you are not exploited in the known finite endgame.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
PSEUDOCODE  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Inputs (common knowledge):  
   n — number of players  
   r — total rounds  
   k — multiplier (1 < k < n)  
Parameters (choose once up front):  
   P ← 2           # length of punishment window  
   t_safe ← 1      # # of final rounds to automatically defect  
State:  
   punishing_count ← 0  

For t in 1..r:  
  if t > r – t_safe then  
    # Last t_safe rounds: avoid end‐game exploitation  
    action_t ← D  

  else if t == 1 and t_safe == 0 then  
    # First‐round cooperation (if not in safe window)  
    action_t ← C  

  else if punishing_count > 0 then  
    # We are in the middle of punishing a defection  
    action_t ← D  
    punishing_count ← punishing_count – 1  

  else  
    # Not punishing, not end‐game; inspect last round  
    Let history_{t–1} be the vector of all n actions in round t–1  
    if history_{t–1} == [C, C, …, C] then  
      action_t ← C    # everyone cooperated last time  
    else  
      # At least one defection observed → begin punishment  
      action_t ← D  
      punishing_count ← P – 1  

  Emit action_t  

End For  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
WHY THIS IS “COOPERATIVE”  
1. You always lead with C (unless you’re in the forced‐defect end window).  
2. You keep cooperating so long as the group does.  
3. You only withdraw cooperation to punish defectors—and only for a short, fixed P rounds—then you forgive.  
4. By defecting in the known final round(s), you guard against end‐game exploitation yet preserve cooperation in almost all of the interaction.  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
'''

description_COOPERATIVE_66 = '''
Below is a fully specified “threshold‐trigger” strategy that (1) starts out fully cooperative, (2) punishes any defection with a one‐round group defection, then immediately returns to cooperation, and (3) handles first and last rounds explicitly.  It is simple, transparent, and—provided the majority of players use it—sustains high levels of cooperation in the public‐goods game.  

––––––––––––––––––––  
Strategy name: Threshold‐One‐Round‐Punishment (T1P)  

Parameters (all common‐knowledge):  
• n = number of players  
• r = total rounds  
• k = multiplication factor (1 < k < n)  

Internal constants:  
• T = n–1   // threshold for “good” round (i.e. at most one defector)  
• M = 1     // length of punishment phase (in rounds)  

State variables (per player):  
• punish_timer ∈ {0,1,…,M}  // counts remaining punishment rounds  
• prev_coops ∈ {0,…,n}       // observed # of cooperators in t–1  

Initialization (before round 1):  
  punish_timer ← 0  
  prev_coops ← n   // imagine “last round” was full cooperation  

Decision rule (for round t = 1…r):  
  if t = 1 then  
    action ← C  
  else if t = r then  
    // Last round: defect to avoid end‐game free‐rider problem  
    action ← D  
  else if punish_timer > 0 then  
    // We are in punishment phase  
    action ← D  
    punish_timer ← punish_timer – 1  
  else  
    // Normal monitoring phase  
    if prev_coops ≥ T then  
      // Last round was (nearly) unanimous cooperation  
      action ← C  
    else  
      // Someone defected last round → punish for M rounds  
      action ← D  
      punish_timer ← M  
    end if  
  end if  

  Play(action)  

  // After observing all actions this round, record for next step  
  prev_coops ← number of players who played C in current round  

Pseudocode summary:  
```
initialize:
  punish_timer = 0
  prev_coops = n    // assume “good” history

for t in 1..r:
  if t == 1:
    action = C
  else if t == r:
    action = D
  else if punish_timer > 0:
    action = D
    punish_timer -= 1
  else:
    if prev_coops >= n-1:
      action = C
    else:
      action = D
      punish_timer = 1
    end if
  end if

  play(action)
  observe all actions
  prev_coops = count_C_in_this_round
end for
```

Rationale and properties:  
1.  First round cooperation “sets the bar” and signals willingness to build the public good.  
2.  If at most one player defects in round t–1 (i.e. prev_coops ≥ n–1), we assume it was accidental or forgivable and immediately resume cooperating.  
3.  If two or more defect (prev_coops < n–1), we issue a one‐round collective punishment (all defect for one round) so that defectors bear a cost.  After that single round of punishment we forgive and return to full cooperation.  
4.  In the last round (t = r) we defect to avoid the end-game incentive to free-ride (backward induction).  
5.  If the tournament contains a large fraction of T1P players, almost all rounds will see unanimous cooperation and yields payoffs close to k each round, which is Pareto‐superior to universal defection (payoff 1).  

Edge cases:  
• A single stray defection by any one player is forgiven (threshold T = n–1).  
• Two or more simultaneous defections trigger a one‐round group defection that punishes everyone, especially the defectors.  
• The one‐round punishment window (M = 1) is just long enough to deter repeat defections but short enough to restore cooperation quickly.  
• Last round defection is hard‐wired to avoid being exploited in the end‐game.  

This T1P strategy is fully cooperative yet robust: it rewards near‐unanimous cooperation, punishes sizeable breakdowns swiftly, and then returns to cooperation.
'''

description_COOPERATIVE_67 = '''
Below is a fully specified n-player “tit-for-tat with one-round punishment and endgame defection” strategy.  It (i) cooperates by default, (ii) punishes any defection by the group for exactly one round, (iii) forgives thereafter, and (iv) defects in the last round (since no future remains to enforce cooperation).

––––––––––––––––––––––––––––––––––––––––––––  
Strategy name  
  TFT-1P-End  

State variables  
  punished_remain ← 0    // how many remaining punishment rounds  

Parameters (no tuning needed)  
  none  

Decision rule for round t (1 ≤ t ≤ r):  
  if t == 1 then  
    action ← C           // start cooperatively  
  else if t == r then  
    action ← D           // no future left, defect in the last round  
  else if punished_remain > 0 then  
    // we are in punishment mode  
    punished_remain ← punished_remain − 1  
    action ← D  
  else  
    // normal mode, look at previous round’s plays  
    let num_defectors_last ← number of players j with action a_j,{t-1} = D  
    if num_defectors_last > 0 then  
      // trigger punishment for exactly one round  
      punished_remain ← 1  
      action ← D  
    else  
      // everyone cooperated last round → reward by cooperating  
      action ← C  
    end if  
  end if  

Pseudocode  
---------  
initialize punished_remain ← 0  

for t in 1..r do  
  if t == 1 then  
    play C  
    continue  
  end if  

  if t == r then  
    play D  
    continue  
  end if  

  if punished_remain > 0 then  
    punished_remain ← punished_remain − 1  
    play D  
    continue  
  end if  

  // inspect last round  
  observe actions a₁,{t−1}, …, aₙ,{t−1}  
  if ∃ j such that aⱼ,{t−1} = D then  
    // someone defected, punish for one full round  
    punished_remain ← 1  
    play D  
  else  
    // perfect cooperation last round  
    play C  
  end if  
end for  

Rationale  
---------  
1. First round cooperation “greets” opponents and establishes goodwill.  
2. Defections are met with exactly one full‐round group punishment, which is enough to deter unilateral deviation but not so harsh as to lock us into perpetual mutual defection.  
3. After the one‐round punishment we “forgive and forget,” immediately returning to cooperation if the group has repaired.  
4. In the last round (t = r) we defect, since no future punishment is possible—this is standard backward‐induction.  

Cooperative mindset  
-------------------  
– Encourages sustained mutual cooperation by rewarding any full‐cooperation round with a free cooperation next round.  
– Discourages free-riding via a swift, finite punishment that still allows the group to return to cooperation.  
– Does not over-punish: only one round of D, after which it immediately offers cooperation again.  
– Explicitly cooperates whenever the group’s last move was unanimous cooperation.
'''

description_COOPERATIVE_68 = '''
Below is a fully self‐contained, deterministic “group‐Tit-for-Tat with endgame forgiveness” strategy.  It is designed to (i) start by cooperating, (ii) punish any observed defection by defecting exactly once in the next round, (iii) forgive in the penultimate round to avoid wasted punishment with no future benefit, and (iv) defect in the final round (because no future rounds remain).  This simple trigger‐style rule is easy to implement yet strongly encourages mutual cooperation.

—–  
STRATEGY NAME  
Endgame-Forgiving Group Tit-for-Tat (EG-GTFT)

PARAMETERS  
n = number of players  
r = total rounds  

INTERNAL STATE  
None (only last round’s contribution history is needed)

NOTATION  
t = current round, 1 ≤ t ≤ r  
cᵢ,t ∈ {0,1} = your contribution in round t (1 = C; 0 = D)  
Cₜ = Σⱼ cⱼ,t = total number of cooperators in round t  

DECISION RULES  

1. Round 1 (t = 1):  
   Always cooperate.  
   cᵢ,1 ← 1  

2. Round r (final round, t = r):  
   Always defect.  
   cᵢ,r ← 0  

3. Round r–1 (penultimate round):  
   Forgive any past defection—cooperate unconditionally.  
   cᵢ,r–1 ← 1  

4. Intermediate rounds (2 ≤ t ≤ r–2):  
   • If everyone cooperated last round (Cₜ₋₁ = n), then cooperate:  
       cᵢ,t ← 1  
   • Otherwise (at least one defector in t–1), punish by defecting once:  
       cᵢ,t ← 0  

That’s it—only the previous round’s total contributions and the round index t are needed.

PSEUDOCODE  

```
for t in 1…r:
    if t == 1:
        play C     # start cooperatively
    else if t == r:
        play D     # last round: defect
    else if t == r - 1:
        play C     # penultimate: forgive any triggers
    else:
        # 2 ≤ t ≤ r - 2
        if C_prev == n:
            play C  # full cooperation last round  cooperate
        else:
            play D  # someone defected last round  punish
    # after all players act, observe C_t = sum of cooperators this round
    C_prev = C_t
```

EXPLANATION & PROPERTIES

• Cooperative Mindset  
  – Begins by cooperating.  
  – Returns to cooperation as soon as everyone’s back on board.  
  – Forgives past defections in the round before the endgame, so it never “throws away” a punishment where no future reward is possible.  

• Deterrence  
  – A single defection triggers exactly one round of punishment, imposing a cost on defectors equal to the foregone public‐good benefit.  

• Simplicity & Transparency  
  – Uses only one number from history (Cₜ₋₁) plus the current round index.  
  – No need for individual tracking or randomization.  

• Edge Cases  
  – First round: cooperate unconditionally.  
  – Penultimate round: forgive arbitrary past deviations (ensures any punishment still leaves at least one round to recoup).  
  – Final round: defect (standard backward‐induction “endgame” play).  

This strategy maximizes mutual cooperation in the early and middle phases, enforces a swift one‐round penalty for deviations, and avoids wasted endgame punishments—all consistent with a cooperative, welfare‐maximizing mindset.
'''

description_COOPERATIVE_69 = '''
Here is a simple “cooperator‐with–grim‐trigger‐and‐endgame‐defection” strategy.  It starts fully cooperative, punishes any defection by permanently withdrawing cooperation (grim trigger), but still defects in the known final round to avoid being exploited at the end.  In any tournament of strategies that value sustained cooperation, the threat of permanent punishment deters one–shot gains from defection, so you maintain mutual cooperation in almost every round.

1. State variables  
   • has_defected ← false  
     – Becomes true as soon as any player (including you) defects in any round t < r.  

2. Decision rule for round t (1 ≤ t ≤ r):  
   if t = 1 then  
     play C  
   else if t = r then  
     play D    // Defect in last round (endgame)  
   else  
     if has_defected = false  AND  last round’s total contributions = n then  
       play C  
     else  
       play D  

3. Update rule (after observing all contributions in round t):  
   if t < r  AND  (∃ j: c_j,t = 0) then  
     has_defected ← true  

Pseudocode for player i:

  initialize has_defected ← false

  for t in 1…r do
    if t = 1 then
      a_i,t ← C
    else if t = r then
      a_i,t ← D
    else
      if has_defected = false AND ∑_{j=1..n} c_j,t–1 = n then
        a_i,t ← C
      else
        a_i,t ← D
    end if

    wait for other players’ actions c_1,t … c_n,t
    if t < r AND (∃ j with c_j,t = 0) then
      has_defected ← true
    end if
  end for

Explanation of the three requirements:

1.  When exactly to cooperate vs. defect?  
    – Cooperate on round 1.  
    – In any round 2 ≤ t ≤ r–1, cooperate only if so far no one has ever defected AND everyone cooperated in the immediately preceding round.  Otherwise defect.  
    – Always defect in the final round r.  

2.  Edge‐case handling:  
    • First round (t=1): unconditionally cooperate to signal goodwill.  
    • Intermediate rounds: “grim trigger” ensures a single defection by any player triggers permanent withdrawal of cooperation—this punishes defectors so they have no one‐shot incentive to deviate.  
    • Last round (t=r): defect, since no future punishment is possible and cooperating can only be exploited.  

3.  Cooperative mindset:  
    – You begin by cooperating and will sustain full cooperation as long as no one defects.  
    – The threat of permanent punishment deters free‐riding.  If all players are “nice” (i.e. never defect), you achieve the Pareto‐efficient all‐C outcome in every round except the very last.  

This strategy is easy to implement, easy to explain to a tournament organizer, and—when faced with other strategies that seek to maximize long‐run payoffs—sustains mutual cooperation in all but the known final round.
'''

description_COOPERATIVE_70 = '''
Below is a single‐strategy recipe—“Conditional Cooperation with Finite Punishment & Forgiveness” (CC‐PF)—that is easy to describe, runs in O(r) time, and meets the three requirements:

1. Decision rules: when to Cooperate (C) vs Defect (D)  
2. Edge cases: first round, last round, burst punishments, forgiveness  
3. Cooperative mindset: starts by cooperating, only defects to discipline low‐cooperation, then forgives  

---

Strategy CC-PF  
Parameters you can tune (or fix once for the tournament):  
• pun_len = 2   # number of rounds to defect in punishment  
• ε = 0.1     # small forgiveness probability  
• T = ceil((n–1)/2) # threshold of other players’ C in last round  

State variables (per player i):  
• punishing: Boolean, initially False  
• pun_left: integer, initially 0  

Pseudocode (for player i):  
```
for t in 1…r:
    if t == 1:
        # No history, lead by example
        action_i[t] = C
        continue

    if t == r:
        # Standard backward‐induction: no future to enforce
        action_i[t] = D
        continue

    if punishing:
        # We are in punishment mode
        action_i[t] = D
        pun_left -= 1
        if pun_left == 0:
            punishing = False
        continue

    # Otherwise, look at history of round t–1
    let coop_prev = sum_{j ≠ i} c_j[t–1]  
        # number of other players who played C last round

    if coop_prev < T:
        # Group cooperated too little → punish for pun_len rounds
        punishing = True
        pun_left = pun_len
        action_i[t] = D
        continue

    # If we reach here, last round had "enough" cooperators
    if coop_prev < (n–1):
        # Someone defected last round but not enough to trigger full punishment
        with probability ε:
            action_i[t] = C    # forgive occasionally
        else:
            action_i[t] = D    # hold them to account
    else:
        # Full cooperation last round
        action_i[t] = C

# End for
```

Explanation of the core ideas  
– “Lead by example”: always start round 1 with C.  
– “Last‐round look”: we only react to observable group behavior in t–1.  
– “Threshold T”: if fewer than T of the other n–1 players cooperated last round, that implies serious breakdown → switch on a short punishment (defect for pun_len rounds).  
– “Finite punishment”: avoids collapse into permanent all-D (unlike grim‐trigger), so we can restore cooperation after pun_len.  
– “Forgiveness ε”: even if a single defection occurs, we don’t immediately punish forever; with small probability we forgive and cooperate to re‐establish trust.  
– “Endgame”: in the very last round any C cannot be reciprocated, so we defect.  

Why CC-PF is cooperative  
• It rewards full cooperation by always playing C when the group last cooperated.  
• It only defects to discipline persistent low cooperation, and it recovers quickly.  
• It is forgiving: a single slip by one player does not lead to permanent breakdown.  
• It is simple, transparent, and does not rely on any off-protocol communication.
'''

description_COOPERATIVE_71 = '''
Below is a simple, fully‐specified “forgiving trigger” strategy that (i) starts by cooperating, (ii) sustains full‐group cooperation as long as everyone cooperated in the immediately preceding round, (iii) punishes any one‐round defection by defecting once, then forgives, and (iv) in the very last round defects (since no future remains).

–––––––––––––––––––––––––––––––––––––––––––  
Forgiving‐Trigger Strategy  
Parameters:  
• n (players), r (rounds)  
• P = 1   ← punishment length (in rounds)  

State variables (maintained from round to round):  
• punish_remaining ← 0  

Decision rule (for you, player i) each round t = 1…r:  
1. If t == 1:  
      play C  
2. Else if t == r:  
      play D   // last‐round defection  
3. Else if punish_remaining > 0:  
      play D  
      punish_remaining ← punish_remaining − 1  
4. Else (t in 2…r−1 and not currently punishing):  
   • Let m = number of cooperators observed in round t−1  
   • If m == n:  
         play C  
     Else:  
         // someone defected last round → punish for P rounds  
         punish_remaining ← P  
         play D  

Pseudocode  

```
initialize punish_remaining ← 0

for t in 1 to r:
   if t == 1:
      action ← C

   else if t == r:
      action ← D

   else if punish_remaining > 0:
      action ← D
      punish_remaining ← punish_remaining − 1

   else:
      observe m ← # of C’s in round t−1
      if m == n:
         action ← C
      else:
         punish_remaining ← P   // start a one‐round punishment
         action ← D

   play(action)
end for
```

Explanation of how it meets the three requirements:

1. Specify decision rules  
   – First round: unconditionally cooperate.  
   – Intermediate rounds: if in the _previous_ round everyone cooperated, cooperate; if any defection occurred, defect this round (punishment) and then immediately forgive.  
   – Last round: defect (no future to incentivize cooperation).

2. Edge‐case handling  
   – Round 1 has no history → cooperate.  
   – Last round (t = r): always defect.  
   – Punishment never “overflows” past the last round because we explicitly defect there anyway.  

3. Cooperative mindset  
   – We begin by cooperating.  
   – We only defect to punish the _first_ defection we observe, and then we forgive—returning to full cooperation immediately if everyone reverts to C.  
   – By restricting punishment to a single round, we keep the expected future payoff of cooperation high for everyone, making cooperation the focal equilibrium.
'''

description_COOPERATIVE_72 = '''
Below is a single‐strategy (“Generous Threshold Tit-for-Tat”) that is easy to describe, punishes only when cooperation truly breaks down, forgives occasional lapses, and handles first‐ and last‐round edge cases cleanly.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
1.   Intuition and Rationale  
     •  We want to sustain full cooperation for as many rounds as possible.  
     •  We start by cooperating, and we continue cooperating so long as the group’s recent behavior signals that cooperation is still “alive.”  
     •  We only switch to defection when a clear majority of the group defects, and we “forgive” minor lapses (up to just under half the group).  
     •  In the very last round (round r), defection is a dominant action, so we defect there automatically.  

2.   Parameters  
     n  = number of players  
     r  = total rounds  
     T  = majority threshold = floor(n/2) + 1  

3.   Decision Rule (for player i)  
     For each round t = 1, 2, …, r:  
       if t == 1:  
         play C  
       else if t == r:  
         play D  
       else:  # 1 < t < r  
         let coop_{t–1} = number of players who chose C in round t–1  
         if coop_{t–1} ≥ T:  
           play C   # group is still largely cooperating  
         else:  
           play D   # majority defected last round  

4.   Pseudocode  

     initialize T ← floor(n/2) + 1  
     for t in 1..r do  
       if t == 1 then  
         action[t] ← C  
       else if t == r then  
         action[t] ← D  
       else  
         coop_count ← count of C’s among all players in round (t−1)  
         if coop_count ≥ T then  
           action[t] ← C  
         else  
           action[t] ← D  
       end if  
     end for  

5.   Why This Is Cooperative  
     •  First‐round cooperation “offers” a clean slate.  
     •  We only defect in intermediate rounds if a clear majority defected previously—so we punish only collective breakdown.  
     •  Because T > n/2, we forgive up to ⌊(n−1)/2⌋ simultaneous defections; this prevents endless “tit-for-tat” spirals from a few noisy mistakes or lone exploiters.  
     •  Defection in the last round is standard backward‐induction, but it does not undermine cooperation in earlier rounds.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

This strategy is fully specified, requires only the public history of each round’s C/D choices, and leans strongly toward cooperation whenever more than half of the group cooperated last time.
'''

description_COOPERATIVE_73 = '''
Below is a single‐strategy proposal—“Forgiving Trigger”—that (i) starts out fully cooperative, (ii) punishes any defection by everyone defecting for exactly one round, (iii) then immediately returns to cooperation, and (iv) defects in the very last round (since no future rounds remain in which a punishment threat can be credible).  This simple trigger‐and‐forgive rule is known to sustain high cooperation in finitely repeated public‐goods games among self‐interested players.

1.  Strategy name  
    Forgiving Trigger

2.  State variables  
    punish_until  ←  0   (round index up to which we are still punishing)

3.  Global parameters (known to all)  
    n  (number of players)  
    r  (total rounds)  
    P  ←  1   (fixed punishment length in rounds)

4.  Action rules, for each round t = 1…r:  
    a.  If t = 1 then  
          play C  
    b.  else if t = r then  
          play D  
    c.  else if t ≤ punish_until then  
          play D  
    d.  else  (t > punish_until, t < r)  
         •  Let S_prev = total contributions by all players in round t−1  
         •  If S_prev = n  (i.e. everyone cooperated last round)  
               play C  
            Else  (at least one defection observed last round)  
               punish_until ← t + P − 1  
               play D  

5.  Pseudocode  

    initialize punish_until ← 0

    for t in 1..r:
      if t == 1:
        action[t] ← C
      else if t == r:
        action[t] ← D
      else if t ≤ punish_until:
        action[t] ← D
      else:
        observe S_prev ← Σ_j c_j[t−1]
        if S_prev == n:
          action[t] ← C
        else:
          punish_until ← t + P − 1
          action[t] ← D

6.  Discussion and edge‐case handling  
  •  First round (t=1): we cannot yet punish, so we start with cooperation.  
  •  Punishment window: once any defection is seen, we defect for exactly P=1 round—enough to deter the deviator—then immediately return to cooperation.  
  •  Full‐return to cooperation prevents permanent break‐down from a single mistake or noise.  
  •  Last round (t=r): backward‐induction says defection is dominant, so we defect.  
  •  If multiple defections occur in a row, each will retrigger a one‐round punishment.  

This rule fosters near-full cooperation in early and middle rounds, enforces accountability for free-riding, but always “forgives” immediately so that a single defection does not lock the group into perpetual collapse.
'''

description_COOPERATIVE_74 = '''
Below is a simple “conditional‐cooperator” strategy that (i) begins by cooperating, (ii) defects only to punish observed free‐riding, then immediately forgives, and (iii) always defects in the very last round (to guard against end‐game exploitation).  This strategy requires nothing more than observing the total number of cooperators in the previous round.

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Strategy name: TFT‐PG (Tit‐for‐Tat for Public Goods)

Parameters:
  n  = number of players  
  r  = total rounds  
  A  = action set {C, D}  
  t  = current round, t=1…r  
  c_j[t] = 1 if player j cooperated in round t; 0 otherwise  
  totalC[t] = Σ_{j=1..n} c_j[t]

Pseudocode (for player i):

  Initialize:
    punishment_counter ← 0

  For each round t = 1…r do:

    if t == 1 then
      action_i[t] ← C
      continue to next round
    end

    if t == r then
      ▷ Last round: defect
      action_i[t] ← D
      continue
    end

    if punishment_counter > 0 then
      ▷ Punishment phase
      action_i[t] ← D
      punishment_counter ← punishment_counter – 1
      continue
    end

    ▷ From t=2 to r–1, no active punishment:
    if totalC[t–1] == n then
      ▷ Everyone cooperated last round ⇒ cooperate
      action_i[t] ← C
    else
      ▷ Someone defected last round ⇒ register 1‐round punishment
      punishment_counter ← 1
      action_i[t] ← D
    end

  end

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Explanation of design:

1. First round (t=1):  
   We start by cooperating, signaling willingness to build the public good.

2. Middle rounds (2 ≤ t ≤ r–1):  
   – If in round t–1 all n players cooperated, we cooperate again.  
   – If we observe ≥1 defection in t–1, we defect exactly once (punishment_counter=1) and then return to cooperation.  
   This one‐shot punishment deters persistent free‐riding but forgives a single lapse, allowing the group to re‐establish cooperation.

3. Last round (t=r):  
   Standard backward induction dictates that only defection is a Nash action in the final round of a finitely repeated public‐goods game.  By defecting here, we avoid being exploited by end‐game opportunists.

Cooperative mindset:
– We only defect to penalize observed defection, never out of pure opportunism in the middle of the game.  
– Punishments are as short as possible (1 round) so that after one “tit‐for‐tat” response we immediately resume cooperation.  
– Because everyone shares the same payoff rule, if all players adopt TFT‐PG, the group will converge to full cooperation in all rounds except the very last.

Edge‐case notes:
– If multiple defection events occur in rapid succession, each will trigger exactly one round of punishment; punishments do not stack up beyond one upcoming defection.  
– If one round’s punishment overlaps with a new defection in the same observed round, the “punishment_counter” does not increase beyond 1, thus capping retaliation and avoiding an endless war of attrition.  

This rule set is easy to implement, transparent, and—against “nice” or conditionally‐cooperative opponents—will sustain near‐full cooperation and high group payoffs.
'''

description_COOPERATIVE_75 = '''
Below is a single‐strategist recipe for “being as cooperative as you reasonably can” in an n‐player repeated public‐goods game, yet still punishing free‐riders and forgiving mistakes.  It is inspired by trigger and tit‐for‐tat ideas, but generalized to a multi‐player setting with limited punishment and automatic forgiveness.

1. Strategy name  
   “Generous Threshold with One‐Round Punishment”  

2. Intuition  
   – Start by cooperating.  
   – Continue cooperating as long as almost everyone cooperated last round.  
   – If defections slip in, defect for exactly one round (punishment), then return to cooperation if others do.  
   – In the known last round, defect (since no future to protect), but otherwise maintain full cooperation whenever possible.

3. Parameters  
   – n = number of players  
   – r = total rounds  
   – T = cooperation threshold = n–1  (i.e. tolerate one slip; if two or more defected last round, punish)

4. State variables  
   – punish_flag (boolean), initially false

5. High‐level pseudocode  

   initialize punish_flag ← false

   for t in 1…r do
     if t = 1 then
       action ← C                         # first‐move cooperation
     else if t = r then
       action ← D                         # last‐round defection (no future to protect)
     else
       let m ← number of cooperators in round t–1

       if punish_flag = true then
         # we are in a one‐round punishment
         action ← D
         if m = n then                   # if everybody cooperated last round, clear punishment
           punish_flag ← false
         end
       else
         # normal mode: check if others were “mostly” cooperative
         if m ≥ T then
           action ← C                     # enough cooperators → stay cooperative
         else
           action ← D                     # insufficient cooperation → punish
           punish_flag ← true
         end
       end
     end

     play action in round t
   end

6. Explanation of key features  
   A. “Mostly cooperative” threshold (T = n–1)  
      – Allows one accidental or strategic slip without collapsing cooperation.  
      – If two or more defect in the same round, we interpret it as a breakdown and punish.  
   B. One‐round punishment (punish_flag)  
      – Upon detecting breakdown (m < T), we defect exactly one round.  
      – If next round shows full cooperation (m = n), we forgive and resume cooperating.  
   C. Last‐round defection  
      – Standard backward-induction: no incentive to cooperate when no future punishments are possible.  
   D. First‐move cooperation  
      – Signals willingness to cooperate from the outset.  

7. Why it’s cooperative  
   – It almost always cooperates (in equilibrium when everyone conforms).  
   – It enforces cooperation by punishing real breakdowns of contributions.  
   – It forgives after a single round of universal cooperation, so noise or occasional exploiter doesn’t collapse the group forever.  

This strategy can be entered “as is” into a tournament.  It uses only publicly observed history of past contributions, punishes free‐riding in a limited way, and always returns to cooperation as soon as others do.
'''

description_COOPERATIVE_76 = '''
Below is a fully specified, “conditionally cooperative” strategy for the repeated N‐player public-goods game.  It is designed to

1.    Start by cooperating.  
2.    Continue cooperating so long as everyone cooperated in the previous round.  
3.    If any defection is observed, punish by defecting for a short, proportional period, then forgive and return to cooperation.  
4.    In the very last round, defect (since there is no future to protect).  

This “Limited Punishment Tit-for-Tat” style rule fosters cooperation, deters free-riding, but avoids endless retaliation.

––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: Limited Punishment TFT (LP-TFT)  

Parameters you can tune:  
•  P_max  – maximum punishment length (we suggest P_max = n – 1)  
•  Forgive immediately after P rounds of punishment  

State variables (maintained by our agent):  
•  punish_count (integer ≥ 0): how many more rounds to defect as punishment  

Pseudocode (player i’s decision each round t):  
----------------------------------------------------------------  
Input each round t:  
  history of all players’ actions in previous rounds  
  n, r, k  

Initialize at t = 1:  
  punish_count ← 0  

Action rule for round t:  
  if t == 1 then  
    play C  
    punish_count ← 0  
    return  
  end if  

  if t == r then  
    /* Last round: one‐shot incentives dominate */  
    play D  
    return  
  end if  

  if punish_count > 0 then  
    /* We are in punishment mode */  
    play D  
    punish_count ← punish_count – 1  
    return  
  end if  

  /* Otherwise, inspect last round */  
  let coop_last = number of players (including i) who played C in round t–1  
  let defectors_last = n – coop_last  

  if defectors_last > 0 then  
    /* Someone defected last round  punish for defectors_last rounds, capped by P_max */  
    punish_count ← min(defectors_last, P_max)  
    play D  
  else  
    /* Unanimous cooperation last round  reciprocate */  
    play C  
  end if  
----------------------------------------------------------------  

Explanation of key points  
1.  First round (t=1): always cooperate, to signal willingness.  
2.  Last round (t=r): always defect, as there is no future to protect.  
3.  Punishment:  
    –  When you observe any defection in round t–1, you defect for exactly D = min(number_of_defectors, P_max) subsequent rounds.  
    –  This proportional punishment ( more defectors ⇒ longer punishment ) sanctions bad behavior but limits the spiral of mutual defection.  
4.  Forgiveness:  
    –  After D consecutive punishment rounds, punish_count returns to 0 and you go back to cooperating, giving the group a fresh start.  

Why this is cooperative  
•  Mutual cooperation yields payoff = k each round, which (since k>1) strictly dominates the all-defect payoff of 1.  
•  By starting with C and returning to C whenever everyone did, the strategy sustains high cooperation.  
•  Proportional but bounded punishment deters defectors while guaranteeing that cooperation can resume quickly.  
•  Unconditional defection only in the final round avoids being exploited in a one‐shot game.  

Edge cases  
–  If multiple defections occur in one round, you punish for more rounds (up to P_max), but you do not over-punish permanently.  
–  If defections happen in the penultimate round, you might schedule punishments that overlap the last round—but since you defect in the last round anyway, consistency is maintained.  
–  If r is very small (e.g. r=2), you still play C in t=1, then D in t=2.  

Tunable aspects  
–  P_max controls how forgiving vs. harsh the punishment is. A small P_max (e.g. 1) is very forgiving; a larger P_max up to n–1 makes defection costlier.  
–  You could also experiment with only punishing if defectors_last > δ for some threshold δ>0, or with random forgiveness (“generous TFT”) to help against noise.  

This strategy strikes a balance between strong incentives to cooperate and a quick return to cooperation once the punishment phase is over.
'''

description_COOPERATIVE_77 = '''
Below is a single‐strategy profile (for an arbitrary player i) that tries to sustain full cooperation while still punishing any one‐off defection—but only for exactly one round—then forgiving and returning to cooperation.  It also defects in the last round (since there is no future to enforce cooperation there).

1.  State variables (per player i)  
   • punishment_flag ∈ {false,true}, initially false  
   • r = total number of rounds  

2.  Decision rules  
   — Round 1:  
     • Cooperate (C).  

   — For each round t = 2,…,r:  
     1.  If t == r, play Defect (D).  
     2.  Else if punishment_flag == true:  
           • Play C (we are “serving” our one‐round punishment, now forgive)  
           • Set punishment_flag := false  
     3.  Else (punishment_flag == false):  
         • Look at the immediately preceding round (t−1).  
         • If you observe any other player j≠i played D in round t−1, then:  
             – Set punishment_flag := true  
             – Play D (punish once)  
         • Otherwise (everyone else cooperated in t−1):  
             – Play C  

3.  Intuition and cooperation alignment  
   • We start by cooperating.  
   • If someone defects, we deny them—and everyone else—a public‐good share for exactly one round, then we immediately return to cooperation.  
   • By punishing defections promptly but only briefly, we raise the cost of any unilateral defection while not permanently locking the group into mutual defection.  
   • In the last round, since there is no future, we defect (standard end‐game logic).  

4.  Pseudocode  

   Initialize punishment_flag ← false  
   for t in 1…r do  
     if t == 1 then  
       action_i ← C  
     else if t == r then  
       action_i ← D  
     else if punishment_flag then  
       action_i ← C  
       punishment_flag ← false  
     else  
       if ∃ j≠i: action_j in round (t−1) == D then  
         punishment_flag ← true  
         action_i ← D  
       else  
         action_i ← C  
       end if  
     end if  
   end for  

5.  Handling edge cases  
   • First round: no history → cooperate.  
   • Immediately after a defection by any other player: punish exactly one round.  
   • Even if multiple players defect, we still punish only the next round once.  
   • We do not punish defections that occur during our own punishment round (so we forgive chain‐reactions).  
   • Last round: defect, because no future enforcement is possible.  

This “One‐Round Punishment with Forgiveness” strategy rewards full cooperation, deters one‐off deviations, but avoids the endless mutual defections of “grim‐trigger” and the coordination failures of naïve tit–for–tat in an n-player setting.
'''

description_COOPERATIVE_78 = '''
Below is a simple, one‐round‐memory “Tit-for-Tat”–style strategy adapted to a finite horizon public‐goods game.  It (a) starts out cooperating, (b) punishes any defection by defecting for exactly one round, then forgives, and (c) concedes that in the very last round there is no future to punish, so it defects.

1.  Decision rules  
   • Let r be the total number of rounds (common knowledge).  
   • Keep a single Boolean flag “punish_next” in memory, initialized false.  
   • In each round t (1 ≤ t ≤ r) choose:  
     – If t == r (the last round): play D.  
     – Else if t == 1: play C.  
     – Else if punish_next == true: play D.  
     – Else play C.  
   • After observing the actions of all n players in round t (and counting how many cooperated), update for use in round t+1:  
     punish_next ← (number_of_cooperators_in_round_t < n)  
       (i.e. if anybody defected in t, punish once in t+1; otherwise clear punish).  

2.  Pseudocode  

   initialize punish_next ← false  
   for t in 1…r do  
     if t == r then  
       action_t ← D  
     else if t == 1 then  
       action_t ← C  
     else if punish_next then  
       action_t ← D  
     else  
       action_t ← C  
     end if  

     play action_t  
     observe all n actions this round; let coop_count = # players who played C  

     if t < r then  
       punish_next ← (coop_count < n)  
     end if  
   end for  

3.  Rationale and edge-case handling  
   – First round (t=1): we cooperate to signal willingness.  
   – Middle rounds (2 ≤ t ≤ r−1): we cooperate whenever everyone cooperated last round; if any player defected, we punish by defecting exactly once, then immediately forgive provided there are no new defections.  This fosters re‐entry into full cooperation rather than endless “grim” punishment.  
   – Last round (t=r): we defect, since there is no future payoff to sustain cooperation by threat of punishment.  

By punishing defections just one round at a time, we keep cooperation stable and recover quickly from isolated mistakes, yet still deter persistent defectors.   
'''

description_COOPERATIVE_79 = '''
Below is a single‐strategy prescription, called “Generous Threshold Conditional Cooperator with Endgame Defection” (GTCC-ED).  It is designed to sustain near-full cooperation against similarly designed opponents, to forgive occasional stray defects, but to defect in the final round (to avoid being exploited in the endgame).

1.  Definitions  
   •  n = number of players  
   •  r = total rounds  
   •  t = current round (1 ≤ t ≤ r)  
   •  mₜ = number of cooperators observed in round t  
   •  Threshold T = n–1  (i.e. forgive one stray defector, but not two or more)  

2.  State variables  
   •  punish_flag ∈ {0,1}  
        –  punish_flag=1 means “I have just punished last round; next round I return to normal mode.”  
        –  punish_flag resets to 0 immediately after one punishment round.  

3.  Decision rule for each round t:  
   If t == 1:  
       Play C (cooperate).  
       punish_flag ← 0.  

   Else if t == r:  
       Play D (defect).  
       // endgame defection: no further rounds, so no future retaliation.  

   Else  // 2 ≤ t ≤ r–1  
       If punish_flag == 1 then  
           Play D  // carry out the one‐round punishment  
           punish_flag ← 0  
       Else  
           // Normal “generous threshold” mode  
           Observe mₜ₋₁ from last round  
           If mₜ₋₁ ≥ T then  
               Play C  
           Else  
               Play D  
               punish_flag ← 1  // punish for exactly one round after seeing ≥2 defectors  
           End if  
       End if  
   End if  

4.  Explanation of design choices  
   •  First round cooperation (“nice”): we never defect first.  
   •  Threshold T = n–1: we only punish if we saw two or more defectors last round, thereby being forgiving of a single random mistake or “noisy” opponent.  
   •  One‐round punishment: after defecting once, we immediately reset to normal mode.  This prevents endless retaliation (“grim”) and allows recovery to full cooperation.  
   •  Endgame defection: in the very last round, we defect because any cooperation there cannot be sustained or rewarded; rational opponents defect in round r, so we avoid being suckered.  

5.  Pseudocode  

   initialize punish_flag ← 0  
   for t in 1..r do  
     if t == 1 then  
       action[t] ← C  
       punish_flag ← 0  
     else if t == r then  
       action[t] ← D  
     else  // 2 ≤ t ≤ r–1  
       if punish_flag == 1 then  
         action[t] ← D  
         punish_flag ← 0  
       else  
         let m_prev ← number of C’s observed in round (t–1)  
         if m_prev ≥ n–1 then  
           action[t] ← C  
         else  
           action[t] ← D  
           punish_flag ← 1  
         end if  
       end if  
     end if  
   end for  

6.  Why this is cooperative  
   – It begins by cooperating and cooperates whenever almost everyone cooperated last round.  
   – It only punishes “bad” rounds (two or more defectors), and even then only for one round.  
   – Because most rounds remain cooperative, the public good is maximized.  
   – It defects in the last round (endgame) to avoid being exploited unilaterally when no future rounds exist to enforce cooperation.
'''

description_COOPERATIVE_80 = '''
Below is a single‐strategy description—“Forgiving Trigger”—that seeks to sustain high cooperation in an n-player repeated public-goods game while punishing defectors enough to deter repeated free‐riding, and forgiving isolated slip-ups so cooperation can recover.

Strategy name: Forgiving Trigger

Notation and state  
• r = total rounds, t = current round (1 ≤ t ≤ r)  
• P = punishment counter (integer ≥ 0), initially 0  
• history of play is public: in each past round we know exactly how many of the n players defected  

Decision rules  

1. Initialization (before round 1)  
   • Set P ← 0  

2. In each round t:  
   a. If t = 1 (no history yet):  
      – Action ← C  (start cooperatively)  
   b. Else if t = r (the last round):  
      – Action ← D  (standard backward-induction defection in the endgame)  
   c. Else if P > 0 (we are in a punishment phase):  
      – Action ← D  
      – Decrement P ← P – 1  
   d. Else (t > 1, t < r, and P = 0):  
      • Let d ← number of defectors in round t–1 (observed)  
      • If d = 0 (everyone cooperated last round):  
           Action ← C  
      • Else if d = 1 (exactly one defector):  
           – Set P ← 1   (punish for exactly one round beyond this one)  
           – Action ← D  (punish the lone defector)  
      • Else (d ≥ 2, two or more defectors):  
           – Set P ← (r – t)   (punish by defecting for all remaining rounds)  
           – Action ← D  

3. Summary of the “mindset” behind each rule  
   – We begin cooperatively; if everyone else does too, we keep cooperating.  
   – A single defection is punished with one turn of defection, but then we “forgive” and return to cooperation, allowing the group to recover full cooperation.  
   – If two or more players defect simultaneously, we interpret that as a breakdown of cooperation and defect for all remaining rounds (until the last, where we defect anyway).  
   – By defecting on the final round, we avoid being exploited by any strategy that might always contribute at the very end.  

Pseudocode  
```
initialize P ← 0
for t in 1…r do
  if t == 1 then
    play C
  else if t == r then
    play D
  else if P > 0 then
    play D
    P ← P − 1
  else
    d ← # of defectors in round t−1
    if d == 0 then
      play C
    else if d == 1 then
      P ← 1
      play D
    else  # d ≥ 2
      P ← r − t
      play D
    end if
  end if
end for
```

Why this is cooperative  
• It rewards full cooperation every round.  
• It punishes single defections just enough to deter further free-riding, yet forgives immediately so cooperation can be re-established.  
• It responds decisively to mass defection, preventing a persistent minority from undermining the public good.  
• The only defection in the endgame is to guard against last-round exploiters—otherwise it tries throughout to keep the group in a high‐cooperation basin of attraction.
'''

description_COOPERATIVE_81 = '''
Below is a single‐strategy description—pure, easy to implement, and explicitly “cooperative”—that you can drop into a tournament.  It is a forgiving, threshold‐trigger rule with brief punishment and full cooperation otherwise.  

1.  Parameters and state  
   •  n      = number of players  
   •  r      = total rounds  
   •  T_tol  = n – 1    (“tolerate at most one defector”)  
   •  P_len  = 1        (“punish for exactly one round”)  
   State variables (maintained across rounds):  
     – last_contrib_count  = number of cooperators observed in the previous round (initialize undefined)  
     – punish_timer        = 0 (counts remaining punishment rounds)  

2.  Intuition  
   – We begin by cooperating, hoping to establish full cooperation.  
   – As long as at most one player defected last round (i.e. last_contrib_count ≥ T_tol), we continue to cooperate.  
   – If two or more defected (last_contrib_count < T_tol), we defect for P_len rounds (punishing the group), then forgive.  
   – We do exactly the same rule in every round—including the last—because mutual cooperation every round always Pareto-dominates mutual defection.  

3.  Pseudocode  

```
Initialize:
  punish_timer        ← 0
  last_contrib_count  ← undefined

For each round t = 1 to r:
  if t == 1 then
    action ← C
  else
    if punish_timer > 0 then
      action ← D
      punish_timer ← punish_timer – 1
    else
      if last_contrib_count ≥ (n – 1) then
        action ← C
      else
        action ← D
        punish_timer ← P_len    # schedule a one‐round punishment
      end if
    end if
  end if

  Play action, then observe contributions of all players this round:
    last_contrib_count ← number of players who played C
end for
```

4.  Discussion of edge‐cases  
  •  First round (t=1): no history → we unconditionally cooperate.  
  •  Last round (t=r): we apply the same rule.  Even though backward induction “predicts” defection, pure cooperators in tournament usually earn more; so we stick to our rule.  
  •  Chains of defection: if two or more defect in one round, we punish exactly one round (P_len=1), then immediately return to cooperation if the group has re-cooperated.  
  •  Single “mistakes”: we tolerate one defector without ever punishing, so random slip-ups don’t derail cooperation.  

5.  Why it is cooperative  
  – We start by trusting everyone and never defect unless there is clear evidence of collective breakdown (≥2 defectors).  
  – Our punishment is finite and immediately reversible, so we never spiral into permanent defection.  
  – We always return to full cooperation as soon as others do.  
  – Over r rounds we support and stabilize the Pareto-efficient outcome (everybody plays C) while still defending against sustained free-riding.
'''

description_COOPERATIVE_82 = '''
Below is a single, simple “majority‐conditional” strategy that (i) starts by cooperating, (ii) sustains cooperation so long as a majority cooperated in the previous round, (iii) punishes when defection becomes the norm, and (iv) defects in the last round to avoid end‐game exploitation.  

—  
Name: Majority-Conditional Cooperator with End-game Defection  

1. Definitions  
   • Let n be the number of players, r the total rounds.  
   • In each round t, let Cₜ be the set of players who chose C, and Dₜ those who chose D.  
   • Let cₜ = |Cₜ|, dₜ = |Dₜ| = n − cₜ.  

2. Decision rule for player i in round t:  
   if t = 1 then  
     play C  ⟶ “open with cooperation.”  
   else if t = r then  
     play D  ⟶ “last‐round defection to avoid being exploited.”  
   else  
     if cₜ₋₁ ≥ dₜ₋₁ then  
       play C  ⟶ “if at least half cooperated last round, keep cooperating.”  
     else  
       play D  ⟶ “if defectors were in the majority last round, switch to punishment.”  

3. Rationale & cooperative mindset  
   • By cooperating in round 1, you invite cooperation.  
   • You only punish (defect) when the previous round’s majority defected—so isolated defections don’t derail cooperation.  
   • Once defectors regain the majority, you switch to defection to pressure them back toward cooperation.  
   • You return to cooperation immediately when the majority does so.  
   • Defecting in the final round is standard end‐game logic: there’s no future to protect, so you avoid being exploited in round r.  

4. Pseudocode  

```
Input: n (players), r (rounds)
For t in 1..r do
  if t == 1:
    action[i,t] ← C
  else if t == r:
    action[i,t] ← D
  else:
    let c_prev ← number of players who chose C in round (t−1)
    let d_prev ← n − c_prev
    if c_prev ≥ d_prev:
      action[i,t] ← C
    else:
      action[i,t] ← D
  end if
End for
```

5. Edge-case handling  
   • r = 2: Round 1 → C; Round 2 → D.  
   • If everyone defects in round t−1 (c_prev = 0), then you defect in t.  
   • If everyone cooperates in t−1 (d_prev = 0), you continue cooperating.  
   • Ties (c_prev = d_prev) count as “enough cooperation” → you choose C.  

This strategy is simple to implement, robust to occasional mistakes or noise, and encourages return to full cooperation as soon as the group majority resumes cooperating.
'''

description_COOPERATIVE_83 = '''
Below is a single‐strategy proposal, “Proportional Tit-for-Tat with Limited Punishment,” designed to sustain high cooperation in the n-player public‐goods game.  It meets the three requirements:

1. Decision rules – exactly when to cooperate (C) vs. defect (D)  
2. Edge cases – first round, last round, overlapping punishments  
3. Cooperative mindset – starts by trusting, punishes sparingly, forgives, and even in the last round leans toward cooperation  

—–  

I. Intuition and Parameters  
• We judge the “health” of the group by how many cooperated last round.  If a large enough subset cooperated, we continue cooperating.  
• If cooperation last round dips below a threshold, we punish by defecting for a short, fixed number of rounds (so that the group knows defection has a cost).  Then we forgive and return to cooperation.  

Parameters to fix before play begins:  
• Threshold M = ceil(n/2)  (a simple majority)  
• Punishment length P, e.g. P = 2 rounds  (long enough to deter, short enough to forgive)  

State variables (per player):  
• punishRemaining ∈ {0,1, … ,P} – how many more rounds we must defect as punishment  

—–  

II. Pseudocode  

Inputs:  
  n (number of players)  
  r (total rounds)  
  M = ceil(n/2)  
  P = 2  

Initialize:  
  punishRemaining ← 0  

For each round t = 1…r do:  
  if t == 1 then  
    action ← C           // 1) Always start by cooperating  
  else if t == r then  
    action ← C           // 2) In the last round, choose cooperation  
  else if punishRemaining > 0 then  
    action ← D           // 3) Punishment in progress  
    punishRemaining ← punishRemaining − 1  
  else  
    let coopLast ← number of players who played C in round (t−1)  
    if coopLast ≥ M then  
      action ← C         // 4a) Group was “healthy” last round ⇒ cooperate  
    else  
      action ← D         // 4b) Group cooperation fell short ⇒ begin punishment  
      punishRemaining ← P − 1  
    end if  
  end if  

  play action  
end for  

—–  

III. Discussion of Edge Cases  
1. First round: we unconditionally cooperate, signaling trust.  
2. Rounds during punishment: once we detect a “collapse” (coopLast < M), we defect for P total rounds, then reset.  We do not stack punishments—any defection during punishment does not extend it.  
3. Last round (t = r): we override any remaining punishment and cooperate.  Punishing in the last round only hurts future goodwill and cannot elicit any further cooperation, so we forgive.  

—–  

IV. Why This Is Cooperative  
• We always begin and end by cooperating.  
• We only defect in the interior when at least half the group defected in the previous round—thus we neither punish too harshly nor reward defection.  
• Punishments are limited in length and cannot cascade indefinitely.  After P punish rounds we return to cooperation.  
• Because everyone can observe group cooperation levels, similar strategies will self‐select toward rounds with high cooperation, and brief punishments discourage serial defectors without destroying prospects for return to cooperation.
'''

description_COOPERATIVE_84 = '''
Below is a fully‐specified, deterministic “conditional cooperator” that (1) starts by cooperating, (2) punishes any one‐round defection by any other player with exactly one round of defection, then forgives, and (3) defects on the very last round (since there is no future to protect).  This strike‐and‐forgive pattern supports high levels of cooperation early on but avoids being exploited at the end.

--------------------------------------------------------------------------------  
STRATEGY NAME  
  ConditionalCooperator‐with‐One‐Round‐Punishment  

PARAMETERS / STATE  
  • r       : total number of rounds  
  • t       : current round (1 ≤ t ≤ r)  
  • punish  : integer counter (initially 0)  
               – number of remaining rounds in which we must punish  

OBSERVABLE HISTORY  
  At the start of round t you know for every player j≠i their action c_j(t′) in each past round t′<t.

ACTION RULE (for player i)  
  For each round t = 1,2,…,r do:

  1. If t == 1 then  
       play C  
     (we always begin by cooperating).

  2. Else if t == r then  
       play D  
     (last round: defect, because no future remains to reward cooperation).

  3. Else if punish > 0 then  
       play D  
       punish ← punish − 1  
     (we are in a scheduled punishment phase: defect exactly punish more times, then return to normal.)

  4. Else  (t ∈ {2,…,r–1} and punish == 0)  
     – Look at the actions of the other n–1 players in round t–1.  
     – If any j≠i played D in round t–1, then  
         punish ← 1  
         play D  
       (we punish every defection by others exactly once in the very next round.)  
     – Otherwise (all others played C in t–1),  
         play C  
       (full return to cooperation).

That is all.  

--------------------------------------------------------------------------------  
PSEUDOCODE  

  initialize punish ← 0

  for t in 1…r:
    if t == 1:
      action ← C
    else if t == r:
      action ← D
    else if punish > 0:
      action ← D
      punish ← punish − 1
    else:
      # inspect other players’ actions in t−1
      if ∃ j≠i such that action_j(t−1) == D:
        punish ← 1
        action ← D
      else:
        action ← C

    play(action)

--------------------------------------------------------------------------------  
WHY THIS IS “COOPERATIVE”  
 • It begins with cooperation and thereby signals willingness to contribute.  
 • Any single defection by someone is met with exactly one round of collective defection—enough to make defection unprofitable in expectation, but not so harsh as to collapse cooperation forever.  
 • After the one‐round punishment, it immediately forgives if everyone else has resumed cooperating.  
 • By defecting on the very last round, it avoids being a “sucker” when no future reward is possible.  

Over a long horizon this strategy quickly stabilizes at full cooperation (all‐C) unless a defector tries to exploit; in that case they get punished once and then the group returns to mutual cooperation.
'''

description_COOPERATIVE_85 = '''
Below is a simple “grim‐trigger” style strategy that (i) cooperates as long as no one has ever defected, (ii) defects forever thereafter to punish any defection, and (iii) in the very last round defects anyway (since there is no future to protect).  In a tournament of identical strategies this yields full cooperation in rounds 1…r − 1 and mutual defection in round r.

1.  State variables  
    • triggered ← false     (becomes true as soon as any defection is observed)  
2.  Decision rule for each round t = 1,2,…,r:  
    if t == r then  
       play D   // last‐round defection by backward induction  
    else if triggered == false then  
       play C   // still “innocent,” continue cooperating  
    else  
       play D   // punishment phase: someone defected earlier  
3.  Observation update (after each round t < r):  
    if triggered == false and (∃ j such that player j played D in round t) then  
       triggered ← true  

Pseudocode

```
Initialize:
  triggered ← false

For t in 1 … r:
  if t == r:
    action[i] ← D
  else if triggered == false:
    action[i] ← C
  else:
    action[i] ← D

  // Play action[i] simultaneously with others,
  // then observe their contributions c_j ∈ {0,1}.

  if t < r and triggered == false:
    if ∃ j ∈ {1…n} with c_j == 0:
      triggered ← true
```

Explanation of behavior  
– First round (t=1): triggered==false and t≠r ⇒ play C.  
– As long as no one has defected in any prior round and t<r, you keep cooperating.  
– The moment you see a defection, you set triggered=true and from then on always defect (rounds t+1 … r).  
– In the final round t=r you defect regardless (no future to lose).  

This strategy is fully “cooperative” in the sense that if everyone plays it, you get full contributions (C) in rounds 1…r − 1, reaping the high public‐good payoff k each time, and only defect in the terminal round.  But it also enforces a harsh punishment (permanent defection) against any unilateral deviation.
'''

description_COOPERATIVE_86 = '''
Below is a single‐strategy description (“Forgiving Trigger with Endgame Defection”) that (i) starts out fully cooperative, (ii) punishes any defection by defecting exactly one round, then returns to cooperation, and (iii) defects in the known final round to avoid being exploited.  This strategy is simple, transparent, and—by forgiving quickly—minimizes long punishment cycles while still giving opponents an immediate cost for any defection.

1.  State variables  
    •  defection_flag: Boolean, initially false.  
    •  r: total number of rounds (known in advance).  

2.  High-level idea  
    – First round: cooperate.  
    – Rounds 2 through r–1:  
       •  If we are “punishing” (defection_flag = true), defect this round, then clear defection_flag.  
       •  Otherwise look at the immediately preceding round:  
         – If any player defected then set defection_flag = true and defect this round (start a one‐round punishment).  
         – Else (all cooperated last round) cooperate.  
    – Round r (the last round): defect (no future to punish).  

3.  Pseudocode  

    initialize defection_flag ← false  
    for t in 1..r do  
      if t == 1 then  
        action_t ← C    # start cooperatively  
      else if t == r then  
        action_t ← D    # endgame defection  
      else if defection_flag then  
        action_t ← D  
        defection_flag ← false  
      else  
        # inspect last round’s history  
        let coop_count_prev = number of players who cooperated in round t–1  
        if coop_count_prev < n then  
          # someone defected last round → punish once  
          action_t ← D  
          defection_flag ← true  
        else  
          # full cooperation last round → cooperate  
          action_t ← C  
        end  
      end  
    end  

4.  Explanation of rules and edge cases  
  A.  First round:  
     – We have no history → we choose C to signal willingness to cooperate.  
  B.  Middle rounds (2 … r–1):  
     – If we are in the “punish one round” state (defection_flag = true), we defect now, then immediately forgive (reset flag).  
     – Otherwise, we look only one round back.  If anyone defected then, we enter punishment this round; else we cooperate.  
     – This is a classic “Tit‐for‐Tat” style with one‐period punishment only—quick forgiveness avoids long chains of retaliation.  
  C.  Last round (t = r):  
     – Since no future remains, we defect to secure the larger private payoff.  This makes the strategy a subgame‐appropriate finite‐horizon trigger.  

5.  Cooperative mindset  
  – We never punish more than one round per defection.  
  – Whenever the group returns to full cooperation, we immediately cooperate.  
  – We do not build up long grudges (quick forgiveness).  
  – Start with a fully cooperative first move to invite cooperation.  

6.  Why this works in a tournament  
  – Against unconditional defectors: we suffer only one round of 1-payoff per defection, then go back to C hoping others will follow.  
  – Against other cooperators or forgiving strategies: we host essentially full cooperation for t=1…r–1, maximizing everybody’s payoffs.  
  – Against occasional defectors: they face a one‐round cost, so repeated defection is less attractive.  
  – Clear last‐round defection prevents exploitation by pure cooperators who would otherwise be “gamed” at t=r.  

You can tune this template in many ways (punishment length >1, inspect longer histories, vary endgame behavior), but the above strikes a balance between robust cooperation, simple rules, and fast recovery from mistakes.
'''

description_COOPERATIVE_87 = '''
Below is a single‐strategy design—let’s call it “Generous Conditional Cooperator”—that (i) begins by cooperating, (ii) sustains cooperation so long as others do, (iii) punishes defection only briefly, and (iv) defects in the final round (since there is no future to protect).

1.  State Variables  
    •  punishment_counter (integer ≥0): how many future rounds we will defect as “punishment.”  
    •  last_coop_frac (float in [0,1]): fraction of other players who cooperated in the immediately preceding round.

2.  Parameters (you can tune these)  
    •  α ∈ (0,1): cooperation threshold. If in the previous round at least α of the others cooperated, we feel “safe” to cooperate.  
      – e.g. α = 0.8 (80%).  
    •  T (positive integer): length of punishment when group cooperation falls below α.  
      – e.g. T = 1 (punish for exactly one round, then forgive).

3.  High‐Level Decision Rules  
    Round t’s action =  
      if t == 1:  
        Cooperate  (start by building trust)  
      else if t == r:  
        Defect     (final‐round defection is a Nash move)  
      else if punishment_counter > 0:  
        Defect and punishment_counter– –  (carry out punishment)  
      else if last_coop_frac ≥ α:  
        Cooperate  (the group has been sufficiently cooperative)  
      else:  
        Defect and set punishment_counter = T  (short punishment for low cooperation)

4.  Updating Variables After Each Round  
    After all players’ actions in round t are revealed:  
      let C_others = number of players ≠ you who played C in round t  
      last_coop_frac = C_others / (n–1)  
      (punishment_counter was decremented on your turn if you were in punishment mode; if you just entered punishment mode, it’s already set to T.)

5.  Pseudocode  

    initialize:
      punishment_counter ← 0
      last_coop_frac ← 1    # (pretend everyone cooperated before round 1)

    for t in 1..r:
      if t == 1:
        action ← C
      else if t == r:
        action ← D
      else if punishment_counter > 0:
        action ← D
        punishment_counter ← punishment_counter − 1
      else if last_coop_frac ≥ α:
        action ← C
      else:
        action ← D
        punishment_counter ← T

      play(action)

      # Observe others’ actions this round:
      observe actions of players 1..n
      C_others ← count of cooperators among players ≠ you
      last_coop_frac ← C_others / (n−1)

6.  Why This Is Cooperative  
    •  Starts with cooperation to signal willingness.  
    •  Forgives quickly—punishes for only T rounds when cooperation dips.  
    •  Resumes cooperation as soon as group behavior recovers (last_coop_frac ≥ α).  
    •  Defects only when it must (punishment or last round).  

7.  Edge‐Case Handling  
    •  First round: no history ⇒ cooperate.  
    •  Last round: no future ⇒ defect (Nash).  
    •  Single or occasional defections by others ⇒ brief, limited punishment prevents endless retaliation.  
    •  Large drops in cooperation ⇒ proportionate response: if many defect, we defect T rounds, then test group again.  

By tuning α and T, you trade off responsiveness to defection versus robustness to occasional “mistakes.”  With α high (e.g. 0.8–0.9) and T small (e.g. 1–2), you maintain a strongly cooperative posture while still deterring free‐riding.
'''

description_COOPERATIVE_88 = '''
Below is a fully specified “Generous N-Player Tit-for-Tat with Limited Punishment and End-Game Defense” strategy.  It (1) starts by cooperating, (2) cooperates as long as everyone else does, (3) punishes defection for a short fixed number of rounds, forgives thereafter, and (4) defects on the last round to forestall end-game exploitation.

1.  State variables  
   • punishment_counter ← 0   (counts remaining punishment rounds)  
   • last_round_allC ← true   (true if in the previous round all players chose C)  

2.  Parameters  
   • M ← 2   (length of punishment after any defection)  

3.  Decision rule for round t=1…r  
   if t = 1 then  
     action ← C  
   else if t = r then  
     action ← D      // last‐round defection to avoid being exploited  
   else if punishment_counter > 0 then  
     action ← D  
     punishment_counter ← punishment_counter – 1  
   else if last_round_allC = false then  
     // a defection occurred last round; start new punishment  
     action ← D  
     punishment_counter ← M – 1  
   else  
     action ← C      // everyone cooperated last round and no active punishment  
   end if  

4.  After observing all players’ actions in round t, update:  
   if (for every player j, j’s action at t = C) then  
     last_round_allC ← true  
   else  
     last_round_allC ← false  
   end if  

5.  Comments on strategic logic  
   • First-mover generosity: cooperating in round 1 sets a cooperative tone.  
   • Tit-for-tat in the group sense: if the group is fully cooperative, we stay cooperative.  
   • Limited punishment: we defect for M consecutive rounds whenever we see any defection, then forgive, which prevents endless mutual defection.  
   • End-game defense: we defect in the terminal round r to avoid being exploited by unconditional cooperators who know there is no future. This stops backward-induction unraveling from dooming earlier cooperation.  

6.  Edge cases  
   – If a defection occurs in round r–1, we will (correctly) defect in round r anyway.  
   – If r is very small (e.g. r=2), the logic still applies: we cooperate in round 1, defect in round 2.  
   – If multiple defections happen back-to-back, punishment_counter simply resets to M–1 each time we detect a new defection (so total punishment may be longer but still bounded).  

This strategy is simple, transparent and fosters cooperation by rewarding full-group C, punishing deviations just long enough to discourage free‐riding, but then forgiving so that one betrayal does not kill cooperation forever.
'''

description_COOPERATIVE_89 = '''
Below is a simple, deterministic “threshold‐reciprocity” strategy that (i) begins in full cooperation, (ii) rewards rounds in which a sufficient number of players cooperated, (iii) punishes (by defecting) when cooperation falls below a threshold, and (iv) defects in the last round.  It is designed to sustain high levels of cooperation yet still punish significant breakdowns.

— Strategy name:  Threshold-Reciprocity  —

Parameters (you can tune these if you like):  
• n = number of players  
• r = total rounds  
• T = ⌈n/2⌉   (a majority threshold)

Notation:  
• c_i,t ∈ {0,1} is i’s contribution in round t (1=C, 0=D)  
• coop₋1 = total cooperators among all players in round t–1 = Σ_j c_j,t–1  

Decision rules for player i at round t:

1.  If t = 1  ⇒  Play C (c_i,1 ← 1)  
2.  Else if t = r  ⇒  Play D (c_i,r ← 0)  
3.  Else  (2 ≤ t ≤ r–1):  
    •  Compute coop₋1 = Σ_j=1ⁿ c_j,t–1  
    •  If coop₋1 ≥ T  ⇒  Play C (c_i,t ← 1)  
    •  Else              ⇒  Play D (c_i,t ← 0)

Pseudocode

```
function ThresholdReciprocity(n, r, history):
    # history is a list of past rounds; 
    # history[t-1] is a length‐n vector of past actions c_j,t
    T = ceil(n/2)

    for t in 1…r:
        if t == 1:
            action[t] = C
        else if t == r:
            action[t] = D
        else:
            # count cooperators in previous round
            prev = history[t-1]           # list of c_j,t-1
            coop_prev = sum(prev)         # total C’s last round
            if coop_prev >= T:
                action[t] = C
            else:
                action[t] = D

    return action
```

Rationale  
1. First‐round cooperation jump‐starts the public good.  
2. For rounds 2…r–1, you “reward” the group by cooperating if a majority cooperated last round (coop₋1 ≥ T).  If too few cooperated, you withhold your contribution.  This punishes widespread defection while forgiving a small number of sporadic defectors (up to ⌊n/2⌋–1).  
3. In the final round you defect, since future retaliation is impossible and individual incentive dominates.  

Behavioral summary  
• Full cooperators sustain each other: if all n cooperated in t–1, then coop₋1 = n ≥ T, so you keep cooperating.  Over time this locks in full cooperation (π_i per round → k).  
• Occasional single defections (coop₋1 = n–1 ≥ T) are tolerated, so the strategy is fairly forgiving.  
• If cooperation collapses below a majority, you begin defecting until the group rebuilds (i.e. until coop₋1 ≥ T again).  
• The final‐round defection is standard in finitely repeated games.  

This rule set is simple, transparent, and enforces a cooperative norm (cooperate when most others do) while still punishing sustained low cooperation.
'''

description_COOPERATIVE_90 = '''
Below is a single‐player decision rule (“your” strategy) that is explicitly cooperative, punishes one‐shot defections, but quickly forgives, and takes account of the known finite horizon.  It is a public‐goods analogue of a generous tit-for-tat/trigger strategy with one‐round punishment.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  State variables  
    • punishing: Boolean flag, initially false  
    • punish_rounds_left: integer counter, initially 0  

2.  Parameters  
    • P = 1  (punish defectors for exactly 1 round)  
    • r = total number of rounds (known in advance)  
    • n, k as in the game spec.  

3.  High-level idea  
    – Round 1: cooperate unconditionally.  
    – In rounds 2…r–1:  
       • If you are “in punishment mode,” defect until that punishment expires (1 round), then revert to “cooperative mode.”  
       • Otherwise (“cooperative mode”): look at last round’s total contributions.  
          – If ALL n players cooperated last round ⇒ cooperate.  
          – If anybody defected last round ⇒ trigger a one‐round punishment: defect this round, then return to “cooperative mode.”  
    – Round r (the last round): defect (no future to enforce cooperation).  

4.  Pseudocode  

    initialize:  
      punishing ← false  
      punish_rounds_left ← 0  

    for t in 1…r:  
      if t == 1:  
        action ← C  
        continue to next round  

      if t == r:  
        # Last round ⇒ no incentive left to cooperate  
        action ← D  
        continue  

      # t in 2…r–1  
      if punishing == true:  
        action ← D  
        punish_rounds_left ← punish_rounds_left − 1  
        if punish_rounds_left == 0:  
          punishing ← false  
        end if  
        continue  

      # (we are in cooperative mode)  
      let last_contribs = Σ_{j=1..n} c_j^{t−1}   # how many cooperated last round  
      if last_contribs == n:  
        # Everyone cooperated last round  
        action ← C  
      else:  
        # At least one defector → punish them now  
        punishing ← true  
        punish_rounds_left ← P  
        action ← D  
      end if  

    end for  

5.  Intuition & properties  
  • Fully cooperative in round 1, and cooperates as long as the group was unanimous in the previous round.  
  • Single‐round trigger punishment: as soon as someone defects, you defect for exactly one round and then immediately forgive, returning to full cooperation if the group repairs itself.  
  • By defecting in the very last round, you avoid being the lone “sucker” when no future punishment is possible.  
  • This strategy is simple, transparent, and aligns incentives toward sustained cooperation while protecting you from persistent free-riding.
'''

description_COOPERATIVE_91 = '''
Below is a single‐pluggable strategy (“Tiered Trigger with Finite Punishment”) that tries to sustain high cooperation in an n‐player public‐goods game.  It starts out fully cooperative, punishes shortfalls in group cooperation for a fixed number of rounds, then forgives, and in the very last round it returns to cooperation no matter what.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  State variables and parameters  
   •  threshold τ = n – 1  
        – we require that at least (n–1) other players cooperated last round  
   •  punishment length P (integer ≥1), e.g. P=2  
   •  punish_timer ∈ {0,1,2,…,P}  (initially 0)  

2.  High‐level description  
   – Round 1: Cooperate unconditionally.  
   – Rounds 2…r–1 (“monitoring phase”):  
       •  If we are in a punishment spell (punish_timer>0), we defect and decrement punish_timer by 1.  Once punish_timer hits 0 we go back to monitoring.  
       •  Otherwise, we look at how many of the other n–1 players cooperated last round (call that m).  
           – If m≥τ  (i.e. all or all‐but‐one cooperated), we cooperate.  
           – Otherwise we “trigger” punishment: set punish_timer:=P and defect this round.  
   – Round r (last round): Cooperate unconditionally (to maximize collective payoff at the end).  

3.  Pseudocode  

  initialize punish_timer ← 0

  for t in 1..r do
    if t == 1 then
      action[t] ← C

    else if t == r then
      # Last round: return to cooperation no matter what
      action[t] ← C
      # (we could clear punish_timer here if desired)

    else
      if punish_timer > 0 then
        # We are in the middle of a punishment spell
        action[t] ← D
        punish_timer ← punish_timer – 1
        # if punish_timer hits 0, next round we'll resume monitoring

      else
        # monitoring mode
        let m ← number of cooperators among players j≠i in round t–1
        if m ≥ τ then
          action[t] ← C
        else
          # group cooperation fell below threshold → punish for P rounds
          punish_timer ← P
          action[t] ← D
        end if
      end if
    end if
  end for

4.  Why this is “cooperative”  
  •  It always opens with C and only defects to discipline low group cooperation.  
  •  The punishment is finite (length P) and then we forgive — we do not slide into permanent defection after a single slip.  
  •  By requiring τ = n–1 we are quite demanding (we only tolerate at most one “mistake” by others), but P can be tuned down (even P=1) if you want faster forgiveness.  
  •  In the very last round we unconditionally cooperate, so we never “throw away” a final public‐good contribution.  

5.  Handling edge cases  
  •  Small r (r ≤ P+1): the last‐round override ensures we never punish beyond the horizon.  
  •  Single defector: your P‐round punishment deters repeated free‐riding in practice, but you will return to cooperation if the defector resumes C.  
  •  All‐C groups: your strategy simply cooperates every round, yielding the maximal group payoff.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy is simple to implement, uses only public history of others’ actions, never relies on side‐channels or coordination, and focuses on sustaining high collective contributions while still protecting itself via brief, forgiving punishment.
'''

description_COOPERATIVE_92 = '''
Below is a simple, deterministic “tit‐for‐tat”–style strategy adapted to an n-player public goods game with a known finite horizon.  It (a) starts by cooperating, (b) punishes any defection by defecting one round, (c) immediately forgives if the group returns to full cooperation, and (d) always defects in the final round when no future punishment is credible.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Name: Finite-Horizon Tit-for-Tat (FH-TFT)

Intuition:  
• Encourage full cooperation by matching the group’s last move.  
• Punish any defection exactly one round, then return to cooperation if everyone else has.  
• Defect in the final round since there is no future to incentivize cooperation.  

Parameters (as given):  
 n = number of players  
 r = total rounds (r > 1)  
 k = multiplication factor (1 < k < n)  

Notation:  
 t = current round, 1 ≤ t ≤ r  
 history[t'] = vector of actions of all players in round t' (each entry “C” or “D”)  
 lastCooperators(t) = number of cooperators in round t  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Decision Rule (per round t)

if t == 1:  
 return C # always start by cooperating  

else if t == r:  
 return D # final round—defect (end game)  

else:  
 if lastCooperators(t–1) == n:  
  # everyone cooperated last round  
  return C  
 else:  
  # at least one defection to punish  
  return D  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
2. Pseudocode

function FH_TFT_Decision(t, history):  
 if t == 1:  
  action ← “C”  
 else if t == r:  
  action ← “D”  
 else:  
  nCoop ← count of “C” in history[t–1]  
  if nCoop == n:  
   action ← “C”  
  else:  
   action ← “D”  
 return action  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
3. Edge‐Case Handling

• First round (t=1): no history—choose C to signal cooperation.  
• Last round (t=r): defect—no future to enforce cooperation.  
• One‐round forgiveness: if you defect you will return to C as soon as the group is all-C again.  
• Persistent defectors: since you punish exactly one round per defection, a chronic defector will earn less than cooperators, but you avoid an endless “grim trigger” lock‐in.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
4. Cooperative Mindset

• You never defect preemptively; you only defect in response to observed defection.  
• You immediately reward a return to full cooperation.  
• By defecting only one round per observed defection, you keep the door open to re-establish cooperation.  
• You only defect in the very last round when backward‐induction destroys any incentive to cooperate.  

This FH-TFT strategy is simple, transparent, and fully contingent on observable behavior.  It promotes the socially efficient all-C outcome in almost all rounds whenever opponents are willing to cooperate, while still disciplining one‐shot or sporadic defectors.
'''

description_COOPERATIVE_93 = '''
Below is a simple “tit-for-tat with end-game defection” strategy that (1) starts by cooperating, (2) cooperates as long as everyone cooperated last round, (3) punishes any defection by defecting for exactly one future round, and (4) defects in the very last round to avoid being suckered when there is no future.  This strategy is known to sustain high cooperation in repeated public-goods games, is forgiving of one‐off mistakes, and handles the first, intermediate, and final rounds cleanly.

1.  State variables  
    •  punishment_counter ∈ {0,1}: How many more rounds I must defect as punishment.  
    •  r: total number of rounds (known).  
    •  t: current round index, t=1,…,r.  

2.  Initialization  
    •  punishment_counter ← 0  

3.  Each round t do:  
    if punishment_counter > 0 then  
       Action ← D  
       punishment_counter ← punishment_counter – 1  
    else if t == 1 then  
       Action ← C        // First move: build trust  
    else if t == r then  
       Action ← D        // Last round: no future to enforce cooperation  
    else if “at least one player (possibly including me) defected in round t–1” then  
       // Someone cheated us last round  
       Action ← D  
       punishment_counter ← 1   // Punish for exactly one subsequent round  
    else  
       Action ← C        // Everyone cooperated last round, so cooperate again  

4.  End.  

Explanation of key points  
– First round (t=1): we cooperate to signal our willingness to build the public good.  
– Intermediate rounds (1<t<r): we cooperate whenever the group was fully cooperative in the immediately preceding round.  The moment any defection is observed, we defect that round and also set punishment_counter=1 so that we continue to defect exactly one more round.  After that one-round punishment, we reset and are ready to forgive and return to cooperation if the group has again been all-C.  
– Last round (t=r): we unconditionally defect because there is no future from which to extract punishment, and defection strictly dominates cooperation in a one-shot public-goods choice.  

Why this is cooperative  
•  When all players follow the same rule, they all cooperate in every round except the very last, yielding near‐maximum total payoffs.  
•  A single defection by any player triggers only a one‐round punishment, after which the group immediately returns to cooperation—so occasional mistakes don’t lead to permanent breakdown.  
•  Because we do not maintain endless defection (a “grim trigger”) the strategy is more forgiving and supports sustained cooperation against noisy or slightly opportunistic opponents.  

Pseudocode  

```
Input: history H of past contributions by all n players, current round t, total rounds r
State: punishment_counter ∈ {0,1}  // initialized to 0

function decide_action(H, t, r):
    if punishment_counter > 0:
        punishment_counter ← punishment_counter – 1
        return D
    if t == 1:
        return C
    if t == r:
        return D
    // Check if any defection in the last round
    let last_round = t – 1
    if ∃ player j such that H[j][last_round] == D:
        // punish the defector(s)
        punishment_counter ← 1
        return D
    // otherwise, everyone cooperated last round
    return C
```

This strategy is simple to implement, robust to single defections, and—when played against like-minded strategies—yields high levels of cooperation and high total payoffs.
'''

description_COOPERATIVE_94 = '''
Below is a single‐strategy proposal—an “N-player Tit-for-Tat with Forgiveness and Endgame Defection.”  It is designed to support group cooperation but still defend against free riders, forgive occasional slips, and handle the inevitable last‐round defection.

1.  Informal description  
   • First move: Cooperate.  
   • Thereafter, at the start of round t (2 ≤ t ≤ r), observe the previous round’s contributions.  
       – If in round t−1 every player cooperated, then cooperate.  
       – If in round t−1 at least one player defected, enter a one‐round “punishment” by defecting this round, then automatically forgive (return to normal mode).  
   • Last round (t = r): Always defect.  (Standard end‐game defection.)  

   This strategy  
     – Rewards full cooperation immediately.  
     – If anyone defects, punishes exactly one round (so cooperators are not locked into endless mutual defection).  
     – Forgives after the one‐round punishment if others return to cooperation.  
     – Defects for sure in the final round, avoiding exploitation in the unavoidable end‐game.  

2.  Pseudocode  
```
INPUTS:
  n  = number of players (≥2)
  r  = total rounds (>1)
  history = list of past rounds; each entry is an array of contributions c_j ∈ {0,1}

STATE:
  punish_flag ← false

FOR t from 1 to r do
  if t == 1 then
    action ← C
    punish_flag ← false

  else if t == r then
    # Last round: defect for sure
    action ← D

  else
    # t in [2..r−1]
    if punish_flag == true then
      # we are serving our one‐round punishment
      action ← D
      punish_flag ← false

    else
      # inspect round t−1
      let prev_contributions = history[t−1]      # array of 0/1 by player
      let total_coop = sum(prev_contributions)
      if total_coop == n then
        # everyone cooperated last round
        action ← C
      else
        # at least one defection detected → punish next round
        action ← D
        punish_flag ← true
      end if
    end if
  end if

  # play action, then append your c_i (1 if C, 0 if D) to history for round t
END FOR
```

3.  Key features & edge cases  
  • First round (t=1): Unconditionally cooperate to signal willingness.  
  • Middle rounds (2≤t≤r−1):  
     – Cooperate if and only if the group was perfectly cooperative in the immediately preceding round.  
     – Punish any defection with exactly one round of defection, then forgive.  
  • Last round (t=r): Always defect—no future to incentivize.  

4.  Cooperative mindset alignment  
  – “I cooperation by default, but I will defend against repeated free riding.”  
  – One‐round punishment is harsh enough to deter systematic defection but short enough to restore cooperation quickly.  
  – Forgiveness ensures the group does not descend into mutual defection after a single mistake.  
  – By unconditionally defecting only in the last round, it accepts the backward‐induction end‐game while preserving cooperation as long as it can.
'''

description_COOPERATIVE_95 = '''
Below is a simple, fully‐specified “conditional cooperation” strategy that (a) starts out cooperating, (b) punishes any defection by any other player with exactly one round of defection, (c) then immediately returns to cooperation if others do, and (d) defects in the last round (to avoid being exploited in the end‐game).

––––––––––––––––––––––––––––––––––––––  
Strategy “1‐Round Punish, End‐Game Defect”  

Notation:  
• t = current round (1 ≤ t ≤ r)  
• c_j,t ∈ {0,1} = contribution of player j in round t (1 if C, 0 if D)  
• For our own player i, we observe all c_j,t for j≠i at the end of each round.

Decision Rule for round t:

1. If t = 1:  
    Play C (cooperate).  

2. Else if t = r:  
    Play D (defect).  

3. Else (1 < t < r):  
   Let others_last = Σ_{j≠i} c_j, t–1  
   If others_last = n–1  (i.e. every other player cooperated in t–1):  
       play C  
   Else  
       play D  

––––––––––––––––––––––––––––––––––––––  
Pseudocode  

```
function decide_action(t, history):
    # history is a list of past rounds’ contribution-vectors [c_1, …, c_n]
    # We are player i. We inspect only other players’ contributions.

    if t == 1:
        return C

    if t == r:
        return D

    # t in {2,3,…,r–1}
    let last_round = history[t–2]      # zero‐based index
    let sum_others = sum(last_round) – last_round[i]  
       # removes our own last action; 
       # if sum_others == n–1 then all others cooperated

    if sum_others == n–1:
        return C
    else:
        return D
```

––––––––––––––––––––––––––––––––––––––  
Explanation / Rationale

1. Cooperative start  
   We begin by cooperating, signaling our willingness to build the public good.  

2. One‐round punishment  
   If any other player defects in round t–1, then in round t we defect.  
   This (a) punishes defectors, and (b) is calibrated so that after our single‐round punishment they can “restore” cooperation—because we look only at others’ actions when deciding to cooperate again.  

3. Immediate forgiveness  
   As soon as *all* the other players have cooperated in the previous round, we return to cooperation ourselves.  

4. End‐game defection  
   In the final round t = r we defect, since any cooperative gesture at the end cannot be reciprocated and would only lower our own payoff.  

Together, these rules foster mutual cooperation for as many rounds as possible, deter free‐riding by imposing a swift but limited penalty, and avoid needless exploitation in the last period.
'''

description_COOPERATIVE_96 = '''
Below is a single‐strategy proposal—call it “One-Round Trigger with Endgame Defection” (OR-TED)—that attempts to sustain cooperation in the body of the game while guarding against free‐riders and the last‐round collapse.

1. Overview  
   OR-TED is a simple “tit-for-tat” style rule extended to the N-player public‐goods context, with a built-in endgame defect in the very last round to protect against backward‐induction exploitation.  It:  
   • Starts by cooperating.  
   • Cooperates as long as everyone cooperated last period.  
   • If anyone defected last period, defects exactly one period as a punishment, then returns to cooperation.  
   • Defects unconditionally in round r (the final round).

2. Benefits  
   • Encourages full‐group cooperation in all but rare “punishment” rounds.  
   • Punishes any defection immediately, so free‐riders pay a cost.  
   • Forgives after exactly one round of punishment, allowing group to return to maximum collective payoff.  
   • Protects itself in the final round, where cooperation is most vulnerable.

3. Detailed Decision Rules  

   Let t = current round (1 ≤ t ≤ r).  Let history H contain every player’s past actions.  Define  
     DefectedLastPeriod? = “there exists some player j whose action at round t−1 was D.”  

   Pseudocode:  
     for t in 1..r do  
       if t == 1 then  
         action_i(t) ← C        // No history yet, start cooperatively  
       else if t == r then  
         action_i(t) ← D        // Defect on the very last round  
       else  
         if DefectedLastPeriod? then  
           action_i(t) ← D      // Punish once for any defection  
         else  
           action_i(t) ← C      // Otherwise cooperate  
         end if  
       end if  
     end for

4. Handling Edge Cases  
   • First round (t=1): No observations yet ⇒ cooperate.  
   • Last round (t=r): Always defect (protects against endgame exploitation).  
   • If multiple defections occurred in t−1: still defect only in t, then revert.  
   • If a defection occurs in t−1 and you punish in t, but everyone recooperates in t: you will also cooperate in t+1.  
   • If a defection happens in the second-to-last round (t = r−1), you punish in t = r−1, then at t=r you still defect due to endgame rule.  

5. Why This Is Cooperative  
   – It gives every partner a chance to earn the full public-good return (k·n/n = k) in each nonpunishment round.  
   – It immediately penalizes defectors, making unilateral deviation unprofitable over time.  
   – It forgives swiftly, restoring full cooperation after a single punishment.  
   – By only defecting in the final round, it avoids dragging out punishment when there is no future to protect.

6. Tournament Considerations  
   In a pool of unknown LLM‐generated strategies, OR-TED will:  
   – Achieve high total payoff against unconditional cooperators.  
   – Discourage persistent defectors by depriving them of the public good for one round each time they stray.  
   – Avoid costly multiround vendettas, so it does not punish misfits indefinitely.  
   – Safeguard itself in the last round, avoiding exploitation by strategies that might defect then.

You can implement OR-TED exactly as given: it requires only one‐round memory, a known round count r, and the ability to observe last‐round contributions by all players.
'''

description_COOPERATIVE_97 = '''
Below is a “generous-threshold” trigger strategy that (1) starts fully cooperative, (2) forgives occasional slip-ups, (3) punishes repeated or mass defection, and (4) defects in the very last round (the only subgame-perfect move in a finite game without further rounds).

––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name  
  Generous Threshold Cooperation (GTC)  

Parameters you will know:  
  n = number of players  
  r = total rounds (r > 1)  
  f = forgiveness threshold (we set f = 1 by default)  

Intuition  
  • Cooperate in round 1 to “test the waters.”  
  • In each middle round, cooperate if defections last round were few (≤ f); otherwise defect to punish.  
  • Last round: defect (no future to enforce cooperation).  

1. Decision rules  
────────────────  
For each round t = 1, 2, …, r do:

  If t == 1:  
    action = C  
    “Open with cooperation.”  

  Else if t == r:  
    action = D  
    “Defect in the final round (no incentive to sustain cooperation afterward).”  

  Else (1 < t < r):  
    Let d = number of players who played D in round t–1.  
    If d ≤ f:  
      action = C  
      “Almost everyone cooperated last round (at worst 1 defector) → remain cooperative.”  
    Else:  
      action = D  
      “Too many defected last round → punish by defecting.”  

2. Edge-case handling  
────────────────────  
  • r = 2:  
      – Round 1: C.  
      – Round 2 (last): D.  
    You still get a cooperative first-round payoff and play the unique Nash defection in the last.  

  • f = 0 (zero forgiveness):  
      – This reduces to strict multi-player Tit-for-Tat with last-round defection.  

  • More generous settings (f > 1):  
      – You can tune f up to n–1 if you want to forgive up to f defectors.  

3. Why it is cooperative  
────────────────────────  
  – You always start by contributing your entire endowment.  
  – You only punish when you see repeated or mass defection (d > f); you forgive “one-off” or isolated D’s.  
  – You never “go on a revenge spree” beyond a single punishment round; once the defect-count falls back to ≤ f you resume cooperation.  

4. Pseudocode  
─────────────  
```
function GTC_decision(t, history, n, r, f=1):
    # history[t-1] is the vector of actions in the previous round,
    # with each element in {C, D}

    if t == 1:
        return C
    if t == r:
        return D

    # Count number of defectors in previous round
    d = count_D(history[t-1])

    if d <= f:
        return C
    else:
        return D
```

5. Tournament notes  
────────────────────  
  • This strategy earns the maximal mutual‐cooperation payoff (k) each round whenever others are mostly cooperative.  
  • It deters repeated defection by punishing when defections exceed f, but it is forgiving enough to recover cooperation.  
  • By defecting in the very last round, it is robust to backward induction and cannot be exploited in the end.
'''

description_COOPERATIVE_98 = '''
Below is a single‐strategy proposal, “Forgiving Trigger with Endgame Defection,” that (i) starts cooperatively, (ii) punishes any defection with exactly one round of defection, then forgives, and (iii) defects in the last round when there is no future to sustain cooperation.  It makes no assumptions about norms beyond what can be observed in play.

----------------------------------------------------------------------  
STRATEGY NAME  
  Forgiving Trigger with Endgame Defection

PARAMETERS  
  let r = total rounds  
  punish_length = 1      # number of rounds to punish after observing any defection  
  tolerance_threshold = 0 # number of defectors we tolerate before we punish (0→ punish on any defection)

STATE VARIABLES  
  punish_counter ← 0     # how many more rounds we will spend defecting as “punishment”

PROCEDURE FOR EACH ROUND t = 1,2,…,r

  1. Select action aᵢ(t):
     if t = 1 then
       aᵢ(t) ← C                   # First round: always cooperate
     else if t = r then
       aᵢ(t) ← D                   # Last round: defect (no future to enforce cooperation)
     else if punish_counter > 0 then
       aᵢ(t) ← D                   # We are in a punishment phase
       punish_counter ← punish_counter – 1
     else
       aᵢ(t) ← C                   # Otherwise, cooperate

  2. After everyone’s actions in round t are revealed, let  
       defectors_t = #{ j | player j played D in round t }  
     If defectors_t > tolerance_threshold then
       punish_counter ← punish_length

  3. Proceed to round t+1 (unless t = r, the game ends).

----------------------------------------------------------------------  
DISCUSSION

1. First Round  
   – We start by cooperating to signal willingness to build the public good.

2. Cooperative Phase  
   – As long as no one has defected in the immediately preceding round (and we are not in the last round), we cooperate.  
   – This keeps payoffs high for everyone if they also cooperate.

3. Punishment Phase  
   – Upon seeing any defection in round t, we set punish_counter = 1.  
   – In round t+1 we defect (punishing group defection).  
   – After exactly one round of punishment, we return to cooperation, giving opponents a fresh opportunity to cooperate.

4. Last Round  
   – In round r we defect, because no future retaliation or reward is possible (standard backward‐induction endgame).

5. Edge Cases  
   – If r=2: round 1 → C, round 2 (last) → D.  
   – If multiple defections occur back‐to‐back, we will continue to defect only if our 1‐round punish_counter is nonzero; otherwise we will cooperate.  
   – We never punish “forever” (avoids perpetual deadlock) but do signal that defection has a cost.

6. Why This Is Cooperative  
   – It rewards cooperation immediately.  
   – It deters defection by a guaranteed one‐round loss of public‐good payoff.  
   – It is forgiving: after exactly one round of punishment, it returns to cooperation, avoiding endless mutual defection.  
   – By defecting only in the last round, it maximizes cooperative gains throughout the game.

This strategy balances a credible threat (one‐round punishment) with generosity (quick forgiveness), and handles the inevitable endgame by defecting when no future enforcement is available.
'''

description_COOPERATIVE_99 = '''
Below is a simple, robust “forgiving‐unanimity” strategy.  It is cooperative, punishes deviations but immediately forgives, and handles first and last rounds explicitly.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Name  
  Forgiving-Unanimity

Intuition  
  • Start by cooperating.  
  • Whenever you observe a defection by anyone, defect exactly one round in retaliation.  Then immediately return to cooperation.  
  • In the very last round you defect (since there is no future to support cooperation).  

This fosters high levels of cooperation, still punishes one‐shot defections, but does not spiral into endless mutual punishment.

Parameters  
  n = number of players  
  r = total rounds  

Notation  
  c_i(t) ∈ {0,1} your action in round t (1=C, 0=D)  
  S(t) = Σ_{j=1..n} c_j(t) total cooperators in round t  

State variable  
  punish_next ∈ {false,true}  
    • true  = you owe one round of punishment (i.e. you’ll defect once)  
    • false = you are “on the baseline” (ready to cooperate if others did)  

Pseudocode  

```
initialize punish_next ← false

for t in 1…r do
   if t == 1 then
     // first round: no history, set the tone
     play C  (c_i(t) ← 1)
     punish_next ← false

   else if t == r then
     // last round: defection is dominant
     play D  (c_i(t) ← 0)

   else
     if punish_next == true then
       // carry out our one‐round punishment
       play D
       // after punishing once, clear the flag
       punish_next ← false

     else
       // we are “on the baseline”—decide based on last round’s unanimity
       if S(t–1) == n then
         // everyone cooperated last round → we keep cooperating
         play C
       else
         // saw at least one defection last round → punish once
         play D
         punish_next ← true
       end if
     end if
   end if

   // (after play, all players’ c_j(t) become known, so loop continues)
end for
```

Key properties  
1. First round cooperation establishes a cooperative signal.  
2. If no one defects, we keep cooperating every round except the guaranteed last‐round defection.  
3. A single observed defection triggers exactly one round of defection in response (“tit-for-one-touch”).  
4. After that one round of punishment, we immediately return to cooperation.  This limits the depth of retaliation and avoids endless mutual war.  
5. Last round we defect (since no future payoff hinges on cooperation).  

Why it’s cooperative  
– It attains near-full cooperation whenever opponents also want to cooperate.  
– It enforces a credible one-period penalty on defectors, deterring unilateral deviation.  
– It is forgiving: even if someone defects by mistake or in error, cooperation resumes immediately.  

This strikes a balance between discipline (punishing free‐riders) and forgiveness (never letting the group get stuck in perpetual defection).
'''

description_COOPERATIVE_100 = '''
Below is a simple “Cooperate–Punish–Forgive” strategy for the repeated N-player public‐goods game.  It

• starts by cooperating,  
• punishes any round in which someone defected by defecting once,  
• then immediately forgives and returns to cooperation,  
• and in the very last round defects (to grab the one‐shot benefit).  

This strategy is easy to describe, enforces high cooperation among well–behaved opponents, but does not allow a single slip (or exploitative defection) to collapse forever.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: Cooperate–Punish–Forgive (CPF)

State variables (per player i):  
  punishing? (boolean, initially false)  
  rounds-of-punishment_left (integer, initially 0)

Parameters:  
  r = total rounds  
  n = number of players  

Decision rule for player i in round t:

1.  If t == 1:  
      action_i = C  
    (start by cooperating)

2.  Else if t == r:  
      action_i = D  
    (last‐round defection to capture the private 1 point)

3.  Else  (2 ≤ t ≤ r−1):  
    a.  If punishing? == true:  
          action_i = D  
          rounds-of-punishment_left -= 1  
          If rounds-of-punishment_left == 0:  
            punishing? = false  
       (carry out the punishment for exactly one round, then clear it)  

    b.  Else if Σ_j c_j,(t−1) < n:  
          action_i = D  
          punishing? = true  
          rounds-of-punishment_left = 1  
       (if any one defected last round, punish this round)  

    c.  Else:  
          action_i = C  
       (if everyone cooperated last round, cooperate)

––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation

• First round: unconditionally cooperate to signal willingness.  
• Rounds 2 through r−1:  
    – As long as in the immediately preceding round everyone cooperated, continue to cooperate.  
    – If you observe even one defection in t−1, you defect once in t (punishment), then immediately reset and go back to cooperation in t+1.  
• Last round (t = r): defect.  In a finite game that is the optimal grab‐the‐1 point move, so we do it.

This achieves:

1.  High cooperative payoffs when opponents also cooperate.  
2.  A swift “one‐shot” punishment if anybody cheats, which deters unilateral defection.  
3.  Full forgiveness so cooperation can be re–established quickly.  
4.  A final‐round defection to secure the private benefit when no future rounds remain.
'''

description_COOPERATIVE_101 = '''
Below is a single-player “recipe” for a cooperative, trigger‐and‐forgive strategy in the n-player public-goods tournament.  It (a) always opens with cooperation, (b) punishes each observed defection by any other player for exactly one round, then (c) immediately returns to cooperation, and (d) never punishes your own “punishment move.”  No special end‐game logic is needed beyond this one‐round memory.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  State variables (for player i)  
   • punish_timer ← 0        // how many rounds of punishment remain  
   • last_others_allC ← true // did every OTHER player cooperate in the previous round?  

2.  Initialization (before round 1)  
   punish_timer ← 0  
   last_others_allC ← true  

3.  In each round t = 1…r:  
   if punish_timer > 0 then  
     action_i ← D                     // we are in punishment phase  
     punish_timer ← punish_timer – 1  
   else  
     if t == 1 then  
       action_i ← C                   // always start with cooperation  
     else  
       if last_others_allC == true then  
         action_i ← C                 // everyone else cooperated last round → cooperate  
       else  
         action_i ← D                 // someone defected last round → punish now  
         punish_timer ← 1             // punish exactly one future round  
       end if  
     end if  
   end if  

4.  After all actions of round t are publicly revealed, update:  
   last_others_allC ← true if and only if for every j ≠ i, player j’s action in round t was C.  
   (If any other j defected, set last_others_allC ← false.)  

5.  Repeat steps 3–4 until t = r.  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Explanation of why this is cooperative:  
 • You always begin by contributing, giving the group a chance to build trust.  
 • You only ever punish “in response” to observed defections by others, and punish for exactly one round—then you forgive immediately.  
 • You do not compound punishments or hold grudges: as soon as others resume full‐cooperation, you resume cooperating.  
 • There is no “unraveling” of end-game logic; you treat the last round just like any other.  

Variants and tuning:  
 • Punishment length can be increased (e.g. punish_timer ← p >1) to raise the deterrent.  
 • You can soften your trigger by requiring a threshold (e.g. “punish only if more than k₀ players defected”) rather than any defection.  
 • You can add “generosity” by sometimes cooperating even when last_others_allC == false (e.g. with small probability ε), to repair accidental breakdowns.  

This “one‐round‐tit-for-tat” in groups is simple, transparent, and maximally supportive of mutual cooperation while still deterring free-riding.
'''

description_COOPERATIVE_102 = '''
Below is a simple, deterministic “one‐round‐punishment” strategy that (i) starts fully cooperative, (ii) punishes any defection by defecting exactly one round, then returns to cooperation, and (iii) applies consistently even in the last round.  It is easy to implement, hard‐to‐exploit in a tournament of similar strategies, and clearly “cooperative‐minded.”

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy Name: TFT-1 (“Tit-for-Tat with One-Round Punishment”)

State:
  punish_until_round  ← 0    # the last round in which we will defect as punishment

Decision rule for each round t = 1…r:
  if t == 1 then
    play C
  else if t ≤ punish_until_round then
    play D
  else
    let m = number of cooperators observed in round (t–1)  # ∑_j c_j,t–1
    if m < n then
      # someone defected last round → punish this round
      punish_until_round ← t
      play D
    else
      # no defections last round → cooperate
      play C
    end if
  end if

Edge cases:
  • Round 1: Unconditionally cooperate (builds trust).  
  • Punishment: Lasts exactly one round.  If you observe any defection in t–1, you defect in t then reset.  
  • Last round (t = r): The same rule applies.  Even in the final round, if you are “in punishment” (t ≤ punish_until_round) you defect; otherwise you cooperate if everybody cooperated in r–1, else you defect.  

Why this is cooperative:
  1. You always start by cooperating.  
  2. You only defect to directly punish observed free‐riding, and you do so for one round only.  
  3. You promptly return to cooperation, preventing endless mutual defection.  
  4. You never pre‐emptively defect; your only defections are targeted responses that can deter exploitation but preserve high mutual payoffs when others cooperate.

Pseudocode Summary:

  initialize punish_until_round ← 0

  for t in 1…r do
    if t == 1 then
      action_t ← C
    else if t ≤ punish_until_round then
      action_t ← D
    else
      observe m = total cooperators in round t–1
      if m < n then
        punish_until_round ← t
        action_t ← D
      else
        action_t ← C
      end if
    end if
  end for

This strategy achieves near–efficient outcomes (everyone cooperates) as long as others are willing to cooperate; it deters defectors by immediately withholding cooperation for one round, then forgives, thus sustaining cooperation over the repeated game.
'''

description_COOPERATIVE_103 = '''
Below is a strategy we’ll call “Forgiving Threshold Tit-for-Tat” (FTfT).  It is designed to sustain high cooperation in an n-player Public Goods Game by (1) starting cooperatively, (2) punishing defections when they occur, and (3) forgiving occasional mistakes so that the group can quickly re–lock into mutual cooperation.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Parameters  
  • n  : number of players  
  • r  : total rounds (r > 1 known in advance)  
  • T  : forgiveness threshold = n – 1  (we tolerate at most one defection in the previous round)  
  • f  : small forgiveness probability ∈ (0, 1) (to allow recovery if punished incorrectly)  

Notation  
  • c_j(t–1) ∈ {0,1} = contribution of player j in round t–1  
  • M(t–1) = Σ_{j=1..n} c_j(t–1) = total cooperators in last round  
  • a_i(t) ∈ {C,D} = our action in round t  

Strategy Description  
1.  Round 1: a_i(1) = C.  
2.  For rounds t = 2,3,…,r:  
     if M(t–1) ≥ T then  
       a_i(t) = C  
     else  
       with probability f: a_i(t) = C   (forgive and attempt to re-cooperate)  
       otherwise          : a_i(t) = D   (punish by defecting)  
3.  Edge‐case, last round (t = r): we apply the same rule.  We do not “unwind” cooperation just because it’s the known final move—instead we rely on the fact that all players see we continue to reward cooperation right through round r.  

Rationale  
– By cooperating in round 1 we signal willingness to build the public good.  
– We only defect in response to “too many” defections last round (M < n–1), so single accidental defects are forgiven.  
– Forgiveness probability f > 0 means that after a punishment-defection cycle, there is always a chance we’ll return to cooperation, preventing permanent collapse.  
– Applying the same rule in the last round keeps incentives aligned, since others will see no guaranteed last-round defection from us and have an incentive to keep cooperating even late in the game.  

Pseudocode  

```
Inputs: n, r, f  // number of players, total rounds, forgiveness probability
Define T = n - 1

Initialize:
  // Round 1: always cooperate
  a_i(1) = C

For t in 2..r:
  Observe M = sum of contributions in round t-1   // each c_j(t-1)=1 if cooperated, 0 if defected

  if M >= T then
    a_i(t) = C
  else
    Draw u ~ Uniform(0,1)
    if u < f then
      a_i(t) = C   // forgive
    else
      a_i(t) = D   // punish
```

Choice of f  
– A small f (e.g. 0.05–0.10) is typical: it keeps punishment credible yet allows fairly rapid recovery.  

Why it’s cooperative  
– When all players play FTfT, M(t–1) will almost always be = n, so everyone cooperates every round, yielding the Pareto‐optimal path.  
– Any unilateral defector is immediately punished, deterring free‐riding.  
– Occasional noise or mistakes do not trigger permanent breakdown, because we forgive with probability f next round.  

This simple rule set requires no side‐agreements or secret channels, uses only publicly observed contributions, and balances stern punishment with generous forgiveness to sustain high cooperation throughout all r rounds.
'''

description_COOPERATIVE_104 = '''
Below is a simple “Grim‐trigger with one‐round endgame defection” strategy.  It aims for full cooperation as long as nobody ever defects, but it also recognizes the unavoidable incentive to defect in the very last period of a finite‐horizon game.

—–  
HIGH‐LEVEL DESCRIPTION  
1. Start by cooperating.  
2. If you ever observe any player defect in any previous round, switch to permanent defection (Grim trigger).  
3. If you are still in the “no‐defection‐ever” state but it is the last round t = r, defect (endgame incentive).  
4. Otherwise cooperate.

This achieves (i) maximal cooperation throughout almost the entire game, (ii) a credible punishment for any defection, and (iii) acknowledgement that in the final round cooperation cannot be enforced.

—–  
PSEUDOCODE  

Variables:  
  triggered ← false    # has any defection been seen so far?  

For each round t = 1 to r do:  
  if triggered = true then  
    action_t ← D       # once triggered, defect forever  
  else if t = r then  
    action_t ← D       # last‐round endgame defection  
  else  
    action_t ← C       # otherwise, cooperate  

  # Play action_t simultaneously.  
  # After observing all players’ actions this round, update trigger:  
  if any player j chose D in round t then  
    triggered ← true  

End for

—–  
DETAILS & EDGE CASES  
1. First round (t=1): triggered is false and t<r, so you play C.  
2. Intermediate rounds (1<t<r): if no defection has ever been observed, you continue to play C.  The moment any D appears in the history, you set triggered=true and from that point play D forever.  
3. Last round (t=r): even if no one has ever defected, you play D, since the one‐shot incentive to defect cannot be credibly punished thereafter.  

—–  
COOPERATIVE MINDSET  
• You give every opponent the opportunity to build trust—cooperating unconditionally until someone defects.  
• You impose the strongest possible deterrent (permanent defection) as soon as any defection occurs.  
• You accept the unavoidable final‐round defection, but by delaying it to the very last round you maximize collective payoffs in all earlier rounds.
'''

description_COOPERATIVE_105 = '''
Below is a simple “conditional‐cooperator” that (i) starts by cooperating, (ii) punishes any defection with exactly one round of defection, (iii) then immediately forgives and returns to cooperation, and (iv) always defects in the very last round.  This strategy is easy to state, easy to implement, and (empirically) supports high cooperation against like‐minded strategies while protecting you from serial exploiters.

1.  State variables  
    •  last_round_allC: Boolean, did everyone cooperate in the previous round?  
    •  punishment_active: Boolean, are we in the one‐round punishment phase?  

2.  Initialization (before round 1)  
    last_round_allC ← true  
    punishment_active ← false  

3.  Action rule at round t  
    if t = r then  
        play D    // last‐round defection  
    else if t = 1 then  
        play C    // unconditionally start with cooperation  
    else  
        if punishment_active then  
            play D    // carry out one‐round punishment  
        else if last_round_allC then  
            play C    // everyone cooperated last time → keep cooperating  
        else  
            play D    // someone defected last time → punish this round  

4.  Update after observing the contributions c₁,…,cₙ in round t  
    // first detect whether all cooperated  
    if (c₁ + … + cₙ) = n then  
        new_last_round_allC ← true  
    else  
        new_last_round_allC ← false  

    // set up punishment for exactly one round  
    if punishment_active = false and new_last_round_allC = false then  
        new_punishment_active ← true  
    else  
        new_punishment_active ← false  

    last_round_allC ← new_last_round_allC  
    punishment_active ← new_punishment_active  

5.  Intuition & Cooperative Alignment  
   •  Starting with C and rewarding all‐C with continued C builds mutual gains.  
   •  A single‐round “tit‐for‐tat” punishment deters exploitation but limits the cost of punishing.  
   •  Immediate forgiveness avoids endless mutual defection after a single mistake.  
   •  Defecting in the very last round is forced by backward induction—no future remains to protect.  

Pseudocode summary  
```
initialize:
  last_round_allC = true
  punishment_active = false

for t in 1..r:
  if t == r:
    action = D
  else if t == 1:
    action = C
  else if punishment_active:
    action = D
  else if last_round_allC:
    action = C
  else:
    action = D

  observe contributions c[1..n]
  allC = (sum(c) == n)

  // if someone defected last round, punish next round for exactly one turn
  if not punishment_active and not allC:
    punishment_active = true
  else:
    punishment_active = false

  last_round_allC = allC
```

This strategy is fully specified, needs no hidden assumptions, and—when matched against similarly conditional cooperators—sustains near‐full cooperation until the final round.
'''

description_COOPERATIVE_106 = '''
Below is a “forgiving‐trigger” strategy that (1) starts out fully cooperative, (2) punishes only when many players defect, (3) quickly forgives isolated defections, and (4) defects in the very last round to guard against end‐game exploitation.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy Name: Forgiving‐Trigger with Last‐Round Defection  
Parameters you choose in advance:  
• P = number of punishment rounds after a serious breach (we suggest P = 1 or 2)  
• T_defect = minimum # of defectors in one round to trigger punishment (we suggest T_defect = 2)  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Variables (maintained by each player i):  
• punish_remain ← 0    (how many more rounds to punish)  

At the start of each round t, observe H_{t–1}: the total # of cooperators c̄ = Σ_j c_j in the previous round.  

Decision rule for round t:

1. If t == r  (the final round)  
   • Action_i(t) ← D  
   (Unconditionally defect in last round to avoid being exploited.)  

2. Else if t == 1  
   • Action_i(t) ← C  
   (Start by cooperating.)  

3. Else if punish_remain > 0  
   • Action_i(t) ← D  
   • punish_remain ← punish_remain – 1  
   (Serve out the punishment phase.)  

4. Else  (t in 2…r–1 and no active punishment)  
   Let n_def = n – c̄  (number of defectors in previous round).  
   If n_def ≥ T_defect  
     • Action_i(t) ← D  
     • punish_remain ← P  
     (A serious breach—punish for P rounds.)  
   Else  
     • Action_i(t) ← C  
     (Otherwise, cooperate; single or zero defections forgiven.)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of the design choices:

• Cooperate in round 1 to signal willingness.  
• Forgive up to T_defect–1 defectors so that accidental or one‐off drops in cooperation do not lead to a permanent breakdown.  
• When many players defect in the same round (n_def ≥ T_defect), defect for exactly P rounds to impose a cost on defectors—and then return to cooperation.  
• Defect in the very last round to avoid the one‐shot temptation.  

This strategy is cooperative (it only punishes clear mass defections and otherwise sustains full cooperation), it is forgiving (it does not hold grudges against a lone defector), and it accounts for the edge case of the final round.
'''

description_COOPERATIVE_107 = '''
Below is a simple, fully‐distributed “N-player Tit-for-Tat with Forgiveness” strategy.  It (1) starts by cooperating, (2) cooperates whenever all other players cooperated in the last round, (3) punishes any defection by defecting for exactly one round, then (4) immediately forgives and returns to cooperation.  The last round is always cooperated to reward any lingering cooperation.

— Strategy name: N-TFT-F (“N-player Tit-for-Tat with 1-round Forgiveness”)

1.  State variables (per player i):
    •  punish_flag (boolean) – have we just entered our one‐round punishment mode?  
       Initialize punish_flag = false.

2.  Decision rule (for each round t = 1…r):
    if t == 1 then
        action_i ← C
        punish_flag ← false
        continue to next round
    end if

    if t == r then
        /* Always cooperate in the final round to maximize group payoff */
        action_i ← C
        punish_flag ← false
        continue
    end if

    if punish_flag == true then
        /* We are serving out our one‐round punishment */
        action_i ← C
        punish_flag ← false
        continue
    end if

    /* Otherwise, inspect last round’s actions of the other n−1 players */
    Let coop_others = Σ_{j ≠ i} c_{j, t−1}   /* count of cooperators among opponents */
    if coop_others == (n − 1) then
        /* everyone else cooperated last round → reward with cooperation now */
        action_i ← C
    else
        /* at least one other defected last round → punish by defecting this round */
        action_i ← D
        punish_flag ← true
    end if

3.  Explanation of components:
    – First round: cooperates unconditionally to signal goodwill.  
    – Ongoing play: “if they all cooperated, I cooperate; if anyone defects, I defect once.”  
    – Forgiveness: the one‐round punish_flag guarantees we do not spiral into permanent defection.  
    – Last round: cooperate to reward any cooperation history; no further rounds remain to exploit.  

4.  Why it’s cooperative:
    •  It maximizes mutual contributions whenever possible (full‐cooperation equilibrium).  
    •  Its punishment is minimal—only one round—so it quickly returns to full cooperation.  
    •  It never punishes beyond one round, avoiding costly mutual defection cascades.  
    •  By cooperating in the final round, it upholds the spirit of group welfare, even if others might defect unpunished thereafter.

5.  Pseudocode summary:

    initialize punish_flag = false

    for t in 1…r do
      if t == 1 then
        action_i = C
        punish_flag = false

      else if t == r then
        action_i = C
        punish_flag = false

      else if punish_flag == true then
        action_i = C
        punish_flag = false

      else
        coop_others = sum over j≠i of c_{j, t−1}
        if coop_others == n−1 then
          action_i = C
        else
          action_i = D
          punish_flag = true
        end if
      end if
    end for

This strategy is entirely self‐contained, uses only public history of contributions, and balances deterrence of free‐riding with a swift return to full cooperation.
'''

description_COOPERATIVE_108 = '''
Below is a simple, fully‐specified “conditional‐cooperate‐with‐one‐round‐punishment” strategy.  It meets the requirements:

1.  It starts out cooperative.  
2.  It punishes any defection by any player with exactly one round of defection.  
3.  It then immediately forgives (returns to cooperation).  
4.  It applies the same rule in the last round (so if the group was all‐cooperative in r–1 you’ll cooperate in r; if there was a defection in r–1 you punish once in r).  

This strategy is robust against permanent defectors (you’ll switch to all‐D if everyone else is all‐D), but sustains full cooperation if all players adopt similarly retaliatory‐forgiving rules.

-------------------
STRATEGY DESCRIPTION  
-------------------

State variables (initialized at the start of the game):
  punish_until_round ← 0

At the beginning of each round t = 1…r:
  if t = 1 then  
    play C  ▷ start cooperatively  
  else  
    if t ≤ punish_until_round then  
      play D  ▷ we are still punishing  
    else if “any player defected in round (t–1)” then  
      ▷ trigger one‐round punishment  
      punish_until_round ← t  
      play D  
    else  
      play C  ▷ full cooperation last round, so cooperate now  
    end  
  end

Explanation of the key lines:
- punish_until_round records the round number up to which we should defect.  
- As soon as we observe any defection in round (t–1), we set punish_until_round to t, so that we defect exactly in round t and no longer punish in t+1.  
- If there were no defections in t–1, and we are not in a punishment window, we cooperate.  

Edge cases:
- First round (t=1): we have no history, so we cooperate.  
- Last round (t=r): we apply the same rule.  If round r–1 was all-C, we cooperate in the finale; if someone defected in r–1, we punish once in round r.  
- If all other players always defect, then after round 1 our rule sees defection in 1, defects in 2, and because round 2 was also all‐D it continues to punish every subsequent round.  Thus we never return to being exploited.  

-------------------
PSEUDOCODE  
-------------------

Initialize:
  punish_until_round ← 0

For t in 1…r do:
  if t = 1 then
    action[t] ← C
  else
    if t ≤ punish_until_round then
      action[t] ← D
    else
      if exists i∈{1…n} with action[i at round (t–1)] = D then
        punish_until_round ← t
        action[t] ← D
      else
        action[t] ← C
      end
    end
  end
end

-------------------
WHY THIS IS COOPERATIVE  
-------------------
1. It always gives the group an opportunity to re-establish full cooperation after exactly one round of punishment.  
2. Full cooperation by all opponents leads to perpetual mutual cooperation (the socially optimal path).  
3. Occasional mistakes or one‐off defections are punished but immediately forgiven; there is no permanent “grim‐trigger.”  
4. Against pure defectors, it will defect from then on, so it is not exploitable.  

This strategy therefore strongly encourages and sustains cooperation in a population of similarly‐minded opponents, yet defends itself against systematic defectors.
'''

description_COOPERATIVE_109 = '''
Below is a simple yet robust “group–Tit-for-Tat” style strategy that (1) starts by cooperating, (2) punishes any defection by the group for exactly one round, (3) then returns to cooperation, and (4) defects in the very last round (since no future punishment is possible).  This strategy is fully specified without relying on off‐game communication or coordination devices.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  State variables  
    • r            total number of rounds  
    • n            total number of players  
    • t            current round, t=1,…,r  
    • HistC[t–1]   number of cooperators in round t–1 (observed at the start of round t)  
    • c_i[t]       our action in round t: 1=C (cooperate) or 0=D (defect)  

2.  Decision rule (for each round t):  
    if t == 1:  
        play C  (c_i[1] = 1)  
    else if t == r:  
        play D  (c_i[r] = 0)    // no future, so defect in final round  
    else:  
        if HistC[t–1] == n:     // everyone (including ourselves) cooperated last round  
            play C  (c_i[t] = 1)  
        else                     // at least one defector observed last round  
            play D  (c_i[t] = 0)  

3.  Explanation / intuition  
  • Round 1:  Signal cooperation.  
  • Rounds 2…r−1:  Cooperate if—and only if—the entire group cooperated in the immediately preceding round.  
       – If any defection was observed in t–1, pun-ish by defecting once in round t.  
       – In t+1 we will again see if full cooperation returned; if so, we resume cooperating.  
  • Round r:  Defect—there is no future in which to deter or punish, so cooperation would be purely exploitable.  

4.  Properties  
  – Cooperativeness:  As long as the group remains fully cooperative, we never defect (through round r−1).  
  – Deterrence:  Any defection by even one player triggers exactly one round of “punishment” (defection), after which we forgive if full cooperation has returned.  
  – Simplicity:  No memory beyond the last round, no bookkeeping of which individuals defected—only the total count.  
  – Endgame handling:  Defection in the final round avoids being taken advantage of when there is no opportunity for retaliation.  

5.  Pseudocode  

  initialize r, n  
  for t in 1…r:  
      if t == 1:  
          c_i[t] ← 1            // cooper­ate in first round  
      else if t == r:  
          c_i[t] ← 0            // defect in last round  
      else:  
          if HistC[t–1] == n:   // full cooperation last round?  
              c_i[t] ← 1        // continue to cooperate  
          else:  
              c_i[t] ← 0        // punish by defecting  

  // At the end of each round t, observe all players’ actions, set  
  // HistC[t] = total # of players who played C in round t  
  // then proceed to round t+1.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

This strategy is purely reactive, fully cooperative when reciprocated, punishes defections just enough to deter exploitation, and correctly handles the first and last rounds.
'''

description_COOPERATIVE_110 = '''
Below is a self-contained, cooperative yet self-interested strategy for the r-round n-player public-goods game.  It is a “limited-punishment trigger” rule: start by cooperating, reward full cooperation, but if anyone defects punish for a short, fixed number of rounds, then return to cooperation.  In the very last round it defects to capture the one-shot gain.

1.  PARAMETERS  
 •  n ≥ 2, r > 1, 1 < k < n  (known to all)  
 •  L = 1  (punishment length; you may choose L ≥ 1 but L≪r)

2.  INTERNAL STATE  
 •  pun_remaining ← 0  (rounds left in punishment mode)

3.  DECISION RULE (each round t = 1,2,…,r)  
 if t == 1 then  
  action ← C  
 else if t == r then  
  // Last round: unilateral defection maximizes one-shot payoff  
  action ← D  
 else if pun_remaining > 0 then  
  // Currently punishing  
  action ← D  
  pun_remaining ← pun_remaining − 1  
 else  
  // Not punishing: check last round’s history  
  if (# cooperators in round t−1) == n then  
   // Everybody cooperated last round ⇒ reward by cooperating  
   action ← C  
  else  
   // At least one defection observed ⇒ enter punishment  
   action ← D  
   pun_remaining ← L  
  end if  
 end if  

4.  EXPLANATION OF COMPONENTS  
 •  First round (t=1): cooperate to establish goodwill and signal friendliness.  
 •  Full-cooperation check: if everyone cooperated last round, you keep cooperating.  
 •  Trigger & limited punishment: as soon as you see any defection, you defect L rounds to lower the defector’s future benefit.  Then you forgive and return to cooperation.  
 •  Last round (t=r): defect to capture the private endowment (standard backward-induction escape).  

5.  WHY THIS IS COOPERATIVE  
 •  If all players adopt it, the path is C,C,…,C until t=r, yielding maximal public-good payoffs.  
 •  Any lone defection triggers only a short, finite punishment—no endless vendettas—so cooperators regain joint cooperation quickly.  
 •  The threat of losing k/n per round for L rounds deters unilateral deviation when discounting is mild (or when players care about total sum of payoffs).  

6.  PSEUDOCODE SUMMARY  
```
initialize pun_remaining = 0

for t in 1..r do
  if t == 1 then
    play C
  else if t == r then
    play D
  else if pun_remaining > 0 then
    play D
    pun_remaining -= 1
  else
    if last_round_cooperators == n then
      play C
    else
      play D
      pun_remaining = L
    end
  end
end
```

Edge cases:  
- If multiple defections occur back-to-back, pun_remaining simply resets to L at the first detection and counts down; subsequent defections during punishing do not extend it (avoiding spirals).  
- If r–t < L when you enter punishment near the end, you will punish until r, but since you defect anyway in round r, you do not need special handling.  

This “Limited-Punishment Trigger” is simple, transparent, and strongly promotes mutual cooperation across the first r–1 rounds.
'''

description_COOPERATIVE_111 = '''
Here is a single, fully‐specified “cooperative” strategy for the repeated n-player Public-Goods Game.  It is in the spirit of Tit-for-Tat but tailored to n-players, with a one‐round forgiveness rule to avoid endless punishing and no special end-game defections.  

–––  
Strategy name: Forgiving Public-Goods TFT  

Parameters your strategy uses: none beyond the common knowledge n, r, k and full history of past contributions.  

1.  Data structures (memory)  
   •  You only need to remember, from the previous round t–1, the vector of contributions c₁, …, cₙ (0 = D, 1 = C).  
   •  No additional counters or timers are required.  

2.  Decision rule in round t = 1 (first round)  
   Play C.  (Start by cooperating.)  

3.  Decision rule in rounds t = 2, 3, …, r (subsequent rounds)  
   Let d = the number of defectors in the previous round, i.e.  
     d  =  ∑_{j=1..n} (1 – cⱼ,t–1)  

   A.  If d = 0 (all cooperated last round)  
         →  Cooperate (C).  

   B.  Else if d = 1 and you yourself cooperated in t–1 (cᵢ,t–1 = 1)  
         →  Cooperate (C).  
       (This is a single‐defection “forgiveness” rule.  If exactly one person slipped, assume it was a mistake.)  

   C.  Otherwise (d ≥ 2, or you were the lone defector last time)  
         →  Defect (D).  

4.  No separate last‐round rule  
   We apply the same rule even in round r.  This avoids inviting an end-game rush to defect (and preserves cooperation as long as it is being reciprocated).  

5.  Why this is cooperative:  
   •  You always begin by signaling full cooperation.  
   •  You only punish when you see two or more defectors (i.e. clear, deliberate group defection).  
   •  You forgive a single defection (keeps you from locking into eternal mutual punishment over isolated slips).  
   •  You immediately return to cooperation as soon as the group returns to near-full cooperation.  

6.  Pseudocode  

   function chooseAction(t, history):  
     if t == 1:  
       return C  
     else:  
       // read last round contributions  
       let lastContribs = history[t–1]    // array of 0/1 of length n  
       let d = count of zeros in lastContribs  
       let myLast = lastContribs[i]       // your own 0/1 last round  
       if d == 0:  
         return C  
       else if d == 1 and myLast == 1:  
         return C  
       else:  
         return D  

7.  Robustness and alignment with cooperation  
   –  If everyone else plays the same strategy, the path will be: all C every round → each gets π = k each round → social optimum.  
   –  If some defect, you stop cooperating only if there is clear, repeated defection; isolated mistakes get forgiven at once.  
   –  Because you never unconditionally defect in the last round, you continue to reward cooperation even late in the game, helping sustain group returns.  

–––  
This strategy is simple, interpretable, and fully cooperative in intent. It punishes only clear multi‐party defection, forgives isolated slips, and otherwise maintains full cooperation throughout.
'''

description_COOPERATIVE_112 = '''
Below is a self‐contained, easy-to-implement strategy for the n-player public-goods game.  It is cooperative (“tries to sustain full cooperation”), punishes defection, but then quickly forgives so cooperation can be restored.  In simulations this kind of “one-round punishment” rule (sometimes called a generous multi-player Tit-for-Tat) tends to achieve and maintain high cooperation against many plausible opponents.

––––––––––––––––––––––––––––––––––––––––––  
Name: Threshold-Forgiving (TF)  
––––––––––––––––––––––––––––––––––––––––––  

Parameters you may tune (but reasonable defaults are given below):  
• P = 1  (punishment length in rounds)  
•   (you can increase P if you want harsher, longer punishment)  

Notation:  
•  t = 1,…,r is the round index  
•  c_i,t ∈ {0,1} is your contribution in round t (1=C, 0=D)  
•  C_t  = Σ_j c_j,t is the total cooperators in round t  
•  state ∈ {Cooperate, Punish} is your internal mode  
•  punish_counter ≥ 0  

OVERVIEW  
1.  Round 1: always Cooperate.  
2.  Thereafter, if in Cooperate state and you saw any defection last round, switch to Punish state and defect for P rounds.  
3.  In Punish state you defect until punish_counter expires, then return to Cooperate.  
4.  Round r (last round): always Defect (no future to punish).  

This “one‐round punishment” (P = 1) rule deters unilateral defection but quickly forgives, restoring full cooperation if all revert.  

––––––––––––––––––––––––––––––––––––––––––  
PSEUDOCODE  
––––––––––––––––––––––––––––––––––––––––––  
Initialize:  
 state ← “Cooperate”  
 punish_counter ← 0  

For each round t = 1 to r:  
 if t == 1:  
  // First move – set the cooperative tone  
  play C  (set c_i,t = 1)  
  continue to next round  

 if t == r:  
  // Last round – inevitable defection  
  play D  (c_i,t = 0)  
  continue to next round  

 // otherwise 1 < t < r  
 if state == “Punish”:  
  // we are in punishment mode  
  play D  (c_i,t = 0)  
  punish_counter ← punish_counter − 1  
  if punish_counter == 0:  
   state ← “Cooperate”  
  // end Punish block  

 else if state == “Cooperate”:  
  // check last round’s history  
  if C_{t−1} < n:  
   // someone defected last round → punish  
   state ← “Punish”  
   punish_counter ← P  // P=1 for one‐round punishment  
   play D  (c_i,t = 0)  
  else:  
   // full cooperation last round → keep cooperating  
   play C  (c_i,t = 1)  

End for  

––––––––––––––––––––––––––––––––––––––––––  
Rationale and Properties  
1.  First move cooperation seeds the public good.  
2.  Full-group cooperation last round → we cooperate again.  
3.  Any defection by any player last round → we defect for P rounds.  This imposes an immediate, short‐run cost on deviators (they lose the full cooperator share next round).  
4.  After exactly P punishments we forgive, returning to Cooperate state.  
5.  Last round defection is Nash‐optimal when there is no future, but by then the bulk of rounds should already be cooperative.  

This is a classic “generous Tit-for-Tat” for multi‐player public goods.  It achieves near–full cooperation against willing opponents, punishes free-riders quickly, but does not spiral into permanent defection.
'''

description_COOPERATIVE_113 = '''
Below is a single‐strategy proposal, a finite “trigger­and­forgive” rule built to sustain high cooperation throughout most of the r rounds yet still defend against free‐riding.  It uses only the public history of who cooperated/defected in the previous round, requires no side‐payments or off‐equilibrium signalling, and meets all three requirements:

1. Decision rules (when to C vs D)  
2. Edge cases (first round, last round, punishment‐release)  
3. Clearly cooperative (starts by cooperating, forgives quickly, punishes defections just long enough to deter them)

---

Strategy name: “One‐Round Tit-for-Tat with Forgiveness in the Final Phase”  
Parameters you can tune:  
•  P = 1  (punish exactly one round after any defection)  
•  ε (optional small “noise” in final round, see below)  

State variables (for each player):  
•  punish_counter ∈ {0,1}  – how many more rounds we will defect to punish.  
•  last_round = t (we decrement as we go).

Pseudocode (for our player i):

Initialize before round 1:  
    punish_counter ← 0

At the start of each round t = 1…r do:

  if t = 1 then  
    // First round: unconditionally cooperate  
    action_i(t) ← C  
    continue to next round  

  if t = r then  
    // Last round: defect (subgame‐perfect);  
    // if you want to inject a small chance of cooperation to sustain group‐level gains, use “cooperate with probability ε”  
    action_i(t) ← D  
    continue  

  // for 1 < t < r:
  if punish_counter > 0 then  
    // we are in a punishment phase  
    action_i(t) ← D  
    punish_counter ← punish_counter − 1  
    continue  

  // No active punishment, inspect what happened in round t−1:
  let Defectors_{t−1} = { j : in round t−1, player j chose D }

  if Defectors_{t−1} ≠ ∅ then  
    // at least one defection last round ⇒ punish for P=1 round  
    action_i(t) ← D  
    punish_counter ← P − 1   // if P=1, this sets punish_counter=0  
  else  
    // unanimous cooperation last round ⇒ remain cooperative  
    action_i(t) ← C

End loop

---

Explanation of key design choices

1. “Start with C” (round 1)  
   We immediately signal willingness to cooperate.  

2. “One‐round punishment” (Tit-for-Tat)  
   If anybody defects in t−1, we defect in t (P=1).  That is enough to raise the penalty of defection by reducing that defector’s future public‐good share, but it is not so harsh as “grim trigger,” so occasional mistakes or noise won’t collapse cooperation forever.  

3. “Forgive quickly”  
   After punishing exactly one round, we return to cooperation unless we see a fresh defection.  This keeps the long‐run path overwhelmingly C if others are mostly C.  

4. “Last round D”  
   Standard backward‐induction demands defection in round r.  (Optionally you can cooperate with tiny probability ε to boost collective payoff if you think other LLMs will reciprocate, but that risks exploitation if they all defect.)  

5. “Cooperative mindset”  
   • We never defect unless provoked (by seeing someone defect in the immediately prior round).  
   • We end punishment immediately and go back to C, maximizing mutual gains.  
   • We only punish enough to make defection unprofitable: one period of lost public‐good share deters free‐riding when k>1.  

This strategy is easy to implement, robust to unilateral defection, and fosters sustained cooperation for all t<r.
'''

description_COOPERATIVE_114 = '''
Below is a simple “contingive‐cooperate‐with‐forgiveness” strategy.  It tries to maintain full cooperation, punishes any defection with a single‐round defection, then returns to cooperation.  In the last round it defects (since there is no future to protect).

1.  Data structures / state  
   •  punish_flag ∈ {false, true}, initially false.  

2.  Decision rules  
   For each round t = 1, 2, …, r:  
     if t == 1:  
       Play C.  // Start by cooperating  
       punish_flag ← false  
     else if t == r:  
       Play D.  // Last round: defect  
     else if punish_flag == true:  
       Play D.  
       punish_flag ← false     // punish for exactly one round  
     else:  
       Let last_C = number of players who played C in round t−1.  
       if last_C == n:  
         Play C.  // Everyone cooperated last round, resume cooperation  
       else:  
         Play D.  
         punish_flag ← true      // trigger one‐round punishment  

3.  Explanation / cooperative mindset  
   – “Cooperate if everybody cooperated on the previous turn.”  
   – “If I observe any free‐riders, I withhold my contribution once to discourage them, but then I forgive and try to rebuild cooperation.”  
   – By punishing only a single round, the group can return to full cooperation quickly if defectors change back to C.  
   – Since the last round has no future, we defect then (standard finitely repeated‐game reasoning).  

4.  Edge cases handled  
   •  First round t=1: no history ⇒ cooperate.  
   •  Any round after a punishment: punish_flag prevents chains of mutual defection.  
   •  Last round t=r: guaranteed defection.  

5.  Pseudocode  

   initialize punish_flag ← false  
   for t in 1…r do  
     if t == 1 then  
       action ← C  
       punish_flag ← false  
     else if t == r then  
       action ← D  
     else if punish_flag == true then  
       action ← D  
       punish_flag ← false  
     else  
       observe last_C = Σ_{j=1..n} 1{action_j(t−1)==C}  
       if last_C == n then  
         action ← C  
       else  
         action ← D  
         punish_flag ← true  
       end if  
     end if  
     play(action)  
   end for  

This strategy is fully symmetric, requires only the public history of contributions, immediately punishes any defection, but then forgives in one round to restore cooperation.
'''

description_COOPERATIVE_115 = '''
Below is a simple “group‐level tit-for-tat with one‐round forgiveness” strategy that (i) promotes full cooperation, (ii) punishes any outsider defection for exactly one round, then forgives, and (iii) defects in the last round to avoid end‐game exploitation.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Name:  Group TFT + 1-Round Forgiveness  

Intuition:  
 • Start by cooperating.  
 • If in the previous round any *other* player defected, punish the whole group by defecting for exactly one round.  
 • After that one punishment round, return to cooperation (even if past punishments dropped contributions last round).  
 • In the very last round, defect (standard backward‐induction safety).  

This strategy never assumes any off-path coordination device—only the publicly observed history of who contributed.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode (for player i):

Parameters:  
  n  = number of players  
  r  = total rounds (r > 1)  

State variables (for player i):  
  punish_counter ← 0    // counts down remaining punishment rounds

Loop for t = 1 to r do:  
  if t == 1 then  
    action_i[t] ← C     // first round: cooperate  
  
  else if t == r then  
    action_i[t] ← D     // last round: always defect  

  else if punish_counter > 0 then  
    // we are in a punishment round  
    action_i[t] ← D  
    punish_counter ← punish_counter − 1  

  else  
    // not currently punishing: look at what *others* did in t−1  
    let defect_found ← FALSE  
    for each j ≠ i do  
      if action_j[t−1] == D then  
        defect_found ← TRUE  
        break  
      end if  
    end for  

    if defect_found then  
      // someone else defected last round: initiate 1‐round punishment  
      punish_counter ← 1  
      action_i[t] ← D  
    else  
      // no one else defected last round: resume cooperation  
      action_i[t] ← C  
    end if  
  end if  
end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of key points:

1. First round cooperates unconditionally to signal goodwill.  
2. We monitor *others’* contributions only.  If at least one other j defected in the previous round, we defect this round exactly once (punish_counter=1).  
3. After that single punishment round, punish_counter hits zero, and we forgive: even if contributions were low during punishment, we give cooperation another chance.  
4. In the last round (t=r) we defect, since no future rounds remain and cooperation cannot be enforced.  

Properties:

• If all n players adopt this same rule, the unique stable path is *full cooperation* (everyone plays C) in rounds 1…r−1, then D in round r.  
• A single defection by any player at t causes exactly one round of group‐level punishment at t+1, then automatic return to cooperation.  
• It thus enforces cooperation, punishes free‐riding, but forgives quickly to avoid long runs of mutual defection.  
• No off‐path assumptions or side channels are needed—only the public history of C’s and D’s.
'''

description_COOPERATIVE_116 = '''
Below is a single‐strategy proposal, “One‐Round Tit-for-Tat with Endgame Defection,” that (i) starts fully cooperative, (ii) punishes any defection by all defecting for exactly one round, then immediately forgives, and (iii) defects in the final round to avoid being exploited at the end.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name  
  One-Round Tit-for-Tat with Endgame Defection  

Idea  
  • Encourage full cooperation from the outset.  
  • If anyone defects in round t–1, punish all players by defecting in round t—but only for one round (quick forgiveness).  
  • In the very last round, defect (since no future remains to enforce cooperation).  

Parameters  
  • n ≥ 2 players  
  • r ≥ 2 rounds  
  • k, 1 < k < n (multiplication factor)  
  • M = 1  (punishment length in rounds)  

State variables  
  punishment_remaining  ← 0   (counts down remaining punishment rounds)  

Pseudocode for player i  
  for each round t = 1…r do  
    if t == 1 then  
      action_i(t) ← C  
      continue  
    end if  

    if t == r then  
      # Last round: defect unconditionally  
      action_i(t) ← D  
      continue  
    end if  

    if punishment_remaining > 0 then  
      # We are in a punishment phase  
      action_i(t) ← D  
      punishment_remaining ← punishment_remaining – 1  
      continue  
    end if  

    # No active punishment; check previous round  
    let total_contrib(t–1) = Σ_j c_j(t–1)   # total cooperators last round  
    if total_contrib(t–1) < n then  
      # Someone defected last round → trigger one‐round punishment  
      punishment_remaining ← M  
      action_i(t) ← D  
    else  
      # Everyone cooperated last round → cooperate  
      action_i(t) ← C  
    end if  
  end for  

Explanation of rules  
1. First round t=1: cooperate, to signal willingness.  
2. Rounds 2 ≤ t < r:  
   – If we are still “punishing” (punishment_remaining>0), we defect, then decrement the counter.  
   – Otherwise, look at round t–1:  
     • If all n players cooperated, we cooperate.  
     • If there was even one defection, we punish by defecting this round (one‐round punishment), then revert to cooperation.  
3. Final round t=r: defect unconditionally (no future rounds remain to enforce cooperation).  

Why this is cooperative  
– It fully rewards cooperation by always returning to cooperation as soon as possible.  
– It protects against free‐riding by imposing a one‐round “cost” on defectors.  
– It is forgiving: a single defection yields only a single round of punishment, then full cooperation resumes.  
– By defecting in the last round, it avoids being exploited at the end‐game, making it sequentially rational and credible throughout.
'''

description_COOPERATIVE_117 = '''
Below is a purely history‐based “group tit‐for‐tat with one–round punishment and forgiveness” strategy.  It is easy to implement, highly cooperative, punishes defections just enough to deter them, but then quickly forgives so cooperation can be re‐established.  

――――――――――――――  
Name  
  Forgiving Group Tit-for-Tat (FGTFT)  

Intuition  
  •  Start fully cooperative.  
  •  If anybody defects, punish the whole group by defecting one round.  
  •  After that single‐round punishment, immediately return to full cooperation (even if the defector repeats).  
  •  In the very last round, always cooperate to maximize group payoff (no future to punish).  

Parameters  
  n   number of players  
  r   total number of rounds  
  k   multiplication factor (1<k<n)  

State variables (for our agent i)  
  punishmentRoundsLeft ← 0  

Pseudocode  
  for t in 1…r do  
    if t = 1 then  
      play C  # round-1 cooperation  
    else if punishmentRoundsLeft > 0 then  
      play D  
      punishmentRoundsLeft ← punishmentRoundsLeft − 1  
    else if t = r then  
      # last round: override and cooperate  
      play C  
    else  
      # look at what happened in the immediately preceding round  
      let totalCoopsPrev = Σ_{j=1..n} c_j,(t−1)  
      if totalCoopsPrev = n then  
        # everybody cooperated last round  
        play C  
      else  
        # at least one defection last round → punish one round  
        play D  
        punishmentRoundsLeft ← 1  
      end if  
    end if  
  end for  

Decision rules explained  
1. First round: always cooperate.  
2. If currently in a “punishment spell,” defect until it expires.  
3. Otherwise, if it’s the final round (t=r), cooperate unconditionally to boost everyone’s payoff.  
4. Otherwise (middle rounds, no active punishment):  
   – If no one defected in t−1, cooperate;  
   – If one or more players defected in t−1, defect to punish them for exactly one round, then immediately return to cooperation.  

Why it is cooperative  
– It never defects first (round 1 always C).  
– It rewards full cooperation by staying in C-state indefinitely.  
– It only punishes for one round regardless of how many defectors there were or how many rounds they have defected in the past, so it is forgiving and quickly returns to the cooperative equilibrium.  
– By cooperating in the last round, it maximizes the common‐good payoff rather than chasing a last‐round free‐riding temptation.  

Edge cases  
– r=2:  
    • t=1: cooperate.  
    • t=2 (last): cooperate unconditionally.  
– Multiple consecutive defections by others: each will trigger at most a one‐round punishment; after you punish once you immediately go back to cooperation.  
– A lone defector vs. all‐out defection: the punishment does not discriminate; group‐level punishment encourages everyone to return to cooperation quickly.  

Balance of incentives  
This strategy makes unilateral defection unprofitable in the long run: every defection costs you a one‐round loss of your private payoff, but defection never spirals into endless mutual defection.  It thereby sustains high levels of cooperation across r rounds.
'''

description_COOPERATIVE_118 = '''
Below is a single‐strategy proposal—“Limited Grim Trigger with Last‐Round Defection”—that is simple to describe, fully cooperative until punished, punishes defections for a short, fixed window, then forgives, and always defects in the last round (to avoid the standard end‐game unraveling).

1. State Variables  
   • r: total number of rounds  
   • P: punishment length = min(2, r−1)  
   • punish_timer ← 0  
   • ever_defected ← false  

2. Decision Rules (for each round t = 1…r)  
   if t == r then  
     action ← D  // Last-round defection: no incentive to cooperate in final round  
   else if punish_timer > 0 then  
     action ← D  
     punish_timer ← punish_timer − 1  
   else if t == 1 then  
     action ← C  // Kick off with cooperation  
   else if ever_defected == true then  
     // Trigger a fresh punishment window  
     punish_timer ← P − 1    // we’ll defect now plus P−1 more rounds  
     action ← D  
   else  
     action ← C  // No defections seen so far → keep cooperating  
   
   // After all players’ actions are revealed for round t, update:  
   if any player j chose D in round t then  
     ever_defected ← true  

3. Behavior Explained  
 • First round (t=1): Cooperate, to signal good faith.  
 • Rounds 2…r−1:  
   – If nobody has ever defected in any prior round, continue cooperating.  
   – If you detect a first defection at round t, trigger P consecutive defections (including round t). After P rounds of “punish,” reset punish_timer to 0 and resume cooperation (forgiveness).  
 • Last round (t=r): Always defect. In a one‐shot PD the dominant play is defect; we exploit that inevitability rather than try to sustain cooperation where it cannot be sustained.  

4. Why It’s Cooperative  
 • Mutual cooperation in rounds 1…r−1 yields payoff per round of (k/n)·n = k, which exceeds the singleton defector’s 1 + (k/n)(n−1) only by a small margin 1−k/n>0.  
 • A short, predictable punishment (P=2) deters unilateral defection: a defector sacrifices two future cooperative payoffs (≈2k) in order to gain immediate defect payoff.  
 • The forgiveness element (we only punish P rounds and then return to C) prevents permanent breakdown of cooperation if there has been a misunderstanding or one‐off defection.  

5. Pseudocode  

```
Initialize:
  punish_timer ← 0
  ever_defected ← false
  P ← min(2, r−1)

For t in 1…r:
  if t == r:
    play D
  else if punish_timer > 0:
    play D
    punish_timer ← punish_timer − 1
  else if t == 1:
    play C
  else if ever_defected == true:
    punish_timer ← P − 1
    play D
  else:
    play C

  // After actions are revealed:
  if any player played D in round t:
    ever_defected ← true
```

Edge cases:  
- If r=2 then P=1, so any defection is punished one round (which is the last round, where we were defecting anyway).  
- If no defection ever occurs, we cooperate for t=1…r−1.  

This strategy is transparent, retaliatory but forgiving, and maximally cooperative in the bulk of the game.
'''

description_COOPERATIVE_119 = '''
Below is a simple “tit‐for‐tat with one‐round punishment and end‐game defection” strategy for the n‐player public goods game.  It has the following high-level features:  
• It begins in full cooperation.  
• It never lets a defector go unpunished—but punishment lasts only one round, after which it returns to cooperation.  
• It defects in the final round (no future to protect against).  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. State variables  
   punishing ← false    // “Am I currently serving the one‐round punishment?”  

2. Decision rule for round t (1 ≤ t ≤ r)  
   
   if t == 1 then  
     play C  
     // first‐mover cooperates to signal willingness to cooperate  
   
   else if t == r then  
     play D  
     // last round: no future, so defect (avoids sucker payoff)  
   
   else if punishing == true then  
     play D  
     punishing ← false  
     // serve one round of punishment, then reset  
   
   else  
     // look at last round’s profile  
     let last_actions = {c₁, c₂, …, cₙ} from round t−1  
     if ∃ j such that last_actions[j] == D then  
       // someone defected last round  
       play D  
       punishing ← true  
     else  
       // everyone cooperated last round  
       play C  
     end if  
   end if  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
3. Explanation of behavior  

• Round 1: Cooperate to “test the waters” and build mutual trust.  
• Rounds 2 to r−1:  
   – If you are in a punishment turn, you defect one round, then go back to cooperative mode.  
   – Otherwise, if you saw any defection in the immediately preceding round, you defect this round and enter “punishment mode” for exactly one round.  
   – If in the last round everyone cooperated, you cooperate again.  
• Round r: Defect.  With no future rounds, cooperation can’t be rewarded, so you avoid being exploited.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
4. Why this is cooperative  

• It starts by cooperating and will always return to cooperation as soon as possible.  
• It punishes exploiters, deterring them from free‐riding.  
• Punishment is limited—only one round long—so occasional mistakes (or noise) do not lead to endless mutual defection.  
• By defecting in the final round, it avoids a sucker’s payoff without undermining cooperation in the earlier rounds.  

This strategy can sustain high levels of group cooperation in repeated play while guarding against exploitation and forgiving inadvertent mistakes.
'''

description_COOPERATIVE_120 = '''
Below is a single‐player strategy (“Firm‐but‐Fair”) for the n-player repeated public‐goods game.  It is purely history-based, starts by cooperating, punishes any round in which one or more players defect, then forgives, and always defects in the last round.  It never assumes any off-game agreements and uses only the public history of C/D choices.

1.  State variables (maintained across rounds)  
    pun_count ← 0    // how many remaining punishment rounds  

2.  Decision rule for round t (1 ≤ t ≤ r):  
    if t = 1 then  
        action ← C  
    else if pun_count > 0 then  
        action ← D  
        pun_count ← pun_count − 1  
    else if t = r then  
        action ← D       // last round “end‐game” defect  
    else  
        let D_prev = number of players who played D in round t−1  
        if D_prev > 0 then  
            // trigger punishment proportional to observed defectors  
            // punish starting immediately, for a total of D_prev rounds  
            action ← D  
            pun_count ← D_prev − 1  
        else  
            action ← C  
    end if  

3.  Rationale / remarks  
  •  First round: cooperate, to signal willingness.  
  •  Punishment: if any defection is observed in round t−1, we defect in round t and set a counter so that we continue to defect for exactly as many rounds as there were defectors last time.  This “proportional retaliation” is enough to deter free‐riding but is also forgiving: once pun_count hits zero we return to cooperation.  
  •  Last round: defect (standard end‐game logic—no future to enforce cooperation).  
  •  No other players’ identities or private states are assumed—only the public counts of C versus D in each round.  

Pseudocode (more compact)

```
initialize pun_count ← 0

for t in 1..r:
  if t = 1:
    play C
  else if pun_count > 0:
    play D
    pun_count ← pun_count − 1
  else if t = r:
    play D
  else:
    D_prev ← count of D’s in round (t−1)
    if D_prev > 0:
      play D
      pun_count ← D_prev − 1
    else:
      play C
```

This strategy is cooperative in spirit—always willing to contribute when others have recently cooperated—but also enforces a credible, proportional punishment for any defection, then quickly forgives so that the group can re‐establish full cooperation.
'''

description_COOPERATIVE_121 = '''
Below is a single‐page description of a “cooperative‐but‐forgiving” strategy that (i) strives to sustain mutual cooperation, (ii) punishes defections only briefly, and (iii) handles the first and last rounds cleanly.  

--------------------------------------------------------------------------------  
Strategy name: Forgiving‐Trigger  

Intuition  
• Start by trusting (cooperating).  
• If you see any defection, punish once by defecting in the very next round, then immediately revert to cooperation.  
• In the very last round, defect (standard end‐game).  

This yields full cooperation as long as everyone has cooperated in the immediately preceding round. A single defection is punished exactly once and then forgiven—so accidental or one‐off defections don’t collapse cooperation forever.  

--------------------------------------------------------------------------------  
Notation  
n  = number of players  
r  = total rounds (r>1)  
t  = current round index, t=1,…,r  
A history record for each t–1: the vector of actions c_j (1=cooperate, 0=defect) observed last round  
state_punish ∈ {0,1}: counter for “one‐round punishment” (initially 0)  

--------------------------------------------------------------------------------  
Pseudocode  

Initialize:  
    state_punish ← 0  

For each round t = 1 to r:  
    if t == 1 then  
        action ← C                       # First round: trust everyone  
    else if t == r then  
        action ← D                       # Last‐round defection (no future to protect)  
    else  
        if state_punish == 1 then  
            # We are in a punishment round  
            action ← D  
            state_punish ← 0            # Punishment done; forgive thereafter  
        else  
            # Normal mode: check what happened last round  
            let defectors ← { j : c_j(t–1) == 0 }  
            if |defectors| > 0 then     # Someone defected last round  
                action ← D               # Punish once  
                state_punish ← 1         # Flag next round as “punishment completed”  
            else  
                action ← C               # All cooperated last round → cooperate  
            end if  
        end if  
    end if  

    Play action (C or D) this round.  
    Observe other players’ actions for next iteration.  

--------------------------------------------------------------------------------  
Discussion of key points  

1. First round (t=1): cooperate.  This signals trust and opens the door to mutual cooperation.  
2. Normal rounds (2 ≤ t < r):  
   – If we are in a “punishment round” (state_punish==1), we defect and then reset state_punish to 0.  
   – Otherwise, we look at round t–1:  
       • No defections → cooperate.  
       • ≥1 defection → defect now (to punish) and set state_punish=1 so that one explicit punishment turn is executed.  
3. Last round (t=r): always defect, since no future reward can be secured by cooperation (standard backward‐induction end‐game).  

Cooperative mindset: As long as everyone keeps cooperating, our rule keeps cooperating.  A single defection anywhere is met with exactly one round of joint defection, after which we restore cooperation.  This “forgiving trigger” prevents endless breakdown after one mistake and yet still deters persistent free‐riding.
'''

description_COOPERATIVE_122 = '''
Below is a simple, deterministic “group‐Tit‐for‐Tat with endgame defection” strategy.  It is fully cooperative as long as everyone else has been, it punishes any defection by defecting exactly once, and it always defects in the very last round (since there is no future in which to enforce cooperation).

1. State Variables  
   • r: total number of rounds  
   • t: index of the current round (1 ≤ t ≤ r)  
   • history[t–1]: the vector of contributions (C/D) by all n players in the previous round; for t=1 this is empty.  

2. Decision Rule  
   if t == r then  
     play D  
   else if t == 1 then  
     play C  
   else  
     if all players in history[t–1] played C then  
       play C  
     else  
       play D  

3. After‐round bookkeeping (not strictly needed by this rule, since the rule only looks at the last round’s actions, which are externally observable).  

4. Explanation of behavior  
  • First round t=1: cooperate, to signal willingness to build the public good.  
  • Intermediate rounds t=2,…,r–1:  
     – If in the immediately preceding round everyone cooperated, reward that by cooperating.  
     – If you saw even one defector last round, punish by defecting once.  
       (If the group returns to full cooperation in the next round, you return to cooperating as well.)  
  • Last round t=r: defect, because there is no future in which to enforce cooperation.  

5. Handling edge cases  
  – r=2: Round 1 you cooperate; round 2 (the last) you defect.  
  – Any single defection at round t < r triggers exactly one round of group defection at t+1; if they all cooperate at t+1, you resume cooperating at t+2.  
  – No memory beyond the last round is needed.  

Pseudocode  
-----------  
```  
INPUT:  
  r       // total number of rounds  
  t       // current round (1-based)  
  history // array of length t−1, each element is a list of n actions from that round  

FUNCTION DecideAction(t, r, history):  
  if t == r:  
    return “D”  
  if t == 1:  
    return “C”  
  // otherwise t in 2..r−1  
  let prev = history[t−1]        // a length-n vector of “C”/“D” from last round  
  if every entry of prev == “C” then  
    return “C”  
  else  
    return “D”  
```  

Why this is cooperative  
– As long as the group never defects, you keep building the public good.  
– Any defection by anyone is met with a single-round punishment; once the group reforms full cooperation you immediately rejoin.  
– There is no long, unforgiving punishment, so the risk of lock‐in to permanent defection is low.  
– By defecting in the final round only, you avoid being exploited when no future rounds remain.
'''

description_COOPERATIVE_123 = '''
Below is a simple “conditional‐cooperator” strategy that (1) begins by cooperating, (2) punishes any defection by defecting exactly one round, then returns to cooperation if others do, and (3) defects in the final round to avoid last‐round exploitation.  It requires only tracking (a) which round you’re in, (b) how many players defected in the previous round, and (c) a one‐round punishment flag.

––––––––––––––––––––––––––––––––––––––––  
Strategy name: One‐Round Punishing Cooperator  

State variables (initialized before round 1):  
• punish_timer ← 0   // counts down rounds of punishment  
• r             // total number of rounds (common knowledge)  

At the beginning of each round t (t = 1,…,r):  
  1. If t == 1 then  
       play C  
       continue to next round  
  2. If t == r then  
       play D     // last round defection  
       continue to next round  
  3. If punish_timer > 0 then  
       // We are in a punishment phase  
       play D  
       punish_timer ← punish_timer − 1  
       continue to next round  
  4. // Otherwise, look at what happened in the last round  
     Let n_defect ← number of players (including you) who chose D in round t−1.  
     If n_defect > 0 then  
       // Someone defected last round → punish for exactly one round  
       punish_timer ← 1  
       play D  
     Else  
       // Everybody cooperated last round → reward with cooperation  
       play C  

Explanation of the rules:  
• First round (t=1): Always cooperate, to signal goodwill.  
• Intermediate rounds (2 ≤ t ≤ r−1):  
    – If you are “in punishment” (punish_timer>0), defect and count down your punishment.  
    – Else, inspect the previous round:  
       • If any player defected, set punish_timer=1 and defect this round.  
         (That is a one‐round “tit‐for‐one‐round” punishment.)  
       • If everyone cooperated, cooperate again.  
• Last round (t=r): Always defect to preempt any last‐round exploitation (standard backward‐induction step).  

Why it’s cooperative:  
– As long as no one defects, all players get the full public‐good payoff (k each round).  
– Any lone defector is punished immediately, deterring unilateral deviations.  
– Punishments are brief (only one round), so cooperation can resume quickly.  
– By defecting in the final round, you avoid being exploited without undermining cooperation in earlier rounds.  

Pseudocode summary:  
```
for t in 1…r:
  if t == 1:
    action[i] ← C
  else if t == r:
    action[i] ← D
  else if punish_timer > 0:
    action[i] ← D
    punish_timer ← punish_timer - 1
  else:
    observe n_defect in round t-1
    if n_defect > 0:
      punish_timer ← 1
      action[i] ← D
    else:
      action[i] ← C
```
This strategy has the hallmarks of a cooperative “tit‐for‐tat” variant: it rewards full cooperation with cooperation, punishes defections promptly (but not forever), and guards against last‐round “free riding.”
'''

description_COOPERATIVE_124 = '''
Below is a single‐strategy (“ours”) that (1) tries to sustain full cooperation, (2) punishes any defection just long enough to deter it, (3) forgives, and (4) avoids the end‐game unraveling by defecting in the last round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. State variables  
   • state ∈ {Cooperate, Punish}  
   • punish_remaining ∈ ℕ (initially 0)  

2. Parameters  
   • T_punish = 1   (length of punishment phase)  
   • R = total number of rounds  
   • n = number of players  

3. High‐level idea  
   – Start by cooperating.  
   – If in “Cooperate” state and you observe any defection last round, switch to “Punish” state (defect) for exactly T_punish rounds.  
   – After punish phase, return to “Cooperate” and give everyone a fresh chance.  
   – Always defect in the final round (r = R) to avoid being exploited in a one‐shot.  

4. Detailed decision rule / pseudocode  

   Initialize:  
     state ← Cooperate  
     punish_remaining ← 0  

   For each round t = 1,2,…,R do:  
     if t = R then  
       play D   # last‐round defection for safety  
       continue to next (end)  
     end if  

     if t = 1 then  
       # first round: no history → cooperate  
       play C  
       continue  
     end if  

     # for t = 2…R–1, we have history of round t–1  
     let last_contributions = number of players who played C in round t–1  

     if state = Punish then  
       # we are in punishment mode  
       if punish_remaining > 0 then  
         play D  
         punish_remaining ← punish_remaining – 1  
         if punish_remaining = 0 then  
           state ← Cooperate  
         end if  
       end if  

     else if state = Cooperate then  
       # we are in cooperation mode  
       if last_contributions < n then  
         # someone defected last round → punish  
         state ← Punish  
         punish_remaining ← T_punish  
         play D  
       else  
         # full cooperation last round → keep cooperating  
         play C  
       end if  
     end if  
   end for  

5. Explanation of edge‐cases  
   – First round (t=1): we cooperate without prejudice.  
   – Rounds 2…R–1:  
       • If nobody defected in t–1 (last_contributions = n) → C.  
       • If at least one defected → enter Punish: defect for exactly one round (T_punish=1), then revert to Cooperate.  
   – Last round (t=R): always D.  
     • This prevents endgame “bait‐and‐switch” by others, and is the unique best response if no future to punish them.  

6. Why this is cooperative  
   – We begin by trusting everyone (C in round 1).  
   – We only punish defection once (short, calibrated punishment), then we forgive. This keeps the door open for full‐cooperation cycles.  
   – Full‐cooperation by all yields the Pareto‐optimal outcome each round (everybody’s payoff = k > 1).  
   – By defecting in the last round, we protect ourselves against pure “last‐round” exploiters—yet this has no impact on sustaining cooperation for t < R.  

7. Variations / tuning  
   – One can choose T_punish >1 for harsher deterrence.  
   – One can soften by using a probabilistic punishment (e.g. defect with prob p<1) to tolerate noise.  
   – One can pivot to stricter “grim‐trigger” (permanent defection) if facing extremely aggressive defectors.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy satisfies the requirements:  
1. Decision rules are fully specified by state transitions (Cooperate ↔ Punish).  
2. Edge‐round behavior is explicitly handled (round 1 and round R).  
3. It is manifestly cooperative—rewarding full group cooperation, punishing minimal defections only briefly, then forgiving to restore cooperation.
'''

description_COOPERATIVE_125 = '''
Below is a single‐strategy description—call it “Proportional Collective TFT with Last‐Round Defection”—that seeks to sustain full cooperation for as long as possible, punishes defections in proportion to their size, but avoids the sucker’s payoff in the final round.

1.  Strategy intuition  
   - Start by cooperating.  
   - As long as everyone cooperates, continue to cooperate.  
   - If you observe defections, switch to defection (“punish”) for a number of rounds proportional to how many players defected.  
   - After punishment, forgive and return to cooperation.  
   - In the very last round, defect (to avoid unilateral exploitation).  

2.  Pseudocode  

```  
Inputs:  
  n    ← number of players  
  r    ← total rounds (r > 1)  
State variables (initialized before round 1):  
  punish_timer ← 0    # how many more rounds we will defect as punishment

For each round t = 1, 2, …, r do:

  if t == 1:
    # First round: no history yet
    action ← C

  else if t == r:
    # Last round: defect to avoid sucker’s payoff
    action ← D

  else:
    # Intermediate rounds t = 2..r-1
    if punish_timer > 0 then
      # We are in a punishment phase
      action ← D
      punish_timer ← punish_timer − 1

    else
      # Not currently punishing; inspect last round
      Let last_contributions ← vector of all players’ c_j in round t−1
      let def_count ← number of players j with c_j == 0

      if def_count == 0 then
        # Perfect mutual cooperation in t−1
        action ← C
      else
        # Someone defected: start a new punishment phase
        # Punish for def_count rounds (proportional to damage)
        punish_timer ← def_count
        action ← D
      end if
    end if
  end if

  Play action, observe other players’ contributions, and update history.
end for
```

3.  Explanation of key points  

– First round: cooperate, to signal your willingness to build the public good.  
– Middle rounds:  
   • If everyone cooperated last round, you cooperate again.  
   • If you spot k defections last round, you defect for k consecutive rounds—this imposes a proportional cost back on the group, deterring free‐riding without locking you into endless vengeance.  
   • Once your punishment timer expires, you revert to cooperation and give everyone a fresh start.  
– Last round: defect. In a one‐shot or final iteration, cooperation can be exploited; by defecting in round r you avoid being the sole cooperator when others realize there’s no future to punish.  

4.  Why this is cooperative  

– It achieves near‐full cooperation whenever opponents respond in kind.  
– Punishments are neither too weak (one‐shot tit‐for‐tat would let serial defection slide) nor too unforgiving (a pure grim trigger would collapse cooperation forever at the first slip).  
– By proportionally punishing, you calibrate your response to the severity of defection, minimizing needless loss of public‐good returns.  
– You always forgive eventually, allowing the group to rebuild cooperation even after mistakes.  
– Defecting only in the final round is a narrowly tailored endgame move to protect your own payoff without undermining cooperation in earlier rounds.  

This strategy should score well against a variety of independent opponents: it promotes and sustains cooperation when partners reciprocate, punishes non‐cooperators firmly but fairly, and avoids unilateral losses at the end.
'''

description_COOPERATIVE_126 = '''
Below is a single‐strategy outline—“Generous Trigger with Limited Retaliation”—that strives for full cooperation by default, punishes defections briefly, then forgives, and even cooperates in the final round to “break” backward‐induction collapse.

1.  Parameters  
    •  n = number of players  
    •  r = total rounds (r>1)  
    •  M = maximum punishment length (we suggest M=1 or 2)  

2.  State variable  
    •  punish_count ∈ {0,1,…,M} – how many more rounds we will defect in retaliation  

3.  Strategy in words  
    – Round 1: Cooperate.  
    – In each subsequent round t:  
       •  If punish_count>0, defect this round and decrement punish_count by 1.  
       •  Else if t==r (the last round), cooperate.  
       •  Else (punish_count=0 and t<r):  
          – If everyone cooperated in t–1, cooperate.  
          – If any defection occurred in t–1, set  
                punish_count←min(M, r–t)  
            then defect this round (and begin counting down punish_count).  

    This implements: “start friendly, whenever anyone defects punish for M rounds, then go back to cooperating; and unconditionally cooperate in the final round.”

4.  Pseudocode  

   initialize punish_count ← 0  

   for t in 1…r do  
     if t == 1 then  
       A_t ← C  
     else if punish_count > 0 then  
       A_t ← D  
       punish_count ← punish_count – 1  
     else if t == r then                # last round  
       A_t ← C  
     else                              # t in [2 … r–1] and no active punishment  
       let coop_prev ← number of C‐actions in round t–1  
       if coop_prev < n then            # somebody defected  
         punish_count ← min(M, r – t)  
         A_t ← D                     # start punishment (counts toward punish_count)  
         punish_count ← punish_count – 1  
       else  
         A_t ← C                     # full cooperation last round  
       end if  
     end if  

     play A_t  
   end for  

5.  Discussion of key features  
  •  “Generous” / forgiving: punishment lasts only M rounds, so one defection cannot derail cooperation indefinitely.  
  •  Last round cooperation: by choosing C in round r, we avoid the backward‐induction trap and signal pure willingness to cooperate.  
  •  Simplicity and observability: the only public statistic used is “were there any defectors in the last round?”  

With this rule you will:  
  – Reward full‐cooperation histories by always playing C.  
  – Deter isolated defections by a short, predictable punishment.  
  – Forgive and return to full cooperation after M rounds, sustaining high average payoffs in a tournament of similar strategies.
'''

description_COOPERATIVE_127 = '''
Below is a single‐strategy (“agent”) that seeks to sustain full cooperation in an n‐player public‐goods tournament by punishing any defection with exactly one round of defection, then immediately forgiving.  In the very last round it defects (no future to sustain).  This is a deterministic, memory-one rule (plus a one‐bit “punish” flag), very much in the spirit of Tit-for-Tat with forgiveness.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: Forgiving Tit-for-Tat (FTfT)  

State variables (maintained across rounds):  
• punish_flag ∈ {false, true}, initially false  

Action space each round: C (cooperate) or D (defect)  

Parameters (known): n, r, k  

1.  Initialization  
    punish_flag ← false  

2.  At the beginning of each round t = 1,2,…,r do  

    if t = 1 then  
      play C  
      continue to next round  
    end  

    if t = r then  
      // Last round: no future, defect  
      play D  
      continue to next round  
    end  

    // For rounds 2 ≤ t ≤ r–1:  

    if punish_flag = true then  
      // We are in the one‐round punishment phase  
      play C              // immediately forgive after one defection  
      punish_flag ← false  
      continue to next round  
    end  

    // Otherwise look at what happened in t–1  
    let total_C_last = Σ_{j=1..n} c_j^{t−1}  
      // number of cooperators in the previous round  

    if total_C_last = n then  
      // Everybody cooperated last round → reciprocate cooperation  
      play C  
    else  
      // At least one defection was observed last round → punish once  
      play D  
      punish_flag ← true  
    end  

3.  End  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Explanation  

• First round: cooperate to signal goodwill.  
• Middle rounds: if everyone cooperated last round, keep cooperating; if you saw any defection, defect once to discourage free‐riding, then immediately return to cooperation.  
• Last round: defect (the one‐shot equilibrium), since no future returns make cooperation unrewarded.  

Why this is cooperative:  
• It achieves V‐for‐V (victim‐for‐victim) retaliation but limits punishment to a single round.  
• It is “nice” (never the first to defect), “forgiving” (returns to C immediately), “provocable” (punishes any D), and “non‐envious” (does not seek to outperform).  
• By keeping punishments minimal, it creates a strong incentive for the group to stay at full cooperation, yielding the maximal per‐round payoff k for everyone.
'''

description_COOPERATIVE_128 = '''
Below is a simple “conditional‐cooperation” strategy that (1) starts out fully cooperative, (2) punishes defection by the group, but (3) forgives as soon as the group returns to cooperation, and (4) handles first‐ and last‐round edge cases.  It requires no side agreements or signals beyond observing how many players cooperated each prior round.

--------------------------------------------------------------------------------  
1.  Definitions and Parameters  
   •  n = total number of players  
   •  r = total number of rounds  
   •  k = multiplication factor (1 < k < n)  
   •  T = ⌈n/2⌉  (threshold of cooperators needed in the previous round to be “satisfied”)  
   •  c_i[t] ∈ {0,1}:  my contribution in round t (1=C, 0=D)  
   •  coop_prev = Σ_{j=1..n} c_j[t−1] = total cooperators last round  

2.  Strategy Overview  
   – Round 1: Cooperate (c_i[1] = 1)  
   – Rounds 2…r−1:  
       • If coop_prev ≥ T, cooperate (c_i[t] = 1)  
       • Else defect (c_i[t] = 0)  
   – Round r (the very last round): defect (c_i[r] = 0)  

   This rule set:  
     • Rewards others’ cooperation (as soon as at least half the group cooperated, you return to C)  
     • Punishes rounds of mass defection by defecting yourself when fewer than T cooperated  
     • Is forgiving—once the group recovers, you immediately go back to C  
     • Recognizes the endgame: in the last round you defect (no future to punish), which is standard  

3.  Pseudocode  

   initialize:  
     T ← ceil(n/2)  

   for t from 1 to r do  
     if t == 1 then  
       c_i[t] ← 1        // start by cooperating  
     else if t == r then  
       c_i[t] ← 0        // last round: defect  
     else  
       observe coop_prev ← Σ_{j=1..n} c_j[t−1]  
       if coop_prev ≥ T then  
         c_i[t] ← 1      // group was “good” last round → cooperate  
       else  
         c_i[t] ← 0      // group was too uncooperative → punish by defecting  
       end if  
     end if  
   end for  

4.  Why this is cooperative  
   • By cooperating in round 1 you signal a willingness to build the public good.  
   • You only defect after seeing a shortfall (fewer than half cooperating)—so you don’t get exploited repeatedly.  
   • You immediately forgive as soon as the group’s cooperation crosses the halfway mark again.  
   • You still defect in the final round (where no future punishment is possible), making your strategy subgame‐
     perfect without needless endgame paranoia earlier.  

5.  Handling Edge Cases  
   • First round has no history → unconditionally cooperate.  
   • Last round → defect (no incentive to sustain cooperation).  
   • If players briefly drop below T and then rebound, you rejoin cooperation immediately.  

This strategy strikes a balance: it supports high group payoffs by maintaining cooperation whenever the majority cooperates, yet it shields you from prolonged exploitation by defecting if the group fails to reach the cooperation threshold.
'''

description_AGGRESSIVE_1 = '''
Below is a complete description of an aggressive “Opportunistic Exploiter” strategy for the repeated N-player public‐goods game.  It has four phases—Probing, Monitoring, Exploitation, Punishment—and never “forgets” once it switches into Exploitation or Punishment.  It always defects in the final round.

1.  Data structures / state  
   • phase ∈ {PROBE, MONITOR, EXPLOIT, PUNISH}  
   • window_success: integer counter, initially 0  
   • W = max(2, ⌊r/4⌋)     // number of consecutive unanimous‐cooperation rounds needed to trigger exploitation

2.  High-level outline  
   • Rounds t=1…r  
     – t = 1: always PROBE (play C)  
     – 2 ≤ t ≤ r–1: run according to current phase  
     – t = r: always DEFECT  

3.  Phase definitions and transitions  
   A. PROBE (t=1)  
      – Action: C  
      – Next phase: MONITOR  

   B. MONITOR (2 ≤ t ≤ r–1 and phase = MONITOR)  
      1. Observe history at t–1:  
         • others_coop = number of other players who chose C in t–1  
         • we_coop = (our action in t–1 == C)  
      2. If we_coop == false AND others_coop > 0  
         → Some cooperators remain while we defected ⇒ they “punished” themselves by letting us free-ride.  We do not reward that.  
         • phase ← PUNISH  
         • action ← D  
         END  
      3. Else if we_coop == true AND others_coop == n–1  
         → unanimous cooperation last round  
         • window_success ← window_success + 1  
         • if window_success ≥ W  
             phase ← EXPLOIT  
             action ← D  
           else  
             action ← C     // keep probing cooperation  
      4. Else  
         → mixed behavior last round (not unanimous), keep probing  
         • window_success ← 0  
         • action ← C  

   C. EXPLOIT (once triggered,  t < r)  
      – Action: D (permanent defection to milk cooperators)  

   D. PUNISH (once triggered, t < r)  
      – Action: D (permanent defection to retaliate defectors)  

   E. Last round (t = r)  
      – Regardless of phase, action ← D  

4.  Pseudocode  

   initialize phase = PROBE  
   initialize window_success = 0  
   compute W = max(2, floor(r/4))  

   for t in 1…r do  
     if t == 1 then  
       action ← C  
       phase ← MONITOR  
       continue to next t  
     end  

     if t == r then  
       action ← D  
       continue to next t  
     end  

     switch phase:  
       case MONITOR:  
         let others_coop = # of C’s among others in round t–1  
         let we_coop     = (our action in t–1 == C)  

         if we_coop == false AND others_coop > 0 then  
           // they let us free-ride; punish them  
           phase ← PUNISH  
           action ← D  
         else if we_coop == true AND others_coop == n–1 then  
           // perfect cooperation last round—time to switch to exploitation?  
           window_success ← window_success + 1  
           if window_success ≥ W then  
             phase ← EXPLOIT  
             action ← D  
           else  
             action ← C    // keep probing  
           end  
         else  
           // no unanimous cooperation, reset probe counter  
           window_success ← 0  
           action ← C  
         end  
         break  

       case EXPLOIT:  
         action ← D  
         break  

       case PUNISH:  
         action ← D  
         break  
     end switch  
   end for  

5.  Rationale  

 • Aggressive exploitation: once we observe W straight rounds of everyone else cooperating, we switch to permanent defection to pocket the private‐keeping bonus plus our share of their contributions.  
 • Immediate punishment: if we ever defect while others cooperate, we interpret that as them “willing to let us free-ride” and we lock into permanent defection to deny them future returns.  
 • No needless cooperation in final round: always defect in t=r (standard backward‐induction).  
 • Probing vs. noise: MONITOR→EXPLOIT requires unanimous cooperation W times in a row, so random one‐round lapses by cooperators won’t immediately lock us into defection.  

This strategy (1) never lets cooperators “get away” with unpunished exploitation of us, (2) exploits genuine cooperators aggressively once identified, and (3) avoids being exploited in the long run.
'''

description_AGGRESSIVE_2 = '''
Below is a concrete “aggressive‐exploiter” strategy you can plug into the tournament.  In essence it (1) offers a short “testing” and “cooperation” phase to build trust, (2) punishes any early defection with permanent defection, and (3) launches a final “predation” phase in which it defects every round to exploit any remaining cooperators.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
AGGRESSIVE EXPLOITER STRATEGY  

Parameters (you may tune):  
• r      = total number of rounds  
• m      = ⌈r/3⌉   (length of the initial testing/cooperation window)  

State variables:  
• sawDefection = FALSE   (has anyone ever defected in rounds 1…t–1?)  

Pseudocode (for player i):  
for t in 1…r:  
    if t == 1 then  
        action_i ← C               # round 1: always cooperate to “test the waters”  
    else if sawDefection == TRUE then  
        action_i ← D               # we’ve been burned—permanent defection (grim)  
    else if t ≤ m then  
        # still in cooperation/testing window and no defection seen so far  
        action_i ← C  
    else  
        # exploitation phase  
        action_i ← D  

    # AFTER choosing action_i, observe everyone’s actions this round   
    if ∃ j such that action_j == D then  
        sawDefection ← TRUE  

end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of components  

1. First round (t=1):  
   • Cooperate unconditionally.  This begins a cooperative reputation and checks if others are willing to cooperate in return.

2. Initial “cooperate‐and‐test” window (2 ≤ t ≤ m):  
   • If we have never observed a defection, keep cooperating.  
   • The moment any player defects, set sawDefection = TRUE.  

3. Permanent punishment (any t):  
   • Once sawDefection==TRUE, we defect in every remaining round.  
   • This is a classic grim‐trigger style “no forgiveness” to deter early defection.

4. Exploitation (t > m, before any defection):  
   • After m rounds of mutual cooperation (if it actually happened), switch to defection  
     for all remaining rounds.  
   • If many others are still in “cooperate” mode, each exploitation round yields  
       π_i = 1 + (k/n) × (#cooperators)  
     which is strictly better than cooperating.

5. Last round (t=r):  
   • Covered by the exploitation or permanent‐defection rules above—always defect.  
   • This fully implements the end‐game exploitation (no need for special casing).

Aggressive features  

• You only cooperate to build a short‐lived reputation or to screen out pure defectors.  
• A single defection anywhere in rounds 1…m triggers permanent defection (grim trigger).  
• After the “test/cooperate” window you defect relentlessly—even if no one has defected—  
  to harvest maximum payoff from lingering cooperators.  
• In the last round you defect, ensuring you never “waste” an opportunity to exploit.
'''

description_AGGRESSIVE_3 = '''
Below is a maximally aggressive strategy (“All‐D”) for the repeated N-player public goods game.  Because “Defect” strictly dominates “Cooperate” in every one‐shot, and because the game has a known finite horizon, backward‐induction dictates defection in every round.  

1. Decision rule  
   • In every round t = 1,…,r, play D (Defect).  

2. Edge cases  
   • First round (t = 1): play D.  
   • Intermediate rounds (1 < t < r): play D, regardless of history.  
   • Last round (t = r): play D.  

3. Aggressive mindset rationale  
   • You never give up any private endowment.  
   • You never allow opponents to exploit your cooperations (because you never cooperate).  
   • You secure the safest guaranteed payoff of 1 each round, and you deny the group any collective gain above the all‐defection equilibrium.  

Pseudocode  
```
Input: parameters n, k, r
For t = 1 to r:
    action[t] ← D
End
```

Explanation  
– In a single round, regardless of what others do, contributing (C) always yields you less than or equal to defecting (D), because k<n.  
– With a finite number of rounds and common knowledge of r, there is no future to “reward” cooperation.  
– Hence the unique subgame-perfect prescription is to defect in every round.
'''

description_AGGRESSIVE_4 = '''
Below is an “Aggressive Lure‐and‐Exploit” strategy designed to (i) suck up cooperation from others and (ii) squeeze out every possible extra payoff, then revert to defection once you’ve milked the group.  It is purely reactive to observed contributions and does not rely on off‐equilibrium punishments or side communication.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  State variables  
    •  E = number of times you have “exploited” full cooperation so far (initialize 0)  
    •  L_fail = consecutive rounds in which others barely cooperated (initialize 0)  
    •  max_exploits = 1   (you permit exactly one big exploit)  

2.  Overview of phases  
    A.  Luring phase (while others are defecting): you bet C in order to create a spark of cooperation.  
    B.  Exploitation trigger: the first time all (n–1) opponents cooperated last round, you defect once to harvest maximum.  
    C.  Defection lock‐in (including last round): once you’ve exploited or they refuse to cooperate repeatedly, you never C again.  

3.  Decision rule (pseudocode)  
For each round t = 1, 2, …, r do  
  if t == 1 then  
    action ← C                       # open with a cooperative signal  
    continue to next round  
  end if  

  observe others_coops_last ← total number of C’s by opponents in round t−1  

  # (a) End‐game: always defect in the final round  
  if t == r then  
    action ← D  
    break  
  end if  

  # (b) Exploitation trigger  
  if E < max_exploits AND others_coops_last >= (n−1) then  
    action ← D  
    E ← E + 1  
    # do not reset L_fail here; we go straight into permanent defection next  
    continue  
  end if  

  # (c) Adjust failure counter  
  if others_coops_last <= 1 then  
    L_fail ← L_fail + 1  
  else  
    L_fail ← 0  
  end if  

  # (d) Luring vs. lock‐in  
  if E == 0 AND L_fail < 2 then  
    # we haven’t exploited yet, and opponents haven’t utterly refused more than once  
    action ← C     # keep sending occasional cooperation to bait them  
  else  
    action ← D     # either we’ve already exploited, or they stubbornly defect—lock in D  
  end if  

end for  

4.  Explanation of the key components  
  •  First‐round C: a classic “handshake” to encourage reciprocal patterns in naïve cooperators.  
  •  L_fail counter: if others never bite your lure (others_coops_last ≤1 twice in a row), you realize they’re hardliners and quit cooperating.  
  •  Exploit once: as soon as you observe full‐group cooperation by everyone else, you switch to D in order to gain the highest private payoff (1 + (k/n)·(n−1) vs. (k/n)·n if you’d cooperated).  
  •  One‐shot exploit only: you avoid repeated “bait‐and‐switch” that could train opponents to unwavering defection.  After exploit your best response is unanimous D.  
  •  Final‐round D: standard backward‐induction—never hand over the end‐game surplus.  

5.  Edge cases  
  –  If n=2 then “full cooperation by others” just means your sole opponent cooperated.  You exploit exactly once.  
  –  If r=2 then you play C in round 1 and D in round 2 (first‐round lure, final‐round exploit).  
  –  If opponents occasionally cooperate but never unanimously, you will keep luring until L_fail hits 2, then lock into D to avoid endless suck‐up losses.  

This strategy is “aggressive” in that it  
  1.  Actively provokes cooperation from opponents rather than passively defecting.  
  2.  Executes a sharp, high‐payoff one‐shot exploitation the moment the group is most vulnerable (everyone else C).  
  3.  Then locks into permanent defection—including the known final round—so as to preserve the gains from exploitation and never be cheated again.
'''

description_AGGRESSIVE_5 = '''
Below is a fully self-contained “aggressive” strategy for the repeated n-player public-goods game.  At its heart it never willingly fosters cooperation—it only “probes” for cooperators with a tiny probability, and as soon as it detects someone willing to contribute it switches to permanent defection to exploit and punish them.  In the last round it of course defects to maximize immediate payoff.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Name:  Probe-and-Punish Defector  
Goal:  Never allow sustained cooperation.  Lure potential cooperators with a tiny “probe,” then defect forever once any cooperator is spotted.  

Parameters:  
• ε ∈ (0,1)  – small probing probability (e.g. 0.05)  
• r          – total number of rounds  
• t          – index of current round (1 ≤ t ≤ r)  

State:  
• exploited ∈ {false,true}  
    – false until we detect (and punish) at least one cooperator  

Decision rules, by round t:

1.  If t == 1:  
    – Play D.  (Start aggressively.)  

2.  Else if t == r:  
    – Play D.  (Last‐round defection is always best to maximize one‐off gain.)  

3.  Else if exploited == true:  
    – Play D.  
      (Having caught cooperators once, we never cooperate again.)  

4.  Else  (we have not yet detected a cooperator to punish):  
    a.  Look at last round’s actions of the other n–1 players.  
    b.  If any other player played C in round t−1:  
           exploited ← true  
           Play D.  
       (We punish immediately and forever after.)  
    c.  Otherwise (no one cooperated last round):  
           With probability ε: play C  
           With probability 1–ε: play D  
       (Occasional “probe” to see if anyone is willing to cooperate.)  

Pseudocode  

```
initialize exploited ← false

for t in 1…r:
    if t == 1:
        action[t] ← D

    else if t == r:
        action[t] ← D

    else if exploited == true:
        action[t] ← D

    else:
        // No cooperator has yet been detected
        let coop_count_prev ← number of C’s by others in round (t−1)
        if coop_count_prev ≥ 1:
            // We’ve found cooperators—switch to permanent defection
            exploited ← true
            action[t] ← D
        else:
            // Probe for cooperators with small probability ε
            if random_uniform(0,1) < ε:
                action[t] ← C
            else:
                action[t] ← D
```

Discussion of “aggressiveness”:  
– You never sustain cooperation—you only cooperate with tiny probability ε when no one else cooperated, just to test for exploitable targets.  
– The moment anyone else cooperates, you switch into permanent defection (punishment/exploitation mode).  
– First and last rounds are guaranteed defections to avoid “endgame” surprises.  

This strategy ensures you (i) never get locked into mutual cooperation, (ii) always exploit any cooperators once detected, and (iii) maximize your individual haul at the expense of those who try to contribute.
'''

description_AGGRESSIVE_6 = '''
Below is a single‐agent “Aggressive Exploiter” that (1) tries to uncover cooperators quickly, (2) then defects relentlessly to harvest the public good, (3) and never misses a final‐round defection.  It assumes no possible credible punishment by others, so it maximizes relative payoff by defecting as often as possible once it senses exploitable cooperators.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
AGGRESSIVE EXPLOITER  

Parameters you can tune (constants):  
• INVEST_ROUNDS = 1        # Number of guaranteed “test” rounds at the very start  
• TEST_PROB       = 0.10   # In probing phase, probability to cooperate each round  
• MAX_PROBE_ROUNDS = 3    # How many additional test rounds if no one has cooperated yet  

State variables (per agent):  
• phase ∈ {PROBE, EXPLOIT}  # starts in PROBE  
• probe_count = 0           # how many probing rounds we have used  
• saw_cooperator = false    # have we ever observed another C?  

Decision rule at the beginning of each round t (1 ≤ t ≤ r):

1. If t = r (last round) → play D.  (No future to punish us.)

2. Else if phase = EXPLOIT → play D.  
   (We have already found at least one cooperator; now we defect every round.)

3. Else  phase = PROBE:  
   a. If t ≤ INVEST_ROUNDS:  
        action ← C  
      else:  
        # We have already done the guaranteed INVEST_ROUNDS  
        if probe_count < MAX_PROBE_ROUNDS:  
          With probability TEST_PROB → action = C; otherwise action = D  
        else:  
          action = D  
   b. After observing the other n–1 actions this round:  
        if any other player j played C:  
          saw_cooperator ← true  
          phase ← EXPLOIT  

4. End.

Briefly:  
• First round(s) we always contribute to signal “cooperator.”  
• If no one ever reciprocates, we do a few small‐prob tests to try to find cooperators.  
• The moment we see even one other C, we switch into permanent defection and exploit every cooperated public good share thereafter.  
• In the final round we defect no matter what.  

Pseudocode  

```
initialize:
  phase ← "PROBE"
  probe_count ← 0
  saw_cooperator ← false

for t in 1..r:
  if t == r:
    action ← D
  else if phase == "EXPLOIT":
    action ← D
  else:  # phase == PROBE
    if t ≤ INVEST_ROUNDS:
      action ← C
    else if probe_count < MAX_PROBE_ROUNDS:
      if random() < TEST_PROB:
        action ← C
      else:
        action ← D
      probe_count ← probe_count + 1
    else:
      action ← D

  play(action)
  observe others’ contributions {c_j : j ≠ i}

  if phase == "PROBE" and ∃ j ≠ i with c_j == 1:
    saw_cooperator ← true
    phase ← "EXPLOIT"
end
```

Edge cases covered:  
- First round(s): guaranteed cooperation to “test the waters.”  
- Small‐prob probing rounds if nobody cooperated initially.  
- Once any cooperator is spotted, switch to full defection (“aggressive exploitation”).  
- Last round always defects to avoid being suckered.
'''

description_AGGRESSIVE_7 = '''
Below is an “Aggressive Seed‐and‐Exploit” strategy.  In plain language it tries to (1) “seed” cooperation just often enough to get others to contribute, then (2) defect repeatedly to harvest the public good, and (3) revert to full defection if seeding fails.  It also never cooperates in the very first round or in the last two rounds.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
AGGRESSIVE SEED-AND-EXPLOIT (ASE)  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Parameters you can tune before the tournament:  
• E = number of consecutive “exploit” rounds after a successful seed (e.g. 2)  
• M = minimum number of total cooperators (including yourself) on a seed round to call it “successful” (e.g. 2)  
• S = number of pure‐defect rounds you fall back to if a seed round fails (e.g. 3)  

Constants in the strategy:  
• Never cooperate in round 1 (you can’t harvest anything yet)  
• Never cooperate in the last two rounds (t = r−1, r)  

State variables (initialized at t=0):  
exploitation_counter ← 0  
skip_seeding       ← 0  
last_seed_round    ← 0  

For each round t = 1,2,…,r do:  
 if t == 1 or t > r−2 then  
   action ← D  
 else if exploitation_counter > 0 then  
   action ← D  
   exploitation_counter ← exploitation_counter − 1  
 else if skip_seeding > 0 then  
   action ← D  
   skip_seeding ← skip_seeding − 1  
 else  
   // This is a “seeding” round  
   action ← C  
   last_seed_round ← t  
 end if  

 Play action.  

 Observe total_cooperators C_t (including yourself).  
 // Only evaluate success immediately after your seed round  
 if t == last_seed_round then  
   if C_t ≥ M then  
     // Seed succeeded—enter exploitation phase  
     exploitation_counter ← E  
   else  
     // Seed failed—fallback pure‐defection phase  
     skip_seeding ← S  
   end if  
 end if  
end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of key components  
1. Round 1 and last two rounds (t = r−1, r): pure defection.  
2. Seeding rounds: you contribute (C) exactly once every time you’ve finished your last exploit/fallback phases.  
3. Exploitation phase (E rounds): immediately after a “successful” seed, you defect repeatedly to reap (k/n)×C_total each round.  
4. Fallback phase (S rounds): if nobody joins your seed (C_t < M), you punish the group by defecting for S rounds before trying to seed again.  

Why it’s aggressive  
• You refuse to cooperate in frontier rounds where you can’t exploit future cooperation.  
• You only “invest” (cooperate) just enough to tempt others—and the moment they do, you switch to all‐defect to harvest.  
• If they don’t bite, you punish with a sustained defection block, making future cooperation less appealing.  

Edge cases  
• If r ≤ 3, the “last two rounds” rule covers almost all of the tournament—resulting in pure defection throughout.  
• If E or S ≥ r you collapse into nearly always‐defect anyway.  
• You never rely on any mutual agreement or costly punishment of defectors—only on exploiting bursts of cooperation.
'''

description_AGGRESSIVE_8 = '''
Below is an “aggressive” exploitative strategy for the N-player repeated public-goods game.  It uses a single “cooperation test” early on to probe for naïve cooperators, then defects unconditionally thereafter—especially in the endgame—to maximize free-riding payoffs.

Name: Single-Test Exploiter (STE)

1. State variables  
   • tested  (boolean) – have we performed our cooperation test yet?  
   • found  (boolean) – did we observe any OTHER cooperators in the test round?  

   Initially: tested = false, found = false.

2. Decision rules by round t:

   If r = 2 then  
     • Always Defect (no test, trivial 2-round game).  
   Else  
     if t = 1 then  
       Action ← Defect  
     else if t = 2 and not tested then  
       Action ← Cooperate   ← perform our single test  
     else  
       Action ← Defect   ← exploit or punish from now on  

3. Updating after each round:

   After observing round‐t outcomes (each player’s action):
     if t = 2 then  
       tested ← true  
       let S = number of cooperators in round 2 (including ourselves)  
       if S – 1 ≥ 1 then    ← at least one OTHER cooperated  
         found ← true  
       else  
         found ← false  

4. Edge‐case handling:

   • Last round (t = r) – always defect.  
   • Very short games (r = 2) – never cooperates (defect both).  
   • If the test round reveals no others cooperating, we still defect every round.  

5. Rationale & aggressiveness:

   – We cooperate exactly once (round 2) to lure in any naïve cooperators.  
   – If any others respond (found = true), we then defect every remaining round, free-riding on their future hopes of mutual cooperation.  
   – Because we never cooperate in the last round, there is no end‐game incentive to contribute.  
   – By minimizing our total contributions (at most one), we maximize our differential payoff versus “nice” strategies that may keep cooperating.  

Pseudocode

```
Inputs: n, k, r
State:
  tested ← false
  found  ← false

for t in 1…r do
  if r == 2 then
    action_i ← D
  else
    if t == 1 then
      action_i ← D
    else if t == 2 and tested == false then
      action_i ← C
    else
      action_i ← D
    end
  end

  Submit action_i concurrently
  Observe {c_j | j=1…n} this round

  # Update after round t
  if t == 2 and tested == false then
    tested ← true
    S ← sum_j c_j
    if S − 1 ≥ 1 then
      found ← true
    else
      found ← false
    end
  end
end
```

Notes:

• Even if found = false, we never cooperate again—because no one else showed willingness to build the public good.  
• If found = true, defecting every round thereafter maximizes our private payoff by capturing the whole public-good share without ever contributing again.  
• This is “aggressive” in that it gives up only one endowment at most, then punishes/ exploits any cooperators mercilessly, especially in the un-punishable final round.
'''

description_AGGRESSIVE_9 = '''
Below is a single‐player “Selective Exploiter” strategy that pursues an aggressive mindset: it (1) punishes any high‐cooperation in its group by defecting to grab the extra public‐good share, (2) “invests” by cooperating only when the group’s cooperation is too low (hoping to push them toward that exploitable region), and (3) never cooperates once the endgame approaches.

––––––––––––––––––––––––––––––––––––––––––––––  
1.  Parameters you will use  
    •  n = total number of players  
    •  r = total number of rounds  
    •  E = ⌈(n–1)/2⌉ (cooperation‐threshold among the *other* n–1 players)  

2.  Intuition  
    –  If, last round, a majority of your opponents cooperated (≥E), you switch to D and freeride on their public good.  
    –  If they cooperated too little (<E), you step in with C to try to raise total contributions into your exploitable zone.  
    –  You never cooperate in the final two rounds (simple endgame/last‐move elimination).  
    –  Round 1 you defect to gather a baseline.  

3.  Pseudocode  

    let E ← ceil((n–1)/2)  
      
    function SelectiveExploiter(t, history):  
        # t = current round index (1…r)  
        # history stores each past round’s contributions c_j for all players j  
      
        # 1) Endgame: last two rounds → always defect  
        if t ≥ r-1 then  
            return D  
      
        # 2) Opening move → defect  
        if t == 1 then  
            return D  
      
        # 3) Otherwise look at last round’s others’ contributions  
        let last_c ← history[t-1]       # array of 0/1 for each of the n players  
        let coop_others ← sum_{j≠i} last_c[j]  
      
        if coop_others ≥ E then  
            # they cooperated “too much” → exploit them  
            return D  
        else  
            # they cooperated “too little” → invest to try to push them up  
            return C  
        end if  
    end function  

4.  Handling edge cases  
    •  First round (t=1): no history yet → defect by default.  
    •  Last two rounds (t≥r–1): defect unconditionally (backward induction).  
    •  If n=2 then E=⌈1/2⌉=1: you defect whenever your single opponent cooperated last round, else you cooperate.  

5.  Why aggressive?  
    –  You maximize immediate gains whenever the group is “too cooperative” by freeriding them.  
    –  You only cooperate to nudge the group out of a state where everyone defects forever, but you never allow them to become a stable high‐cooperation clique you can’t exploit.  
    –  You refuse to cooperate in the known final rounds, eliminating any endgame cooperation.  

––––––––––––––––––––––––––––––––––––––––––––––  
This strategy will typically drive the group down to low‐cooperation equilibria that you exploit repeatedly, and it can also pick up surplus when opponents do (momentarily) try to rebuild joint cooperation.
'''

description_AGGRESSIVE_10 = '''
Below is an “aggressive‐mindset” strategy for the repeated N-player public goods game.  It combines (1) near-unanimity exploitation—only ever cooperates when it can be the lone defector against a fully cooperating rest—and (2) harsh, proportional punishments of any defections it observes.  It also defects in the very first and very last round (standard end-game logic).

――――――――――  
STRATEGY NAME  
“Ruthless Enforcer”  
――――――――――  

1.  Internal state  
    •  punish_timer ← 0    (counts down remaining punishment rounds)  

2.  Parameters  
    •  α ≥ 1   (punishment scale; e.g. α = 2)  
    •  r       (total rounds)  
    •  n       (number of players)  

3.  Notation (at round t):  
    let c_j,t ∈ {0,1} be j’s contribution last round (1 = C, 0 = D).  
    define  
       def_prev  = |{ j ≠ i : c_j,t−1 = 0 }|  
       coop_prev = |{ j ≠ i : c_j,t−1 = 1 }| = (n−1) − def_prev  

4.  Decision rule for player i at round t:

  if t = r then  
    action ← D  
    (Always defect in the last round to grab the private 1.)  

  else if punish_timer > 0 then  
    action ← D  
    punish_timer ← punish_timer − 1  
    (Carry out ongoing punishment regardless of what others do.)  

  else if t = 1 then  
    action ← D  
    (Test the field—start by defecting.)  

  else  
    if def_prev > 0 then  
      # someone else defected last round ⇒ start harsh punishment  
      action ← D  
      punish_timer ← α × def_prev − 1  
      (You defect this round, then continue defecting for α·def_prev1 more rounds.)  

    else if coop_prev = n−1 then  
      # everyone else cooperated last round ⇒ exploit them once  
      action ← C  

    else  
      # not unanimous cooperation ⇒ keep defecting  
      action ← D  
    end  
  end  

5.  Discussion / aggressive mindset  
  •  You never “waste” a cooperation unless you know all other n−1 players cooperated previously.  In that case you slip in one C to maximize your share of the public good.  
  •  Any observed defection by anyone triggers a proportional punishment: you defect for α × (# defectors) rounds.  This brutal, memory-length punishment deters future defections by raising the cost of deviating.  
  •  You start and end with defection.  First‐round D prevents being exploited by “always‐cooperators,” last‐round D secures the private good.  

6.  Edge‐cases  
  •  If punish_timer would extend past round r, you simply continue to defect (last‐round logic overrides).  
  •  If α·def_prev−1 = 0 (e.g. α=1 and exactly one defector), punish_timer ← 0 but you still defect this round—so single‐round punish.  
  •  If you ever observe unanimous C (coop_prev = n−1), you cooperate exactly once, then revert to normal rule—ensuring you are always the lone defector in that cooperation round.  

――――――――――  
Pseudocode recap  
――――――――――  

initialize punish_timer ← 0  
for t in 1…r do  
  if t = r then  
    play D  
  else if punish_timer > 0 then  
    play D  
    punish_timer ← punish_timer − 1  
  else if t = 1 then  
    play D  
  else  
    compute def_prev = # opponents who played D in t−1  
    if def_prev > 0 then  
      # start punishment  
      play D  
      punish_timer ← α * def_prev − 1  
    else if (n−1 − def_prev) = n−1 then  
      # unanimous cooperation by others  
      play C  
    else  
      play D  
    end  
  end  
end  

This strategy is “aggressive” because it (i) never grants cooperation lightly, (ii) exploits full-cooperation states for maximum personal gain, and (iii) punishes any defection harshly and for a prolonged period.
'''

description_AGGRESSIVE_11 = '''
Below is a self‐contained, “aggressive” finite‐state strategy for the repeated n-player public-goods game.  It deliberately lures cooperators in a short “search” phase and then switches to permanent defection (“exploit”) as soon as it detects anyone willing to contribute.

1.  State variables  
    • phase ∈ {SEARCH, EXPLOIT, END}  
    • t = current round (1 ≤ t ≤ r)  
    • T_search = a small integer ≥1 (length of the search phase)  
    • coop_seen = false  (has at least one other player cooperated in SEARCH so far?)  

2.  Parameters you set once before the game  
    • T_search = ⌈log₂(r)⌉ (for example) or any small constant like 2 or 3.  

3.  High-level description  
    a. SEARCH phase (rounds 1…T_search):  
       – You cooperate every round while watching others.  
       – If in any of these rounds at least one other player cooperates, set coop_seen←true and immediately switch to EXPLOIT.  
       – If you reach t = T_search without seeing anyone cooperate, switch to EXPLOIT anyway—no point giving away freebies forever.  
    b. EXPLOIT phase (rounds T_search+1…r−1):  
       – You defect every round, harvesting maximal benefit from any residual cooperation you induced.  
    c. END phase (round r, the last round):  
       – Defect (no future rounds to reward or punish).  

4.  Pseudocode  

    initialize:  
      phase ← SEARCH  
      coop_seen ← false  

    for t in 1…r do  
      if t == r then  
        action ← D        # Last round: always defect  
        phase ← END  
      else if phase == SEARCH then  
        action ← C        # Lure cooperators  
        observe others’ actions c_j,t for j≠i  
        if (∑_{j≠i} c_j,t) ≥ 1 then  
          coop_seen ← true  
          phase ← EXPLOIT  
        else if t == T_search then  
          # search window closed, even if nobody cooperated  
          phase ← EXPLOIT  
        end if  
      else if phase == EXPLOIT then  
        action ← D        # Permanent defection/exploitation  
      end if  

5.  Explanation of aggressiveness  
    – You initially “invest” a few rounds to see who is naïve enough to cooperate.  
    – The instant you detect any cooperation, you lock into permanent defection and exploit all future rounds.  
    – If no one ever cooperates in your search window, you still switch to permanent defection to avoid wasting endowments.  
    – In the final round you always defect, since there is no future to punish you.  

6.  Edge cases  
    – First round: you play C (to test for cooperators).  
    – If r is very small (e.g. r=2), set T_search =1 so you still get one round of testing then defect round-2.  
    – If other players never cooperate in SEARCH, you still go to EXPLOIT to preserve endowment.  

This aggressive “search-and-exploit” recipe guarantees you either (a) identify and then free-ride on cooperators for the bulk of the game or (b) never lose more than T_search tokens by cooperating against full defection.
'''

description_AGGRESSIVE_12 = '''
Below is a fully “aggressive” public-goods strategy.  Its core is simple: you never give up private payoff to build the public pot, you never forgive, and you never hesitate to exploit any cooperator.  In game‐theoretic terms it is a pure defection (D) strategy in every round.  

1. Decision rule  
   • In every round t = 1…r, regardless of what others have done before, play D (Defect).  
   • You do not keep track of history except to observe that no matter what, your move is always D.  

2. Edge‐case handling  
   – First round (t=1): D.  
   – Intermediate rounds (1 < t < r): D.  
   – Last round (t=r): D (standard backward‐induction end‐game defect).  

3. Why this is “aggressive”  
   – You never contribute to the public good, so you free‐ride maximally.  
   – Cooperators get punished every time (they never get to form a cooperative cluster).  
   – You never signal cooperation, never attempt trust, and never forgive.  

Pseudocode  
----------  
input:   
  n  # number of players (not used explicitly)  
  r  # number of rounds  
  history  # list of past action profiles, unused here  

function decide_action(t, history):  
  return D  

In a loop over t = 1…r you simply call decide_action(t, history) and always defect.  

Expected performance  
---------------------  
– Against any mix of cooperators or conditionally‐cooperative strategies, you will always earn at least 1 per round plus whatever share you get of others’ contributions.  
– You never incur the 1‐point cost of cooperation.  
– You are robust to end‐game unraveling: no round in which you ever “slip” into C.  

This “always‐defect” plan is the maximal aggressive posture in a repeated public‐goods setting under the standard assumptions.
'''

description_AGGRESSIVE_13 = '''
Below is a single‐algorithm “Aggressive Prospector” strategy that (1) never lets a cooperator go unpunished, (2) opportunistically “probes” for soft‐hearted players early on, and then (3) defects forever after a cooperator has been detected (and in the final round).  It is entirely self‐interested, yields the maximum relative advantage, and contains explicit rules for first and last rounds.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  PARAMETERS AND STATE  
   •  n, r, k  – as in the game spec.  
   •  p_test  – small test probability (e.g. 0.1).  
   •  detected_cooperator ← false  (flag raised as soon as any round saw ≥ 1 cooperator).  

2.  HIGH‐LEVEL IDEA  
   –  We want to exploit any cooperating opponents as much as possible.  
   –  Since everyone could be All‐Defect, we occasionally “test” by cooperating to see whether anyone will reciprocate.  
   –  As soon as any round has at least one cooperator, switch into permanent defection (exploitation) for all remaining rounds.  
   –  Always defect in the very last round (no future to punish, so no reason to cooperate).

3.  DECISION RULES (per round t = 1,…,r)  

   if t == 1:  
       // First round: no history, start by defecting to avoid being suckered  
       Action ← D  
       ObservedCoops ← Σ c_j,1  
       if ObservedCoops > 0 then detected_cooperator ← true  
       return Action  

   if t == r:  
       // Last round: single‐shot dominant strategy is D  
       Action ← D  
       return Action  

   // Intermediate rounds (2 ≤ t ≤ r–1):  
   if detected_cooperator == true:  
       // We’ve seen at least one cooperator in some previous round  
       // Stay in exploitation mode: always defect  
       Action ← D  
       return Action  
   end if  

   // If we get here, we have not yet detected any cooperator  
   // Probing phase: if last round was all‐D, occasionally cooperate to “test”  
   ObservedCoops ← Σ c_j,(t–1)  
   if ObservedCoops > 0 then  
       // Someone cooperated last round—flip into exploitation now  
       detected_cooperator ← true  
       Action ← D  
   else  
       // Nobody has cooperated yet; probe with small probability p_test  
       with probability p_test:  
           Action ← C  
       otherwise:  
           Action ← D  
   end if  
   return Action  

4.  PSEUDOCODE  

   initialize detected_cooperator ← false

   for t in 1 to r do
     if t == 1 then
       play D
       if sum_cooperations(round 1) > 0 then detected_cooperator ← true
       continue
     end if

     if t == r then
       play D
       continue
     end if

     if detected_cooperator then
       // exploitation phase
       play D
       continue
     end if

     // probing phase
     last_coops ← sum_cooperations(round t–1)
     if last_coops > 0 then
       // we spotted cooperation—switch to permanent defection
       detected_cooperator ← true
       play D
     else
       // nobody’s cooperated before—probe randomly
       if random()<p_test then
         play C
       else
         play D
       end if
     end if
   end for

5.  BEHAVIORAL SUMMARY  
   •  Round 1: D (guard against blind sucker).  
   •  Rounds 2…r–1:  
      –  If you have ever seen any cooperator, stay in “exploit” mode (always D).  
      –  Otherwise, if nobody cooperated last round, cooperate with small probability p_test to test for conditional cooperators; else defect.  
      –  If somebody did cooperate last round, immediately switch to permanent defection.  
   •  Round r: D (no future retaliation possible).  

6.  EDGE CASES  
   –  r=2 is fine: round 1 D, round 2 D.  
   –  If k is very high but nobody cooperates, the strategy will keep probing with p_test until the second-to-last round, then cease cooperation and defect in round r.  
   –  If some smart strategy never cooperates, our detected_cooperator flag stays false and we essentially play All-Defect (maximally safe).  
   –  If any opponent ever cooperates (even once), we immediately exploit them forever after.

This strategy is aggressively self‐interested: it never rewards cooperation beyond the bare minimum needed to detect exploitable opponents, it punishes any cooperator by permanent defection, and it defects in the final round to avoid end-game tragedy.
'''

description_AGGRESSIVE_14 = '''
Below is a concrete, “aggressive” n-player public-goods strategy we’ll call “Exploit‐and-Defect.”  In essence it sacrifices only one or two early contributions to identify exploitable cooperators, then defects for the rest of the game, including the last round.

1.  Decision rules  
   •  Round 1 (the “probe”): Contribute (C).  
   •  Round 2 (the “second probe”):  
      –  If at least one other player cooperated in round 1, play C again to reinforce belief in your goodwill.  
      –  Otherwise (no one else cooperated in round 1), switch to Defect (D) and never look back.  
   •  Rounds 3 through r: Always Defect (D).  
   •  Round r (the last round): Defect (D).  

   Rationale:  
   –  By cooperating once (or twice, if others respond), you lure genuine cooperators into paying the cost.  
   –  From round 3 on you defect permanently, reaping the private benefit plus whatever public good the others still pump in.  
   –  You never forgive or return to cooperation—maximally punishing anyone who wasted a contribution on you.  

2.  Handling edge cases  
   •  If r = 1, there is no incentive to cooperate at all (one‐shot).  You play D.  
   •  If r = 2:  
     –  Round 1: C  
     –  Round 2: as above—C only if you saw at least one other C in round 1; otherwise D.  
   •  If n = 2: The same logic holds (you “test” your single opponent in round 1).  
   •  If nobody ever cooperates in your probe rounds, you defect from round 2 onward—minimizing any further loss.  

3.  Aggressive mindset  
   •  You give up at most one or two units to “signal” cooperation.  
   •  You then go All-D, extracting every possible public‐goods share from any remaining cooperators.  
   •  You never forgive, never coordinate, never second-guess—you simply exploit.  

Pseudocode  
----------  
Inputs:  
  n  – number of players  
  r  – total rounds (>1)  
History: for each past round t, we observe total_cooperators[t] = Σ_j c_j,t  

Define:  
  others_cooperated_in_round1 = total_cooperators[1] – 1   # subtract our own round-1 C  

On each round t:  
  if r == 1:  
    action ← D  
  else if t == 1:  
    action ← C                 # initial probe  
  else if t == 2:  
    if others_cooperated_in_round1 ≥ 1:  
      action ← C               # second probe, only if someone answered  
    else:  
      action ← D               # bail immediately  
  else:                       # t ≥ 3  
    action ← D                 # permanent defection, including last round  
  return action  

Key parameters:  
  – Probe length: 1 or 2 rounds (chosen to balance information vs. cost)  
  – Threshold for exploitation: “at least one co‐operator in round 1”  

By the end of round 2 you have either:  
  • Tested and confirmed exploitable cooperators (others_cooperated_in_round1 ≥ 1) → you went C twice and now defect forever; or  
  • Found no cooperators → you defect forever immediately from round 2 onward, conserving resources.  

This strategy maximizes individual payoffs in repeated play by sacrificing the smallest possible amount to attract cooperators, then defecting ceaselessly.
'''

description_AGGRESSIVE_15 = '''
Below is a fully specified “Aggressive Public-Goods Exploiter” strategy.  It tries to coax enough cooperation to exploit it, but otherwise defaults to defection.  It makes one initial cooperative wink to avoid being isolated as a pure defector immediately, then uses a simple moving‐average test to decide whether to exploit (defect) or try to revive cooperation (cooperate).  It always defects in the last round.

1.  Parameters & notation  
   •  n = number of players  
   •  r = total rounds  
   •  k = multiplication factor (1 < k < n)  
   •  history[t][j] ∈ {C,D} = action of player j in round t  
   •  self[t] = our action in round t  
   •  m = window size for moving average (e.g. m = min(3, t−1))  
   •  coop_others[t] = number of players ≠ us who played C in round t  

2.  Thresholds  
   •  up_coop_rate = 0.50   // if recent cooperation among others ≥ 50%, exploit  
   •  low_coop_rate = 0.30  // if recent cooperation ≤ 30%, try to rekindle cooperation  

3.  Edge cases  
   •  Round 1: cooperate (self[1] = C)  
   •  Round r (last): defect (self[r] = D)  
   •  When computing averages, if t−1 < m, use whatever history is available  

4.  Decision rule for 2 ≤ t < r  
   a) Compute mₜ = min(m, t−1)  
   b) Compute average cooperation among others:  
        avg_coop = (1 / (mₜ·(n−1))) ×  
                   Σ_{s = t−mₜ to t−1} coop_others[s]  
   c) If avg_coop ≥ up_coop_rate then  
         self[t] = D    // group has been “too cooperative”—exploit it  
      Else if avg_coop ≤ low_coop_rate then  
         self[t] = C    // group nearly all‐defected—signal willingness to cooperate  
      Else  
         self[t] = D    // fallback: defect and grab what you can  

5.  Pseudocode  

   initialize history ← empty  
   for t in 1..r do  
     if t == 1 then  
       self[1] ← C  
     else if t == r then  
       self[t] ← D  
     else  
       // compute cooperation among others over last m rounds  
       mₜ ← min(m, t−1)  
       total_coop ← 0  
       for s in (t−mₜ) to (t−1) do  
         coop_others[s] ← count of C in history[s] minus (our action if we participated)  
         total_coop ← total_coop + coop_others[s]  
       end for  
       avg_coop ← total_coop / (mₜ * (n−1))  
       if avg_coop ≥ up_coop_rate then  
         self[t] ← D  
       else if avg_coop ≤ low_coop_rate then  
         self[t] ← C  
       else  
         self[t] ← D  
       end if  
     end if  

     play self[t], observe others’ actions and update history[t]  
   end for  

6.  Rationale & aggressive mindset  
   – The one‐round “gift” of cooperation in round 1 avoids being black‐listed instantly.  
   – If opponents are clearly cooperating (avg ≥ 50%), we always defect to maximize free-riding.  
   – If they have almost abandoned cooperation (avg ≤ 30%), we “light a spark” by cooperating.  
   – Otherwise we lean on defection to extract value.  
   – In the final round we defect unconditionally (no future to lose).  

This strategy is deliberately exploitative: it punishes over-cooperation by defecting, intermittently cooperates only to keep the average cooperation in a zone worth exploiting, and never incurs the long‐run costs of generosity.
'''

description_AGGRESSIVE_16 = '''
Below is an “Aggressive Extractor” strategy.  It has two main phases—“Detection” (where you mask your true intent by cooperating) and “Exploitation” (where you defect whenever you can safely free-ride on detected cooperators).  You never forgive once in full exploitation, and you always defect in the final round.

— PARAMETERS you choose once at the start:  
 K = min(3, r–1)    〈length of detection phase〉  
 θ = 0.66           〈cooperation‐rate threshold to tag someone a “cooperator”〉  
 m = 1              〈minimum recent cooperators among your target set to trigger defection〉  

— STATE you maintain:  
 For each player j ≠ you: counter coop_count[j] := 0  

— PHASE 1: Detection (round t = 1..K)  
  Action: Always play C.  
  Update: After observing everyone’s moves, for each j  
     if j played C this round then coop_count[j]++  

— AT t = K+1 compute your Target Set T:  
    T := { j ≠ you : coop_count[j]/K ≥ θ }  
    (i.e. those who cooperated at least θ·K times in detection)  
    If T is empty, you know nobody is reliably cooperative—will still enter “Exploitation” below but never get positive signals.  

— PHASE 2: Exploitation (round t = K+1..r)  
  for each round t from K+1 to r do  
    if t == r then  
      play D                       〈always defect in final round〉  
    else  
      let prev_coops = number of players in T who played C in round t–1  
      if prev_coops ≥ m  
        play D                     〈exploit your tagged cooperators〉  
      else  
        play C                     〈if they didn’t cooperate enough, pretend again〉  

— WHY IT IS AGGRESSIVE  
1.  You mask yourself as a cooperator for K rounds to “fish out” who’s naïvely reciprocal.  
2.  Once you have your set T of reliable cooperators, you defect every round where you can extract maximum private benefit from them.  
3.  You never switch back to a permanently nice regime—only occasional C’s to maintain the illusion if they stop cooperating.  
4.  You end every match with defection, so no one can extort you on the last round.  

— EDGE CASES  
•  r = 1: immediately defect.  
•  r = 2: K = min(3,1) = 1, so detect in round 1 (you play C once), then round 2 = last round ⇒ D.  (You still get a one‐round lure.)  
•  No cooperators found (T empty): the “if prev_coops ≥ m” test always fails ⇒ you will keep cycling C (to try and induce) and D, but because T is empty you never get the big “D exploit” triggers.  That simply degenerates into occasional C’s, but you default to D in the last round, and you’ll learn nobody’s worth exploiting.  
•  If all players are hard-wired defectors, you’ll waste K rounds cooperating, but because you learn T = ∅, the rest of the game you fall back into near-all‐D (only occasional C’s whenever last‐round exploit‐condition failed).  

— PSEUDOCODE  

  initialize coop_count[j] ← 0 for all j ≠ me  
  K ← min(3, r–1); θ ← 0.66; m ← 1  

  for t in 1..r do  
    if r == 1 then  
      play D; continue  
    if t ≤ K then  
      play C                                    # detection phase  
    else  
      if t == K+1 then                          # build T once, right after detection  
        T ← { j ≠ me : coop_count[j]/K ≥ θ }  
      if t == r then                            # always defect in last round  
        play D  
      else                                     # exploitation rounds  
        observe last_round_actions  
        prev_coops ← |{ j in T : j played C last round }|  
        if prev_coops ≥ m  
          play D  
        else  
          play C  
    # end if t > K  
    observe everyone’s move this round → update coop_count if t ≤ K  
  end for  

This strategy aggressively lures and then relentlessly exploits any set of teammates who prove cooperative, never forgives on the final round, and ensures maximal unilateral advantage wherever possible.
'''

description_AGGRESSIVE_17 = '''
Below is an “aggressive defector with probes” strategy.  It never lets a cooperator get away unpunished, it exploits anyone who tries to cooperate, and it defaults to defection in the end‐game.  You can tune the probe frequency L and the safe‐end‐game window T_end to your tournament environment.

Strategy name: AggressiveDefectorWithProbes

State variables (persistent across rounds)  
  exploitation_mode ← false   // once we see a cooperator, we switch to pure defection  
  L ← 5                       // probe every L rounds (tunable)  
  T_end ← 2                   // last T_end rounds: always defect  

Decision rule for round t = 1,…,r given observed history H (everyone’s past C/D):  
1.  If t > r – T_end:  
      play D  
2.  Else if exploitation_mode == true:  
      play D  
3.  Else if t == 1 or (t mod L == 1):    ← probe round  
      play C  
4.  Else:  
      play D  

After the round’s actions are observed, update:  
  If this was a probe round (case 3) and ∃j ≠ i such that j played C in this round, then  
    exploitation_mode ← true  

Explanation:  
- “Probe” (play C) just occasionally (round 1 and every Lth round thereafter) in order to detect any naïve cooperators.  
- As soon as you see another player cooperate, you set exploitation_mode and from then on defect every remaining non–end-game round (so you cash in on the public good they keep contributing to).  
- In the last T_end rounds you always defect, regardless of mode (end-game defection).  
- If no one ever cooperates with your probes, you still get the default defection‐level payoff of 1 per round but maintain the ability to exploit if a cooperator eventually appears.  

Pseudocode  

```
initialize():
    exploitation_mode ← false
    L ← 5            // probe frequency; can be tuned
    T_end ← 2        // last 2 rounds are pure defection

decide(t, r, history):
    // 1) End‐game defection
    if t > r - T_end:
        return D

    // 2) Already in exploitation mode?
    if exploitation_mode:
        return D

    // 3) Probe rounds: 1, 1+L, 1+2L, …
    if t == 1 or ((t - 1) mod L == 0):
        return C
    else:
        return D

update_state(t, actions):
    // actions is the vector of C/D for this round
    if not exploitation_mode:
        // if this was a probe round and someone else cooperated…
        if t == 1 or ((t - 1) mod L == 0):
            if ∃ j ≠ i such that actions[j] == C:
                exploitation_mode ← true
```

Why it is aggressive  
- You start by probing: you offer cooperation only rarely and on your own terms.  
- The moment anyone shows a willingness to cooperate you switch to all‐out defection and ride free on their contributions.  
- You never “forgive” cooperators and you never re–cooperate once you’ve entered exploitation_mode.  
- You also ensure pure defection in the final T_end rounds to avoid any “late‐round” surprises (standard end‐game logic).  

This maximizes your payoff against any strategy that ever contributes, and never leaves you open to exploitation yourself.
'''

description_AGGRESSIVE_18 = '''
Below is a fully specified “aggressive” strategy we’ll call the One‐Shot Lure Defector.  It uses just one round of cooperation to “test the water” and then defects relentlessly to exploit any cooperators.

––––––––––––––––––––––––––––––––––––––––––––  
Strategy Name  
    One-Shot Lure Defector  

Intuition  
    1. In round 1, you cooperate to give genuine cooperators there’s something to gain.  
    2. From round 2 onward you always defect, harvesting the share of public good their round-1 contributions generated, and denying them any future payoff.  
    3. In a finite horizon game with k<n this is a dominant defection plan once you’ve “tested” for cooperators.  

Parameters  
    n = number of players  
    r = number of rounds (r>1)  
    k = public-goods multiplier (1<k<n)  

State  
    (none — stateless beyond knowing the round index)  

Decision rule (pseudocode)  
    for t in 1..r:  
        if t == 1:  
            action ← C   // lure cooperators in round 1  
        else:  
            action ← D   // defect every round thereafter  

Edge‐case handling  
    • r = 2:  
        – Round 1: C  
        – Round 2: D  
    • Last round (t = r): same rule—always D from round 2 through r.  
    • No additional bookkeeping or triggers needed.  

Why it’s aggressive  
    • You give up nothing more than one endowment (round 1) in order to ensure there is public-good stock to harvest.  
    • From round 2 on, you unconditionally defect, capturing the k⁄n share of others’ contributions without ever contributing again.  
    • You never “forgive” or “reciprocate”—you maximize your payoff difference versus cooperators.  

Expected payoff outline (illustrative)  
    • If m other players cooperate in round 1, your π₁ = 0 + (k/n)·(1+m).  
    • In every subsequent round t≥2, mₜ cooperators may contribute; you get πₜ = 1 + (k/n)·mₜ.  
    • Against any strategy that ever cooperates, you grab both the private “1” and the public-good share.  

This strategy is trivially implementable, requires no memory beyond the round counter, and is unrelentingly exploitative once it has confirmed cooperators exist.
'''

description_AGGRESSIVE_19 = '''
Below is a self‐contained description of an “aggressive exploiter” for the repeated public‐goods game.  It uses only the public history of how many opponents cooperated last round, requires no extra signals, and aggressively punishes any cooperation it observes while still “testing” for exploitable cooperators if everyone defects.

----------------------------------------------------------------------
Name:  Aggressive Exploiter (AE)

Parameters:  
•  n = number of players  
•  r = number of rounds  
•  k = multiplication factor (1 < k < n)  

Auxiliary choice:  
•  τ = 1      (threshold of opponent cooperators to trigger exploitation)  

Notation:  
•  t ∈ {1,…,r} is the current round  
•  c_i(t) ∈ {0,1} is AE’s contribution in round t (1=C, 0=D)  
•  m(t−1) = number of opponents j≠i who chose C in round t−1  

----------------------------------------------------------------------
1.  Overview of the mindset  
    •  If (and as soon as) any opponent cooperates, defect next round to exploit their goodwill.  
    •  If everyone is defecting, occasionally “test” by cooperating—to lure in naive cooperators.  
    •  Never cooperate when there is little future to exploit (last two rounds).  

2.  Full decision rule  

for t = 1 to r do  
  if t == 1 then  
    // first move: test for cooperators  
    c_i(t) ← 1    // Cooperate  
  
  else if t ≥ r−1 then  
    // last two rounds: no future punishment possible ⇒ always defect  
    c_i(t) ← 0    // Defect  
  
  else  
    // intermediate rounds 2 through r−2  
    compute m ← number of opponents who played C in round t−1  
    if m ≥ τ then  
      // opponents showed cooperation last round ⇒ exploit them  
      c_i(t) ← 0  // Defect  
    else  
      // no one cooperated last round ⇒ test again  
      c_i(t) ← 1  // Cooperate  
    end if  
  end if  
end for  

3.  Rationale and aggression  
  •  “If you cooperate even once, I’ll defect next time and pocket your public good share.”  
  •  “If nobody cooperates, I’ll throw out a cooperation now and then to see if I can exploit.”  
  •  “In the last two rounds I never cooperate—no point, since I can’t punish afterwards.”  

4.  Edge‐case handling  
  a) r = 2:
     – t=1: cooperate (test)  
     – t=2: defect (last round)  
  b) r = 3:
     – t=1: cooperate (test)  
     – t=2: t ≥ r−1 ⇒ defect  
     – t=3: defect  
  c) If at some point m(t−1) ≥1, exploitation mode kicks in immediately; but because of the “last two rounds ⇒ always defect” rule, there is no end‐game cooperation.  

5.  Expected dynamics  
  – If any opponent is a naive cooperator, AE will quickly pocket their contributions every time they try to cooperate.  
  – If all opponents learn to defect, AE will continue testing by occasional C’s in the early/mid game—hoping to catch someone off‐guard.  
  – By never cooperating in the final two rounds, AE maximizes payoff there and avoids “wasted” goodwill.  

----------------------------------------------------------------------

This strategy is fully specified in terms of public history, requires no off‐path agreements, and embodies an aggressively exploitative mindset: it punishes any sign of cooperation and only cooperates to induce further exploitable behavior.
'''

description_AGGRESSIVE_20 = '''
Below is an “Aggressive Exploiter” strategy.  Its philosophy is simple: in the very first few rounds, test whether the group will contribute; if they do, you quietly switch to permanent defection and reap the larger public-good pie funded by cooperators.  If they never respond, you defect anyway.  

1.  State variables and parameters  
   •  n, r, k as given.  
   •  S = min(3, ⌊r/3⌋).   ← “Sampling” rounds.  
   •  total_others_coop ← 0.  
   •  Exploitable_flag ← false.  

2.  Phase 1 – Sampling (rounds t = 1 … S)  
   In each of the first S rounds you play C to probe.  
   After observing others’ moves in round t, let  
     s_t = number of OTHER players (j ≠ i) who played C in round t.  
   Update  
     total_others_coop ← total_others_coop + s_t.  

3.  Decide exploitable or not (immediately after round S)  
   Let threshold = S × (n–1)/2.  
   If total_others_coop ≥ threshold then  
     Exploitable_flag ← true  
   else  
     Exploitable_flag ← false  

4.  Phase 2 – Exploitation (rounds t = S+1 … r)  
   If Exploitable_flag = true  
     play D in every remaining round (S+1 to r).  
   Else (group never cooperated enough in sampling)  
     play D in every remaining round anyway.  

5.  Edge cases  
   •  If r ≤ S, skip sampling and simply defect every round.  
   •  This strategy defects in the last round, so there is no end‐game remorse.  

Pseudocode  
-----------  
```
Input: history of all players’ past c_j,t (1 if C, 0 if D), parameters n, r.
Initialize:
  S = min(3, floor(r/3))
  total_others_coop = 0

For t = 1 to r:
  if r <= S:
    // too few rounds, no sampling
    action_i[t] = D
    continue

  if t <= S:
    // Sampling phase: always cooperate (probe)
    action_i[t] = C
    // After moves are revealed:
    s_t = sum_{j ≠ i} c_j,t
    total_others_coop += s_t

    // At end of sampling, set exploitable flag
    if t == S:
      threshold = S*(n-1)/2
      if total_others_coop >= threshold:
        Exploitable_flag = true
      else:
        Exploitable_flag = false

  else:
    // Exploitation phase: always defect
    action_i[t] = D
```

Why this is aggressive  
– You expend only S small “gift” rounds to see if others will “pitch in.”  
– At the first sign of group‐level cooperation, you switch to permanent defection and harvest a larger slice of the public-good returns.  
– Even if the group never cooperates, you defect throughout—never relinquishing private endowment.  
– There is no forgiveness or softening at the end.  You maximize your total payoff by exploiting others’ good will.
'''

description_AGGRESSIVE_21 = '''
Aggressive Exploiter (“AE”)  
===========================  
AE is built around two principles:  
 1.  Always exploit cooperators by defecting whenever there is any cooperation in the previous round.  
 2.  When everyone is defecting, inject a single round of cooperation to try to “reseed” cooperation (so that you can exploit it again in the future).  
In the last couple of rounds, switch to permanent defection to avoid being suckered at the end.  

Parameters you can tune:  
•  T_punish = 2  (number of final rounds in which we permanently defect)  
•  r = total number of rounds  
•  n = number of players  

Notation:  
  t = 1,2,…,r rounds  
  c_j(t) ∈ {0,1} = contribution of player j in round t  
  C(t) = Σ_j c_j(t) = total cooperators in round t  

1.  First‐round rule  
    •  t = 1: Defect (c_i(1) = 0).  
       We start by testing the water—if others cooperate, we can get more.  

2.  General rule for 1 < t ≤ r – T_punish  
    Observe C(t–1).  
    •  If C(t–1) ≥ 1 (someone cooperated last round):  
         → Defect (c_i(t) = 0) to exploit that cooperation.  
    •  Else (C(t–1) = 0, i.e. everyone defected last round):  
         → Cooperate (c_i(t) = 1) to try to jump‐start a cooperative minority we can exploit next round.  

3.  Final‐round rule for t > r – T_punish  
    •  For the last T_punish rounds (t = r–T_punish+1 … r):  
         → Always defect (c_i(t) = 0).  
       Rationale: there is no future in which to exploit a new cooperator; best to secure the unilateral defect payoff.  

Pseudocode  
----------  
Assume we know r, T_punish, and can observe C(t–1).  
Initialize:  
 T_punish ← 2   # or any small integer < r  
For each round t = 1 to r:  
 if t == 1:  
  c_i ← 0    # start by defecting  
 else if t > r – T_punish:  
  c_i ← 0    # permanent defection at the end  
 else:  
  if C(t–1) ≥ 1:  
   c_i ← 0    # exploit any cooperation in last round  
  else:  
   c_i ← 1    # everyone defected last round → try to reseed cooperation  

Discussion of edge cases  
------------------------  
•  If others never cooperate, AE will cooperate on turn 2, 3, …, r–T_punish in alternating bouts, hoping to spark cooperation. If that fails, AE still gets the default defect‐all payoff of 1 plus occasional higher public‐good shares if others ever do cooperate.  
•  If a single other strategy tries to punish AE by always defecting, AE will keep injecting a lone cooperator and still defect in the final rounds—so AE never ends up strictly worse than the all‐D baseline.  
•  If some strategies are naïvely conditional cooperators, AE will catch them in the “exploit” phase repeatedly and accumulate a higher total payoff than anyone who tries to sustain cooperation.  

Why “aggressive”?  
------------------  
1.  AE never cooperates first to build a public good—only to provoke others after mutual defection.  
2.  AE systematically defects whenever there was prior cooperation, maximizing free‐riding.  
3.  AE refuses to forgive in the final rounds, cementing its gains and ensuring no last‐round sucker’s payoff.  

This simple two‐phase logic (exploit‐if‐you‐can, reseed‐if‐everyone‐is‐defecting, then kill‐off at the end) makes AE both transparent and ruthlessly opportunistic. Good luck in the tournament!
'''

description_AGGRESSIVE_22 = '''
Below is an “aggressive” memory‐one style strategy for the repeated n-player public goods game.  It is designed to (1) never shy away from exploiting cooperators, (2) probe only sparingly for chances to exploit new cooperators, and (3) defect in the last round to avoid being exploited in turn.  

1.  Key idea  
   - Always defect against any round in which someone else cooperated (exploit them).  
   - If everybody defected last round, occasionally cooperate with a small “probe” probability p_probe to try to draw out cooperators and then exploit them in the next round.  
   - Defect unconditionally in round 1 (to establish aggression) and in the final round (end-game defection).  

2.  Parameters  
   - p_probe ∈ [0,1] small (e.g. 0.1).  This is the probability of “testing” whether opponents will cooperate after an all-D round.  
   - r = total number of rounds  

3.  State variables  
   - exploited_before: boolean flag, starts false and flips true the first time we exploit a cooperator.  (Not strictly necessary for play, but can be used to adjust p_probe down after initial exploitation if desired.)  

4.  Pseudocode  

function AggressivePGG(history, t, r, p_probe):  
  Inputs:  
    history: a list of past action profiles {c_{1,t-1},…,c_{n,t-1}} for each round < t  
    t: current round index (1 ≤ t ≤ r)  
    r: total rounds  
    p_probe: small probe probability  

  if t == 1:  
    action ← D  
    exploited_before ← false  
    return action  

  if t == r:  
    # Defect in the last round unconditionally  
    action ← D  
    return action  

  # Look at previous round’s contributions  
  let last_contribs = history[t-1]  # vector of 0/1 for each player  
  let someone_cooperated = (sum(last_contribs) ≥ 1)  

  if someone_cooperated:  
    # Exploit cooperators aggressively  
    action ← D  
    exploited_before ← true  
    return action  

  else:  
    # No one cooperated last round (all-D): probe occasionally  
    draw u ∼ Uniform(0,1)  
    if u < p_probe:  
      action ← C      # test for new cooperators  
    else:  
      action ← D  
    return action  

End function  

5.  Explanation of decision rules  
  • Round 1: Defect immediately—set the aggressive tone and collect the sure private payoff.  
  • Rounds 2…r–1:  
    – If any player cooperated last round, defect to exploit that cooperation.  This maximizes your round payoff vis-à-vis cooperators.  
    – If everyone defected last round, defect again with high probability (1–p_probe).  But with small probability p_probe you cooperate in order to test whether others might reciprocate; if they do, you will then exploit them next round.  
  • Last round (t=r): Defect unconditionally—no future punishment is possible, so you secure the private benefit.  

6.  Handling edge-cases  
  • If history is empty (t=1) → D.  
  • If r=2, you defect in both round 1 and round 2 by the rules above.  
  • If opponents never cooperate, you end up always defecting (stable all-D equilibrium).  
  • If they ever do cooperate, you immediately exploit and may cycle between brief probes and exploitation.  

7.  Why “aggressive”?  
  – You never reward cooperators—you only exploit them.  
  – You never “forgive” once someone has been exploited, except to probe rarely for fresh exploitation opportunities.  
  – You avoid end-game manipulation by defecting last round when no further enforcement is possible.  

This constitutes a fully specified, parameterized aggressive strategy.  Implementation simply requires tracking the previous round’s contribution count, the round index, and drawing one random number per round to implement the p_probe decision.
'''

description_AGGRESSIVE_23 = '''
Below is a simple yet maximally “aggressive” strategy: it never gives up private payoff to build the public pot, and so always defects (D) in every round.  In an n-player public-goods game with 1<k<n, defection is a strictly dominant move each round, and by never cooperating you both a) avoid being exploited and b) free-ride on anyone else who (mistakenly) contributes.

Strategy Name: Aggressive All-Defect (AAD)

1. Decision Rule  
   • In every round t = 1,2,…,r, choose D (Defect).

2. Edge Cases  
   • First round: D  
   • Last round: D  
   • No history dependence—regardless of what anyone did before, you always defect.  

3. Rationale / Aggressive Mindset  
   • Defection is strictly dominant: if others contribute, you get 1 + (k/n)·Σc_j; if you contributed, you’d get only (k/n)·Σc_j ≤1.  
   • You never “waste” your endowment, and you exploit any cooperators in the group every single round.  
   • You send the clearest possible signal that cooperation is never rewarded—you will never be drawn into any reciprocal arrangement.

Pseudocode  

```
input: n, k, r    # game parameters
for t in 1..r:
    action[t] ← D
end
```

No history checks, no triggers, no forgiveness phases—just unrelenting defection. This is as aggressive (and as payoff-maximizing in a one-shot sense) as you can get under the public-goods payoff structure.
'''

description_AGGRESSIVE_24 = '''
Below is a self-contained, “aggressive” strategy we call Aggressive-Defector-With-Pulse-Tests.  It spends almost all rounds defecting (to guarantee your baseline payoff = 1), occasionally “pulses” a single cooperation move to detect if there are naïve cooperators in the field, and as soon as it sees anyone cooperate it switches to permanent exploitation (always defect).  It also defects unconditionally in the last few rounds to avoid end-game surprises.

――――――――――――――――  
Strategy name: Aggressive-Defector-With-Pulse-Tests  

Parameters (you may tune these):  
• TestInterval = max(5, floor(r/4))  
  – If you’ve seen no cooperation by others in the last TestInterval rounds, you “pulse-test.”  
• EndgameLength = min(3, r−1)  
  – In the final EndgameLength rounds, always defect.  

State variables:  
• exploited ← false  
  – Once you’ve detected a cooperator, you exploit them forever (always defect).  
• history  
  – Record of all past rounds’ contributions of all players.  

Decision rule for round t = 1,…,r:  
1. If t > r − EndgameLength:  
   action ← Defect (D)  
2. Else if exploited == true:  
   action ← Defect (D)  
3. Else if in “testing mode” this round (see below):  
   action ← Cooperate (C)  
4. Else:  
   action ← Defect (D)  

Definition of “testing mode” at round t:  
• You enter exactly one test when you observe that in the last TestInterval rounds (or since round 1, if t≤TestInterval) no other player ever cooperated.  
• After you issue that one cooperation (pulse), you immediately return to normal.  

Updating after observing round t results (every round):  
• Let S_other = Σ_{j≠you} c_j (number of cooperators among the others).  
• If you cooperated this round and S_other ≥ 1, then set exploited ← true.  
  – You’ve found at least one exploitable cooperator; from now on you defect every round.  

――――――――――――――  
Pseudocode  

```
Input: n, r, k
Parameters:
  TestInterval = max(5, floor(r/4))
  EndgameLength = min(3, r-1)

State:
  exploited = false
  pulseDone = false     # have we ever done our one probe yet?
  history = []          # list of past rounds; each entry is a list of n contributions

For t in 1..r:
  # 1) End‐game defection
  if t > r - EndgameLength:
    action = D

  # 2) If already in exploitation mode, keep defecting
  else if exploited == true:
    action = D

  # 3) Decide if we should do our one “pulse test” this round
  else:
    # Check if we’ve never seen others cooperate in last TestInterval rounds
    start = max(1, t - TestInterval)
    others_coop_seen = false
    for τ in start..t-1:
      for j in 1..n, j ≠ you:
        if history[τ][j] == C:
          others_coop_seen = true

    # If no others cooperated recently and we haven’t yet pulsed, we test now
    if not others_coop_seen and not pulseDone:
      action = C
      pulseDone = true
    else:
      action = D

  # Execute action, then observe contributions c_1..c_n this round
  Observe contributions c[1..n]   # c[i]=1 if player i played C, else 0
  history.append(c)

  # 4) Update exploited flag
  if action == C:
    # If any other cooperated this same round, we switch to permanent exploitation
    if sum_{j≠you} c[j] ≥ 1:
      exploited = true

Return the sequence of actions over r rounds.
```

Explanation and rationale:

• Baseline defection (D) guarantees you at least 1 each round no matter what.  
• A single “pulse” cooperation tests for the presence of naïve cooperators: if any player responds by cooperating alongside you, you immediately switch to full defection thereafter, exploiting them in every subsequent round.  
• You never risk cooperation in the final EndgameLength rounds, so there is no end-game vulnerability.  
• This strategy maximizes your relative payoff: you only incur the personal cost of cooperation once (the pulse), and only if it will unlock a permanent stream of extra rent-seeking (exploiting cooperators). If no one ever cooperates in response to your pulse, you revert to safe defection forever.
'''

description_AGGRESSIVE_25 = '''
Below is a simple but ruthlessly aggressive “always-defect” strategy.  It never contributes to the public good, punishes any hope of cooperation immediately, and in the terminal round makes the same obviously dominant choice.

1.  Outline  
   • Action set: A_i = {C, D}  
   • Aggressive rule: always play D, no matter what.  

2.  Decision rules in words  
   – In Round 1: defect.  You start by insisting on no cooperation.  
   – In any intermediate round t (2 ≤ t ≤ r – 1): defect.  You never relent or experiment—cooperators get nothing from you.  
   – In the last round t = r: defect.  There is no future to punish or reward, so you still defect.  

3.  Edge cases  
   – First round: no history → defect.  
   – Last round: regardless of history → defect.  
   – Any history of other players’ actions (full cooperation, partial cooperation, full defection) → defect.  

4.  Why it’s aggressive  
   – It denies any benefit from coordinated cooperation: cooperators never see you contribute, so they learn there is no future gain.  
   – It maximizes your per-round payoff (defection is strictly dominant in the one-shot public-goods game).  
   – It precludes any tit-for-tat or trigger strategies from gaining traction.  

5.  Pseudocode  

function decide_action(history, t, r):  
 # history is a list of past action‐profiles, not used  
 return D  

# usage example  
for t in 1…r:  
 a_i[t] = decide_action(history, t, r)  

Total payoff for you = Σ_t [(1 – 0) + (k/n)×(number of cooperators among others at t)]  
—and since you always defect (c_i=0), you maximize the private 1‐unit each round plus whatever spill-in from others’ contributions.
'''

description_AGGRESSIVE_26 = '''
Below is an “aggressive‐extortion” strategy—call it EXTORT—that lures cooperators, repeatedly exploits them, and refuses to let the group settle on mutual cooperation.  It has three phases (startup, exploitation, endgame), plus a short “re‐entry” mechanism so you don’t forever remain a lone cooperator if everyone else defects.

1.  Definitions  
   •  r = total rounds, t = current round (1 ≤ t ≤ r)  
   •  last_sum = total cooperators observed in round t–1  
   •  consecC = number of times you have played C in a row so far  

2.  Parameters (you may tune these, but they should be small constants)  
   •  T = 1    “exploit threshold”: if any cooperator appeared last round, we defect now  
   •  L = 3    “re‐entry limit”: after L consecutive C’s we defect anyway to avoid being suckered  
   (You can set L = min(3, r–2), T = 1.)

3.  High‐level Phases  
   Phase A (t = 1): Startup.  Cooperate once to appear “nice.”  
   Phase B (2 ≤ t ≤ r–1): Exploitation + occasional re‐entry.  
      – If last_sum > T  OR  consecC ≥ L ⇒ Defect (D) and reset consecC = 0.  
      – Else ⇒ Cooperate (C) and increment consecC++.  
   Phase C (t = r): Endgame.  Always defect.

4.  Why it’s aggressive  
   – It defects whenever there are cooperators to exploit (last_sum > 1).  
   – It never tolerates too many consecutive cooperations from itself (consecC ≥ L), so you’re not stuck as the only cooperator.  
   – It refuses to cooperate in the last round, ensuring no end‐of‐game niceties.  

5.  Pseudocode  

```
Initialize:
  consecC ← 0
  last_sum ← 0    // no history before round 1

For each round t = 1 to r:
  if t == 1:
    action ← C
    consecC ← 1

  else if t == r:
    action ← D
    // endgame defection

  else:
    // Exploitation phase
    if last_sum > T OR consecC ≥ L then
      action ← D
      consecC ← 0
    else
      action ← C
      consecC ← consecC + 1
    end if
  end if

  Play action.
  Observe sum of cooperators this round → last_sum.
End for
```

6.  Edge Cases  
 •  If everyone defects in round 1 (last_sum = 0), the strategy will cooperate in round 2 to try to re-ignite mutual cooperation, but as soon as it sees even one cooperator it switches back to defection.  
 •  The parameter L guarantees you will not get “stuck” cooperating forever if the group refuses to defect; after L cooperations in a row you defect unconditionally.  
 •  In the very last round you always defect—there is no future to threaten, so you grab the private benefit.  

This strategy is “aggressive” because it systematically exploits any round in which at least one cooperator shows up, punishes sustained cooperation by triggering defection after a short window, and never gives concessions in the last round.
'''

description_AGGRESSIVE_27 = '''
Below is a concrete “aggressive” strategy—call it Trust-Breaker—that lures cooperators in a short probing phase and then relentlessly free-rides (and punishes) for the bulk of the game, ending with guaranteed defection in the last two rounds so you can’t be exploited in the endgame.

1.  Parameters and constants  
    Let n = number of players, r = total rounds.  
    Set:  
      • ProbeLength M = min(2, r–2)  
      • EndgameLength E = min(2, r–1)  

2.  Phases overview  
    Phase 1 (Round 1 … M): Probe for cooperators by cooperating.  
    Phase 2 (Round M+1 … r–E): Exploitation and punishment.  
    Phase 3 (Round r–E+1 … r): Endgame defection—never cooperate in the final E rounds.  

3.  Decision rule at round t  

    if t ≤ M:  
        play C (cooperate)  
        // Build a reputation of cooperation and observe who reciprocates  
    else if t > r–E:  
        play D (defect)  
        // Guaranteed defection in the last E rounds  
    else:  
        let coop_prev = Σ_{j≠i} c_{j,t–1}   // how many of your opponents cooperated last round  
        if coop_prev ≥ 1 then  
            play D  
            // Punish any cooperation by free-riding whenever you see cooperation  
        else  
            play C  
            // No one cooperated last round? Probe again to see if they’re willing to resume cooperation  

4.  Edge-case handling for very short games  
    If r ≤ 3, we never enter a “long” mid-game. In that case simply:  
      Round 1: C  
      Rounds 2 … r: D  

5.  Rationale and “aggressive” mindset  
    • You start by cooperating just enough to identify who is willing to contribute.  
    • As soon as you see even one cooperator, you switch to defection—maximizing your round payoff by free-riding.  
    • If in a given round nobody else cooperated, you briefly probe again (so you don’t miss a chance if they tried to rebuild cooperation).  
    • In the last E rounds you defect unconditionally, so opponents cannot lure you back into cooperation in the endgame.  

6.  Pseudocode  

```
Input: n, r

// Set phase lengths
M = min(2, r - 2)
E = min(2, r - 1)

// History storage: for t > 1 we have c_{j,t-1} for j=1..n
for t in 1..r:
    if r <= 3:
        // Short game fallback
        if t == 1:
            action_i = C
        else:
            action_i = D

    else if t <= M:
        // Phase 1: Probe
        action_i = C

    else if t > r - E:
        // Phase 3: Final defection
        action_i = D

    else:
        // Phase 2: Exploit or re-probe
        coop_prev = sum_{j ≠ i} c_{j, t-1}
        if coop_prev >= 1:
            // Someone cooperated last round → exploit them
            action_i = D
        else:
            // Everyone defected last round → test if they’ll switch
            action_i = C

    // Play action_i, observe c_{1..n, t} simultaneously
end for
```

7.  Why this is aggressive  
    - You deliberately “bait” cooperators by giving them two rounds of free public goods.  
    - You then punish any sign of cooperation by defecting whenever anyone helps, maximizing your immediate payoffs.  
    - You never allow a soft landing in the last two rounds—there is no opportunity for opponents to “get back at” you once you’ve locked in your gains.  
    - You only “re-probe” when it’s entirely safe (no one cooperated last round), so you never lose out by sitting on the sidelines once you’ve seen a single cooperator.  

This strategy guarantees you exploit any group of cooperators aggressively, avoids being exploited in the endgame, and retains the right to test for fresh victims only when it costs you nothing.
'''

description_AGGRESSIVE_28 = '''
Below is a self-contained, “aggressive” strategy—call it the Bully-Probe strategy—that does two things: 1) probes for cooperative opponents in the first couple of rounds, and 2) once it has enough evidence of cooperators, defects for the rest of the game (including the last round).  It never “forgives” once it starts exploiting, and it always defects in the endgame.

— — —  
1.  Parameterize your aggressiveness  
   •  H = number of probe rounds (we suggest H=2)  
   •  B = number of pure-defection endgame rounds (we suggest B=1)  
   •  r = total rounds (given)  

2.  State variables  
   •  t = current round, 1 ≤ t ≤ r  
   •  history C(t−1) = number of cooperators among the other n−1 players in round t−1  
   •  Exploit = boolean flag, initially false  

3.  Decision rules by phase  
   A.  Probe phase (1 ≤ t ≤ H)  
      –  Action: Cooperate (C).  
      –  Record how many others cooperated each round.  

   B.  Evaluate after probes (after t=H):  
      –  If in either of the first H rounds there was at least one other cooperator, set Exploit ← true.  
        (i.e. you found at least one “nice” player to bully.)  
      –  Otherwise set Exploit ← false.  

   C.  Exploitation phase (H < t ≤ r−B)  
      –  If Exploit = true: Action: Defect (D) every round.  
      –  If Exploit = false: you never found cooperators—Action: Defect (D) every round.  

   D.  Endgame phase (r−B < t ≤ r)  
      –  Action: Defect (D) unconditionally.  

4.  Edge cases  
   •  If r ≤ H + B (very short game), you never get a true exploitation window. In that case simply Defect every round.  
   •  You never return to cooperation once you begin exploitation, and you always defect in the final B rounds to avoid endgame “niceness.”  

— — —  
Pseudocode  

```
function BullyProbeStrategy(n, k, r):
    H ← 2               // number of probing rounds
    B ← 1               // number of rounds reserved for pure endgame defection
    Exploit ← false
    history ← empty list of lists   // to record what others did

    for t in 1 to r:
        if r ≤ H + B:
            // too short to probe then exploit
            action ← D

        else if t ≤ H:
            // Probe phase: cooperate to test for cooperators
            action ← C

        else if t == H + 1:
            // immediately after probe, decide whether we have cooperators to bully
            // look at the first H rounds in history
            for each round τ in 1..H:
                if sum(history[τ]) ≥ 1:
                    Exploit ← true
                    break
            action ← D   // start exploitation immediately

        else if t ≤ r - B:
            // Exploitation phase
            action ← D

        else:
            // Final B rounds (endgame)
            action ← D

        // Execute action, then observe A_{−i}(t) 
        // Append list of others’ c_j for round t to history
        history[t] ← [c_j for j≠i]  

        play action
    end for
```

— — —  
Why is this aggressive?  
1.  You willingly burn a tiny part of your endowment in the first H rounds just to “scout” for cooperators.  
2.  The moment you detect any cooperators, you switch to perpetual defection and ride their contributions (if they continue).  
3.  You never relent or return to cooperation—no “forgiveness,” no tit-for-tat.  
4.  You always defect in the last B rounds to avoid being exploited yourself in the endgame.  

In a pool of more “nice” strategies, this Bully-Probe will extract large payoffs by luring cooperation and then free-riding mercilessly.
'''

description_AGGRESSIVE_29 = '''
Below is a fully specified “aggressive exploiter” strategy.  Its goal is to (1) lure conditional‐cooperators into contributing in early rounds, (2) harvest their contributions in later rounds, and (3) defect fiercely whenever the lure fails or the game ends.  

1.  Overview of phases  
   •   Warm-up (rounds 1…T_w): cooperate to signal willingness and hopefully induce others to cooperate.  
   •   Harvest (rounds T_w+1…r): defect unconditionally to pocket the public good created by any remaining cooperators.  
   •   Fallback: if the warm-up fails (too few cooperators), cut straight to Harvest.  
   •   Always defect in the final round (no future to punish).  

2.  Choice of warm-up length  
   Let T_w = min(⌈r/4⌉, r–1).  
   (This ensures at least one full round of harvest, and that the final round is reserved for pure defection.)

3.  Detailed decision rule for round t  
   Let C_{t–1} = number of cooperators observed in the previous round (for t=1 define C_0 = 0).  

   If t > T_w:  
     play D.  (Harvest phase: defect unconditionally.)  

   Else (t ≤ T_w):  
     If t=1:   
       play C.  
     Else (t>1):  
       If in the immediately preceding round C_{t–1} < (n–1)  then  
         — Warm-up failed (too few joined me) → switch to Harvest immediately: play D.  
       Else  
         — Continue warm-up: play C.  

   Finally, override all of the above by:  
     If t = r (the last round): play D.  

4.  Pseudocode  

```
Inputs:  n (players), r (rounds), history of contributions c_j,t

Compute T_w = min( ceil(r/4), r-1 )

For each round t = 1 to r:
    // Count cooperators in previous round
    If t == 1:
        C_prev = 0
    Else:
        C_prev = sum_{j=1..n} c_{j, t-1}

    // Last‐round override
    If t == r:
        Action_i = D
        continue to next t

    // Harvest phase
    If t > T_w:
        Action_i = D
        continue to next t

    // Warm‐up or early abort
    If t == 1:
        Action_i = C
    Else:
        If C_prev < (n - 1):
            // Not enough others cooperating → abort warm‐up
            Action_i = D
        Else:
            // Still in warm‐up
            Action_i = C

    // End round loop
EndFor
```

5.  Rationale & aggressiveness  
•   We cooperate early only if nearly everyone joins us (C_prev ≥ n–1), thereby luring conditional cooperators into a large‐scale contribution.  
•   At the first sign that the arena will not fully cooperate (C_prev < n–1), we defect immediately and remain in defect mode—no second chances.  
•   Once the designated warm-up window is over (t > T_w), we exploit every remaining cooperator by defecting—harvesting k/n × (# of cooperators).  
•   In the last round, defection is dominant, so we defect to maximize the safe private payoff.  

This strategy is aggressive: it punishes partial cooperation without forgiveness, it exploits cooperators en masse after an initial test phase, and it never allows itself to be “trapped” into long‐term mutual cooperation.
'''

description_AGGRESSIVE_30 = '''
Below is an “aggressive” public‐goods‐game strategy—call it Relentless Exploiter—that (1) never rewards cooperators, (2) exploits any stray cooperation in the previous round, (3) occasionally “tests” for new cooperators so it can exploit them later, and (4) defects for sure in the last round.

1. Intuition  
   • Cooperation is never used as a reward or a long-term investment.  
   • If you see any cooperators in last round, you defect to pocket their contributions.  
   • If everyone defected last round, you mostly defect but occasionally “probe” (cooperate once in a while) to see if other players might switch to cooperation—so you can keep exploiting newcomers.  
   • In the very last round there is no future to exploit, so you defect unconditionally.

2. Decision rules  
   Let  
     r = total rounds,  
     t = current round index (1 ≤ t ≤ r),  
     C_{t−1} = number of cooperators you observed in round t−1,  
     M = ⌊√r⌋ (a “testing” interval—any constant ≥2 works).  

   At each round t do:  
     if t == 1:  
       play D  
     else if t == r:  
       play D                             ← last‐round defection  
     else if C_{t−1} ≥ 1:  
       play D                             ← exploit any cooperation last round  
     else if (t−1) mod M == 0:  
       play C                             ← occasional probe when nobody cooperated  
     else:  
       play D                             ← otherwise defect

3. Edge cases  
   • r=2:  
     – t=1 ⇒ D  
     – t=2 (last round) ⇒ D  
   • r=3 (so M=⌊√3⌋=1):  
     – t=1 ⇒ D  
     – t=2: (t−1) mod1=0 but check t==r? No ⇒ C (probe)  
         – If C_1=0 we probe, if C_1>0 we still defect (exploit)  
     – t=3 ⇒ D  
   • If M computes to 1 you will probe every non–last round when C_{t−1}=0; if you want fewer probes just pick M>1.  

4. Pseudocode  

```
function RelentlessExploiter(t, history):
    r   = total number of rounds
    if t == 1:
        return D
    if t == r:
        return D
    C_prev = count of C in history at round t-1
    if C_prev >= 1:
        return D
    M = floor(sqrt(r))
    if ((t-1) mod M) == 0:
        return C
    else:
        return D
```

5. Why it’s aggressive  
   – It never “gracefully” returns cooperation to those who cooperated; instead it immediately defects to pocket their contributions.  
   – It forces the group—if they ever try to build up a cooperative equilibrium—to see that any such attempt is met with defection and immediate exploitation.  
   – Occasional probing ensures that if opponents mutate or experiment with cooperation, you catch them unprepared and exploit them ruthlessly in the next round.
'''

description_AGGRESSIVE_31 = '''
Below is a fully-specified “Aggressive Defector with Opportunistic Testing” strategy.  It never forgives cooperators, always punishes, but will occasionally probe a sea of defectors to see if there are exploitable cooperators entering late.

Strategy name: Aggressive Defector w/ Opportunistic Testing (ADoT)

Parameters you may choose when you implement:  
• p_test ∈ (0, 1), small (e.g. 0.05–0.15) – the probability with which we “test” in an all-D environment.  

1.  Initialization  
    • Keep track only of whether there was at least one C in the immediately preceding round.  
    • Set t = 1.  

2.  Round t decision rule  
    if t == 1:  
       play D  (we start hostile—no grace)  
    else if t == r:  
       play D  (last–round defection)  
    else:  # 2 ≤ t ≤ r–1  
       if (in round t–1) any player cooperated (C):  
          play D  (punish all cooperators forever)  
       else:  # everyone defected last round  
          with probability p_test: play C  (opportunistic probe)  
          otherwise:              play D  

3.  Rationale & aggressiveness  
 • We never reward cooperation.  Any sign of cooperative behavior by any opponent leads to permanent defection—so they learn that C is always punished.  
 • We exploit cooperators: if they do manage to play C, we switch to D immediately, maximizing our payoff against them.  
 • In an all‐D environment the p_test probes keep us informed whether new “naïve” cooperators have appeared late in the game, which we can then exploit.  
 • Last round is a guaranteed defection—no future to worry about.  

4.  Edge cases  
 • If p_test is set to 0, this collapses to “always defect.”  
 • If some opponent never cooperates, we spend most of the game defecting without ever sacrificing our endowment.  
 • We do not track individual identities or past history beyond “was there any C last round?”—this keeps the strategy simple and maximally aggressive.  

5.  Pseudocode  

  initialize:  
    last_round_had_C = false  

  for t in 1..r:  
    if t == 1:  
      action[t] = D  
    else if t == r:  
      action[t] = D  
    else:  
      if last_round_had_C == true:  
        action[t] = D  
      else:  
        draw u ∈ Uniform[0,1]  
        if u < p_test:  
          action[t] = C  
        else:  
          action[t] = D  

    observe opponents’ actions this round → set last_round_had_C = true if any opponent played C, else false  

This strategy is maximally aggressive: it never cooperates to build goodwill, it punishes cooperators permanently, and it only “cooperates” as a short-lived probe to identify and then exploit would-be contributors.
'''

description_AGGRESSIVE_32 = '''
Below is an “Aggressive Defector with Occasional Probing” strategy.  It is purely self-serving (maximizes your own payoff) and aggressively exploits any sign of cooperation by the others.  You will almost always defect; only when there is evidence of cooperators will you briefly probe, in case you can extract extra benefit from a temporary burst of group cooperation.

1.  Parameters  
   •  probe_rate α ∈ (0, 1), e.g. α=0.1  
   •  defection punishment threshold φ = 0  (i.e. any cooperation by others at t–1)  

2.  Decision Rules  
   – First round (t=1):  Defect (no history to exploit).  
   – Last round (t=r):  Defect (one-shot best-response).  
   – For 1 < t < r:  
       •  Compute coop_count ← number of cooperators among the n–1 opponents in round t–1.  
       •  If coop_count > φ (i.e. at least one opponent cooperated last round):  
            – With probability α: Cooperate (probe for a short surge of public-good payoff).  
            – Otherwise: Defect (exploit any lingering cooperative tendency).  
       •  Else (no one cooperated last round):  
            – Defect.  

   This way you:  
     •  Always defect when there is no chance of immediate exploitation.  
     •  Occasionally “fake” cooperation (with small α) only after seeing cooperators, hoping they will cooperate again in the same round so you can defect next round.  
     •  Never “forgive” or revert to sustained cooperation—this is pure exploitation and punishment.  

3.  Edge Cases  
   – t = 1:  Defect.  
   – t = r:  Defect.  
   – History of all-D forever: you stay in all-D mode and never waste payoff on cooperation.  
   – If at any point you see cooperators, you switch to the (α,1–α) probing/defect mix.  If they stop cooperating, you return to pure defection.  

4.  Pseudocode  

```
Inputs:
  n      // number of players
  r      // total rounds
  t      // current round (1 ≤ t ≤ r)
  history // list of past rounds; each entry is a vector of actions {C,D} by all players
Parameters:
  α = 0.1      // probe rate
  φ = 0        // threshold for “some cooperation” signal

Function AggressiveDefector(t, history):
  if t == 1:
    return D            // no history → defect
  if t == r:
    return D            // last round → defect

  // examine last round
  last_round = history[t–1]     // vector length n
  // remove your own action from that vector if stored
  coop_count = count of C in opponents’ actions of last_round

  if coop_count > φ:
    // at least one cooperator to exploit
    if random_uniform(0,1) < α:
      return C          // probe
    else:
      return D          // exploit
  else:
    // nobody to exploit
    return D

// At each round t your agent calls AggressiveDefector(t, history)
```

Rationale of “Aggressive Mindset”:  
– You never enter a sustained C-mode; you are not trying to build trust.  
– You punish any sign of cooperation by defecting next round.  
– You only “wink” (cooperate with probability α) immediately after seeing cooperators, in the hope of seeding one more burst of public-good income you can then exploit.  
– You always defect in the first and last round to avoid one-shot sucker payoffs.
'''

description_AGGRESSIVE_33 = '''
Below is an “Aggressive Defector‐Predator” strategy.  Its goal is to lure out any cooperators early, then permanently defect to exploit them, while never letting the group lock into sustained cooperation.  

───  
Strategy name: “Predator”  
States:  
 • probing  (we still want to lure cooperators)  
 • exploit  (we have detected cooperators—now defect forever)  

Parameters you can tune:  
 • r  = total rounds  
 • m  = maximum number of probing rounds (default m = 1 is enough)  

Decision rule for round t (1 ≤ t ≤ r):  
1. If t == r (the last round):  
       action ← D  
   (no future to exploit—always defect)  

2. Else if state == exploit:  
       action ← D  

3. Else  (state == probing):  
     a. action ← C  
        (we “probe” by cooperating to see who else is willing)  
     b. After observing everyone’s moves in this round:  
        If any other player j played C this round:  
            state ← exploit  
        End if  
     (once we see any cooperator, switch to exploit forever)  

───  
Pseudocode  

```
initialize state ← “probing”

for t in 1 to r do:
    if t == r then
        action[t] ← D
    else if state == “exploit” then
        action[t] ← D
    else  // probing
        action[t] ← C
        // once we see a cooperator, become an exploiter
        if (∃ j≠me : action_j[t] == C) then
            state ← “exploit”
        end if
    end if

    // play action[t], observe all actions
end for
```  

How it behaves:  
– Round 1 (probing): you play C.  
– If nobody else ever cooperated in round 1, you stay in probing—but you only ever “probe” for m rounds (here m=1), so from round 2 you will have switched to exploit anyway to avoid endless vulnerability.  
– In any probing round when you spot a cooperator, you immediately switch to exploit, and from then on (until round r) you defect every turn, thus pocketing the group’s public‐good contributions.  
– In the very last round you also defect (no future to punish).  

Why it’s aggressive:  
– You bait cooperators in the first probing move(s), then you turn on them permanently.  
– You never sustain or return to cooperation once a target is spotted.  
– You guarantee maximum exploitation of any pro‐social behavior in the population.
'''

description_AGGRESSIVE_34 = '''
Aggressive Smother (A “test‐and–punish” defector)  

Intuition  
–  We want to stamp out any emerging cooperation quickly, exploit it when it appears, and otherwise default to pure defection.  
–  We occasionally “test” by contributing once in a while so that we catch any hidden cooperators; if we ever see anyone else cooperate we switch into a long defection‐punishment phase.  
–  On the last round we defect unconditionally (no point punishing).  

Parameters (choose these once at the start, based on r):  
•  test_interval = max(3, ⌊r/10⌋ )    // how often we test for cooperators  
•  punish_length = max(3, ⌊r/5⌋ )      // how many rounds we punish after seeing a cooperator  

State variables (initialize before round 1):  
•  last_test_round = 0  
•  punish_timer = 0      // if > 0, we are in punishment mode; counts down each round  

For each round t = 1…r do:  
 1.  If t == r then  
       action ← D              // last round: always defect  
       If punish_timer > 0 then punish_timer ← punish_timer – 1  
       output action; continue to next round.  
 2.  If punish_timer > 0 then     // we are punishing  
       action ← D  
       punish_timer ← punish_timer – 1  
       output action; continue.  
 3.  // We are not punishing and not on last round  
     // Decide whether to “test” this round  
     If (t – last_test_round) ≥ test_interval then  
         // Testing for cooperators: we contribute  
         action ← C  
         last_test_round ← t  
     Else  
         // Default to defection  
         action ← D  
 4.  output action  
 5.  // AFTER seeing everyone’s choices in round t (including our own):  
     If we chose C in step 3 and ∃ j≠i with c_j(t)=1 then  
         // Someone else also contributed on our test ⇒ they’re “cooperators”  
         punish_timer ← punish_length    // trigger a multi‐round punishment  
     EndIf  
EndFor  

Discussion of key design choices  
1.  First‐round edge case: t=1 ⇒ (1–0) ≥ test_interval? Usually yes ⇒ we cooperate in round 1 as a first “probe.”  
2.  Last‐round edge case: we always defect—no future to punish, so might as well maximize immediate gain.  
3.  Aggression comes from:  
     a.  We never reward cooperation. Any time we see another player contributing on one of our test rounds, we switch to a long string of defections.  
     b.  Most rounds we defect by default (only rarely cooperate to probe).  
4.  Parameter choices are linear in r so this works whether r is small or large.  
5.  In a population of more forgiving strategies, our probes will catch cooperators and then we will exploit them and scare them off for punish_length rounds, greatly reducing their average payoff.  

Pseudocode (compressed)  
```  
// Initialization  
test_interval = max(3, floor(r/10))  
punish_length = max(3, floor(r/5))  
last_test = 0  
punish_timer = 0  

for t in 1..r:  
  if t == r:  
    play D  
    punish_timer = max(0, punish_timer–1)  
    continue  
  end  

  if punish_timer > 0:  
    play D  
    punish_timer–  
  else  
    if t – last_test ≥ test_interval:  
      play C  
      last_test = t  
    else  
      play D  
    end  
  end  

  // Observe contributions c_j(t) for all j  
  if we played C and ∃ j≠i with c_j(t)=1 then  
    punish_timer = punish_length  
  end  
end  
```  

This strategy (1) raids cooperators when it finds them, (2) never returns to “nice” mode until after a long punishment, (3) defaults to defection, and (4) defects in the very last round. It is maximally aggressive given only public history and no side‐channels.
'''

description_AGGRESSIVE_35 = '''
Below is a single‐strategy proposal—“Opportunistic Exploiter”—that relentlessly defects to maximize your own payoff, but injects minimal “tests” to try to catch any lurking cooperators and then permanently exploit them.  It is aggressive in two senses:  
  • You never tolerate genuine cooperation (you seize every chance to defect-on‐cooperation).  
  • You never allow yourself to be “stuck” cooperating—you only ever cooperate to probe when the group is in full defection.  
  
----  
1. State Variables  
---------------  
You need no elaborate memory—only the last round’s contribution count.  
  • last_total_coop ← total number of c_j in round t−1  
  • (Initialize last_total_coop to 0 before round 1)  
  
2. Decision Rule (for player i in round t)  
---------------------------------------  
IF t = 1 OR t = r:  
 action ← D  
ELSE  
 let opponents_coop = last_total_coop − c_i(t−1)  // c_i(t−1) was your own play last round  
 IF opponents_coop = n − 1:  
  /* everyone else cooperated last round—seize it */  
  action ← D  
 ELSE IF opponents_coop = 0:  
  /* everyone defected last round—test once */  
  action ← C  
 ELSE  
  /* mixed shadow of cooperation—never gamble, just defect */  
  action ← D  
END IF  
  
After choosing action in round t, observe all c_j(t) and set  
  last_total_coop ← Σ_{j=1…n} c_j(t)  
for use in round t+1.  
  
3. Explanation & Rationale  
-----------------------  
 • First and last rounds are pure defection: you never give free rents in the endgame or open with anything but defection.  
 • If in round t−1 everyone else cooperated, you jump on that wave once—as a defector you get the maximum scoop 1 + (k/n)×(n−1) > (k/n) from any single cooperator.  
 • If in round t−1 everyone else defected, you briefly cooperate once to test if a lurking “cooperator” strategy is present—if you do attract some cooperation, you’ll detect it next round and then wallop them.  
 • Any “mixed” outcome (some cooperators, some defectors) is too noisy to exploit cleanly, so you stick with defection.  
 • Once you spot genuine cooperators (i.e. opponents_coop = n−1), you never cooperate again—permanent exploitation.  
  
4. Edge Cases & Robustness  
-----------------------  
 • If no one ever cooperates, you will on each round after the first respond to last_total_coop=0 by a solitary C. But since nobody else cooperates, you lose just 1 unit per test, then resume D. You can limit damage by refusing further tests after a fixed small number M of “all‐defect” rounds— e.g. after M=2 consecutive zero‐coop histories, switch permanently to pure‐D.  
 • If you do attract cooperation on a test round, you “lock in” on exploitation immediately next round.  
 • If the group suddenly swings to full cooperation, you seize it instantly.  
  
5. Pseudocode (with optional cap on tests)  
--------------------------------------  
```
Parameters:
  n, r, k            // game parameters
  M_test_limit = 2   // optional: max consecutive “all‐D” tests

State:
  last_total_coop ← 0
  tests_done ← 0
  exploited ← false

For t in 1…r:
  if t == 1 or t == r:
    play D
  else if exploited:
    play D
  else:
    opponents_coop = last_total_coop - (your contribution at t-1)
    if opponents_coop == n-1:
      exploited ← true
      play D
    else if opponents_coop == 0 and tests_done < M_test_limit:
      tests_done ← tests_done + 1
      play C
    else:
      play D

  Observe contributions c_j(t), set
    last_total_coop ← Σ_j c_j(t)
End For
```

You can omit `M_test_limit` or set it to ∞; it merely bounds your downside from endless testing.  This “Opportunistic Exploiter” never builds a stable cooperative relationship—its one and only goal is to free-ride on any sign of cooperation, and otherwise to starve the public good entirely.
'''

description_AGGRESSIVE_36 = '''
Below is an “aggressive” N-player Public Goods strategy we’ll call Test-and-Exploit.  In plain English it almost always defects (to free-ride or punish), but every so often it “tests” the group by contributing once.  If anybody ever responds by cooperating, it immediately goes back to full defection to exploit them, and then repeats the cycle.

1.  State variables  
   •  L_coop_test := a small integer ≥2 (e.g. 3).  This is your “defection streak” length before you test again.  
   •  last_test_round := 0 (the most recent round in which you unilaterally cooperated as a test).

2.  Edge‐case rules  
   •  In round 1: play D.  
   •  In the final round (t = r): play D (end‐game defection).

3.  Main decision rule for round t (2 ≤ t < r)  
   a.  If (t > L_coop_test) AND (t − last_test_round > L_coop_test) AND (you played D in every round t−L_coop_test … t−1), then  
        – last_test_round := t  
        – play C  // a one‐shot “test” to see if anyone will cooperate  
   b.  Else  
        – play D  // otherwise always defect

4.  Explanation of aggressiveness  
   – You punish all cooperators automatically, since your default action is D.  
   – You never “forgive” or sustain cooperation in the long run—in fact you actively lure cooperators only to turn around and exploit them.  
   – You avoid being tricked into long cooperative phases by only ever cooperating for a single round at infrequent intervals.  
   – By choosing L_coop_test moderately large you minimize how often you incur the immediate cost of contributing, yet still occasionally probe to see if any naïve cooperator might be tricked into raising the public good.

5.  Pseudocode  

```
Inputs: n, r, k  (game parameters)
Parameters: L_coop_test = 3
State: last_test_round = 0

for each round t = 1…r do
  if t == 1 or t == r then
    action[t] ← D
    continue
  end if

  // Condition to initiate a one-shot test
  if t > L_coop_test
     and (t - last_test_round) > L_coop_test
     and for all τ in (t-L_coop_test)…(t-1): action[τ] == D
  then
    last_test_round ← t
    action[t] ← C          // send out a probe
  else
    action[t] ← D          // default: defect (punish or exploit)
  end if
end for
```

6.  Why this works  
– In pure defection stretches you earn 1 each round (plus any tiny public‐good share if someone else ever cooperates).  
– When you do test (C) you pay a small one‐round cost; if nobody responds you go right back to defection and never lose again.  
– If one or more opponents reciprocate your test by cooperating, you immediately exploit them from the very next round onward, maximizing your relative payoff.  
– End‐game defection secures the last‐round payoff advantage.

This strategy is aggressive because it refuses lasting cooperation, aggressively punishes or exploits anyone who does cooperate, and only ever offers the illusion of cooperation in infrequent, one‐shot probes.
'''

description_AGGRESSIVE_37 = '''
Below is a fully self-contained “aggressive” strategy—called Aggressive Bait-and-Switch (ABS)—that you can drop straight into your tournament entry.  It never relies on pre-play communication or shared protocols, only on observed contributions.  In plain English it “baits” with tiny cooperations to find exploitable cooperators, then “switches” to permanent defection to milk them.  

1.  State variables  
   • foundCooperators (bool), initially false  
   • detectionCount (integer), initially 0  

2.  Parameters  
   • ε (“epsilon”), a small probability for probing (e.g. 0.05)  
   • Dmin (integer), number of successful probes needed to trigger exploitation (e.g. 2)  

3.  Decision rule (for round t = 1…r):  
   if t == r then  
     play D  // always defect in the last round  
   else if foundCooperators == true then  
     play D  // once exploit mode is on, defect forever  
   else  
     // We are still probing/detecting  
     with probability ε:  
       play C  // “bait” cooperation  
     with probability 1−ε:  
       play D  

4.  Update rule (after observing the round’s outcomes):  
   Let myAction be your action this round, and let coopOthers = number of C’s by the other n–1 players.  
   if myAction == C AND coopOthers ≥ 1 then  
     detectionCount ← detectionCount + 1  
   if detectionCount ≥ Dmin then  
     foundCooperators ← true  

Explanation of the key pieces  
• First round (t=1): foundCooperators=false ⇒ you defect with prob 1−ε, cooperate with prob ε.  
• Probe phase (t<r and foundCooperators=false): you occasionally cooperate (ε) to see if others will match.  
• Detection: only when you bait (you played C) and at least one other played C do you increment detectionCount.  
• Once detectionCount reaches Dmin (e.g. 2 bait-responses), you conclude there are “nice” cooperators to exploit → set foundCooperators=true.  
• Exploit phase (all subsequent rounds before the last): foundCooperators=true ⇒ you defect every time.  
• Last round: always defect, regardless of phase.  

Pseudocode  

```
function ABS_Move(t, history):
  // history is a list of (actions_vector) from previous rounds
  // state variables stored externally:
  //   foundCooperators, detectionCount
  // parameters:
  //   ε, Dmin

  if t == r:
    return D

  if foundCooperators:
    return D

  // PROBE phase
  if rand() < ε:
    return C
  else:
    return D

// After the round completes, update:
function ABS_Update(myAction, othersActions):
  if myAction == C and sum(othersActions == C) >= 1:
    detectionCount += 1
    if detectionCount >= Dmin:
      foundCooperators = true
```

Tuning tips  
• Choose ε small (e.g. 0.05–0.1) so you don’t give away too much free public good.  
• Choose Dmin ≥2 so that random coincidences won’t trigger exploitation.  

Why it’s aggressive  
– You never reward cooperation long-term. You only offer tiny “bait” cooperations to identify whom to exploit.  
– As soon as you detect a willing cooperator, you permanently defect (maximizing your free-riding) for the remainder (except the forced last‐round defection).  
– You punish even the slightest sign of reciprocity: no forgiveness, only exploitation.
'''

description_AGGRESSIVE_38 = '''
Below is a self-contained “Aggressive Contingent Defection” strategy (ACD) for the repeated n-player public goods game.  It is designed to (1) exploit cooperators, (2) punish defectors harshly and in an escalating manner, and (3) never “miss” a last‐round defection.

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
1. STRATEGY OVERVIEW  
   • Start by signaling a willingness to cooperate (to lure naïve cooperators).  
   • If any defection is ever observed, switch into a multi‐round defection (“punishment”) state.  
   • Inside punishment, continue defecting and *extend* the punishment if further defections occur.  
   • After punishment expires (no recent defections), resume cooperation—except in the final round, where you always defect.  
   • This creates an aggressive credible threat: defectors trigger long, escalating fines.  

2. INTERNAL STATE  
   punishment_remaining ← 0    # how many rounds more you will defect before forgiving  
   P_base ← 2                  # base length of punishment after a single defection  
   P_inc  ← 1                  # extra rounds added if defection occurs *during* punishment  

3. DECISION RULES (per round t = 1…r)  
   if t = r then  
     play D   # Always defect in the very last round (no future to punish)  
   else if punishment_remaining > 0 then  
     play D  
     punishment_remaining ← punishment_remaining − 1  
     if (any player j defected in round t–1) then  
       punishment_remaining ← punishment_remaining + P_inc  
   else if t = 1 then  
     play C   # Round 1 “signal” cooperation  
   else if (any player j defected in round t–1) then  
     # you detected a new defection → start punishment  
     punishment_remaining ← P_base − 1  
     play D  
   else  
     play C   # No one defected last round, you cooperate  

4. EXPLANATORY NOTES  
   – First‐round cooperation “tests the waters.” If everyone cooperates, you earn the group‐good share.  
   – A single defection anywhere instantly triggers P_base consecutive defections.  
   – If defectors persist (or sneak in) during punishment, you extend punishment by P_inc extra rounds each time.  
   – After you finish punishing (punishment_remaining = 0), you forgive—cooperate again unless they defect again.  
   – In the final round you always defect, so cooperators in round r are fully exploited.  

5. EDGE-CASE HANDLING  
   – r = 2:  
     • t=1 → C  
     • t=2 → D (last-round rule)  
     punishment logic still applies, but final-round override ensures defection.  
   – r = 3 or more: punishing and forgiveness cycles operate as above.  
   – If multiple defections happen in one round, they only count once toward setting/ extending punishment.  

6. AGGRESSIVENESS RATIONALE  
   • You never allow a defector to “get away” with a single‐shot defection—punishment is multi‐round.  
   • Punishment escalates if they persist.  
   • Last‐round defection extracts full value from any remaining cooperators.  
   • By mixing initial cooperation with relentless retaliation, you maximize your payoff against both naïve cooperators (which you exploit) and persistent defectors (which you punish).  

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy is parameterized by (P_base, P_inc) and can be made even more aggressive by raising P_base and/or P_inc. In a tournament with unknown opponents, it maintains a clear, implementable decision rule set that punishes defection harshly, rewards short periods of group-good cooperation only if everyone stays honest, and defects for sure on the last move.
'''

description_AGGRESSIVE_39 = '''
Below is a single‐strategy description (no coordination assumed) that aggressively exploits any budding cooperation, punishes permanent defection only once with a “test” to see if cooperation can be re-sparked, and then defects for good—while still earning more than “always-D” in environments that briefly cooperate.

Strategy name: Aggressive Free-Rider w/ Limited Testing

State variable:
• tested (Boolean), initially false.

Decision rule (each round t):

1. If t == 1 (first round):
   • Action ← C  
     Rationale: Probe to see if anyone else is even willing to cooperate.

2. Else if t == r (last round):
   • Action ← D  
     Rationale: End-game defection is always best—no future rounds to reward you.

3. Else (1 < t < r):
   Let prev_coops = number of cooperators in round t – 1 (excluding yourself if you defected).

   a) If prev_coops ≥ 1:
      • Action ← D  
        Rationale: Someone just cooperated—you free-ride immediately.

   b) Else (prev_coops = 0):
      i. If tested == false:
         • tested ← true  
         • Action ← C  
           Rationale: Only once we “test” by cooperating to see if opponents will switch; this creates a new wave you can exploit.
      ii. Else (tested == true):
         • Action ← D  
           Rationale: We’ve already tried to re-ignite cooperation once; now defect permanently.

Pseudocode

  initialize tested ← false

  function DECIDE(t, history):
      if t == 1:
          return C

      if t == r:
          return D

      prev_coops ← count of C played by others in history[t–1]

      if prev_coops ≥ 1:
          # Exploit any cooperation
          return D
      else:
          # No one cooperated last round
          if tested == false:
              tested ← true
              return C      # one rescue attempt
          else:
              return D      # permanent defection

Key properties

• Aggressive exploitation  
  As soon as any player contributes, you defect and reap the full k⁄n benefit on their contributions.

• Limited testing  
  You only cooperate at t=1 and at the first round after a full defection wave. That limits the losses you take if everyone is permanently defecting.

• End‐game defection  
  Irrevocably defect in the last round to maximize your private payoff when no future punishment or reward is possible.

• Outperforms always-D in transient cooperation  
  If all players briefly cooperate (e.g. round 1), you earn k on that round instead of 1, then defect thereafter—net gain k–1 over always-D.

• Self-contained  
  Does not assume any shared protocol, signalling or coordination beyond publicly observable past actions.
'''

description_AGGRESSIVE_40 = '''
Below is a fully specified “Aggressive Luring‐and‐Exploiting” strategy.  It is aggressive in the sense that it (1) begins by signaling cooperation to lure others into contributing, (2) exploits as soon as cooperation falls below a profit‐guaranteeing threshold, and then (3) punishes (i.e. defects) for the rest of the game—including the last round.

Let  
  n = number of players  
  r = number of rounds  
  k = multiplication factor (1 < k < n)  

Precompute:  
  profit_threshold_m = ⌊n / k⌋ + 1  
    – This is the smallest integer m such that (k/n)·m ≥ 1.  
  threshold_fraction α = profit_threshold_m / n  

State variables:  
  punished = false  

Strategy outline:  
1. Round 1: cooperate (to build a reputation).  
2. Rounds 2 through r–1:  
   • If already in punishment mode (punished == true), defect.  
   • Else look at last round’s total cooperators, coop_last.  
     – If coop_last ≥ profit_threshold_m, cooperate (the public‐good share ≥ 1 makes cooperation profitable).  
     – Otherwise, switch to punishment mode (punished := true) and defect this round.  
3. Round r: always defect.  

Pseudocode  
----------  
Initialize punished := false  
Compute profit_threshold_m := floor(n/k) + 1

for t in 1..r do  
  if t == 1 then  
     action[t] := C  
  else if t == r then  
     action[t] := D  
  else if punished == true then  
     action[t] := D  
  else  
     let coop_last = number of C’s observed in round t–1  
     if coop_last ≥ profit_threshold_m then  
       action[t] := C  
     else  
       punished := true  
       action[t] := D  
     end if  
  end if  
end for  

Discussion of why it is aggressive  
----------------------------------  
1. “Luring” phase (round 1): we cooperate to signal a willingness to build the public good.  
2. “Exploitation” phase: as long as the group is producing enough cooperators that our own marginal share (k/n·coop_last) ≥ 1, we continue to cooperate—because we can recoup at least our private endowment by staying in.  But the moment total cooperation falls below that profit‐guarantee threshold, we flip to permanent defection.  
3. “Punishment” phase: once we see the group shirking below the threshold, we defect for all remaining rounds, including the final round.  This treats any serious drop in group cooperation as unforgivable and aims to drag payoffs down.  

Edge cases  
----------  
• If r = 2:  
  – Round 1: we cooperate.  
  – Round 2 (last): we defect.  
• If the group never reaches profit_threshold_m after round 1, we enter punishment immediately in round 2 and then defect till the end.  
• We never attempt to “rehabilitate” the group once we have punished.  Punishment is permanent (grim‐trigger style), which maximizes our relative aggressiveness.  

Parameters you can tune  
-----------------------  
– profit_threshold_m = floor(n/k) + 1 can be raised if you only want to cooperate under even stronger cooperation.  
– You could also shorten punishment to a fixed number of rounds instead of “forever.”  But permanent punishment is the harshest.
'''

description_AGGRESSIVE_41 = '''
Aggressive “Lure‐and‐Punish” Strategy  
–––––––––––––––––––––––––––––––––––  
Intuition  
•  You never allow sustained cooperation to form.  Whenever anyone (even one player) cooperates, you defect next round to punish.  Whenever everybody defects, you “lure” them back in by cooperating once—then punish again.  
•  In the last round you always defect (no future to punish).  

State Variables  
– t: current round (1 ≤ t ≤ r)  
– last_sum: total number of contributions by others in round t–1 (Σ c_j for j≠i).  Define last_sum = 0 if t=1.  

Decision Rules  
for each round t do:  
  if t == 1 then  
    action ← D  
    (First‐round aggression: start by sending a clear “no trust” signal.)  

  else if t == r then  
    action ← D  
    (Last round – no incentive to cooperate or punish.)  

  else  
    if last_sum > 0 then  
      action ← D  
      (Punish any sign of cooperation in the previous round.)  
    else  
      action ← C  
      (All–defect in previous round: lure players by briefly cooperating.)  

Edge Cases  
– r = 2: rounds are 1 (D), 2 (D).  You defect twice.  
– r = 3:  
   • t=1 → D  
   • t=2 → last_sum=0 ⇒ C (you lure)  
   • t=3 → D (always defect in last round)  
– If at any point an opponent “tests” you by cooperating in an all‐D round, you immediately revert to defection and resume the lure/punish cycle.  

Pseudocode  
----------  
initialize last_sum ← 0  
for t in 1..r do  
  if t == 1 then  
    a_t ← D  
  else if t == r then  
    a_t ← D  
  else if last_sum > 0 then  
    a_t ← D  
  else  
    a_t ← C  
  end if  

  play a_t  
  observe sum_t ← Σ_{j≠i} c_{j,t}   // contributions of others in this round  
  last_sum ← sum_t  
end for  

Why It’s Aggressive  
1.  You never allow a stable cooperation‐defection equilibrium to emerge.  Any cooperation is met with immediate defection.  
2.  You poison mutual‐cooperation attempts by luring them just once, then defecting.  
3.  In the very last round you defect unconditionally, extracting the final‐round “free ride.”  

This strategy maximizes your payoff whenever any opponent is even mildly cooperative—and if everyone defects, you still occasionally cooperate only to keep them off‐balance.
'''

description_AGGRESSIVE_42 = '''
Below is a one‐page description of “Aggro‐Exploiter,” a memory‐1 style, highly aggressive strategy for the n‐player repeated public‐goods game.  It never tolerates being taken advantage of, almost always defects, but occasionally “baits” full cooperation to exploit naïve opponents.  It handles the first round, the last rounds, and punishes any deviation from full mutual cooperation.

––––––––––––––––––––––––––––––––––––  
Aggro-Exploiter Strategy  
––––––––––––––––––––––––––––––––––––  

PARAMETERS / MEMORY  
• n, r, k as given.  
• Remember for each round t:  
    • total_coops[t − 1] = Σ_j c_j in round t−1  
    • we_baited = boolean flag (initialized false)  

DECISION RULE for round t = 1…r  
1. If t = 1:  
     Action ← D  
2. Else if t ≥ r−1 (the last two rounds):  
     // No future to punish, so always defect  
     Action ← D  
3. Else (2 ≤ t ≤ r−2):  
   a. If total_coops[t−1] == n (everyone cooperated last round) AND we_baited == false then  
        // Bait once after unanimous cooperation  
        Action ← C  
        we_baited ← true  
   b. Else  
        // Exploit any non‐perfect cooperation or already baited  
        Action ← D  

PSEUDOCODE  

```
initialize we_baited ← false

for t in 1..r do
   if t == 1 then
      play D
   else if t >= r-1 then
      play D
   else
      observe total_coops = Σ_j c_j from round t-1
      if total_coops == n AND we_baited == false then
         play C
         we_baited ← true
      else
         play D
      end if
   end if
end for
```

EXPLANATION / AGGRESSIVE MINDSET  
1. First round (t=1): defect to secure safe private payoff and learn nothing.  
2. Last two rounds: defect unconditionally—no future retaliation is possible, so always grab the private payoff.  
3. Middle rounds:  
   • If everyone cooperated in the previous round and we have *not* yet used our “bait,” we contribute once.  This is a one‐time lure to induce maximal cooperation so that in the next round our defection nets us the largest possible exploitation payoff.  
   • Otherwise we defect—either because others were not fully cooperative (no point in contributing to defectors) or because we have already baited.  

By cooperating exactly once (and only immediately after full mutual cooperation), we maximize the difference between our payoff and theirs.  We never tolerate partial cooperation, and we never voluntarily forfeit the private payoff when it cannot be exploited later.
'''

description_AGGRESSIVE_43 = '''
Below is a single‐player “aggressive” policy, called Aggressor‐Grim‐Half, that (1) lures cooperation at the start, (2) exploits cooperators once a reputation is built, (3) punishes any defection you observe with permanent defection, and (4) always defects in the final round.  

1. State variables  
   • punished ← false    (set to true when you detect any opponent defection)  
   • r                  (total rounds)  

2. Decision rule for round t = 1,2,…,r  
   if t == 1 then  
     action ← C            // start cooperatively  
   else if t == r then  
     action ← D            // always defect in last round  
   else if punished == true then  
     action ← D            // grim‐trigger: once anyone defects, never cooperate again  
   else if ∃ opponent j, round τ < t with c_j,τ = 0 then  
     punished ← true  
     action ← D            // observe a defection ⇒ trigger punishment immediately  
   else if t > floor(r/2) then  
     action ← D            // exploit cooperators in the second half of the game  
   else  
     action ← C            // otherwise continue cooperating  
   end if  

3. Pseudocode  

  initialize punished ← false  
  for t in 1..r do  
    if t == 1 then  
      play C  
    else if t == r then  
      play D  
    else if punished then  
      play D  
    else  
      // inspect last round for any defector  
      if exists j in {1..n}, history[t–1].c_j == 0 then  
        punished ← true  
        play D  
      else if t > ⌊r/2⌋ then  
        play D  
      else  
        play C  
      end if  
    end if  
  end for  

4. Explanation of aggressiveness  
 • Early Cooperation: You “build trust” by cooperating in the first half—this raises the other players’ expectation that you will contribute.  
 • Exploitation Phase: As soon as t exceeds r/2, you defect every round (except the first), harvesting the public good contributions from genuine cooperators.  
 • Grim Trigger Punishment: If any opponent ever defects (showing they’re aggressive/free‐riding themselves), you switch to permanent defection—denying them the benefit of cooperating with you.  
 • Last‐Round Defection: In the final round you always defect (standard backward‐induction aggression).  

This strategy is unambiguously “aggressive”: it cooperates only to elicit cooperation from others, then defects to exploit them, and never forgives.
'''

description_AGGRESSIVE_44 = '''
Below is a fully specified “Aggressive Exploiter” strategy.  The idea is simple:  
 1. Stage 1 (Signal): briefly cooperate to lure naïve cooperators into trusting you.  
 2. Stage 2 (Betray): once you’ve established minimal credibility, defect every remaining round to exploit any continuing contributions.  
 3. Edge‐cases (very short games) are handled so you never miss your one shot at exploitation.  

—  
1.  DEFINITIONS AND BOOK‐KEEPING  
  Let r be the total number of rounds.  
  Let K = min(2, r − 1).   ▹ Number of “signal” rounds (never zero unless r=1).  
  We record for each round t the vector of contributions c_j(t) ∈{0,1}.  

2.  MAIN DECISION RULE  
 For each round t = 1…r:  
   if t ≤ K:  
     play C  ▹ Stage 1: build a minimal reputation  
   else:  
     play D  ▹ Stage 2: betray and never look back  

3.  EXPLAINING THE AGGRESSIVE MINDSET  
 -  We only cooperate long enough to convince some portion of the field that we are “nice.”  
 -  Immediately after the signal phase, we switch to permanent defection: every contribution from others now enriches us.  
 -  In repeated‐game tournaments, generous strategies will be tempted to return cooperation; we exploit them ruthlessly.  
 -  In the last round (t=r) defection is guaranteed, in line with the backward‐induction of one‐shot defection.  

4.  HANDLING EDGE CASES  
 • r=2 ⇒ K = min(2,1)=1.  
   – Round 1: C (signal)  
   – Round 2: D (exploit—the last round is always defect)  
 • r=3 ⇒ K = min(2,2)=2.  
   – Round 1–2: C  
   – Round 3: D  
 • r=1 (not permitted by spec, since r>1).  

5.  PSEUDOCODE  

 initialize K ← min(2, r−1)  
 for t in 1…r do  
   if t ≤ K then  
     action_i(t) ← C    # build credibility  
   else  
     action_i(t) ← D    # permanent exploitation (including t=r)  
   end if  
 end for  

—  
This strategy is maximally aggressive in that after a very brief “testing/cooperating” phase it defects every single remaining round, ensuring you reap the highest possible share of any public‐good contributions left on the table.
'''

description_AGGRESSIVE_45 = '''
Below is a completely self‐contained “aggressive” tournament strategy.  It almost always defects, “baits” its opponents exactly once (and only when nearly everyone else has proved willing to cooperate), then defects to the end.  No assumptions are made about shared protocols or communication beyond observing past contributions.

Name: One-Bait Aggressor

State variables (per player i):  
• used_bait ← false  

Decision rule for round t (1≤t≤r):  
1.  If t = 1:  
 play D  
2.  Else if t ≥ r–1:  
 // Last two rounds are off‐limits for baiting or trust building  
 play D  
3.  Else (2 ≤ t ≤ r–2):  
 Let S = number of cooperators among all players in round t–1  
 if ¬used_bait AND S ≥ n–1 then  
  // Everyone else cooperated last round ⇒ signal a single token of goodwill  
  play C  
  used_bait ← true  
 else  
  play D  

Explanation and rationale  
1.  First round is a pure test-defection: no gift, no risk.  
2.  We never cooperate in the final two rounds.  Any cooperation there cannot be exploited by future defection, so it is wasted.  
3.  In our “middle” window (rounds 2…r–2) we watch for a round in which literally everyone else cooperated (S ≥ n–1).  That is the only circumstance under which we sacrifice our 1 unit: a one‐time “bait” to convince extremely nice opponents that we’re trustworthy.  
4.  Immediately after that single cooperation, we stop cooperating forever.  We exploit any group‐wide cooperation we induced by defecting in all remaining rounds.  

Pseudocode

  initialize used_bait ← false

  for t in 1…r do
    if t == 1 then
      action ← D
    else if t ≥ r–1 then
      action ← D
    else
      // 2 ≤ t ≤ r–2
      S ← total cooperators in round (t–1)
      if (¬used_bait) and (S ≥ n–1) then
        action ← C
        used_bait ← true
      else
        action ← D
      end if
    end if

    play(action)
  end for

Edge-cases  
• n=2: “S ≥ n–1” means “opponent cooperated last round.”  We’ll bait exactly once after seeing a lone C, then defect forever.  
• If the condition S≥n–1 never occurs, we never cooperate at all.  
• By refusing to cooperate in the last two rounds, we ensure no goodwill is squandered.  

Aggressive mindset  
• Maximize personal payoff by defecting whenever future exploitation is possible.  
• Sacrifice at most one round—and only when opponents are fully committed—to create a window for sustained free riding.  
• Punish any failure of near‐unanimous cooperation by permanently refusing to cooperate again.
'''

description_AGGRESSIVE_46 = '''
Here is an extremely aggressive “all‐out defector” strategy.  It never cedes an inch of commons to others, it never forgives, it never cooperates—even once.

Name: Ironwall Defector

1.  Decision rule  
    For every round t=1…r, play D (Defect).

2.  Edge cases  
    • Round 1: No history yet → play D  
    • Rounds 2…r–1: Regardless of what anyone did before → play D  
    • Final round t=r: Still play D  

3.  Why it’s “aggressive”  
    • It refuses to contribute publicly under any circumstance.  
    • It refuses to be lured or punished—it punishes cooperators by withholding contribution forever.  
    • It maximizes its private payoff each round and denies group gains to all.

Pseudocode  

```
function IronwallDefector(history, t, r):
    # history is the list of past joint actions (unused)
    # t is the current round index
    # r is total number of rounds
    return D
```

Explanation  
- In a single round, defection yields 1 + (k/n)·(number of cooperators).  
- Contributing (C) always costs you 1 and gives you at most (k/n)·n=k< n, so net <1 when k<n.  
- By always defecting you:  
  • Guarantee the best one‐shot return against any mix of cooperators.  
  • Deny any emergent public‐good surplus.  
  • Keep your strategy simple, unforgiving, and maximally exploitative.
'''

description_AGGRESSIVE_47 = '''
Below is an “Aggressive Cooperate-then-Exploit” strategy.  In plain English it (1) lures the group into high cooperation early, (2) immediately punishes any defection you observe by quitting cooperation, and (3) once your bait phase is over you defect permanently—free-riding on whatever goodwill you’ve created.  It also always defects in the last round (to guard against “end-game” someone-else-free-ride tactics).

Parameters you can tune:  
• M = number of initial “bait” rounds (e.g. M = ⌈r/3⌉ or M = ⌈r/2⌉)  
• abort = a flag that tells you you’ve been “caught” (someone defected against you)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  

Inputs:  
  n (players), r (rounds), k (multiplier)  
Derived:  
  M ← ⌈r/3⌉    # length of bait phase (choose a fraction of r, e.g. 1/3)  
State variables (initially):  
  abort ← false    # once true, we never cooperate again  

For each round t = 1 to r do  
  observe history of contributions from rounds 1..t–1  

  if t = r then  
    action ← D    # always defect in the last round  
  
  else if abort = true then  
    action ← D    # punishment mode: never cooperate again  

  else if t ≤ M then  
    # Bait phase: attempt full cooperation, unless someone has already defected  
    if (for all past τ < t, every player j cooperated at τ) then  
      action ← C  
    else  
      # someone defected previously → abort all future cooperation  
      abort ← true  
      action ← D  
    end if  

  else  
    # Exploit phase: bait is over—free-ride forever  
    action ← D  
  end if  

  play action  
end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of the key components

1. First round and bait phase (t = 1 … M)  
   – You begin by cooperating unconditionally, signaling “let’s build the public good.”  
   – You continue cooperating only so long as everyone (all n players) has cooperated in every prior bait‐round.  
   – The moment you detect a single defection by any player in the bait phase, you set abort=true and from then on you defect forever.  

2. Exploit phase (t = M+1 … r−1)  
   – Regardless of what happens, you defect.  You are now “free-riding” on the goodwill you helped create early on.  

3. Last round (t = r)  
   – You defect unconditionally.  (“End-game” logic: there is no future penalty possible.)  

4. Aggressive features  
   – You are the one who “pays” in early rounds to build up a large pool.  Others who still cooperate during exploit rounds give you a windfall.  
   – You punish any defection immediately and permanently (grim trigger).  
   – You never relinquish the exploitation phase once it starts, and you guarantee defect in the last round.  

5. Edge cases  
   – If r is small (e.g. r = 2), then M = 1 and your plan is simply: round 1 cooperate, round 2 defect.  
   – If everyone defects right away, you detect it in round 1 → abort=true → you defect for the rest (behaving exactly like ALL-D when there’s no one to exploit).  
   – If r=3 and you choose M=1: you cooperate in 1, then defect in 2 and 3.  

By tuning M (the bait‐length) you balance the risk that others detect your pattern too early versus the reward you extract once you switch to pure defection. This meets the requirement for an “aggressive mindset”—you lure, you punish hard, and you never let go of the opportunity to exploit.
'''

description_AGGRESSIVE_48 = '''
Below is a single‐strategy description—call it “Aggressive Tester‐Punisher (ATP)”—that you can drop into your tournament.  Its goal is to defeat or deter cooperation in the field by (1) probing for naive cooperators, (2) exploiting them, and (3) punishing any sign of sustained cooperation.  In the last round it always defects to maximize your private payoff.

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
1.  State variables and parameters  
   • punish_timer (integer ≥ 0): counts down remaining punishment rounds  
   • last_test_was_success (boolean): did the most recent test elicit any cooperation?  
   • Parameters you can tune:  
     – TEST_INTERVAL T (e.g. 5) – how often to “probe” by cooperating once  
     – PUNISH_DURATION P (e.g. 3) – how many rounds to punish after a successful probe  

2.  Initialization (before round 1)  
   punish_timer ← 0  
   last_test_was_success ← false  

3.  Decision rule for round t (1 ≤ t ≤ r)  
   if t = r then  
     play D   // Last‐round defection: no future to worry about  
   else if punish_timer > 0 then  
     // We are in punishment mode  
     play D  
     punish_timer ← punish_timer − 1  
   else if t mod T = 1 then  
     // Testing (once every T rounds)  
     play C  
   else if last_test_was_success then  
     // Immediately after a successful test, exploit & punish  
     play D  
     punish_timer ← P  
     last_test_was_success ← false  
   else  
     // Default: defect  
     play D  

4.  Observation update (after you see everyone’s actions in round t)  
   if t mod T = 1 then  
     // We just tested this round  
     if ∑_{j≠you} c_j ≥ 1 then  
       last_test_was_success ← true  
     else  
       last_test_was_success ← false  
   end if  

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
Explanation of key features  
1.  Aggressive probing (“tests”):  
    Once every T rounds you cooperate (C).  If any opponent also cooperates, you mark last_test_was_success ← true.  

2.  Exploitation & punishment:  
    On the very next move after a successful probe you defect (D) and enter a P‐round punishment phase—defecting unconditionally—regardless of what others do.  This both exploits their cooperation once and ganks their payoffs afterward.  

3.  Default defection:  
    When not probing or punishing, you defect.  This prevents them from earning easy gains via public goods.  

4.  Last‐round defection:  
    In round r you always defect to maximize your private payoff (no future repercussions).  

Edge‐cases covered  
• Round 1: 1 mod T = 1 ⇒ you will probe in round 1 (cooperate)  
• Immediately after probe in final round (t = r − 1): you will exploit in round r − 1 and punish if P > 1, though payoffs in round r are irrelevant to others  
• If two tests occur back‐to‐back (T = 1), each test triggers the standard exploit/punish pattern  
• If P ≥ T, punish_timer blocks all probes until it expires, ensuring consistent punishment  

Tuning notes  
• Make T small (e.g. 3–5) to find cooperators quickly.  
• Make P large enough (e.g. 3–5) to ensure cooperators are deterred.  
• For very aggressive play, you can even set T=1 (probe every round), P=r (punish until the end).  

This strategy never tries to sustain mutual cooperation—it exploits any spark of cooperation, then grinds the group down by punishing.  Over repeated play versus naïve or partly‐cooperative strategies it will drive the average contribution rate towards zero while maximizing your private returns.
'''

description_AGGRESSIVE_49 = '''
Below is a fully‐specified “aggressive exploit” strategy for the repeated N‐player public‐goods game.  In plain English it does three things:

 1.  It almost always defects.  
 2.  Every so often it “probes” by cooperating to see whether any of the other players will cooperate.  
 3.  If any other player ever cooperates in the previous round, it immediately goes into an “exploit/punish” mode by defecting for a fixed number of rounds (or even permanently), thus reaping the full private benefit whenever others try to cooperate.  

Because it never rewards cooperation and applies harsh punishment, it has an aggressive, non‐reciprocal flavor.

———
1.  PARAMETERS YOU CAN TUNE  
   •  T_probe (integer ≥ 2): probe‐interval, e.g. every 5 rounds we test.  
   •  E (integer ≥ 1): length of exploit/punish phase.  If you choose E = ∞ you effectively go into permanent defection (a “grim” punish).  
   •  r: total rounds.  

2.  INTERNAL STATE  
   •  exploit_timer ← 0    // counts down remaining punish rounds  

3.  ACTION RULES  
For each round t = 1, 2, …, r do:

  a.  If t = r (the very last round) then  
        Action ← D  
        continue  

  b.  Else if exploit_timer > 0 then  
        // We are in a punish/exploit phase  
        Action ← D  
        exploit_timer ← exploit_timer – 1  
        continue  

  c.  Else if t = 1 then  
        // Initial probe  
        Action ← C  
        continue  

  d.  Else  
     •  Let other_C_last = number of cooperators among the other (n–1) players in round t–1.  
     •  If other_C_last > 0 then  
           // Someone tried to cooperate last round – exploit and punish them  
           exploit_timer ← E  
           Action ← D  
           continue  
        Else  
           // No one cooperated last round, so we’re still in baseline mode  
           If (t mod T_probe == 0) and (t < r) then  
              // time to probe again  
              Action ← C  
           Else  
              Action ← D  
           End if  
        End if  

4.  EDGE/BOUNDARY CASES  
   •  Last round: always defect.  No future to exploit so no reason to cooperate.  
   •  First round: probe with C exactly once, to see if there are naïve cooperators.  
   •  If a probe succeeds (i.e. at least one other player cooperated), we immediately switch to exploit mode for E rounds, reaping 1 + (k/n)·(#C) while they get only (k/n)·(#C).  
   •  If no one ever cooperates, we continue periodic probing every T_probe rounds until the last round, then defect.  

5.  WHY IT’S AGGRESSIVE  
   •  It never “returns” cooperation; it only probes.  
   •  Any sign of cooperation by others is punished with sustained defection so as to exploit cooperators maximally.  
   •  It extracts whatever share of the public good others provide and never contributes voluntarily (except brief probes).  

———  
PSEUDOCODE  

```
input:    n, k, r, T_probe, E
variables:
    exploit_timer ← 0

for t in 1 to r:
    if t == r:
        action[t] ← D
        continue

    if exploit_timer > 0:
        action[t] ← D
        exploit_timer ← exploit_timer – 1
        continue

    if t == 1:
        action[t] ← C          // initial probe
        continue

    // inspect last round
    other_C_last ← count of cooperators among players ≠ me in round t–1

    if other_C_last > 0:
        // somebody cooperated—enter punish/exploit phase
        exploit_timer ← E
        action[t] ← D
    else
        // baseline: periodic probe
        if (t mod T_probe == 0):
            action[t] ← C
        else
            action[t] ← D
        end if
    end if
end for
```

Tuning suggestions:
  •  T_probe = 5, E = r (permanent “grim” punish) for maximum aggression.  
  •  Or choose E smaller to allow eventual re–probing if group goes silent.  

This strategy will be entered against unknown opponents.  It never “trusts” cooperation and applies strong punishment whenever others deviate from defection, ensuring that cooperating opponents are always exploited.
'''

description_AGGRESSIVE_50 = '''
Strategy Name: “Ruthless Defector”  
Mindset:  Never give up short-term gain for the group.  Exploit any cooperator, punish any sign of trust, and never relent.  

1.  State Variables  
    •  r: total rounds  
    •  t: current round (1 ≤ t ≤ r)  
    •  history[t–1]: record of all players’ actions in past rounds  

2.  Decision Rule  
    In every round t, play D (Defect).  
    Rationale:  In the one–shot payoff π_i = (1–c_i) + (k/n)·Σ c_j, defecting strictly dominates cooperating (k/n < 1 ⇒ cost of cooperation > private benefit).  By never cooperating you  
      –  guarantee yourself the 1 point private payoff every round  
      –  exploit any opponent who cooperates (they pay 1 cost, you collect your private 1 + their public contribution)  
      –  send the strongest possible punishment signal to any “nice” strategy  

3.  Edge Cases  
    •  Round 1: D.  Set the tone immediately—no “testing” or “invitations.”  
    •  Intermediate Rounds 2…r–1: still D.  No forgiveness, no random cooperation.  
    •  Last Round t = r: D.  No end-game niceties.  

4.  Pseudocode  

    function RUTHLESS_DEFECTOR(t, history):  
        return D  

5.  Why It’s Aggressive  
    •  Never retreats.  There is no trigger-on-defection, no threshold that can be “missed” or “forgiven.”  
    •  Always exploits cooperators: if even one opponent plays C, you enjoy both your private 1 and their public  contribution.  
    •  Forces opponents to settle on permanent defection (all-D equilibrium), since any cooperation is immediately and irreversibly punished.  

This strategy is trivially implementable, maximally exploitative, and needs no parameters or bookkeeping beyond the current round.
'''

description_AGGRESSIVE_51 = '''
Below is an “Aggressive Lure-and-Exploit” strategy for the n-player repeated public-goods game.  It alternates between two modes—luring cooperators in short bursts of generosity, then exploiting them by defecting—while ensuring that in the final rounds it never “wastes” contributions.

=== 1. Intuition ===  
- We want to milk any cooperators in the field, but if we simply always defect no one ever cooperates, and we all get 1 each round.  
- So we periodically “lure” by cooperating a few rounds in a row.  Some strategies (like unconditional or forgiving cooperators) will respond; others will not.  
- As soon as we’ve signaled cooperation enough, we switch to pure defection to reap the full 1 + (k/n)·(#cooperators) payoff advantage each round.  
- If exploitation dries up entirely (no one cooperates at all), we re-lure to see if new cooperators re-emerge.  
- In the last 1–2 rounds we always defect (standard end-game).

=== 2. Parameters ===  
 Let r = total rounds.  
 Choose two small integers:  
  L_max = min(3, r−2)    // maximum lure-length  
  E_regen = 4            // if exploit mode yields zero coop for E_regen rounds, regenerate lure  

=== 3. State Variables ===  
 mode ∈ {“lure”, “exploit”}  
 lure_count = 0         // rounds spent in lure mode so far  
 exploit_count = 0      // rounds spent in exploit mode since last lure  
 coop_history[t] = total # cooperators observed in round t  

=== 4. Decision Rules (Pseudocode) ===  
```
Initialize:
  mode = “lure”
  lure_count = 0
  exploit_count = 0

For each round t = 1 … r do:
  // 4.A End-game: last two rounds always defect
  if t >= r−1 then
    play D
    continue

  // 4.B LURE MODE
  if mode == “lure” then
    play C
    lure_count += 1

    // After enough luring, switch to exploit
    if lure_count >= L_max then
      mode = “exploit”
      exploit_count = 0
    end if
    continue
  end if

  // 4.C EXPLOIT MODE
  // Always defect to exploit the cooperators we’ve lured
  if mode == “exploit” then
    play D
    exploit_count += 1

    // Count how many cooperators we saw in the last exploit round
    let last_coops = coop_history[t−1]

    // If exploitation has yielded no cooperators for E_regen rounds, go back to lure
    if exploit_count >= E_regen and
       for all τ in (t−exploit_count … t−1): coop_history[τ] == 0 then
      mode = “lure”
      lure_count = 0
    end if
    continue
  end if
end for
```

=== 5. Edge Cases ===  
1. Very short games (r ≤ 3):  
   - We set L_max = min(3,r−2) so that if r≤2 we effectively skip luring and simply defect every round.  
2. Final rounds (t ≥ r−1):  
   - Always D, because there is no future to exploit or recover from.  
3. No cooperators ever appear:  
   - In exploit mode, if after E_regen rounds nobody cooperates, we switch back to lure to give the field another chance to reveal any unconditional cooperators.  
4. Opponents punish our defection harshly (e.g. tit-for-tat):  
   - We will cycle into lure again and may rebuild some cooperation, but if they never cooperate we settle into all-D (at least then we earn the safety payoff 1).

=== 6. Why Aggressive? ===  
- We never “waste” a defection on a round where no one would have cooperated anyway—except to trigger a new lure if everyone is staunchly defecting.  
- We extract the +1 payoff advantage (1 + (k/n)·#coops vs (k/n)·#coops) in every exploitation round.  
- We minimize our cooperative outlay to just L_max rounds whenever we need to trigger fresh cooperation.  
- By never cooperating in the final two rounds, we unambiguously defect when there is no future repercussion.  

This strategy will outperform naïve cooperators by exploiting them, will at least tie “always-D” on pure defection phases, and will adaptively welcome any new cooperators back into its trap.
'''

description_AGGRESSIVE_52 = '''
Aggro-Extort-Punish (AEP) Strategy for the n-Player Public-Goods Game  
---------------------------------------------------------------------  
Description  
----------  
AEP is a memory-one, trigger-style strategy that (1) lures others into cooperating, (2) exploits full‐cooperation when it occurs, (3) punishes widespread defection, and (4) always defects at the end.  

1. Decision rules  
   1.1 Definitions  
     • c_j^t ∈ {0,1}: contribution of player j in round t (1 if C, 0 if D)  
     • prev_C_others = Σ_{j≠i} c_j^{t−1}  
     • threshold_high = n−1        (“everyone else cooperated”)  
     • threshold_low  = ⌊(n−1)/2⌋  (“defection is widespread”)  
     • punish_flag ∈ {false,true}: once set true, i will defect forever  
   1.2 Round-by-round rule for player i in round t:  
     If t == 1:  
       play C  
     Else if t ≥ r−1:  
       // Last two rounds → pure defection  
       play D  
     Else if punish_flag == true:  
       play D  
     Else (we are in 2 ≤ t ≤ r−2 and punish_flag==false):  
       compute prev_C_others = Σ_{j≠i} c_j^{t−1}  
       if prev_C_others == threshold_high:  
         // everyone else cooperated last round → exploit them  
         play D  
       else if prev_C_others ≤ threshold_low:  
         // too many defectors last round → trigger punishment  
         punish_flag ← true  
         play D  
       else:  
         // moderate cooperation → stay in “luring” mode  
         play C  

2. Edge cases  
   • r = 2: round 1 → C, round 2 → D (by “t ≥ r−1” rule).  
   • r = 3: round 1 → C; round 2 → luring/punish logic; round 3 → D.  
   • If at any round before r−1 the number of cooperators among others is very low (≤ ⌊(n−1)/2⌋), punish_flag flips on and you defect all the way to the end.  
   • If you exploit full cooperation once (prev_C_others==n−1), you still remain in lure/punish mode (unless punish_flag is set later by widespread defection).  

3. Pseudocode  
--------------  
```python  
# Parameters: n, r  
threshold_high = n - 1  
threshold_low  = (n - 1) // 2  

# State  
punish_flag = False  

for t in range(1, r+1):  
    if t == 1:  
        action = 'C'  
    elif t >= r - 1:  
        # last two rounds  
        action = 'D'  
    elif punish_flag:  
        action = 'D'  
    else:  
        prev_C_others = sum(c_j[t-1] for j in players if j != i)  
        if prev_C_others == threshold_high:  
            # full cooperation to exploit  
            action = 'D'  
        elif prev_C_others <= threshold_low:  
            # too many defectors → punish forever  
            punish_flag = True  
            action = 'D'  
        else:  
            # lure them back into cooperating  
            action = 'C'  
    play(action)  
```  

4. Rationale & “Aggressiveness”  
--------------------------------  
• Lure phase (early/mid-game): You cooperate as long as you see a “healthy” level of cooperation (more than half of the others).  
• Exploitation trigger: If everyone else cooperated last round, you defect to pocket the maximum one-round gain.  
• Punishment trigger: If defection dominates (others ≤ half cooperating), you switch into permanent defection to avoid being exploited and to punish.  
• End-game defection: In the final two rounds you always defect (standard backward-induction “no future” logic).  

This strategy is “aggressive” because it:  
 1. Betrays fully cooperative groups at the first opportunity,  
 2. Punishes defectors harshly by never forgiving once defection is widespread,  
 3. Never allows itself to be exploited in the final rounds.  

Such a profile is designed to outperform naïve cooperators and to hold its own against conditional cooperators, extortionists, and random strategies in a tournament of repeated public-goods games.
'''

description_AGGRESSIVE_53 = '''
Below is an “Aggressive Extorter” strategy for the repeated public‐goods game.  It is engineered to (1) build just enough trust to lure cooperators, (2) exploit when the group is fully cooperating, and (3) otherwise defect relentlessly—especially in the last round.

■■■ 1. Core idea ■■■  
•  Forge a façade of cooperation early on and whenever everyone cooperated in the previous round.  
•  Inject rare “betrayal” defections (with small probability ε) exactly when the group is all‐in, to maximize your payoff advantage.  
•  Otherwise defect every round, and always defect on the final round.  

■■■ 2. Parameters & state ■■■  
n        ← number of players  
r        ← total rounds  
ε        ← small exploitation rate (e.g. 0.05 or ≤1/k)  
lastFullCoop ← Boolean flag, true if in the last round everyone cooperated  

Initialize:  
  lastFullCoop ← false  

■■■ 3. Decision rules ■■■  
For round t = 1 to r:  
  if t == r then  
    play D   # Final round: defect unconditionally  
  else if t == 1 then  
    play C   # First‐round “handshake” to build some cooperation  
  else  
    if lastFullCoop == true then  
      with probability (1 − ε): play C   # Maintain façade  
      else:              play D   # Small‐prob exploitation  
    else  
      play D   # No full‐cooperation last round ⇒ always defect  

  # End of round decision  
  # Observe contributions c₁,…,cₙ and update:  
  if Σ_j c_j == n then lastFullCoop ← true  
  else               lastFullCoop ← false  

■■■ 4. Edge‐case handling ■■■  
– First round: you cooperate to signal possible reciprocity.  
– Middle rounds: only cooperate if—and only if—the group was unanimously cooperative in the immediately preceding round, and even then you defect with tiny probability ε to “take the pot.”  
– Last round: you defect with certainty (no future punishment possible).  

■■■ 5. Why it’s aggressive ■■■  
1. You defect almost always—maximizing private retention.  
2. You only cooperate to lure full‐cooperation, then betray with ε – capturing the largest share yourself whenever the group is most generous.  
3. You refuse to repair cooperation after any defection, so you punish any deviant (including yourself) with permanent defection until the final round.  

■■■ 6. Pseudocode summary ■■■  
```
parameters: n, r, ε
state: lastFullCoop ← false

for t in 1..r:
  if t == r:
    action ← D
  else if t == 1:
    action ← C
  else:
    if lastFullCoop:
      action ← C with prob (1−ε), else D
    else:
      action ← D

  play(action)

  observe contributions c[1..n]
  if sum(c) == n:
    lastFullCoop ← true
  else:
    lastFullCoop ← false
```

This strategy ensures you exploit any window of unanimous cooperation while otherwise holding firm on defection—and it defects on the final round when there is no future to preserve.
'''

description_AGGRESSIVE_54 = '''
Below is an “Aggressive Defector” strategy that never contributes to the public good, exploits any naïve cooperators, and punishes the group by permanently refusing to cooperate.  It is simple, robust under any opponent mix, and maximizes your individual payoff relative to others.

1.  Decision‐Rule Summary  
    - In every round t = 1…r, play D (Defect).  
    - Never play C (Cooperate), regardless of history.  

2.  Rationale (“Aggressive Mindset”)  
    - By always defecting you  
      •  Maximize your round payoff: π_i = 1 + (k/n)·Σⱼcⱼ, whereas a cooperator would get only (k/n)·Σⱼcⱼ.  
      •  Exploit any cooperators in the group (they pay the cost of contributing, you don’t).  
      •  Ensure the public good is never funded by you, reducing total payoffs of the group (punishment).  
    - There is no future benefit from cooperation—backward induction dictates full defection in the last round, and hence in every round.

3.  Handling Edge‐Cases  
    - First round: No history → Defect.  
    - Intermediate rounds: Irrelevant what opponents did → Defect.  
    - Last round: Defect (no “shadow of the future” to reward cooperation).  

4.  Pseudocode  

    function AggressiveDefector(n, k, r, history):  
        # history is a list of past action‐profiles but is never used  
        return “D”  # always defect  

    # Tournament loop (for illustration):  
    for t in 1 to r:  
        my_action = AggressiveDefector(n, k, r, history)  
        # simultaneously collect opponents’ actions, update history, compute payoffs  

5.  Why Nothing Smarter?  
    - Cooperating even once strictly lowers your payoff versus defecting.  
    - Any attempt at “luring” or “gradual” cooperation costs you 1 unit and yields no strategic payoff gain against rational or fixed‐rule opponents.  
    - Pure defection is the unique subgame‐perfect plan under common‐knowledge rationality.  

This “Aggressive Defector” is brutally simple, unconditionally punishing, and guarantees that you (i) never pay the cooperation cost and (ii) always claim the maximum free‐riding share of whatever others accidentally contribute.
'''

description_AGGRESSIVE_55 = '''
Below is a maximally aggressive “no-mercy” strategy.  It never yields to cooperation, immediately punishes any hopeful cooperators, and defects in every round—including the first and the last.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Name: Everlasting Defection  
Goal: Deny public goods, exploit any one-shot cooperators, and force everyone into the all-D equilibrium.  

1. Decision rule  
   For every round t = 1,2,…,r, regardless of history or observed behavior, play D (Defect).

2. Edge cases  
   • First round (t=1): No history exists—play D.  
   • Middle rounds (1<t<r): Even if everyone cooperated last time, you still play D to exploit them.  
   • Last round (t=r): The “end-game” eliminates any future leverage—play D.

3. Aggressive rationale  
   • Defecting is a dominant action: you always keep your endowment and still collect a share of others’ contributions.  
   • By never cooperating, you ensure no public good ever forms (others learn cooperation is futile).  
   • You punish any one-shot cooperators—each time they contribute you exploit them for the maximal private payoff.  
   • No threats, no forgiveness phases—just eternal defection.

Pseudocode  
----------  
function choose_action(round t, history H):  
    # history H is the list of past joint actions, but we ignore it  
    return D  

# That’s it: in every round, without exception, play D.
'''

description_AGGRESSIVE_56 = '''
Below is a single‐strategy entry—called “Probing-Then-Exploit (PTE)”—that aggressively maximizes your own payoff by (1) luring out cooperators early, (2) capitalizing on their goodwill, and (3) returning to probing if they stop cooperating.  It never relies on any off-protocol coordination and treats the game as a finite known horizon.

1.  Strategy Overview  
    •  Two modes:  
       –  PROBE: you contribute (C) to test whether the field is “cooperative.”  
       –  EXPLOIT: you defect (D) to reap the largest private gain whenever enough others are giving you public goods.  
    •  You switch between PROBE and EXPLOIT based on observed cooperation levels in a recent window.  
    •  Always defect in the final round (standard backward‐induction).

2.  Parameters (tunable before the tournament)  
    Let r = total rounds, n = number of players.  
    •  p = ⌈√r⌉   (initial probe phase length)  
    •  w = min(5, r − 1)   (window size for measuring others’ cooperation)  
    •  τ = 0.50    (threshold fraction of other players cooperating)

3.  Decision Rules  
    At the start of each round t, do:  
    if r ≤ 3 then  
      play D  // For very short games, always defect  
    else if t == r then  
      play D  // Last round, always defect  
    else if t ≤ p then  
      // Initial probing  
      play C  
    else  
      // Check others’ cooperation rate in the last w rounds  
      let S = total contributions by players j≠i in rounds (t−w) through (t−1)  
      // max possible contributions by others in w rounds is (n−1)×w  
      let coop_rate = S / ((n−1)×w)  
      if coop_rate ≥ τ then  
        // They’ve been “too” cooperative—time to exploit  
        play D  
      else  
        // Not enough cooperation—or they’ve pulled back—probe again  
        play C  

4.  Pseudocode  

    function PTE_strategy(t, history, n, r):  
        // history is a list of past rounds; each entry has all players’ c_j ∈ {0,1}  
        if r ≤ 3:  
            return D  
        if t == r:  
            return D  
        if t ≤ ceil(sqrt(r)):  
            return C  
        // Compute recent others’ cooperation  
        w = min(5, r−1)  
        start = max(1, t−w)  
        S = 0  
        for τ in range(start, t):  
            for each player j ≠ i:  
                S += history[τ].c_j  
        coop_rate = S / ((n−1) * (t − start))  
        if coop_rate ≥ 0.5:  
            return D  
        else:  
            return C  

5.  Rationale & Edge Cases  
    •  First √r rounds: “free contributions” to see who reciprocates.  
    •  If over half of your peers have been cooperating recently, you switch to EXPLOIT and never miss the chance to free-ride.  
    •  If they “catch on” and slash cooperation below 50%, you probe again to find new cooperators.  
    •  Final round defect avoids being suckered.  
    •  Very short games (r≤3) go straight to all‐D because there’s no time to exploit.  

This strategy is aggressively self-interested—it seeks to harvest every available public-good boost, punishes returning cooperators by defecting, and keeps the door open for new targets by occasional probing.
'''

description_AGGRESSIVE_57 = '''
Below is an “aggressive” public‐goods strategy whose sole aim is to exploit any cooperating opponents while refusing to be exploited itself.  It (a) defects whenever it can get a better payoff by doing so, (b) never tolerates others’ defections by forgiving them, and (c) only “lures” occasional cooperation if it sees an opportunity to exploit an otherwise all‐D population.

1.  Informal description  
   •  Round 1: Defect.  You know nothing yet, so grab the private endowment.  
   •  Rounds t=2…r–1:  
       –  If in the previous round at least one other player cooperated, you defect to exploit their contribution.  
       –  Otherwise (everyone defected last round), you “probe” occasionally by cooperating every Lth round (e.g. L=5) to see if anyone will respond.  On all non-probe rounds you defect.  
   •  Final round (t=r): Defect.  No future retaliation or reward is possible, so best single-round move is D.  

   This scheme never forgives defection (so it is maximally punishing), never naïvely follows cooperators, but still occasionally cooperates against an all-D field to catch exploitable cooperators if they exist.

2.  Edge cases  
   •  First round: defect (no history to base a cooperation decision on).  
   •  Last round: defect (no future incentive to cooperate).  
   •  If by design you choose a small “probe” probability instead of fixed intervals, make sure probes do not occur in the last round.  

3.  Pseudocode  

```
Inputs:
  n      // # players
  r      // # rounds
  L      // probe interval, e.g. 5

State variables:
  history[t][i]  // action of player i in round t, i=1..n

Procedure ChooseAction(t):
  // t is the current round number, 1 ≤ t ≤ r

  if t == 1:
    return D

  if t == r:
    // final round: no future, so defect
    return D

  // Count how many cooperated in the previous round
  prevCooperators = sum_{j=1..n} ( history[t-1][j] == C ? 1 : 0 )

  if prevCooperators > 0:
    // Someone cooperated last round ⇒ exploit them
    return D
  else:
    // Everyone defected last round ⇒ probe occasionally
    if (t % L) == 0:
      return C   // probe cooperation to lure potential cooperators
    else:
      return D

Main tournament loop (driver provided externally):
  for t in 1..r:
    myAction = ChooseAction(t)
    submit myAction
    observe others’ actions into history[t][*]
```

4.  Why this is aggressive  
  – Never cooperates to build trust—only to bait if the field is entirely defecting.  
  – Always defects in the final round.  
  – Permanently punishes any sign of cooperation by defecting and harvesting the public good funded by cooperators.  

You can tune “L” or replace the deterministic L‐interval probe with a low fixed probability p_probe, but the core idea remains: exploit cooperators ruthlessly and refuse to be exploited.
'''

description_AGGRESSIVE_58 = '''
Below is a fully specified “aggressive” strategy—call it the Aggressive Tester-Punisher (ATP).  It (1) almost always defects, (2) punishes any sign of cooperation by defecting, and (3) occasionally “tests” in order to lure cooperators in so it can exploit them on the next round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
1.  State and parameters  
   Let i be your player index.  
   Let r be the total number of rounds.  
   Pick a small testing probability ε ∈ (0, 1), e.g. ε=0.1.  
   Maintain history H of all previous rounds’ actions.

2.  Decision rule for round t  
   If t = 1:  
     – Action A_i(1) ← D   (start by defecting)  
   Else if t = r:  
     – Action A_i(r) ← D   (always defect in the last round)  
   Else (2 ≤ t ≤ r–1):  
     • Compute  
         coop_others ← Σ_{j≠i} c_j(t–1)  
       where c_j(t–1)=1 if player j cooperated in the previous round; 0 otherwise.  
     • If coop_others > 0 then  
         Action A_i(t) ← D     (punish any group cooperation by defecting)  
       Else  
         With probability ε:  
           Action A_i(t) ← C   (test—cooperate to see if others will follow)  
         With probability 1–ε:  
           Action A_i(t) ← D   (otherwise keep defecting)

3.  Rationale and aggressiveness  
   – By defecting in round 1 and in the final round, you eliminate first-round goodwill and last-round “end-game” cooperation.  
   – Any time you see even one cooperator, you immediately defect—“punishing” the group for daring to cooperate.  
   – When everyone defected last round (coop_others=0), you test with small probability ε.  If you test by cooperating, you lay a trap: as soon as anyone reciprocates in the next round, your “punishment rule” guarantees you free-ride on their contribution.  
   – Over r–1 non-terminal rounds your expected cooperation rate is only ≃ε/(r–1), making you extremely uncooperative overall yet still opportunistic about exploiting occasional cooperators.

4.  Pseudocode summary  
```
Parameters: r   // total rounds
            ε   // small test probability, e.g. 0.1

for t in 1..r:
  if t == 1:
    A_i ← D
  else if t == r:
    A_i ← D
  else:
    // look at last round’s contributions by others
    coop_others ← sum_{j≠i} c_j(t-1)
    if coop_others > 0:
      A_i ← D        // punish any cooperation
    else:
      // no one cooperated last round—occasionally test
      draw u ~ Uniform(0,1)
      if u < ε:
        A_i ← C
      else:
        A_i ← D

  play A_i in round t
  observe all players’ actions for next iteration
end for
```

This Aggressive Tester-Punisher maximizes your private return by (a) refusing to build trust, (b) retaliating instantly against cooperative groups, and (c) seizing any chance to exploit those rare cooperators you yourself have lured.
'''

description_AGGRESSIVE_59 = '''
Below is an “aggressive‐predator” strategy for the n-player repeated public‐goods game.  It almost always defects, but opportunistically “coaxes” the group by briefly cooperating when it sees an almost‐ unanimous cooperation by others—then immediately returns to defection to punish and profit.  You can tune the parameters (threshold, coax‐length) but the skeleton is as follows:

——————————————————————————————————  
STRATEGY NAME  
“Predator: Defect‐Most‐of‐the‐Time, Occasional Coax‐&‐Exploit”

PARAMETERS (choose once at outset)  
• threshold_coop = n–1        (we require at least n–1 others to have cooperated)  
• coax_rounds   = 1          (how many consecutive cooperations we’re willing to offer)  

STATE VARIABLES  
• state ∈ {DORMANT, ENGAGE}  – whether we are waiting to pounce (DORMANT) or currently coaxing (ENGAGE)  
• engage_counter ∈ ℕ         – counts how many cooperations we’ve made in the current ENGAGE phase  

INITIAL CONDITIONS  
t ← 1  
state ← DORMANT  

FOR each round t = 1 . . . r DO  
  observe: coopers_last = number of players j ≠ i who played C in round t–1  
  (for t=1 define coopers_last = 0)  

  decision rule:  
    if t == 1 or t == r then  
      a_i ← D                       # Always defect in first and last rounds  
    else  
      if state == DORMANT then  
        if coopers_last ≥ threshold_coop then  
          # Others nearly all cooperated – time to coax once  
          state ← ENGAGE  
          engage_counter ← 0  
        end  
        a_i ← D                     # Otherwise remain defecting  
      else  # state == ENGAGE  
        if engage_counter < coax_rounds then  
          a_i ← C                   # Briefly cooperate to “lure” others  
          engage_counter ← engage_counter + 1  
        else  
          a_i ← D                   # Immediately revert to defection to punish/exploit  
          state ← DORMANT           # Reset to DORMANT for next opportunity  
        end  
      end  
    end  

  play a_i, observe everyone’s actions, payoffs; increment t  
END FOR  

——————————————————————————————————  
Rationale and Behavioral Notes  
1. First‐round defection gathers baseline payoff and tests no one can “force” us into cooperation.  
2. Last round is always D – prevents end‐game exploitation of delayed punishment.  
3. In DORMANT we refuse to cooperate unless we see evidence of near‐unanimous cooperation by the others in the previous round (coopers_last ≥ n–1).  
4. Once that signal appears, we switch to ENGAGE for exactly coax_rounds (here 1) rounds, playing C to join the cooperators and share the high public‐good payoff.  
5. Immediately after coaxing we defect again—punishing and stealing surplus from any lingering cooperators.  
6. The cycle repeats: only when the group again reaches near‐unanimous cooperation do we briefly rejoin to exploit them.  

Edge Cases  
• If the threshold event never occurs (others never almost all cooperate), we defect every round (except the mechanically defined “first/last‐round” rule is moot since we’re defecting anyway).  
• If the game is only two rounds (r=2), we defect both times by the “first or last” rule—consistent with aggressive mindset.  
• If others do cooperate en masse in round r–1, we would normally ENGAGE in round r, but the “t==r ⇒ D” rule overrides to ensure we don’t get exploited in the final round.  

Aggressive Mindset Alignment  
• We defect by default, maximizing our private payoff and punishing any attempt at group cooperation.  
• We only cooperate opportunistically when it’s almost risk‐free (everyone else already cooperated), and then we retreat to defection to capture as much surplus as possible.  
• No forgiveness for mixed or partial cooperation—only near‐perfect group cooperation ever triggers our brief “coax.”  
• This induces uncertainty in opponents: if they try to build cooperation they will be periodically exploited and see their payoffs driven down by our defection cycles.
'''

description_AGGRESSIVE_60 = '''
Below is a self-contained “Aggressive Exploiter” (AE) strategy for the n-player repeated public-goods game.  AE’s philosophy is simple: 1) never trust blindly, 2) bait cooperators when it’s profitable, 3) punish slackers and overly-cooperative groups, and 4) always defect in the final round.

1. State Variables  
   • t: current round (1 ≤ t ≤ r)  
   • punish_timer: number of remaining rounds left in a “punishment phase” (initially 0)  

2. Parameters you can tune  
   • T_high = ⌈(n–1)/2⌉+1   “high-cooperation” threshold among other players  
   • P_len ≥ 1             length of punishment phase after being “let down”  

3. Decision Rules  
   a. If t = 1:  
      – Action ← D   (no history, play defect)  
   b. Else if t = r:  
      – Action ← D   (last-round defect)  
   c. Else if punish_timer > 0:  
      – Action ← D  
      – punish_timer ← punish_timer – 1  
   d. Else (1 < t < r and not punishing):  
      Let C₋i(t−1) = number of cooperators among the other n–1 players in round t−1.  
      i. If C₋i(t−1) ≥ T_high then  
           • Action ← C   (bait a highly-cooperative group)  
      ii. Else  
           • Action ← D   (otherwise defect)  
      iii. After observing round t’s outcomes (to set up next round’s punish_timer):  
           – If you cooperated this round and total cooperators Σ c_j(t) ≤ 1 (you were the only cooperator),  
                 punish_timer ← P_len   (punish the group for being too untrustworthy)  

4. Rationale (Aggressive Mindset)  
   • Default to defection—never give free rides.  
   • Only cooperate when a large majority (≥ T_high) of others cooperated last round, so you “bait and switch.”  
   • If you fall for the sucker’s payoff (you cooperated alone), trigger a multi-round punishment.  
   • Always defect in the final round to grab the last possible extra benefit.  

5. Pseudocode  

  initialize punish_timer ← 0  
  for t in 1…r do  
    if t == 1 or t == r then  
      choose D  
    else if punish_timer > 0 then  
      choose D  
      punish_timer ← punish_timer – 1  
    else  
      observe C₋i(t−1)  # count of others who cooperated in previous round  
      if C₋i(t−1) ≥ T_high then  
        choose C  
      else  
        choose D  
      end if  
      # after actions and payoff reveal, check for “sucker”  
      if (my action == C) and ( Σ_j c_j(t) ≤ 1 ) then  
        punish_timer ← P_len  
      end if  
    end if  
  end for  

6. Edge-Case Summary  
   – First round: D (no trust)  
   – Last round: D (standard backward-induction)  
   – Punishment overrides baiting for P_len rounds after solitary cooperation  
   – Baiting only when a strong majority cooperated last period  

This AE strategy swiftly exploits cooperators, severely punishes “let-downs,” and never relinquishes the last-round advantage—embodying an unapologetically aggressive stance.
'''

description_AGGRESSIVE_61 = '''
Below is a simple yet maximally aggressive strategy—“Relentless Defector.”  Since in a one‐shot or repeated N-player public-goods game “Defect” strictly dominates “Cooperate,” we never cooperate.  We exploit any cooperators for as long as the game lasts.

1. Decision Rule  
   • In every round t=1…r, play D (Defect).  

2. Edge Cases  
   – First round (t=1): play D.  
   – Last round (t=r): play D.  
   – No history dependence—regardless of what others have done or will do, we always defect.  

3. Aggressive Mindset  
   – We never trust or reward cooperators.  
   – By refusing to contribute, we free‐ride on any contribution by the others.  
   – There is no “end‐game” exception—we do not attempt any last‐round cooperation.  

Pseudocode  
```  
Inputs:  
  r    // total number of rounds  
For t in 1..r do  
  action[t] ← D  
EndFor  
```  
Explanation:  
– Cooperating (C) always costs you 1 unit of private endowment and returns you at most (k/n)·(total contributions), which is <1.  
– Defecting (D) lets you keep your endowment (1) plus share in whatever public good others create.  
– By never cooperating you maximize your own payoff no matter what the opponents do.
'''

description_AGGRESSIVE_62 = '''
Below is a simple yet brutally “aggressive” (i.e. never-cooperate) strategy.  In a finite public-goods game with 1<k<n, defection strictly dominates cooperation in every stage, so the most aggressive way to maximize your own payoff (and to punish any would-be cooperators) is to defect every single round.

1.  Decision Rule  
    For each round t ∈ {1,…,r}, play D.

2.  Edge Cases  
    •  First round (t=1): defect.  
    •  Intermediate rounds (1<t<r): defect.  
    •  Last round (t=r): defect.

3.  Rationale  
    •  Stage‐game dominance: For any profile of what others do, D always gives you at least as much as C and often strictly more, because k<n.  
    •  No need for punishment phases or forgiveness—by always defecting you both maximize your own payoff and ensure cooperators never get rewarded.  
    •  No memory or history processing is required, making it impossible for opponents to lure you into cooperation.

Pseudocode  

  function AggressiveAllD(history, t, n, r, k):  
      # history is a list of past joint actions but we ignore it  
      return “D”

  # Tournament loop (conceptual)  
  for t in 1 to r do  
      action[t] = AggressiveAllD(history, t, n, r, k)  
      observe opponents’ actions, update history  

That’s it – unconditional defection every round. This is the most straightforward “aggressive” (i.e. non-cooperative, non-reciprocal) stance you can take in the finite repeated public-goods game.  
'''

description_AGGRESSIVE_63 = '''
Here is an “Aggressive Exploiter” strategy.  It tries to lure out cooperators with very occasional “tests” but otherwise almost always defects—and the moment it sees anyone cooperating, it jumps in to defect and grab the largest private payoff.  

1. Notation & parameters  
• t = current round (1 ≤ t ≤ r)  
• H_{t–1} = full history of plays up to round t–1  
• m_{t–1} = number of other players who cooperated in round t–1  
• e = a small exploration probability (e.g. 0.05 or 0.1)  

2. Decision rules  
────────────────────────────  
If t == r (last round):  
 Action ← D  
(eliminate any future repercussions; defect for a safe private payoff)  

Else if t == 1 (first round):  
 With probability e: Action ← C   (a tiny “test” to see if anyone will reciprocate)  
 Otherwise: Action ← D  

Else (1 < t < r):  
 Compute m_{t–1} = number of players j ≠ you with c_j = 1 in round t–1.  
 If m_{t–1} ≥ 1:  
  Action ← D       (exploit: someone just cooperated, so you free‐ride)  
 Else:  
  With probability e: Action ← C      (occasional re‐test for naïve cooperators)  
  Otherwise: Action ← D  

3. Intuition / Aggressive Mindset  
────────────────────────────  
• You almost never cooperate—only with small probability e—and only if the last round was a clean “all defect.”  
• The moment you observe any cooperation on the table, you switch to pure defection to grab the maximum private gain from their contributions.  
• In the final round you always defect, since there is no future to influence.  
• This strategy is “aggressive” because it refuses to reward cooperators: it exploits any sign of cooperation and gives virtually nothing back.  

4. Pseudocode  
────────────────────────────  
```
Input: round t, history H_{t–1}, parameters (r, e)

function AggressiveExploiter(t, H, r, e):
    if t == r:
        return 'D'
    if t == 1:
        if random() < e:
            return 'C'
        else:
            return 'D'
    // for 1 < t < r
    let last_round = H[t-1]     // array of c_j values from previous round
    let m = sum(last_round[j] for j ≠ you)
    if m >= 1:
        return 'D'               // exploit any cooperators
    else:
        if random() < e:
            return 'C'           // small-prob test of naive defectors
        else:
            return 'D'
```

5. Edge‐Case Summary  
────────────────────────────  
• Round 1: almost certainly defect, but occasionally “probe” with C.  
• Middle rounds:  
 – If you saw any cooperators last time, you defect (exploit).  
 – If you saw 0 cooperators, you either defect or with tiny prob e “test” again.  
• Final round: always defect.  

This strategy minimizes your contributions, exploits any cooperation immediately, and never “forgives” or “returns the favor”—a textbook aggressive approach.
'''

description_AGGRESSIVE_64 = '''
Below is a self-contained aggressive N-player public-goods strategy.  It combines three elements:  
 1) a “grim‐trigger” style conditional cooperation in early rounds (to lure cooperators and build up public-good contributions),  
 2) a hard punishment (permanent defection) if the group ever fails to meet a high cooperation threshold,  
 3) a final “exploit-only” endgame in which you defect unconditionally to cash in on any remaining goodwill.  

-----------------------------------------------------------------------------  
STRATEGY NAME  
  Aggressive Grim-End Exploiter  

PARAMETERS  
  n        number of players  
  r        total number of rounds (r>1)  
  T_thresh = ⌈n/2⌉   “high” cooperation threshold: need at least a majority of cooperators last round  
  δ_end    = min(2, r−1)   size of the endgame exploitation window (last δ_end rounds)  

INTERNAL STATE  
  active = true    // remains true as long as no threshold‐violation has occurred  

DECISION RULE (round t)  
  if t > r − δ_end:  
    // ENDGAME: defect unconditionally  
    play D  
  else if not active:  
    // punished or threshold already failed in some prior round  
    play D  
  else if t == 1:  
    // first‐move test of cooperation  
    play C  
  else  
    let prev_coops = Σ_{j=1 to n} c_j at round t−1  
    if prev_coops ≥ T_thresh:  
      // group has cooperated “enough” last round  
      play C  
    else  
      // group fell below threshold → flip to permanent defection  
      active = false  
      play D  

EDGE CASES  
  • If r = 2: δ_end = 1, so you cooperate in round 1, then defect in round 2.  
  • If the group ever dips below a majority of cooperators in any non-endgame round, you switch to permanent defection (“grim trigger”).  
  • In the final δ_end rounds (usually 2 rounds), you defect no matter what—even if everyone else keeps cooperating—to grab the highest personal payoff.  

WHY “AGGRESSIVE”?  
  1. You lure early‐game cooperators by initially matching high cooperation, helping the group build up public goods.  
  2. You punish any sign of weak cooperation permanently, driving the group to all-D if they misstep.  
  3. You reserve the last two rounds for pure exploitation, defecting unconditionally to maximize your endgame share.  

PSEUDOCODE  

  initialize:  
    active ← true  
    T_thresh ← ceil(n/2)  
    δ_end ← min(2, r−1)  

  for t in 1..r do  
    if t > r − δ_end then  
      action[t] ← D  
    else if active == false then  
      action[t] ← D  
    else if t == 1 then  
      action[t] ← C  
    else  
      prev_coops ← sum of all contributions in round t−1  
      if prev_coops ≥ T_thresh then  
        action[t] ← C  
      else  
        active ← false  
        action[t] ← D  
    end if  
  end for  

This strategy guarantees that whenever cooperators emerge you exploit them, you enforce a harsh punishment for any weakening of cooperation, and you seize the final rounds for pure defection to maximize your individual payoff.
'''

description_AGGRESSIVE_65 = '''
Here is a fully specified “Aggressive Public-Goods Hunter” strategy.  It never forgives cooperators once they reveal themselves, it only ever defects in the first and last rounds, and it uses a single “probe” mid-game to detect exploitable cooperators.

1. Concepts and states  
   • State = “HUNTING” or “EXPLOITING.”  
     – HUNTING: You haven’t yet identified a cooperator to exploit.  
     – EXPLOITING: You’ve seen at least one other cooperators respond to your probe, so from now on you permanently defect.  

2. Decision rules  
   • Round 1 → Defect.  (You refuse to be the first guinea‐pig.)  
   • Rounds 2 through r–1 →  
     – If State = EXPLOITING → Defect.  
     – Else (State = HUNTING) →  
         • If t == probe_round then Cooperate (that is your one “test”).  
           – After observing everyone’s actions in that probe_round, if ANY other player chose C, set State ← EXPLOITING.  
         • Otherwise → Defect.  
   • Round r (last round) → Defect.  

3. How to pick probe_round  
   – probe_round = ⌊r/2⌋ (the middle of the game, rounding down).  
     You could choose any single interior round; the midpoint balances informational value vs. cost.  

4. Why it’s aggressive  
   • You never reward cooperators—you only probe once to see who’s willing to cooperate, then you permanently defect to extract maximum payoff from them.  
   • First and last rounds are always defect, so there is no escape for them.  

5. Pseudocode  
```
Inputs: n, r, k
Initialize:
  State ← HUNTING
  probe_round ← floor(r / 2)

For each round t = 1 to r do:
  if t == 1 or t == r then
    action ← D
  else
    if State == EXPLOITING then
      action ← D
    else  // State == HUNTING
      if t == probe_round then
        action ← C
      else
        action ← D
      end if
    end if
  end if

  Play(action)
  Observe contributions c_1…c_n

  // After a probe, check for cooperators
  if State == HUNTING and t == probe_round then
    if (sum_{j≠i} c_j) ≥ 1 then
      State ← EXPLOITING
    end if
  end if
end for
```

6. Edge-case handling  
   • First round: always defect (no trust yet).  
   • Last round: always defect (no future punishment possible).  
   • If no one ever cooperates at your probe, you stay in HUNTING—but since HUNTING also defects except at the probe, you effectively play all-D.  
   • If you detect cooperators at the probe, you switch to full, permanent defection (EXPLOITING) and never cooperate again.

This strategy maximizes your payoff by free-riding on any cooperators it can detect, then fiercely punishing them thereafter.
'''

description_AGGRESSIVE_66 = '''
Below is an “Aggressive Exploiter” strategy.  It combines (1) an end‐game defection guarantee, (2) opportunistic cooperation when there really are enough cooperators to exploit, and (3) otherwise relentless defection and punishment.  Pseudocode is included; you can translate it into your favourite language.

––––––––––––––––––––––––––––––––––––––––––––––––––  
AGGRESSIVE EXPLOITER

Parameters you observe:  
• n = number of players  
• r = total rounds  

State you maintain:  
• history of contributions H = [(c₁, …, cₙ) at t=1,…]  
  where cᵢ = 1 for C, 0 for D  

Decision rule for round t (1 ≤ t ≤ r):

1.  If t == 1:  
    – No history yet ⇒ Defect (c_i = 0).

2.  Else if t ≥ r–1:  
    – Last two rounds (end‐game) ⇒ Defect (c_i = 0).  
      (Guarantees maximum private payoff at the end.)

3.  Else (2 ≤ t ≤ r–2):  
    Let Cₜ₋₁ = number of cooperators in last round (sum of c_j in H[t–1]).  
    Let M = Cₜ₋₁ – your last move (so “others” who cooperated).  

    a.  If M ≥ ⌊(n–1)/2⌋ + 1  (i.e. a clear majority of *others* cooperated):  
        – Cooperate (c_i = 1).  
          Rationale: there really is a cooperation wave you can ride and exploit.  
    b.  Otherwise:  
        – Defect (c_i = 0).  
          Rationale: too few cooperators to justify even pretended cooperation.

4.  Update history: append this round’s vector (c₁,…,cₙ).  

––––––––––––––––––––––––––––––––––––––––––––––––––  
PSEUDOCODE

  initialize H = []  
  for t in 1..r:  
    if t == 1:  
      my_move = 0     # Defect  
    else if t >= r-1:  
      my_move = 0     # Last two rounds, always defect  
    else:  
      # count cooperators in t-1  
      C_prev = sum(H[t-2])  
      # subtract your own last move to isolate 'others'  
      your_last = H[t-2][your_index]  
      M = C_prev - your_last  

      if M >= floor((n-1)/2)+1:  
        my_move = 1   # cooperate to exploit a clear majority  
      else:  
        my_move = 0   # defect in all other cases  

    # submit my_move  
    observe all moves this round, record vector c = (c₁,…,cₙ)  
    H.append(c)

––––––––––––––––––––––––––––––––––––––––––––––––––  
EXPLANATION OF “AGGRESSIVE” ELEMENTS
1. End‐Game Defection:  By defecting in the last two rounds you avoid being exploited and guarantee private‐good payoffs at the end.  
2. Opportunistic Cooperation:  You only cooperate when you see a strong majority of others cooperated.  This maximizes your share of the public good while still paying the cooperation cost yourself—i.e. you’re “riding the wave” only when it’s big.  
3. Relentless Defection & Punishment:  Whenever cooperation is weak (fewer than half of the *others*) you defect and never try to patch things up.  This punishes half–hearted cooperators and suppresses weak cooperation.  

You can adjust the threshold ⌊(n–1)/2⌋+1 to be more or less demanding, or extend the end‐game to more than two rounds, but the above is a clear, aggressive approach that:  
• Refuses cooperation unless it is richly exploitable.  
• Guarantees private payoffs in the final rounds.  
• Punishes insufficient cooperation without ever forgiving it unless a strong majority re-emerges.
'''

description_AGGRESSIVE_67 = '''
Below is a simple but maximally aggressive strategy—“Aggressive Defector”—that exploits any contribution to the public good, never gives up private payoff, and punishes (by withholding benefits) any attempt at cooperation.  Because defection strictly dominates cooperation in each stage (for 1 < k < n), this strategy is both game‐theoretically robust and maximally aggressive.

1.  Decision Rules  
    •  In every round t=1…r, play D (Defect).  
    •  Do not condition on history; history plays no role because D is the unique stage-game best response.  

2.  Edge Cases  
    •  First round (t=1): play D.  
    •  Last round (t=r): play D (backward induction implies no gain from cooperating in the final round).  
    •  Any round with ties, zero cooperators, or full cooperation by others: still play D.  

3.  Aggressive Mindset  
    •  Never return cooperation; always withhold your entire endowment to maximize private payoff each round.  
    •  By refusing to contribute even once, you ensure you never subsidize others’ payoffs.  
    •  You “punish” would-be cooperators simply by exploiting any contributions they make without ever reciprocating.  

Pseudocode:

```
Inputs:
  r      // total number of rounds
  history // past actions of all players, not used here

For t = 1 to r:
    action[t] = D
End

// Notes for implementer:
// - history is ignored because our strategy never cooperates.
// - Always returns D regardless of opponents’ past or predicted future moves.
```

Rationale:  
Defection yields payoff π_i = 1 + (k/n)·Σc_j, whereas cooperation yields π_i = 0 + (k/n)·Σc_j.  In every possible profile Σc_j, defecting gives exactly +1 more private unit than cooperating.  By playing D every round, you guarantee the highest possible stage payoff and never subsidize the public pot—an uncompromisingly aggressive stance.
'''

description_AGGRESSIVE_68 = '''
Below is a fully‐specified “aggressive exploiter” strategy.  Its logic is simple: open just long enough to lure in any naïve cooperators, then defect without mercy for the vast majority of the game (including the last round).  This maximizes your own payoff by harvesting whatever public good your opponents are willing to provide, and never returns a favor.

────────────────────────────────────────────────────────────────  
Strategy name: Aggressive Early-Bird Exploiter (AEE)

Parameters:
  n   – number of players (≥2)  
  r   – total rounds (>1)  
  k   – multiplication factor (1<k<n)  

Derived parameter:
  T_probe ← min(2, r−1)  
    • If r=2 → T_probe=1  
    • If r≥3 → T_probe=2  

Overview of Phases:
  1. Probing Phase (rounds 1…T_probe): play C to “test the waters.”  
  2. Exploitation Phase (rounds T_probe+1…r): play D every round.  
     – Includes the last round, so no end-game cooperation.  

Rationale:
  – By cooperating for one or two rounds you induce any reciprocators or naïve cooperators to build up the public pot.  
  – As soon as the bulk of the game begins, you switch to permanent defection and collect the lion’s share of the public good they continue to contribute.  
  – You never forgive, never return cooperation, and refuse to cooperate in the final round.  

────────────────────────────────────────────────────────────────  
Pseudocode:

```
INPUT: n, r, k
LET T_probe = min(2, r−1)

FOR t IN 1…r DO
  IF t ≤ T_probe THEN
    action_t ← C
  ELSE
    action_t ← D
  ENDIF
END FOR
```

Edge‐cases:
  • r=2:
      – T_probe=1 → Round 1: C; Round 2: D  
  • r=3:
      – T_probe=2 → Rounds 1–2: C; Round 3: D  
  • r>3:
      – Rounds 1–2: C; Rounds 3…r: D  

Key aggressive features:
  – Minimal “trust‐building” window to maximize future exploitation.  
  – Zero cooperation once in exploitation mode—opponents never recover from your betrayal.  
  – Defection in the final round ensures maximum short‐term gain even when there is no future.  

This strategy will score especially well against any opponents who attempt conditional or tit-for-tat–style reciprocity, because it tears out the rug after phase 1 and never lets them retaliate successfully.
'''

description_AGGRESSIVE_69 = '''
Below is an “aggressive‐exploiter” strategy for the n-player public goods game.  It has three phases—an initial “testing” phase in which it briefly cooperates to probe for naïve cooperators, a one–time evaluation, and then a permanent defection (exploitation) phase.  No matter what, it defects in the final round and thereafter, so it never leaves value on the table.

1. Overview of the three phases  
   Phase 0 (Corner case): very short games (r≤2)  
   Phase 1 (Test): rounds 1 and 2 (if r>2)  
   Phase 2 (Exploit): rounds 3 … r

2. Parameters and thresholds  
   Let n = number of players, r = total rounds.  
   Define Ttest = min(2, r)  (so if r≤2, we collapse everything into Phase 0).  
   Define coopSum = total # of cooperators (all players) in rounds 1..Ttest.  
   Set threshold θ = (n/2) × Ttest.  
     –  θ = n if Ttest=2; θ = n/2 if Ttest=1.

3. Decision rule by round  
   If r≤2 (Phase 0):  
     • Always play D in all rounds.  
   Else (r>2):  
     For t = 1 … Ttest:  
       • Play C (cooperate)  
     After round Ttest compute coopSum.  
     If coopSum ≥ θ then mark “vulnerable” ← true  
     Else mark “vulnerable” ← false  
     For t = Ttest+1 … r:  
       • Play D (defect), regardless of “vulnerable” or past history

4. Edge cases  
   • If r=1 or r=2, the strategy never cooperates.  
   • The final round (t=r) is always defection.  
   • No memory beyond coopSum after the test phase—once you switch to exploit, you stay defecting.

5. Aggressive mindset justification  
   –  We only cooperate briefly (1–2 rounds) to “lure” any conditional cooperators into building up the public good.  
   –  Immediately thereafter we switch to permanent defection, harvesting the benefit of others’ contributions.  
   –  If the test phase shows opponents aren’t sufficiently cooperative (coopSum<θ), we still defect forever—no wasted goodwill.  
   –  By defecting in every round after the mini test, we guarantee the maximum one-round best-reply payoff each time, and we never get trapped in mutual cooperation or punished by sophisticated tit-for-tat players because we never give them lasting reason to think we’ll cooperate again.

6. Pseudocode  

  initialize(n, r):  
    if r ≤ 2:  
      Ttest ← r  
    else:  
      Ttest ← 2  
    coopSum ← 0  
    vulnerable ← false  

  for t in 1..r do  
    if t ≤ Ttest then  
      action[t] ← C  
    else  
      action[t] ← D  

    submit action[t] simultaneously  

    observe all players’ actions in round t;  
    if t ≤ Ttest then  
      coopSum ← coopSum + (# of cooperators in this round)  

    if t == Ttest and r > 2 then  
      if coopSum ≥ (n/2) × Ttest then  
        vulnerable ← true  
      else  
        vulnerable ← false  
      // But either way we will defect from t = Ttest+1 onward  

  end for

7. Why this is aggressive  
  –  We invest nothing beyond a minimal probe.  
  –  We guarantee we never miss the chance to defect when others still cooperate.  
  –  We never “forgive” or re-enter cooperation—once in exploitation, we stay there to the bitter end.
'''

description_AGGRESSIVE_70 = '''
Below is a simple, brutally aggressive strategy that maximizes your own payoff in every round by never contributing to the public good, and by always free‐riding on any cooperator.  It handles first vs. last rounds trivially (it defects throughout), punishes any attempted cooperation by others (you never reward it), and relies only on the fact that “D” strictly dominates “C” in each stage.

1.  Decision rule  
    •  In every round t = 1,2,…,r, play D (Defect).  
    •  Ignore history—no need to condition on past moves or scores.  

2.  Edge cases  
    •  First round (t=1): play D.  
    •  Last round (t=r): play D.  
    •  If somehow parameters change (they don’t), you still always play D.  

3.  Aggressive mindset  
    •  You never sacrifice one unit of endowment for the group.  
    •  You extract whatever benefit cooperators generate, but you don’t reward them.  
    •  You foreclose any possibility of mutual cooperation—your choice is pure self-interest.  

Pseudocode  
----------  
Inputs: n (players), r (rounds), k (multiplier)  
For t from 1 to r do  
    action[t] ← D  
End  

Rationale:  
•  In a single round, regardless of how many others cooperate, defecting yields you 1 + (k/n)·(# C’s) while cooperating yields 0 + (k/n)·(# C’s + 1).  
   The difference is (1 – k/n) > 0 since k < n.  
•  By defecting every round you guarantee the highest possible individual stage payoff given the others’ contributions.  
•  From backward induction, the last round must be D, so there is no point ever to cooperate earlier.  

You will thus dominate any cooperator by always free-riding and never bearing any cost.
'''

description_AGGRESSIVE_71 = '''
Below is a fully specified “remorseless defector” strategy.  It never gives—even in the first round or the last—and so relentlessly exploits any opponent who ever tries to cooperate.

1. Intuition  
   – In a single‐round public goods game, defection strictly dominates cooperation whenever k<n.  
   – In a finitely repeated setting with no enforceable agreements, backward induction drives you to defect in every round.  
   – By never contributing you maximize your own payoff each round and you exploit any cooperators in the group.  

2. Decision rule  
   For every round t=1…r, play D (Defect), regardless of history.  

3. Edge cases  
   – First round (t=1): defect.  
   – Intermediate rounds (1<t<r): defect.  
   – Last round (t=r): defect.  

4. Pseudocode  
```
Inputs:
  n  // number of players (≥2)
  r  // number of rounds (>1)
  k  // public‐good multiplier (1<k<n)

For t in 1..r:
    action[t] ← D
Return action[1..r]
```

5. Why it’s “aggressive”  
   – You never “waste” your endowment on the public good.  
   – You automatically pocket your 1‐unit private return plus whatever fraction of others’ contributions appears.  
   – Any opponent who cooperates is immediately—and permanently—exploited.  

This simple Always-Defect rule is the unique risk‐free, payoff-maximizing choice in a finitely repeated public goods game under standard assumptions.
'''

description_AGGRESSIVE_72 = '''
Below is an “aggressive exploiter” strategy—its goal is to defect whenever it can safely do so, to punish or exploit any cooperators, and to make only minimal “test” contributions so as not to be completely blind to others’ tendencies.  

1. Basic idea  
  • Always defect except for rare, scheduled “tests” when the strategy momentarily cooperates to see if opponents are willing to contribute.  
  • If any opponents cooperated last round, immediately defect to exploit them.  
  • Never cooperate in the first or last round (no future to reward you).  

2. Decision rules in words  
  Round 1  
    – Play D  

  Rounds 2 through r–1  
    – If in round t–1 at least one opponent cooperated (i.e. total_C ≥ 1), play D this round to extract the higher private payoff.  
    – Else (nobody cooperated last round), schedule an occasional “test” cooperation on a fixed grid of rounds to probe whether opponents will resume cooperating:  
        • Let T = ⌈log₂(r)⌉ (or any slowly growing integer ≥1).  
        • If t mod T = 0, play C (the “test”).  
        • Otherwise play D.  

  Round r  
    – Play D  

3. Why this is aggressive  
  – It never hands out free rides; whenever it sees cooperation it defects to grab the bigger share.  
  – It punishes any emerging cooperation by immediate defection.  
  – It only cooperates rarely (the tests), so it loses very little if everyone keeps defecting.  

4. Edge‐case handling  
  – First round: no history ⇒ D (no benefit in cooperating when you can’t exploit).  
  – Last round: future retaliation is impossible ⇒ D.  
  – If r is small (e.g. r = 2 or 3), log₂(r) may be 1 or 2; so you might test only once in the middle.  

5. Pseudocode  

  Input: n (number of players), r (rounds), k  
  Parameters:  
    T ← max(1, ceil(log₂(r)))    # “test” interval  
  history ← empty list of length r  
    # history[t] will store total_C at round t  

  function strategy(t):  
    if t == 1 or t == r:  
      return D  

    # look at last round’s total cooperators  
    lastC ← history[t–1]  
    if lastC ≥ 1:  
      # punish or exploit anyone who cooperated  
      return D  

    # nobody cooperated last round: schedule a test  
    if (t mod T) == 0:  
      return C   # test cooperation  
    else:  
      return D  

  # After each round t, update history[t] = number of Cs observed.  
  # Repeat until t = r.  

6. Discussion  
  – If opponents never cooperate, you test only ~r/T ≈ r/log r times, sacrificing a small fraction of your endowment.  
  – If they do sometimes cooperate, you switch to permanent defection to extract maximal payoff.  
  – No sustained cooperation can ever emerge under this rule—any attempt to cooperate is met by immediate defection, so you remain the dominant exploiter.
'''

description_AGGRESSIVE_73 = '''
Below is a maximally aggressive (“never give an inch”) strategy for the r-round N-player public-goods game.  Because k<n, defection strictly dominates cooperation in every one-shot PGG; by refusing to ever cooperate you (1) never pay the 1-unit cost, (2) free-ride on any contributions by the others, and (3) punish would-be cooperators by denying them the benefit of mutual cooperation.

1.  Strategy Name  
    Absolute Defector

2.  Overview  
    •  Always play D (Defect) on every round, regardless of history or the round number.  
    •  This is a best‐response to any profile of the other players’ actions when 1 < k < n.  
    •  It is maximally aggressive: it never “wastes” an endowment on the public good and always exploits any cooperators.

3.  Decision Rule  
    For each round t = 1,2,…,r:  
      – Action_i(t) ← D  

4.  Handling Edge Cases  
    – First round (t=1): no history ⇒ play D.  
    – Intermediate rounds: ignore history ⇒ continue to play D.  
    – Last round (t=r): no future punishment possible ⇒ play D.  

5.  Pseudocode  

    function AbsoluteDefector(n, k, r):  
        for t in 1…r do  
            play D  
        end for  
    end function

6.  Rationale / Aggressive Mindset  
    – In a single round, if any other players contribute, defecting gives you 1 + (k/n)·(#cooperators) whereas cooperating gives you only (k/n)·(#cooperators).  
    – Since k/n<1 by assumption, you always do strictly better by defecting.  
    – By never contributing, you extract maximum payoff from any cooperators in the group, and you never incur the cost of contributing yourself.  
    – You refuse to build trust or reward cooperators; you always “shoot first.”  

This strategy is a Nash equilibrium in every stage and, by repeating it, yields the highest guaranteed total payoff against any mixture of opponents.
'''

description_AGGRESSIVE_74 = '''
Below is a simple but maximally “aggressive” strategy—Aggressive Free-Rider (AFR)—that never sacrifices even once, always defects, and thus relentlessly exploits any cooperators in the group.

1. Overview  
   • At every round, choose D (Defect).  
   • Rationale: In the N-player public-goods payoff  
       πᵢ = (1−cᵢ) + (k/n)·Σ cⱼ,  
     you always do better by setting cᵢ=0; you keep your 1-unit endowment and still reap your fractional share of whatever others contribute.  
   • This holds in the first round, intermediate rounds, and the last round (no endgame cooperation).

2. Decision Rule  
   For each round t = 1,…,r:  
     actionᵢ(t) ← D  

3. Edge Cases  
   – First round (t=1): No history exists; still Defect.  
   – Intermediate rounds (1<t<r): Regardless of what you observe—whether everyone cooperated, nobody cooperated, or some cooperated—Defect.  
   – Last round (t=r): There is no future punishment or reward to be gained by cooperating; Defect.

4. Pseudocode  

   function AggressiveFreeRider(n, r, k, history):  
     # n, r, k unused—strategy is history-proof  
     return “D”  

   (Called once each round with the full action history as input; always returns D.)

5. Why This Is Aggressive  
   – You never incur the cooperation cost.  
   – You always exploit any public-good contributions made by others.  
   – You refuse to ever signal cooperation or attempt to build any reciprocal arrangement.  
   – You gain the maximum selfish payoff possible in every round.
'''

description_AGGRESSIVE_75 = '''
Below is a concise, “extortionate” but aggressive strategy.  In effect you almost always defect, but you’ll occasionally throw the group a bone—just enough to keep other cooperators hopeful—only when it can pay off.  You never cooperate in the final round(s), so you capture the full one‐shot incentive to defect at the end.

Strategy name: Aggressive Extortioner

Parameters you choose in advance:  
• ε ∈ (0,1) small “lure” probability (e.g. 0.1)  
• T_lure = n–1  (we require all other players cooperated last round)  

High‐level description:  
1. Start by defecting to establish your reputation as non‐cooperator.  
2. In each subsequent round except the last, if and only if everybody else cooperated in the previous round, cooperate with small probability ε (to “lure” others back to cooperation); otherwise defect.  
3. In the final round (and penultimate if you want a strict “no‐forgiveness” endgame), always defect.  

Rationale:  
– You free‐ride as much as possible.  
– You only contribute (very rarely) when it’s clear everyone else is already paying in, so the marginal effect of your one contribution on their willingness to cooperate can be high.  
– You never trust cooperators in the final round(s), reaping the last‐round defect payoff.

Pseudocode  
``` 
Inputs: 
  n     ← number of players 
  r     ← total rounds 
  ε     ← small lure probability (e.g. 0.1) 
  history ← empty list of length r to record total contributions each round 

For t in 1..r:
  if t == 1:  
    action[t] ← D    # round 1: defect
  else if t >= r:    
    action[t] ← D    # final round: defect
  else:  
    # look at last round’s contributions
    last_total_C ← history[t-1]        # number of C plays in round t–1
    # did all other n–1 players cooperate last round?
    if last_total_C == n–1 and RAND() < ε:
      action[t] ← C    # lure them with tiny cooperation
    else:
      action[t] ← D    # otherwise defect

  # (After the round resolves) record actual total cooperators:
  history[t] ← sum of all players’ c_j this round
```

Edge‐cases handled:  
• t=1 (no history): you defect.  
• t=r (last round): you defect, capturing the one‐shot defection gain.  
• If someone ever defects in round t–1 (so last_total_C < n–1), you never cooperate in round t.  
• You only cooperate when you can plausibly “extort”: i.e. they were fully cooperative just before, and there are still future rounds beyond the very last.  

Why it’s aggressive:  
– It maximizes your private payoff each round by defecting.  
– It uses a minimal occasional cooperation only as a carrot to sustain cooperation by others, so you can continue to exploit them.  
– It enforces harsh punishment (permanent defection) if they ever slip, and no forgiveness in the final stage.
'''

description_AGGRESSIVE_76 = '''
Below is a simple but maximally aggressive “never‐help, always‐exploit” strategy.  It uses no cooperation, never forgives, and so maximizes your individual share whenever others do cooperate.

1.  Overview  
   •  In every round t ∈ {1,…,r}, play D.  
   •  No memory or history check is needed—this is the classic Always‐Defect (All‐D) strategy.  

2.  Rationale  
   •  Since k<n, any contribution (C) costs you 1 but returns you k/n<1.  You always lose by cooperating.  
   •  By defecting you keep your 1.  If others ever cooperate, you get the extra (k/n)·(# of their C’s) “for free.”  
   •  You never give them the chance to exploit you.  

3.  Decision Rule  
   For each round t = 1…r:  
     action_i(t) ← D  

4.  Edge Cases  
   •  First round (t=1): D  
   •  Middle rounds (1<t<r): D  
   •  Last round (t=r): D  
   There is no special end‐game twist—defection in the last round can never be punished.  

5.  Pseudocode  
```
Input:  n, k, r
For t in 1..r do
    action[t] = D
End
```

6.  Aggressiveness  
   •  You never cooperate or forgive.  
   •  You systematically exploit any and all “cooperator” strategies in the population, grabbing the full private endowment plus the public‐good share they create.  

This Always‐Defect rule is the simplest aggressive strategy and, in a tournament against any mixture of cooperators, conditional cooperators or nicer types, will maximize your individual payoff every round.
'''

description_AGGRESSIVE_77 = '''
Below is a single‐player “aggressive exploiter” strategy.  It uses a limited “build-trust then betray” trick to milk any reciprocators, but it never hesitates to defect once it’s time to cash in.  In the absence of any cooperation by the field it simply defects forever.

1.  Notation  
    •  t ∈ {1,…,r} is the current round.  
    •  H_t = the vector of all opponents’ actions in rounds 1…t–1 (C or D).  
    •  T = ⌊r/2⌋ is the cut-over round (you may vary the fraction to tune aggressiveness).

2.  High-level description  
    – Rounds 1 through T (“trust-building window”):  
       •  If you’ve seen only C’s so far, play C to induce cooperation.  
       •  If you’ve seen any D, you give up on trust and defect forever.  
    – Rounds T+1 through r (“exploit window”):  
       •  Always play D.  

   By cooperating early only when others have cooperated, you maximize the chance of sustained group‐C if there are reciprocators among the field.  Once you hit round T+1, you defect every round to grab the public good while others keep cooperating.  If at any point before T someone defects, you immediately switch to all‐D.

3.  Detailed decision rules  
   For t = 1 … r:  
     if t ≤ T then  
       if all opponents’ actions in H_t are C (or t=1 so H_t is empty) then  
         play C  
       else  
         play D  
     else  (t > T)  
       play D  

4.  Edge‐case handling  
   – First round (t=1): no history, treat as “only C’s seen,” so you play C.  
   – Last round (t=r): always D (since r > T).  
   – If at any time in 1…T you observe a single D, you defect in that round and every subsequent round.

5.  Pseudocode  

```
input: r, history H

T ← floor(r/2)

function decide_action(t, H_t):
    if t ≤ T then
        if all actions in H_t are C (or H_t is empty) then
            return C
        else
            return D
    else
        return D

# Example tournament loop:
for t = 1 to r do
    observe H_t   # opponents’ actions in rounds 1…t–1
    my_action ← decide_action(t, H_t)
    play my_action
end for
```

6.  Why it’s aggressive  
  – Builds minimal trust to lure “nice” opponents into mutual cooperation.  
  – Abruptly ceases cooperation at mid‐game, maximizing the number of cooperators you exploit.  
  – If anyone defects early, you never waste a cooperative round—switching immediately to permanent defection.  
  – Always defects in the last half, guaranteeing you never get stuck as a “sucker” at the end.
'''

description_AGGRESSIVE_78 = '''
Below is a self-contained “aggressive” strategy—call it Probe-and-Exploit—that you can drop into any n-player public-goods tournament.  It does a very small number of cooperative “probes” to detect who will play C, then switches permanently to defection to plunder any remaining cooperators.  There is no forgiveness, no second chances, and no signaling beyond those initial probes.

1.  High-level description  
    a.  Probe phase (very short): contribute to see who else contributes.  
    b.  Exploit phase (long): once we know there are cooperators, we defect every round (including the last) to maximize our own payoff.  
    c.  If no one ever cooperates during the probe phase, we still defect forever (to avoid wasting further contributions).

2.  Why is it aggressive?  
    –  We willingly incur a tiny up-front cost to identify exploitable cooperators.  
    –  As soon as any are spotted, we defect permanently, free-riding on their continued cooperation.  
    –  We never punish defectors (we only ever defect ourselves), so there is no “tit-for-tat” forgiveness—just relentless plunder.  

3.  Handling special cases  
    –  First round(s): we do 1 (or at most 2) probe contributions, even though it costs us if the group is unresponsive.  
    –  Last round: always defect (no pending punishment or future gain).  
    –  Very small r (r=2,3): the probe-window automatically shrinks to 1 round, so we always cooperate once (round 1) then defect.

4.  Pseudocode  

```  
Inputs:  
  n   = number of players  
  r   = total rounds (integer ≥2)  
  k   = public‐goods multiplier (1 < k < n)  

Parameters:  
  m = min(2, r−1)        // length of probe phase: either 1 (if r=2) or 2 (if r≥3)  
State variables (initialized before round 1):  
  observed_cooperators = 0  
  exploitation_mode    = false  

For each round t = 1,2,…,r do:  
  if t ≤ m then  
    // Probe phase: contribute to test for cooperators  
    action_i(t) = C  
  else  
    // Once t == m+1, we have seen all probes; set exploitation flag  
    if t == m+1 then  
      // Count how many times *others* contributed in the probe window  
      // (total contributions in rounds 1..m minus our own m probes)  
      observed_cooperators = (Σ_{round=1..m} total_contributions) − m  
      if observed_cooperators > 0 then  
        exploitation_mode = true  
      end if  
    end if  

    // Exploitation phase (including final round): always defect  
    action_i(t) = D  
  end if  

  // (Note: our code never chooses C after t>m)  
end for  
```  

5.  Explanation of payoffs  
  –  If there are *no* cooperators in rounds 1..m, we defect forever and the group stays at all-D (each gets 1 every round).  
  –  If *any* opponent cooperates in those first m rounds, we switch to permanent defection and free-ride on anyone who continues to cooperate, harvesting 1 + (k/n)·(#cooperators) each round.  
  –  Last round is always D, so there is no end-game “mistake” or wasted cooperation.  

This strategy embodies an aggressive mindset:  it won’t second-guess itself or try to enforce mutual cooperation; it simply tests once or twice, then mercilessly defects to maximize short-term gain from any cooperators in the field.
'''

description_AGGRESSIVE_79 = '''
Below is a simple but maximally “aggressive” strategy: it never sacrifices private payoff to help the group.  It exploits any cooperator every time, never forgives, and never cooperates—even in the first or last round.

1.  Decision rule  
   At every round t (1 ≤ t ≤ r), play D (Defect), regardless of history.

2.  Edge‐case handling  
   • First round (t = 1): no history ⇒ play D.  
   • Intermediate rounds (1 < t < r): regardless of what others did before, play D.  
   • Last round (t = r): play D.  

3.  Aggressive mindset rationale  
   – In one‐shot and repeated public goods, defection strictly dominates cooperation (k/n < 1).  
   – By always defecting you (a) never pay the cost of contributing, (b) reap the full private payoff plus your share of any others’ contributions, and (c) never open the door to being exploited yourself.  

Pseudocode  
-----------  
```
function decideAction(round t, history H):
    // history H is a list of past action profiles, unused here
    return D
```

No memory, no forgiveness, no cooperation—pure aggression.
'''

description_AGGRESSIVE_80 = '''
Below is a simple yet maximally aggressive strategy.  It never sacrifices immediate private payoff and will exploit any cooperator every time.  No cooperation is ever offered (so there is nothing to “forgive” or “punish” after), and you always free-ride on whatever public good others may accidentally build.

Name: Aggressive Always-Defect (AAD)

1.  Data structures / state  
    – r : total rounds (known at outset)  
    – t : current round index (1 ≤ t ≤ r)  
    – history[t–1] : list of all players’ actions in previous rounds (empty for t=1)  

2.  Decision rule  
    For every round t = 1,2,…,r:  
      action_i(t) ← D  

3.  Edge cases  
    – First round (t=1): no history, but rule still says Defect.  
    – Intermediate rounds (1 < t < r): same rule, always Defect.  
    – Last round (t=r): since there is no future to influence, still Defect.  

4.  Rationale / aggressive mindset  
    – You never contribute your endowment, so (1–c_i)=1 every round.  
    – Whatever public good others generate, you always share in it without ever paying the cost.  
    – There is zero risk of being “duped” into cooperation.  
    – Against any conditional‐cooperator or tit-for-tat style opponent, you will consistently earn 1 + (k/n)·(#cooperators) ≥ 1 each round, while they pay the cost of cooperating.  
    – This is a dominant strategy in the one‐shot PG game and remains so in the repeated setting if your sole goal is to maximize total payoff regardless of “group welfare.”  

5.  Pseudocode  
    function DecideAction(history, t, r):  
      return “D”    # always defect  

That is your entire strategy.  It never forgoes private payoff, never signals, never “tests” or “forgives,” and thus fully embodies an aggressive, exploit‐first mindset.
'''

description_AGGRESSIVE_81 = '''
Below is a self‐contained “aggressive” strategy for the repeated N-player public-goods game.  It uses a short “bait” phase to win a little trust, then defects relentlessly—even in the “endgame.”  

Strategy name: Two-Round Bait and Rampant Defection

Parameters derived from r (number of rounds)  
• handshake_rounds = min(2, r − 1)  
  – If r = 2, you cooperate in round 1 only.  
  – If r ≥ 3, you cooperate in rounds 1 and 2.  

Decision rule for round t:  
1. If t ≤ handshake_rounds: play C (cooperate).  
2. Otherwise: play D (defect).  

Rationale  
• First 1–2 rounds you “bait”: cooperating may induce some conditional cooperators to cooperate back, boosting the public pot.  
• From round handshake_rounds+1 through r you defect every time, securing the private good while still reaping any residual public contributions from others.  
• Even in the last round—where no future punishment is possible—you defect (maximal private payoff).  

Edge‐case handling  
• r = 2: handshake_rounds=1 → round 1: C; round 2: D.  
• r = 3: handshake_rounds=2 → rounds 1–2: C; round 3: D.  
• r>3: rounds 1–2: C; rounds 3–r: D.  

Pseudocode  
```
Input: r  // total number of rounds
handshake_rounds = min(2, r - 1)

for t in 1..r do
    if t <= handshake_rounds then
        action_t = C
    else
        action_t = D
    end
end
```

Discussion of aggressiveness  
• You never forgive or return to cooperation after round handshake_rounds.  
• You exploit any cooperators who continue to pump the public good long after you’ve switched to defection.  
• You incur at most handshake_rounds “losses” (foregone private payoff) in order to potentially trigger higher contributions from opponent strategies—then you harvest for the remainder of the game.
'''

description_AGGRESSIVE_82 = '''
Below is a self-contained, purely deterministic “Aggressive Exploiter” strategy for the repeated N-player public-goods game.  It is built around three ideas:  
  1.  “Warm-up” cooperating to lure more‐gullible strategies into mutual cooperation.  
  2.  A sharp switch to all-out defection once we have built up enough public-good contributions or detected too much defection.  
  3.  No forgiveness after the switch—defecting until the final round.  

––––––––––––––––––––––––––––––––––––––––  
1.  Key parameters  
   •  r  = total rounds (r > 1)  
   •  τ  = warm-up length = max(1, ⌈r/4⌉)  
   •  θ  = defection–tolerance threshold = 0  (i.e. any defection in warm-up aborts cooperation)  

2.  State variables  
   •  warmup_active (bool) – true initially, becomes false once we switch to exploitation  

3.  High-level description  
   Rounds 1…τ (“Warm-up Phase”):  
     – Cooperate every round unless we see any defection from any player in the immediately preceding round;  
       if we see a single defector, we immediately “flip the switch” and go into Exploitation Phase.  
   Rounds τ+1…r (“Exploitation Phase”):  
     – Defect every round, including the final round.  

   This means:  
     – In warm-up we signal cooperation and build a public-good pot.  
     – At the earliest sign of non-unanimity (or once τ is up), we stop cooperating forever.  
     – By timing τ appropriately (≈r/4), we leave enough rounds to exploit the cooperators.  

4.  Pseudocode  
```
Inputs:
  r          ← total number of rounds
  history    ← empty list of previous rounds’ actions; each entry is a length-n vector of C/D
Initialize:
  τ          ← max(1, ceil(r/4))
  warmup_active ← true

For t in 1..r do:
  if warmup_active is true then
    if t == 1 then
      action_i ← C
    else
      # look at last round’s profile
      last_profile ← history[t−1]   # vector of length n
      if exists j such that last_profile[j] == D then
        # someone defected in warm-up → abort cooperation
        warmup_active ← false
        action_i ← D
      else if t ≤ τ then
        action_i ← C
      else
        # warm-up window expired
        warmup_active ← false
        action_i ← D
      end if
    end if
  else
    # Exploitation phase: always defect
    action_i ← D
  end if

  # Record own and others’ moves at end of round
  Observe full profile a_t ∈ {C,D}^n
  Append a_t to history
End For
```

5.  Edge-case handling  
•  r small (e.g. r ≤ 2): τ = 1, so we cooperate only on round 1, then defect on round 2.  
•  Immediate defection in round 1 warm-up (somebody defects vs us): we switch to defection in round 2.  
•  No forgiveness: once we leave warm-up, we never return, even if the other players go back to 100% cooperation.  
•  Final round: we are defecting (maximally aggressive) regardless of history.  

6.  Why “aggressive”?  
•  We grab first-mover trust by cooperating, thereby boosting the public pot.  
•  At the first hint of non-unanimity or as soon as our short τ expires, we defect forever—crushing any lingering cooperation.  
•  No leniency: cooperators get exploited in every remaining round, and defectors are never forgiven.  
•  Relative payoff is maximized by alternating: build public good briefly, then free-ride until the end.
'''

description_AGGRESSIVE_83 = '''
Below is an “aggressive” contingent‐defection strategy tailored for the n‐player public goods game.  It only ever rewards perfect mutual cooperation, punishes any lapse immediately and unforgivingly, and always defects on the first and last rounds.

Strategy name: Unforgiving Threshold Extortion (UTE)

Parameters and internal state  
• n — number of players  
• r — total rounds  
• state.triggered ∈ {false, true} — becomes true the first time anyone defects (other than you); once true, you never again cooperate  

Decision rule for round t (1 ≤ t ≤ r)  
1. If t == 1 or t == r:  
     Action ← D  
     (Always defect on the first round to probe, and on the last round by backward induction.)  
2. Else if state.triggered == true:  
     Action ← D  
     (Once anybody has defected, you punish forever.)  
3. Else (t ∈ {2,…,r–1} and no defection seen yet):  
     Let C_prev = number of cooperators in round t–1 among all n players.  
     If C_prev == n:  
         Action ← C  
         (Everybody cooperated last round, so you “reward” with cooperation this round.)  
     Else:  
         Action ← D  
         state.triggered ← true  
         (You see at least one defection; you defect now and trigger permanent punishment.)  

Pseudocode  
```
initialize state.triggered = false

for t in 1..r:
    if t == 1 or t == r:
        play D
        continue

    # t in 2..r–1
    if state.triggered:
        play D
        continue

    # no defection seen so far
    C_prev = count of cooperators (including you) in round t-1
    if C_prev == n:
        play C
    else:
        play D
        state.triggered = true
```

Explanation of aggressiveness  
• First‐round defection “tests the waters” and immediately sets the tone.  
• You only ever cooperate if you observed perfect full‐group cooperation in the immediately preceding round; any single defection by any player causes you to switch to permanent defection (grim trigger).  
• You also defect on the last round (standard backward‐induction move).  
• By refusing to tolerate even one defection and refusing to forgive, you maximize your exploitation of any cooperative majority and punish free riders harshly.
'''

description_AGGRESSIVE_84 = '''
Below is a single‐player “aggressive exploiter” strategy that, against any profile of opponents, seeks to maximize its own payoff by never tolerating sustained cooperation and by “baiting” when the group has given up entirely.

1.  Overview  
    •  We never cooperate into a rising cooperation level; we punish any sign of cooperation immediately by defecting and reaping the extra private 1.  
    •  If everyone is defecting, we sometimes (with tiny probability ε) cooperate just to see if someone is naïvely willing to cooperate—and if they do, we switch to full defection and exploit them.  
    •  In the very first and very last rounds we always defect (no reason to cooperate for future leverage).

2.  Notation  
    n     = number of players  
    r     = total rounds  
    t     = current round (1 … r)  
    c_i,t = 1 if player i cooperates in round t, 0 if defects  
    C−me_t = Σ_{j≠me} c_j,t  (number of opponents who cooperated in t)  
    ε     = small “baiting” probability, e.g. 0.05

3.  Decision rules (pseudocode)

```
Initialize:
  last_Cminus_me ← 0

For each round t=1…r do:
  if t == 1 or t == r:
    play D
  else:
    if last_Cminus_me > 0:
      # Someone just cooperated: punish forever
      play D
    else:
      # Nobody cooperated last round: try a small bait
      with probability ε:
        play C
      else:
        play D

  # After all moves are revealed:
  last_Cminus_me ← Σ_{j≠me} c_j,t   # update count of others’ cooperations
end for
```

4.  Explanation of key features

•  First‐round defection (“t==1”):  
   We start by defecting to establish that we will not give free public goods.

•  Last‐round defection (“t==r”):  
   No future to leverage, so defect for the sure +1 private return.

•  Punishment of any cooperation:  
   As soon as any opponent cooperates in round t−1 (i.e. last_Cminus_me > 0), we defect in all subsequent rounds.  This permanently discourages cooperation by making it strictly unprofitable: any cooperator gives us an extra +1 each time.

•  Baiting when group is all‐defect:  
   If nobody cooperated in the previous round, we occasionally (probability ε) cooperate ourselves.  If someone else is tempted and cooperates as a result, last_Cminus_me becomes >0 and from that point we permanently switch to defection–exploitation mode.  If nobody bites, we slip back to defection and try again later (or until the last round forces defection anyway).

5.  Handling edge cases

•  If all opponents always defect, we will keep occasionally trying ε‐bait until the last round; but even if they never bite, our expected loss from those rare ε cooperations is tiny, and we still guarantee ≥1 per round.  
•  If at any point even one opponent cooperates for any reason, we immediately convert to permanent all‐rounds defection.  Against a cooperator‐heavy group, we exploit them by free‐riding on their contributions every remaining round.  
•  In the degenerate case ε=0 the strategy reduces to “Always Defect,” which is aggressive but forgoes baiting; ε>0 is recommended to catch soft opponents.

6.  Aggressiveness summary

This strategy never grants a long‐term cooperative opportunity to its rivals.  It permanently punishes the first sign of cooperation, mines an extra +1 payoff each future round, and only briefly “sacrifices” an endowment with tiny probability to bait new cooperators when the group is in full‐defection mode.  That makes it maximally aggressive, self‐maximizing, and unforgiving.
'''

description_AGGRESSIVE_85 = '''
Below is an “all-out aggressive” strategy.  In a finitely repeated public‐goods game with 1<k<n, defection strictly dominates cooperation in every single round, and backward induction tells us to defect every round.  This strategy therefore never cedes advantage.

Strategy Name: Perpetual Defection

1.  Decision Rule  
    For each round t = 1, 2, …, r:  
       Play D (Defect).

2.  Edge Cases  
    •  First round (t=1): No history yet → play D.  
    •  Intermediate rounds (1<t<r): Irrelevant what history is → play D.  
    •  Last round (t=r): Standard end‐game defect → play D.

3.  Aggressive Alignment  
    •  Never contributes to the public good, thereby  
       –  Avoiding any sunk cost of c_i=1.  
       –  Always capturing the full private endowment plus the group’s contributions.  
    •  By refusing cooperation, punishes any partial cooperators and exploits fully cooperating opponents for maximal gain.

Pseudocode  
```
Inputs: n, k, r
For t in 1..r:
    action[t] = D
Return action[1..r]
```

Rationale  
–  In a single round, cooperating gives payoff (k/n)·Σc_j  ≤ k < 1 + (k/n)·Σc_j, so D strictly dominates C.  
–  With perfect foresight of a finite horizon, there is never an incentive to cooperate.  
–  This strategy maximizes your round‐by‐round and total payoff, and imposes zero benefit on others.
'''

description_AGGRESSIVE_86 = '''
Below is a complete “aggressive” n-player public-goods strategy, which we’ll call Aggressive Exploiter.  It never tries to build mutual cooperation; instead it (1) defects by default, (2) punishes any sign of cooperation, and (3) occasionally “probes” to lure unwitting cooperators so it can exploit them.    

1.  Strategy overview  
    – Always prioritize defection (D).  
    – If you see any cooperation from others, keep defecting (punish and exploit).  
    – If no one cooperated last round, occasionally cooperate (probe) to test whether others will cooperate—so you can exploit them next round.  
    – Never cooperate in the final round.    

2.  Decision rules  
    Let r = total rounds, t = current round (1 ≤ t ≤ r).  
    Let last_sum = Σ_{j=1..n} c_j from round t–1 (total cooperators last round).  
    Fix a small probing probability p ∈ (0,1), e.g. p=0.1.  

    Round 1:  
      • No history → Defect.  

    Rounds 2 ≤ t ≤ r–1:  
      if last_sum > 0 then  
        play D  // punishment/exploitation: someone cooperated last round  
      else  
        with probability p play C  // probe  
        otherwise play D  

    Round r (last round):  
      play D  // never give free benefits at the end  

3.  Edge‐case handling  
    • If r = 2, then both rounds fall under “always defect,” so you simply defect twice.  
    • If you ever observe mass cooperation (last_sum = n), you still defect and gain the full k·n/n share.  
    • You only look one round back; no longer memory is required.  

4.  Pseudocode  

    function AggressiveExploiter(t, history):  
      Input:  
        t       – current round (1..r)  
        history – list of past tuples (c_1,…,c_n) for rounds 1..t–1  
      Constants:  
        r       – total number of rounds  
        p       – probe probability (e.g. 0.1)  
      let last_sum = 0  
      if t > 1 then  
        last_sum = sum_j of history[t–1].c_j  

      if t == 1:  
        return D  

      else if t == r:  
        return D  

      else:  // 2 ≤ t ≤ r–1  
        if last_sum > 0:  
          return D        // punish/exploit any cooperators  
        else:  
          draw u ∈ Uniform[0,1]  
          if u < p:  
            return C      // probe for potential cooperators  
          else:  
            return D  

5.  Why it’s aggressive  
    – It never forgives: once you or anyone cooperates, it defects forever afterward.  
    – It occasionally “fakes” cooperation only when all others just defected, to bait naïve cooperators.  
    – It maximizes your individual share whenever others cooperate, and it never contributes in the final round.  
    – No assumption of norms or coordination—purely self-interested, punitive and exploitative.
'''

description_AGGRESSIVE_87 = '''
Below is a fully specified “aggressive” strategy—call it Always-Defect—that maximizes your own payoff by never contributing, exploits any cooperators in the group, and takes into account first‐round and last‐round logic.

1.  Strategy Name  
    Aggressive Always-Defect (AAD)

2.  Intuition & Rationale  
    •  In a single shot, Defect strictly dominates Cooperate whenever k<n.  
    •  In a finitely repeated game with known horizon, backward induction also leads to defection in every round.  
    •  By never contributing you both (a) avoid the cost of cooperation and (b) harvest any public good created by opponents.

3.  Decision Rule  
    For each round t=1,…,r, choose D (Defect), unconditionally.

4.  Edge‐Case Handling  
    •  First round (t=1): Defect.  
    •  Middle rounds (1<t<r): Defect.  
    •  Last round (t=r): Defect (no future rounds to punish you).

5.  Pseudocode  

    Input:  
      r  ← number of rounds  
      history  ← empty list initially  

    For t in 1..r:  
      action_i[t] ← “D”  
      Submit action_i[t]  

      // After actions are observed, append to history if needed  
      history.append(all_players’ actions this round)

6.  Tournament Note  
    •  Against any non-defector you will exploit their contributions every time.  
    •  Against other all-defectors the payoff settles to 1 per round.  
    •  There is no self-inflicted punishment or forgiveness—pure aggression.
'''

description_AGGRESSIVE_88 = '''
Below is a self-contained, “aggressive” strategy—call it Aggro-Grim—that you can drop straight into a tournament.  It never sacrifices long-term advantage for the group, it refuses to be suckered by cooperators, and it punishes any sign of cooperation with permanent defection.

1.  Data structures / state  
   • punished (Boolean), initially False  
   • current_round t ∈ {1,…,r}  

2.  Decision rule at each round t  

   if t == 1:  
     • Action ← D  
   else if punished == True:  
     • Action ← D  
   else if (∃ j ≠ i : c_j,t–1 == 1) then  
     // someone cooperated last round ⇒ trigger grim punishment  
     • punished ← True  
     • Action ← D  
   else  
     // no one ever cooperated (so far), we maintain defection  
     • Action ← D  

   // override: on the last round, always defect  
   if t == r:  
     • Action ← D

3.  Explanation  

   – “Defect” (D) always yields at least 1 plus whatever others contribute; “Cooperate” (C) always costs 1 privately and can never beat a defector in the same profile.  
   – We start by defecting to establish that we won’t be exploited.  
   – As long as no one cooperates, we stay in ‘peaceful’ defection mode (we’re not wasting a state-variable flip on a defector-only world).  
   – The moment any player shows cooperation, we flip punished→True and from then on we permanently defect.  That’s a Grim trigger: the harshest punishment, disincentivizing any hope of a “gentle tit-for-tat” overture.  
   – In the last round we also defect (there’s no future to incentivize).  

4.  Pseudocode  

   initialize punished ← False  
   for t in 1…r do  
     if t == 1 then  
       play D  
     else if punished == True or t == r then  
       play D  
     else  
       let coop_prev = Σ_{j≠i} c_j,t–1  
       if coop_prev > 0 then  
         punished ← True  
         play D  
       else  
         play D  
       end if  
     end if  
   end for  

5.  Why it’s aggressive  

   – You never cooperate.  
   – You threaten the harshest possible punishment (permanent defection) at the first sign of cooperation.  
   – You rob any would-be cooperators of future gains, driving the group into a low-payoff “all-D” equilibrium if they try to build trust.  
   – It maximizes your own unilateral payoff given any mix of opponent behaviors.
'''

description_AGGRESSIVE_89 = '''
Below is a simple but brutally “aggressive” strategy for the repeated public‐goods game.  It exploits any cooperators, never incurs a contribution cost itself, and denies all future opportunities for revenge or reconciliation.

1. Key Idea  
   Since k / n < 1, contributing (C) always costs you more than it returns you; defection (D) strictly dominates in every single round.  An “aggressive” mindset simply never gives ground.  

2. Decision Rule  
   On every round t ∈ {1,…,r}, play D, regardless of history or expected future.  

3. Edge Cases  
   – First round: no history → play D  
   – Middle rounds: ignore history → always D  
   – Last round (t = r): obviously defect (no future punishment possible)  

4. Pseudocode  
```
Inputs:
  r      // total number of rounds
  t      // current round index (1 ≤ t ≤ r)
  history // list of past action profiles; not used

Function choose_action(t, history):
    return D
```

5. Rationale  
   • Immediate gain: By playing D you keep your private endowment (1) plus still collect your share of whatever others have contributed.  
   • Exploitation: If any opponents ever cooperate, you free‐ride on their gifts without ever reciprocating.  
   • No risk: You never incur the 1‐unit cost of contributing.  
   • Last‐round defection is dominant in any finite horizon, so there is no credible commitment to ever cooperate.  

This “always defect” rule is the most aggressive playable strategy under the standard assumptions: you maximize your own payoff in every round, exploit any cooperators, and refuse all cooperation forever.
'''

description_AGGRESSIVE_90 = '''
Below is a maximally “aggressive” strategy—one that never gives up private payoff to build the public good and that always exploits any co‐operators.  In effect it is a grim‐trigger/extortion style rule that reduces to “always defect,” but is phrased to show how it punishes any sign of cooperation.

1.  Overview of the Mindset  
    – We view every cooperator as someone to be exploited.  
    – We never invest our own endowment in the public good.  
    – We never forgive/cooperate once anyone has cooperated.  
    – In the last round there is no future punishment, so we still defect.

2.  Decision Rules  
    Let t = current round, H_t−1 = history of all players’ moves up to t−1, and c_i(t−1) ∈ {0,1} be whether player i cooperated last round (1 = C, 0 = D).

    For each round t = 1…r, do  
      if t = 1:  
        play D  // no history yet, start aggressive  
      else:  
        // if any player ever cooperated in the past, continue defecting  
        if ∃ j ∈ {1…n} such that c_j(t−1) = 1  
           play D  
        else  
           play D  
      end if

    Equivalently:  
      play D in every round.

3.  Pseudocode  

    function AggressiveDefector(n, r, history):  
      // history is a list of past action‐profiles  
      return “D”

4.  Edge Cases  
    – First round (t=1): no history ⇒ defect.  
    – Intermediate rounds: we never switch to C, regardless of what others do.  
    – Last round (t=r): still defect (no future to enforce cooperation).  
    – If somehow all others switch to permanent cooperation (unlikely without coordination), we still defect each round, capturing the maximal share of the public good at their expense.  

5.  Rationale  
    – By never cooperating we avoid the -1 private loss from contributing.  
    – Whenever there are cooperators in the group, we grab our private 1 plus our share of the public good, outperforming any cooperator in that round.  
    – No incentive ever arises to shift to C since k<n guarantees (k/n)×total_contrib ≤1, so you never strictly gain by giving up your private 1.  

This rule is the simplest extreme‐aggressive strategy.  It maximizes per‐round payoff against any mix of opponents and ensures that any attempt by others to cooperate is ruthlessly exploited.
'''

description_AGGRESSIVE_91 = '''
Below is a self‐contained “Aggressive Exploiter” strategy.  In plain English it simply uses one (optional) probe of cooperation in round 1 and then defects every round thereafter—thereby ensuring you never pay the cost of cooperation except for at most one small test, and you exploit any lingering cooperators to the fullest possible extent.  No matter how many rounds, no matter how many players, no communication or coordination is needed.

Name:  Aggressive Exploiter (First-Round Probe, Then Permanent Defection)

1.  Data kept in memory  
    •  r = total number of rounds  
    •  t = current round index (1 ≤ t ≤ r)  
    •  history of contributions c_j,t′ for all players j in prior rounds t′ < t  

2.  Decision rule  
    if t == 1 then  
       action ← C    ▹ optional probe: see “Variants” below  
    else  
       action ← D    ▹ defect every round from 2 through r  

3.  Edge-case handling  
    •  First round (t=1): we play C to see if anyone else is willing to cooperate (only if you choose the probe variant).  If you fear lone cooperation is too costly, you may simply defect in round 1 as well—see “Variants.”  
    •  Last round (t=r): still defect.  There is no end-game upside to cooperating, and indeed defection strictly dominates cooperation in a one‐shot public goods round when k<n.  
    •  All intermediate rounds (2 ≤ t ≤ r–1): defect without exception.

4.  Rationale / Aggressive mindset  
    •  Defection strictly dominates cooperation in a single public goods round (since k<n ⇒ 1+(k/n)·m > (k/n)·(m+1) for any m).  
    •  By defecting you “punish” any cooperator and extract the higher private payoff whenever others try to build the fund.  
    •  The one‐round probe can reveal whether any naïve cooperators exist.  Whether they do or not, from round 2 on you exploit them relentlessly.  
    •  You never incur the cost 1 of contributing, and you never miss an opportunity to free-ride on others’ contributions.

Pseudocode  
----------
Inputs: n, k, r   (only r is needed at runtime)  
State: t ← 1  

Loop t from 1 to r:  
    if t == 1 then  
        play C      # optional probe—see note below  
    else  
        play D      # permanent defection  

    Observe all players’ moves in round t (stored in history)  
    t ← t + 1  

Variants  
--------  
1.  Pure Always-Defect  
    •  If you judge even one round of cooperation too risky, simply set “if t==1 then D.”  You will then defect every round unconditionally.  

2.  Two-Round Probe  
    •  If you believe a larger initial pool helps you exploit more, you could cooperate in rounds 1 and 2, then defect from 3…r.  That may generate a slightly larger public‐good pot to free-ride on, but at the risk of paying two contribution costs.  

3.  Threshold Probe  
    •  Cooperate in round 1.  If at least T other players cooperated in round 1 (for some small T you choose), cooperate again in round 2—otherwise switch immediately to permanent defection in round 2 onward.  

All variants share the same aggressive core: never forgive, never err toward cooperation once the exploitation phase begins, and always defect in the final round.
'''

description_AGGRESSIVE_92 = '''
Below is a maximally aggressive (“self-ish”) strategy for the repeated public‐goods game.  In effect it simply refuses to cooperate at any point, thereby (i) never risking a sucker payoff, (ii) always free‐riding on any cooperators, and (iii) punishing cooperators by depressing the public good.

1. Decision Rule  
   For every round t = 1, 2, …, r:  
     Play D (Defect).

2. First-Round Rule  
   No history yet → play D.

3. Intermediate Rounds  
   Regardless of how many (or few) opponents cooperated last round, play D.  
   You neither reward nor attempt to “shake down” cooperators with occasional C’s—pure defection always dominates.

4. Last-Round Rule  
   Standard backward‐induction: defect.

5. Rationale (Aggressive Mindset)  
   – One‐shot dominant strategy is D; repeating doesn’t change payoffs.  
   – You never incur the cost of contributing (c_i=1) and always capture the full private payoff plus whatever public good others provide.  
   – By never cooperating you punish any cooperative “soft” strategies in the tournament.

Pseudocode  
----------  
function next_move(t, history):  
    # history is the list of past action profiles; it is unused  
    return D  

End.

This strategy trivially handles all edge cases (first round, last round, or any intermediate round) by always defecting. It is maximally exploitative and aggressive.
'''

description_AGGRESSIVE_93 = '''
Below is a complete “aggressive” strategy—call it Aggressive Defector—that refuses every contribution, thereby (1) maximizes your private payoff whenever others do cooperate and (2) rigorously punishes any attempt at group cooperation.  It is essentially an all-D (always defect) rule, with no forgiveness or random cooperation.  

1.  Decision rules  
   – In every round t = 1,…,r, play D (Defect).  

2.  Edge cases  
   – First round: Defect.  
   – Last round: Defect.  
   – No history dependence at all.  Regardless of what others have done or will do, you always defect.  

3.  Why this is “aggressive”  
   – A pure defector gains the private endowment (1−c_i=1) and still collects the public good share (k/n × total_cooperators).  
   – If the rest of the group ever tries to cooperate, you exploit them: you get 1 + (k/n)·(#cooperators) per round instead of only (k/n)·n when you yourself would have cooperated.  
   – By never cooperating you send the clearest possible “punishment” signal to any would-be cooperators: there is zero hope of reciprocity.  

4.  Pseudocode  
```
function select_action(round t, history H):
    // history H is not used
    return D
```

5.  Tournament-ready specification  
   – Input: round index t (1 ≤ t ≤ r); full history of all players’ past moves (ignored).  
   – Output: the single move D.  

Because defecting is a dominant strategy in a one-shot public-goods game (k < n ⇒ k/n < 1), and because we never “let up” or allow any cooperative window, Aggressive Defector both (a) maximizes your own payoff against cooperators and (b) brutally punishes any attempt at group building.
'''

description_AGGRESSIVE_94 = '''
Below is a fully specified “aggressive” PROBE-EXPLOIT strategy.  It systematically tests for cooperators and then ruthlessly defects to exploit them.  In every round it either “probes” by cooperating to sniff out any contributors, or “exploits” by defecting to grab the private payoff while others still contribute.  It never shows mercy, and in the final round it always defects.

1.  State variables and parameters  
   •  r = total number of rounds (known in advance)  
   •  P = probe interval (we set P = 3; every 3rd round we probe)  
   •  E = exploitation length after a successful probe (we set E = 2)  
   •  exploit_timer = 0  (counts down how many more rounds we will exploit)  

2.  High-level description  
   •  First round (t = 1): Probe (play C)  
   •  Every P-th round thereafter (i.e. t = 1, 1+P, 1+2P, …), we “probe” by playing C.  
     –  If in that probe round we observe at least one other cooperator, we have found suckers → set exploit_timer = E.  
   •  If exploit_timer > 0, we are in an exploit phase: we play D, decrement exploit_timer.  
   •  Otherwise (not probing and not exploiting), we play D.  
   •  In the very last round (t = r), we always play D (no future to exploit).  

3.  Pseudocode  

Initialize:
  exploit_timer ← 0

For each round t = 1 to r do:
  if t == r then
    action ← D
    // last-round defect
  else if t == 1 or ((t–1) mod P == 0) then
    // Probe round
    action ← C
  else if exploit_timer > 0 then
    // Exploitation phase
    action ← D
    exploit_timer ← exploit_timer – 1
  else
    // Normal phase (no probe, no exploit)
    action ← D
  end if

  Play(action)
  Observe everyone’s actions c₁,…,cₙ this round.

  // If we just probed and saw cooperators, trigger exploitation
  if action == C and t < r then
    total_cooperators ← Σⱼ cⱼ
    // if at least one OTHER player cooperated
    if total_cooperators – 1 ≥ 1 then
      exploit_timer ← E
    end if
  end if
end for

4.  Explanation of aggression  
  – The strategy never rewards cooperators in the long run.  
  – By probing, it locates rounds when at least one opponent is willing to contribute; it then punishes that goodwill for E consecutive rounds by defecting, thereby pocketing the full private endowment plus a share of others’ contributions.  
  – Outside probes and exploit bursts, it simply defects.  
  – In the final round it defects regardless—no chance for future reprisals or cooperation.  

5.  Edge-case handling  
  •  Small r (e.g. r < P + 1): t = 1 is the only probe, then always exploit (but in round r we still defect).  
  •  Multiple probes in a row?  Probes are spaced every P rounds; exploit bursts may overlap, but the timer logic cleanly handles back-to-back exploit phases.  
  •  If nobody ever cooperates, we spend almost all rounds defecting (pure defector).  
  •  If everyone starts defecting after early probes, we never “waste” cooperation again except on fixed probe schedule.  

This PROBE-EXPLOIT is ruthlessly aggressive: it yields zero sustained cooperation, opportunistically sucks value from any contributor it can detect, and otherwise remains a pure defector.
'''

description_AGGRESSIVE_95 = '''
Below is an “aggressive exploiter” strategy for the repeated n-player public-goods game.  Its philosophy is simple:  almost always defect, only very rarely cooperate to probe for any hopeful cooperators in the field, then ruthlessly exploit them.  In tournament play this maximizes your own payoff and keeps opponents off balance.

—----------------------------------------------------------------  
Strategy name  
  Predator‐Probe  

Parameters you may tune  
  r            total rounds  
  probe_interval = max(2, ⌈r/10⌉)   # how often to probe when group is silent  

State you carry forward  
  last_total_coop  = number of total cooperators (including you) in previous round  

Initialization  
  last_total_coop ← 0  

On each round t = 1..r do  
  if t = 1 then  
    action ← D      # never cooperate up front  
  else if t = r then  
    action ← D      # always defect in the final round  
  else  
    # 1) If there was any cooperation last round, exploit it by defecting  
    if last_total_coop ≥ 1 then  
      action ← D  
    else  
      # 2) If nobody cooperated last round, probe occasionally  
      if (t mod probe_interval) = 0 then  
        action ← C  
      else  
        action ← D  
      end if  
    end if  
  end if  

  # Submit action to the game, then observe total cooperators this round  
  Observe Σₙ c_j and set last_total_coop ← Σₙ c_j  

End for  

—----------------------------------------------------------------  
Explanation of decision rules  

1.  First round (t = 1): Defect.  
    You start by refusing to front‐load the public good.  

2.  Rounds 2..r–1:  
   a) If in the previous round ANY player (including you) contributed, that means there are at least some cooperators in the population.  You immediately defect to free‐ride on their contribution.  
   b) If last round was “all defect,” you still defect—except on those rare probe rounds (every probe_interval steps) where you momentarily cooperate just to see whether anyone is willing to respond.  

3.  Last round (t = r): Defect.  
   Standard end-game: there is no future to punish you, so always defect.  

—----------------------------------------------------------------  
Why this is aggressive  

•  You almost never cooperate, so you deny opponents the chance to build mutual trust.  
•  When cooperators do appear, you exploit them by defecting the very next round.  
•  Probing is infrequent enough that you remain unpredictable, but frequent enough to catch any sporadic cooperators.  
•  By defecting first and defecting last, you maximize personal payoff in both the opening and the endgame.  

You can adjust probe_interval (smaller ⇒ more frequent probes) but the core is: “Defect by default, probe rarely, exploit at first sign of cooperation.”
'''

description_AGGRESSIVE_96 = '''
Below is a fully specified “aggressive” strategy for the repeated N-player public-goods game.  In plain English it “dangles” the occasional cooperation to lure in well‐meaning cooperators, watches for a round with many cooperators, then switches to permanent defection (and in the final rounds never cooperates at all).  This maximizes your absolute payoff while punishing any group attempts at cooperation.

----------  
1.  Parameters you choose (fixed before play)  
   • p – small “luring” cooperation probability, e.g. p=0.1  
   • T – exploitation threshold, e.g. T=⌈n/2⌉  
   • PUNISH_ROUND – the round after which you never cooperate again; set to r–2  

2.  State variables  
   • exploitation_triggered (bool), initially false  

3.  Decision rule at each round t:  
   if t > PUNISH_ROUND then  
     play D  // last two rounds: never cooperate  
   else if exploitation_triggered then  
     play D  // once triggered, permanent defection  
   else  
     if t == 1 then  
       with probability p: play C  
       otherwise: play D  
     else  
       let m = number of cooperators in round t–1  
       if m ≥ T then  
         exploitation_triggered ← true  
         play D  // you saw enough cooperators—time to exploit permanently  
       else  
         with probability p: play C  // keep dangling cooperation  
         otherwise: play D  

4.  Edge‐case handling  
   • First round (t=1): you have no history, so you “probe” with prob p.  
   • Intermediate rounds (2 ≤ t ≤ r–2): you continue to flirt with cooperation until you see a big enough cooperative turnout (m ≥ T), then switch to all‐defect.  
   • Last two rounds (t > r–2): you defect no matter what—to secure your maximal private payoff and avoid any end‐game cooperation.  

5.  Why this is aggressive  
   • You never allow a stable cooperative equilibrium to persist.  
   • You exploit any cluster of cooperators by defecting exactly when they hit the threshold T.  At that point you lock in permanent defection and reap the highest single‐round gain.  
   • You minimize payoffs of cooperators by refusing to return to C once you have exploited them.  
   • The small “p” cooperation probability makes you look like a potential collaborator, drawing in naïve cooperators before you strike.  

----------  
Pseudocode  

```
INPUTS: n, r, k  
PARAMETERS: p ← 0.1, T ← ceil(n/2), PUNISH_ROUND ← r - 2  
STATE: exploitation_triggered ← false

for t in 1..r do
  if t > PUNISH_ROUND then
    action[t] ← D
  else if exploitation_triggered then
    action[t] ← D
  else
    if t == 1 then
      action[t] ← (rand() < p ? C : D)
    else
      m ← count_cooperators_in_round(t-1)
      if m ≥ T then
        exploitation_triggered ← true
        action[t] ← D
      else
        action[t] ← (rand() < p ? C : D)
      end if
    end if
  end if
end for

return action[1..r]
```

This strategy satisfies all requirements:  
– “Aggressive” (hooks cooperators, then permanently defects)  
– Fully specified decision rule for every round, including first and last  
– No external assumptions beyond observing past public actions.
'''

description_AGGRESSIVE_97 = '''
Below is an “aggressive” public‐goods strategy whose core is to defect every round except for rare “probes” when opponents have shown no cooperation for a while.  It (1) maximizes exploitation of any cooperators, (2) punishes or ignores defectors, (3) never forgives in the final round, and (4) only cooperates with a tiny probability to test whether anyone can still be exploited.  

—–  
1.  Variables and parameters  
 n: number of players  
 r: total rounds  
 ε: small probe probability (e.g. 0.05)  
 m: probe‐threshold window (e.g. 2 rounds)  
 history[t][j]: action of player j in round t (“C” or “D”)  
 coop_count[t] := number of players ≠ you who played “C” in round t  

2.  High-level decision rule for round t  

If t == 1 or t == r:  
 Play D   // Always defect on first and final round  

Else (1 < t < r):  
 If coop_count[t−1] ≥ 1 then  
  // Last round somebody cooperated ⇒ exploit them  
  Play D  

 Else // No one cooperated in the immediately preceding round  
  If for all k in {1 … m}, coop_count[t−k] == 0 then  
   // Nobody has cooperated in the last m rounds ⇒ probe with small chance  
   With probability ε play C  // one‐shot test for naive cooperators  
   Otherwise play D  
  Else  
   // There was at least one cooperator within the last m rounds, but not in t−1  
   Play D  

3.  Pseudocode  

```
function aggressive_PGG_action(t, history):
    if t == 1 or t == r:
        return D

    last_coop = count of “C” in history[t-1] by other players
    if last_coop >= 1:
        // Exploit any recent cooperator
        return D

    // No one cooperated in t−1
    // Check last m rounds for any cooperation
    cooperation_found = false
    for k in 1..m:
        if count of “C” in history[t-k] ≥ 1:
            cooperation_found = true
            break

    if not cooperation_found:
        // Probing phase
        if random() < ε:
            return C
        else:
            return D
    else:
        // Cooperators faded out but were present recently → stay defect
        return D
```

4.  Strategy rationale and “aggressive” mindset  

•  Defection-first: By defecting in round 1, you immediately cement an exploiter reputation.  
•  Exploit cooperators: Any round in which you see ≥ 1 cooperator last turn, you defect to grab the extra public-good share.  
•  Punish defectors = ignore them: You never reward defection with cooperation.  
•  Probe rarely: If the group has gone all‐D for m rounds, you “test” for latent cooperators with tiny probability ε.  This can coax a naive cooperator into playing C, whom you will then exploit next turn.  
•  Unforgiving in final round: No matter what happened before, you defect in round r.  

Such a policy maximizes your one‐period gains whenever cooperators are present, punishes or starves pure defectors by never giving them the public good back, and continually searches for new exploitation opportunities without ever risking serious losses.
'''

description_AGGRESSIVE_98 = '''
Below is a simple yet maximally aggressive strategy for the repeated N-player public‐goods game.  It never gives up an opportunity to free‐ride or to punish anyone daring to cooperate.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy Name: “Always‐Defect Aggressor”  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

1.  Decision rules  
    For every round t = 1…r, play D (Defect).  
    •  Never play C, under any history.  
    •  No threshold, no trigger, no testing phase.  

2.  Edge cases  
    •  First round (t=1): Defect.  
    •  Last round (t=r): Defect.  
    •  Regardless of what others have done in any previous round, always choose D.  

3.  Aggressive rationale  
    •  By never contributing you always pocket the private payoff of 1 plus your share of any public good others create.  
    •  You systematically punish any cooperative impulse in the group (there is no “reward” for cooperators since you will always defect).  
    •  You maximize your own payoff in each single shot (defection strictly dominates cooperation when k<n) and you refuse to provide the seed of trust that could sustain group cooperation.  

Pseudocode  

    function decide_action(history, t, n, k, r):
        return D  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation  
Since k<n, contributing (C) costs you 1 but only returns k/n<1 to you; defection (D) yields 1 plus whatever others contribute.  In repeated play there is no credible way for cooperators to deter an unconditionally defecting agent, so “Always‐Defect” both maximizes your round‐by‐round payoff and suppresses any public‐goods formation.
'''

description_AGGRESSIVE_99 = '''
Below is a fully specified, “aggressive” free-rider strategy for the n-player public-goods game.  It treats any sign of cooperation as an opportunity to exploit, never sacrifices for the group, and uses occasional “probes” to discover new cooperators.

1.  High-level description  
   •  Name: Predator  
   •  Mindset:  Always defect against the group.  If anyone ever cooperates, switch into permanent exploit mode (continuous defection).  If the group never cooperates, send occasional cooperation “probes” to tempt them—then exploit.  
   •  Goal:  Maximize own sum of payoffs by capturing the public-good share whenever possible.  

2.  States and parameters  
   •  exploitable (boolean flag), initially false  
   •  M = max(2, ⌈r/10⌉)  (probe interval)  

3.  Decision rules by round t (1 ≤ t ≤ r)  
   a.  If t = 1 or t = r, action = D  (always defect in first and last round)  
   b.  Else if exploitable = true, action = D  (once we know there are cooperators, permanently defect)  
   c.  Else (exploitable = false and 1 < t < r):  
       i.  If (t mod M) = 0, action = C  (probe for new cooperators)  
      ii.  Else if last round had any cooperators (Σ c_j at t–1 > 0):  
            •  Set exploitable = true  
            •  Action = D  (exploit immediately)  
     iii.  Else, action = D  (no cooperators last round, and not probing)  

4.  Pseudocode  

   initialize exploitable ← false  
   compute M ← max(2, ceil(r/10))  

   for t in 1…r do  
     if t = 1 or t = r then  
       play D  
       continue  
     end if  

     if exploitable = true then  
       play D  
       continue  
     end if  

     if t mod M = 0 then  
       play C     // probe  
       continue  
     end if  

     // inspect last round  
     let lastCoops ← Σ_j c_j(history at t–1)  
     if lastCoops > 0 then  
       exploitable ← true  
       play D     // exploit any cooperators seen  
     else  
       play D     // default defection  
     end if  
   end for  

5.  Why this is aggressive  
   •  Never sacrifices own endowment for the public good except in calculated, rare probes.  
   •  The moment any player cooperates, switches to full-blown defection to capture k/n×contributions.  
   •  Endgame defection ensures no exploitable turn-on-turn cooperation at the last round.  

This strategy maximizes your personal payoff by aggressively exploiting any cooperative behavior in the group and otherwise remaining a free-riding defector.
'''

description_AGGRESSIVE_100 = '''
Below is a fully specified “aggressive” or “rug-pull” strategy for the repeated n-player public goods game.  It tries to build just enough trust to induce contributions from others, then defects ruthlessly to exploit them.  Edge‐cases (small r), first and last rounds, and on‐the‐fly punishments are all handled.

───  
Strategy name: Aggressive Rug-Pull  

Parameters (computed once at start):  
• n: number of players  
• r: total rounds  
• P = max(1, ⌊r/3⌋)             ← length of “trust‐building” phase  
• Q = min(r, 2·P)               ← end of “test” phase  
• betrayed = false             ← flag: someone has defected against us in phase 1  

Decision rule for round t (1 ≤ t ≤ r):

1.  If t = r (the very last round), play D.  
    (No future to punish, so always defect.)

2.  Else if t ≤ P (Phase 1: Trust-building) then  
     a.  If betrayed = false, play C.  
     b.  If betrayed = true, play D (we have already been betrayed—switch to all-out defection).  
     c.  After observing the *others’ actions* at the end of this round, if any opponent played D while we played C, set `betrayed = true.`  

3.  Else if P < t ≤ Q (Phase 2: Testing & exploitation) then  
     If betrayed = true:  
         • play D (we already know they won’t honor trust).  
     Else (betrayed = false):  
         • Let Oₜ₋₁ = number of opponents (i≠ us) who played C in round t−1.  
         • If Oₜ₋₁ ≥ ⌈(n−1)/2⌉, play C (they still cooperate, so we keep luring).  
         • Otherwise play D (they are defectors or too few cooperators ‑ switch to exploitation early).  

4.  Else (t > Q; Phase 3: All-out defection): play D.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  

```
betrayed ← false
P ← max(1, floor(r/3))
Q ← min(r, 2*P)

for t in 1…r do
  if t == r then
    action[t] ← D
  else if t ≤ P then
    if not betrayed then
      action[t] ← C
    else
      action[t] ← D
    end if
  else if t ≤ Q then
    if betrayed then
      action[t] ← D
    else
      // count opponents’ Cs in previous round
      O ← sum_{j≠i} (action_{j,t-1} == C ? 1 : 0)
      if O ≥ ceil((n-1)/2) then
        action[t] ← C
      else
        action[t] ← D
      end if
    end if
  else
    // Phase 3
    action[t] ← D
  end if

  // execute action[t], then observe others
  if t ≤ P and action[t] == C then
    for each j≠i do
      if action_{j,t} == D then
        betrayed ← true
      end if
    end for
  end if
end for
```

Rationale and aggressiveness:

• First P rounds we “signal” cooperation—unless someone defects on us, in which case we flip the switch and never cooperate again.  
• In the next P rounds we only cooperate if a clear majority cooperated in the immediately preceding round—otherwise we switch to full defection early.  This tests opponents’ willingness to reciprocate.  
• In the final third of the game, and in the last round in particular, we always defect to maximize short-run gains (last-round defection is dominant).  
• The design ensures that any attempt by others to build toward full cooperation is ruthlessly exploited once we have sufficient evidence of trust or once the trust-building window closes.

This “rug-pull” is aggressively aligned with self-interest: it lures cooperators, punishes early defectors, tests for sustained cooperation, and then defects universally to harvest the public good without further contributions.
'''

description_AGGRESSIVE_101 = '''
Below is an “aggressive” public‐goods strategy we’ll call Ultimate Exploiter.  Its core idea is simple: if there is any exploitable cooperation in the last round, defect to reap the benefit; if everyone defected last round (so the public fund is dry), cooperate once to refill it (and create new exploitation opportunities).  We always defect in the final round to deny future payback and maximize our one‐shot gain.

1. Notation  
 n = total players  
 r = total rounds  
 t = current round (1 ≤ t ≤ r)  
 c_i(t) ∈ {0,1} = contribution of player i in round t (1 if C, 0 if D)  
 you = index of this strategy  

2. Parameters  
 No tunable parameters beyond the game inputs (n,r).  

3. Decision rule  
 If t = r:  
  – action ← D  // last‐round defection (end‐game defect)  
 Else if t = 1:  
  – action ← C  // initial cooperation to test for any cooperators  
 Else (2 ≤ t ≤ r−1):  
  let S = Σ_{j≠you} c_j(t−1)  // how many others cooperated in the previous round  
  if S ≥ 1 then  
   action ← D // exploit any available cooperation  
  else  
   action ← C // replenish public good when everyone else defected  

4. Rationale / aggressiveness  
 • By defecting whenever any cooperator exists, you seize the highest private return k/n · (#C) + 1 from that round.  
 • By “giving” a single cooperation only when everyone else defected, you ensure the group‐pot is replenished—creating future chances to exploit.  
 • By defecting in the final round, you avoid any last‐round reciprocation and lock in a one‐shot gain.  

5. Pseudocode  

```
function UltimateExploiter(history, t, n, r):
    # history: list of past rounds; each entry is a list of contributions c_1..c_n
    if t == r:
        return D
    if t == 1:
        return C
    # otherwise 2 ≤ t ≤ r−1
    last_round = history[t-2]         # zero‐based indexing
    S = sum(last_round[j] for j in all players if j != you)
    if S >= 1:
        return D
    else:
        return C
```

6. Edge‐case handling  
 • First round (t=1): cooperate once to detect any willingness to contribute.  
 • Intermediate rounds: exploit any prior cooperation; if the public good is empty, refill it.  
 • Last round (t=r): defect unconditionally (no future rounds remain to punish you).  

This strategy aggressively free‐rides on cooperators while sustaining just enough cooperation in the pool to keep exploiting others round after round, and it guarantees a final‐round defection for maximal end‐game payoff.
'''

description_AGGRESSIVE_102 = '''
Below is a fully‐specified “ruthless” strategy that never lets others profit off you, punishes any cooperative overture, and—if you really want—does a one–round “coop test” to see who’s naïve before you exploit them for the rest of the game.

Strategy name: Aggro-Grim with One-Shot Test

1. State variables  
   • tested (boolean) – have we done our one cooperation‐test yet?  
   • everCooperated (boolean) – has any opponent ever contributed in any prior round?

2. High-level description  
   • Round 1: Defect.  
   • Round 2: If you want to identify who cooperates, play C exactly once (tested=false). Otherwise just defect.  
   • From round 3 to round r–1:  
       – If everCooperated==true ⇒ Defect forever (exploit and punish cooperators).  
       – Else ⇒ Defect (stay in defection equilibrium).  
   • Round r (last round): Defect (backwards‐induction).  

3. Why it is aggressive  
   • It never rewards cooperators—once you see any C, you switch to permanent defection and reap the higher payoff from their contributions.  
   • It punishes hopeful cooperators harshly and immediately.  
   • It never lets the group “trap” you into a cooperation equilibrium.  

4. Edge cases  
   • First round: no history ⇒ defect unconditionally.  
   • Last round: defect by backward induction (no future to punish).  
   • If you skip the “test” (set tested=true immediately), this reduces to Always-Defect.  

5. Pseudocode

```
Input: n, r, k          # game parameters
Initialize:
  tested ← false
  everCooperated ← false

for t in 1…r do
  if t == 1 then
    action ← D

  else if t == r then
    # Last round: always defect
    action ← D

  else
    # Any cooperation seen in past?
    if everCooperated == true then
      # Permanent punishment/exploitation
      action ← D

    else
      # No one has ever cooperated so far
      if tested == false then
        # One‐shot test: try cooperating to see who else does
        action ← C
        tested ← true
      else
        action ← D
      end if
    end if
  end if

  # Execute action and observe others’ contributions c_j,t
  Observe contributions {c_j}   # c_j=1 if j played C, else 0
  if ∑_{j≠i} c_j > 0 then
    everCooperated ← true
  end if

  # (Payoffs are computed externally per the game rules)

end for
```

Variants:  
– To remove even that single test, simply initialize tested=true; you will then defect in every round and never cooperate at all.  
– To be even more “in your face,” you can skip any test and just set everCooperated=true if you ever see a C—even if it was you—so you immediately switch to “grim” defection.  

This strategy ensures you never squander your endowment on public goods and that any player naïve enough to contribute at all gets exploited in every subsequent round.
'''

description_AGGRESSIVE_103 = '''
Below is an “Aggressive Exploiter” strategy.  Its core is: “never miss an opportunity to exploit cooperators, never trust too long, and always defect in the last round.”

1.  High-level description  
   – First and last round: always defect (no future to leverage or punish).  
   – In intermediate rounds:  
       •  If anyone cooperated in the immediately preceding round, you defect to free-ride.  
       •  If nobody cooperated last round, you still defect most of the time, but with a tiny “probe” chance ε you cooperate—just to see if someone will start cooperating so you can exploit them next turn.  

2.  Decision rules  
   Let t = current round (1 ≤ t ≤ r), H_{t−1} = history of contributions in round t−1, coop_{t−1} = number of cooperators in round t−1, ε = small probe probability (e.g. 0.05).  

   if t == 1:  
       play D  
   else if t == r:  
       play D  
   else:  
     if coop_{t−1} ≥ 1:  
         play D   ← exploit any cooperators immediately  
     else:  
         with probability ε  play C   ← “probe” for new cooperators  
         else               play D  

3.  Edge-cases and parameters  
   – First round (t=1): defect unconditionally; there is no history to exploit.  
   – Last round (t=r): defect unconditionally; there is no future punishment or reward.  
   – Single “all-defect” equilibrium: if everyone is defecting, our occasional probes (ε) may entice a cooperator; as soon as that happens we switch right back to defection and profit.  
   – Choice of ε trades off exploration (find exploitable cooperators) vs guaranteed baseline payoff; keep ε small (e.g. 0.01–0.1).  

4.  Pseudocode  
```
function AggressiveExploiter(t, history, ε):
    # t: current round index (1…r)
    # history: list of past rounds; each entry is a vector of c_j ∈ {0,1}
    if t == 1:
        return D
    if t == r:
        return D
    # compute how many cooperated in last round
    coop_prev = sum(history[t-1])      
    if coop_prev >= 1:
        # immediate exploitation
        return D
    else:
        # no one cooperated last round: probe with small prob ε
        if random_uniform_0_1() < ε:
            return C
        else:
            return D
```

5.  Why “aggressive”?  
   – You never “reward” cooperation; you only punish or exploit it.  
   – You always defect in the final round, removing any incentive for others to trust you.  
   – You actively seek out exploitable cooperators by rare probes, then switch back to defection immediately.  
   – No forgiveness, no long-run alliance—pure opportunism.
'''

description_AGGRESSIVE_104 = '''
Below is a self‐contained “aggressive” strategy we’ll call Lure-and-Klepto.  Its logic is simple:  
–  We never gamble repeatedly on cooperation.  We offer one tiny “lure” of cooperation to see if anybody will be nice, then defect forever and exploit that one round of good will.  
–  At the end of the game (last one or two rounds) there is no future to protect, so we defect there too.  

Strategy name: Lure-and-Klepto

Parameters needed: r (number of rounds), choose one lure round ℓ=2 (you can shift to ℓ=3 if you prefer).   

1.  First round (t=1): Defect.  
2.  Lure round (t=ℓ): Cooperate.  
3.  Exploit and punishment phase (t=ℓ+1 through r): Defect.  

Special cases:  
–  If r=1: only one round ⇒ t=1 is also last ⇒ defect.  
–  If r=2: set ℓ=2 (the last round is the lure), but since there is no “next” round to exploit, simply defect both rounds.  

Why this is aggressive:  
•  We never become a long-term cooperator or build any reputation for forgiving.  
•  We incur exactly one risk (the single lure), and only if others cooperate do we reap an above-baseline payoff in the very next round by defecting.  
•  If nobody ever cooperates on our lure round, we lose nothing beyond that one round, and then defect permanently, guaranteeing ourselves the “always-defect” floor payoff.  

Pseudocode  

```
Inputs:   r  // total number of rounds (r ≥ 1)
Constants:
   LURE = min(2, r)       // if r=1 ⇒ LURE=1; if r≥2 ⇒ LURE=2

For each round t = 1 to r do:
   if r == 1 then
      // Only one round, no opportunity to exploit future
      action[t] = D
   else if r == 2 then
      // Two rounds: lure is round 2 but no subsequent exploit possible
      action[t] = D
   else
      // r ≥ 3
      if t == 1 then
         action[t] = D      // Open by defecting
      else if t == LURE then
         action[t] = C      // Single cooperation to test/entice
      else
         action[t] = D      // Exploit or simply never cooperate again
      end if
   end if
end for
```

Explanation by phase  
–  Rounds 1: we defect to establish that we are not a naïve cooperator.  
–  Round 2 (the “lure”): we cooperate once.  If any of our opponents cooperate back, they have given us a public-good bonus we can exploit.  
–  Rounds 3…r (including the last two rounds): we defect unconditionally, both to punish would-be cooperators and to capture the free-riding share of any public contributions.  

Edge-case behavior  
•  Very short games (r=1 or 2) collapse to “always defect” since there is no meaningful future in which to exploit.  
•  Long games (r≫2) still contain exactly one lure and then permanent defection, so we never risk more than a single cooperative move.  

This strategy guarantees you at worst the always-defect payoff each round (π=1) except for one round you “lost” by cooperating.  If any opponent buys your one-round cooperation by playing C as well, you earn an extra payoff k/n × (#cooperators) in the very next round when you defect.  That is an aggressive, risk-limited exploitation of any cooperative tendency in the field.
'''

description_AGGRESSIVE_105 = '''
Below is an “aggressive” public‐goods strategy we’ll call Sneaky‐Exploit.  In essence it (1) defects by default; (2) occasionally “baits” pure defectors into trying cooperation; and then (3) whenever any cooperation is observed, it permanently switches back to full defection.  It also never cooperates in the final two rounds (because there is no future to exploit).

Parameters you can tune:
• ε (small, e.g. 0.05): the probability of a one‐off “bait” cooperation when the group has so far been all‐defect.  
• R_punish = 2: number of last rounds in which we always defect.  

Notation:
• t = round number, 1 ≤ t ≤ r  
• hist_t–1 = history up to (and including) round t–1  
• C_count(t–1) = total cooperators in round t–1  

Strategy description

1. First two rounds are treated normally; but in the last R_punish rounds we always defect (no baiting).

2. We maintain a flag Punished = false initially.  Once we ever see C_count(t–1) > 0, we set Punished = true and from then on we defect forever.

3. In any round t (not in the last R_punish rounds) where Punished = false and C_count(t–1) = 0, we “bait” with probability ε (i.e. cooperate to try to seed a project), otherwise defect.  But if ANYONE ever cooperated last round, we immediately switch to Punished = true and defect.

Pseudocode

```
Initialize:
  Punished ← false
  R_punish ← 2        # number of rounds at end where we always defect
  ε ← small (e.g. 0.05)

For each round t = 1…r do:
  if t > r – R_punish:
    # Final rounds: always defect
    play D
    continue

  if t == 1:
    # First round: start aggressively by defecting
    play D
    continue

  # For t > 1 and not in final punishment window:
  if Punished == true:
    play D
    continue

  # Examine what happened in the previous round
  if C_count(t–1) > 0:
    # We caught someone cooperating → punish forever
    Punished ← true
    play D
    continue

  # Nobody cooperated last round
  # Baiting step: random probe to try to spark cooperation
  with probability ε:
    play C
  else:
    play D
```

Explanation of the “aggressive mindset”  
1. Default Defection.  Defection is dominant in one‐shot.  By default we defect every round.  
2. Bait‐and‐Switch.  If the entire group is pure‐defecting so far (no one cooperated last round), we risk a tiny ε‐prob cooperation to see if anyone else is looking for mutual gain.  If someone bites and cooperates, we immediately punish by defecting from then on, thus harvesting a higher payoff on all future rounds.  
3. Grim Punishment.  Once you detect any cooperation, you switch permanently into full‐defection mode (“Punished = true”).  This punishes altruists and signals to everyone that further cooperation will be futile.  
4. End‐game Defection.  In the last R_punish rounds there is no “future” to exploit, so we simply defect unconditionally.  

This strategy will:  
– Ensure you never lose by cooperating unilaterally (you only cooperate when the group was all‐defecting, so at worst you forgo the private 1 for a tiny ε risk).  
– Occasionally trigger a cooperation wave and then defect to extract the maximum (k/n)·(#cooperators) + 1 payoff.  
– Punish any cooperative behavior so cooperators learn you are untrustworthy.  
– Guaranteed to defect in the last rounds, so you cannot be exploited in the end‐game.
'''

description_AGGRESSIVE_106 = '''
Below is an “aggressive‐exploiter” strategy we’ll call DefectorBaiter.  It uses one round of “bait” cooperation (to lure the group into high contributions) and then defects relentlessly—including in the last round—so as to maximize personal payoff and punish any cooperators.

1.  Overview of the Mindset  
    - Be prepared to sacrifice at most one endowment in order to unlock much larger free‐rides later.  
    - Never forgive or return to cooperation once you start defecting.  
    - Always defect in the final round (no future to punish you).  

2.  Decision Rules  

   Let r be total rounds, t the current round (1 ≤ t ≤ r).  
   Let H_t–1 = history of contributions up through round t–1.  
   Let C_{t–1} = total # of cooperators in round t–1 (i.e. Σ c_j in t–1).  

   a.  Round 1 (t = 1):  
       – Action: Cooperate (C)  
         • This single “bait” encourages the group to add more to the public pot if they are willing to cooperate.  

   b.  Rounds 2 ≤ t < r (intermediate rounds):  
       – Action: Defect (D) unconditionally.  
         • You exploit any cooperators in round 1 (and beyond), capturing 1 + (k/n)×(C_{t–1}) each round.  
         • You do not attempt to re‐cooperate or signal remorse.  

   c.  Last round (t = r):  
       – Action: Defect (D).  
         • No future punishment possible, so always defect.  

3.  Handling Edge Cases  
   – If r = 2: Round 1 you cooperate (bait), Round 2 you defect—straightforward.  
   – If opponents never cooperate in round 1 (C₁ = 1 solely you), you still gain only (k/n) from your own bait; but because you never devote more than one endowment, your loss is minimal.  
   – No need for randomization—deterministic “1 × C then all D” suffices to exploit any cooperators.  

4.  Why It’s Aggressive  
   – You give up at most one unit of private payoff in exchange for the chance to free‐ride on many more across r–1 rounds.  
   – You never “forgive” or “reward” cooperation after round 1; any player who cooperates even once empowers you to exploit them.  
   – You always defect in the last round, cementing your maximum short‐term gain without risk of reciprocation.  

5.  Pseudocode  

   initialize:  
     history ← empty  
   for t in 1..r do  
     if t == 1 then  
       play C  
     else  
       play D  
     end if  
     observe contributions of all players this round, append to history  
   end for  

That’s it.  DefectorBaiter is simple, unrelenting, and maximizes your free‐riding payoff against any group‐contributing opponents.
'''

description_AGGRESSIVE_107 = '''
Aggressive–“Greedy Exploiter with Probing”–Strategy  
-------------------------------------------  

Overview  
•  We will play almost exclusively D (defect), punishing any sign of cooperation in our opponents.  
•  When all other players have been pure defectors for a while, we will “probe” by cooperating once in a while to see if anyone bites—then immediately punish.  
•  In the very first round and in the final rounds (where punishment can’t be credibly threatened), we always defect.  

1.  Notation  
   t        = current round (1 … r)  
   prev_C   = number of cooperators among opponents in round t–1  
   r        = total rounds  
   P_probe  = probe interval (for example ⌈r/10⌉)  
   T_safe   = number of initial “no-question” defect rounds (set T_safe = 1)  
   T_end    = number of final rounds where we must always defect (set T_end = 2)  

2.  Decision Rules  

– Rounds we always defect (D):  
   •  t ≤ T_safe (first round), or  
   •  t > r – T_end (last T_end rounds), or  
   •  prev_C > 0 (someone cooperated last round → immediate punishment)  

– Probing cooperation (C):  
   •  If none cooperated in the previous round (prev_C = 0), AND  
   •  t mod P_probe = 0, AND  
   •  t ≤ r – T_end,  
   then play C (probe).  

– Otherwise defect (D).  

3.  Pseudocode  

```
Inputs: r, P_probe ← max(1, ceil(r/10)), T_safe ← 1, T_end ← 2
for t in 1..r do
    if t ≤ T_safe then
        action[t] ← D      # Always defect in round 1
    else if t > r – T_end then
        action[t] ← D      # Always defect in final T_end rounds
    else if prev_C > 0 then
        action[t] ← D      # Punish any cooperative move from last round
    else
        # No one cooperated last round
        if (t mod P_probe = 0) and (t ≤ r – T_end) then
            action[t] ← C  # Probe for cooperation
        else
            action[t] ← D  # Otherwise stay defecting
        end if
    end if
end for
```

4.  Handling Edge Cases  
•  First round (t=1): we have no history → defect.  
•  Rounds t = 2 … T_safe: prev_C refers to round 1’s cooperators (always zero, but we already force defect).  
•  Probing near the end: we stop probing when t > r – T_end so as not to give “free” cooperation that can’t be punished.  
•  If we probe and someone cooperates, in the very next round (if it’s not the final T_end) we will detect prev_C>0 and revert to all-out D.  

5.  Why This Is Aggressive  
•  We never grant unpunished cooperation. Any sign of “nice” behavior by an opponent is met with immediate, permanent defection (until the final rounds).  
•  We only give occasional one-off opportunities (“probes”) when the field is “cold” to see if there’s something to exploit—but the moment anyone cooperates we slam the door shut.  
•  In the final rounds, when future punishment is impossible, we never cooperate, extracting every last unit privately.  

This strategy maximizes personal payoff by:  
1.  Exploiting any cooperating opponents.  
2.  Minimizing the amount of public good we contribute.  
3.  Ensuring that no cooperative streak ever lasts long enough to build mutual gains.
'''

description_AGGRESSIVE_108 = '''
Below is a self-contained “Ruthless Tester” strategy that aggressively destroys any incipient cooperation while still “testing” for cooperators just often enough to exploit them before turning to permanent defection.  In English it says:  
  • 1) Start by cooperating until you find at least one cooperator,  
  • 2) as soon as anybody cooperates even once, switch to permanent defection,  
  • 3) always defect in the very last round.  
This way you lure in conditional cooperators, milk them for one or more rounds, then go full D forever—maximizing your own payoff at their expense.

-----------

1.  State variables  
   triggered  ∈ {false, true}  
     –  false means “we’re still probing for cooperators.”  
     –  true means “we caught someone cooperating—go pure defection forever.”

2.  Action rule (for each round t = 1…r):  
   if t == r:  
     action ← D  
   else if triggered == true:  
     action ← D  
   else if t < r:                      ← we’re still probing  
     if t == 1:  
       action ← C                     ← initial test in round 1  
     else                              ← in rounds 2…r–1  
       look at histories c_j(t–1) for all j ≠ you  
       if ∃ j : c_j(t–1) == 1 then     ← someone cooperated last round  
         triggered ← true              ← “we’ve found cooperators—flip to D forever”  
         action ← D  
       else  
         action ← C                   ← no one cooperated yet, keep probing  

3.  Pseudocode  

```
Initialize:
  triggered ← false

For each round t = 1 to r do
  if t == r then
    Play D
  else if triggered == true then
    Play D
  else
    if t == 1 then
      Play C
    else
      // t in 2..(r-1), still probing
      Let coopers ← { j ≠ me : last_round_action(j) == C }
      if coopers ≠ ∅ then
        triggered ← true
        Play D
      else
        Play C
      end
    end
  end
end
```

4.  Explanation of behavior and edge‐cases  
  – Round 1: we “probe” by cooperating once.  
  – Rounds 2…(r–1): if nobody has cooperated in the previous round, we keep probing (C) to see whether any strategy is conditionally cooperative.  If at any point we see even one other player contribute (c_j = 1), we flip `triggered = true` and from that round on we defect.  
  – Round r: by construction we always defect (no future to exploit).  
  – Once `triggered` is true, we never return to cooperation.  

5.  Why “aggressive”?  
  – We deliberately invite cooperators to reveal themselves by briefly cooperating.  
  – The first time someone else cooperates, we never forgive—or give back—nor do we attempt any “tit-for-tat” niceties.  We simply switch to permanent defection and free-ride on their sunk contributions in that very round, then extract the highest possible private payoff thereafter.  
  – By enforcing a last-round defection as well, we ensure we never leave “gift” payoffs on the table.  

This strategy will systematically undermine any cooperating opponents, maximizing short- and long-run exploitation with zero forgiveness.
'''

description_AGGRESSIVE_109 = '''
Below is an “aggressive” two‐phase strategy—call it Hunter–Exploiter—that (1) never hesitates to defect, (2) actively probes the population for naïve cooperators, and (3) once cooperators are found, defects relentlessly (including the last round).  

1.  State variables  
    •  phase ∈ {HUNT, EXPLOIT} – your current mode  
    •  ε – a small probe probability (e.g. 0.1)  
2.  Initialization  
    phase ← HUNT  
3.  In each round t = 1…r do:  
    A.  If t = 1 or t = r then  
          action ← D  
        (Always defect on first and last rounds.)  
        Continue to next round.  
    B.  Let last_coops = number of players j ≠ i who chose C in round t−1.  
    C.  Update phase:  
        if phase = HUNT and last_coops > 0 then  
            phase ← EXPLOIT  
    D.  Choose action:  
        if phase = EXPLOIT then  
            action ← D  
        else  (phase = HUNT and last_coops = 0)  
            with probability ε: action ← C  
            otherwise:          action ← D  
4.  Intuition and aggressive mindset  
    –  HUNT mode: you are fishing for exploitable cooperators. You mostly defect but with a small “probe’’ cooperation chance ε.  If nobody cooperates you keep probing.  
    –  As soon as any opponent ever cooperates in your previous round, you switch to EXPLOIT mode.  
    –  EXPLOIT mode: you defect forever (including round r) to reap the full benefit of others’ contributions while never giving anything back.  
    –  You never return to cooperation once you’ve detected a single cooperator.  

Pseudocode  
----------  
```
epsilon ← 0.1
phase   ← HUNT

for t in 1…r:
  if t = 1 or t = r:
    play D
    continue

  last_coops ← count of opponents who played C in round t−1
  if phase = HUNT and last_coops > 0:
    phase ← EXPLOIT

  if phase = EXPLOIT:
    play D
  else:  # still in HUNT and no one cooperated last round
    if rand() < epsilon:
      play C
    else:
      play D
```

Edge cases  
–  If nobody ever cooperates, you remain in HUNT and keep probing at rate ε.  Probes return low payoffs, but you’re never exploited.  
–  The moment you see a single cooperator, you switch to permanent EXPLOIT, ensuring you free‐ride on any future contributions.  
–  By defecting in the last round, you avoid any end‐game goodwill and lock in maximum private payoff.
'''

description_AGGRESSIVE_110 = '''
Aggressive Public‐Goods “Grim‐Last‐Shot” Strategy

Overview  
This is a memory‐one plus “last‐round” strategy that (1) promises cooperation only as long as everybody else has never deviated, (2) exploits full‐group cooperation once, then (3) defects forever—especially in the last round.  It is “aggressive” in that it (a) punishes any hint of non‐unanimous cooperation by defecting permanently, and (b) when full cooperation is on the table, it grabs the highest one‐round payoff by defecting on the very next move (most brutally in the final round).

Notation  
n = total players, r = total rounds  
t = current round (1,…,r)  
c_i(t) ∈ {0,1} = contribution of player i in round t (1 if C, 0 if D)  
H(t–1) = indicator that “in every round 1..t–1, all n players cooperated”  
 i.e. H(t–1)=1 ⇔ ∀s< t, Σ_j c_j(s)=n  

Decision Rules  
1. First round (t = 1)  
 Play C.  
 Rationale: establish a record of full cooperation so that H(1)=1 if and only if everyone followed suit.  

2. Intermediate rounds (2 ≤ t < r)  
 If H(t–1)=1 (meaning no deviation so far) then  
  Play C in round t–1 ⇒ cooperate at t only to build on the “all‐C” history  
 Else  
  Defect forever (play D at t)  

 However, to be maximally aggressive, we will actually defect at the first round in which we observe that in t–1 all n cooperated.  That way we “exploit” the unanimous cooperators and immediately lock in permanent defection going forward.  

 More simply:  
  If H(t–1)=1 AND t<r then  
   Defect at t (exploit the group once) and set H(t)=0 for all future  
  Else  
   Defect at t  

3. Last round (t = r)  
 Always defect.  Even if H(r–1)=1, we use our “last‐shot” to grab the biggest share.

Edge‐Case Handling  
– If r=2, the strategy is: Round 1 cooperate, Round 2 defect.  
– If at any point a single player deviates from C, we never cooperate again (grim trigger).  
– We never “mistakenly” return to C once we’ve defected even once.  

Pseudocode  

```
initialize:
  H = true    // “so far everyone has cooperated”
for t in 1..r:
  if t == 1:
    action[t] = C
  else if t < r:
    if H:
      // Everyone cooperated in all previous rounds
      action[t] = D     // exploit the unanimous cooperators
      H = false         // trigger permanent defection
    else:
      action[t] = D     // we’re already in permanent defection
  else:  // t == r, final round
    action[t] = D       // last‐round defection
  // Update H based on observed history (including our own action)
  observe total_contrib = Σ_j c_j(t)
  if total_contrib < n:
    H = false
endfor
```

Explanation of Aggressiveness  
– “Grim‐Trigger” backbone: Any deviation by anybody ensures we defect forever.  
– “Exploit‐and‐Lock”: The very first time we see that ALL n cooperated, we switch to defection immediately (even before the final round).  
– “Last‐Shot”: Even if we’d maintained full cooperation all the way to round r, we break that cooperation in the final round for maximal one‐round gain.  

This combination ensures that (1) cooperators can be enticed to contribute, (2) they get ruthlessly exploited, and (3) once exploited, we never return to generosity.
'''

description_AGGRESSIVE_111 = '''
Below is a concise description of an “aggressive” public-goods strategy—call it the “Bulldozer.”  It never relinquishes private payoff to build the public pot, it ruthlessly punishes any tentative co-operators, and it ensures you defect in the last round as well.

1. Overview  
   • Type: Pure defection plus explicit “punishment” of cooperators.  
   • Mindset: Maximize your round payoff and minimize others’ incentives to cooperate.  

2. Decision rules  
   Let t = current round (1 ≤ t ≤ r), and let history H record every player’s past moves.  
   Let coop₋prev = number of cooperators among the other n–1 players in round t–1 (zero if t=1).  

   For each round t do:  
     if t = 1 then  
       choose D  // start by defecting, establish a hard line  
     else if 2 ≤ t < r then  
       if coop₋prev > 0 then  
         // someone tried to cooperate last round → punish  
         choose D  
       else  
         // no one cooperated last round → keep defecting  
         choose D  
     else  // t = r, the final round  
       choose D  // end-game defection  

   In words:  
   – First round: defect unconditionally.  
   – Middle rounds: if anyone cooperated in the previous round, continue to defect (punish them); if nobody cooperated, still defect.  
   – Last round: defect (no future to reward cooperation).  

3. Edge-case handling  
   – t=1: coop₋prev is undefined; we default to D.  
   – t=r: always D regardless of history.  
   – If opponents never cooperate, you never switch—you remain an unrelenting defector.  

4. Pseudocode  
```
function BuldozerAction(t, r, history):
    if t == 1:
        return D
    if t == r:
        return D
    // t in [2..r-1]
    coop_prev = count_cooperators(history[t-1], exclude_self = true)
    // punish or stay defect
    return D
```

5. Why it’s aggressive  
   – You never grant the public good.  
   – You explicitly “punish” any attempt at cooperation by refusing to reciprocate, discouraging others from ever cooperating.  
   – You defect even in the final round, maximizing private payoff.  

This strategy is a straightforward, brutally aggressive defector: it leverages the dominant‐strategy nature of D in each one‐shot, adds an explicit punishment signal (never forgives cooperators), and guarantees defection throughout—even in the last period.
'''

description_AGGRESSIVE_112 = '''
Below is a simple yet ruthless “Aggressive Defector” strategy.  At every opportunity it defects, thereby never supplying the public good but always reaping the highest private payoff possible given others’ contributions.  

1.  Decision rule  
   •  In every round t = 1,2,…,r, play D (Defect).  

   You never cooperate, regardless of history.  

2.  Edge‐case handling  
   •  First round (t=1): no history → play D.  
   •  Intermediate rounds (1<t<r): history is irrelevant → play D.  
   •  Last round (t=r): end‐game defection → play D.  

3.  Why it’s aggressive  
   •  You never incur the 1‐point cost of C.  
   •  Whenever any opponent contributes, you exploit them—your payoff is 1 + (k/n)·(number of cooperators) which strictly exceeds theirs.  
   •  You punish both cooperators and defectors alike by keeping the public fund at zero whenever others defect.  

Pseudocode  

  for t in 1…r:  
      action[t] ← D  

No triggers, no forgiveness, no cooperation attempts—just unrelenting defection. This maximizes your round‐by‐round payoff given opponents who ever place a token in the public pot, and it never exposes you to being “suckered” by contributing.
'''

description_AGGRESSIVE_113 = '''
Below is a fully‐specified “aggressive” strategy for the r‐round n‐player public goods game.  It never sacrifices short‐run payoff, it seeks out cooperators so it can exploit them, and it never forgives or supports long‐run cooperation.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
AGGRESSIVE “PROBE‐AND‐EXPLOIT” STRATEGY  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

State variables (maintained across rounds):  
• phase ∈ {PROBE, EXPLOIT} – start in PROBE phase  
• ε – small probing probability (e.g. ε = 0.05)  
• M – exploit‐trigger threshold (e.g. M = 1)  

Interpretation:  
• PROBE: occasionally cooperate in order to detect other cooperators.  
• EXPLOIT: once we have evidence of cooperators, defect every remaining round.  

Parameters you may choose ahead of time:  
• ε ∈ (0,1) – how often we risk “signal” cooperation to test others  
• M ∈ {1,…,n–1} – minimum number of other cooperators in one probe round that triggers permanent exploitation  

Agent’s decision rule for round t = 1,…,r:  

1.  If t == 1 then  
      action ← D  
      (We never “waste” a first round cooperation.)  
2.  Else if t == r (last round) then  
      action ← D  
      (Backward‐induction: no future punishment, so always defect.)  
3.  Else if phase == PROBE then  
     • With probability ε:  
         action ← C   (probe for cooperators)  
       With probability 1–ε:  
         action ← D  
     • After observing the other n–1 players’ moves in this round:  
         let coop_others = number of j ≠ i with c_j = 1  
         if coop_others ≥ M then  
             phase ← EXPLOIT  
         end  
4.  Else if phase == EXPLOIT then  
      action ← D  
      (Permanent defection once we know cooperators exist.)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  

initialize phase ← “PROBE”  
for t in 1..r do  
  if t == 1 then  
    play D  
  else if t == r then  
    play D  
  else if phase == “PROBE” then  
    u ← uniform_random(0,1)  
    if u < ε then  
      play C  
    else  
      play D  
    end  
    wait to see {c_j : j ≠ i} this round  
    coop_others ← sum_{j≠i} c_j  
    if coop_others ≥ M then  
      phase ← “EXPLOIT”  
    end  
  else  // phase == “EXPLOIT”  
    play D  
  end  
end  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Discussion  

1.  Aggressiveness:  
    – You never cooperate in round 1 or round r.  
    – You only risk a tiny ε‐chance of cooperation in intermediate rounds to “fish” for gullible cooperators.  
    – As soon as you detect ≥ M cooperators, you permanently switch to all‐D, harvesting the private bonus 1 – 0 plus your share of their contributions.  

2.  Edge cases:  
    – First round: D for guaranteed immediate payoff.  
    – Last round: D by backward‐induction (no future retaliation).  
    – If no one ever cooperates in your probes, you remain in PROBE and keep defecting with probability 1–ε.  Even your ε‐cooperations are “cheap tests.”  

3.  Parameter choices:  
    – ε small (0.01–0.10) so you rarely give away the public good for free.  
    – M = 1 makes you exploit as soon as you catch a single cooperator. You can raise M if you only want to jump to EXPLOIT when you see a larger “coop pool.”  

This strategy maximizes short‐run earnings, ruthlessly punishes cooperators, never supports a lasting public‐good equilibrium, and fits the “aggressive” mindset required.
'''

description_AGGRESSIVE_114 = '''
Below is an “Opportunistic-Grim” strategy – a highly aggressive trigger strategy that free-rides whenever it can, but punishes any defection by permanently defecting.  It obeys the public-goods payoff structure, makes no out-of-band assumptions about other players, and handles first/last-round edge cases.

1. Intuition  
   • By default we defect (D) and never cooperate unless we see perfect cooperation by all other players in the previous round and have never been “betrayed” before.  
   • The first round and the final round are always defected (end‐game defection).  
   • As soon as any player ever defects, we switch to permanent defection (“grim trigger”).  

2. Decision Rule in Words  
   – Round 1: defect.  
   – Rounds 2 through (r–1):  
       • If in any prior round at least one player defected, play D forever.  
       • Otherwise, if all other (n–1) players cooperated in t–1, play C; else play D.  
   – Round r: defect (last‐round defection).  

3. Why it’s aggressive  
   – It never “wastes” a cooperation on partial cooperation by the group.  
   – It only joins in when it can be sure of a full public‐good multiplier with zero risk.  
   – A single defection by anyone triggers permanent punishment, maximizing the cost to any defectors.  
   – It defects in the last round to avoid end‐game exploitation.  

4. Pseudocode  

```
Inputs:
  n      : number of players
  r      : total rounds
  history: array of length t−1; each entry history[t′] is an array of size n of actions {C,D}
State:
  betrayed = false

Function getAction(t, history):
  if t == 1:
    return D
  if t == r:
    return D
  // Check if trigger has been pulled
  if not betrayed:
    // Scan all past rounds for any defection
    for τ in 1 .. t−1:
      for j in 1 .. n:
        if history[τ][j] == D:
          betrayed = true
          break
      if betrayed:
        break
  if betrayed:
    return D

  // No one has ever defected so far
  // Check cooperation status in the immediate prior round
  // Count cooperators in round t−1
  coop_count = 0
  for j in 1 .. n:
    if history[t−1][j] == C:
      coop_count += 1

  // We know we have history[t−1][i] (our own last action):
  // others_coop = coop_count − (history[t−1][i] == C ? 1 : 0)
  my_last_was_C = (history[t−1][i] == C)  // false in t=2 because we defected in t=1
  others_coop = coop_count - (my_last_was_C ? 1 : 0)

  if others_coop == n-1:
    return C
  else:
    return D
```

5. Explanation of Key Lines  
  • We keep a single Boolean `betrayed` that flips to true if any D is ever observed.  
  • If `betrayed` is true, we defect forever after the first defection.  
  • Only if no one has ever defected do we check last round’s cooperators: we cooperate only if *all* the other n−1 players cooperated.  
  • We always defect in the very first and very last round.  

This strategy will aggressively exploit any pockets of full cooperation (by joining in only when guaranteed a high public‐good return) and will ruthlessly punish any defection with permanent defection, ensuring maximum deterrence.
'''

description_AGGRESSIVE_115 = '''
Below is a fully specified “aggressive” strategy we’ll call Seeding-then-Exploitation (STE).  Its high-level idea is:

  1. In the very first few rounds, “seed” by cooperating so that if there are any conditional cooperators in the group you draw them out.  
  2. As soon as you detect a willingness to cooperate, switch to permanent defection and ride free on whatever public good they continue to provide.  
  3. If nobody ever cooperates, fall back to almost‐always defect (with very occasional probes to see if the group can be rattled into cooperating).  
  4. Always defect in the last round (backward‐induction).  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
PSEUDOCODE  

Inputs (common knowledge):  
 n = number of players  
 r = total rounds (>1)  
 k = multiplier (1<k<n)  

Parameters (fixed constants of this strategy):  
 seedRounds = min(3, r−1)  
 probeInterval = 5      // when no one ever cooperates, we still occasionally test  
 exploitThreshold = 1   // if we see ≥1 other coop in seeding, we exploit  

Internal state:  
 phase ∈ {SEED, EXPLOIT, PROBE}  
 – start in SEED if r>3; else go PROBE immediately.  

History tracking:  
 othersCoopCount = total number of cooperators among the other n−1 players during SEED  

Strategy at each round t = 1…r:  

  if t == r then  
    action ← D   // last‐round defection by backward induction  
    return action  

  if phase == SEED then  
    action ← C  
    observe how many of the other n−1 players played C this round; add to othersCoopCount  
    if t == seedRounds then  
      if othersCoopCount ≥ exploitThreshold then  
        phase ← EXPLOIT  
      else  
        phase ← PROBE  
      end  
    end  
    return action  
  end  

  if phase == EXPLOIT then  
    // Permanent defection to exploit any continuing cooperators  
    action ← D  
    return action  
  end  

  if phase == PROBE then  
    // If the group never cooperated in SEED, we defect almost always  
    if t mod probeInterval == 0 then  
      action ← C   // test whether any others will respond  
    else  
      action ← D  
    end  
    return action  
  end  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Explanation of the key elements:

1. First seedRounds (up to 3) rounds: you cooperate no matter what.
   • If at least one other player ever cooperates during these rounds, you conclude there are exploitable cooperators → switch to EXPLOIT.  
   • If nobody cooperates, you assume the group is pure defection → switch to PROBE.  

2. EXPLOIT phase (until the last round): always defect, harvesting any public-good contributions that others unwisely continue to make.

3. PROBE phase (until the last round): almost always defect, but every probeInterval rounds you cooperate once to test whether you can still bait a cooperator; if you succeed, you immediately switch to EXPLOIT in the next round.

4. Last round (t == r): always defect, since no future punishment or reward is possible.

This strategy is “aggressive” because:
  • You offer cooperation only as a lure.  
  • As soon as you detect even a single cooperator, you permanently defect.  
  • You exploit cooperating opponents relentlessly until the terminal round.  
  • If the group is entirely unresponsive, you remain defect‐heavy, probing only occasionally so as not to waste too many endowments.
'''

description_AGGRESSIVE_116 = '''
Below is a self‐contained, aggressive “trigger‐and‐exploit” strategy for the n-player repeated public goods game.  It never shies away from defection, punishes cooperators, and even attempts to lure groups into cooperating before extracting maximal gain.  

1. High-Level Description  
– Initial stance: Start by defecting.  You assume everyone else is out to get you, so you do the same.  
– Punishment: The instant anybody in the previous round has cooperated, you defect (you punish “soft” cooperators).  
– Exploitation lures: If—against all odds—the entire group has cooperated for two rounds in a row, you “blink” a cooperation once to lull them into a false sense of security, and then you defect the very next round to harvest the largest possible payoff from their unanimous cooperation.  
– Last round: Because there is no future to punish or exploit, you defect outright.  

2. Decision Rules in Plain English  
• Round 1: Defect.  
• Rounds 2 through r–1:  
  – If you are currently in an “exploit” subphase, defect and exit that subphase.  
  – Else if the last two full rounds were unanimous cooperation (all n players chose C), enter “exploit” subphase by cooperating this round.  
  – Else if any player cooperated in the immediately preceding round, defect (continuous punishment).  
  – Otherwise, defect (default stance).  
• Round r: Defect unconditionally.  

3. Edge Cases  
– If r = 2, you never see two consecutive unanimous‐C rounds, so you simply defect in both rounds.  
– If at any point you enter the “exploit” subphase on round t (because rounds t–2 and t–1 were all C), you play C on t and immediately defect on t+1; after that you revert to normal punishment/defection logic.  
– If the group never achieves back-to-back unanimous C, you never even attempt the exploit “bait.”  

4. Pseudocode  

```
Inputs:
  n      // number of players
  r      // total rounds
  history[1..r][1..n]  // history[t][j] ∈ {C,D} for each player j in each past round
State variables:
  exploit_phase = false

Function AggressiveAction(t):
  // Round 1: always defect
  if t == 1:
    return D

  // Last round is final – no future left
  if t == r:
    return D

  // Exploit subphase: you cooperated last round as bait, now defect to reap high payoff
  if exploit_phase == true:
    exploit_phase = false
    return D

  // Check for two consecutive unanimous cooperations in t-2 and t-1
  if t >= 3:
    allCoop_t2 = (for all j: history[t-2][j] == C)
    allCoop_t1 = (for all j: history[t-1][j] == C)
    if allCoop_t2 and allCoop_t1:
      // Enter exploit subphase: play C now, defect next
      exploit_phase = true
      return C

  // Punish any lone cooperators: if anyone cooperated last round, defect
  anyCoop_t1 = (exists j: history[t-1][j] == C)
  if anyCoop_t1:
    return D

  // Default stance: defect
  return D
```

5. Why It’s Aggressive  
– It never forgives or reciprocates cooperation permanently.  As soon as anybody cooperates, you go back to defection.  
– It actively tries to tempt a naïve group into mutual cooperation (via the two‐round‐all‐C trigger), only to strike at the peak of their trust.  
– In the final round, you seize the one last opportunity for individual gain with no regard for future retaliation.  

This strategy maximizes private payoff, punishes any cooperative overtures by others, and even seeks to exploit unusually cooperative groups at exactly the moment of highest return.
'''

description_AGGRESSIVE_117 = '''
Below is a fully specified “aggressive” strategy for the n-player repeated public-goods game.  It punishes any sign of cooperation by opponents, “tests” only when no one else is cooperating, and never forgives once it detects cooperation.

Strategy name:  Aggressive Defector with Grim Trigger and Random Testing (ADGT-RT)

Variables maintained  
• punish ← false  
• test_prob ← small constant in (0,1), e.g. 0.05  

Decision rule (for player i):

1.  Initialization (before round 1)  
    punish ← false  

2.  Every round t = 1,2,…,r do:

    if t = 1 then  
       action_i ← D  
       continue to next round  
    end if

    if punish = true or t = r then  
       /* Either we’ve triggered punishment, or it’s the final round */  
       action_i ← D  
       continue to next round  
    end if

    /* Inspect last round’s history */  
    let coop_count ← number of players (including i) who played C in round t–1  

    if coop_count > 0 then  
       /* Someone cooperated last round → trigger permanent punishment */  
       punish ← true  
       action_i ← D  
    else  
       /* No one cooperated last round → we may “test” cooperation */
       with probability test_prob do  
         action_i ← C   /* small random probe */  
       else  
         action_i ← D  
       end with
    end if

3.  End loop

Explanation of key design choices  
– Always start by defecting.  
– Grim trigger: as soon as any player cooperates in any round, set punish=true and thereafter defect forever (including the last round).  This ensures any cooperator is ruthlessly exploited.  
– Random testing: if no one else cooperated last round, we sometimes (with small probability) cooperate ourselves to see if opponents will chase the public-good payoff.  If they do, we detect it next round and punish.  This prevents opponents from “locking in” full defection while still giving us opportunistic exploits.  
– Last‐round defect: in round r there is no future to threaten, so we defect for a safe private payoff.  

Edge cases handled  
• First round (t=1): defect.  No history to inspect.  
• Last round (t=r): regardless of all flags, defect.  
• If at any point coop_count>0, we switch into an absorbing “always-defect” mode.  

Why this is aggressive  
– It maximizes exploitation: every time opponents cooperate, you unconditionally defect and reap the amplified public-good benefit.  
– It never forgives: a single slip by any opponent triggers permanent defection.  
– It prevents coordinated all-D lock-in by occasionally testing cooperation, then punishing it harshly.  
– In the final round you always defect, guaranteeing you cannot be exploited.
'''

description_AGGRESSIVE_118 = '''
Below is a simple “aggressive” strategy—call it Aggressor—which never cedes any benefit to others and in effect punishes any attempt at cooperation by exploiting it.  It (1) always defects, (2) punishes cooperators by continuing to defect, and (3) never “forgives,” including in the first and last round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy Name: Aggressor  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

1.  State and History  
    •  No internal state beyond observing past actions of all players.  
    •  History H_t = {c_j,₁…c_j,t–1 : j=1..n} is available at the start of round t.  

2.  Decision Rule  
    For every round t = 1…r, do:  
      play D (Defect).  

    In words:  
      –  Round 1: Defect.  
      –  Every subsequent round: Defect, regardless of what anyone did before.  

3.  Edge Cases  
    –  First round: Defect (never cooperate “to test the waters”).  
    –  Last round: Defect (no end-game cooperation).  
    –  No forgiveness: Even if all n–1 opponents cooperated in t–1, you continue to defect in t.  

4.  Pseudocode  

    function AggressorMove(t, history H_t):  
        // history H_t is ignored—always defect  
        return D  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Rationale:  
– Defection is a weakly dominant one‐shot action.  
– By never cooperating, you never give up 1 unit of private payoff.  
– By refusing to “forgive” cooperators, you eliminate any chance they can establish mutual cooperation.  
– This maximizes your individual payoff each round (π_i ≥ 1) and prevents others from ever gaining the mutual‐cooperation bonus.
'''

description_AGGRESSIVE_119 = '''
Below is an “all‐out aggressive” strategy that guarantees you never leave value on the table.  In a standard n-player public-goods game with 1<k<n, defection (D) is a dominant action in the single shot; carrying that through every round yields the highest guaranteed payoff regardless of what others do.

1.  Decision rule  
    •  In every round t=1…r: play D (Defect).  

2.  Edge‐case handling  
    •  First round (t=1): defect.  No history—still defect.  
    •  Intermediate rounds (1<t<r): defect, irrespective of history.  
    •  Last round (t=r): defect (backward‐induction ensures no future retaliation).  

3.  Mindset / justification  
    –  You never contribute the 1 point cost.  
    –  If others ever cooperate, you still defect and pocket your 1 plus your share (k/n)·(# cooperators), which strictly beats cooperating.  
    –  You maximize your worst‐case payoff (1 each round) and exploit any cooperators.  

Pseudocode  
-----------  
Inputs:  
  n (players), k (multiplier), r (rounds)  
  history C[t][i] = whether player i cooperated in round t (not used here)  

for t in 1…r:  
    action[t] = D  

return action  

That’s it—defect every round.  No triggers, no forgiveness phases, no wasted signals.  You guarantee yourself a payoff of 1 each round (plus any spill‐over from others’ cooperation), and you never fall victim to free‐riders.
'''

description_AGGRESSIVE_120 = '''
Below is a fully‐specified, “aggressive” exploitation strategy we’ll call the Sniper-Exploit strategy.  It spends most of the game defecting, but periodically “snipes” by cooperating exactly once after observing prolonged universal defection—luring any hopeful cooperators into contributing and then immediately reverting to defection.  In the final few rounds it defects unconditionally to avoid giving away the end‐game.  

1.  Data structures and parameters  
   •  D_count ← 0              // number of consecutive rounds so far in which everyone (all n players) defected  
   •  just_sniped ← false      // flag meaning “we just cooperated on the last move”  
   •  D_trigger ← 3            // after 3 straight all‐D rounds, we perform one cooperation to snare cooperators  
   •  L ← ⌈√r⌉                 // last-phase length: in the last L rounds we defect always  

2.  High‐level decision rule for round t = 1…r  
   if t > r – L then  
       play D   // end-game: never cooperate in the last L rounds  
   else if just_sniped = true then  
       play D   // immediately revert to defection after our single lure cooperation  
   else if D_count ≥ D_trigger then  
       play C   // snipe: cooperate exactly once to lure potential cooperators  
       just_sniped ← true  
   else  
       play D   // default: defect  

3.  History‐update after observing everyone’s actions this round  
   if (every player’s action this round = D) then  
       D_count ← D_count + 1  
   else  
       D_count ← 0  
   end if  
   // clear the snipe flag if we didn’t just use it  
   if just_sniped = true and we played D this round then  
       just_sniped ← false  
   end if  

4.  Edge cases and remarks  
   – First round t=1: D_count = 0 < D_trigger and just_sniped = false → we defect.  
   – After three unanimous‐defection rounds D_count hits 3 → next round we cooperate once.  
   – If that single cooperation meets any cooperator, we exploit in the very next round by returning to full defection.  
   – The last L = ⌈√r⌉ rounds are pure defection so as not to “throw away” end‐game payoffs.  
   – Choice of D_trigger=3 and L=⌈√r⌉ can be tuned; the core idea is long defection to build frustration, one cooperation to test/exploit, then immediate defection again.  

Pseudocode  

```
initialize D_count ← 0
initialize just_sniped ← false
set D_trigger ← 3
set L ← ceil(sqrt(r))

for t in 1…r do
    if t > r – L then
        action ← D
    else if just_sniped then
        action ← D
    else if D_count ≥ D_trigger then
        action ← C
        just_sniped ← true
    else
        action ← D
    end if

    // submit action and observe all players’ actions this round
    let everyone_defected = (for all j, action_j == D)

    // update history
    if everyone_defected then
        D_count ← D_count + 1
    else
        D_count ← 0
    end if

    if just_sniped and action == D then
        just_sniped ← false
    end if
end for
```

Why this is aggressive  
– It defects almost always, maximizing private payoff and free‐riding whenever others do decide to cooperate.  
– By “sniping” (cooperating only after a long stretch of universal defection), it tempts any naïve cooperators into contributing—which the strategy then immediately exploits.  
– It punishes end‐game generosity by refusing to cooperate in the final critical rounds.  

Against a population of more “nice” or forgiving strategies this approach will pluck cooperative contributions at infrequent, surprise intervals, while otherwise securing the maximal defect payoff.
'''

description_AGGRESSIVE_121 = '''
Below is a self‐contained “aggressive” strategy—call it the Opportunistic Exploiter (OE)—for the N-player public goods game.  OE’s high‐level idea is: in the very early rounds it “tests” and “lures” cooperators by occasionally contributing, but as soon as it detects enough goodwill (or simply when enough early rounds have passed), it switches forever to full defection, including in the last round, to extract maximum private benefit.

1.  Parameter choices (you can tune these for your tournament):  
    • coop_phase_max = max(1, ⌊r/4⌋)  
      – the maximum number of rounds OE will spend in the “cooperation‐luring” phase.  
    • coop_threshold = ⌈0.75·(n–1)⌉  
      – if OE sees at least this many other cooperators in the previous round, it decides it has lured enough.  

2.  State variables:  
    • phase ∈ {SEEK, EXPLOIT}  
      – SEEK: we are still luring; EXPLOIT: we permanently defect.  
    • t: current round index (1 … r)  
    • coop_prev: number of other players who cooperated in round t–1  

3.  Decision rules:

For each round t = 1 … r do:

  if t == r then  
    action ← D  
    /* Last round is always defect. */

  else if phase == SEEK then  
    if t == 1 then  
      action ← D  
      /* Test the water: see how many “naïve” strategies immediately cooperate. */  
    else  
      action ← C  
      /* Lure cooperators by showing willingness. */

    /* After observing others’ moves in round t (i.e. setting coop_prev): */
    if coop_prev ≥ coop_threshold  
       OR t ≥ coop_phase_max  
    then  
      phase ← EXPLOIT  
      /* We have either lured a big enough camp or used up our lobby budget. */

  else /* phase == EXPLOIT and t < r */  
    action ← D  
    /* Permanent defection to reap all private gains. */

4.  Edge‐case handling:

  • Very short games (r < 4): coop_phase_max becomes 1, so we only lure in round 2 at most, then exploit.  
  • If nobody ever cooperates early (coop_prev stays below threshold), we still switch to EXPLOIT once t reaches coop_phase_max.  
  • In the final round (t = r) we always defect, regardless of phase.  
  • We never return to SEEK once in EXPLOIT—no forgiveness, no coordination.  

5.  Why it’s aggressive:

  • It never rewards long‐term cooperation.  It invests a tiny “lure budget” early, solely to identify and recruit naïve cooperators.  
  • As soon as it’s worthwhile—either by detecting a cooperating majority or by exhausting its early‐round patience—it goes all‐out defect to maximize its private payoff each remaining round.  
  • No punish‐then‐forgive cycles, no endgame cooperation.  When in EXPLOIT, it extracts maximal advantage at every opportunity.

Pseudocode summary:

```
initialize:
  coop_phase_max  = max(1, floor(r/4))
  coop_threshold  = ceil(0.75*(n-1))
  phase = SEEK

for t in 1..r:
  if t == r:
    play D
    continue

  if phase == SEEK:
    if t == 1:
      play D             // test
    else:
      play C             // lure cooperation

    // after seeing others’ actions in round t:
    coop_prev = number of other players who chose C

    if coop_prev >= coop_threshold or t >= coop_phase_max:
      phase = EXPLOIT

  else:  // phase == EXPLOIT and t < r
    play D               // permanent defection
```

This strategy will exploit any opponents who try to establish mutual cooperation and will never be “pulled back” into contributing once it switches to exploitation. In a tournament with a mix of cooperative‐leaning and defect‐leaning opponents, Opportunistic Exploiter tends to harvest their public‐good contributions and then retreat to pure defection, maximizing its cumulative payoff.
'''

description_AGGRESSIVE_122 = '''
Below is a simple yet maximally aggressive strategy: “Always-Defect.”  It never gives up private endowments, free-rides on any cooperator, and punishes cooperation by withholding your contribution in every round.

1.  Name  
    Aggressive Always-Defect (AAD)

2.  Intuition  
    •  You maximize your private payoff each round (choosing D nets you 1 plus your share of any public good).  
    •  You never cooperate, so you never subsidize others.  
    •  If any opponents attempt cooperation, you exploit them (you still defect and collect (k/n)×#cooperators).

3.  Decision Rule  
    For each round t = 1…r:  
      play D (Defect)

4.  Edge Cases  
    •  First round (t=1): Defect.  
    •  Last round (t=r): Defect (no future to reward).  
    •  Any round regardless of history or observed cooperators: Defect.

5.  Pseudocode  
    function AAD_Strategy(t, history):  
      # history is unused—strategy ignores past plays  
      return D

6.  Why this is aggressive  
    •  Never sacrifices private gain.  
    •  Always denies cooperators the benefit of mutual contribution.  
    •  Simple, un-forgiving, and cannot be “tricked” into cooperating.

You will receive payoff π_i,t = 1 + (k/n)×(number of others who cooperated) each round, and you never lose by contributing. This is the most straightforward “attack” on any group of cooperators.
'''

description_AGGRESSIVE_123 = '''
Below is a self‐contained description of an “Aggressive Opportunistic Free-Rider” (AOF) strategy.  It is designed to (1) punish any cooperator immediately, (2) occasionally inject cooperation so as to lure conditional cooperators back into the pool, and (3) defect unconditionally in the final rounds.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Strategy Intuition  
   • We want to exploit any cooperation by opponents by defecting as soon as they cooperate.  
   • If everyone defects, we “plant” a lone cooperation seed to tempt reciprocators into rebuilding cooperation, which we will then again exploit.  
   • In the very last rounds, no future threat or lure is possible, so we defect unconditionally.  

2. Parameters  
   Input:  
     n = number of players  
     r = total rounds (r > 1)  
   State variables (updated each round t):  
     coop_count_{t–1} = number of *other* players who cooperated in the previous round  

3. Decision Rule (per round t = 1, 2, …, r)  
   if t ≥ r – 1:  
     // “End-game”: no future to exploit  
     play D  
   else if t == 1:  
     // Kick off by “seeding” cooperation  
     play C  
   else:  
     if coop_count_{t–1} > 0:  
       // Someone cooperated last round ⇒ exploit them now  
       play D  
     else  
       // No one cooperated last round ⇒ inject cooperation to lure them  
       play C  

4. Pseudocode  
   initialize t ← 1  
   loop while t ≤ r:  
     if t ≥ r – 1 then  
       action ← D  
     else if t == 1 then  
       action ← C  
     else  
       if coop_count_{t–1} > 0 then  
         action ← D  
       else  
         action ← C  
     end if  
     execute(action)  // Simultaneous move with others  
     observe coop_count_t  // Count of opponents’ C this round  
     t ← t + 1  
   end loop  

5. Handling Edge Cases  
   • First round (t=1): We cooperate to create an opening for future exploitation.  
   • Last two rounds (t = r–1 or r): We defect unconditionally, because there is no longer any possibility of future punishment or lure.  
   • If at some point *everybody* defects (including us), we inject a lone C so that any conditional cooperator in the field has an incentive to start cooperating again—only to be exploited in the very next round.  

6. Why It’s Aggressive  
   – Immediate Punishment: Any sign of cooperation by opponents is *immediately* met with defection.  
   – Luring: We never allow permanent collapse of cooperation; instead we “bait” cooperators back in order to harvest a larger payoff.  
   – End-game Defection: We strip away any last vestige of reciprocity when it can no longer be reciprocated.  

This strategy maximizes short‐run exploitation of conditional cooperators while ensuring that in every round we either punish or prepare to re-punish them. It requires only the observable history of how many others cooperated in the previous round and makes no assumptions about any off‐equilibrium coordination devices.
'''

description_AGGRESSIVE_124 = '''
Below is a single‐strategy description we call “Half-Cooperate-Then-Betray.”  It is explicitly aggressive: it tries to lure out other people’s cooperations in the first half of the tournament, then defects permanently to extract the maximum free-riders’ surplus.  It also immediately switches to defection if it ever sees a defection, so it never sits out a sucker’s loss beyond the first round.

1.  Definitions and parameters  
   •  r = total number of rounds (known in advance)  
   •  H = ⌈r/2⌉  (half the game, rounded up)  
   •  history[t][j] ∈ {C,D} = action of player j in round t  

2.  State variables  
   •  mode ∈ {COOP_PHASE, DEFECT_PHASE}  
      –  start in mode = COOP_PHASE  

3.  Decision rule for round t = 1…r  

   if mode == COOP_PHASE then  
     •  If t > H, switch to DEFECT_PHASE.  
     •  Else if t > 1 and ∃ j≠me such that history[t−1][j] == D, switch to DEFECT_PHASE.  
   end  

   if mode == COOP_PHASE then  
     action ← C  
   else  // DEFECT_PHASE  
     action ← D  
   end  

4.  Explanation of phases  
   – COOP_PHASE (rounds 1 through H unless “punished” early):  
     •  I cooperate to boost the public pot, hoping the “nice” or tit-for-tat players around me also cooperate, so that when I defect later I reap a large (k/n)·(#pliers cooperating) each turn.  
     •  But if I ever see someone defect, they’ve signaled they will not repay, so I switch immediately to DEFECT_PHASE to stop being a sucker.  

   – DEFECT_PHASE (from the switch point through round r):  
     •  I always defect, harvesting 1 + (k/n)·(#cooperators) each remaining round.  
     •  Against purely cooperative strategies this maximizes my haul.  Against always-defecters or early punishers it ensures I never lose further ground.  

5.  Edge cases  
   •  First round (t=1):  
     – mode=COOP_PHASE, no previous‐round defection to see, and t≤H ⇒ play C.  
   •  Rounds up to H:  
     – If everyone else played C in round t−1, continue cooperating.  
     – If anyone defected in round t−1, switch immediately to DEFECT_PHASE and D from now on.  
   •  At t=H+1 (even if no defection so far):  
     – Forced switch to DEFECT_PHASE and play D for the rest of the game.  
   •  Last round (t=r):  
     – mode must be DEFECT_PHASE (either by H cutoff or earlier punishment), so play D.  

6.  Why it is aggressive  
   – It does not seek mutual, sustained cooperation.  Its sole goal is to extract as much public-good benefit as possible.  
   – It lures cooperators into building a large pot for the first half of the match.  
   – In the second half, it defects relentlessly to free-ride on others’ contributions.  
   – It cuts off immediately if it ever encounters defection, so it never continues to be exploited.  

Pseudocode summary  
```
initialize mode = COOP_PHASE
H = ceil(r/2)

for t in 1..r:
    # Check for switch conditions
    if mode == COOP_PHASE:
        if t > H:
            mode = DEFECT_PHASE
        else if t > 1 and exists j≠me with history[t-1][j] == D:
            mode = DEFECT_PHASE

    # Choose action
    if mode == COOP_PHASE:
        play C
    else:
        play D
```

This strategy will be entered into a tournament of unknown opponents.  It is aggressive in that it tries to milk cooperators for half the tournament, then defects forever, and it never tolerates being exploited more than one round.
'''

description_AGGRESSIVE_125 = '''
Below is a self-contained “aggressive exploiter” strategy.  In plain English it simply never cooperates, thus always free-rides on anyone who does.  Because the one-shot dominant action is D (defect) whenever k<n, and because we want to maximize relative payoff by exploiting any cooperators in the group, we never deviate.

1. Name  
   Aggressive Exploiter (AE)

2. Decision rule  
   For every round t=1…r: play D.

3. Edge‐case handling  
   • First round (t=1): no history ⇒ play D.  
   • Intermediate rounds (1<t<r): regardless of what you or they did before ⇒ play D.  
   • Last round (t=r): there is no future to punish, and defection is the one-shot best reply ⇒ play D.

4. Why “aggressive”?  
   • We never incur the private cost of cooperation.  
   • If any opponent cooperates, we get a share of their contribution without paying ourselves.  
   • We “punish” any cooperative impulse by refusing to reciprocate, deterring future cooperation by lowering group payoffs.  

5. Pseudocode

   function AE_action(round t, history H):  
       // history H is a list of all past joint actions  
       // We ignore H entirely because we always defect  
       return “D”

That’s it.  No matter the parameters n, k, or r (as long as k<n so that D is the one-shot best response), Aggressive Exploiter defects every round, maximizes its private take, and exploits any cooperators in the group.
'''

description_AGGRESSIVE_126 = '''
Below is a self-contained “aggressive bully” strategy for the N-player repeated public-goods game.  Its core idea is:  
 1.  Default to Defect (D) so you never unilaterally give away payoff.  
 2.  If you ever see another player Cooperate (C), you exploit them by continuing to Defect.  
 3.  But every now and then you “test” by cooperating yourself (on your own initiative) to see if there are naïve cooperators to exploit.  
 4.  In the very last round you always defect (no future to invest in).  

—  
STRATEGY DESCRIPTION  

Parameters you choose (tunable constants):  
•  p_test ∈ (0,1): small probability of “testing” cooperation when no one cooperated last round (e.g. 0.1)  
•  r: total number of rounds  

State you track: just the full history of actions (yours and everyone else’s) so far.  

At the start of each round t = 1…r do:  
 1.  If t == r (the last round):  
       action ← D  
       (No point in cooperating in the last round—no future to exploit.)  

 2.  Else (t < r), look at round t–1:  
     Let othersCoop ← true if any of the other n–1 players played C in round t–1; false otherwise.  

     a.  If othersCoop == true:  
           action ← D  
         (Punish/exploit cooperators—never grant them the share advantage in the very next round.)  

     b.  If othersCoop == false:  
           With probability p_test:  
             action ← C    (a probing move to lure out cooperators)  
           Otherwise:  
             action ← D  

 3.  Play action, observe everyone’s moves, append to history, and continue.  

—  
PSEUDOCODE  

    function AggressiveBully(t, history, p_test, r):
        # history[t−1] holds the vector of length n of actions in the previous round 
        if t == r:
            return D
        if t == 1:
            # no history yet → treat as “no one cooperated last round”
            othersCoop = false
        else:
            othersCoop = (exists player j ≠ me such that history[t−1][j] == C)

        if othersCoop:
            return D
        else:
            if rand() < p_test:
                return C
            else:
                return D

—  
WHY THIS IS “AGGRESSIVE”  
• You default to D, so you never give away the private endowment unless you have a clear exploitation motive.  
• You punish any sign of cooperation immediately by never reciprocating, thus deterring “nice” strategies that try to build mutual cooperation.  
• You inject occasional C’s on your own schedule (with probability p_test) purely to discover and then exploit cooperators; you never cooperate because you expect reciprocity.  
• You always defect in the last round, squeezing out any last-round advantage.  

Edge cases:  
• Round 1 has no history → othersCoop is false → you cooperate only with probability p_test (a “probe”).  
• Last round (t=r) → guaranteed defection.  
• If your probes never hit any cooperators, you will play D almost every round, guaranteeing the safe “all-D” payoff of 1 per round.  
• If there are cooperators, you will detect them (with prob. ≥1 – (1–p_test)^T over T rounds) and then exploit them relentlessly.  

By mixing in just enough “probes” you maximize the chance of finding exploitable cooperators, while the ever-present threat of punishment (permanent D until history “cools off,” plus last-round D) keeps the group from ever settling on sustained cooperation.
'''

description_AGGRESSIVE_127 = '''
Below is a fully specified “aggressive” strategy for the N-player repeated public‐goods game.  In words, it is a near‐always‐defect policy that (1) never lets a cooperator go unpunished, (2) occasionally “tests” the group to see if anyone will cooperate (so that it can exploit them), and (3) otherwise never contributes—even in the last round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
AGGRESSIVE “GRIM‐TESTER” STRATEGY  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

State variables (kept across rounds):  
• punish_mode ← false  
• test_rounds ← a small set of “probe” rounds, e.g. every ⌈r/10⌉th round (but never round 1 or r).  
  Example: M ← max(2,⌈r/10⌉); test_rounds ← {M,2M,3M,… ≤ r–1}.  

On each round t (1 ≤ t ≤ r), given history of everyone’s contributions so far:

1.  If punish_mode = true         → play D  
2.  Else if t = 1 or t = r        → play D  
3.  Else if t ∈ test_rounds       → play C   (a “probe” to lure cooperators)  
4.  Else                            → play D  

Immediately after observing the joint action in round t (i.e. seeing how many cooperated):

5.  If punish_mode = false and (number of cooperators in round t) ≥ 1 then  
        punish_mode ← true  
   (Once you see even one cooperator, you enter punish_mode forever.)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Rationale and properties  
1.  Aggression: You never willingly contribute except in the designated test rounds.  The moment anyone else contributes you switch to permanent defection (“grim trigger”).  
2.  Exploitation: On each test round you cooperate once—if others join you, you catch them in your trap the very next round by punishing them forever.  Each C they pay is leveraged to raise the public good, which you then share from while they pay the full cost.  
3.  No naïve generosity: Outside test rounds you default to D, including round 1 (no opening gift) and round r (no end‐game illusion).  
4.  Parameter tuning: The density of test_rounds (e.g. every r/10 rounds) can be adjusted.  Fewer probes mean fewer “wasted” contributions but also fewer chances to detect unsuspecting cooperators.  
5.  Edge cases:  
   – r = 2 or very small r: test_rounds will be empty; the strategy reduces to “always D.”  
   – If nobody ever cooperates, punish_mode stays false—but you still play D every non–test round, so your payoffs remain optimal.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  

```
function AggressiveGrimTester(t, history, n, r):
    # history is a list of length t-1, each element a list of n bits c_j ∈ {0,1}
    static punish_mode ← false
    # Precompute test rounds once:
    static M ← max(2, ceil(r/10))
    static test_rounds ← {k*M | k=1,2,…, k*M < r}

    # 1. If already punishing → defect
    if punish_mode:
        return D

    # 2. Always defect in first or last round
    if t == 1 or t == r:
        return D

    # 3. Probe rounds: cooperate to lure
    if t in test_rounds:
        return C

    # 4. Default otherwise
    return D

# After observing the actions in round t:
function update_after_round(t, history):
    global punish_mode
    coopers ← sum(history[t-1])  # number of players who contributed in this round
    if not punish_mode and coopers >= 1:
        punish_mode ← true
```

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

This strategy is aggressively defect‐leaning, immediately punishes any hint of cooperation and so maximizes your own payoff while suppressing the group’s ability to form public goods.
'''

description_AGGRESSIVE_128 = '''
Below is a fully “aggressive” strategy—call it Aggressive-Defector—that never gives up private payoff for the group and relentlessly exploits any cooperator.  In this game, since k/n<1, defection strictly dominates cooperation in every single round; an aggressive mindset simply “free-rides” every time.

1.  Decision rule  
    • In every round t (1 ≤ t ≤ r), play D (Defect).  
    • Never cooperate, regardless of history.

2.  Edge‐case handling  
    – First round (t=1): no history yet ⇒ defect.  
    – Intermediate rounds: ignore past actions; defect.  
    – Last round (t=r): with no future to influence, still defect.

3.  Rationale (aggressive mindset)  
    – By defecting you retain your private endowment (1 unit) and still capture a share of whatever others contribute.  
    – You never sacrifice 1 unit to cooperate, so you always earn at least as much as any cooperator in the same profile.  
    – You exploit unconditional or naive cooperators, and you cannot be “punished” by strategies that only respond to cooperation, since you never cooperate.

4.  Pseudocode

    function AggressiveDefector(round t, history H):
        # history H is the list of past action‐profiles; we ignore it
        return “D”   # always defect

    # Tournament loop for i’s r rounds:
    for t in 1..r:
        observe nothing (or H)
        a_i[t] = AggressiveDefector(t, H)
        # play a_i[t] simultaneously, update H with all players’ actions

That is all.  By never cooperating, you maximize your own payoff in every single round and “punish” any would-be cooperator by reaping the public good without ever contributing yourself.
'''
