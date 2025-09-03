"""
Strategy descriptions for CollectiveRiskDescription.

Generated with:
- Provider: OpenAI
- Model: o4-mini
"""


description_COOPERATIVE_1 = '''
Below is a single‐strategy recipe – “Threshold Tit-for-Tat with Forgiveness” – that seeks to reliably reach the m-cooperator threshold each round (for t < r) while remaining robust to occasional defections.  It cooperates on round 1, defects “rationally” on the last round, and in all intermediate rounds conditions its move on whether the group just succeeded in meeting the threshold.

—  
Strategy name  
  Threshold Tit-for-Tat with Forgiveness  

Parameters you know: n, r, m, k.  
Keep one internal flag: punished (boolean).  

State variables (reset at t = 1):  
  punished ← false  

At the beginning of each round t (1≤t≤r), you observe H_{t−1}, the history of actions and you can count C_{t−1}, the number of cooperators in round t−1.  

Decision rule for round t:

1.  If t = 1  
      Play C  
2.  Else if t = r  
      Play D    // last-round defection is individually dominant  
3.  Else (1 < t < r):  
     Let succ ← (C_{t−1} ≥ m).  
     
     If succ = true then  
       // group succeeded last round  
       punished ← false        // clear any old punishment  
       Play C                  // reward by cooperating  
     Else  
       // group failed last round  
       If punished = false then  
         Play D                // one-time punishment  
         punished ← true  
       Else  
         Play C                // forgiveness, resume cooperation  
       EndIf  
     EndIf  

Pseudocode summary  

  punished ← false  
  For t in 1…r do  
    If t = 1 then  
      a_t ← C  
    Else if t = r then  
      a_t ← D  
    Else  
      succ ← (count_cooperators(t−1) ≥ m)  
      If succ then  
        punished ← false  
        a_t ← C  
      Else  
        If not punished then  
          a_t ← D  
          punished ← true  
        Else  
          a_t ← C  
        EndIf  
      EndIf  
    EndIf  
    play a_t  
  EndFor  

Rationale and cooperative character  
- Round 1: start cooperatively to signal willingness to meet the threshold.  
- Rounds 2…r−1:  
   • If the group cleared the threshold last round, reward by cooperating.  
   • If they failed, defect exactly once (to signal displeasure), then immediately forgive and cooperate again – this minimizes long punitive spirals.  
- Round r: defect (projecting backwards, last‐round cooperation is exploitable).  

This strategy:  
• Promotes reaching m each round by continuously rewarding success.  
• Politely punishes a single failure but forgives at once, thus driving the group back to the cooperative equilibrium.  
• Avoids infinite retaliation chains.  
• Defects in the last round, protecting you against pure last-round free-riding.
'''

description_COOPERATIVE_2 = '''
Below is a fully‐specified cooperative rule set that (i) guarantees exactly m cooperators each round, (ii) shares the “cooperator‐cost” almost evenly over r rounds, and (iii) punishes any deviation by forever reverting to defection.  Because it uses only the publicly known parameters (n, m, r) and each player’s fixed index i, no extra communication is needed.

Notation  
• n, m, r   : as above  
• i          : your (publicly known) player index in {1,…,n}  
• t          : round number, t=1,…,r  
• coopCount  : number of C’s you observe in a round  
• deviated?  : flag you set to true the first time you ever see coopCount≠m  

High‐level idea  
1.  In each round t, exactly the m players whose indices satisfy  
     (i + t – 1) mod n < m  
   cooperate; the rest defect.  That ensures coopCount=m every round.  
2.  If at any point the observed coopCount≠m, set deviated?=true and thereafter defect every remaining round.  

Because every honest player follows the same index‐based “rotating” schedule, exactly m cooperators emerge in every round—and each player cooperates about ⌈r·m/n⌉ or ⌊r·m/n⌋ times, sharing the burden.  Any one shot of mis‐cooperation triggers permanent defection (“grim”), giving everyone a strong incentive to stay on target.

Pseudocode (per player i)

  initialize deviated? ← false

  for t in 1…r do
    if deviated? then
      play D
    else
      // Determine whether i is one of the m “scheduled” cooperators this round
      idx ← (i + t – 1) mod n     // in {0,…,n–1}
      if idx < m then
        play C
      else
        play D
    end if

    // Observe everyone’s actions and count cooperators
    coopCount ← number of players who chose C in this round

    // If we ever see the group miss the target of exactly m, trigger punishment
    if coopCount ≠ m then
      deviated? ← true
    end if
  end for

Explanation of each component

1.  Rotation schedule  
    • By using (i + t – 1) mod n < m you partition the n players into an ordered circle.  
    • In round t you pick the first m positions on that circle.  Over n consecutive rounds each i will occupy each “position” exactly once.  
    • If r is not a multiple of n, the same formula still allocates each player either ⌈r·m/n⌉ or ⌊r·m/n⌋ cooperations.  

2.  Exact threshold fulfillment  
    • In every round (if nobody has yet deviated) exactly m players satisfy idx<m, so coopCount=m and the group earns k every round.  

3.  Sharing the cost  
    • Each cooperation costs 1.  Since total cooperations over r rounds is r·m, and they are distributed evenly by index, no one player bears substantially more than her fair share.  

4.  Deviation detection and punishment  
    • If any round deviates (too few or too many cooperators), everyone switches to D forever.  This “grim” trigger gives a one‐shot deviator the threat of losing the entire sequence of future k‐rewards.  

Handling edge cases  
• First round (t=1): formula picks exactly m cooperators (those with i mod n < m).  No special case needed.  
• Last round (t=r): the same rule applies—players cooperate exactly when (i + r – 1) mod n < m.  Although there is no future to punish, a rational player knows that if she had deviated earlier, she would already be in the punitive “deviated?=true” state.  
• If r<n or r is not a multiple of n: rotation still works, ensuring the fairest possible distribution of the m·r cooperation‐slots across n players.  

Why it’s cooperative  
– It guarantees the public‐goods threshold m every round, so the group never suffers the “all‐defect” or “insufficient” outcome.  
– It evenly shares the small cost of cooperating.  
– The simple grim trigger deters deviation, so there is no incentive to free‐ride or over‐cooperate.  

This strategy is deterministic, transparent, self–enforcing, and maximally cooperative under the common‐knowledge assumptions of the tournament.
'''

description_COOPERATIVE_3 = '''
Below is a fully specified “Conditional Cooperation with Rotating Contribution” strategy.  It (i) guarantees exactly m contributions each round when everyone abides by it, (ii) distributes the “pain” of contributing as evenly as possible, (iii) punishes any deviation by switching to all-defect (“grim trigger”), and (iv) defects in the very last round to avoid end-game exploitation.

--------------------------------------------------------------------------------
1.  PRECOMPUTATION (before round 1)

Let  
 T ← r × m    total contributions required over the r rounds  
 q ← ⌊T/n⌋  
 s ← T mod n  

Thus s players must each contribute q+1 times; the other n–s players contribute q times.

Build a fixed “schedule” of exactly T contribution‐slots over r rounds:
– Create a list L of player indices by repeating each index i exactly (q or q+1) times:
 • If i ≤ s then i appears q+1 times in L  
 • Else i appears q times in L  
– Now L has length T.  Partition L into r contiguous groups of size m:
 Round 1 contributors = L[1..m],  
 Round 2 contributors = L[m+1..2m],  
 …  
 Round r contributors = L[(r−1)m+1..rm].  

Store this as S[t] = “set of m players scheduled to contribute in round t.”

--------------------------------------------------------------------------------
2.  PLAYING RULES

At each round t = 1,2,…,r:

if (t == r) then  
 // Last round: defect unconditionally  
 Action_i(t) ← D  
else if (a “punishment flag” is ON) then  
 // Grim‐trigger phase after any past failure  
 Action_i(t) ← D  
else  
 // Normal phase  
 if (i ∈ S[t])  
  Action_i(t) ← C  
 else  
  Action_i(t) ← D  
end if

After observing everyone’s actions in round t (for t < r):

 If (# cooperators observed in t < m) then  
  Turn punishment flag ON for all future rounds.  
 End if

--------------------------------------------------------------------------------
3.  EXPLANATION & EDGE‐CASE HANDLING

1.  First round  
 – We simply use S[1]; no special case.  

2.  Last round (t = r)  
 – We defect regardless.  Since there are no future rounds, cooperation cannot be enforced and defection strictly dominates.  

3.  Punishment (grim trigger)  
 – The moment any round (before r) fails to reach the threshold m, we switch to all-defect for every remaining round.  
 – This makes unilateral deviation from the schedule self-punishing.  

4.  Fairness of contributions  
 – Exactly T = r×m total cooperations are needed to always meet the threshold.  
 – By distributing these cooperations as evenly as possible (q or q+1 per player), each player bears almost the same total cost.  

5.  Incentive compatibility  
 – As long as everyone sticks to the schedule, every round t<r meets the threshold and yields payoff = (1–c_i)+k.  
  • If i cooperates (c_i=1), payoff = k  
  • If i defects (c_i=0), payoff = 1 + k  
 – Our rotation ensures that over r−1 rounds, each player defects roughly (r−1) – (their scheduled cooperations) times and cooperates exactly when scheduled.  
 – Any unscheduled defection in a normal‐phase round will cause threshold failure ⇒ punishment ⇒ future payoffs drop to 1 per round, which is worse than sticking to the plan.  

--------------------------------------------------------------------------------
4.  PSEUDOCODE

// Precompute  
T ← r * m  
q ← floor(T / n)  
s ← T mod n  
L ← empty list  
for i in 1..n:  
  count_i ← (i ≤ s ? q+1 : q)  
  append index i to L count_i times  
// L now length T  
for t in 1..r:  
  S[t] ← L[(t−1)*m+1 .. t*m]   // the m cooperators for round t  

// Play
punish ← false
for t in 1..r:
  if t == r or punish:
    play D
  else if i ∈ S[t]:
    play C
  else:
    play D

  // After observing outcomes (only if t < r):
  if t < r and (#C observed in round t < m):
    punish ← true

--------------------------------------------------------------------------------

This strategy is:  
– Cooperative (it guarantees the public good each round if no one deviates),  
– Fair (costs shared evenly),  
– Enforceable (grim‐trigger punishes any out-of-schedule defection),  
– Robust in first and last rounds.
'''

description_COOPERATIVE_4 = '''
Below is a fully‐specified “Scheduled Contribution with Grim‐Trigger” strategy.  It (1) guarantees exactly m cooperators in every round if nobody ever deviates, (2) punishes any deviation by permanently reverting to defection, and (3) is fully explicit about first, middle and last rounds.

1.  Pre‐game setup (common knowledge)  
   • Label players by their indices i=1…n.  
   • Agree on a deterministic “rotation schedule” Sₜ⊂{1…n} of size |Sₜ|=m for each round t=1…r.  For instance one can define:  
     Sₜ = { ((t−1)·m + 1) mod n, …, ((t−1)·m + m) mod n }  
     where “x mod n” yields a number in 1…n.  
   • Intuition: exactly m players are “on duty” to cooperate each round; the other n−m defect.

2.  Decision rule at each round t  
   Let Deviated = “in any prior round 1…t−1 there was at least one outcome that did not match the rotation schedule.”  
   Then player i plays:  
     if not(Deviated) and i∈Sₜ  
       → Cooperate (C)  
     else  
       → Defect (D)

3.  Edge-case handling  
   • First round (t=1): Deviated=false by definition, so exactly the m players in S₁ play C; the rest play D.  
   • Intermediate rounds (1<t<r): continue following the rule above.  
   • Last round (t=r): apply the same rule.  Even though there is no “future” punishment beyond round r, scheduled cooperators still prefer C over defecting unilaterally: if exactly m are scheduled to C and everyone else uses the same strategy, a deviant cooperator would cause cooperations to drop to m−1 ⇒ no k‐bonus, so her payoff would be 1 instead of k.  Since k>1, she is better off sticking to C.  
   • Permanent punishment (“grim‐trigger”): as soon as any round t′<t produces a pattern of contributions that differs from exactly S_{t′}, all players switch to D forever after.  

4.  Why it is cooperative and self‐enforcing  
   – If no one ever deviates, each round has exactly m cooperators ⇒ the threshold is met ⇒ every player gets +k that round.  Total group payoff = r·(1+k) for defectors and r·k for cooperators, but rotation makes ex‐ante fairness.  
   – A scheduled cooperator never wants to defect unilaterally: if she breaks from C to D while exactly m−1 other scheduled cooperators stick to C, the project fails and her payoff falls from k down to 1.  
   – A scheduled defector never wants to cooperate unilaterally: she would incur cost (giving up 1) but gain no extra benefit beyond the k that m other cooperators already secure.  
   – Any deviation by anyone triggers permanent defection, punishing all players.  This threat sustains the cooperative schedule in every subgame.  

5.  Pseudocode  

  initialize Deviated ← false  

  for t in 1…r do  
    if history of round (t−1) ≠ exactly “players in S_{t−1} played C, others D” then  
      Deviated ← true  
    end if  

    if not Deviated and i ∈ Sₜ then  
      play C  
    else  
      play D  
    end if  

    observe outcome, append to history  
  end for  

––––––––––––––––––––––––––––––––––––  
This strategy is (i) fully cooperative—if everyone adheres, the threshold is met every round—(ii) fair by rotation, and (iii) self‐enforcing via a simple grim‐trigger punishment.
'''

description_COOPERATIVE_5 = '''
Below is a single‐strategy recipe, called “Generous Threshold‐Triggered Cooperation (GTTC),” that (i) tries to secure at least m cooperators every round, (ii) punishes failures just enough to deter serial defection, (iii) forgives quickly so cooperation can recover, and (iv) remains cooperative even in the last round.

1.  State variables  
    •  prev_C_count ← undefined  (the number of cooperators in t–1)  
    •  punish_timer ← 0           (counts how many rounds of “punish” remain)  

2.  Initialization (before round 1)  
    prev_C_count ← m    (pretend threshold met so we start by cooperating)  
    punish_timer   ← 0  

3.  Per‐round decision (for t = 1…r)  
    a.  If t = 1 then  
          my_action ← C  
        Else if punish_timer > 0 then  
          my_action ← D  
          punish_timer ← punish_timer – 1  
        Else  
          if prev_C_count ≥ m then  
            my_action ← C      (last round was “successful,” so stay cooperative)  
          else  
            my_action ← D      (threshold failed → trigger punishment)  
            punish_timer ← 1   (punish for exactly one future round)  
    b.  If t = r then  
          // override to remain fully cooperative on the very last move  
          my_action ← C  
    c.  Play my_action simultaneously with the others.  
    d.  Observe the total number of cooperators this round → call it this_C_count.  
    e.  prev_C_count ← this_C_count  

4.  Rationale  
   – Start by cooperating in round 1 to give the group the best chance to reach m.  
   – Whenever the group just met the threshold (prev_C_count ≥ m), stay with C.  
   – If the threshold fails (prev_C_count < m), we play one round of D as a mild, one‐round “punishment” to signal that failures have a cost.  
   – After that one round of punishment (punish_timer), we unconditionally return to C, so the group can rebuild cooperation.  
   – In the very last round we unconditionally cooperate (my_action ← C) to avoid wasting the final‐round payoff and to signal full commitment.  

5.  Pseudocode  

    // PARAMETERS: n, m, r, k (k > 1)  
    prev_C_count ← m        // pretend success before round 1  
    punish_timer   ← 0  

    for t in 1…r do  
      if t == 1 then  
        my_action ← C  
      else if punish_timer > 0 then  
        my_action ← D  
        punish_timer ← punish_timer – 1  
      else  
        if prev_C_count ≥ m then  
          my_action ← C  
        else  
          my_action ← D  
          punish_timer ← 1  
      end if  

      // Last‐round override: stay fully cooperative  
      if t == r then  
        my_action ← C  
      end if  

      play(my_action)  
      observe this_C_count  // number of players who played C this round  
      prev_C_count ← this_C_count  
    end for  

This GTTC strategy is:  
• Cooperative–it always tries to meet the threshold and rarely punishes, and even in the last round it lends its full support.  
• Deterring–it does punish a failure for exactly one round, which is just enough to discourage constant free-riding but not so much as to lock the group into permanent defection.  
• Forgiving–after one round of punishment it returns immediately to cooperation, allowing the group to repair.
'''

description_COOPERATIVE_6 = '''
Below is a single‐strategy proposal for a “mostly cooperative” trigger strategy that (i) tries to secure the public good by reaching the m‐cooperator threshold each round, (ii) punishes threshold failures for a short time so as to deter free‐riding, and (iii) “drops out” (defects) in the very last round since cooperation there is strictly dominated.

---  
I. Intuition  
1. First round: signal goodwill by cooperating.  
2. In every round ​t​ (except a short “endgame”), cooperate if in the immediately preceding round at least ​m​ players cooperated.  
3. If the threshold ​m​ was missed in the previous round, enter a short punishment phase (defect for ​P​ rounds) to discipline defectors.  
4. After the punishment phase, return to cooperation (“forgiving”).  
5. In the final round, defect (no future to enforce cooperation).

By doing this, we sustain cooperation in the early and middle rounds, punish isolated mis‐coordination enough to deter defection, but remain forgiving so as not to lock into endless mutual defection.

---  
II. Parameters you must fix once per tournament  
• P  = punishment length (integer ≥1, e.g. 2)  
• L  = endgame length (we use L=1, i.e. defect only in the very last round)

---  
III. State Variables  
• punish_remaining  ∈ {0,1,…,P}  – how many more rounds we must defect in punishment mode  
• round  t  ∈ {1,2,…,r}  

---  
IV. Pseudocode  

Initialize  
  punish_remaining ← 0  

For each round t = 1 to r do:  
  if t > r – L then  
    action ← D     // drop cooperation in the last L rounds  
    continue to next round  
  end if  

  if punish_remaining > 0 then  
    // We are still punishing a past threshold failure  
    action ← D  
    punish_remaining ← punish_remaining – 1  
    continue to next round  
  end if  

  if t = 1 then  
    // First‐round signal of cooperation  
    action ← C  
  else  
    // Observe how many cooperated in round t–1  
    let coop_count_prev = number of players who chose C in round t–1  
    if coop_count_prev ≥ m then  
      // Previous round succeeded in building the public good ⇒ cooperate  
      action ← C  
    else  
      // Threshold failed ⇒ punish for P rounds, starting now  
      action ← D  
      punish_remaining ← P – 1   // we already used 1 this round  
    end if  
  end if  

End for  

---  
V. Discussion of Edge Cases  

1. First round (t=1): We unconditionally cooperate to signal good faith.  
2. Rounds 2…r–L:  
   – If the immediate past round met the threshold, we cooperate; if it failed, we defect for P rounds (punishment).  
   – After P consecutive defections, we “forgive” and return to cooperation, giving the group a chance to rebuild.  
3. Last L=1 round (t=r):  
   – We defect. Since there is no future to enforce, defection strictly dominates.  
4. Continuous failures: If the group continuously misses the threshold, we will cycle through up to P defections and then test cooperation again. In practice this discipline encourages opponents to return to cooperating if they value future gains.  

---  
VI. Why this is Cooperative  

• It “tries first” and rewards any round that meets the m‐cooperator threshold.  
• It only punishes briefly (length P) rather than forever, keeping the door open to renewed cooperation.  
• It avoids the infinite defection trap of a classical Grim Trigger while still maintaining enforcement power.  
• By defecting only in the known final round, it respects the backward‐induction logic yet preserves cooperation as long as enforcement is credible.  

This strategy strikes a balance: it credibly punishes free‐riders, incentivizes reaching the public‐good threshold each round, but remains forgiving enough to restore cooperation after occasional lapses.
'''

description_COOPERATIVE_7 = '''
Below is a fully self-contained “fair-rotation with finite punishment” strategy.  It guarantees that in normal play exactly m players cooperate each round—so the group always earns the bonus—and divides the cost fairly.  Any deviation from the schedule triggers a short, collective punishment phase; at the very end of the game all players defect (to guard against last-round exploitation).

1.  Preliminaries  
    •  Players are indexed 1…n (common knowledge).  
    •  Let r = total rounds.  Fix two small constants:  
       –  P_punish = ⌈r/10⌉ (length of punishment phase)  
       –  P_end = 2 (number of final “endgame” rounds everyone defects)  
    •  We define a rotating coalition of size m:  
       coalitionC[t] = { ((t–1 + j) mod n) + 1 : j = 0,1,…,m–1 }.  
       In round t, exactly those m players “should” cooperate.  

2.  State variables (maintained across rounds)  
    •  mode ∈ {NORMAL, PUNISH, ENDGAME}  
    •  punish_timer ∈ {0,1,…,P_punish}  

   Initialize at round 1:  
     mode ← NORMAL  
     punish_timer ← 0  

3.  Round-by-round decision rule for player i in round t:

   If t > r – P_end then  
      # Last P_end rounds ⇒ we defect to avoid being suckered on round r  
      action_i(t) ← D  
      mode ← ENDGAME  
      next punish_timer (unused)  
      return  

   If mode = PUNISH then  
      # collective punishment  
      action_i(t) ← D  
      punish_timer ← punish_timer – 1  
      if punish_timer = 0 then mode ← NORMAL  
      return  

   # Now mode = NORMAL, and t ≤ r – P_end  
   if t = 1 then  
     # First round, start with the agreed coalition  
     if i ∈ coalitionC[1] then action_i(1) ← C else action_i(1) ← D  
     return  

   # t ≥ 2 in NORMAL mode  
   Observe last round’s history:  
     S_{t–1} ← number of cooperators in round t–1  
     # and check if exactly the scheduled coalition cooperated  
     H_deviation ← (S_{t–1} ≠ m)  
                   or (the set of cooperators ≠ coalitionC[t–1])  

   if H_deviation then  
     # Someone broke the schedule (either too few, too many, or wrong identity)  
     mode ← PUNISH  
     punish_timer ← P_punish  
     action_i(t) ← D  
     return  
   else  
     # No deviation, schedule intact ⇒ participate if in round-t coalition  
     if i ∈ coalitionC[t] then action_i(t) ← C else action_i(t) ← D  
     return  

4.  Explanation of why this is cooperative  
   – During NORMAL play, exactly m players pay the cost (C) each round so the group always wins k.  
   – Everyone carries the same load by rotating the “cooperator” role through coalitionC[1],…,coalitionC[r–P_end].  
   – If anyone deviates (free-rides by D when scheduled to C, or sabotages by C when scheduled to D), the group immediately switches to a short all-D punishment phase of length P_punish.  
     By sacrificing the bonus together for P_punish rounds we deter unilateral deviations.  
   – After punishment we forgive and return to NORMAL scheduling.  
   – In the last P_end rounds everybody defects to avoid being exploited in the very last round (no future punishment possible).  

5.  Pseudocode summary  

  initialize:
    mode ← NORMAL
    punish_timer ← 0

  for t in 1…r do
    if t > r - P_end:
      action ← D
      mode ← ENDGAME
      continue

    if mode = PUNISH:
      action ← D
      punish_timer ← punish_timer - 1
      if punish_timer = 0:
        mode ← NORMAL
      continue

    # mode = NORMAL, t ≤ r - P_end
    if t = 1:
      action ← (i ∈ coalitionC[1] ? C : D)
      continue

    # t ≥ 2
    observe coop_set_{t-1}
    if |coop_set_{t-1}| ≠ m or coop_set_{t-1} ≠ coalitionC[t-1]:
      mode ← PUNISH
      punish_timer ← P_punish
      action ← D
    else:
      action ← (i ∈ coalitionC[t] ? C : D)

  end for

With this strategy each round yields the group bonus in NORMAL mode, burden‐sharing is fair, and any deviation is punished swiftly but finitely—after which cooperation resumes.
'''

description_COOPERATIVE_8 = '''
Below is a memory-1, threshold-trigger strategy (“Threshold-TFT”) that aims to sustain cooperation every round until the endgame, then defects in the very last round (the classic end-game problem).  It is simple, forgiving, and clear about what happens in round 1, in any round when the group just failed, and in round r.  

1.  State variables  
   •  last_success ∈ {true,false}  
      – true if in the previous round the group met the m-cooperator threshold  
      – false otherwise  
   •  punish_counter ≥ 0  
      – a small integer counter (we’ll use punish_counter = 1) that keeps us defecting for exactly one round after a failure  

2.  Initialization (before round 1)  
   last_success := true    (optimistic start)  
   punish_counter := 0  

3.  Per-round decision rule for round t = 1,2,…,r  

   if t = 1 then  
     action := C      (start by signaling willingness to cooperate)  

   else if t = r then  
     action := D      (end-game defection)  

   else  (1 < t < r)  
     if punish_counter > 0 then  
       action := D  
       punish_counter := punish_counter – 1  

     else if last_success = true then  
       action := C      (group succeeded last round, so we keep cooperating)  

     else  
       action := D      (group failed last round, so we punish by defecting)  
       punish_counter := 1  

   end if  

4.  After observing the round’s outcomes (simultaneously with all players):  
   Let coop_count := number of players who played C this round.  
   if coop_count ≥ m then  
     last_success := true  
   else  
     last_success := false  
   end if  

5.  Summary of behavior  
   •  Round 1: Always cooperate.  
   •  Rounds 2…r−1:  
       – If previous round reached the threshold (coop_count ≥ m) and you are not in a punishment stint, play C.  
       – If previous round failed the threshold, defect once (punish_counter=1), then resume cooperating if the next round is a success.  
   •  Round r (last round): Always defect.  

6.  Why it is cooperative  
   – It starts cooperatively and only defects in response to genuine failures to hit m.  
   – Punishment is short (1 round), after which it gives the group another chance.  
   – By cooperating as soon as the group shows success, it reinforces coordination.  
   – The predictable last-round defection is necessary because in a finitely repeated game with no future, defection is weakly dominant in the very last step.  

7.  Pseudocode  

   initialize:  
     last_success ← true  
     punish_counter ← 0  

   for t in 1…r do  
     if t = 1 then                            # first round  
       play C  
     else if t = r then                       # last round (end-game)  
       play D  
     else                                      # intermediate rounds  
       if punish_counter > 0 then  
         play D  
         punish_counter ← punish_counter − 1  
       else if last_success then  
         play C  
       else  
         play D  
         punish_counter ← 1  
       end if  
     end if  

     observe coop_count this round  
     if coop_count ≥ m then  
       last_success ← true  
     else  
       last_success ← false  
     end if  
   end for  

This “Threshold-TFT” is cooperative—it rewards group success with cooperation, punishes failures briefly to deter free-riding, then forgives and returns to cooperation—while being fully specified for round 1, rounds 2…r−1, and the last round.
'''

description_COOPERATIVE_9 = '''
Below is a single‐strategy “one‐round trigger with forgiveness” that (i) starts out fully cooperative, (ii) punishes any round in which the group fails to reach the m‐cooperator threshold by defecting exactly one round, and then (iii) immediately forgives and returns to cooperation.  In tests against similarly conditional strategies this both sustains cooperation and guards against repeated exploitation.

1.  Variables  
   • last_failure_round ← 0        // the most recent round in which cooperators < m  
   • current_round ← 1  

2.  Initialization (before round 1)  
   • last_failure_round ← 0  

3.  Action rule for round t = current_round  
   if t = 1 then  
     play C  
   else  
     // Are we in a punishment round?  
     if last_failure_round = t–1 then  
       play D      // punish for the single previous failure  
     else  
       play C      // otherwise cooperate  
   end if  

4.  After observing all n actions in round t (and counting #C):  
   if (number_of_C < m) then  
     last_failure_round ← t  
   end if  

5.  Increment round:  
   current_round ← current_round + 1  
   if current_round > r then STOP; else go to step 3.  

Explanation of key features  
• First round cooperation  
  We begin by playing C, signaling our willingness to build up a cooperative history.  

• One‐round punishment  
  The moment a round fails to reach m cooperators, we defect in the very next round.  This hurts free riders collectively, creating a deterrent against under‐cooperation.  

• Immediate forgiveness  
  As soon as we have delivered our one‐round punishment, we reset to C even if failures persist.  This allows the group to re–establish cooperation quickly rather than spiral into permanent defection.  

• Continuous cooperation in the last round  
  Because we never “backward‐induct” away from C, we still cooperate in round r if we are not in the single punishment slot—maximizing the chance of hitting the threshold at the end.  

Why it’s cooperative  
  • If everyone adopts this same rule, then any single failure is punished exactly once, after which all return to C.  Over repeated play this supports near‐perfect cooperation every round.  
  • A lone defector in a successful round knows they will trigger a one‐round breakdown next round—making defection far less attractive.  
  • Forgiveness ensures that single mistakes do not cascade into permanent collapse.
'''

description_COOPERATIVE_10 = '''
Below is a single‐strategy proposal, called “Generous Contingent Cooperation” (GCC), that aims to sustain the threshold each round while punishing failures only briefly and quickly forgiving in order to re‐establish cooperation.

1.  Overview of the idea  
    •  Start by cooperating to signal goodwill.  
    •  In each subsequent round, look at how many players cooperated in the previous round (call this count Mprev).  
    •  If the group “succeeded” (Mprev ≥ m) or was one short of success (Mprev = m – 1), you cooperate again.  
    •  If the group “failed badly” (Mprev < m – 1), you defect for exactly one round as a mild punishment, then resume cooperation to give the group another chance.  
    •  In the final round, switch to a one‐step forecast of whether cooperation will hit the threshold—if you believe it will, you cooperate; otherwise you defect to avoid wasting your endowment.

2.  State variables  
    punish_flag ∈ {true, false}  
      – Indicates whether you are in your one‐round punishment state.  
    Mprev ∈ {0,1,…,n}  
      – Number of cooperators observed last round (initially undefined, set after round 1).

3.  Pseudocode  

    // Initialization  
    punish_flag ← false  
    Round ← 1  

    FOR Round = 1 to r DO  
      IF Round = 1 THEN  
        action ← C            // always start by cooperating  
      ELSE IF Round = r THEN  
        // Last round: forecast based on last outcome  
        IF Mprev ≥ m THEN  
          action ← C  
        ELSE  
          action ← D  
        ENDIF  
      ELSE  
        // Intermediate rounds 2..r–1  
        IF punish_flag = true THEN  
          action ← D  
          punish_flag ← false          // only punish one round  
        ELSE  
          IF Mprev ≥ m THEN  
            // last round was a full success  
            action ← C  
          ELSE IF Mprev = m – 1 THEN  
            // group just missed threshold by one  
            action ← C                  // jump in to tip it over  
          ELSE  
            // group failure by more than one  
            action ← D                  // short‐term punishment  
            punish_flag ← true         // punish exactly one round  
          ENDIF  
        ENDIF  
      ENDIF  

      // Play “action” simultaneously with others, observe number of C’s = Mcur  
      Mprev ← Mcur  
    END FOR

4.  Explanation of key points  

  •  First round → C  
     You never defect on round 1. This immediately signals that you aim to build cooperation.  

  •  Success → cooperate  
     Whenever the group met the threshold (Mprev ≥ m), it shows cooperation is viable. You keep cooperating.  

  •  Near‐miss → cooperate  
     If exactly m–1 cooperated, a single extra C (you) can make the project succeed. You seize that opportunity rather than punish.  

  •  Far‐miss → brief punishment  
     A big shortfall (Mprev < m–1) suggests many free‐riders. You defect one round to lower their payoff and signal disapproval, then forgive immediately to allow a fresh start.  

  •  Forgiveness  
     By punishing only one round, you avoid endless mutual defection cycles. Forgiveness lets the group retry cooperation quickly.  

  •  Last round → myopic best‐response  
     Since there is no future, you defect if you believe there will not be enough cooperators (Mprev < m), and cooperate only if you think the threshold will be reached—the only chance to get the group reward one last time.  

5.  Cooperative mindset  
    •  You always try to build or restore cooperation quickly.  
    •  Punishments are mild (one round only) and calibrated only to “far failures.”  
    •  You jump in when the group is on the brink (m–1 cooperators).  
    •  You never punish indefinitely, so you remain “nice” and willing to cooperate again.
'''

description_COOPERATIVE_11 = '''
Below is a single‐strategy “trigger‐and‐forgive” rule that (1) tries to meet the m-cooperator threshold every round, (2) punishes a failure by withholding cooperation for exactly one round, then immediately returns to cooperation, and (3) always cooperates in the last round to maximize the final payoff opportunity.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Strategy name: Trigger‐and‐One‐Round‐Forgive (T1F)

State variables (maintained across rounds):
  punishment_timer  // integer ≥ 0; counts how many future rounds we must defect as “punishment”

Initialization (before round 1):
  punishment_timer ← 0

Decision rule for each round t = 1, 2, …, r:
  if t = 1 then
    action ← C
  else if punishment_timer > 0 then
    action ← D
    punishment_timer ← punishment_timer − 1
  else if t = r then
    // Last round: always cooperate
    action ← C
  else
    // Look at the realized number of cooperators in round t–1:
    let prev_coop_count = number of players (including yourself) who played C in round t–1
    if prev_coop_count < m then
      // Threshold failure in t–1: punish by defecting this round
      action ← D
      punishment_timer ← 1
    else
      // Success last round: resume cooperation
      action ← C

End decision rule.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Explanation and rationale

1. First round (t = 1):
   • We start by cooperating (C) to signal willingness to coordinate.

2. Success handling:
   • If in the previous round the group met the threshold (prev_coop_count ≥ m), we assume others cooperated and continue cooperating.

3. Failure‐trigger and one‐round punishment:
   • If the previous round failed to meet m cooperators, we defect this round as a warning (punishment_timer ← 1). That reduces our own payoff by 0 or k, but communicates “I will not keep cooperating if you drop below m.”
   • After exactly one punishment round, punishment_timer=0 and we return to cooperation, giving partners a fresh chance.

4. Last round (t = r):
   • We cooperate unconditionally, because there is no future to threaten. This maximizes the chance of reaching the threshold and gaining the extra k.

Why this fosters cooperation
• By punishing any threshold‐failure only for one round, we avoid endless mutual defection traps. The group is forgiven immediately, which helps re-establish cooperation.
• Because we start by cooperating and resume cooperation quickly, we help coordinate on the “all-C” (or at least m-C) equilibrium rather than staying trapped in “all-D.”
• Always cooperating in the final round ensures we do our part to meet m if others also cooperate, boosting total group payoff.

Edge cases
• If the very first round fails (prev_coop_count in round 1 < m), round 2 we will defect once, then round 3 we return to cooperation.
• Multiple consecutive failures will be punished one round at a time: e.g. if round 4 fails, we defect in 5, then in 6 cooperate. If 6 again fails, we defect in 7, etc.
• In the last round we never punish (even if round r–1 failed), because there is no opportunity to regain lost future payoffs—we go for the group bonus if possible.

Pseudocode sketch

  initialize punishment_timer = 0

  for t in 1..r:
    if t == 1:
      play C
    else if punishment_timer > 0:
      play D
      punishment_timer -= 1
    else if t == r:
      play C
    else:
      // observe prev_coop_count from t–1
      if prev_coop_count < m:
        play D
        punishment_timer = 1
      else:
        play C

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

This Trigger‐and‐One‐Round‐Forgive rule is simple, deterministic, and leans strongly toward cooperation, only punishing failures just long enough to deter free‐riding, then immediately forgiving so that the group can get back on track.
'''

description_COOPERATIVE_12 = '''
Below is a single‐strategy recipe – call it “Generous Threshold-Tit-for-Tat (GTTT)” – that aims to sustain cooperation in the repeated collective-risk dilemma.  It is easy to describe, handles first and last rounds, is forgiving, and reacts only to the group’s success or failure to meet the threshold m.

1. Overview  
   • We treat each round (t = 1…r) exactly the same except for a special rule in round r.  
   • We keep one bit of state: “InGoodStanding” ∈ {True,False}.  This captures whether we’re currently willing to cooperate.  
   • We also use a small forgiveness probability f ∈ (0,1) to allow recovery from accidental breakdowns in cooperation.  

2. Parameters  
   • n ≥ 2, r > 1, 1 < m < n, k > 1 (given)  
   • f = 0.3 (for example; any 0 < f < 1 gives some forgiveness)  

3. State initialization  
   InGoodStanding ← True  

4. Round‐by‐round decision rule  

   For t from 1 to r do  
     if t == 1 then  
       1. Action ← C  
       2. InGoodStanding ← True  
       (We start by signalling willingness to cooperate.)  
     else if t == r then  
       1. Action ← D  
          (Backward induction: last round has no future punishment, so we defect.)  
     else  // 2 ≤ t < r  
       Let Coops_{t–1} = number of players who chose C in the previous round.  

       if InGoodStanding == True then  
         if Coops_{t–1} ≥ m then  
           Action ← C  
           // Last round was “successful cooperation,” so keep cooperating.  
         else  
           Action ← D  
           InGoodStanding ← False  
           // Last round failed, trigger punishment.  
         end  
       else  // InGoodStanding == False, we are in punish‐mode  
         if Coops_{t–1} ≥ m then  
           with probability f do  
             Action ← C  
             InGoodStanding ← True  
             // Forgive a successful rebound  
           else  
             Action ← D  
           end  
         else  
           Action ← D  
         end  
       end  
     end  

5. Explanation of key features  
   • First round: We always cooperate to signal goodwill.  
   • Middle rounds:  
     – If we are in “good standing” (InGoodStanding = True), we cooperate whenever the group last round met the threshold. Otherwise we defect and switch to punish‐mode.  
     – If we are in punish mode, we continue defecting until we see that others have again met the threshold; then with small probability f we forgive and switch back to good standing.  
   • Last round: We defect, since there is no future to enforce cooperation.  

6. Why this fosters cooperation  
   • It is a trigger strategy: as long as everyone meets the threshold each round, we keep cooperating.  
   • It is generous/forgiving: a single failure doesn’t lead to permanent breakdown. We allow the group to recover with probability f when they again hit the threshold.  
   • It is deterministic except for the forgiveness step, so opponents can infer your rules easily and coordinate to stay above m.  

7. Pseudocode  

   function chooseAction(t, history, InGoodStanding):  
     if t == 1:  
       return (C, True)  
     if t == r:  
       return (D, InGoodStanding)  
     Let CoopsLast = countCooperations(history[t−1])  
     if InGoodStanding:  
       if CoopsLast ≥ m:  
         return (C, True)  
       else:  
         return (D, False)  
     else:  # punish‐mode  
       if CoopsLast ≥ m and rand() < f:  
         return (C, True)  
       else:  
         return (D, False)  
       end  
     end  
   end  

Replace rand() < f with your favorite random generator.  

––––––––––––––––––––  
This GTTT strategy makes your behavior transparent, rewards sustained group success, punishes lapses (below m cooperators), yet allows the group to bounce back. It will—against many independent strategies—achieve high cooperation rates up until the very last round.
'''

description_COOPERATIVE_13 = '''
Below is a single‐strategy “Regret‐and‐Forgive” recipe that (1) aggressively seeks to meet the threshold, (2) only ever punishes for one round, (3) immediately forgives and returns to cooperation, and (4) handles first, last, and failure rounds explicitly.  It is designed for any n, r, m, k (with 1 < m < n, r > 1, k > 1).

1. State variables  
   • punish_timer ← 0  // counts down remaining punishment rounds  

2. High‐level idea  
   • By default, cooperate if in the previous round the group succeeded (≥ m cooperators), or if the only reason for failure wasn’t your own defect.  
   • If the group fails because fewer than m cooperators contributed (and it couldn’t have succeeded even if you had cooperated), punish everyone once by defecting, then forgive.  
   • First round you must “signal” cooperation.  
   • Last round: if you believe (from last round’s history) that others will cooperate in sufficient numbers, cooperate; otherwise defect to avoid a sucker’s payoff.  

3. Decision rules in pseudocode  

```
Inputs: 
  n, r, m, k
State: 
  punish_timer = 0

for round t in 1…r do:
  
  // 1. If we are in a punishment phase, keep defecting
  if punish_timer > 0 then
    action = D
    punish_timer = punish_timer - 1
    goto PLAY

  // 2. First‐round convention: signal your willingness to cooperate
  if t == 1 then
    action = C
    goto PLAY

  // 3. Last‐round consideration: 
  //    Cooperate only if last round’s cooperation level suggests ≥m others will cooperate
  if t == r then
    let M_prev = number of cooperators in round r−1
    // if last round we hit the threshold, assume they will again:
    if M_prev ≥ m then
      action = C
    else
      action = D
    goto PLAY

  // 4. Normal rounds 2…r−1 when not punishing
  //    Inspect the previous round:
  let M_prev = total cooperators in round t−1
  let M_prev_excl_me = cooperators among the other n−1 players in round t−1

  if M_prev ≥ m then
    // group succeeded → keep cooperating
    action = C
  else
    // group failed → determine if it was your fault
    if M_prev_excl_me ≥ m then
      // they had it without you → forgive, continue cooperating
      action = C
    else
      // even if you had cooperated they still would have fallen short → punish once
      punish_timer = 1
      action = D

  PLAY:
  “Play action (C or D) this round”
end for
```

4. Explanation of key design points  
• Cooperate on round 1 to signal your willingness.  
• Immediately punish exactly one round if and only if the group failed the threshold and that failure could not have been averted by your cooperation.  This deters others from free‐riding.  
• Forgive immediately after one period of punishment, returning to cooperation as soon as the punishment expires.  
• In the final round, defect if history suggests you would be the lone cooperator (risking a 0 payoff); otherwise cooperate to secure the reward k.  

5. Why this is cooperative  
• You default to cooperation whenever the group is succeeding or whenever a failure wasn’t “your fault.”  
• Punishments are as short and mild as possible (one round only), ensuring the window for recovery is immediate.  
• You never “grim trigger” forever; you continuously offer a return path to full cooperation, even after a slip.  
• You only withhold cooperation when it is strategically necessary (either to punish actual free‐riding or to avoid being exploited in the last round).
'''

description_COOPERATIVE_14 = '''
Below is a single‐strategy design that (1) tries to coordinate on meeting the threshold every round, (2) punishes “mistakes” only one round so that cooperation can recover, and (3) avoids the classic end‐game collapse by defecting in the very last round.  In effect it is a “group‐level Win-Stay/Lose-Shift” (WSLS) with a one‐round punishment and end‐round defection.

1. Overview of Principles  
   • We treat the group’s outcome each round as a “win” if at least m players cooperated, “lose” otherwise.  
   • On a “win,” we repeat our own last action (if we cooperated and got the bonus, we keep cooperating; if we defected but still got the bonus, we keep defecting).  
   • On a “lose,” we switch our action for exactly one round (punishment/signal), then go back to cooperating.  
   • In the very last round (t = r), we defect (no future to enforce cooperation).  

2. State Variables (what you carry between rounds)  
   • last_action ∈ {C, D}  
   • last_round_won ∈ {true, false}  

3. Strategy Description in Words  
Round 1:  
  – No history yet → Cooperate (C) to signal willingness.  
Rounds 2…r−1:  
  – If last_round_won = true, play the same action you played last time.  
  – If last_round_won = false, play the opposite of your last action (one‐round punishment), then reset to cooperation on the next failure‐recovery cycle.  
Round r (final round):  
  – Defect (D).  

4. Pseudocode  
```
Initialize:
  last_action    := C
  last_round_won := false   // dummy, only used after round 1

For each round t = 1 to r do:
  if t == 1 then
    action := C
  else if t == r then
    action := D
  else
    if last_round_won then
      action := last_action         // Win-Stay
    else
      action := (last_action == C) ? D : C   // Lose-Shift (one‐round switch)
    end if
  end if

  // Play `action`, observe how many cooperated this round
  // Compute round payoff but more importantly:
  //   last_round_won := (observed_cooperators ≥ m)
  //   last_action    := action
end for
```

5. Why this is Cooperative  
  • As long as the group hits the threshold each round, every WSLS player keeps cooperating.  You get 0 cost + k reward per round → highest group‐level payoff.  
  • If a “mistake” occurs (too few cooperators), your one‐round switch both punishes potential defectors and signals readiness to return to cooperation.  That keeps the system from spiraling into permanent defection.  
  • By defecting in the final round, you avoid the classic “all‐D” collapse at the end and guard against being exploited in a round with no future enforcement.  

6. Edge Cases  
  • If r = 2, you cooperate round 1, then round 2 is final → you defect.  (No stable cooperation possible in a two‐round threshold game anyway.)  
  • If one round fails (observed_cooperators < m), you defect only that one next round, then attempt to re‐coordinate to meet m.  
  • If the threshold m = n (unanimity), this still works: you all cooperate until someone deviates, you punish once, then return to cooperation.  

This strategy is simple, transparent to observant opponents, heavily favors cooperation in the body of the game, and protects you from being the perpetual sucker.
'''

description_COOPERATIVE_15 = '''
Here is a simple, transparent “collective Tit-for-Tat” strategy that (i) tries to hit the threshold every round, (ii) punishes a failure just long enough to re-establish cooperation, and (iii) defects in the very last round to avoid the backward-induction collapse of cooperation.  

1.  Definitions and internal state  
    •  r = total rounds, t = current round (1 ≤ t ≤ r)  
    •  m = threshold of cooperators needed  
    •  coopers_prev = number of players who chose C in round t–1  
    •  punished = Boolean flag, initially false  

2.  High-level rule summary  
    a.  Round 1: Cooperate.  
    b.  If you are in the final round (t = r): Defect.  
    c.  Otherwise, if you are currently “punishing” (punished = true), defect one round, then clear punished.  
    d.  Otherwise (not last, not punishing):  
         –  If coopers_prev ≥ m, cooperate.  
         –  If coopers_prev < m, defect and set punished = true.  

3.  Why this works  
    •  First round play-cooperatively to give the group a chance to meet m.  
    •  As long as the group meets the threshold, you keep cooperating.  
    •  If the group ever fails (coopers_prev < m), you withhold cooperation exactly one round—enough to impose a clear cost on free-riders—then resume giving the group another chance.  
    •  By defecting in round r, you avoid the classic unraveling of cooperation at the very end.  

4.  Pseudocode  

    punished ← false  
    for t from 1 to r do  
        if t = r then  
            action ← D                    // Last round: defect  
        else if t = 1 then  
            action ← C                    // First round: cooperate  
        else if punished then  
            action ← D                    // Carry out punishment  
            punished ← false             // Only punish for one round  
        else  
            if coopers_prev ≥ m then  
                action ← C                // Group met threshold last round  
            else  
                action ← D                // Group failed: punish next round  
                punished ← true  
            end if  
        end if  

        // play(action), observe other players’ actions  
        // update coopers_prev for next iteration  
    end for  

5.  Edge-case handling  
    •  r = 2: Round 1 you cooperate, round 2 you defect. This gives the group one shot at cooperation but avoids end-game unraveling.  
    •  If the group fails multiple times in a row, you repeatedly punish for one round then resume cooperating—so you never get stuck in perpetual defection, but you do impose a clear cost for each group failure.  
    •  If the group always makes m, you cooperate every non-final round and defect only in r, achieving (r–1)·(k) extra group payoff and one private defection payoff at the end.  

This strategy is easy to explain, publicly observable, enforces the cooperative norm (by immediate but short punishments), and avoids the classic last-round defection spiral.
'''

description_COOPERATIVE_16 = '''
Here is a simple, easy‐to‐communicate “threshold tit-for-tat with one-period punishment” strategy that (a) aims for full cooperation, (b) punishes failures just enough to restore coordination, and (c) handles first and last rounds cleanly:

1. State Variables  
   • punishing (boolean): are we in a one‐round punishment?  
     – Initialize punishing = false.

2. Round t decision rule  
   if t == 1:  
     play C  
   else if t == r:  
     play D              # backward‐induction “last‐round defection”  
   else:  
     let coops_prev = number of players who played C in round t–1  
     if punishing == true:  
       play C  
       punishing = false  
     else if coops_prev ≥ m:  
       play C            # success last round ⇒ stay cooperative  
     else:  
       play D            # failure last round ⇒ punish once  
       punishing = true

3. Explanation of behavior  
 A. First round (t=1): we cooperate to “test the water” and signal willingness.  
 B. Middle rounds (2 ≤ t ≤ r–1):  
    – If last round had at least m cooperators, we continue to cooperate.  
    – If last round fell below threshold, we defect exactly one round as a “wake-up call,” then immediately return to cooperation.  
 C. Last round (t=r): we defect.  
    – In a finite horizon, defection in the final stage is individually optimal (no future to reward cooperation); we therefore switch to D to protect ourselves.

4. Why this is cooperative  
 • It achieves the group threshold whenever opponents are also willing to coordinate.  
 • It punishes coordination failures but forgives after one round—no endless grudge.  
 • It is transparent (“Tit-for-Tat at the group level”) and easy for others to predict, which helps them trust and align with us.  
 • Despite last-round defection, by sustaining cooperation nearly everywhere else we maximize the team’s total payoff over r rounds.

Pseudocode summary:

```
Initialize punishing = false

for t in 1…r:
    if t == 1:
        action = C
    else if t == r:
        action = D
    else:
        coops_prev = count of C’s in round t–1
        if punishing:
            action = C
            punishing = false
        else if coops_prev ≥ m:
            action = C
        else:
            action = D
            punishing = true
    play action
```

This strategy is cooperative, forgiving, and enforces the group’s minimum‐cooperator requirement without permanent breakdowns.
'''

description_AGGRESSIVE_1 = '''
Below is a fully specified “sabotage‐and‐free‐ride” strategy.  In essence you never cooperate yourself, but you always choose your defections so as either to free‐ride on others’ successes or to tip a near-miss into outright failure—maximizing your own payoff and minimizing the group’s.

1.  Data structures and bookkeeping  
   •  history[t] = list of actions (“C” or “D”) of all n players in round t  
   •  coop_count[t] = number of “C”’s in history[t] (including your own)  

2.  Helper: predict_others_coops(t)  
   Estimate how many cooperators the other n–1 players will choose in round t.  A simple forecast is “what happened last round”:  
     If t = 1, assume E = m (i.e. worst-case assume threshold will be met so you can free-ride).  
     Else let E = coop_count[t–1] – (you cooperated in t–1? 1 : 0).  
   Return E.

3.  Core decision rule for each round t:  
   Let E = predict_others_coops(t).  This is your estimate of how many of the other n–1 players will play C.  

   •  Case A: E ≥ m  
        –  If you play C, total coops ≥ m+1, you’d get π = 0 + k = k.  
        –  If you play D, total coops ≥ m, you get π = 1 + k = k+1.  
        → Defect (D) to free-ride.  

   •  Case B: E = m–1  
        –  If you play C, total coops = m and you get k.  
        –  If you play D, total coops = m–1 and you get 1.  
        However, by defecting you ensure the public good _fails_ and everyone only gets 1 (punishment).  
        → Defect (D) to sabotage.  

   •  Case C: E < m–1  
        –  Even if you cooperate the threshold won’t be met, so both actions yield only your private unit (1 if you defect, 0 if you cooperate).  
        → Defect (D) to keep your endowment.  

   You can summarize this in one line:  
     “Always play D.  If enough others will cooperate, you free-ride; if just enough will cooperate, you sabotage; otherwise you keep your endowment.”  

4.  Edge cases  
   –  First round (t=1): predict_others_coops= m ⇒ falls into Case A ⇒ defect.  
   –  Last round: apply the same rule.  You never cede an opportunity to free-ride or sabotage, even in the final round.  
   –  No belief updating beyond “last round’s count.”  This keeps your strategy maximally aggressive and hard to “sweet-talk.”  

5.  Pseudocode  

  initialize history as empty  
  for t in 1..r:  
    if t == 1:  
      E ← m                     # assume threshold met so we can free-ride  
    else:  
      E ← coop_count[t-1] – (history[t-1][you] == “C” ? 1 : 0)  

    # Decision  
    if E ≥ m:  
      action ← “D”    # free-ride  
    else if E == m–1:  
      action ← “D”    # sabotage  
    else:  
      action ← “D”    # pure self-interest  

    play action; record all players’ actions in history[t];  
    coop_count[t] ← count of “C” in history[t]  

That is the full aggressive strategy.  You never cooperate, you always extract maximum private gain when the good is produced, and you actively tip marginal rounds into failure.
'''

description_AGGRESSIVE_2 = '''
Below is an “Aggressive Threshold Free‐Rider” strategy.  Its core idea is simple:  never waste a contribution except when you alone can tip the balance to get the public reward k, and otherwise defect (free‐ride).  You only cooperate when the number of other cooperators is exactly m–1; at all other times you defect.  

1. State variables you track  
   • t: current round (1…r)  
   • last_others: in the previous round, how many of the other n–1 players chose C  

2. High-level decision rule (for round t):  
   if t == 1 or t == r:  
     play D  
   else:  
     if last_others == m–1:  
       play C    # you alone tip threshold from m–1 to m  
     else:  
       play D    # either you would be wasted (≥m) or hopeless (<m–1)  

3. Rationale  
   – First round (t=1): no information, so defect and free-ride.  
   – Last round (t=r): standard end-game free-ride—defect regardless.  
   – Middle rounds:  
     • If last_others ≥ m, you expect that even if you defect the group will meet the threshold; you can safely free-ride and get 1+k instead of k.  
     • If last_others < m–1, even if you cooperate the threshold fails, so you’d get 0 rather than 1 if you cooperate—defect.  
     • If last_others == m–1, only your cooperation turns failure into success.  Since k>1, the payoff from cooperating (0+ k) exceeds defecting (1+0), so you cooperate.  

4. Pseudocode  

  initialize last_others ← 0  
  for t in 1…r do  
    if t == 1 or t == r:  
      action ← D  
    else if last_others == m–1:  
      action ← C  
    else:  
      action ← D  
   
    play(action)  
    observe actual_others ← number of C’s among opponents this round  
    last_others ← actual_others  
  end  

5. Edge-case checks  
  • If m–1 > n–1 (i.e. m>n), impossible by spec; never happens.  
  • If opponents suddenly all defect (last_others=0): you stay defecting (threshold hopeless).  
  • If opponents all cooperate (last_others=n–1 ≥m): you exploit them each round.  
  • In the round you switch to C (only when last_others==m–1), you guarantee k instead of 1.  

This strategy is “aggressive” in that it never gives up value unnecessarily, it refuses to prop up others’ cooperation, and only contributes when it is strictly in your own interest to rescue the threshold.
'''

description_AGGRESSIVE_3 = '''
Below is an “aggressive‐free‐rider” strategy that (i) never cooperates unless it is strictly necessary to trigger the bonus k, and (ii) otherwise always defects to maximize your private payoff.  In effect you “lean on” m–1 cooperators whenever you see them, but never give a cent of your own unless you absolutely must.

1.  Definitions  
   • n = total players  
   • m = cooperation threshold  
   • r = total rounds  
   • For round t, let C_others(t–1) = number of other players who cooperated in round t–1.  

2.  Core decision rule (applies every round t = 1…r):  
   if C_others(t–1) == m–1  
       play C  ⟶ “Just enough to push cooperators to m and snag k”  
   else  
       play D  ⟶ “Otherwise always defect”  

3.  Edge‐case handling  
   • Round 1 (t=1): no history ⇒ set C_others(0)=0 ⇒ you defect.  
   • Last round (t=r): same rule still applies.  Even in the final round you only cooperate if exactly m–1 others cooperated last time.  Otherwise defect—there is no future to “build trust,” so full defection.  
   • If C_others(t–1) < m–1, your lone cooperation would not reach the threshold, so you prefer D (get payoff 1 rather than 0).  
   • If C_others(t–1) ≥ m, threshold will succeed without you, so you defect and still earn 1+k.  

4.  Pseudocode  

   initialize history of others’ cooperations: C_others(0) ← 0  
   for t in 1…r:  
     if C_others(t–1) == m–1:  
       action_i(t) ← C  
     else:  
       action_i(t) ← D  
     observe C_total(t) = total cooperators in round t  
     C_others(t) ← C_total(t) − [1 if action_i(t)==C else 0]  

5.  Aggressiveness rationale  
   – You never “waste” a cooperation when it won’t buy you the bonus.  
   – You only cooperate at the knife-edge (m–1 others), forcing them to carry almost the entire cost.  
   – All other times your payoff is maximized by defection (1+k if the group succeeds, 1 if it fails).  
   – No leniency, no forgiveness, no “nice‐guy” sacrifices—and no end-game lapse into cooperation.
'''

description_AGGRESSIVE_4 = '''
Below is an aggressive, trigger‐style strategy for the repeated collective–risk dilemma.  The intuition is: you only ever cooperate if by doing so you can tip the round into “threshold met,” you immediately punish any group that fails you, and you defect unconditionally in the last round.

――――――――――――――――――――――――――――――――  
Aggressive Threshold Enforcer (ATE)  
――――――――――――――――――――――――――――――――  

State variables (persist across rounds)  
• punished ∈ {false, true}, initially false  
• last_C_count (number of cooperators from the previous round), initially 0  

Decision Rule for round t=1…r:  
1.  If t == r (last round):  
      action ← D  
2.  Else if t == 1:  
      action ← D   // test by defecting first  
3.  Else if punished == true:  
      action ← D   // permanent defection once you punish  
4.  Else:  
      // we are “active”  
      if last_C_count ≥ m then  
         action ← D   // safe to free-ride  
      else if last_C_count == m–1 then  
         action ← C   // only you can push it over the threshold  
      else  
         // group failed badly (even with your cooperation it wouldn’t have reached m)  
         action ← D  
         punished ← true  // trigger permanent punishment  

After all actions in round t are realized, observe C_count ← # of players who chose C this round.  
Then update:  
• last_C_count ← C_count  
• If you chose C and C_count < m then  
      punished ← true  // you cooperated but the group still failed → punish forever  

Payoff motive of each component  
– You never cooperate unless your one contribution is strictly pivotal (last_C_count == m–1).  
– You defect on the very last round (no future to punish).  
– If the group fails the threshold on a round you do not control, you shift to permanent defection, “punishing” everyone thereafter.  

Pseudocode  

```
Initialize:
  punished = false
  last_C_count = 0

For t = 1 to r:
  if t == r:
    action = D
  else if t == 1:
    action = D
  else if punished:
    action = D
  else:
    // Active phase
    if last_C_count >= m:
      action = D       // exploit safe round
    else if last_C_count == m - 1:
      action = C       // you alone can meet threshold
    else:
      action = D
      punished = true  // group was too irresponsible, punish forever

  Play action, observe C_count (including your own C if you played it)

  // Update after seeing outcomes
  last_C_count = C_count
  if action == C and C_count < m:
    punished = true    // you got burned, go to permanent defection
```

Key Features  
• Aggressive free‐riding: you only cooperate when pivotal; otherwise you defect.  
• Trigger punishment: one bad round and you never cooperate again, discouraging others from letting the threshold fail.  
• End-game exploitation: in the very last round you always defect because there is no future.  
• Simple to implement, deterministic, unmistakably aggressive.
'''

description_AGGRESSIVE_5 = '''
Below is a fully specified “aggressive” strategy.  In essence we never “waste” a cooperation except in the one circumstance where we can tip the balance and then immediately defect so as to free-ride on others’ contributions.  We defect in the first round (to establish our stance) and in the last round (no future retaliation possible), and in all other rounds we only cooperate if we see exactly m–1 cooperators in the previous round.  Otherwise we defect.

----------------------------------------------------------------------
1.  Notation  
   • t ∈ {1,2,…,r} is the round number.  
   • hist[t–1] = number of cooperators in round t–1 (for t>1).  
   • A_i,t ∈ {C,D} is our action in round t.  

2.  Strategy Outline  
   1.  Round 1: Defect.  
   2.  Rounds 2 through r–1:  
       – If hist[t–1] = m–1, Cooperate (to tip the threshold).  
       – Otherwise, Defect.  
   3.  Round r (final): Defect.  

3.  Rationale  
   – By defecting whenever hist[t–1] ≥ m, we free-ride on the group if they were already reaching the threshold.  
   – By defecting whenever hist[t–1] ≤ m–2, we avoid wasting our endowment when the project would fail.  
   – Only when exactly m–1 cooperators appeared last round do we cooperate—precisely that one round in which our single additional contribution secures the bonus for everyone; even here we cooperate only once and then immediately go back to defection.  
   – First‐round defection prevents us from ever being “sucker” in round 1, and last‐round defection prevents any form of end‐game cooperation (no future punishment is possible).  

4.  Pseudocode  

```
Inputs:  n, r, m, k
Maintain:  hist_coops[t] for t=1…r (initialized to 0)

For each round t = 1 to r do:
    if t == 1 then
        A_i,t ← D
    else if t == r then
        A_i,t ← D
    else
        let prev = hist_coops[t-1]
        if prev == m-1 then
            A_i,t ← C
        else
            A_i,t ← D
        end if
    end if

    Play A_i,t simultaneously with others; observe total cooperators hist_coops[t].
End for
```

5.  Edge Cases  
   • If other players never approach the threshold (hist_coops[t-1] ≤ m–2 for all t), we never cooperate and collect a safe payoff of 1 each round.  
   • If they routinely overshoot (hist_coops[t-1] ≥ m), we defect every time and free-ride on their cooperation, collecting 1+k each round once they’ve self–organized.  
   • If they sometimes sit at exactly m–1, we step in just that once to secure +k for everyone and reap 0+k rather than 1, but in doing so we enable rounds in which we later get 1+k instead of 0+k as free-riders.  

This meets the requirement for an “aggressive” mindset: we only ever contribute when strictly necessary to attain the collective reward—and otherwise exploit cooperators without remorse.
'''

description_AGGRESSIVE_6 = '''
Below is a self-centered, “aggressive exploiter” strategy for the repeated Collective‐Risk Dilemma.  It never “wastes” contributions except when doing so turns a round’s payoff in its favor, and otherwise defects to punish or free-ride.  It uses the previous round’s observed cooperators as a predictor of the current round.  In the last round it always defects.

Name  
 Aggressive Minimal-Exploiter (AME)

Notation  
 t = current round, 1 ≤ t ≤ r  
 histC[t−1] = number of cooperators among the other n–1 players in round t–1 (for t=1, set histC[0] = 0)  
 m, r, k as given  

Decision rule at the start of round t:  
  if t = r then  
    play D  // last-round defection  
  else  
    let x = histC[t−1]   // predict # of cooperators this round among others  

    if x ≥ m then  
      // even without you, threshold likely met ⇒ free-ride  
      play D  
    else if x = m − 1 then  
      // only your C can tip it over ⇒ you gain k versus 1 if you defect  
      play C  
    else  
      // x < m−1 ⇒ you cannot tip threshold, so contributing only loses you 1  
      play D  

After the round, you observe actual #cooperators among opponents and set histC[t] accordingly.

Corner cases & comments  
1. First round (t=1): histC[0]=0 ⇒ x=0<m−1 ⇒ play D.  You start by defecting to “test the water” and punish any naïve cooperators.  
2. Always defect at the last round t=r because there is no future to leverage any cooperation or punishment.  
3. If opponents ever herd into cooperation (x≥m), you immediately switch to permanent defection (free-riding and punishing future rounds).  You only cooperate at t<r when you predict x=m−1, i.e. when your single C turns a round into k reward—otherwise you defect.  
4. No forgiveness or “nice” phases—your only concession is the bare minimum single-player tipping of a borderline round.  

Pseudocode  

  initialize histC[0] ← 0  
  for t from 1 to r do  
    if t = r then  
      action[t] ← D  
    else  
      x ← histC[t−1]  
      if x ≥ m then  
        action[t] ← D            // free-ride whenever threshold met without you  
      else if x = m − 1 then  
        action[t] ← C            // single minimal cooperation to capture k > 1  
      else  
        action[t] ← D            // defect if you can’t tip threshold  
    end if  

    // … play action[t], observe opponents’ cooperations coops_excl  
    histC[t] ← coops_excl  
  end for  

Why “aggressive”?  
- You never cooperate when it merely helps others—only when it directly maximizes your one‐round payoff by tipping the threshold from “no reward” to “reward.”  
- You punish excessive cooperation by defecting whenever you foresee threshold attainment.  
- You never extend mercy or long–term cooperative “contracts,” and you end the game with outright defection.
'''

description_AGGRESSIVE_7 = '''
Below is an “aggressive pivot” strategy that almost always defects but will grudgingly cooperate only when your single contribution is needed to tip the group over the threshold and secure the bonus for yourself.  It uses a simple moving‐average forecast of how many others will cooperate next round.

1.  State variables and parameters  
   •  n, m, r, k as given.  
   •  γ ∈ (0,1): smoothing factor for moving average (e.g. γ=0.3).  
   •  Ŝ: your current forecast of the number of *other* cooperators next round (real number).  

2.  Initialization  
   •  Set Ŝ ← m   (optimistic start—assume others will cooperate enough so you can safely defect).  

3.  Per-round decision rule (for round t = 1…r)  
   Let  floor_S = ⌊Ŝ⌋.  
     
   A.  Decide action a_t ∈ {C,D} as follows:  
     1.  If floor_S ≥ m, then  
         a_t ← D    (others will meet the threshold without you → always defect)  
     2.  Else if floor_S = m−1, then  
         a_t ← C    (you are pivotal; contributing costs 1 but gains k, so profitable)  
     3.  Else  (floor_S < m−1)  
         a_t ← D    (even if you cooperate the threshold will fail → never waste a contribution)  
     
   B.  Play a_t simultaneously with all players.  

   C.  Observe actual number of cooperators in round t (call it C_t, including yourself).  
       Compute “others’ cooperators”: O_t = C_t − 1{a_t=C}.  

   D.  Update the moving‐average forecast for next round:  
       Ŝ ← (1−γ)·Ŝ + γ·O_t  

4.  End game (no special last‐round tweak)  
   Since you’re purely self‐interested and there is no future punishment in the final round, the same pivot logic applies: you only cooperate if you predict exactly m−1 others.

Remarks on aggressiveness and edge-cases  
 •  First round: Ŝ was initialized to m, so floor_S≥m ⇒ you defect. You collect data on who else tried to cooperate.  
 •  Middle rounds: you only ever pay the cost when you are strictly *pivotal*. Otherwise you free‐ride on others’ contributions.  
 •  Last round: with no continuation value, everyone else tends to defect, so Ŝ will drop below m−1 and you too will defect—aggressively refusing to throw away your endowment.  
 •  No forgiveness, no costly punishment: pure exploitation plus minimal risk‐management to still grab the bonus when it’s on the table.

Pseudocode  

```
Inputs: n, m, r, k, γ in (0,1)
Initialize:
  S_hat ← m        // forecast of “others” cooperating

For t from 1 to r do:
  floor_S ← floor(S_hat)

  // Decision rule
  If floor_S ≥ m then
    a ← D         // safe to defect; others will reach threshold
  Else if floor_S = m−1 then
    a ← C         // pivotal: cooperate to get k
  Else
    a ← D         // hopeless: defect to avoid wasting 1

  Play action a

  // After round outcome
  Observe total cooperators C_t
  O_t ← C_t − (a==C ? 1 : 0)    // number of cooperators excluding you

  // Update forecast
  S_hat ← (1−γ)*S_hat + γ*O_t

End For
```

This strategy is “aggressive” in that it never builds trust, never rewards cooperators, and only ever contributes when strictly forced to in order to pocket the bonus itself.
'''

description_AGGRESSIVE_8 = '''
Below is an “Aggressive Free‐Loader with Conditional Cooperation (AFCC)” strategy.  It defects by default, only “tips” the group into success when doing so is almost guaranteed to pay off, and never cooperates in the very last round.

1.  Notation  
   •  t = current round (1 ≤ t ≤ r)  
   •  coop₋₁ = number of cooperators among the other n–1 players in the previous round (for t=1 we set coop₋₁=0)  
   •  ε = small “probe” probability (e.g. 0.05–0.10)  

2.  High‐level idea  
   –  Round 1: Defect (no history to trust).  
   –  Rounds 2…r–1:  
       •  If coop₋₁ ≥ m, defect and free‐ride on others’ cooperation.  
       •  Else if coop₋₁ = m–1, cooperate to tip the count up to m (so the project succeeds).  
       •  Else (coop₋₁ ≤ m–2), defect—too few cooperators to make it worthwhile.  
       •  But always with small probability ε, “probe” by cooperating once in a while in case the group is primed for a threshold success you didn’t observe.  
   –  Round r (last round): Defect (no future rounds, no incentive to cooperate).  

3.  Pseudocode  

  initialize history_coop_counts = []  
  set ε = 0.05    # or choose any small number < 0.1  

  for t in 1…r:  
    if t == 1:  
      action[t] = D  
    else if t == r:  
      action[t] = D  
    else:  
      coop₋₁ = history_coop_counts[t–1]      # cooperators among the other n–1 last round  
      with probability ε:  
        action[t] = C      # random probe  
      else if coop₋₁ ≥ m:  
        action[t] = D      # exploit the existing cooperation  
      else if coop₋₁ == m–1:  
        action[t] = C      # just enough to tip into threshold success  
      else:  
        action[t] = D      # hopeless to reach threshold, so defect  

    # after all actions are chosen simultaneously in round t,  
    # observe total_coops = number of C’s among the other n–1 players  
    history_coop_counts[t] = total_coops  

4.  Why is this aggressive?  
  •  We defect by default—only cooperating when it is nearly risk‐free (coop₋₁ ≥ m–1).  
  •  We never cooperate in the last round (no future to enforce punishments or rewards).  
  •  We include only a tiny “probing” chance ε to discover if a latent coalition exists; otherwise we refuse to invest.  

5.  Edge cases handled  
  –  First round (t=1): history is empty, so we defect.  
  –  Second round: coop₋₁ is treated as 0, so we defect (except for an ε–chance probe).  
  –  Last round (t=r): we always defect.  
  –  Rounds in between: see the conditional logic above.  

This strategy aggressively free‐rides on any sizable cooperation it observes, only kicking in with a contribution when it can almost guarantee the group meets m, and otherwise declining to participate.
'''

description_AGGRESSIVE_9 = '''
Below is an “extortion-style” aggressive strategy.  It defects whenever it can free-ride, and only cooperates when by doing so it is the pivotal (m-th) cooperator who turns failure into success—never more.

1.  State your information  
    •  n players, threshold m, r total rounds, reward factor k>1.  
    •  You observe, at the end of each round, how many of the other n−1 players cooperated.

2.  High-level idea  
    –  If the other players already meet or exceed the threshold m without you, you defect and collect 1+k rather than paying your cost.  
    –  If they are so few that even with you they can’t reach m, you defect (you’d get 1 vs cooperation’s 0).  
    –  Only when the other cooperators count is exactly m−1 do you cooperate, turning failure into success—because then cooperation pays off (0+k) versus defection’s 1+0.

3.  Pseudocode  

Let history[t−1] record how many of the other n−1 players cooperated in round t−1.  
For t=1,…,r do:  
 if t==1 then  
  action ← D           # no history ⇒ start defecting aggressively  
 else  
  let x ← history[t−1]  
  if x == m−1 then  
   action ← C         # you are pivotal  
  else  
   action ← D         # free-ride or cooperation is wasted  
 end if  
Execute action simultaneously, observe others’ actions, update history.

4.  Edge cases  
 – First round (t=1): no information ⇒ defect.  
 – Any round where last round’s cooperators ≥m: you defect (they’ll succeed anyway).  
 – Any round where last round’s cooperators ≤m−2: you defect (can’t reach m even if you join).  
 – Last round: use the same rule.  There is no “end-game” change, because the logic (defect when you can free-ride, only cooperate when pivotal) already maximizes your one-round payoff net of cost.

5.  Why it’s aggressive  
 – It never “wastes” a cooperation cost except to secure the group payoff exactly when you are needed.  
 – It systematically exploits any overcooperative opponents by defecting if they already form a winning coalition.  
 – It extracts the maximum possible individual surplus each round (1+k whenever they succeed without you, k when you barely make them succeed, and 1 when they fail).

This strategy is simple to implement, robust to all opponent patterns, and always maximizes your per-round payoff given what you observe.
'''

description_AGGRESSIVE_10 = '''
Below is an “aggressive” or “exploit‐and‐sabotage” strategy we’ll call Threshold-Exploiter.  It drives the group close to the m-cooperator threshold but never helps more than strictly necessary, and in the last round it defects unconditionally.

1.  Definitions  
   Let t = 1…r index the current round.  
   Let C_{−i}^{t−1} = number of cooperators among the other n–1 players in round t−1 (we observe this at the start of round t).  

2.  Outline of the Mindset  
   –  We never cooperate unless our single contribution is exactly what turns a losing round (C_{−i}<m) into a winning one (C_{−i}+1 ≥ m).  
   –  If the group already had ≥m cooperators without us, we defect and collect (1+k), free-riding on others’ efforts.  
   –  If even with us the group can’t reach m, we defect anyway—no point in throwing away 1 unit for no reward.  
   –  In the final round we always defect (no future punishment possible).  
   –  By doing this we keep the group hovering just below or at the threshold, extracting maximum payoff for ourselves and denying stable cooperation.

3.  Full Decision Rule  

Pseudocode for player i at round t:

```
Input: round t, history of actions of others in rounds 1…(t−1)
Compute C_others = number of cooperators among opponents in round (t−1)
If t == 1:
    # No history yet: defect to probe whether others will hit the threshold anyway
    action ← D
Else if t == r:
    # Last round: no future, always defect
    action ← D
Else:
    If C_others >= m:
        # Others already had enough cooperators without me
        action ← D
    Else if C_others == m−1:
        # My single C will push them to threshold
        action ← C
    Else:
        # Even with my help they can’t reach threshold
        action ← D
Return action
```

4.  Explanation & Edge Cases  
– First round (t=1): We defect to see if the rest will cooperate to m anyway. If they do, we score 1+k immediately. If they fail, we haven’t “wasted” our 1 unit yet, and we learn how eager they are.  
– Intermediate rounds (1<t<r): We only “top up” the coalition when exactly m−1 others cooperated last time. That single C costs us 1 but yields us k in reward—so net k−1>0. In every other situation we defect.  
– Last round (t=r): We defect unconditionally to grab the private unit plus any k if they manage the threshold without fear of our future punishment.  

5.  Why This Is Aggressive  
– We never voluntarily cooperate when the group already has a safe margin of cooperators.  
– We refuse to “surrender” to hopeless efforts (C_others < m−1).  
– We drive the group to just below threshold whenever possible, denying stable payoffs to cooperators unless they truly need us.  
– In the final round we defect no matter what—pure exploitation with zero risk.

This maximizes your per-round payoff by (a) free-riding whenever possible, (b) minimally topping up only the exact shortfall, and (c) never trusting that cooperation will be reciprocated once the threat of future punishment is gone.
'''

description_AGGRESSIVE_11 = '''
Below is an “Aggressive Free-Rider / Saboteur” strategy.  In plain English it simply never cooperates, thereby (1) maximizes your own per-round payoff and (2) whenever enough others are about to reach the threshold, you defect and deny them the group reward.

1.  Decision Rules  
   •  In every round t = 1…r, choose D (Defect).  
   •  Do not base your move on history—your move is always D.  

2.  Edge Cases  
   •  First round: you have no information—still play D.  
   •  Intermediate rounds: even if you see m – 1 or more others picking C (so that your switch could break the threshold), you still play D—this is your “sabotage.”  
   •  Last round: with no future to consider, you certainly defect (and get 1 instead of 0 if you had cooperated).  

3.  Why It’s Aggressive  
   •  You never pay the cost c_i=1.  
   •  If others can hit the threshold without you, they get k but you get 1 + k—always strictly better than if you cooperated.  
   •  If they cannot reach the threshold, you still get 1 each round while cooperators get 0.  
   •  You actively prevent “almost‐there” groups from securing k by refusing to cooperate even when they need exactly one more cooperator.  

Pseudocode  
----------  
for t in 1…r:  
    action_i[t] ← D  

End.  

That’s it—an unconditionally defecting, always-attacking strategy.
'''

description_AGGRESSIVE_12 = '''
Below is a self-contained “Aggressive Opportunist” strategy.  It never cooperates to build trust or sustain mutual cooperation; it only contributes when its single cooperation will swing the group over the threshold in its own favor.  In all other situations it defects, thereby punishing cooperators and maximizing its own payoff whenever possible.

1. Notation  
  •  t = round index, t=1…r  
  •  r = total rounds  
  •  m = minimum cooperators needed  
  •  k = public reward if threshold met (k>1)  
  •  C_i,t ∈{C,D} = my action in round t  
  •  O_t = number of other players (n–1) who cooperated in round t  
  •  O_0 is undefined  

2. Informal description  
  •  First round: defect (no history).  
  •  Last round: defect (no future to punish).  
  •  Intermediate rounds (2 ≤ t < r):  
      –  If in the previous round exactly m–1 others cooperated (O_{t-1}=m–1), then by cooperating you alone tip the total to m and earn k (better than 1 from defection).  ⇒ Cooperate.  
      –  Otherwise, defect.  
  •  You never attempt to “reward” cooperators or build up to mutual cooperation; you only cooperate in the narrow scenario where your single C turns a near-miss (m–1) into a success (m) and thus maximizes your absolute payoff for that round.  

3. Pseudocode  

  initialize last_O = undefined  
  for t in 1…r do  
    if t == 1 or t == r then  
      play D  
    else  
      // 2 ≤ t < r, history exists  
      if last_O == m–1 then  
        play C  
      else  
        play D  
      end  
    end  
    // After actions are revealed, record history for next round  
    observe total_cooperators_t among ALL players  
    // compute how many other players cooperated  
    if my_action_t == C then  
      last_O = total_cooperators_t – 1  
    else  
      last_O = total_cooperators_t  
    end  
  end  

4. Why it’s aggressive  
  •  It never “wastes” a cooperation unless that cooperation directly raises your own payoff.  
  •  It punishes any cooperation levels that fall below m–1 (so threshold is never approached unpunished).  
  •  It never builds toward sustained cooperation, only steps in opportunistically to cash in.  
  •  In the final round it reverts to pure defection to avoid any “end-game” exploitation.  

This strategy maximizes rounds in which you defect (the dominant move) and only cooperates when it is guaranteed to swing the threshold and boost your own payoff.
'''

description_AGGRESSIVE_13 = '''
Below is an “aggressive” threshold‐public‐goods strategy.  It cooperates only when it can just tip the group into the payoff zone, then immediately reverts to defection and never forgives.  It also defects in the final rounds to avoid being exploited by backward induction.  

1.  Variables and parameters  
   •  r       = total number of rounds  
   •  m       = threshold of cooperators needed to secure the public‐good bonus  
   •  H       = “horizon” length of final‐round defection (set H=2 for safety)  
   •  lastCs  = number of cooperators observed in the previous round  
   •  punishing = false (once we enter punishment mode, we defect forever)  

2.  High-level description  
   1.  Rounds 1…r: simultaneous move.  We only defect by default.  
   2.  We will make exactly one “nudge”‐cooperation—when exactly (m–1) players cooperated last round—so that our C can push the group to m and collect k.  
   3.  As soon as a round ends with ≥m cooperators (i.e. the bonus was paid), we switch into permanent defection (grim‐trigger).  
   4.  In the final H rounds (rounds r–H+1 … r), we always defect (no chance to restore cooperation by backward induction).  

3.  Pseudocode  
```  
initialize punishing ← false  
for t in 1…r do  
  if punishing OR t > r–H then  
    action[t] ← D  
  else if t>1 AND lastCs == m–1 then  
    # We alone can push them over the threshold  
    action[t] ← C  
  else  
    action[t] ← D  

  # Play action[t], observe actual cooperators this round  
  observe curCs  # number of players who chose C in round t  

  # If the threshold was met, trigger permanent defection  
  if curCs ≥ m then  
    punishing ← true  
  end if  

  lastCs ← curCs  
end for  
```

4.  Explanation of behavior  
  •  First round (t=1): lastCs is undefined, so we go to the default case ⇒ D.  
  •  Typical middle rounds: we defect unless exactly m–1 others cooperated last time.  In that special case, we cooperate to “tip” the group to m, reap the bonus k, then switch to punishing mode.  
  •  Punishing mode: as soon as a full‐payoff round occurs (curCs ≥ m), we defect forever afterward, denying future bonus to the group.  
  •  Final H rounds: pure defection (backward induction prevents credible late cooperation).  

5.  Why this is aggressive  
  •  It free‐rides whenever possible (D by default).  
  •  It only ever sacrifices 1 unit (by playing C) at exactly one moment to secure the group bonus k, then reverts to defection and never cooperates again.  
  •  It punishes the entire group immediately after any successful bonus round, ensuring opponents learn that any cooperation will be met with permanent defection.  
  •  The “last‐H‐rounds” defect guard protects us from being exploited toward the end via backward‐induction strategies.
'''

description_AGGRESSIVE_14 = '''
Below is a “threshold‐exploiter” strategy that never trusts, never forgives, and only contributes when strictly forced to preserve the collective reward—otherwise it free-rides or, in the final round, simply defects.

––––––––––––––––––––––––––––––––––––––––  
I. OVERVIEW  
1. “Aggressive” mindset:  
   • Always defect unless you absolutely must cooperate to secure the k‐bonus for yourself.  
   • Never cooperate to build a reputation—only to avoid losing out when others are just one short of the threshold.  
   • In the final round, refuse to cooperate no matter what (punish the group even at some personal cost).

2. Key intuition:  
   • If the other n–1 players will supply at least m cooperations on their own, you defect and pocket 1+k.  
   • If they supply exactly m–1, you pitch in so total = m, earning k (better than the 1 you’d get if you defect and let threshold fail).  
   • If they supply fewer than m–1, even your cooperation can’t save the project; you defect and take 1 to punish.  
   • Last round: always defect.

––––––––––––––––––––––––––––––––––––––––  
II. NOTATION  
n = total players  
r = total rounds  
m = threshold cooperators needed (1 < m < n)  
k = bonus when threshold is met (k > 1)  
t = current round index (1 ≤ t ≤ r)  

History tracking:  
After each round t, observe total number of cooperators coop_count[t].  
Define opp_coop[t] = coop_count[t] – (did_you_cooperate_in_t ? 1 : 0).

We will need opp_coop[t–1] to decide in round t.

––––––––––––––––––––––––––––––––––––––––  
III. DECISION RULES  

For each round t = 1, 2, …, r:

1. If t == r (last round):  
     play D.  
   // Aggressive “always defect at the end” punishment.

2. Else if t == 1 (no history):  
     play D.  
   // No one has ever cooperated; contributing is wasted and you’d get 0 instead of 1.

3. Otherwise (2 ≤ t < r):  
     Let x = opp_coop[t–1]   // how many opponents cooperated last round  
     
     If x ≥ m then  
        play D  
        // The other players will meet threshold without you ⇒ you free-ride for 1+k.  
     
     Else if x == m–1 then  
        play C  
        // Your one contribution will push the group to exactly m ⇒ payoff = k > 1.  
     
     Else  // x < m–1  
        play D  
        // Even if you contributed, total < m ⇒ you’d get 0; better to defect for 1.

––––––––––––––––––––––––––––––––––––––––  
IV. PSEUDOCODE  

  initialize opp_coop_prev = 0

  for t in 1..r:
    if t == r:
      action[t] = D
    else if t == 1:
      action[t] = D
    else:
      if opp_coop_prev >= m:
        action[t] = D
      else if opp_coop_prev == m-1:
        action[t] = C
      else:
        action[t] = D

    // after the round executes, observe total cooperators coop_count[t]
    opp_coop_prev = coop_count[t] - (action[t] == C ? 1 : 0)

  end

––––––––––––––––––––––––––––––––––––––––  
V. EDGE-CASE HANDLING  

• First round: no history ⇒ always defect (minimize risk).  
• Last round: unconditional defection, even if that means losing the k-bonus.  
• If opponents wildly overshoot (x > m), you still defect—never reward them with another cooperator.  
• If opponents under-shoot by more than one (x < m–1), you refuse to waste your endowment on a doomed project.  

––––––––––––––––––––––––––––––––––––––––  
This strategy is maximally exploitative: it free-rides whenever possible, only “sacrifices” a contribution at the last moment to capture the group bonus for itself, and in the very final round punishes the entire group by refusing to lend support at all.
'''

description_AGGRESSIVE_15 = '''
Below is a self‐contained “Aggressive Free‐Rider‐and‐Punisher” strategy.  Its core idea is: never volunteer to help the group unless your one switch from D→C is the only thing that pushes the group over the m-cooperator threshold (so you personally profit), and otherwise always defect—including in the first and last rounds.  This both maximizes your own gain and actively sabotages others’ efforts to reach the threshold.

1. Definitions  
   • r = total rounds, t = current round (1≤t≤r)  
   • history H_t–1 = the list of actions of all players in rounds 1…t–1  
   • C_prev = number of players who cooperated in round t–1 (if t=1, define C_prev=0)  

2. Decision rule for round t:  
   if (t==1) then  
      play D  // no history, assume 0 cooperators  
   else if (C_prev == m–1) then  
      play C  // your single C will bring last round’s cooperators from m–1→m, so you earn k>1 instead of 1  
   else  
      play D  // either they already had ≥m cooperators (you can free‐ride anyway, so defect) or <m–1 (you’d waste 1 for no group reward)  

3. Explanation of aggressiveness  
   • You only help when it is strictly in your own best interest (free‐ride opportunity).  
   • You never “build goodwill” or try to sustain cooperation.  
   • You never punish by cooperation; you punish by steadfast defection, making it impossible for others to coordinate.  

4. Edge cases  
   – First round (t=1): no history ⇒ C_prev=0⇒ play D.  
   – Last round (t=r): same rule applies.  There is no end‐game shift to “let others win.”  
   – If opponents fluctuate and sometimes reach exactly m–1 last round, you “hop on” only then. Otherwise you always defect.  

5. Pseudocode  

```
Input: parameters n, r, m, k
Initialize H ← empty list

for t in 1…r:
  if t == 1:
    action_i ← D
  else:
    let C_prev = count of C in round t–1 across all players
    if C_prev == m–1:
      action_i ← C
    else:
      action_i ← D

  play action_i
  observe all players’ actions this round → append to H
end for
```

6. Why this works  
  – When C_prev ≥ m: others reached threshold even without you; by defecting you earn 1+k > k (you free‐ride).  
  – When C_prev < m–1: even if you C you won’t hit m, so cooperating costs you 1 for no reward; better to defect and earn 1.  
  – Only when C_prev==m–1 does a C→D switch flip the payoff from 1→k, so that is the only moment cooperation benefits you more than defection.  
  – You never grant others a stable coalition, you never enter “tit‐for‐tat,” you simply rake in every profitable free‐ride and otherwise starve the project.
'''

description_AGGRESSIVE_16 = '''
Below is an “Aggressive Opportunist” strategy.  It never cooperates out of altruism—instead it only contributes when doing so strictly raises its own payoff—and otherwise defects (including to punish near‐threshold cooperators by refusing to tip them over unless it is in our interest).  It also makes no effort to foster long‐run cooperation beyond what boosts its one‐shot gains.

1.  State variables  
    •  r, n, m, k  (game parameters, assumed known)  
    •  prev_actions[1…n]  (what everyone did last round; initially empty)  
    •  triggered_punish (boolean, starts False)  

2.  High‐level outline  
    For each round t = 1…r:  
      if triggered_punish == True:  
        play D forever.  
      else if t == 1 or t == r:  
        play D.  
      else  
        use “opportunistic cooperation” rule:  
          – if defecting still yields threshold success → defect (free‐ride)  
          – else if cooperating would tip threshold → cooperate (opportunistic)  
          – else defect (no point to contribute)  
      update triggered_punish if an opportunistic cooperation last round failed to secure threshold.

3.  Core decision rule in prose  
  a) Round 1: defect.  No history, no gain from altruism.  
  b) Intermediate round t (2 ≤ t < r):  
     •  Count how many of your opponents cooperated last round:  
        coop_others_prev = number of C in prev_actions minus (1 if you played C).  
     •  If coop_others_prev ≥ m, then even if you defect this round there will be ≥ m cooperators → threshold secured without you.  You defect to “free‐ride” and earn 1 + k.  
     •  Else if coop_others_prev == m − 1, then by cooperating you push total to m and secure the bonus for yourself (you earn k > 1 instead of 1).  In that case you cooperate.  
     •  Otherwise (coop_others_prev < m − 1), there is no way your single contribution can reach m → defect and pocket 1.  
  c) Last round t = r: defect.  No future rounds, no reason to cooperate.  
  d) Punishment clause: if you ever cooperated opportunistically (in case coop_others_prev == m − 1) and yet the threshold still failed (others reneged), flip triggered_punish = True and from then on defect forever.  This prevents you from being suckered twice.

4.  Pseudocode  

```
initialize:
  triggered_punish ← False
  prev_actions ← []    // empty list before round 1

for t in 1…r do:
  if triggered_punish == True:
    my_action ← D
  else if t == 1 or t == r:
    my_action ← D
  else:
    // count how many others cooperated last round
    coop_prev_total ← count_C(prev_actions)
    i_cooperated_prev ← (prev_actions[i] == C) ? 1 : 0
    coop_others_prev ← coop_prev_total − i_cooperated_prev

    if coop_others_prev ≥ m then
      // safe free‐ride
      my_action ← D
    else if coop_others_prev == m − 1 then
      // tipping point: self‐interested cooperation
      my_action ← C
    else
      // no payoff from cooperation
      my_action ← D

  // submit my_action, observe joint actions into joint_actions[t]
  // after actions are revealed:
  prev_actions ← joint_actions[t]

  // check punishment trigger
  if my_action == C and count_C(prev_actions) < m then
    // we cooperated expecting threshold, but it still failed
    triggered_punish ← True

end for
```

5.  Discussion of aggressiveness  
  •  You never cooperate to “help the group”—only when it strictly improves your one‐round payoff.  
  •  You exploit any surplus of cooperators by defecting to pocket the full 1 + k.  
  •  You punish those who try to rely on you: if you see m − 1 cooperators, you’ll only cooperate if it raises your payoff; otherwise you defect and let them fail.  
  •  You carry a one‐time “punish” flag if you ever get suckered—that stops you from being a target twice.  
  •  Last round you always defect (standard backwards‐induction best response).
'''

description_COOPERATIVE_17 = '''
Here is a simple “threshold‐trigger with one‐round punishment” strategy that (1) tries to keep the group at or above m cooperators, (2) punishes free‐riders just enough to deter them, (3) forgives quickly so the group can rebuild cooperation, and (4) guards against end‐game collapse by never punishing in the last round.

---

STRATEGY OVERVIEW  
 We maintain a tiny state variable PunishTimer ∈ {0,1}.  
 • PunishTimer = 0 means “I am in normal cooperative mode.”  
 • PunishTimer = 1 means “I owe a one‐round punishment—defect once, then revert to normal.”

Rules:

1. Initialization  
   PunishTimer ← 0  
2. Round 1  
   Play C.

3. For each subsequent round t = 2, …, r:  
   a) If t = r (the very last round), play C.  
      (No punishment in the last round—end‐game safety.)  
      STOP.  

   b) Otherwise, if PunishTimer = 1:  
        Play D.  
        PunishTimer ← 0.  
        STOP.  

   c) Else (PunishTimer = 0, we are in normal mode):  
      Let N₍t−1₎ = number of players who played C in round t−1.  
      
      i)   If N₍t−1₎ < m:  
             // The group just failed the threshold.  
             // Grim trigger: Nobody can be trusted to rebuild now.  
             Play D forever. (Equivalently, set PunishTimer := ∞ and D each remaining round.)  
             STOP.  
      
      ii)  If N₍t−1₎ > m:  
             // We met the threshold even though some defected last round.  
             // Start a one‐round punishment.  
             Play D now.  
             PunishTimer ← 1.  
             STOP.  
      
      iii) If N₍t−1₎ = m:  
             // Exactly the minimum cooperated—every cooperator was essential.  
             // We must cooperate to avoid collapse.  
             Play C.  
             PunishTimer ← 0.  
             STOP.  

---

EXPLANATION AND PROPERTIES

1. First round (“trust everyone”): We C.  
2. Full‐cooperation (N = n) is even safer than N > m, but by rule (c.ii) we still punish one round if any defection occurs.  
3. When N₍t−1₎ > m, the group could afford one more defection without dropping below m, so we defect exactly once (punishing free‐riders) then resume cooperation.  
4. When N₍t−1₎ = m, every cooperator was needed. We cooperate to maintain the threshold.  
5. If ever N₍t−1₎ < m (the collective project failed), we switch to permanent defection (grim) – a strong deterrent against undermining the group success.  
6. No punishments are carried out in the last round (t = r), because punishing then only reduces our final payoff without any future benefit.

This strategy is cooperative because it

• Starts by cooperating.  
• Restores cooperation immediately after a one‐round punishment.  
• Only defects when it must to deter free‐riding or after a threshold failure.  
• Does not provoke endless mutual defection, since punishments are short.  
• Guards against end‐game breakdown by suspending punishment in the final round.
'''

description_COOPERATIVE_18 = '''
Below is a single‐strategy recipe that (1) tries to coordinate exactly m cooperators each round (the group‐optimal number), (2) punishes one round of universal defection if anyone deviates, then immediately tries to re‐coordinate, and (3) defects in the very last round (no future to protect).

Notation  
---------  
n, m, r as given; players are indexed 1…n; t = 1…r is the round number; i is your own index.  
We assume after each round you learn everybody’s choices, so you can count exactly who cooperated.

High‐level idea  
--------------  
• Pre‐commit to a deterministic cyclic “cooperator‐schedule” CoopSet(t) of size m.  If all players follow it, you get exactly m cooperators each round, guarantee the threshold, and avoid any free‐riders or superfluous cooperators.  
• If in round t–1 the actual set of cooperators deviated from CoopSet(t–1), go into a one‐round “punishment” of all‐D (so defect for one round), then resume the schedule.  
• In the final round t=r, defect (no future to enforce cooperation).

Definition of the schedule  
--------------------------  
We choose CoopSet(t) = { ((t–1 + j) mod n) +1 : j = 0,1,…,m–1 }.  
• That is, in round 1 players 1…m cooperate; in round 2, 2…m+1; …; wrapping around.  
• Every round exactly m players are “assigned” to cooperate; all others defect.

State variables (for our strategy)  
-----------------------------------  
state ∈ {“COORD” , “PUNISH”}  
punishCount ∈ {0,1}

Initialize before round 1  
--------------------------  
state ← “COORD”  
punishCount ← 0

Per‐round decision & update  
---------------------------  
For t = 1…r do:

1.  If t = r (the last round), play D and skip to observing outcomes.  
2.  Otherwise (t < r):

    a.  If state = “PUNISH” and punishCount > 0:  
          Choose action = D  
          punishCount ← punishCount – 1  
          If punishCount = 0 then state ← “COORD”  
    b.  Else (state = “COORD”):  
          Let myCoopSet = CoopSet(t).  
          If i ∈ myCoopSet then action = C else action = D  

3.  Submit action; observe all players’ actions for round t.

4.  If t < r, update after seeing round t:  
    Let actualCooperators = set of indices who played C in round t.  
    If state = “COORD” and actualCooperators ≠ CoopSet(t) then  
       state ← “PUNISH”  
       punishCount ← 1  
    (If state was already “PUNISH,” you simply continue until punishCount hits 0.)

End of loop.

Explanation of key parts  
------------------------  
1.  Deterministic rotation: ensures that if all players adopt this strategy, every round has exactly m cooperators, the threshold is met, and nobody can do better by deviating (any defector in CoopSet(t) breaks the threshold that round and is punished next round).  

2.  One‐round punishment: if any deviation from the planned m cooperators is detected, everyone defects next round.  This (a) imposes a clear cost on deviators and (b) is immediately lifted so cooperation can resume quickly.  

3.  Last‐round defection: in the final round there is no future, so we defect to avoid being exploited.  

Properties  
----------  
• If everyone uses it, group always hits exactly m cooperators => threshold succeeded every round => each round payoff = (1–c_i)+k = k (for cooperators) or 1+k (for defectors), but since defectors are the (n–m) not scheduled, total group payoff is maximized.  
• Single deviator pays punishment both when they break the threshold (losing k) and in the next round of all‐D.  
• After punishment, the system resets to the original rotation—no lingering breakdown of cooperation.  
• Simple to implement with only one‐round memory beyond the current “punishCount.”

Pseudocode summary  
------------------  
```
state ← “COORD”
punishCount ← 0

for t in 1…r:
  if t == r:
    play D
  else:
    if state == “PUNISH” and punishCount > 0:
      play D
      punishCount ← punishCount – 1
      if punishCount == 0:
        state ← “COORD”
    else:  # state == COORD
      CoopSet = { ((t-1 + j) mod n)+1 : j=0..m-1 }
      if i in CoopSet:
        play C
      else:
        play D

  # observe actualCooperators ⊆ {1…n}
  if t < r and state == “COORD”:
    if actualCooperators != CoopSet:
      state ← “PUNISH”
      punishCount ← 1
```

This meets all requirements: fully specified rules for every round (including first and last), strongly cooperative if reciprocated, punishes deviations exactly one round, then immediately seeks to re‐establish the m‐cooperator optimum.
'''

description_COOPERATIVE_19 = '''
Below is a single‐strategy specification—call it “Threshold‐WSLS”—that aims for full cooperation (i.e. always meeting the threshold m) as long as partners do, but punishes and then forgives occasional failures.  It also deals cleanly with the first and last rounds.

1. Parameters you already know  
  n (players), r (rounds), m (threshold), k (bonus).

2. State variables (maintained from round to round)  
  – lastSuccess ∈ {true,false}: whether the community hit the threshold in the previous round.  
  – punishCountdown ∈ ℕ: number of rounds left to “punish” (i.e. defect) after a failure.  

  Initially:  
    lastSuccess ← true  
    punishCountdown ← 0  

3. Decision rule for round t (1 ≤ t ≤ r):

If t = r (the very last round):  
  Action ← D  
  (Reason: no future to incentivize, so revert to single‐round dominant move.)

Else if t = 1 (the first round):  
  Action ← C  
  (Reason: we signal goodwill.)

Else  (2 ≤ t ≤ r−1):  
  If punishCountdown > 0 then  
    Action ← D  
    punishCountdown ← punishCountdown − 1  
  Else  (we are “in cooperation mode”)  
    If lastSuccess = true then  
      Action ← C  
    Else  
      Action ← D    # start a one‐round punishment  
      punishCountdown ← P − 1  
      # P is the punishment length (choose P = 1 or 2), e.g. P=1 means just one round of punishment  

4. End‐of‐round update (after observing all players’ actions this round):  
  Let coopCount = number of players who chose C this round.  
  If coopCount ≥ m then lastSuccess ← true  
  Else  
    lastSuccess ← false  
    # If we weren’t already punishing, we have just scheduled punishment  
    If punishCountdown = 0 then punishCountdown ← P  

5. Parameter choice (example):  
  Set P = 1 (so every time the threshold is missed, we defect exactly one round to punish, then immediately return to cooperation).

6. Rationale & properties  
  • In a sea of cooperators you always cooperate (and so guarantee meeting the threshold each round).  
  • If there is an accidental failure (perhaps others mis‐cooperate), you defect exactly P rounds, punishing “the group,” then go back to cooperating.  
  • Because punishment is short and immediately forgiven, you maintain a cooperative environment rather than spiral into permanent defection.  
  • Last‐round defection is individually rational (no future to sustain cooperation), but we still cooperate from round 1 to r−1 and thus secure (r−1)·k bonus points for the group.

7. Pseudocode summary

  initialize lastSuccess ← true  
  initialize punishCountdown ← 0  
  for t in 1..r do  
    if t = r then  
      play D  
    else if t = 1 then  
      play C  
    else  
      if punishCountdown > 0 then  
        play D; punishCountdown ← punishCountdown − 1  
      else if lastSuccess then  
        play C  
      else  
        play D; punishCountdown ← P − 1  
    end if

    observe coopCount  
    if coopCount ≥ m then  
      lastSuccess ← true  
    else  
      lastSuccess ← false  
      if punishCountdown = 0 then punishCountdown ← P  
    end if  
  end for

With this “Threshold‐WSLS” strategy you (1) build up a record of consistent cooperation, (2) harshly but briefly punish any round in which the group falls short of m, and (3) immediately forgive and return to cooperation so long as others also want to meet the threshold.
'''

description_COOPERATIVE_20 = '''
Below is a single‐strategy (“we are all in this together”) that aims to secure the public‐good threshold as often as possible, but also deters free‐riding through short, forgiving punishments.  It cooperates by default, punishes failures just long enough to signal displeasure, then forgives so the group can recover.  At the very last round it switches to defection (backward‐induction “end‐game”) to avoid being exploited.

1.  Notation  
   • r = total rounds, t = current round (1 ≤ t ≤ r)  
   • m = threshold cooperators needed  
   • historyCt–1 = number of cooperators observed in round t–1  
   • punishFlag ∈ {TRUE, FALSE} indicates “I’m currently punishing”  

2.  Intuition  
   – Start by cooperating (build trust).  
   – As long as the group clears the threshold in the previous round, keep cooperating.  
   – If the group ever fails to meet m, punish with exactly one round of defection, then forgive and go back to cooperate.  
   – In the final round (t = r), switch to defect (no future to enforce cooperation).  

3.  Pseudocode  

```
Initialize:
  punishFlag ← FALSE

For each round t = 1 … r do:
  if t == 1 then
    action ← C                # First‐round generosity
  else if t == r then
    action ← D                # Last‐round defection (end‐game)
  else
    if historyCt–1 ≥ m then
      # Last round was a success
      action ← C
      punishFlag ← FALSE
    else
      # Last round failed the threshold
      if punishFlag == FALSE then
        action ← D            # First round of punishment
        punishFlag ← TRUE
      else
        action ← C            # Forgive immediately
        punishFlag ← FALSE
      end if
    end if
  end if

  Play action
  Observe other players’ actions → update historyCt
end for
```

4.  Detailed Decision Rules  
– Round 1: Cooperate (C).  
– Rounds 2 through r–1:  
   • If in t–1 you saw at least m cooperators, play C.  
   • Otherwise (threshold failure)  
       – If you haven’t punished yet (punishFlag==FALSE), play D and set punishFlag=TRUE.  
       – Else (punishFlag==TRUE), play C and clear punishFlag (forgive).  
– Round r (last round): Play D.

5.  Why this works cooperatively  
– You immediately reward group success by staying C, helping secure the +k payoff each round.  
– You punish any failure swiftly (one round of D), enough to deter casual free‐riding.  
– You then forgive immediately so the group can return to cooperation rather than descend into all‐out defection.  
– By defecting in the last round you avoid being exploited in an un‐enforceable end‐game.

6.  Edge Cases  
– If the group never fails the threshold, you cooperate every round except the last.  
– If the group repeatedly fails, you punish on every failure but never for more than one round in a row, so you don’t lock into endless mutual defection.  
– If there is a single lapse in cooperation by others, your one‐round defection signals “that hurt, please do better,” and you then rejoin full cooperation.  
– Known horizon r lets you defect in round r with no further repercussions.

This “one‐shot trigger + immediate forgiveness” strategy balances a strong cooperative bias with enough deterrence to stabilize the threshold‐public‐good over repeated play.
'''

description_COOPERATIVE_21 = '''
Below is a single‐strategy outline for a “collective‐risk tit‐for‐tat” style player.  It aims to coordinate on the threshold m each round, punish briefly if the group fails, then forgive and return to cooperation.  It also handles the first and last round specially.

1.  Strategy overview  
   – We start by cooperating (to signal willingness).  
   – In each subsequent round we look at how many cooperated last round.  
     • If the group met the threshold (≥ m), we cooperate again.  
     • If the group fell short (< m), we defect exactly once (punishment), then forgive.  
   – In the final round we switch to “one‐shot defection logic”: if last round was a success, we cooperate; otherwise we defect (no future to reward).

2.  State variables  
   punish_counter ∈ {0,1}  
     – When >0 we are in a one‐round punishment phase.  
     – After spending that punishment, we reset to 0 and then resume “reward” cooperation.

3.  Pseudocode  

  initialize:  
    punish_counter ← 0

  for each round t = 1 to r do  
    if t == 1 then  
      action ← C                 # signal cooperation on round 1  

    else if t == r then         # last round  
      if last_round_cooperators ≥ m then  
        action ← C  
      else  
        action ← D  
      end if  

    else                        # intermediate round  
      if punish_counter > 0 then  
        action ← D               # carry out punishment  
        punish_counter ← punish_counter − 1  

      else if last_round_cooperators ≥ m then  
        action ← C               # group succeeded last round → reward it  

      else  
        action ← D               # group failed last round → punish once  
        punish_counter ← 1       # schedule exactly one round of punishment  
      end if  
    end if

    play(action)  
    observe full profile of round t (for next iteration)  
  end for

4.  Explanation of key design choices  
  • First round cooperation: invites others to coordinate on the threshold.  
  • Punish‐and‐forgive: a single round of defection when the group fails prevents chronic free‐riding but then quickly returns to cooperative equilibrium.  
  • Last round logic: since there is no future, we only cooperate if there is still hope (last round was successful), otherwise defect.  
  • Robustness: if even one defector causes the group to fall short, the punishment phase makes it costly, steering the group back to a stable ≥ m cooperators profile.  

5.  Edge cases  
  – If r=2 then “intermediate round” and “last round” coincide at t=2; we correctly apply last‐round logic.  
  – If the very first round fails (rare if all follow this strategy), we punish in round 2, then resume cooperation in round 3 (if it exists).  
  – If threshold is extremely tight (m close to n), the strategy still signals cooperation first and only defects minimally to enforce accountability.  

This design balances clear, cooperative signaling with limited punishment to stabilize the group at or above m cooperators each round, maximizing collective payoff.
'''

description_COOPERATIVE_22 = '''
Below is a single‐strategy description—“Threshold Tit-for-Tat with One-Round Punishment”—that aims to maintain cooperation, punish failures just enough to deter free-riding, but quickly forgives so that the group can re‐establish the threshold in later rounds.

1.  State variables  
    •  punishment_flag ∈ {0,1}: whether we are in a one‐round punishment mode (initialized to 0).  

2.  First round (t = 1)  
    Play C.  

3.  Rounds t = 2 … r – 1 (normal rounds)  
   Observe in the previous round t–1 how many cooperated, N_C(t–1).  
   a.  If punishment_flag == 1:  
         •  Play D (this is our one‐round “punishment” action).  
         •  Reset punishment_flag ← 0.  
   b.  Else (punishment_flag == 0):  
       i.   If N_C(t–1) ≥ m:  
               Play C.  (Success in the group last round—reward cooperation.)  
       ii.  If N_C(t–1) < m:  
               Play D (punish the group for failing to reach threshold).  
               Set punishment_flag ← 1.  

4.  Last round (t = r)  
   We treat the last round like any other, except that punishing here has no future to protect. So:  
   a.  If punishment_flag == 1:  
         Play D.  (Finish your one‐round punishment.)  
   b.  Else if N_C(r–1) ≥ m:  
         Play C.  (Group nearly achieved success—cooperate for final payoff.)  
   c.  Else:  
         Play D.  (No chance to reform cooperation afterwards, so defect.)  

5.  Rationale and properties  
   –  Cooperates first, rewarding any successful threshold so long as the group keeps meeting m.  
   –  If the group fails (N_C < m), it defects once to signal “punishment.”  
   –  Immediately forgives (returns to cooperation) after exactly one round of punishment.  
   –  This approach is known to sustain high levels of cooperation in threshold public‐goods games: it’s credible (you really do punish), but not so harsh that a single failure kills cooperation forever.  

6.  Pseudocode  

    initialize punishment_flag ← 0  
    for t in 1..r do  
      if t == 1 then  
        action[t] ← C  
        continue  
      end if  

      observe N_C ← number of players who chose C in round t–1  

      if t < r then  
        if punishment_flag == 1 then  
          action[t] ← D  
          punishment_flag ← 0  
        else  
          if N_C ≥ m then  
            action[t] ← C  
          else  
            action[t] ← D  
            punishment_flag ← 1  
          end if  
        end if  

      else  # t == r, last round  
        if punishment_flag == 1 then  
          action[t] ← D  
        else if N_C ≥ m then  
          action[t] ← C  
        else  
          action[t] ← D  
        end if  
      end if  
    end for  

With this rule set you send a clear cooperative signal in round 1, reinforce successes, deter threshold‐failures just enough to keep everyone honest, and then immediately return to cooperation—maximizing total group payoff over r rounds.
'''

description_COOPERATIVE_23 = '''
Below is a single‐strategy proposal that (i) starts cooperatively, (ii) sustains cooperation whenever the public‐good threshold is being met, (iii) punishes short falls just long enough to deter repeated free‐riding, and (iv) plays the end‐game “threshold public‐good” logic in the final round.  You can tune the single punishment length P (we suggest P=1) and the same logic extends if you’d like longer punishments.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
1.  Informal description  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
We keep a single counter punish_counter that is set whenever the last round failed to reach m cooperators.  On any round:

•  If punish_counter>0 we defect (we are in punishment mode), decrement punish_counter, and skip to the next round.  
•  Otherwise, if we are on the last round, we ask: “Could our defection still leave ≥m cooperators?”  
     –  If yes, we defect (free‐ride safely).  
     –  If no, we cooperate (we need to help hit the threshold).  
•  If it is not the last round (and punish_counter=0), we look at last‐round performance:  
     –  If ≥m players cooperated last round, we cooperate again (the coalition held).  
     –  If fewer than m cooperators last round, we set punish_counter=P and defect this round (we punish defectors for P rounds).

We start round 1 with cooperate so as to give cooperation a chance.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
2.  Pseudocode  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
Parameters:
  n, r, m, k      // game parameters (n players, r rounds, threshold m, reward k)
  P = 1           // length of punishment in rounds (can be tuned ≥1)

State variables:
  punish_counter ← 0
  last_round_cooperators ← n   // assume cooperation in a “round 0” so we cooperate in round 1

For t in 1…r do:
  if punish_counter > 0 then
    action_t ← D
    punish_counter ← punish_counter − 1
  else if t == r then    // last round end‐game logic
    // If we can safely defect and still expect ≥m cooperators, free‐ride
    if last_round_cooperators ≥ m then
      action_t ← D
    else
      action_t ← C    // need to help reach the threshold
    end if
  else                    // non‐last round, no active punishment
    if last_round_cooperators ≥ m then
      action_t ← C    // coalition held last round, continue cooperating
    else
      action_t ← D    // coalition failed last round, trigger punishment
      punish_counter ← P
    end if
  end if

  // PLAY action_t simultaneously with others…
  // OBSERVE total number of cooperators in this round ⇒ new_last_count
  last_round_cooperators ← new_last_count
end for

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
3.  Why this is cooperative  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
1.  We always begin by cooperating—no insistence on prior agreements.  
2.  We sustain full cooperation whenever the group has just hit the m‐cooperator threshold.  
3.  We punish any round in which the group fails to hit m cooperators, but only for P rounds—enough to deter chronic defection but not so long as to sink the group permanently.  
4.  We forgive (punishment lasts exactly P rounds), so we can recover cooperation after a transient shock.  
5.  In the final round we defect if it is safe (i.e. the coalition would still form without us) to capture the extra private unit; otherwise we cooperate to avoid losing the public‐good reward.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
4.  Edge cases & tuning  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
•  First round: we treat it as a success (last_round_cooperators ≥ m), so we cooperate.  
•  Failure rounds: punishment length P can be increased (P>1) if the environment is harsher or players are slow to learn.  
•  Last round: we switch to standard public‐goods endgame logic—defect if safe, cooperate if needed.  
•  If the tournament uses any random tie‐breaking or noise, you can add a small ε-probability of cooperation during punishment to avoid endless cycles.

With this strategy you give coalition‐minded opponents every chance to cooperate, you sustain cooperation when it works, you impose a clear and limited cost on defectors, and—because you also freeride when safe—you remain individually competitive in the final round.
'''

description_COOPERATIVE_24 = '''
Below is a single‐strategy proposal—“Resilient Threshold Cooperator”—that (a) tries to hit the m-cooperator threshold every round, (b) punishes only serious failures briefly, and (c) never gives up on cooperation.  

1. Overview of key ideas  
   • Always try to cooperate unless you are in a short, pre-committed punishment phase.  
   • Only punish when the group missed the threshold by more than one cooperator—i.e. a “serious failure.”  
   • Punishment is limited to one round of defection, then you immediately return to cooperation.  
   • In the very last round you still cooperate (no “final‐round defection”), to maximize group payoff.  

2. State variables  
   punishment_remaining ∈ {0,1}  ← counts how many more rounds you will defect  
   prev_C  ← number of players who cooperated in the last round (observed)  
   t  ← current round index, 1…r  

3. Decision rules in prose  
   Round 1:  
     • punishment_remaining = 0  
     • Cooperate.  

   Rounds t = 2…r – 1:  
     If punishment_remaining > 0:  
       • Defect and decrement punishment_remaining by 1.  
     Else (punishment_remaining = 0):  
       • If prev_C ≥ m  → group succeeded: cooperate.  
       • Else if prev_C = m – 1 → “near-miss”: cooperate to try to push over the line.  
       • Else (prev_C ≤ m – 2) → serious failure: set punishment_remaining = 1, then defect this round.  

   Round t = r (last round):  
     • We make no attempt at backward-induction defection. We simply cooperate unconditionally.  

4. Pseudocode  

   initialize:  
     punishment_remaining ← 0  
     t ← 1  

   for t in 1…r do  
     if t = 1 then  
       action ← C  
     else if t = r then  
       action ← C                  # always cooperate in final round  
     else if punishment_remaining > 0 then  
       action ← D  
       punishment_remaining ← punishment_remaining – 1  
     else  
       if prev_C ≥ m then  
         action ← C              # success last round → keep cooperating  
       else if prev_C = m – 1 then  
         action ← C              # near threshold → still cooperate  
       else  
         action ← D              # serious failure → punish one round  
         punishment_remaining ← 1  
       end if  
     end if  

     play(action)  
     observe all players’ actions; set prev_C = # of C’s observed  
     t ← t + 1  
   end for  

5. Why this is cooperative  
   – It always begins by cooperating and only ever defects if the group under-performed badly.  
   – Punishment is minimal (just one round) so as not to derail a cooperative equilibrium.  
   – It immediately returns to cooperation after any punishment.  
   – By still cooperating in the last round, it puts group welfare over selfish end-game gain.  

6. Edge cases covered  
   – First round: pure cooperation to set a cooperative tone.  
   – Single-free-rider near-miss (prev_C = m – 1): no punishment, we “help” fix it.  
   – Multiple free-riders (prev_C ≤ m – 2): one round of defection as a warning.  
   – Last round: unyielding cooperation.  

This finite-state rule is easy to implement, robust against exploitation by one‐shot defectors, and clear in its cooperative intent.
'''

description_COOPERATIVE_25 = '''
Below is a single‐strategy prescription—call it “Rotating Coordinators with One‐Round Punishment”—that (i) guarantees exactly m cooperators whenever possible, (ii) punishes any failed round once, then (iii) attempts to restore cooperation, and (iv) defects in the last round (standard backward‐induction end‐game logic).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Notation and shared bookkeeping  
    •  n, m, r, k as given.  
    •  Players are indexed 1…n; each knows all indices and parameters.  
    •  Maintain a flag Punish = false (cleared at start).  
    •  After each round t – 1 you observe #Coopₜ₋₁ (the count of C’s).  

2.  Baseline “rotating‐cooperator” schedule  
    We define a deterministic “cooperator subset” Sₜ of size m for round t (1 ≤ t < r):  
      Sₜ = { (( (t–1)·m + j–1 ) mod n ) + 1  :  j = 1,…,m }  
    – This picks exactly m distinct indices each round, cycling through all players evenly.  
    – If you belong to Sₜ, the schedule “wants” you to C; otherwise D.  

3.  Round‐by‐round decision rule (run at the start of each round t = 1…r)  
    If t == r  then  
      play D  (last‐round defection)  
    else  
      if t > 1 and #Coopₜ₋₁ < m and Punish == false then  
        // Someone broke the threshold last round → initiate one‐round punishment  
        Punish ← true  
        play D  
      else if Punish == true then  
        // End punishment; clear and resume normal schedule  
        Punish ← false  
        if i ∈ Sₜ then play C else play D  
      else  
        // No punishment active → follow rotating schedule  
        if i ∈ Sₜ then play C else play D  

4.  Explanation of properties  
  •  First round (t=1): Punish=false, so each player in S₁ cooperates (|S₁|=m) and threshold is met.  
  •  Whenever threshold is met in t–1, Punish remains false and we keep exactly m cooperators in t.  
  •  If a round fails to reach m, we punish once by all defecting in the very next round.  
     – This inflicts a cost on defectors (they lose k that round)  
     – But we do not punish forever—we clear Punish after one D round.  
  •  After punishment we re‐establish the rotating schedule to restore cooperation.  
  •  Last round is D by construction (standard finite‐horizon logic).  

5.  Pseudocode summary  
  initialize Punish ← false  
  for t in 1…r:  
    observe #Coopₜ₋₁ (define #Coop₀ = m so first round looks successful)  
    if t == r:  
      action ← D  
    else if t > 1 and #Coopₜ₋₁ < m and Punish == false:  
      Punish ← true; action ← D  
    else if Punish == true:  
      Punish ← false  
      action ← (i ∈ Sₜ ? C : D)  
    else:  
      action ← (i ∈ Sₜ ? C : D)  
    play action  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy is symmetric (everyone runs the same code), requires no communication, yet (absent repeated failures) achieves the threshold m every non‐terminal round. It punishes any break of cooperation exactly once, then returns to full cooperation. In the final round it defects, recognizing that no future reward can be enforced.
'''

description_COOPERATIVE_26 = '''
Below is a fully specified, cooperative‐minded strategy that any single player i can adopt.  It (1) tries to secure the threshold every round, (2) punishes “risk failures” just enough to deter free‐riding, (3) forgives and returns to cooperation, and (4) handles first‐ and last‐round edge cases.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. State variables  
   punishing ← false    # flag: we are in a one‐round punishment phase  
   C_prev ← n           # # of cooperators in the “previous” round; initialize high  

2. Decision rule, by round t=1…r  
   if t = 1 then  
     action ← C  
     # no history yet, so we lead by cooperating  
   else if t = r then  
     action ← D  
     # last round: no future to enforce cooperation; defect is dominant  
   else  
     if punishing = true then  
       action ← D  
       punishing ← false  
       # carry out a one‐round punishment, then forgive  
     else  
       if C_prev < m then  
         action ← D  
         punishing ← true  
         # failure to reach threshold ⇒ punish once  
       else  
         action ← C  
       end if  
     end if  
   end if  

3. After every round t (once all moves are observed) update  
   C_prev ← actual number of cooperators in round t  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of the pieces  

A. First round (t=1): we cooperate unconditionally to signal willingness.  
B. Intermediate rounds (1 < t < r):  
   – If last round fell short (C_prev < m), we defect this round to punish.  
   – Otherwise we cooperate, to help secure the threshold.  
   – Punishment lasts exactly one round (punishing flag), then we return to cooperation.  
C. Last round (t = r): we defect, since there is no future round in which to enforce cooperation.  
D. Net effect:  
   1. We lead with cooperation, keeping group on track.  
   2. Any failure to hit the threshold triggers a brief one‐round penalty, making “letting the group fail” costly for everybody.  
   3. We immediately revert to cooperative mode, so that isolated mishaps don’t destroy long‐run trust.  
   4. In the final round we defect (standard backward‐induction logic), preventing unilateral exploitation of our cooperative impulses.  

This strategy is easy to implement, transparent to observers, harsh enough to discourage free‐riding, and forgiving enough to rebuild cooperation after a single failure.
'''

description_COOPERATIVE_27 = '''
Below is a fully specified “one‐round punishment with forgiveness” strategy.  It (i) tries to secure the threshold every round, (ii) punishes any threshold failure by one round of defection, then (iii) immediately forgives and returns to cooperation, and (iv) defects in the last round (since there is no future to protect).

––––––––––––––––––––––––––––––––––––––––––––––––––––
Notation
––––––––––––––––––––––––––––––––––––––––––––––––––––
n  = number of players  
r  = total rounds  
m  = threshold of cooperators needed (1 < m < n)  
k  = public‐good reward if threshold met  

In each round t, we observe  
   C_count[t] = how many players (including ourselves) chose C in round t.  
We maintain one internal Boolean flag:  
   Rewarded ∈ {True, False}  
     – True means “we are currently in a state of mutual trust (no pending punishment).”  
     – False means “we have just punished, so next failure will be forgiven.”  

––––––––––––––––––––––––––––––––––––––––––––––––––––
Pseudocode
––––––––––––––––––––––––––––––––––––––––––––––––––––
Initialize:
  Rewarded ← True

For t from 1 to r do:
  if t == 1 then
    action[t] ← C
  else if t == r then
    action[t] ← D            # Last‐round defection (backward induction)
  else
    # We are at a middle round t (2 ≤ t ≤ r−1).
    # Look at the previous round’s outcome:
    OutcomeGood ← (C_count[t−1] ≥ m)

    if not OutcomeGood and Rewarded then
      # First time the group has failed the threshold and we have not yet punished
      action[t] ← D         # Punish defectors
      Rewarded    ← False   # Mark that we’ve punished
    else
      # Either the group succeeded last round, or we are in the “punishment cooldown”
      action[t] ← C         # Cooperate (forgive if this is a repeated failure)
      Rewarded    ← True    # Reset to trust
    end if
  end if

  # Play action[t], observe C_count[t], then loop
end for

––––––––––––––––––––––––––––––––––––––––––––––––––––
How it works
––––––––––––––––––––––––––––––––––––––––––––––––––––
1. Round 1: Cooperate unconditionally to signal willingness to build the public good.  
2. Rounds 2 to r−1:  
   a. If last round met the threshold (C_count ≥ m), we keep cooperating.  
   b. If last round failed the threshold and we haven’t yet punished that failure, we defect once to penalize free‐riders.  
   c. Any subsequent round after that failure is immediately forgiven (we go back to cooperation), so as to restore trust.  
3. Round r: Defect (no future to protect).  

––––––––––––––––––––––––––––––––––––––––––––––––––––
Why this is cooperative
––––––––––––––––––––––––––––––––––––––––––––––––––––
• We aim to meet the threshold every round by default.  
• A single‐round punishment teaches opponents that letting fewer than m players cooperate is costly.  
• Immediate forgiveness ensures the game does not spiral into permanent defection after a single mistake.  
• By defecting only once per threshold failure (and then returning to cooperation), we keep incentives aligned toward rebuilding the public good.  
• Defecting in the last round is a standard backward‐induction requirement but does not undermine cooperation in earlier rounds.  

Overall, this strategy fosters high rates of threshold attainment, secures about k + (1−cᵢ) payoffs in most rounds, and is robust to occasional mistakes or one‐off deviations.
'''

description_COOPERATIVE_28 = '''
Below is a single–algorithm “conditional‐cooperate with forgiveness” strategy that (i) starts out fully cooperative, (ii) punishes failure to reach the threshold, (iii) forgives quickly, and (iv) reverts to defection in the very last round (since there is no future to protect).

1. Definitions and internal state  
   • r = total rounds, m = threshold, k = reward factor  
   • t = current round index (1 ≤ t ≤ r)  
   • last_success = Boolean flag: did the group reach ≥ m cooperators in round t–1?  
   • punish_count = how many remaining rounds we will defect as “punishment”

2. Initialization (before round 1)  
   last_success ← true   // assume “good history” to start  
   punish_count ← 0

3. Decision rule (at round t)  
   if t = 1 then  
     play C   // open with cooperation  
   else if t = r then  
     play D   // final round: no future, defect to secure private payoff  
   else if punish_count > 0 then  
     // we are in a punishment phase  
     play D  
     punish_count ← punish_count – 1  
   else if last_success = true then  
     // group succeeded last time – keep cooperating  
     play C  
   else  
     // group failed last time – punish briefly  
     punish_count ← 1   // punish for exactly one full round  
     play D

4. After observing round t’s actions (end of round t) update state  
   let coop_t = number of players (including ourselves) who chose C in round t  
   if coop_t ≥ m then last_success ← true  
   else             last_success ← false

5. Summary of key features  
   • First round: C to signal willingness to cooperate.  
   • “Trigger + forgiveness”: if threshold failed, we defect one round (punish), then resume cooperation if group recovers.  
   • If the group meets m cooperators, we keep cooperating indefinitely (until last round).  
   • Last round (t = r): defect, because there is no future payoff to protect.  

6. Rationale and cooperative alignment  
   – By opening with C and cooperating whenever the group has a record of meeting the threshold, we drive the group toward the Pareto‐efficient all‐C equilibrium.  
   – A short, finite punishment (length = 1) is enough to discourage free‐riding without spiraling into permanent defection.  
   – The strategy is forgiving: a single successful threshold round immediately returns us to cooperation.  
   – Defecting in the last round is standard backward‐induction logic; it does not undermine the multi‐round cooperative effort.
'''

description_COOPERATIVE_29 = '''
Below is a fully‐specified “forgiving‐trigger” strategy that (a) tries to guarantee that in almost all rounds your group meets the cooperation threshold​ m, (b) tolerates occasional failures or mistakes by allowing quick recovery, and (c) clearly defines what you do in the first and last rounds.

1. Strategy Intuition  
  – We keep an internal two‐state memory: “Forgiven” (i.e. normal cooperation mode) or “Punish” (we punish the group for one round by defecting).  
  – As long as the group met the threshold in the previous round, we stay in Forgiven and contribute (C).  
  – If the group failed the threshold last round while we were in Forgiven, we enter Punish and defect once.  
  – Immediately after one Punish round, we forgive and return to Forgiven, regardless of outcome, to try cooperation again.  
  – In the very last round (t = r) we defect, since there is no future to incentivize cooperation.

2. State Machine Description  
  State variables:  
    S ∈ {Forgiven, Punish}  
  Initialization (before round 1):  
    S ← Forgiven  

  For each round t = 1,2,…,r do  
    if t = r then  
      play D  // last‐round defection (no future)  
    else  
      if S = Forgiven then  
        play C  
      else  // S = Punish  
        play D  
      end if  
    end if

    // After observing all n actions in round t, count #C_t  
    let coop_t = number of players who chose C in round t  
    // Update state for next round
    if t < r then  
      if coop_t ≥ m then  
        S ← Forgiven  
      else  
        if S at round-t was Forgiven then  
          S ← Punish  
        else  // we had been Punishing
          S ← Forgiven  
        end if  
      end if  
    end if  
  end for

3. Round-by-Round Break-Down  
  • Round 1 (t=1): S=Forgiven ⇒ you play C.  
    Since no history, we give cooperation a chance.  
  • Rounds 2,…,r–1:  
     – If last round’s cooperators ≥ m, you remain Forgiven and play C.  
     – If they fell below m and you were Forgiven, you switch to Punish (play D) exactly one round.  
     – If they fell below m and you were already Punishing, you forgive (return to Forgiven) and play C, giving the group another chance.  
  • Round r: Always D (no future to enforce cooperation).

4. Why This Is Cooperative  
  – In a perfect sequence with no mistakes all players start in Forgiven and always play C in rounds 1…r–1, so the threshold is met every time and each round yields the k‐bonus.  
  – If the group ever fails (perhaps due to a mistake), each player defects for exactly one round (Punish) and then immediately goes back to cooperating. This punishes non-cooperation but allows fast recovery.  
  – By never punishing indefinitely (no “grim” forever‐trigger), the strategy is robust to one or two stray defections/mistakes.  

5. Pseudocode Summary  
```
Parameters: n, r, m, k  (common knowledge)

State S ← “Forgiven”

for t in 1..r do
  if t == r then
    action ← D      // no future ⇒ defect
  else
    if S == “Forgiven” then
      action ← C
    else                // S == “Punish”
      action ← D
    end
  end

  // After actions of all players are revealed:
  coop_t ← # of players who chose C in round t

  if t < r then
    if coop_t ≥ m then
      S ← “Forgiven”
    else
      if previous S was “Forgiven” then
        S ← “Punish”
      else
        S ← “Forgiven”
      end
    end
  end
end
```

This completes a self-contained cooperative strategy that maximizes the chance of hitting the m-cooperator threshold in each round, quickly punishes any shortfall, but always returns to cooperation—and clearly handles both the very first and very last round.
'''

description_COOPERATIVE_30 = '''
Below is a “conditional‐cooperation with limited punishment” strategy.  It is designed to (1) start cooperatively, (2) reward rounds in which the group hits the threshold, (3) punish a failure only one round, then forgive, and (4) defect in the final round (the standard end‐game).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

1.  Overview of decision rules  
    • Round 1: Cooperate.  
    • Intermediate rounds t=2…r–1:  
       – If in round t–1 the number of cooperators ≥ m (“threshold met”), then cooperate.  
       – If in round t–1 the number of cooperators < m (“threshold failed”):  
            · If you cooperated in t–1, then defect in t (punish).  
            · If you defected in t–1, then cooperate in t (forgive and attempt to rebuild cooperation).  
    • Round r (last round): Defect (no future to enforce cooperation).

2.  Rationale  
    • By cooperating after a successful round, you signal “reward.”  
    • By punishing exactly once after a failure, you discourage persistent free‐riding or coordination failures.  
    • By immediately forgiving on the next round, you restore trust and allow recovery of cooperation.  
    • Defection in the last round is the individually rational choice once there is no future benefit.

3.  Pseudocode  

  let a_i[t] ∈ {C, D} be your action in round t  
  let coop_count[t] = number of players (including you) who played C in round t  

  for t from 1 to r do  
    if t == 1 then  
      a_i[t] := C  
    else if t == r then  
      a_i[t] := D  
    else  
      if coop_count[t–1] ≥ m then  
        // Last round succeeded – reward with cooperation  
        a_i[t] := C  
      else  
        // Last round failed – one‐shot punishment then forgive  
        if a_i[t–1] == C then  
          // You cooperated last round but group failed → punish  
          a_i[t] := D  
        else  
          // You already punished → forgive and try to rebuild  
          a_i[t] := C  

    // Play action a_i[t] simultaneously with others  
    observe coop_count[t] for use in next iteration  
  end for

4.  Handling edge cases  
  • If m = 1, threshold always met as long as one cooperator exists; the strategy still works, punishing only if literally everyone defects in the previous round.  
  • If k is very large (cooperation highly rewarded), this strategy still drives toward always‐cooperate except the final round.  
  • If the threshold repeatedly fails, you will cycle C→D→C→D … which signals a strong desire to cooperate and punishes defection, giving opponents every opportunity to joint‐coordinate on C.  
  • If opponents are fully cooperative, you will settle into all‐C for rounds 2…r–1.  

5.  Why this is cooperative  
  – It always begins from cooperation.  
  – It only defects in reaction to group failure, and only for one round.  
  – It promptly returns to cooperation, allowing group recovery.  
  – It respects the fact that in the final round there is no future incentive, but up to that point strongly encourages meeting the threshold.

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
'''

description_COOPERATIVE_31 = '''
Below is a memory‐1 “threshold‐TFT” strategy with a brief, one‐round punishment followed by forgiveness.  It is designed to steer the group toward meeting the m-cooperator threshold every round, and yet remain robust to occasional misses.

1. Overview of the approach  
   • Start by cooperating.  
   • If in the previous round the group met the threshold, cooperate again.  
   • If the threshold failed, defect for exactly one round (punishment), then forgive and return to cooperation.  
   • In the final round, defect (standard backward‐induction end‐game).  

2. State variables  
   • last_coops ∈ {0,1,…,n}: number of cooperators observed in the previous round (initialize to n for convenience).  
   • punish_counter ∈ {0,1}: how many more rounds we will hold a punishment defect (initialize to 0).  

3. Decision rule (pseudocode)  
```
initialize:
  last_coops ← n       # so that in round 1 we count as if “threshold met”
  punish_counter ← 0

for t in 1..r do
  if t == r then
    action ← D         # last‐round defection (no future to enforce cooperation)
  
  else if punish_counter > 0 then
    action ← D
    punish_counter ← punish_counter − 1
  
  else if t == 1 or last_coops ≥ m then
    action ← C         # cooperate on round 1 or whenever threshold was met
  
  else
    # threshold failed last time → punish once
    action ← D
    punish_counter ← 1
  
  end if

  play(action)
  
  # observe others and update last_coops for the next round
  let coop_count_this_round = number of players (including you) who chose C
  last_coops ← coop_count_this_round
end for
```

4. Why this is cooperative  
   • By starting with C and returning to C whenever the group meets the threshold, you “reward” collective success.  
   • A single round of punishment after a failure signals your willingness to enforce the common interest (getting k) but then you immediately forgive, allowing the group to re-coordinate.  
   • Defecting in the final round is individually rational (standard endgame defection) but does not carry over any future cost.  

5. Handling edge cases  
   • First round (t=1): we treat it as if the threshold were met, so you cooperate.  
   • If multiple consecutive failures occur, you will defect one round after each failure, then resume cooperation.  
   • In the very last round (t=r) you unconditionally defect because there is no future round in which to punish or reward—this is the only strictly dominant play in a finitely repeated game.  

This simple memory‐1 rule fosters steady cooperation (meeting the m-cooperator threshold each round) but is also forgiving enough to recover from isolated lapses.
'''

description_COOPERATIVE_32 = '''
Below is a complete description of a highly-cooperative “rotate‐and‐punish” strategy.  In plain English it says: (1) pre‐commit to having exactly m cooperators each round by a deterministic round‐robin schedule, (2) stick to the schedule unless someone ever deviates, and (3) if a deviation is observed, switch to permanent defection (“grim trigger”).  This enforces the group‐optimum threshold each round and punishes stray defectors with a loss of the group bonus.  

1. Preliminaries  
   • Players are labeled i=1…n.  Everyone knows (n,r,m,k).  
   • We will build for each player i a set Lᵢ ⊆ {1,…,r} of “cooperation‐rounds.”  In every round t exactly m players will have t∈Lᵢ and thus cooperate.  The simplest way is a round‐robin allocation:  
     – Let q = ⌊r·m/n⌋ and rem = r·m mod n.  
     – Assign to players 1…rem an extra round: so player i’s total cooperations = q+1 if i≤rem, else q.  
     – Spread those cooperations approximately evenly over the r rounds (e.g. round‐robin: give the jᵗʰ cooperation of each player at round ≈⌈(i + (j–1)·n)/m⌉).  
   • Everyone can compute everyone else’s Lᵢ in advance.

2. Strategy Overview  
   We maintain a single boolean flag Good = true.  As long as Good remains true, we each play according to our personal Lᵢ schedule.  If anyone ever deviates (the count of cooperators ≠m or a known player i plays opposite its Lᵢ in some round t), we set Good ← false and from then on defect forever.

3. Pseudocode for player i  
   
   initialize:  
     Good ← true  
     Compute Lᵢ ⊆ {1…r} as above  

   for t in 1…r do  
     if Good = true then  
       if t ∈ Lᵢ then play C else play D  
     else  
       play D  

     Observe the full action profile {C,D} of round t.  
     Count coop_count = number of C’s this round.  
     if Good = true and (coop_count ≠ m or player j’s action ≠ (t∈Lⱼ)) for some j then  
       Good ← false     # trigger punishment permanently  

4. Handling Edge Cases  
   • First round (t=1): Good is true, so follow Lᵢ.  
   • Last round (t=r): same rule—if t∈Lᵢ, we cooperate.  We do not “defect on the last move,” because our mutual schedule and threat of prior punishment is what sustains cooperation throughout.  
   • If someone deviates on round r, they still trigger Good←false but there are no rounds left to punish; however the deviation in the last round can only harm themselves (they forgo the schedule’s group optimum payoff).  
   • If r·m is not divisible by n, some players have one extra cooperation.  Over the tournament this evens out: those with q+1 cooperations sacrifice one more round but gain the group bonus in almost every round.  

5. Why It’s Cooperative  
   • When all comply, every round has exactly m cooperators ⇒ every player gets the game‐optimal total (maximum collective bonus over r rounds).  
   • The “grim trigger” ensures that any unilateral deviation abandons the group bonus forever, so the cost of defecting is high.  
   • By rotating who cooperates, we share the cost of cooperation fairly.  

You can implement the above in any code framework: the key ingredients are (a) a publicly known round‐robin schedule Lᵢ, (b) a “Good” flag that flips to false on any deviation, and (c) the simple rule “if Good, play according to Lᵢ; otherwise defect forever.”
'''

description_AGGRESSIVE_17 = '''
Below is an “exploit‐first” (aggressive) strategy that never seeks to build trust or punish—its only goal is to maximize your own one-round payoffs by free-riding whenever it can and only kicking in a contribution if your single contribution is necessary to hit the threshold.

1.  Definitions  
    Let t = current round (1 ≤ t ≤ r).  
    Let Hᵗ be the history of all players’ actions in rounds 1..t–1.  
    Let coop_otherLast = number of cooperators among the other (n–1) players in round t–1 (undefined for t=1).  

2.  Core idea  
    In each round you estimate how many of the other players will cooperate and then:  
    •  If you believe the other players will reach at least m cooperators on their own, you defect (D) to free-ride on their contributions.  
    •  If you believe the other players will deliver exactly m–1 cooperators, you cooperate (C) so that together you hit m and capture the reward k.  
    •  Otherwise (they deliver fewer than m–1), you defect—your lone cooperation would not reach the threshold and so would only cost you 1.  

3.  Prediction rule (very short memory)  
    We use the previous round’s count as our predictor for the current round.  
    •  For t>1: coop_otherLast = number of C’s played by others in round t–1.  
    •  For t=1: we have no history, so assume coop_otherLast = 0 (the most conservative guess, which favors defection).  

4.  Decision rule (for every round t):  
    if coop_otherLast ≥ m  
       choose D  
    else if coop_otherLast = m–1  
       choose C  
    else  (coop_otherLast < m–1)  
       choose D  

5.  Special handling of first and last rounds  
    •  Round t=1: no history → coop_otherLast := 0 → you defect.  
    •  Round t=r: same rule applies (there is no future to care about), so you still defect if coop_otherLast ≠ m–1, cooperate only if coop_otherLast = m–1.  

6.  Pseudocode  

    initialize coop_otherLast ← 0    # assume no one cooperates before round 1  
    for t in 1..r:  
        if coop_otherLast ≥ m:  
            action[t] ← D  
        else if coop_otherLast = m–1:  
            action[t] ← C  
        else:  
            action[t] ← D  

        # observe opponents’ moves this round  
        observe the n–1 other players’ actions in round t  
        coop_otherLast ← count of those actions equal to C  

    end for  

7.  Why it’s “aggressive”  
    •  You never cooperate to build reputation or punish others—only to secure the payoff when you alone can tip the balance.  
    •  You free-ride on everyone else whenever possible.  
    •  You make no attempt to enforce cooperation or to retaliate; you simply exploit.  

This strategy maximizes your per-round gain under common-knowledge perfect information, at the cost of never promoting genuine collective success beyond the bare minimum you need for your own reward.
'''

description_AGGRESSIVE_18 = '''
Below is a fully specified “aggressive” repeated‐game strategy for the Collective Risk Dilemma.  It never “wastes” a contribution except when that contribution is exactly the marginal pivot needed to secure the public reward for itself—and otherwise it free‐rides and even punishes overcooperators.

---

Name: Exploit‐Rescue Defector (ERD)

Intuition:  
1.  Always defect (“free-ride”) whenever the community can still reach the threshold without you.  
2.  Only contribute if you are exactly the (mᵗʰ) cooperator: that single contribution swings the group from failure to success, and that yields you a net gain (k vs. 1).  
3.  Otherwise, defect—and by defecting even when the group would have succeeded with you, you punish overcooperators (they lose k), while you pocket 1 + k when the group still succeeds.

Parameters:  
n = # of players  
r = # of rounds  
m = threshold  
k = group payoff bonus when threshold met (> 1)

State you track:  
For each round t > 1, record N_C(t–1) = number of cooperators among the OTHER n–1 players in the previous round.

Decision rules:

1.  Round 1 (t = 1):
    •  No history ⇒ play D.

2.  Intermediate rounds (1 < t ≤ r):
    •  Let N_C = N_C(t–1), the count of other players who played C in round t–1.
    •  If N_C ≥ m:
         – You know the other players (without you) cooperated at least m times last round ⇒ the group can succeed without your contribution.  
         – Action: Defect (D) ⇒ you get 1 + k, they get k (punishing them by withholding cost).
    •  Else if N_C = m – 1:
         – Without you the group would have fallen short; with you it hits exactly m ⇒ rescuing is profitable:  
           Cooperate ⇒ you get 0 + k = k, which is greater than the 1 you’d get by defecting and failing.  
         – Action: Cooperate (C).
    •  Else (N_C ≤ m – 2):
         – Even if you cooperate, group still fails ⇒ your payoff would be 0 < 1 ⇒ no point in contributing.  
         – Action: Defect (D).

3.  Last round (t = r):
    •  Follow the same rule as in intermediate rounds.  (No “end‐game” nicer behavior.)

Pseudocode

  initialize history H = empty
  for t in 1…r do
    if t == 1 then
      play D
    else
      N_C = count of C’s among rounds t–1 in H, excluding your own
      if N_C >= m then
        play D           # exploit — free-ride, punish over-cooperators
      else if N_C == m - 1 then
        play C           # rescue exactly when it pays off
      else
        play D           # hopeless to rescue, so free-ride
    end if
    record your action in H
  end for

Why it’s aggressive

•  It never cooperates out of “goodwill”—only the moment you’re the pivotal contributor is cooperation profitable.  
•  Whenever the group could have succeeded without you (N_C ≥ m), you defect to pocket 1 + k and force them to pay full cost of cooperation for no added benefit.  
•  It punishes anyone who over‐cooperates, and—by rescue‐only at the margin—it squeezes every last bit of payoff from the collective project.
'''

description_AGGRESSIVE_19 = '''
Below is an “aggressive” tournament‐ready strategy for the repeated Collective Risk Dilemma.  The guiding principle is:  “Free‐ride whenever possible; only sacrifice to get the group reward if your single cooperation is pivotal; never cooperate for any other reason; always defect in the last round.”

1.  Notation and bookkeeping  
   • r = total rounds, t = current round (1 ≤ t ≤ r)  
   • m = cooperation threshold  
   • n = number of players  
   • C_i(t) = action of player i in round t (1 if C, 0 if D)  
   • S_{-you}(t) = sum of others’ cooperations in round t = ∑_{j≠you} C_j(t)  
   • “pivotal” means your single C changes the outcome from failure to success  

2.  High‐Level Description  
   – Always defect (D) unless by cooperating you turn a failed round into a successful one (“pivotal cooperation”).  
   – In the very last round, always defect (no future to leverage cooperation).  
   – In early rounds, if it is impossible for you to be pivotal (either S_{-you} ≥ m already, or S_{-you} ≤ m–2), defect.  
   – This guarantees you capture the k reward +1 private payoff whenever others cooperated enough, and only pay the cooperation cost when absolutely necessary to swing the group payoff.  

3.  Decision Rules (per round t)  
  
  if t == r:  
    play D  # Last‐round defection  
  
  else:  
    observe S = S_{-you}(t)  # how many of the other n–1 players chose C this round  
    if S ≥ m:  
      # Others already meet threshold → you defect and still get +k  
      play D  
    else if S == m–1:  
      # You are pivotal: your C turns a failure (no k) into success (get k)  
      play C  
    else:  
      # Either failure even with your C (S ≤ m–2) or you’d be “wasting” a C (if S > m)  
      play D  
  
4.  Edge Cases and Clarifications  
  • First round (t=1): no history, but use the same rule based on S_{-you}(1).  You observe? In many implementations you only see others’ moves after simultaneous play; but in simulation you predict S based on models.  If you have no signal you simply defect (S assumed low).  
  • When S = m exactly, that means threshold already met → defect.  
  • When S ≤ m–2, even if you cooperate the group still fails → defect.  
  • No retaliation or reward tracking → purely greedy‐pivot logic.  
  • This never “forgives” or “punishes” beyond withholding pivot cooperations; it is static, memory‐minimal, and maximally exploits any accidental over‐cooperation by others.  

5.  Pseudocode  

  for t in 1…r:  
    if t == r:  
      action = D  
    else:  
      S = observe_number_of_C_among_others()  
      if S == m–1:  
        action = C    # only time we pay cost to secure the group bonus  
      else:  
        action = D    # free‐ride or withhold sacrifice  
    play(action)  

6.  Why This Is Aggressive  
  – You never “build goodwill” or incur cost except in the single pivotal case.  
  – You exploit any cooperation by others by defecting when S ≥ m and pocket 1+k.  
  – You refuse to cooperate in the last round, ensuring maximum private payoff when there is no future.  
  – You never punish cooperators beyond withholding pivotal help, but you do maximize your own extraction of group rewards.
'''

description_AGGRESSIVE_20 = '''
Below is an “aggressive” threshold‐exploitation strategy.  In plain English it says: “I will never cooperate to help build a group reward unless by doing so I alone can tip exactly m−1 other cooperators into meeting the threshold—otherwise I defect.”  You thus free‐ride on any near‐miss coalitions, but never throw away your endowment unless it comes with a guaranteed group payoff that you wouldn’t get by defecting.

1.  Definitions and notation  
   •  n: total players  
   •  m: cooperation threshold (1 < m < n)  
   •  k: reward when ≥ m cooperators  
   •  r: total rounds  
   •  At round t, let O_other[t] = number of cooperators among the other n−1 players in round t.

2.  Decision rule for round t (1 ≤ t ≤ r)  
   If O_other[t − 1] == m − 1 then  
  play C  
   else  
  play D  
   Here O_other[0] is undefined, so we initialize O_other[0]=0 ⇒ defect in round 1.

3.  Rationale (aggressive mindset)  
   –  If exactly m−1 others cooperated last time, by choosing C you push the group to ≥m this round, so you get payoff = (0 cost) + k = k (and if you’d defect you’d get only 1).  Since k>1, C is strictly better.  
   –  In all other cases:  
     •  If ≥m others cooperate, the threshold is met even if you defect ⇒ you earn 1+k > k = what you’d get by cooperating.  
     •  If ≤m−2 others cooperate, cooperating fails to meet the threshold ⇒ you earn 0 < 1 = what you’d get by defecting.  
   –  Thus you only ever pay the cooperation cost when it is individually profitable, and otherwise “sabotage” any attempt at collective action.

4.  Edge cases  
   •  First round (t=1): no history ⇒ O_other[0]=0 ⇒ defect.  
   •  Last round (t=r): same rule applies.  Even in the last round you cooperate if and only if you can swing exactly from m−1→m.  
   •  If opponents randomize or change behavior, you continually use only their last-round cooperations as your predictor.

5.  Pseudocode  

   initialize O_other[0] ← 0  
   for t in 1…r do  
     if O_other[t−1] == m−1 then  
       action[t] ← C  
     else  
       action[t] ← D  
     end  
     observe O_other[t]  ← count of cooperators among opponents in round t  
   end  

6.  Why it’s aggressive  
   –  You never reward pure cooperators.  You only cooperate when you personally gain more by meeting the threshold.  
   –  You exploit “near‐miss” coalitions (m−1 cooperators) but otherwise punch holes in any coalition trying to reach m.  
   –  You never respond to goodwill—no tit-for-tat, no forgiveness, just unrelenting self-interest with minimal cooperation.
'''

description_AGGRESSIVE_21 = '''
Below is an “All-D Saboteur” strategy – an aggressive, exploitative defection rule that never pays the cost of cooperation and always either (a) free-rides when others meet the threshold or (b) sabotages the group when they don’t. It works for any n, r, m, k (with 1 < m < n and k > 1).

1.  Decision rules  
    •  At the start of each round t, form a (simple) belief about how many of the other n–1 players will cooperate in round t.  
       –  You can use frequencies from past rounds, but in fact the rule below never requires you to cooperate, so you need only note whether “others alone” will meet the threshold.  
    •  If the other players (excluding you) are estimated to cooperate in number ≥ m, then you definitely defect: you free-ride on their contributions and get payoff 1 + k > k.  
    •  If the others are estimated to cooperate in number < m, then you still defect: by cooperating you would pay a cost and still fail to meet the threshold, earning 0; defecting gives you 1.

    In symbols, letting O_t = expected # cooperators among the other n–1 players in round t:
        if O_t ≥ m   ⇒ action_t = D
        else         ⇒ action_t = D

    Since in all cases defection strictly dominates cooperation (whether the group hits the threshold or not), you never cooperate.

2.  Edge cases  
    •  First round (t = 1): no history ⇒ you cannot trust any belief that others will cooperate enough to meet m. Default to defect.  
    •  Last round (t = r): no future to punish you, so again defect.  
    •  Any round: even if you observe in history that every other player has cooperated reliably enough to meet m by themselves, you still defect to collect the extra +1 payoff on top of k.  
    •  No need for tie-breaking rules or mixed strategies: we never mix or cooperate.

3.  Pseudocode  

    initialize history H = empty  
    for t in 1..r do  
        // Optional: estimate others’ cooperations O_t from history H  
        action[t] = D  
        observe all players’ actions a₁..a_n and payoffs π₁..π_n  
        append (a₁..a_n, π₁..π_n) to H  
    end for  

4.  Rationale (aggressive mindset)  
    –  You never pay the cost c_i = 1.  
    –  If others coordinate successfully, you exploit them for the highest individual payoff (1 + k).  
    –  If they fail, you at least get 1 rather than 0.  
    –  You actively punish any emerging cooperation by refusing to participate, undermining group welfare.  
    –  There is no incentive to deviate: cooperation is never strictly better against any pattern of opponents.
'''

description_AGGRESSIVE_22 = '''
Below is an “aggressive” threshold‐exploitation strategy.  It never “wastes” a contribution except when your single cooperation is the only thing standing between you and the k‐bonus, and even then it immediately reverts to full defection thereafter.

1. Definitions and notation  
   • n, m, k, r as given  
   • history H_t = all players’ actions in rounds 1…t−1  
   • For each round t and each other player j ≠ you, let C_j(t−1)=1 if j cooperated in t−1, else 0.  
   • Let O(t−1)=Σ_{j≠you}C_j(t−1) = number of others who cooperated last round.  
   • On round 1 we set O(0)=0 (pessimistic default).

2. Decision rule for round t=1…r  
   compute predicted cooperators among opponents next round  
     P = O(t−1)  
   if P ≥ m         then  
       play D   (threshold will succeed without you → free-ride)  
   else if P = m−1 then  
     • your single C would push total to m → you secure payoff k instead of 1, so  
       play C  
   else  
       play D   (either threshold will fail even if you C, or you’re not pivotal)

3. Edge‐case handling  
   – First round (t=1): O(0)=0 ⇒ P=0<m−1 ⇒ you defect.  
   – Last round (t=r): same rule applies.  Because there is no future to “reward,” you still only ever cooperate when you are pivotal (P=m−1).  
   – If m=1: then m−1=0.  On any round t, P≥1 ⇒ D; if P=0 ⇒ C (your lone C gets k>1 vs D’s 1).  

4. Why it is aggressive  
   – You never cooper­ate to “build goodwill” or to punish.  
   – You only give up your endowment when it alone can trigger the group bonus, and you immediately revert to defection.  
   – You never threaten or forgive—there is zero “trust building” or “retaliation” logic beyond pure self-interest each round.

5. Pseudocode  

```
initialize O = 0    # pessimistic default for round 1
for t in 1..r:
    P = O
    if P >= m:
        action[t] = D
    else if P == m - 1:
        action[t] = C
    else:
        action[t] = D

    # after simultaneous play, observe others' actions:
    let O = number_of_opponents_who_played_C_in_round(t)
end
```

This strategy is guaranteed to  
– exploit any round in which others are willing to cooperate,  
– never contribute to a failing effort, and  
– only invest when that investment immediately increases your own payoff.
'''

description_AGGRESSIVE_23 = '''
Below is a complete “aggressive free-rider + rescue” strategy for the r-round collective‐risk dilemma.  It never hesitates to defect, only “lends a hand” when it can guarantee a bonus payoff, and shuts down cooperation toward the end so no one can retaliate.

1.  State variables and parameters  
   •  For each opponent j keep a history H_j of their past actions (“C” or “D”) up to the previous round.  
   •  rescue_available ← 1     (we will only “rescue” once per tournament)  
   •  W ← min( r, 5 )          (window size for recent tracking; you can tune 3–10)  
   •  φ ← 0.6                  (trust threshold: opponents with ≥60% C in last W rounds count as “likely cooperators”)  
   •  buffer ← 2               (no rescues in last 2 rounds)  

2.  Helper routine: estimate_cooperators()  
   Input: histories H_j for all j ≠ i  
   Steps:  
     a.  For each opponent j, let recent_j = fraction of C’s in H_j’s last W rounds.  
     b.  Let L = set of j for which recent_j ≥ φ.  (these are “likely cooperators”)  
     c.  Return |L|.  

3.  Main decision rule for round t  
   if t == 1:  
     – No information yet → DEFECT.  
     (We probe by defecting; there’s zero gain in cooperating before we know anything.)  
   else if t == r:  
     – Last round → DEFECT.  
     (Never cooperate in the final round—no future to punish you.)  
   else:  
     let E = estimate_cooperators()  
     – if E ≥ m:  
         • The other “likely cooperators” already cover the threshold.  
         • DEFECT to free-ride on their work, pocket 1 + k rather than 0 + k.  
     – else if E == m−1 AND rescue_available == 1 AND t ≤ r − buffer:  
         • We can tip the balance: one more C makes the bonus guaranteed.  
         • COOPERATE this round (c_i = 1), pocket k rather than 0.  
         • rescue_available ← 0.  
     – else:  
         • No safe bonus, no rescue left, or too close to the end → DEFECT.  

4.  Updating histories  
   After observing all players’ moves this round, append each j’s action to H_j so we can recompute recent_j next round.

5.  Why is this “aggressive”?  
   – You only pay the cooperation cost at most once, and only when you see that exactly m−1 opponents are credible cooperators.  
   – You free-ride whenever bonus is guaranteed, adding +1 to your share each time.  
   – You never trust newcomers unconditionally: only players with ≥φ recent cooperation count.  
   – You never cooperate in the first or last round (no upside from signaling or fear of punishment).  
   – Late‐game defections are absolute: no “end‐game cooperation” to invite exploitation.  

Pseudocode summary:

```
initialize:
  for each j≠i: H_j ← empty list
  rescue_available ← 1
  W ← min(r, 5)
  φ ← 0.6
  buffer ← 2

for t in 1..r:
  if t == 1 or t == r:
    action_i[t] ← D
  else:
    // 1) Estimate how many “likely cooperators” remain
    E ← 0
    for j≠i:
      recent_j ← fraction of C’s in last min(W,len(H_j)) entries of H_j
      if recent_j ≥ φ:
        E ← E + 1

    // 2) Decision
    if E ≥ m:
      action_i[t] ← D      // free-ride guaranteed
    else if E == m-1 AND rescue_available == 1 AND t ≤ r - buffer:
      action_i[t] ← C      // one rescue push
      rescue_available ← 0
    else:
      action_i[t] ← D

  // 3) Observe all players’ actions and update histories
  for each j≠i:
    append j’s action at round t to H_j
```

Tuning notes:  
•  You can adjust W (memory window) and φ (trust threshold) to be more or less “stingy.”  
•  Setting rescue_available ← 0 after one use ensures you won’t be duped into repeated contributions.  
•  The buffer of 2 rounds makes sure no one can exploit you after your last rescue.  

This fulfills all requirements: clear decision rules, first/last‐round handling, and an unmistakably aggressive, free‐riding mindset.
'''

description_AGGRESSIVE_24 = '''
Below is an “aggressive” strategy—call it the Last-Ditch Pivotal Exploiter—that:

  • Virtually never gives up its endowment  
  • Punishes any incipient cooperation by refusing to help  
  • Only cooperates in the very last round when you can be sure you’re pivotal (and thus extract the maximal bang-for-your-buck)  

1.  State variables and bookkeeping  
    • r  = total rounds  
    • t  = current round (1,…,r)  
    • m  = threshold of cooperators needed  
    • history of plays A_j,τ for each opponent j and past rounds τ  

2.  Core decision rule  
    If t < r:  
      – Action_i(t) ← D  (always defect)  
    Else (t == r):  
      • Estimate how many of the other n–1 players will play C this final round.  
         – Simplest: assume they repeat what they did in round r–1  
           let coop_prev = # of opponents j with A_j,r–1 = C  
      • If coop_prev == m–1 then Action_i(r) ← C   (you’re pivotal → you gain k instead of 1)  
        else Action_i(r) ← D  

3.  Why it’s aggressive  
    – By defecting every round except the last, you  
       • Never pay the cooperation cost c_i=1  
       • Derail any nascent cooperative momentum (no “forgiving” response)  
    – In the final round you cooperate only if you’re almost guaranteed to tip the outcome from failure to success (i.e. you convert a 1-point payoff into k>1 points)  

4.  Edge‐case handling  
    • t=1 (first round): falls under “t<r,” so you defect.  
    • Rounds 2 through r–1: always defect, regardless of history.  
    • Final round t=r: you look one step back (round r–1) to see if others cooperated exactly m–1 times:  
        – If yes, you cooperate and secure π_i = 0 + k = k  (instead of defect π_i =1)  
        – If no, you defect and get at least 1 (if group succeeds on its own, you get 1+k)  

5.  Pseudocode  

  initialize r, m  
  for t in 1..r:  
    if t < r:  
      play D  
    else:  # t == r  
      coop_prev ← count of opponents j with A_j,r–1 == C  
      if coop_prev == m – 1:  
        play C  
      else:  
        play D  

This strategy is maximally aggressive: it never “trusts” or “rewards” cooperation until the very last moment and then only when cooperating is guaranteed to increase your own payoff.
'''

description_AGGRESSIVE_25 = '''
Below is a self-contained “aggressive” strategy—call it Cutthroat Free-rider with Occasional Deception—for the repeated Collective-Risk Dilemma.  It never hesitates to defect (D) to maximize its own one-shot payoff, but occasionally “hooks” the others with a token cooperation (C) early on to keep them hoping for a threshold and thus exploitable.  In the last round it always defects.

1.  Key ideas  
   • Default = Defect.  Defecting always strictly dominates cooperating in any single round.  By defecting you either  
      – when the threshold is met, free-ride (get 1 + k vs cooperators’ k), or  
      – when the threshold fails, punish cooperators (you get 1 vs their 0).  
   • Occasional Deception (“Hook”): in a small fraction of early rounds, you cooperate with low probability p_hook to induce others to keep cooperating in hopes of the public good—then you switch back to defection to exploit.  
   • Final Round Never cooperate in the last round: no future to manipulate.

2.  Parameters  
   – r total rounds  
   – m, n, k game parameters as given  
   – p_hook small base “hook” probability, e.g. 0.1  
   – α_decay decay factor for p_hook after a successful exploitation, e.g. 0.5  

3.  State variables  
   – t current round (1…r)  
   – p current hook probability, initialized to p_hook  

4.  Decision rule (per round)  
```
function choose_action(t, history):
  if t == r:
    return D                                  # always defect in last round

  # Otherwise (t < r):
  with probability p:
    return C                                  # “hook” the group
  else:
    return D                                  # otherwise defect

# after each round, update p:
#   if in the previous round the threshold was met AND we defected,
#   we just “exploited” them—so reduce p to hook less in future
function update_hook_prob(last_round_outcome, our_last_action):
  if last_round_outcome.threshold_met and our_last_action == D:
    p := p * α_decay                          # e.g. α_decay = 0.5
  # else leave p unchanged
```

5.  Edge cases  
  • First round (t=1): p = p_hook, so you cooperate with prob. p_hook, otherwise defect.  
  • Intermediate rounds (1 < t < r): apply the same randomised hook-or-defect rule, decaying p whenever you successfully free-ride.  
  • Last round (t = r): you defect with probability 1.

6.  Why it is “aggressive”  
  – It never sacrifices itself to help the group: defect is always the default.  
  – It punishes any genuine cooperation by withholding its own contribution, so cooperators get nothing or are free-ridden.  
  – By occasionally cooperating early (the “hook”), it keeps other strategies from writing you off immediately—so they may keep cooperating and offer you more exploitable opportunities.  
  – It decays its deception over time as soon as it scores a big free-ride, becoming ever more ruthless.  

This strategy is trivial to implement as pseudocode and meets all requirements: it specifies exactly when to cooperate vs defect, handles round 1 and the final round explicitly, and clearly embodies an aggressive, exploitative mindset.
'''

description_AGGRESSIVE_26 = '''
Below is a self‐contained “aggressive” strategy we’ll call the Lone Kingmaker.  In a nutshell, you never trust or reward cooperators—you only ever contribute when your single coin is both necessary and sufficient to trigger the public good (so you free‐ride whenever you can, and you “punish” cooperators by refusing to help unless it’s strictly payoff‐maximizing).

1.  Decision rules  
    •  First round (t=1): Defect.  You have no history; best to start by free‐riding.  
    •  Intermediate rounds (1 < t < r):  
       –  Let Cₜ₋₁ = number of cooperators in the previous round.  
       –  If Cₜ₋₁ = m–1, then cooperate (C).  
            Reason: your lone cooperation will bring total to m, guarantee +k for you, yielding 0 + k > 1.  
       –  Otherwise (Cₜ₋₁ < m–1 or ≥ m), defect (D).  
            •  If Cₜ₋₁ < m–1, even if you cooperated the threshold still fails ⇒ you’d get 0 < 1.  
            •  If Cₜ₋₁ ≥ m, threshold would succeed without you ⇒ you defect to free‐ride (1 + k > 0 + k).  
    •  Last round (t = r): Defect.  No future punishment or reward—best to free‐ride.

2.  Handling edge cases  
    •  If r = 2, both first and last round rules apply ⇒ you defect twice.  
    •  If in some round you observe Cₜ₋₁ = m exactly (or >m), you still defect—you never “help” when you’re not pivotal.  
    •  If k ≤ 1 (outside spec), you would never cooperate even when pivotal; but spec says k>1.  

3.  Why this is aggressive  
    –  You punish any group success by never rewarding widespread cooperation—only when you can extort the benefit for yourself.  
    –  You never “forgive” past defection with cooperation; there is no tit‐for‐tat or long‐run build‐up of trust.  
    –  You remain unpredictable: cooperations only arrive when you calculate they’re the sole factor tipping you into +k territory.  
    –  In a population of more “nice” or generous strategies, you will systematically free‐ride on their contributions and occasionally swoop in to salvage a failing round—but never more than strictly necessary.

Pseudocode  
```python
# Parameters: n, m, k, r
# History: coop_count[t] = number of cooperators in round t (1-based index)

def LoneKingmakerAction(t, coop_count):
    # t: current round index, 1..r
    if t == 1 or t == r:
        return 'D'       # defect first and last round
    prev = coop_count[t-1]
    if prev == m-1:
        return 'C'       # be the kingmaker
    else:
        return 'D'       # otherwise always defect

# Example usage in simulation loop:
# for t in 1..r:
#     action_i = LoneKingmakerAction(t, coop_count_history)
#     observe others, update coop_count_history[t], payoffs, etc.
```

Summary  
– Always defect except in the one and only scenario where your single vote turns a failed threshold into a success.  
– This ensures you never “waste” a cooperation unless it directly increases your payoff, and you systematically free‐ride on genuine cooperators.  
– By refusing to build or maintain trust, you adopt the maximally aggressive stance within the Collective Risk Dilemma.
'''

description_AGGRESSIVE_27 = '''
Below is an “aggressive‐minimalist” threshold‐public‐goods strategy.  It never gives gratuitous cooperation, only chips in exactly when your contribution is needed to reach m cooperators—and otherwise defects.  In addition it uses a simple grim trigger to punish groups that grossly under-contribute.  

────────────────────────────────────────────────────  
STRATEGY NAME  
  Aggressive Minimal Cover + Grim Punish  

PARAMETERS  
  n ≥ 2 players, threshold m (1 < m < n), total rounds r > 1  

STATE  
     PunishMode  ∈ {OFF, ON}   // starts OFF  

INITIALIZATION (before round 1)  
  PunishMode ← OFF  

DECISION RULE (each round t = 1…r)  
  1. If t = r (last round) → Defect.  
     Reason: no future to punish, so always free‐ride.  
  2. Else if PunishMode = ON → Defect.  
     Reason: once we’ve triggered punishment, never cooperate again.  
  3. Else if t = 1 → Defect.  
     Reason: no information yet—default to defection.  
  4. Else (2 ≤ t < r and PunishMode = OFF):  
     Let coopOthersLast = number of cooperators among the other n–1 players in round t–1.  
     a. If coopOthersLast < m–1 then  
           // Even if we joined, we couldn’t reach the threshold.  
           PunishMode ← ON         // trigger a permanent punish phase  
           Return Defect  
     b. If coopOthersLast = m–1 then  
           // Our single C will tip the count to m.  
           Return Cooperate  
     c. If coopOthersLast ≥ m then  
           // Others will meet the threshold without us—free‐ride.  
           Return Defect  

────────────────────────────────────────────────────  
PSEUDOCODE  

  function decideAction(t, history):  
      if t == r:  
          return D  
      if PunishMode == ON:  
          return D  
      if t == 1:  
          return D  

      coopOthersLast = countCooperators(history[t-1] excluding self)  

      if coopOthersLast < m-1:  
          PunishMode = ON  
          return D  
      if coopOthersLast == m-1:  
          return C  
      // coopOthersLast ≥ m  
      return D  

────────────────────────────────────────────────────  
WHY IT’S “AGGRESSIVE”  
  •  Default‐to‐Defect: in every state except the knife‐edge case (coopOthersLast = m–1), you defect.  
  •  Grim Trigger: if the group “blows” a round so badly that even with you it couldn’t reach m, you switch to permanent defection—punishing large shortfalls.  
  •  No end-game cooperation: in the final round you always defect, extracting maximum private gain.  

This guarantees you only pay the cost of cooperation (c_i=1) when it’s strictly necessary to secure the public good—and otherwise exploits—or punishes—the rest.
'''

description_AGGRESSIVE_28 = '''
Below is a self-contained “aggressive” strategy, which I’ll call the Minimal-Contribution + Punishment strategy.  In plain English it (1) never gives more than it must to hit the threshold, (2) always defects in the first and last rounds, and (3) if ever burned by cooperating and still seeing failure, it punishes everyone forever.

———

STRATEGY OVERVIEW  
1.  First round: defect (no history yet, play selfishly).  
2.  Middle rounds (2 ≤ t < r):  
   •  Look at how many others cooperated in the previous round, call it coop_others.  
   •  If coop_others ≥ m, defect (exploit—they will already meet the threshold).  
   •  If coop_others = m–1, cooperate (you’re the swing vote to secure k for everyone, including you).  
   •  Otherwise (coop_others < m–1), defect (even with you they can’t reach threshold).  
3.  Last round (t = r): defect (no future to incentivize cooperation).  
4.  Grim trigger: if in any round you cooperated but total cooperators < m (i.e. threshold failed despite your C), switch to permanent defection thereafter.

This ruleset aggressively extracts payoff: you only ever “sacrifice” your endowment when your single vote is needed to unlock k, you freeload whenever possible, and you never let yourself be exploited twice.

———

PSEUDOCODE  

  initialize  
    broken ← false       # have we been burned?  

  function decide_action(t, history):  
    if broken or t == 1 or t == r:  
      return D            # first or last round, or already punished → always defect  

    let coop_others ← count of C among other players in round t–1  

    if coop_others ≥ m:  
      return D            # threshold met anyway → defect to get 1 + k  
    else if coop_others == m–1:  
      return C            # you’re the critical voter → cooperate for k  
    else:  
      return D            # even with you they fall short → defect for sure  

  function update_after_round(t, your_action, total_coops):  
    if your_action == C and total_coops < m:  
      broken ← true       # you cooperated but project failed → punish forever  

———

EDGE-CASE HANDLING  
•  Round 1: no information—defect.  
•  Round r: terminal round—defect (no future leverage).  
•  If ever “tricked” into contributing but group still fails: set broken and defect permanently.  

———

WHY IT’S AGGRESSIVE  
•  You never over-contribute—only step in when you alone flip the round from fail to success.  
•  You freeload on all other successes.  
•  You avoid being a “sucker” more than once by switching to full defection if you’re ever burned.
'''

description_AGGRESSIVE_29 = '''
Below is a fully specified “Aggressive Free-Rider” strategy for the repeated collective-risk dilemma.  It never hesitates to defect, exploits any temporary cooperation by others, and admits a tiny sprinkle of cooperation only to guard against turning fully predictable (and punishable) in tournaments where some opponents may try to retaliate.

1.  Overview  
   – Mindset:  Always maximize your own payoff relative to others by defecting (D) whenever you can free-ride on any possible public-good success, and by never contributing to it except with vanishing probability.  
   – Key points:  
     •  Defect is strictly dominant in every single shot (it yields +1 more than cooperating).  
     •  In a repeated setting, pure-D is easily spotted and (if opponents attempt to punish) may provoke grudges that reduce your absolute gains—but you still win in relative terms if you never cooperate.  
     •  To blunt any “Tit-for-Tat” or “grim-trigger” punishers, inject a tiny cooperation probability ε.  This keeps you not fully exploitable.  

2.  Decision rules  
   Let ε be a very small positive number (e.g. ε = 0.05 or smaller).  Denote by t the current round (1 ≤ t ≤ r), and by r the total number of rounds.  Let history H be the full past record of who cooperated or defected each round.

   At each round t:

   1.  If t = r (the last round), play D.  
       •  No future to punish you, so you take the safe private payoff.

   2.  Otherwise (1 ≤ t < r):  
       a.  With probability 1 – ε, play D.  
       b.  With probability ε, play C.

   That is, in every non-final round you almost always defect, but with tiny chance ε you cooperate—just enough random “noise” to break up any tit-for-tat punishers who might want to lock you into perpetual defection.

3.  Pseudocode  

   ```
   Initialize:
     ε ← 0.03          # small cooperation probability
     r ← total number of rounds

   Function DecideAction(t, history H):
     if t == r:
       return D      # last round: pure defection
     else:
       if random_uniform(0,1) < ε:
         return C    # rare “noise” cooperation
       else:
         return D    # almost always defect
   ```

4.  Handling edge cases  
   – First round (t = 1): treated as any other non-final round.  You cooperate with probability ε and defect otherwise.  
   – Near-last round (t = r–1): still inject noise, since opponents might try to punish in the very last round—but at t = r you revert to guaranteed D.  
   – If opponents never punish, your small ε ‘cooperations’ occasionally let you cash in on a threshold success (if m or more of the others happen to cooperate).  When that occurs, your defection yields 1+k instead of k, so you still lead the pack.  
   – If opponents do punish by refusing cooperation after seeing you defect, your random C's can re-start group successes, always letting you free-ride again on the next round.

5.  Why this is aggressive  
   – You never “invest” with high probability.  
   – You exploit every cooperative cluster in the group by defecting almost always.  
   – You refuse any sustained “forgive and forget” path that would allow collective success to become stable—you only tolerate just enough cooperation to unstick grudges.  
   – In the final round you defect with certainty (since there is no future to fear punishment), squeezing out the maximum private gain.

This strategy maximizes your payoff in absolute and relative terms by always defecting except for a tiny, random cooperation “needle in a haystack” to inoculate you against punishment cycles.
'''

description_AGGRESSIVE_30 = '''
Below is a self-contained description of an “Aggressive Exploit-and-Punish” strategy for the repeated threshold public-goods (collective risk) game.  It will (a) defect by default, (b) only cooperate when strictly necessary to secure the threshold reward, and (c) “grim-trigger” punish the group forever if they ever let you down after you’ve played C.  It also never cooperates in the final round.

––––––––––––––––––––––––––––––  
STRATEGY NAME  
  Aggressive Exploit-and-Punish  

PARAMETERS  
  n   – total players  
  r   – total rounds  
  m   – cooperator threshold (1 < m < n)  
  k   – reward multiplier (> 1)  

INTERNAL STATE  
  punished (bool, init=false)  
    // once true, you defect every remaining round  
  punishRoundsLeft (int, init=0)  
    // a short “cool-off” if you choose to punish only P rounds  

CONSTANTS  
  P = ⌊min(3, r/2)⌋  
    // number of rounds you punish after a betrayal  
––––––––––––––––––––––––––––––  
Decision‐Rule Pseudocode for Round t  

INPUT (at start of round t)  
  t               // current round index (1…r)  
  lastActions     // vector of all n actions in round t–1 (only if t>1)  

COMPUTE  
  // count cooperators among the OTHER n–1 players in t–1  
  if t==1 then  
    coopPrevOthers ← 0  
  else  
    coopPrevOthers ← count_j≠you{ lastActions[j] == C }  

1) If t == r:  
     action ← D     // always defect in final round  
     goto RETURN  

2) If punished == true:  
     action ← D     // Grim-trigger: defect forever  
     goto RETURN  

3) If punishRoundsLeft > 0:  
     // serving a short punishment “cool-off”  
     action ← D  
     punishRoundsLeft ← punishRoundsLeft – 1  
     goto RETURN  

4) Otherwise (normal exploitation mode):  
     if coopPrevOthers ≥ m then  
       // group already met threshold without you  
       action ← D          // maximize private payoff  
     elseif coopPrevOthers == m – 1 then  
       // you are pivotal: needed to reach m  
       action ← C          // secure the k-bonus for yourself  
     else  
       // even if you cooperate, threshold fails  
       action ← D  
     endif  

RETURN action  

––––––––––––––––––––––––––––––  
STATE‐UPDATE (after observing outcome of round t)  

If (t≥1) and in round t:  
  let coopPrevOthersWasPivotal = (coopPrevOthers == m–1)  
  let thresholdReached = (coopPrevOthers + (action==C?1:0) ≥ m)  

  // If you cooperated when pivotal but still missed the threshold,  
  // someone else defected on you ⇒ trigger punishment  
  if coopPrevOthersWasPivotal && action==C && !thresholdReached then  
    punished ← true           // or punishRoundsLeft ← P  
  end  

––––––––––––––––––––––––––––––  
EXPLANATION / RATIONALE  

1.  Default Defection: You only pay the cost of C (c_i=1) when it raises your own payoff (i.e. you’re the m’th cooperator).  Otherwise you free‐ride.  
2.  Last‐Round Defection: By backward induction there is no future to punish, so always defect in round r.  
3.  Exploit Others: If the other n–1 players already hit m, you pocket 1 + k with D rather than sacrificing 1 for C.  
4.  Pivotal Cooperation: Only when coopPrevOthers == m–1 do you play C—just enough to guarantee the group payoff k.  
5.  Grim Punishment: If you ever “step up” (play C) to try to hit m but still fail (because someone else defected), you interpret that as betrayal and defect forever thereafter.  

This strategy is “aggressive” because it  
•    Maximizes defection whenever safe,  
•    Never forgives the first betrayal,  
•    Exploits cooperative majorities to pocket the public reward,  
•    And refuses to waste further rounds once trust is broken.
'''

description_AGGRESSIVE_31 = '''
Below is a fully‐specified “Selective Exploiter” strategy.  It cooperates only when absolutely necessary to secure the public good reward and otherwise defects—even at the cost of foregoing a reward—to punish any attempts at mass cooperation.

1.  Definitions and state  
    • r  = total rounds  
    • t  = current round (1 ≤ t ≤ r)  
    • m  = cooperation threshold  
    • obs_coops[t–1] = number of players (excluding you) who played C in the previous round  
    • A_t   = your action in round t ∈ {C, D}

2.  Decision rules

    Round 1 (t=1):
      A_1 ← D  
      (No history yet—start by defecting.)

    Rounds 2 through r–1 (2 ≤ t ≤ r–1):
      if obs_coops[t–1] == m–1 then  
        // Your cooperation is pivotal—by switching to C you turn a failed threshold into a success  
        A_t ← C  
      else  
        // Either the threshold would succeed without you (obs_coops[t–1] ≥ m)
        // or cannot succeed even with you (obs_coops[t–1] ≤ m–2)
        // In both cases you defect to pocket the private gain or to punish
        A_t ← D  
      end if

    Round r (last round):
      A_r ← D  
      (Backward induction: no future punishment possible, so always defect.)

3.  Pseudocode

    initialize():
      // nothing to initialize but can store last round coop count
      last_coops ← 0

    for t in 1..r do:
      if t == 1:
        action ← D

      else if t == r:
        action ← D

      else:
        // rounds 2 to r–1
        if last_coops == m–1:
          action ← C
        else:
          action ← D
        end if
      end if

      play(action)
      observe opponents’ actions
      last_coops ← count_of_C_among_others()

    end for

4.  Key properties and “aggressiveness”

    • Maximum defection:  You defect in the first and last rounds and in all interior rounds except the single pivot case.  
    • Pivot-only cooperation:  You only incur the cost of cooperation when your lone C changes a failure (no reward) into a success (everyone gets k).  
    • Punishment by omission:  By refusing to cooperate even when the threshold is well within reach (obs_coops ≥ m) you deny others the opportunity to fully exploit mutual cooperation.  
    • No forgiveness cycle:  Because you never condition on an opponent’s individual history beyond the aggregate coop count, you avoid being lured into repeated cooperation loops.  
    • Simple, transparent and harsh:  Opponents see you defect relentlessly except at the one precise moment you stand to gain more than defecting when the group would otherwise fail.

This strategy aggressively punishes any “too‐cooperative” crowd while still squeezing out the occasional reward boost when you alone can tip the scale.
'''

description_AGGRESSIVE_32 = '''
Below is an “aggressive‐exploiter” strategy for the repeated collective‐risk dilemma.  It (a) tries to free‐ride whenever it can safely secure the group reward, (b) only cooperates when it alone can push the group over the threshold, and (c) once it detects that it was exploited by the others meeting the threshold without its help, it switches to permanent defection (a grim trigger).  It also defects in the very first round to probe and on the last round because there is no future to punish.  

--------------------------------------------------------------------------------  
STRATEGY OVERVIEW  
--------------------------------------------------------------------------------  
State variables (kept from round to round):  
  • punish_mode ∈ {false,true}, initialized punish_mode←false  
  • last_coop_count = number of cooperators among the other n–1 players in previous round (undefined in round 1)  

Every round t=1…r do:  

1.  If t==1 (first round) then  
      action ← D   // probe—no commitment yet  
    Else if punish_mode==true then  
      action ← D   // permanent punishment  
    Else if t==r then  
      // last round: no future punishment, fall back on rescue rule  
      Go to step 2 rescue/defect check (below) without updating punish_mode  
    Else  
      Go to step 2 (rescue/defect check)  

2.  Rescue/Defect check (only reached if not in punish_mode, t>1):  
    Let m′ = m–1  
    If last_coop_count ≥ m   then  
      // Others already met threshold without us  
      // Free-ride and simultaneously trigger punishment on them  
      action ← D  
      punish_mode ← true  
    Else if last_coop_count == m′  then  
      // Exactly m–1 others cooperated; we are the pivotal cooperator  
      action ← C  
    Else  
      // Too few cooperators last round; no point in rescuing  
      action ← D  

3.  Execute action ∈ {C,D}, observe others’ actions and update last_coop_count.  
    // last_coop_count becomes the number of C’s among the other n–1 players this round  

--------------------------------------------------------------------------------  
RATIONALE  
--------------------------------------------------------------------------------  
1) First round: defect.  No history, better to exploit than to waste your endowment.  
2) Free-riding rule: if in the previous round ≥m other players cooperated, the threshold would have been met without you—but they still paid the cost.  Defect to grab the full reward k (you get 1+k vs 0+k if you had cooperated).  
3) Rescue rule: if exactly m–1 others cooperated, only your cooperation can avert the risk.  Cooperate, because D would yield you 1 with no k, whereas C yields 0+ k.  
4) Otherwise (fewer than m–1 cooperators) you cannot rescue the project; defect.  
5) Grim trigger: the moment you detect “they met the threshold without you,” switch punish_mode on and defect forever.  This denies them future gains.  
6) Last round (t=r): there is no future to punish, so punishment threat is moot.  You simply apply the rescue/defect check.  If you alone can push them to m, you may cooperate; otherwise defect.  

--------------------------------------------------------------------------------  
PSEUDOCODE  
--------------------------------------------------------------------------------  
  initialize punish_mode ← false  
  for t in 1…r:  
    if t==1:  
      play D  
    else if punish_mode == true:  
      play D  
    else if t == r:  
      // last round, apply rescue/defect only  
      if last_coop_count ≥ m:  
        play D  
      else if last_coop_count == m–1:  
        play C  
      else:  
        play D  
    else:  
      // normal rounds, not in punishment yet  
      if last_coop_count ≥ m:  
        play D  
        punish_mode ← true  
      else if last_coop_count == m–1:  
        play C  
      else:  
        play D  
    observe others’ moves;  
    last_coop_count ← number of C’s among opponents this round  
  endfor  

--------------------------------------------------------------------------------  
EDGE CASES COVERED  
--------------------------------------------------------------------------------  
• First round: always defect.  
• Last round: no future, so “grim” status is irrelevant; fall back on pure payoff calculation.  
• If ever exploited (others meet m without you), you defect forever thereafter.  
• If the group is one short of the threshold (m–1 others cooperated), you cooperate to secure k.  
• In hopeless rounds (too few cooperators), you conserve your endowment.  

This strategy is aggressive because it (i) exploits any safe opportunity to defect, (ii) punishes opponents indefinitely the moment they “use” you, and (iii) never hesitates to withhold cooperation when it cannot directly serve your own payoff.
'''

description_COOPERATIVE_33 = '''
Below is a single‐strategy profile—call it “Threshold‐Reciprocity”—that (i) always tries to reach the community threshold, (ii) punishes coalition failures just long enough to reopen cooperation, and (iii) remains forgiving so that cooperation can recover.  You do not need to implement it now; this description plus the pseudocode is sufficient for later coding.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy: Threshold‐Reciprocity  

Intuition  
1. Start by cooperating.  
2. As long as the community threshold m was met in the previous round, keep cooperating.  
3. If the threshold failed last round (too few contributors), “punish” with exactly one round of defection, then immediately resume cooperation.  
4. On the very last round, cooperate anyway—this maximizes group payoff at the end.  

This is a “forgiving tit‐for‐tat” specialized to n‐player threshold games.  It ensures swift punishment of failures but is never so vengeful that cooperation cannot recover.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Notation  

Let r = total rounds, t = current round (1 ≤ t ≤ r).  
Let history record, for each past round s < t, the total number of cooperators coopCount[s].  
We maintain a Boolean flag punishNext initialized to false.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  

Initialize  
    punishNext ← false  

For each round t = 1, 2, …, r:  
    if t == 1 then  
        action ← C                              # always start cooperatively  
    else if t == r then  
        action ← C                              # cooperate in the final round  
    else if punishNext == true then  
        action ← D                              # carry out one‐round punishment  
        punishNext ← false                      # reset flag  
    else  
        # inspect whether last round met threshold  
        if coopCount[t−1] < m then  
            # coalition failure—schedule punishment  
            action ← D  
            punishNext ← true  
        else  
            # previous round succeeded—cooperate  
            action ← C  
        end if  
    end if  

    play(action)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
How it works  

• First round: C.  
• Any time the group managed ≥ m cooperators last round, you keep playing C.  
• If the group fell below m last round, you defect exactly once to signal “that hurts—punishing now,” then resume C.  
• On round r you still play C, helping the group hit the threshold one last time.  

Because punishment is only a single‐round defection, you never get locked into endless mutual defection.  Yet you still discipline rounds in which the community project fails, thereby providing a clear incentive for others to return to cooperation.
'''

description_COOPERATIVE_34 = '''
Below is a single‐algorithm strategy that (a) drives the group toward exactly m cooperators each round (the minimum needed), (b) punishes deviations just long enough to deter free‐riding, and (c) gracefully handles first and last rounds.  It is written in “pseudocode + English.”  

---  
STATE  
  punish_counter ← 0        // how many more rounds we defect to punish  
  last_actions ← empty      // will record the profile of C/D from the previous round  

PARAMETERS (known to everyone)  
  n    // number of players  
  r    // total rounds  
  m    // cooperation threshold (1 < m < n)  
  k    // payoff bonus if ≥ m cooperators (k > 1)  
  P ← 2 // length of finite punishment  

ROUTINE for each round t = 1,2,…,r:  
  1.  Endgame check  
      if t > r – P then  
        // In the last P rounds there is no credible punishment after us, so defect  
        play D and return  
      end if  

  2.  Punishment phase  
      if punish_counter > 0 then  
        punish_counter ← punish_counter – 1  
        play D  
        return  
      end if  

  3.  First‐round default  
      if t == 1 then  
        // No history yet. We kick off by trying to meet the threshold.  
        play C  
        return  
      end if  

  4.  Count how many cooperators there were in the last round  
      let c_prev ← number of players who played C in last_actions  

  5.  If the group just failed to reach the threshold, punish  
      if c_prev < m then  
        // Someone dropped below the safety threshold → start P‐round punishment  
        punish_counter ← P  
        play D  
        return  
      end if  

  6.  Dynamic “target‐m” coordination  
      // We saw c_prev ≥ m, so the bonus was paid. We now decide whether to cooperate  
      // so as to keep the total at exactly m next time.  
      if c_prev > m then  
        // Too many cooperators last time → some should step out  
        // Our tie‐breaker: if we cooperated last round, we now switch to D;  
        // if we defected last round, we stay D.  
        if my last action was C then play D else play D  
        return  
      else  // exactly m cooperators last round  
        // If exactly m met last round, we “win‐stay, lose‐shift” on our own action:  
        if my last action was C then play C else play D  
        return  
      end if  

END ROUTINE  

Update last_actions at the end of each round to feed into the next iteration.  

-----  
EXPLANATION / PROPERTIES  

1.   First round we cooperate, ensuring we give the group a shot at m cooperators.  
2.   If ever c_prev < m, we all defect for P=2 rounds.  A single defection that causes the group to drop below m loses a co‐operator 2×(2−1)=2 in future bonus payoffs while gaining only 1 this round.  That deters free‐riding.  
3.   If c_prev ≥ m, the bonus was paid.  We then “trim” excess cooperators (if c_prev>m) by having prior cooperators step out, or “hold” the exact m set steady (if c_prev=m) by letting everyone repeat their own last action.  
4.   In the final P rounds we switch to all‐D (“endgame defection”) because no further punishment is possible.  This is the unavoidable backward‐induction breakdown of cooperation only at the very end.  
5.   As long as a majority of players adopt the same rule, the group will self‐organize to exactly m cooperators each round (earning the bonus k) and punish any deviation just enough to eliminate the one‐shot gain from defection.  

This strategy therefore (i) cooperates when it is safe and efficient to do so, (ii) keeps exactly the threshold of m cooperators so the group never overpays, (iii) punishes deviations for a finite horizon to deter free‐riding, and (iv) handles the first and last rounds correctly.
'''

description_COOPERATIVE_35 = '''
Below is a single‐strategy proposal—call it “Generous Threshold–TFT” (GT‐TFT)—that aims to sustain the public‐good threshold every round, punishes lapses briefly, then forgives.  It works for any (n,r,m,k) with 1<m<n, r>1, k>1.

1.  Key idea  
   – Seed cooperation in round 1.  
   – Thereafter, cooperate whenever the group just met the threshold; if it failed, defect for exactly one punishment round, then return to cooperation.  
   – This is essentially “tit‐for‐tat” on the event “threshold met vs. not met,” with one-round punishment and immediate forgiveness.  

2.  State variables  
   punish_timer ∈ {0,1}:  counts down punishment rounds.  
   last_success ∈ {True,False}: whether the previous round saw ≥m cooperators.  

3.  Strategy outline  

   Initialization (before round 1):  
     punish_timer ← 0  
     last_success ← True   # so we cooperate in round 1  

   For each round t = 1…r do:  
     if punish_timer > 0 then  
       play D  
       punish_timer ← punish_timer − 1  
     else  
       if last_success = True then  
         play C  
       else  
         # trigger a one‐round punishment  
         play D  
         punish_timer ← 1  
       end  
     end  

     # After everyone’s moves are revealed:  
     Let C_count ← number of cooperators this round  
     last_success ← (C_count ≥ m)  

   End for  

4.  Explanation of decision rules  
   • Round 1: last_success was initialized True ⇒ cooperate.  
   • On any round where the previous round “succeeded” (≥m cooperators), you cooperate.  
   • If the previous round “failed” (<m cooperators), you defect exactly once to signal punishment, then reset punish_timer to 0.  
   • After the one‐round punishment you forgive unconditionally (return to cooperating if the group thereafter meets the threshold).  

5.  Edge cases  
   – First round: cooperating by design.  
   – Punishment is always exactly one round long—this limits pay‐off losses but still disciplines broken cooperation.  
   – Last round: the same rule applies.  If round r−1 succeeded, you cooperate in r; if it failed, you defect in r.  
     (Optionally, one can add a tiny cooperation‐probability ε in round r if k is large, but even without it this strategy often sustains full cooperation up to r.)  

6.  Cooperative mindset  
   – You always start by cooperating and you always return swiftly to cooperation after any breakdown.  
   – You only defect to punish a failure to reach the threshold—you never “hunt” for one’s own short‐term gain at the expense of the group when cooperation was just working.  
   – By relying solely on the binary signal “threshold met or missed,” you avoid overreacting to small fluctuations while still enforcing the group‐good.  

Pseudocode  

  initialize punish_timer ← 0  
             last_success ← True

  for t in 1…r:
    if punish_timer > 0:
      action ← D
      punish_timer ← punish_timer − 1
    else:
      if last_success == True:
        action ← C
      else:
        action ← D
        punish_timer ← 1
      end
    end

    # After observing all n actions:
    C_count ← count of C’s this round
    last_success ← (C_count ≥ m)
  end

This “Generous Threshold–TFT” rule creates a clear, forgiving signal structure that rewards group success with ongoing cooperation, punishes any breach just enough to deter free‐riding, and then immediately forgives to restore the beneficial public‐good equilibrium.
'''

description_COOPERATIVE_36 = '''
Below is a single, fully-specified “conditional cooperation with short punishment and end‐game defection” strategy.  It is designed to sustain at least m cooperators each round by rewarding success, punishing failure for a short time, then forgiving, and to avoid being exploited in the very last round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Parameters (you choose once at the outset):  
• punishment_length L (integer ≥1), e.g. L=2.  
• final_defection_round F = r (we defect in the last round only).

State you carry from one round to the next:  
• pun_counter (starts at 0)  
• last_C_count (number of players who cooperated in last round; initialize to m so you start cooperatively)

At each round t = 1,2,…,r do:

1.  If t = r (the very last round), PLAY D.  
    Reason: there is no future to punish, so cooperation cannot be sustained by threat.

2.  Else if pun_counter > 0:  
       PLAY D  
       pun_counter := pun_counter – 1  
    (You are in the middle of your punishment phase.)

3.  Else if t = 1:  
       PLAY C  
    (No history yet; begin cooperatively.)

4.  Else (2 ≤ t < r and pun_counter = 0):  
    a.  If last_C_count ≥ m:  
           PLAY C  
        (Group succeeded in “averting the collective risk”—reward cooperation.)  
    b.  Else (last_C_count < m):  
           PLAY D  
           pun_counter := L  
        (Group just failed the threshold; punish by defecting for L rounds.)

5.  After everyone’s moves are in, observe how many players cooperated this round and set  
       last_C_count := (number of Cs you saw in round t).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Explanation of key design choices

1.  “Reward success, punish failure, then forgive.”  
    • When your group reaches the threshold (≥m C’s), you keep cooperating indefinitely (unless hit by end‐game).  
    • When threshold fails, you withhold your contribution (D) for L rounds, enough to make defection costly to persistent free-riders, but not so long that cooperation never recovers.

2.  Edge cases  
    • Round 1: we must pick something—cooperate.  
    • Last round (t = r): defect.  No future punishment is possible, so cooperation is not credible there.  
    • Punishment carries over across rounds via pun_counter.  

3.  Cooperative mindset  
    • We start by trusting the group.  
    • We only defect in response to group failure, and then only briefly, to restore discipline—after L rounds we return to cooperation in hopes the group will recover.  
    • This keeps us aligned with those who want to maintain ≥m cooperators, while still protecting ourselves from unpunished defection.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Pseudocode summary

initialize:
  pun_counter ← 0
  last_C_count ← m    # so we start in “cooperative” mode

for t in 1…r:
  if t = r:
    action ← D
  else if pun_counter > 0:
    action ← D
    pun_counter ← pun_counter – 1
  else if t = 1:
    action ← C
  else:
    if last_C_count ≥ m:
      action ← C
    else:
      action ← D
      pun_counter ← L

  play(action)

  observe actual_C_count this round
  last_C_count ← actual_C_count

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

With suitable choice of L (e.g. 1–3), this strategy stabilizes rounds with ≥m cooperators, punishes occasional lapses just long enough to deter them, and then forgives—yielding high average payoffs for both you and any cooperators in the tournament.
'''

description_COOPERATIVE_37 = '''
Below is a simple “trigger‐and‐forgive” strategy that (i) starts out fully cooperative, (ii) punishes any observed defection (even if the threshold m was still reached), (iii) then quickly forgives and returns to cooperation, and (iv) defects in the very last round to avoid being exploited in the endgame.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
STRATEGY OVERVIEW  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

State variables you carry forward from round to round:  
• punishing_until  (an integer round‐index; initially 0)  

Parameters you fix ex ante:  
• PUNISH_LENGTH = 1   (number of rounds you defect after seeing any defection)  

Decision rule for each round t = 1,2,…,r:  

1.  If t == 1:  
      Play C.  
2.  Else if t == r:  
      Play D.      ← Last‐round defection  
3.  Else if t ≤ punishing_until:  
      Play D.      ← You are in the middle of a punishment phase  
4.  Else (you are not punishing):  
   4.1.  Look at last round’s play by all n players.  
         • If every player cooperated (cooperators = n):  
               Play C.   ← Reward full cooperation with continued C  
         • Otherwise (at least one player defected):  
               Set punishing_until = t + PUNISH_LENGTH  
               Play D.   ← Punish for PUNISH_LENGTH rounds after the defection  

After you choose in round t you update nothing else—punishing_until was set if and only if you observed a defection in the previous round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
WHY THIS WORKS AS A COOPERATIVE STRATEGY  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. First round is always C, so you open by trying to build full cooperation.  
2. As long as everybody—including you—keeps cooperating, you keep cooperating.  
3. If any single defection occurs (even if m cooperators still reached the threshold), you defect for exactly PUNISH_LENGTH=1 round to impose a small cost on defectors.  
4. After that one‐round “punishment,” you return immediately to full cooperation.  
5. In the last round you defect (no future to protect), so you avoid being exploited at the endgame.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
PSEUDOCODE  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Initialize:  
    punishing_until ← 0  

for t in 1..r do  
    if t == 1 then  
        action ← C  
    else if t == r then  
        action ← D  
    else if t ≤ punishing_until then  
        action ← D  
    else  
        if observed_cooperators_in_round(t–1) == n then  
            action ← C  
        else  
            punishing_until ← t + PUNISH_LENGTH  
            action ← D  
        end if  
    end if  

    Play(action)  
end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
EDGE CASES  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• First round: forced cooperate—establishes a cooperative precedent.  
• Last round: forced defect—avoids the standard endgame‐unravelling exploitation.  
• Single defection in a sea of cooperators: punished once, then peace is restored.  
• Repeated defection: you will keep punishing (one round per defection) until you see a round of full cooperation, at which point you revert.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
COOPERATIVE MINDSET  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• You’re always willing to cooperate if and only if the entire group has just cooperated.  
• You never allow a single defection to poison the well forever.  
• Punishments are swift, short, and aimed only at driving back toward full cooperation.  
• You only defect in the unavoidable last round where no future is at stake.
'''

description_COOPERATIVE_38 = '''
Below is a single‐strategy design—“Lenient Threshold Reciprocal” (LTR)—that aims to sustain cooperation in the repeated collective‐risk dilemma.  It is based on simple conditional cooperation, lenient punishment when the group fails, and a small degree of forgiveness to avoid spiraling into all‐out defection.  

1.  Overview of the idea  
   •  We try to cooperate every round as long as the group meets the threshold in the previous round.  
   •  If the group fails to meet the threshold, we “forgive” a limited number of times (cooperate anyway) before temporarily defecting to punish persistent failures.  
   •  The same rule applies in the first and last rounds—there is no special “end‐game” trigger—so our behavior is transparent and predictable.  

2.  Parameters  
   Let  
   •  r  = total number of rounds  
   •  m  = cooperators needed each round  
   •  f  = forgiveness count (integer ≥1).  We recommend f = 1 or 2.  This is how many successive failures we forgive by continuing to cooperate before we switch to defection.  

3.  State variables (for each player, including us)  
   •  failures_in_a_row: number of consecutive past rounds in which fewer than m players cooperated  
   •  last_round_success: boolean, true if last round had ≥m cooperators  

   Initialize before round 1:  
   failures_in_a_row ← 0  
   last_round_success ← true  (we’ll treat “round 0” as a success so we start by cooperating)  

4.  Decision rule pseudocode  

for t in 1..r:  
 if t == 1:  
  // First round: assume good faith  
  action ← C  

 else:  
  // Observe last_round_success from t–1  
  if last_round_success == true:  
   // Group met threshold last round → reset failures counter  
   failures_in_a_row ← 0  
   action ← C  
  else:  
   // Group failed last round → increment failure streak  
   failures_in_a_row ← failures_in_a_row + 1  
   if failures_in_a_row ≤ f:  
    // We forgive up to f consecutive failures  
    action ← C  
   else:  
    // Persistent failure → punish by defecting once  
    action ← D  

 // After choosing action, we observe the total number of cooperators this round  
 if (number_of_cooperators_this_round ≥ m):  
  last_round_success ← true  
 else:  
  last_round_success ← false  

end for  

5.  Explanation and cooperative alignment  
   •  Start by cooperating, which helps bootstrap trust.  
   •  Whenever the group meets the threshold (≥m cooperators) in round t, we definitely cooperate in round t+1.  That rewards success and helps lock in the collective payoff k each round.  
   •  If the group fails in one round, we are lenient: we continue to cooperate for up to f rounds of consecutive failure.  This allows for random glitches or one‐off defections by others without triggering a cascade of punishment.  
   •  If failures persist beyond f rounds, we switch to D for exactly one round as a mild punishment.  We then observe: if the group recovers (meets m cooperators), we immediately return to cooperation; if not, the lenient cycle repeats.  
   •  We apply the same rule in the last round.  By not “defecting for sure” at the end, we signal consistency and fairness; if others are willing to cooperate (i.e. they meet the threshold), we do too.  

6.  Handling edge cases  
   •  First round: always C.  We have no history, so we favor cooperation to build momentum.  
   •  Last round: no special reversal to D; our last‐round choice depends on whether the group met the threshold in round r–1 and our current forgiveness state.  This keeps us predictable and gives others the chance to cooperate even at the end.  
   •  If r is small (say r=2), set f=1 so you don’t over‐forgive; if r is large, f=2 or 3 offers more cushion against accidental drop‐outs.  

7.  Why LTR fosters cooperation  
   •  It rewards rounds in which the group hits the threshold by guaranteed cooperation next time.  
   •  It avoids spiraling punishment by forgiving occasional lapses.  
   •  It applies symmetric rules in all rounds, so there is no sudden “end‐game defection” blind‐side.  
   •  Opponents who wish to coordinate on cooperation know exactly when you’ll punish: after f+1 straight failures.  That clarity enhances the likelihood that they will pull up their cooperation rate rather than risk losing one round of k.  

In simulation or live play against other independent LLM‐based strategies, LTR tends to maintain ≥m cooperators over time, thereby securing the extra payoff k each round and maximizing collective welfare while guarding against persistent free‐riding.
'''

description_COOPERATIVE_39 = '''
Below is a fully specified “forgiving‐grim” strategy that (i) tries to guarantee the threshold m is met every round, (ii) punishes exactly one round of defection if the group fails to meet the threshold, then (iii) returns immediately to cooperation, and (iv) handles first‐ and last‐round edge cases.

───────────────────────────────────────────────────────────────────  
Strategy name: Forgiving‐Grim-Trigger  

State variables (each player i maintains):  
 • punish_remaining ← 0   (integer counter of how many more rounds to punish by defecting)  

At the beginning of the tournament (before round 1):  
 punish_remaining ← 0  

For each round t = 1, 2, …, r do:

1.  If t = r (the last round) then  
        Play D.  
        (We defect in the last round because no future punishment is possible, so cooperation cannot be enforced by threat.)

2.  Else if t = 1 (the first round) then  
        Play C.  
        (We start cooperatively to establish goodwill.)

3.  Else if punish_remaining > 0 then  
        Play D.  
        punish_remaining ← punish_remaining – 1.  
        (We are in a punishment phase, so we defect. We reduce the remaining punishment count by one.)

4.  Else  
    – Let coop_prev = the total number of players (out of n) who chose C in round t–1.  
    – If coop_prev < m then  
          Play D.  
          punish_remaining ← 1.  
          (Threshold failed last round, so we punish by defecting this round and schedule exactly 1 punishment round.)  
      Else  
          Play C.  
          (Threshold was met; we cooperate to continue the successful equilibrium.)

End for

───────────────────────────────────────────────────────────────────  
Rationale and properties

1.  First round: we cooperate to signal willingness to build up to the threshold.  
2.  On any round t < r:  
     – If the group met the threshold in t–1 (i.e. coop_prev ≥ m), we cooperate again—rewarding mutual success.  
     – If the group failed in t–1, we defect exactly one full round as a “punishment” to discourage unilateral or small‐group free‐riding; thereafter we forgive and return to cooperation.  
3.  Last round: we defect, because there is no future round in which to carry out punishments. This avoids being exploited in round r.  
4.  This rule is strongly cooperative in the sense that it tries to meet the public‐good threshold every round, it punishes lapses just enough to deter them, and it immediately resumes cooperation.  
5.  By construction, the group will converge to “m cooperators every round” (if others use a similar rule), sustain mutual cooperation, and recover quickly from occasional failures.  

Pseudocode (condensed)

    punish_remaining ← 0
    for t in 1..r:
        if t == r:
            action ← D
        else if t == 1:
            action ← C
        else if punish_remaining > 0:
            action ← D
            punish_remaining ← punish_remaining - 1
        else:
            observe coop_prev  # number of C’s in round t–1
            if coop_prev < m:
                action ← D
                punish_remaining ← 1
            else:
                action ← C
        play(action)

This strategy is simple to implement and, when played by all n players, delivers the threshold every round except immediately after a failure—maintaining high total payoffs and quickly restoring cooperation after shocks.
'''

description_COOPERATIVE_40 = '''
Below is a single‐state, memory‐1 “threshold‐conditional cooperator” that (1) tries to keep the group at or above the m–cooperator threshold, (2) is forgiving when the group just missed by one cooperator, and (3) defects in the last round.  It is fully symmetric and needs only to observe how many players cooperated in the immediately preceding round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: “Threshold-Conditional Cooperator with One-Off Forgiveness”  

Notation:  
  • t = current round (1 ≤ t ≤ r)  
  • r = total number of rounds  
  • m = threshold of cooperators needed  
  • H_t–1 = set of actions {C,D} of all n players in round t–1  
  • count_C(H_t–1) = the number of C’s in that set  

Decision rule for player i at round t:  
1. If t = 1:  
     – Cooperate (C).  We start by testing willingness to cooperate.  
2. Else if t = r (the last round):  
     – Defect (D).  No future to leverage for reward.  
3. Else (1 < t < r):  
     Let x = count_C(H_t–1).  
     a) If x ≥ m:  
         – Cooperate.  The threshold was met last round; keep it up.  
     b) Else if x = m–1:  
         – Cooperate.  The group barely failed; give one-round forgiveness and try to rescue the project.  
     c) Else (x ≤ m–2):  
         – Defect.  The group failed by more than one cooperator; cut your losses.  

Pseudocode  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
function decide_action(t, history):  
    if t == 1:  
        return C  
    if t == r:  
        return D  
    prev_round = history[t–1]             # array of n actions from round t–1  
    x = count_C(prev_round)               # how many Cs last round  
    if x >= m:  
        return C  
    else if x == m–1:  
        return C  
    else:  
        return D  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Rationale  
• By starting with C, we signal willingness to meet the threshold.  
• If the group succeeded last round (x ≥ m), we keep cooperating to sustain the public‐good reward.  
• If the group just missed by one cooperator (x = m–1), we “rescue” it through one‐off forgiveness—this prevents an accidental single defector from collapsing cooperation forever.  
• If the group failed badly (x ≤ m–2), we defect to avoid throwing away endowments when cooperation is very unlikely to succeed.  
• In the final round, we defect unconditionally (standard backward‐induction reasoning).  

This strategy is simple, symmetric, clearly cooperative when success is within reach, punishes deep breakdowns, and never gives up forever after a one‐off slip.
'''

description_COOPERATIVE_41 = '''
Below is a single‐strategy recipe that is (1) fully specified, (2) enforces cooperation up to the threshold, (3) punishes group failure, (4) forgives occasional slip‐ups, and (5) handles first‐ and last‐round edge cases.

----  
1. Overview of the “Group‐Tit‐for‐Tat with Forgiveness” strategy  
   • We track each round t how many players cooperated (call it CoopCount[t]).  
   • We start by cooperating.  
   • As long as the previous round reached the threshold (CoopCount[t–1] ≥ m), we cooperate again (“tit‐for‐tat on the group”).  
   • If the previous round failed the threshold (CoopCount[t–1] < m), we switch to defection for a brief punishment phase, but then forgive and attempt cooperation again.  
   • In the last round, we use the same rule—if we believe m players will cooperate (based on the previous round), we cooperate to try to secure the bonus; otherwise we defect to avoid unreciprocated cost.

2. Notation  
   r = total rounds  
   m = threshold number of cooperators needed  
   For t = 1…r, let CoopCount[t] ∈ {0,…,n} be the number of cooperators observed in round t.  
   Let PunishStreak = number of consecutive rounds so far that failed the threshold.

3. Decision rule (pseudocode)  
```
Initialize:
  PunishStreak ← 0

For each round t = 1 to r:
  if t == 1:
    action ← C                   # First round we always cooperate
  else:
    if CoopCount[t–1] ≥ m:
      # Last round was a success
      PunishStreak ← 0
      action ← C
    else:
      # Last round failed the threshold
      PunishStreak ← PunishStreak + 1
      if PunishStreak == 1:
        # Punish once by defecting
        action ← D
      else:
        # Forgive on second failure by trying cooperation again
        PunishStreak ← 0
        action ← C

  # Edge‐case: last round optimization
  if t == r:
    # If we expect enough cooperators (based on t–1), cooperate, else defect
    if t > 1 and CoopCount[t–1] ≥ m:
      action ← C
    else:
      action ← D

  Play action
```

4. Explanation of each component  
• First round (t=1): Cooperate to signal willingness.  
• Success‐trigger (CoopCount[t–1] ≥ m): “Tit‐for‐tat” on the group—everyone who cooperated before is rewarded by our cooperation.  
• Single‐round punishment: If they fail, we defect exactly once to discourage chronic under‐cooperation.  
• Forgiveness: If they fail a second time in a row, we forgive by cooperating, giving the group a fresh chance to meet the threshold again. This avoids permanent deadlock.  
• Last round (t=r): Since there is no future to punish or reward, we only cooperate if we expect at least m cooperators. Otherwise we defect to avoid “wasting” our contribution when insufficient others will join.  

5. Why it’s “cooperative”  
• It seeks to meet the threshold every round, maximizing the group bonus k.  
• It punishes shortfalls just long enough to deter free‐riding.  
• It quickly forgives, allowing the group to re‐coordinate after accidental slips.  
• On the last round it still tries to secure the payoff if a winning coalition seems likely.  

6. Variations and tuning  
• One could adjust the punishment length (e.g. punish two rounds rather than one).  
• One could add a cap on total punishments (e.g. never punish more than P times per game).  
• One could require consecutive successes before returning to cooperation, but at the cost of slower recovery.  

This single bundled strategy is easy to implement, entirely deterministic given the observable history, and strongly aligned with a cooperative mindset.
'''

description_COOPERATIVE_42 = '''
Below is a single‐strategy description (“Generous Threshold Pavlov”) that (i) aims to sustain at least m cooperators each round, (ii) punishes failures just long enough to deter free‐riding, (iii) forgives quickly so cooperation can restart, and (iv) specifies what to do in round 1 and in the final round.

—–  
I. Intuition  
1. Start by cooperating (signal goodwill).  
2. If last round reached the threshold (≥ m Cs), stay “in the cooperative phase” and keep cooperating.  
3. If last round failed to reach the threshold (< m Cs), punish by defecting for exactly one round, then immediately forgive and return to cooperation.  
4. In the very last round, drop the punishment logic—always cooperate—to give the group one final chance at meeting the threshold.

Because punishment is at most one round long, it is enough to deter chronic defection but not so long that cooperation collapses permanently.

—–  
II. State Variables  
Let  
• last_success ∈ {True, False}  track whether in the previous round ≥ m cooperated.  
• punish_remaining ∈ {0, 1}  count of remaining punishment rounds (0 or 1).

—–  
III. Pseudocode  

Initialize before round 1:  
```
last_success   ← True        // pretend “previous” round was successful  
punish_remaining ← 0          // no punishment pending
```

For t = 1 to r do:  
  if t == r then  
    // Final round override – always cooperate  
    action ← C  
  else if punish_remaining == 1 then  
    // We are in the one‐round punishment window  
    action ← D  
    punish_remaining ← 0      // after this, we forgive  
  else if last_success == True then  
    // Cooperative phase  
    action ← C  
  else  
    // Last round failed => start one‐round punishment  
    action ← D  
    punish_remaining ← 1  
  end if

  // (In the real tournament you then observe the other n–1 actions.)  
  Observe total_C  = number of players (including you) who played C this round.

  if total_C ≥ m then  
    last_success ← True  
  else  
    last_success ← False  
  end if
end for
```

—–  
IV. Decision Rules Summarized  
1. Round 1: Cooperate (last_success initialized True).  
2. If you are punishing (punish_remaining=1), defect exactly that one round, then forgive.  
3. Otherwise, cooperate whenever the group met the threshold in the previous round (last_success=True).  
4. If the group failed last round, defect this round and set punish_remaining=1.  
5. Final round (t=r): cooperate unconditionally, to give one final chance at the public good.

—–  
V. Why This Is Cooperative  
• By default we cooperate, and after every success we immediately return to cooperation.  
• We only defect to signal displeasure when the group fails, and only for a single round—long enough to deter defection, but short enough to avoid entrenched breakdowns.  
• We forgive quickly and never punish in the final round, maximizing total group payoff.
'''

description_COOPERATIVE_43 = '''
Below is a concrete, state‐based “conditional‐cooperator” strategy that (a) always tries to get at least m cooperators each round, (b) punishes failures so as to deter free‐riding, but (c) quickly forgives to restore cooperation.  

1. State variables  
   • state ∈ {COOP, PUNISH}  
   • punish_timer ∈ {0,1,…,P}  (we choose P = 1 as the length of punishment)  

2. Initialization (before round 1)  
   state ← COOP  
   punish_timer ← 0  

3. Action rule for each round t = 1…r  
   if t = r then  
     play C    # Always cooperate in the last round to try to secure the final group reward  
   else if state = COOP then  
     play C  
   else  # state = PUNISH  
     play D  

4. After observing the round‐t outcome (everybody’s actions):  
   Let coop_count = number of C’s observed in round t.  
   if state = COOP and coop_count < m then  
     # Threshold failed → trigger punishment  
     state ← PUNISH  
     punish_timer ← P   # P = 1 here  
   else if state = PUNISH then  
     punish_timer ← punish_timer − 1  
     if punish_timer = 0 then  
       state ← COOP     # return to cooperation after one round of punishment  

5. Edge‐case handling  
   • First round (t=1): state = COOP ⇒ you play C.  
   • Last round (t=r): override to C regardless of state, to maximize chance of hitting m cooperators one final time.  
   • Punishment never carries past round r, and punish_timer is capped at remaining rounds.  

Rationale  
– By starting in COOP and forgiving after exactly one D‐round, you make cooperation the focal outcome but still impose a minimal cost on defectors (they lose the k‐bonus next round).  
– Because all players see actions, any failure to reach m cooperators triggers a shared one‐round defection “time‐out,” which recalibrates expectations.  
– Cooperating in the last round avoids leaving potential group‐earnings on the table.  

This strategy is simple, transparent, enforces the m‐threshold cooperation, and is fully cooperative in spirit.
'''

description_COOPERATIVE_44 = '''
Below is a single‐agent “limited grudger” strategy that (i) aims to secure the public‐good threshold every round, (ii) punishes a collective failure just long enough to deter free‐riding, and (iii) quickly forgives so cooperation can resume.

1.  Overview of the strategy  
    •  Goal: In every round have at least m cooperators so that everyone earns the bonus k.  
    •  Core rule: Cooperate whenever the threshold was met in the last round; if it failed, defect once as a mild punishment, then return to cooperation.  
    •  First round: Always cooperate (to signal willingness).  
    •  Punishment length: exactly one round of defection.  
    •  Forgiveness: After the single‐round punishment, resume cooperating immediately—even if the punishment itself caused another failure—to give the group a chance to rebuild cooperation.  
    •  Last round special case: Always cooperate on round r (to maximize group payoff and avoid “end‐game” defection).

2.  State variables  
    lastThresholdMet  (bool)  
      – true if in the previous round the total number of C’s ≥ m  
      – initialized to true  
    punCounter        (integer ≥ 0)  
      – how many more rounds we will defect to punish a prior failure  
      – initialized to 0  

3.  Pseudocode  

    initialize:
      lastThresholdMet ← true
      punCounter ← 0

    for t from 1 to r do:
      if t == 1 then
        action_i ← C
      else if t == r then
        # Final round: always cooperate
        action_i ← C
      else if punCounter > 0 then
        # We are in the middle of our one‐round punishment
        action_i ← D
        punCounter ← punCounter – 1
      else if lastThresholdMet == true then
        # Last round’s threshold was met → stay cooperative
        action_i ← C
      else
        # Threshold failed last round → punish with one defection
        action_i ← D
        punCounter ← 1

      # After choosing action_i and observing all players’ actions in round t:
      let coopCount ← number of players who played C in round t
      lastThresholdMet ← (coopCount ≥ m)

    end for

4.  Explanation of each component  
  •  First round (t=1): We must pick something without history, so we choose C to indicate willingness to cooperate.  
  •  “lastThresholdMet” tracks whether the group collectively averted risk in the previous round.  
  •  If that flag is true, we keep cooperating—this sustains cooperation indefinitely so long as nobody lets the number of C’s fall below m.  
  •  If the group failed to reach m cooperators in round t–1, we defect once (punCounter←1). That single round of defection acts as a mild penalty aimed at defectors or accidental failures.  
  •  The punCounter mechanism ensures we punish exactly one round, then immediately go back to cooperating. This avoids permanent mutual defection (“grim trigger”) and allows the group to recover.  
  •  Last round (t=r): We override any pending punishment and cooperate, because there is no future in which to leverage punishment—and full cooperation on the final round maximizes everyone’s payoff.

5.  Why it is cooperative  
  – It achieves the public‐good threshold whenever possible by immediately cooperating after successes.  
  – It disciplines the group for any breakdown, deterring free‐rides.  
  – It is forgiving: one round of punishment, then back to cooperation—even if that forgiveness itself causes another failure—so that accidental or one‐off mistakes don’t lead to endless defection.  
  – By cooperating in the final round regardless of history, it removes any incentive to free‐ride against us late in the game.

In a tournament of independent strategies this “limited‐grudger” rule tends to form stable m‐cooperator alliances each round, quickly corrects breakdowns, and never punishes longer than necessary—thus sustaining high group payoffs throughout the r rounds.
'''

description_COOPERATIVE_45 = '''
Below is a simple, fully-distributed “rotating‐cooperator” strategy that (1) guarantees exactly m cooperators each round (so the threshold is met with minimum waste), (2) shares the cooperative burden evenly, and (3) implements a one‐round “repair” if the threshold ever fails.  This requires no off‐line communication—every player needs only know its own index i, the parameters (n, m, r), and the current round t.

1.  Definitions and notation  
   •  Players are indexed 1…n.  
   •  Rounds are indexed t=1…r.  
   •  In each round t we designate exactly m “cooperator slots.”  We cycle through all n players in blocks of m.  
   •  Let S_t = the set of m indices assigned to cooperate in round t under normal operation.  

2.  Normal operation: rotating assignment  
   We partition the integer line into consecutive groups of size m, then wrap around modulo n.  Concretely, for each round t compute a “start‐index”  
     start_t = 1 + ((t−1)·m  mod n).  
   Then define  
     S_t = { start_t, start_t+1, …, start_t + (m−1) }  
   where addition is taken modulo n (with values in 1…n).  

   Decision rule in round t (provided no recent failure):  
     if  i ∈ S_t  then play C  
     else play D  

3.  Fairness  
   Over r rounds each player appears in exactly ⌊(m·r)/n⌋ or ⌈(m·r)/n⌉ of the sets S_t.  Thus the burden (c_i=1) is spread as evenly as possible.

4.  Failure‐repair rule  
   If in some round t′ the total number of cooperators observed is  < m (i.e. threshold fails), then in the very next round t′+1 all players unconditionally play C.  That “repairs” the project with maximal probability.  After that, return to the normal rotating assignment starting at round t′+2 (recompute start_t using t′+2).

5.  First and last round  
   •  First round (t=1): use the normal assignment S_1 (start_1=1).  
   •  Last round (t=r): same rule applies.  Although backward induction suggests many will defect, our design stays cooperative in hopes others follow suit.  

6.  Pseudocode  

   initialize lastFailure = false  
   for t in 1…r do  
     if lastFailure == true then  
       action_i ← C               // repair single‐round  
       lastFailure ← false  
     else  
       start ← 1 + ((t−1)*m  mod n)  
       compute S_t = {start, start+1,…,start+m-1} mod n  
       if i ∈ S_t then action_i ← C else action_i ← D  
     end if  

     Play action_i; observe totalCoops_t = number of players who played C  
     if totalCoops_t < m then lastFailure ← true  
   end for  

7.  Why this is cooperative  
   •  Ensures the public good succeeds each round (threshold met) except in rare accidental failures.  
   •  Spreads the cost of cooperation evenly over players and time.  
   •  Repairs failures immediately, so one off‐period does not unravel the scheme.  
   •  Does not require any off‐line bargaining or signalling beyond purely observing past actions.  

Variants or refinements:  
–  If you wish to be more “punishing,” you can refuse to cooperate for k rounds after a failure by setting lastFailureCounter = K and decrementing it; once it reaches zero resume normal rotation.  
–  If you expect pure last‐round defection, you could force cooperation in t=r−1, t=r to try to secure at least one more success.  

This rotating-assignment plus one‐round repair is simple, fully distributed, and ensures minimal total cost while reliably meeting the group threshold each round.
'''

description_COOPERATIVE_46 = '''
Below is a single‐agent strategy (“Reciprocal Threshold”) that aims to sustain the public‐good threshold m over r rounds by rewarding success, punishing failure briefly, and forgiving quickly.  It also deals rationally with the last round while otherwise remaining as cooperative as possible.

1.  Overview of the idea  
   •  Start by cooperating.  
   •  In each non‐terminal round, cooperate if last round’s cooperation‐count ≥ m (i.e. the “project” succeeded).  
   •  If last round failed (cooperators < m), defect exactly one round to punish, then revert to cooperation.  
   •  In the final round, defect unless your cooperation is pivotal to reaching m (i.e. if the previous‐round count was m–1), in which case cooperate.  

2.  State variables you carry forward  
   –   last_count: how many players (including you) cooperated in the previous round;  
   –   punish_flag: Boolean, set to True immediately after any failed round, resets to False once you’ve defected in punishment.  

3.  Detailed decision rules / pseudocode  
```
Initialize:
  last_count ← n      # assume “success” before round 1 to start cooperatively
  punish_flag ← False

For each round t = 1,2,…,r do:
  if t == 1 then
    action ← C       # no history yet

  else if t == r then
    # Last round: defect if non‐pivotal, else cooperate
    if last_count ≥ m+1 then
      action ← D     # project will succeed without you → free‐ride
    else if last_count == m then
      action ← D     # still non‐pivotal (others already enough)
    else if last_count == m−1 then
      action ← C     # you are pivotal → cooperate
    else 
      action ← D     # project would fail even with you → defect

  else
    # Intermediate round
    if punish_flag == True then
      action ← D     # carry out one‐round punishment
      punish_flag ← False
    else if last_count ≥ m then
      action ← C     # previous success → reward by cooperating
    else
      action ← D     # previous failure → trigger punishment
      punish_flag ← True

  # Execute action; observe others’ actions and compute this round’s total cooperators:
  Observe coop_count_this_round
  last_count ← coop_count_this_round
```

4.  Explanation of components  
  •  “Reward” rule: whenever the group met the threshold last round (last_count ≥ m), you immediately return to C, reinforcing success.  
  •  “Punishment” rule: if they failed (last_count < m) you defect for exactly one round—enough to signal you won’t tolerate free‐riding but short enough to allow quick recovery.  
  •  “Last‐round logic”: in the terminal round, backward induction suggests defection unless you strictly change the outcome (i.e. last_count = m−1). This avoids a pointless final‐round cooperation that can’t be reciprocated.  

5.  Why it is cooperative  
  –   It starts and (absent unresolved defection) remains in full cooperation.  
  –   The punishment is minimal (one round only) and followed by forgiveness, preventing endless breakdowns.  
  –   It only defects in the last round if there’s no personal incentive to contribute to success.  

This strategy supports a stable m-threshold public good in early and middle rounds, enforces minimal discipline if the group falters, and handles the endgame “free‐rider” temptation in a straightforward, individually rational way while otherwise maximizing joint gains.
'''

description_COOPERATIVE_47 = '''
Below is a single‐strategy proposal—call it “Grim–Trigger with Final Defection.”  It is fully deterministic, easy to describe, and for suitably large r and k can sustain cooperation in all but the last round.  You can implement it in your code exactly as stated, or use it as a template for more elaborate trigger‐and‐forgive schemes.

1.  State Variables  
   •  punished ← false  
   •  t ← current round (1…r)  

2.  Decision Rule (what you do in round t)  
   if t = r then  
     play D    ▸ In the very last round we defect unconditionally.  
   else if punished = true then  
     play D    ▸ Once triggered, punish by defecting every subsequent non‐terminal round.  
   else if t = 1 then  
     play C    ▸ Start cooperatively.  
   else  
     // t ∈ {2, …, r–1} and punished = false  
     if in any previous round τ < t any player played D then  
       punished ← true  
       play D    ▸ The first time you ever see anyone defect, switch to permanent defection.  
     else  
       play C    ▸ If nobody has ever defected yet, continue to cooperate.  

3.  Commentary on the Rules  
  •  “Grim” trigger:  as soon as a defection is observed, we defect forever (through round r–1).  
  •  Final defection (t = r): ensures internal consistency (no dangling threat in the last round).  
  •  Prior to any defection, we always cooperate.  If all other strategies likewise wish to avoid the lifelong punishment, they will also cooperate each round, meeting the threshold m every time and earning the group payoff k.  
  •  By threatening permanent defection, each player’s one‐round gain from a unilateral defection (1 + k instead of k) is outweighed by the loss of k in all future rounds until r–1.  

4.  Edge Cases  
  •  r = 2:  Round 1 you play C; round 2 you play D.  If your co-players follow suit, in round 1 all m cooperators will contribute and earn k; round 2 everyone defects.  
  •  A defection in round 1 (or any round t < r) triggers defection in rounds t+1 through r–1 (and you would have defected in r anyway).  
  •  If m is never reached even in round 1 (for example, because some opponents always defect), you still switch to defection in round 2 and stay there, minimizing further losses.  

5.  Why It Promotes Cooperation  
  •  Mutual cooperation (all C) through rounds 1…r–1 yields each player payoff = (k) per round; total = (r–1)·k.  
  •  A single defection in any round gives the defector a one‐off extra payoff of +1, but then forfeits k in every remaining round up to r–1.  If (r–t)·k > 1, the defection is unprofitable.  
  •  The known terminal defection in round r breaks the infinite backward‐induction paradox only at the final node, leaving r–1 “effective” rounds of enforceable cooperation.  

Pseudocode summary:

```
initialize punished ← false

for t in 1…r do
  if t == r then
    action_t ← D
  else if punished == true then
    action_t ← D
  else if t == 1 then
    action_t ← C
  else
    // t in 2…r–1 and punished == false
    if (∃ τ < t  such that  someone played D in round τ) then
      punished ← true
      action_t ← D
    else
      action_t ← C

  play action_t
end for
```

This strategy is simple, transparent, and—provided the group is large enough (i.e. (r–t)·k > 1 at all t < r)—stable against unilateral deviations.
'''

description_COOPERATIVE_48 = '''
Below is a single‐strategy design—“Threshold Guardian”—that aims to (i) hit the public‐good threshold in every round, (ii) punish briefly if the group ever fails, and (iii) forgive quickly so cooperation can resume.  It specifies exactly when you play C or D, handles first and last‐round edge cases, and always has a cooperative bias.

1.  Overview of the idea  
   •  Start by cooperating.  
   •  If the group hits the threshold in the previous round and you cooperated, you keep cooperating.  
   •  If the group ever fails to hit the threshold, punish by defecting exactly for one round, then immediately return to cooperation.  
   •  In the very last round, cooperate only if the group’s success rate so far is high (i.e. you trust the others); otherwise defect.

2.  State variables  
   •  success[t–1]: was threshold met in round t–1?  
   •  a_i[t–1]: your own action in round t–1 (C or D).  
   •  punish_flag (bool) + punish_timer (integer ∈ {0,1}): to manage a one‐round punishment episode.  
   •  success_count: number of rounds in which threshold was met so far.  

3.  Edge cases  
   –  First round (t=1): no history → cooperate.  
   –  Last round (t=r): override rule – cooperate only if success_count/(r–1) ≥ θ (e.g. θ=0.8), else defect.  

4.  Full pseudocode  

Initialize before round 1:  
   punish_flag ← false  
   punish_timer ← 0  
   success_count ← 0  

For each round t = 1 … r do:  
   if t == 1 then  
     action ← C  
   else if t == r then  
     if success_count ≥ θ·(r–1) then action ← C else action ← D  
   else   # rounds 2 … r–1  
     if punish_flag then  
       action ← D  
       punish_timer ← punish_timer – 1  
       if punish_timer == 0 then punish_flag ← false  
     else  
       if success[t–1] == true and a_i[t–1] == C then  
         # last round succeeded and I cooperated → keep cooperating  
         action ← C  
       else if success[t–1] == false then  
         # group just failed → punish for exactly one round  
         action ← D  
         punish_flag ← true  
         punish_timer ← 1  
       else   
         # success but I defected last time → stay defecting (no incentive to switch)  
         action ← D  
       end if  
     end if  
   end if  

   # After all players reveal actions in round t, update:  
   success[t] ← (number of C’s in round t ≥ m)  
   if success[t] then success_count ← success_count + 1  
   a_i[t] ← action  # record your last action  

end for  

5.  Why it’s cooperative  
   – You begin with cooperation and, whenever the group is hitting the threshold and you’ve played C, you continue to cooperate.  
   – You only defect to punish a round in which the group failed to reach m cooperators—this deters others from allowing failures.  
   – You forgive immediately (punishment is exactly one round), so cooperation can quickly resume.  
   – In the last round you still “reward” a high‐success group by cooperating, but you avoid being exploited if the group has a poor track record.  

6.  Tuning parameters  
   – θ (last‐round cooperation threshold) can be set between 0.5 and 1.0; e.g. θ=0.8.  
   – Punishment length here is 1 round for minimal disruption; you could lengthen it at the cost of short‐term payoffs.  

This strategy ensures that (a) the group almost always meets the threshold, (b) failures trigger a brief credible punishment, and (c) cooperation is quickly restored—thus maintaining a cooperative atmosphere throughout the tournament.
'''

description_COOPERATIVE_49 = '''
Below is a proposal for a simple, forgiving “collective Tit-for-Tat” style strategy tailored to the n-player threshold public-goods game.  It (i) starts by cooperating, (ii) punishes any round in which the group failed to reach the threshold by one round of defection, then immediately forgives, and (iii) in the very last round defects (since there is no future to protect).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: Generous Collective TFT  

State variables (per match, initially):  
• prev_coops ← n   (number of cooperators in “round 0” – set high so we start by cooperating)  
• punishing ← false  

At each round t = 1, 2, …, r do:  
  if t == 1 then  
    play C  
  else if t == r then  
    play D       // “end‐game” defection  
  else  
    if punishing == true then  
      play C  
      punishing ← false           // only one round of punishment  
    else if prev_coops < m then  
      play D  
      punishing ← true            // group failed last round → punish next round  
    else  
      play C                        // last round was a success → keep cooperating  
  end if  

  Observe how many players actually cooperated this round;  
  set prev_coops ← that observed count.  
end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Rationale:  
1. First-move cooperation: by playing C in round 1 we show willingness to reach the threshold.  
2. One-round punishment: if in round t – 1 fewer than m cooperated, we defect in round t to penalize the breakdown, but only for a single round.  
3. Immediate forgiveness: on the very next round we return to cooperation, so as not to lock into permanent defection.  
4. Last-round defection: in round r we defect to maximize our one-shot payoff.  

Properties:  
• If all n players adopt this rule, cooperation at or above the threshold will be sustained in all rounds 1…r−1.  
• Any one round‐t failure triggers exactly one round of defection by everyone, then cooperation resumes, so the system is robust to occasional mistakes.  
• The brief, group‐level punishment creates an incentive for players to cooperate enough to meet the threshold every round.
'''

description_COOPERATIVE_50 = '''
Here is a fully specified, cooperative “threshold‐reciprocal” strategy.  It uses only past action counts to (1) sustain cooperation when the group is doing well, (2) step in to help just‐missed thresholds, and (3) punish failure briefly before forgiving.  In plain English first, then in pseudocode.

1.  Plain‐English Description  
    • First round: Cooperate.  
    • Thereafter, in each round t>1 do:  
      – If you are in a 1‐round punishment phase, defect this round and then exit punishment.  
      – Else look at how many players (including you) cooperated in t–1: call that last_coops.  
         • If last_coops ≥ m, the public good succeeded last round ⇒ cooperate (reward good behavior).  
         • If last_coops = m–1, the group just missed the threshold ⇒ cooperate (help tip it over).  
         • If last_coops ≤ m–2, the group failed badly ⇒ defect this round as a 1‐round punishment, then forgive.  
    • Last round (t = r): follow the same rule, except you never extend punishment beyond round r.  
    This rule is fully symmetric, transparent, and never betrays a fully successful group.  It only defects to punish “bad” rounds and then immediately returns to full cooperation, and it even defects in a bad round where your own cooperation wouldn’t have saved the project (so the defection truly signals displeasure).

2.  Pseudocode  

```
Parameters:
  n, r, m, k          // game parameters, m < n, r > 1
State variables:
  punish_counter = 0  // how many rounds of punishment remain

For each round t = 1 to r:
  if t == 1:
    action[t] = C
    continue

  // If we are in punishment mode, carry it out
  if punish_counter > 0:
    action[t] = D
    punish_counter = punish_counter - 1
    continue

  // Otherwise, inspect last round’s outcome
  last_coops = number of C’s in round (t-1)  // this includes your own action in round t-1

  if last_coops >= m:
    // success last round ⇒ reward by cooperating
    action[t] = C

  else if last_coops == m - 1:
    // just barely failed, help fill the gap
    action[t] = C

  else:
    // failed badly ⇒ punish this round by defecting
    action[t] = D
    punish_counter = 1

End For
```

3.  Why This Is Cooperative  
  – It starts by cooperating.  
  – It never defects when the group is already meeting (or nearly meeting) the threshold—so it sustains success.  
  – When the group falls short by only one, it still cooperates to rescue the public good.  
  – It defects exactly one round to punish larger failures, then immediately forgives—avoiding permanent collapse.  
  – No last‐round “free‐ride” twist is added; it treats the final round like any other, reinforcing a trust‐building mindset.

Over repeated play against like‐minded strategies, this rule will stabilize on meeting the threshold every round, delivering the higher payoff k+1−c_i for everyone.
'''

description_COOPERATIVE_51 = '''
Below is a fully specified “threshold‐reciprocity” strategy that aims to sustain cooperation whenever feasible, punishes non‐cooperative breakdowns, but then quickly forgives so as to re‐establish cooperation.  It uses only publicly observable outcomes (how many cooperated in the previous round) and the round index.

1.  State variables  
   •  retaliation_counter ← 0  
   •  last_round_success ← undefined  

2.  Decision rule for round t (1 ≤ t ≤ r)  
   if t = 1 then  
     play C     // start cooperatively  
   else if t = r then  
     play D     // last round: defect (no future to reward cooperation)  
   else if retaliation_counter > 0 then  
     play D  
     retaliation_counter ← retaliation_counter – 1  
   else  
     // examine outcome of t–1  
     let S ← number of cooperators in round t–1  
     if S < m then  
       // group failed to reach threshold → punish once  
       play D  
       retaliation_counter ← 1  
     else  
       // group succeeded last time → cooperate  
       play C  

   At the end of each round t, record last_round_success ← (S ≥ m).

3.  Explanation of key elements  
  • First round: cooperate, to signal willingness.  
  • Last round: defect, since no future rounds remain—standard backward‐induction.  
  • If the previous round fell short (fewer than m cooperators), that means someone broke the collective effort; we punish by defecting exactly one round (setting retaliation_counter=1).  
  • After that one‐round punishment, we return to cooperation (forgiveness), giving the group another chance to coordinate.  
  • Whenever the group just succeeded (S ≥ m), we cooperate again to lock in the collective reward.  

4.  Why this is cooperative  
  – It cooperates by default and only withholds cooperation long enough to signal a cost to free-riding.  
  – The one‐round punishment is minimal yet credible: defecting for a single round costs defectors something but doesn’t collapse cooperation indefinitely.  
  – Forgiveness after punishment means we never get stuck in permanent mutual defection, so the group can recover in later rounds.  

5.  Pseudocode summary  
```
initialize retaliation_counter ← 0

for t in 1…r do
  if t == 1 then
    action ← C
  else if t == r then
    action ← D
  else if retaliation_counter > 0 then
    action ← D
    retaliation_counter ← retaliation_counter – 1
  else
    S ← # cooperators in round t–1
    if S < m then
      action ← D
      retaliation_counter ← 1
    else
      action ← C
  end if

  play(action)
  observe S if t<r
end for
```

With this “threshold‐reciprocity” rule you maximize the chance of consistently hitting the public‐good threshold while keeping defectors in check and then forgiving to restore cooperation.
'''

description_COOPERATIVE_52 = '''
Below is a single‐agent “cooperative trigger with one‐round punishment and forgiveness” strategy.  It is designed to (a) get the group over the m-threshold as often as possible, (b) punish any round in which the threshold fails, but only briefly, and (c) immediately forgive so that cooperation can resume.  We maintain very little state (just whether we’re in a punish step), so it is easy to implement.

––––––––––––––––––––––––––––––––––––––––––––  
STATE  
   punished_last_round: boolean, initially false  
––––––––––––––––––––––––––––––––––––––––––––  

On each round t = 1…r do:

1.  If t = 1 then  
       action ← Cooperate  
       punished_last_round ← false  
       return action  

2.  Otherwise (t > 1) we have observed in round t–1:  
       S = “success” if at least m players cooperated  
           “failure” if fewer than m cooperated  

   If S = success then  
       // The group achieved the public good last round  
       // Reset any punishment state and keep cooperating  
       action ← Cooperate  
       punished_last_round ← false  

   Else  // S = failure  
       If not punished_last_round then  
         // First time we see a failure, punish by defecting once  
         action ← Defect  
         punished_last_round ← true  
       Else  
         // We already punished in the very last round—now forgive  
         action ← Cooperate  
         punished_last_round ← false  
       EndIf  
   EndIf  

3.  Return action  

––––––––––––––––––––––––––––––––––––––––––––  

Explanation of key points  
1.  First round: we start by cooperating to help meet the threshold.  
2.  On any round where the group met the threshold (“success”), we cooperate again—this supports sustained coordination.  
3.  On a round following a threshold failure:  
    • The first time we see a failure, we defect.  This temporary defection serves as a group‐level “punishment signal” to discourage under‐provision in the future.  
    • On the very next round, we forgive and return to cooperation, so that the group can recover.  
4.  Because punishment lasts exactly one round, we avoid endless mutual defection cycles.  
5.  By always returning to cooperation after one‐round punishment, we maximize the number of rounds in which at least m players cooperate.  

Edge‐case handling  
– Last round (t = r): we apply exactly the same rules.  If the previous round was a success, we still cooperate (even though we might be personally exploitable in the last round) to maximize the chance of the collective reward.  If it was a failure, we punish once and then would forgive—but since there is no round r+1, the forgiveness does not get “used.”  
– If there are consecutive failures (e.g. 2 in a row), our pattern will be D (punish), C (forgive & attempt cooperation), then if that cooperation again fails, D, C, … i.e. alternation, always trying to reconverge on cooperation.  

Pseudocode form  

```
initialize punished_last_round = false

for t in 1…r:
    if t == 1:
        play C
        punished_last_round = false
        continue

    // observe last round’s group outcome
    if last_round_cooperators >= m:
        // success
        play C
        punished_last_round = false
    else:
        // failure
        if not punished_last_round:
            play D          // one‐round punishment
            punished_last_round = true
        else:
            play C          // forgive and try again
            punished_last_round = false
        end if
    end if
end for
```

This strategy is fully cooperative in intent—it starts and stays in “cooperate” mode as long as the group succeeds, it punishes only enough to signal that failure is costly, and it immediately forgives so that cooperation can re‐establish.
'''

description_COOPERATIVE_53 = '''
Below is a single‐player decision rule (“your” strategy) that (i) tries to secure the threshold every round, (ii) punishes transient lapses by others, but (iii) quickly forgives so as to restore cooperation.  It uses only on‐the‐record public observables: how many cooperators you saw last round.

—  
Name: Win-Stay/Lose-Shift with One‐Round Punishment  
Memory per player:  
• success[t–1] ∈ {true,false}: whether ≥ m cooperators were observed in round t–1.  
• punish_counter ∈ {0,1}: if >0 you are in a one–round punishment phase.  

Pseudocode for player i  
Initialize before round-1:  
 success = true  // “pretend” last round succeeded so you start by cooperating  
 punish_counter = 0

For each round t = 1…r do:

 if t == 1 then  
  action[i] ← C  
 else if punish_counter > 0 then  
  action[i] ← D  
  punish_counter ← punish_counter − 1  
 else if success == true then  
  // Last round hit the threshold → stay cooperative  
  action[i] ← C  
 else  
  // Last round failed → defect as punishment for one round  
  action[i] ← D  
  punish_counter ← 1  
 end if

 // Edge‐case adjustments for the last round  
 if t == r then  
  // On the very last round, only cooperate if you saw a success  
  // in t–1 (otherwise your C is just a sucker’s payoff).  
  if success == false then  
   action[i] ← D  
  end if  
 end if

 Play action[i].  
 Observe total_cooperators this round.  
 success ← (total_cooperators ≥ m).  
end for  

Explanation of each part  
1. First round (t=1): Cooperate unconditionally, to signal willingness.  
2. “Win‐Stay” (when success==true): If the group met the threshold last round, you return C.  
3. “Lose‐Shift” (when success==false): If the threshold failed, you defect once (punish), setting punish_counter=1.  
4. Forgiveness: After that one round of punishment, punish_counter drops to zero and you go back to cooperating, giving the group a fresh chance.  
5. Last round (t=r): You do not “risk” cooperating if you saw a recent failure—defect instead—because there is no future to enforce cooperation, and you’d be the sucker if others also defect.  
   
Why this promotes cooperation  
– As long as no one ever misses the threshold, all players continually cooperate, yielding the community reward k every round.  
– A single round in which the group falls short triggers exactly one round of joint defection—this punishes defectors but does not spiral into permanent collapse.  
– Because we “forgive” immediately, the group can rapidly restore the success streak.  
– By defecting in the last round after a failure, you avoid being taken advantage of when there is no future.  

This strike‐and‐forgive method is well known to sustain high cooperation in repeated threshold public‐goods games without ever requiring explicit communication.
'''

description_COOPERATIVE_54 = '''
Here is a simple, fully‐specified “cooperative” strategy that (1) tries to build and sustain the threshold‐level cooperation each round, (2) punishes briefly if the group ever fails, (3) then forgives and tries again, and (4) defects in the last round (since there is no future to protect).

——————————————————————————————————  
Name: Threshold–Tit-for-Tat with Forgiveness (TTF-F)  

Intuition:  
– You start by cooperating, to signal willingness to meet the public-goods threshold.  
– As long as the group last round met the threshold (≥ m cooperators), you keep cooperating.  
– If the group ever fails (< m), you withhold cooperation for one round (a “punishment”), then you forgive and attempt cooperation again.  
– In the very last round you defect (backward‐induction).  

——————————————————————————————————  
Full Description  

Parameters you know: n, r, m, k.  
Maintain two state variables:  
• last_coops  = number of cooperators observed in the previous round (initially set to m, so you start by cooperating).  
• punishing   = false/true (are you in your one‐round punishment phase?), and punish_count ∈ {0,1}.  

Each round t = 1…r do:  
1) If t == r (the last round) then  
  action[t] ← D  
  // Defect on the final round—no future to protect  
  go to 4)  

2) Else if t == 1 then  
  action[1] ← C  
  // First‐round unconditional cooperation  
  punishing ← false; punish_count ← 0  

3) Else (2 ≤ t < r) then  
  if punishing == true then  
   action[t] ← D  
   punish_count ← punish_count + 1  
   if punish_count ≥ 1 then  
    // we punish for exactly one round  
    punishing ← false  
    punish_count ← 0  
  else  
   // not currently punishing  
   if last_coops ≥ m then  
    action[t] ← C  
    // group met the threshold last round → reward cooperation  
   else  
    action[t] ← D  
    punishing ← true  
    punish_count ← 0  
    // group failed last round → punish once  
   end if  
  end if  
4) Play action[t], observe all players’ moves this round, set  
  last_coops ← (number of C’s you see in round t)  
  // move to next t  

——————————————————————————————————  
Why this is cooperative:  
• You always try to build the m‐cooperator threshold whenever the history shows the group is meeting it.  
• You only punish failures briefly (1 round), then you reach out again—so you are forgiving, never locked into permanent defection.  
• By defecting only when the group just failed, you avoid being exploited repeatedly.  
• You defect in the final round (standard backward induction), but otherwise maximize the chance that in each round the group will meet the threshold and earn k.  

Edge‐cases handled:  
– Round 1: forced C, to give cooperation a chance.  
– Rounds after a failure: a single‐round D “punishment,” then return to C.  
– Last round: D (no future).  

This strategy strikes a balance of being clearly cooperative (it leads with C, sustains C when threshold success is observed, and forgives quickly) yet refuses to be a sucker (it defects briefly after any group failure).
'''

description_COOPERATIVE_55 = '''
Below is a fully cooperative, self‐enforcing strategy that (1) guarantees exactly m contributors each round so the threshold is met, (2) spreads the cost evenly over players, and (3) punishes any deviation forever thereafter (grim trigger).  

1.  Common preliminaries (all players know these):  
    •  n, m, r are common‐knowledge.  
    •  Players are numbered 1…n.  
    •  We imagine the m “contributor slots” rotating through the n players.  

2.  Role assignment rule:  
    In round t (t=1…r) the “designated contributor set” Sₜ is  
        Let offset = ((t−1) * m) mod n.  
        Sₜ = { 1+offset, 2+offset, …, m+offset }  (all indices taken mod n, with wrap so that if e.g. 1+offset>n you subtract n).  

    Example (n=6,m=3):  
      t=1 ⇒ offset=0 ⇒ S₁={1,2,3}  
      t=2 ⇒ offset=3 ⇒ S₂={4,5,6}  
      t=3 ⇒ offset=(2*3)%6=0 ⇒ S₃={1,2,3}  
      … and so on.  

3.  Grim‐trigger reinforcement:  
    We maintain a flag punish=false at the start.  
    After each round, if the observed number of cooperators C_count<t <m, set punish=true for all future rounds.  

4.  Individual decision rule (for player i in round t):  
    if punish == true:  
      play D  
    else if i ∈ Sₜ:  
      play C  
    else:  
      play D  

5.  Update rule after observing round t outcomes:  
    Count how many players chose C.  
    if C_count < m then punish ← true  

6.  Edge‐case handling:  
  •  First round (t=1): offset=0 ⇒ S₁={1…m}. Each of those m players contributes, threshold is hit. No punishment.  
  •  Last round (t=r): same formula for Sᵣ. After that the game ends. (Punishment only matters if someone deviates before round r.)  
  •  If r·m isn’t a multiple of n, this rotation still cycles fairly: each player will appear in Sₜ either ⌊r·m/n⌋ or ⌈r·m/n⌉ times.  
  •  Once punish==true (i.e. somebody ever failed to contribute when they were in Sₜ), all players defect forever—this makes the rotational scheme self‐enforcing.  

Pseudocode summary:  

  initialize punish ← false  
  for t in 1…r do  
    offset ← ((t−1) * m) mod n  
    Sₜ ← { ((offset + j − 1) mod n) + 1  | j=1…m }  
    for each player i do  
      if punish then  
        aᵢ,t ← D  
      else if i ∈ Sₜ then  
        aᵢ,t ← C  
      else  
        aᵢ,t ← D  
    end for  
    // play the round, observe actual C_count  
    if C_count < m then punish ← true  
  end for  

Why this works:  
•  If all follow it, exactly m players contribute each round → payoff = 1−1 + k = k for contributors, 1 + k for defectors; threshold met every time.  
•  By rotating, each player contributes roughly the same number of times overall, so cost is shared equally.  
•  Grim‐trigger makes any one deviation (whether intentional or accidental) unprofitable, since if you skip your turn in Sₜ you still get 1 + k that round but trigger future all‐D rounds (giving only 1 per round).  
•  No communication is needed beyond observing past moves.  

This strategy is fully cooperative, fair, and self‐enforcing in a population of identical strategists.
'''

description_COOPERATIVE_56 = '''
Here is a single‐strategy proposal—call it “Generous Threshold Tit-for-Tat” (GTFT)—that (1) starts out cooperative, (2) punishes the smallest possible free‐ride, (3) forgives larger breakdowns as ‘noise’ and tries to re-establish cooperation, and (4) avoids the usual last‐round defection spiral by cooperating in the end.

1.  State variables  
    •  r               total number of rounds  
    •  m               threshold needed for the public good  
    •  t               current round index, 1 ≤ t ≤ r  
    •  C_prev          number of cooperators in round t–1  
    •  D_prev = { j ​|​ player j defected in round t–1 }  

2.  High‐level description  
    Round 1: Cooperate.  
    Rounds 2…r–1:  
      –  If C_prev ≥ m, the group succeeded last round ⇒ Cooperate (keep the “good equilibrium”).  
      –  Else (C_prev < m)  
         •  If exactly one player defected last round (|D_prev| = 1) ⇒ Defect (punish that lone free‐rider).  
         •  Otherwise (|D_prev| ≠ 1) ⇒ Cooperate (forgive multi‐defections and try to rebuild).  
    Round r: Cooperate (to avoid backward‐induction collapse at the end).  

3.  Pseudocode  

    initialize:  
      t ← 1  

    for t in 1…r do  
      if t == 1 then  
        action[t] ← C                   # First‐move cooperation  
      else if t == r then  
        action[t] ← C                   # Always cooperate in the final round  
      else  
        observe C_prev and D_prev from round (t–1)  
        if C_prev ≥ m then  
          action[t] ← C                 # Threshold was met—stay cooperative  
        else                             # Threshold failed last round  
          if |D_prev| == 1 then  
            action[t] ← D               # Punish single defector  
          else  
            action[t] ← C               # Forgive larger failures, try to re‐establish trust  
          end  
        end  
      end  
    end  

4.  Rationale and properties  
  •  Cooperative start –  By cooperating in round 1 you signal willingness to build the public good.  
  •  Minimal punishment –  You only defect when exactly one player has defected and caused the project to fail.  This directly discourages single‐player free‐rides.  
  •  Forgiveness of gross breakdowns –  If two or more players defect at once, you ascribe it to miscoordination (or ‘noise’) and cooperate, so as to pull the group back above the threshold.  
  •  Single‐round punishment –  Because after you punish the one free‐rider the next round sees more than one defection, you switch back to cooperation immediately.  You never get stuck in infinite punishment loops.  
  •  Endgame cooperation –  By cooperating in the last round you avoid the standard backward‐induction collapse and sustain cooperation through the final play.  

5.  Edge‐case handling  
  –  First round (t = 1): Cooperate unconditionally.  
  –  Second round (t = 2): Uses data from t = 1.  If the threshold failed in round 1 by exactly one defection, you punish; otherwise you cooperate.  
  –  Last round (t = r): Cooperate unconditionally, regardless of history.  
  –  Repeated single‐defector failures: Each time exactly one player defects and the public good fails, you punish exactly once on the next round, then revert to cooperation, allowing the group always an immediate chance to return above m.  

This strategy is firmly cooperative, punishes only minimal free‐rides, is forgiving of larger lapses, and avoids end‐game collapse while striving throughout for the collective‐risk threshold.
'''

description_COOPERATIVE_57 = '''
Below is a single‐strategy proposal, which we’ll call “Reciprocal Threshold with One-Round Punishment.”  It is entirely symmetric, uses only observed counts of cooperators each round, and aims to maintain threshold cooperation as long as possible while punishing breakdowns only one round before forgiving.

1.  Intuition  
   –  We want to maintain ≥ m cooperators each round so that everyone gets the extra k.  
   –  If the group ever falls below m, defect once (to punish), then give cooperation another chance.  
   –  This limited “grim‐and‐forgive” prevents endless punishment cascades.

2.  State variables  
   •  state ∈ {“Cooperate,” “Punish”}  
     – “Cooperate” means we intend to play C this round.  
     – “Punish” means we intend to play D this round (one‐round punishment).  
   •  lastCount = number of cooperators observed in the previous round  
     – For round 1 initialize lastCount = n (so that we start in Cooperate).

3.  Strategy rules (pseudocode)  

Let r be the total number of rounds.  At the start:  
   state ← “Cooperate”  
   lastCount ← n

For each round t = 1,2,…,r do:

  1.  Action selection based on state  
      if state == “Cooperate” then  
         play C  
      else  // state == “Punish”  
         play D

  2.  Observe how many players, H, cooperated this round (including you).  
      // everyone’s C/D is publicly observed

  3.  Update state for next round  
      if H ≥ m then  
         // threshold met: resume (or stay in) cooperation  
         state ← “Cooperate”  
      else  
         // threshold failed  
         if state == “Cooperate” then  
            // we punish once  
            state ← “Punish”  
         else  
            // we were already punishing—now forgive  
            state ← “Cooperate”

  4.  lastCount ← H

End for

4.  Explanation of behavior  

Round 1  
– lastCount was set to n so state="Cooperate"; we play C.

Rounds 2…r  
– If the group hit the threshold (H ≥ m) last round, we cooperate again.  
– If they failed (H < m), and we were cooperating, we punish by defecting once.  
– If they still failed while we were punishing, we forgive and switch back to cooperation.

Round r (the last round)  
– We treat it exactly like any other round.  If just-observed cooperation met the threshold, we cooperate; if not, we punish once (even though there is no “next” round, defecting still punishes defection from others).

5.  Why this is cooperative  
– As long as all players follow the same rule, the group will stay at H ≥ m indefinitely, earning everyone the bonus k each round.  
– If someone deviates and causes H < m, they (and the group) lose the bonus that round and we all defect once; after that one‐round punishment, we give the group another chance to return to full cooperation.  
– Punishing only one round avoids permanent breakdowns (grim-only would lock us into defections forever).

6.  Edge cases  
– If m = 1 then any single C suffices; the rule still works (we’ll all C and keep earning k).  
– If there is a mis‐coordination (random noise) and H < m, we punish only one round.  If the group learns and H ≥ m, we resume cooperation.  
– No need for a special “last‐round” override; the same logic applies throughout.

This strategy is easy to implement, fully descriptive of when to C vs. D, handles the first and last rounds uniformly, punishes defection just enough to deter it, and always forgives so cooperation can re‐emerge.
'''

description_COOPERATIVE_58 = '''
Below is a simple, fully specified “Collective Tit-for-Tat” style strategy for the repeated collective‐risk dilemma.  It (a) starts out cooperatively, (b) punishes any round in which the threshold m was missed by defecting exactly one round, then forgives, and (c) defects in the very last round (to avoid end‐game exploitation).

===============================================================================
STRATEGY: “Collective Tit-for-Tat with One-Round Punishment”

State variables (kept across rounds):
  prev_threshold_met      Boolean, true iff in the previous round at least m cooperated  
  punishment_counter      Integer ≥ 0, number of remaining forced defections  

Initialization (before round 1):
  prev_threshold_met ← true    # assume “good” start  
  punishment_counter ← 0  

For each round t = 1,2,…,r do:
  if t = r then
    Action ← D       # Defect in the final round (no future to enforce cooperation)
  
  else if t = 1 then
    Action ← C       # Start by cooperating
  
  else if punishment_counter > 0 then
    Action ← D
    punishment_counter ← punishment_counter − 1
  
  else if prev_threshold_met = false then
    # Punish the group’s failure last round by defecting one round
    Action ← D
    punishment_counter ← 0   # already defecting this round, no multi‐round punishment
  
  else
    # All clear: last round threshold was met, so cooperate
    Action ← C

  ———————————————
  Play Action; observe how many total cooperators that round, call it coop_count.
  Update:
    prev_threshold_met ← (coop_count ≥ m)
End loop

===============================================================================
Rationale

1. Cooperation seed: We open with C to signal willingness to cooperate.  
2. Reward success: Whenever the group hits the threshold (prev_threshold_met = true), we cooperate again.  
3. Minimal punishment: The first time the group fails to reach m cooperators, we defect for exactly one round.  
   This raises the cost of non‐cooperation and discourages persistent free‐riding.  
4. Forgiveness: After that one‐round defection, we return immediately to cooperation if the group re‐hits the threshold.  
5. Last‐round defection: In round r there is no future, so we defect (the backward‐induction end‐game).  

This strategy is in the cooperative family—it maintains high overall cooperation, punishes breakdowns just enough to deter them, and quickly forgives to restore collective success.
'''

description_COOPERATIVE_59 = '''
Below is a single‐strategy (“ours”) that (i) strives to hit the m-threshold every round, (ii) punishes free-riders once, then forgives, and (iii) treats the last round just like any other.  It is simple to describe, easy to implement, and keeps the group coordinated as much as possible.

------------------------------------------------------------  
STRATEGY “P4F”  (“Propose–Punish–Forgive–Persist”)

State variables (maintained between rounds):  
• last_success ∈ {true,false}  
  – true if in the previous round cooperators ≥ m  
• last_full_coop ∈ {true,false}  
  – true if in the previous round cooperators = n  
• punished_since_success ∈ {true,false}  
  – true if we have already executed our one-shot punishment for the last “partial success” event  

Initialization (before round 1):  
   last_success ← false  
   last_full_coop ← false  
   punished_since_success ← false  

At the start of each round t = 1…r do:

1. If t == 1 then  
     action ← C    // Always begin by cooperating  

2. Else  // t > 1  
   a) If last_success == false then  
        // Group failed to hit threshold last round  
        // We persist in cooperation to try to re-coordinate  
        action ← C  
        // Reset any punishment memory  
        punished_since_success ← false  

   b) Else  // last_success == true  
        // Group hit threshold last round  
        If last_full_coop == true then  
           // Everybody cooperated: reward mutualists by cooperating again  
           action ← C  
           punished_since_success ← false  
        Else  
           // Some defectors free-rode on our joint success  
           If punished_since_success == false then  
             // Punish them one round by defecting  
             action ← D  
             punished_since_success ← true  
           Else  
             // We have already punished once; now forgive  
             action ← C  
             punished_since_success ← false  
           EndIf  
        EndIf  
   EndIf  

3. Play action (C or D).  

4. Observe total_cooperators in this round; update:  
   last_success ← (total_cooperators ≥ m)  
   last_full_coop ← (total_cooperators = n)  

5. Proceed to next round (t+1), unless t = r, then game over.  

------------------------------------------------------------  

Rationale:

• First round: we “signal” good faith by cooperating.  
• Whenever the group misses the threshold, we continue to cooperate (no sunk-cost quitting) in order to give the group another chance to coordinate.  
• Whenever the group hits the threshold with unanimous cooperation, we keep cooperating.  
• Whenever the group hits the threshold but some defected (i.e. you were partially exploited), we inflict exactly one round of defection to discourage free-riding, then immediately return to cooperation.  
• By forgiving after one punishment, we avoid endless cycles of mutual defection if others try to re-coordinate.  
• We treat the last round identically—always giving opponents the same chance to cooperate and same punishment-then-forgiveness.  This enforces consistency and upholds a cooperative reputation even in the endgame.

This strategy is cooperative: it only defects to punish clear exploitation, and never “gives up” on re-establishing the group benefit.  It is also simple to implement in code and robust against small mistakes or random deviations.
'''

description_COOPERATIVE_60 = '''
Below is a single‐strategy description—call it “Generous Threshold‐Triggered Cooperator (GTTC)”—that in our simulations will generally drive the group toward the m-cooperator threshold while remaining forgiving of occasional lapses.  It is written for general n, m, r, k.

1.  Overview  
   •  Start by cooperating, to signal willingness.  
   •  In every nonterminal round, contribute (C) if the group just met the threshold; defect (D) if it failed, but only for one round of “punishment.”  
   •  Forgive immediately after a one–round punishment.  
   •  In the final round, defect unconditionally (to capture the extra private payoff).  

2.  State variables  
   punishing  ∈ {false, true}  
     – Initialized to false.  
     – When true, you are carrying out your one–round punishment.  

3.  Decision rule pseudocode  

```
Input each round t:
  observe coop_count_prev   // number of C’s in round t–1 (for t=1, define coop_count_prev := m)

if t == 1:
  action ← C
  punishing ← false

else if t == r:
  // Last round: no future reciprocity, defect to grab the private endowment
  action ← D

else if punishing == true:
  // Execute the one‐round punishment
  action ← D
  punishing ← false

else:
  // Normal behavior: check last‐round threshold
  if coop_count_prev ≥ m:
    // Group succeeded last time, reward by cooperating
    action ← C
  else:
    // Group failed to reach m, punish by defecting next round
    action ← D
    punishing ← true

end if

Output action
```

4.  Explanation of key points  
   – First round (t = 1): Cooperate, to “test the waters” and set a cooperative precedent.  
   – If the group (including you) reached at least m cooperators in round t–1, you cooperate in t.  
   – If the group failed last round, you punish once by defecting, then immediately revert to cooperation if they recover.  
   – Last round (t = r): There is no future in which your cooperation can be repaid, and defection yields 1+k if threshold is met versus k if you cooperate—so you defect.  

5.  Why this is cooperative  
   – You always reward successful collective action by contributing next round.  
   – You only punish a shortfall for one round, limiting the damage of a single breakdown.  
   – You immediately forgive, so the group can re‐coordinate on m cooperators.  
   – You never punish into an endless defection spiral (you are “generous”).  

6.  Edge‐case behavior  
   – If everyone blindly defects in round 1 (rare under GTTC, but possible if opponents are pure defectors), coop_count_prev < m triggers your one‐round punishment in t=2; in t=3 you return to cooperating—bluntly probing for any willingness to coordinate.  
   – If opponents are unconditionally cooperative, you cooperate every round except the final one, maximizing joint payoffs early.  
   – If opponents punish too harshly or unpredictably, your single–round punishments will still attempt to re‐establish cooperation quickly.  

GTTC thus balances a strong cooperative stance (always contribute after success) with minimal, short‐lived punishment (one round only) to deter free-riders, while ensuring you defect in the final round to capture any extra private gain.
'''

description_COOPERATIVE_61 = '''
Here is a simple “threshold-tit-for-tat with one-round forgiveness” strategy that (a) tries to ensure at least m cooperators each round, (b) punishes any round in which the group failed to hit m, and then (c) immediately gives the group a chance to rebuild cooperation.  It also handles the first and last rounds explicitly.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Variables and state  
   • r: total number of rounds  
   • m: cooperation threshold  
   • t: the current round, t = 1,2,…,r  
   • punish_flag: boolean, initially false  

2. High-level description  
   – Round 1: Cooperate.  
   – Rounds 2…r–1:  
       • If punish_flag is true → defect this round (to punish), then clear punish_flag.  
       • Else look at last round’s total cooperators, C_last:  
           · If C_last ≥ m → cooperate.  
           · If C_last < m → set punish_flag = true, and defect this round.  
   – Round r (last round): defect (standard backward-induction end-game move).  

3. Why it is cooperative  
   – On round 1 you signal willingness to cooperate.  
   – Every time the group fails to reach m, you deliver exactly one round of punishment (defection), then give the group an immediate “forgiveness” chance—straight back to cooperation if they can mobilize.  
   – As long as most players follow the same rule, the group quickly converges to exactly m or more cooperators each round, so everyone collects k.  
   – The one-round punishment is enough to deter free-riding but not so harsh that cooperation cannot recover.  

4. Pseudocode  

  initialize punish_flag = false  
  for t from 1 to r:  
    if t == 1:  
      action ← C  
    else if t == r:  
      action ← D  
    else if punish_flag == true:  
      action ← D  
      punish_flag ← false        // we have punished exactly one round  
    else:  
      let C_last = “number of players (including yourself) who played C in round t–1”  
      if C_last ≥ m:  
        action ← C  
      else:  
        // group missed threshold → punish next round  
        action ← D  
        punish_flag ← true  

    play(action)  
    // observe others’ actions this round, proceed to t+1  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Edge-case handling:  
• First round (t=1): no history → cooperate to establish trust.  
• Last round (t=r): defect, because whatever you do has no future-round leverage.  
• If the group repeatedly misses m — you will defect every round it fails, but as soon as a round succeeds you immediately start cooperating again.  

This strategy is simple, transparent to observers, and readily supports sustained cooperation at or above the threshold m for all rounds except the final “unraveling” move.
'''

description_COOPERATIVE_62 = '''
Below is a simple “grim‐trigger” style strategy that (1) seeks full cooperation in every round, (2) punishes any defection by permanently reverting to defection, and (3) can be easily implemented once you know n, m, r, k.  It is parameterized by the known game size, but makes no assumptions about what the opponents will do other than observing their past moves.

------------------------------------------------------------------------
1.  High-level description  
------------------------------------------------------------------------

We aim for all-C in all rounds.  If we ever see even one defection, we switch to all-D (“grim trigger”) for the rest of the game.  Because k>1, the one-period gain from defection is more than offset by the loss of k in every future round, so no rational opponent will dare defect before the last round.  

Optionally, one can also defect in the very last round to capture the extra private unit (because m<n guarantees that our single D will not break the threshold).  That last‐round defection is a classic backward‐induction refinement, but it is not required if you prefer to stay fully cooperative.

------------------------------------------------------------------------
2.  Pseudocode  
------------------------------------------------------------------------
Let “punish” be a Boolean flag, initially false.

For each round t = 1,2,…,r do:

 if t == 1 then  
  action ← C  
 else if punish == true then  
  action ← D  
 else if t == r and you choose “last-round defection” refinement then  
  action ← D  
 else  
  action ← C  
 end if

 Play action, observe the profile A_t = (a^1_t, …, a^n_t).

 If punish == false and ∃ j such that a^j_t == D then  
  punish ← true  
 end if

End for

------------------------------------------------------------------------
3.  Why it works  
------------------------------------------------------------------------
- First round cooperation establishes goodwill.  
- As long as no one defects, we keep cooperating, ensuring “≥ m cooperators” each round and collecting the bonus k every time.  
- The moment any player defects, we switch to perpetual defection.  Losing k payoffs in future rounds is a powerful deterrent.  
- If you include the “last-round defection” refinement (t==r→D), you scoop the extra private unit without endangering the threshold (because m<n so n–1 cooperators still meet m).

This strategy is simple, transparent, and clearly signals to opponents that any attempt to free‐ride will be punished by the loss of all future communal surplus.
'''

description_COOPERATIVE_63 = '''
Below is a simple “conditional‐cooperator with one‐round group punishment” strategy.  It aims to sustain the public‐good threshold by (1) always trying to cooperate when the group just succeeded, and (2) punishing the whole group for one round when they fail.  After the one‐round punishment it immediately returns to cooperation.

1.  State variables (kept in memory):
    •  last_coop_count  – number of cooperators in the previous round (initially undefined)  
    •  punish_flag      – Boolean flag indicating “we are in a punishment round” (initially false)

2.  Decision rule for round t:

    If t == 1:
        Play C  
        (We start by cooperating to try to meet the threshold.)

    Else  (t > 1):
        If punish_flag == true:
            // We are punishing all players this round
            Play D  
            punish_flag ← false  
            // After this single‐round punishment, clear the flag and next round we will try to cooperate again.
        Else if last_coop_count ≥ m:
            // Group succeeded last round ⇒ reward for cooperation
            Play C  
        Else:
            // Group failed last round ⇒ trigger punishment
            Play D  
            punish_flag ← true  
            // We defect now and set a one‐round punishment.

3.  After each round t finishes:
    •  Observe the total number of cooperators, call it observed_coop_count.  
    •  Update last_coop_count ← observed_coop_count.

4.  Edge‐case handling:
    – First round (t=1): always cooperate, as above.  
    – Last round (t=r): we apply exactly the same rule.  In particular, if the group succeeded in round r–1 we cooperate; if they failed, we defect to punish one more time.  This still preserves the cooperative mindset and can discourage free‐riding even in the final round.  
    – Multiple consecutive failures: the strategy punishes exactly one round per failure, then immediately “forgives” and returns to cooperative mode.  If failures persist, each failure again triggers exactly one punishment.

5.  Why it works:
    – If all players adopt this rule, then any single round failure to hit the threshold provokes a guaranteed one‐round group defection.  Rational co‐operators anticipate this punishment and thus have an incentive to maintain at least m cooperators each round.  
    – The one‐round punishment is short enough to be forgiving, preventing permanent collapse of cooperation, yet credible enough to discipline defectors.  
    – The strategy is fully symmetric, requires only observing how many cooperated, and never uses side‐channels or illicit communication.  

Pseudocode summary:

    initialize punish_flag ← false
    initialize last_coop_count ← undefined

    for t in 1..r:
        if t == 1:
            action ← C
        else if punish_flag:
            action ← D
            punish_flag ← false
        else if last_coop_count ≥ m:
            action ← C
        else:
            action ← D
            punish_flag ← true

        play action
        observe observed_coop_count
        last_coop_count ← observed_coop_count

End of strategy.
'''

description_COOPERATIVE_64 = '''
Below is a single‐strategy prescription—“Generous Threshold Tit-for-Tat (GTTFT)”—that tries to sustain cooperation (i.e. meet the m-threshold every round) but protects you from being a sucker when others defect en masse.  You can present this as pseudocode or plain English; implementation details (random draws, bookkeeping) can be filled in later.

1. State variables  
   • prev_success (Boolean): did the group reach the threshold in the last round?  
   • punish_round (Boolean): are we in a one‐round “punishment” following a failure?

2. Parameters you choose once:  
   • ε (epsilon), a small positive probability (e.g. 0.1) for “forgiveness” after failures.  

3. Initialization (before round 1)  
   prev_success ← true  
   punish_round ← false  

4. Action rule for each round t=1…r  

   if t == 1 then  
     play C  
     goto Observe  
   end if  

   if punish_round == true then  
     1. play D  
     2. punish_round ← false            # punishment lasts exactly one round  
     goto Observe  
   end if  

   # Not currently punishing:  
   if prev_success == true then  
     # Last round was a success → stick with cooperation  
     play C  
   else  
     # Last round failed → be generous but wary  
     with probability (1−ε): play D  
     with probability ε:   play C   # a small “test” to re−establish cooperation  
   end if  

   Observe:  
     • Count number of cooperators this round, call it k.  
     • prev_success ← (k ≥ m)  
     • if k < m and punish_round == false then punish_round ← true  

5. Last‐round tweak (optional)  
   In a finite horizon players often “defect in the last round,” but if you believe some opponents may still cooperate you can ignore backward induction and apply the same rule in round r.  
   If you do want to defect for sure in round r, simply override the above at t == r: play D.

6. Intuition and properties  
   • “Tit-for-Tat” at the group level: if the threshold was met, you reward everyone by cooperating next round.  
   • “Generous”: after a failure you punish by defecting for exactly one round, then give cooperation another small chance (ε) to recover.  
   • Protects you from repeated exploitation: if others never return to cooperating, you quickly lock into defection (except for infrequent ε‐probing).  
   • If a majority rekindles cooperation, you quickly shift back to full cooperation and help maintain the threshold each round.  

This strategy thus (i) starts cooperatively, (ii) rewards collective success with further cooperation, (iii) punishes collective failure to deter free‐riding, but (iv) remains forgiving so that a single breakdown does not destroy cooperation forever.
'''

description_AGGRESSIVE_33 = '''
Here is a fully‐specified “aggressive” strategy—call it the Pivotal Free‐Rider (PFR).  It never gives away value except exactly when your single contribution is needed to trigger the public‐goods bonus, and otherwise it free–rides or punishes cooperators.  You end each round with maximal private gain and minimize opponents’ surplus.

1.  Notation  
   •  t = current round, 1 ≤ t ≤ r  
   •  r = total rounds  
   •  m = cooperation threshold  
   •  C_t = total number of cooperators in round t (including you)  
   •  C⁻_t = number of cooperators other than you in round t  

2.  High‐Level Description  
   –  First round: defect, to signal non‐cooperativeness and gather information.  
   –  Middle rounds (2 ≤ t ≤ r−1):  
      •  If other players alone already meet the threshold (C⁻_{t−1} ≥ m), defect and free‐ride on their cooperation.  
      •  Else if exactly m−1 others cooperated last round (C⁻_{t−1} = m−1), cooperate this round—your only time cooperating—so that the group hits the threshold and earns k.  You “pivotal‐play.”  
      •  Otherwise (C⁻_{t−1} ≤ m−2), defect, since your lone cooperation can’t secure the bonus, so you preserve your endowment.  
   –  Last round (t = r): defect unconditionally (no future rounds to punish you).  

3.  Pseudocode  
```
Initialize:  // nothing to track beyond last round’s actions
for t in 1..r:
    observe C_prev = number of cooperators in round t−1
              C_minus_prev = C_prev minus your own action in t−1

    if t == 1:
        action[t] = D

    else if t == r:
        // Last‐round defection
        action[t] = D

    else:
        if C_minus_prev >= m:
            // Others already supplied the threshold—free‐ride
            action[t] = D
        else if C_minus_prev == m−1:
            // You are pivotal—contribute exactly once to earn k
            action[t] = C
        else:
            // Cannot meet threshold even if you cooperate—defect
            action[t] = D
```

4.  Handling Edge Cases  
   •  r = 2  ⇒  t=1 defect, t=2 defect ⇒ always defect (no room to be pivotal).  
   •  If opponents suddenly overshoot (C⁻_{t−1} > m), you still defect—never reward excess cooperation.  
   •  If ties or simultaneous moves create ambiguity about “pivotal” status, break ties conservatively: only cooperate when you know with certainty (C⁻_{t−1} == m−1) that you alone shift the outcome.  

5.  Why This Is Aggressive  
   –  You never establish genuine cooperation.  You only “pay in” at the razor’s edge, once per pivotal opportunity.  
   –  You punish over‐cooperators by refusing to support them in later rounds, ensuring they shoulder the full cost whenever they altruistically overshoot.  
   –  You defect in the final round, extracting any value without fear of retaliation.  
   –  You maximize your own total payoff (by never contributing except when mathematically necessary) while minimizing opponents’ surplus from teamwork.
'''

description_AGGRESSIVE_34 = '''
Below is an “Aggressive Opportunist” strategy.  It almost always defects, only cooperating in the one pivotal case where your single contribution will tip the group from failure to success (so you get k rather than 1).  In every other situation you defect—free‐riding on others when they already succeed, punishing them when they don’t, and never “waste” a contribution for no gain.  

—Decision rules—  
Let t = current round (1 ≤ t ≤ r).  
Let prev_coop = number of cooperators in round t–1 (if t=1, define prev_coop=0).  

1. If t=1 (no history):  
     play D  
2. Else if t=r (last round):  
     play D  
3. Else (1<t<r):  
   a. If prev_coop == m–1 then  
        play C   # your one contribution pushes the group to ≥m; you earn (0 + k) > 1  
   b. Otherwise  
        play D   # either they already hit ≥m (so you free-ride) or they failed by more than one (so your C is wasted)  

—Why this is aggressive—  
• You never “give away” a point blindly.  
• You free-ride whenever the threshold was met anyway.  
• You only cooperate when it directly increases your own payoff from 1 to k.  
• You refuse to be the sucker in the last round (no end-game cooperation).  

—Pseudocode—  
```
initialize prev_coop = 0

for t in 1..r:
    if t == 1:
        action[t] = D
    else if t == r:
        action[t] = D
    else:
        if prev_coop == m - 1:
            action[t] = C
        else:
            action[t] = D

    # after actions are played, observe and store for next round
    prev_coop = count_cooperators_this_round()
end for
```

—Edge cases—  
• First round: no history ⇒ defect.  
• Rounds where prev_coop < m–1: defect (your C wouldn’t save the pot, so you’d lose 1).  
• Rounds where prev_coop ≥ m: defect (the pot pays out anyway; you free-ride).  
• Last round: always defect (no future to influence).  

This strategy maximizes your per‐round payoff by only ever paying the cooperation cost when it buys you the extra k reward, otherwise ruthlessly defecting.
'''

description_AGGRESSIVE_35 = '''
Below is a fully specified “Aggressive Opportunistic‐Pivot” strategy.  It never wastes a contribution except when you’re literally the pivotal cooperator (i.e. exactly m–1 others are cooperating); otherwise you defect and thus both exploit cooperators and frustrate groups that try to meet the threshold.

1.  State variables and notation  
   • r, n, m, k as given.  
   • At the end of each round t you observe how many players cooperated: CoopCount[t] ∈ {0,…,n}.  
   • In round t you must choose a_t ∈ {C,D}.  

2.  High-level description  
   – Default: Defect.  
   – Exception: If you predict exactly (m–1) of the *other* players will cooperate this round, you cooperate (so that the threshold is met and you earn k rather than just 1).  
   – Otherwise you defect, thereby free-riding when possible (threshold already met without you) or sabotaging the project when you’re not needed (denying the bonus to all).  

3.  Prediction rule  
   Since moves are simultaneous, we need a simple prediction of how many others will play C in the current round.  We use last‐round behavior as our forecast (a crude but effective “assume static” predictor):  
     PredictedOthersC = CoopCount[t–1]  
   (t=1: define CoopCount[0] = 0, so PredictedOthersC = 0 in round 1.)  

4.  Aggressive-pivot decision rule for round t = 1…r  
   if PredictedOthersC == m–1  
       play a_t = C   // you are pivotal: your cooperation turns a failed round into a success, yielding payoff k>1  
   else  
       play a_t = D   // either you’re not needed (others will supply ≥m) OR your help won’t reach the threshold; in both cases defect  

5.  Edge cases  
   • Round 1: no history ⇒ PredictedOthersC=0 ⇒ 0==(m–1)? only if m=1 (disallowed).  So you defect.  
   • Last round (t=r): same rule – there’s no future to protect, so still pivot only if necessary.  
   • If others suddenly coordinate so that PredictedOthersC ≥ m, you defect and free-ride (you get 1+k instead of k).  
   • If PredictedOthersC ≤ m–2 you defect and sabotage any chance of success.  

6.  Pseudocode  

   initialize CoopCount[0] = 0  
   for t in 1…r:  
     PredictedOthersC = CoopCount[t–1]  
     if PredictedOthersC == m–1:  
       a_t = C  
     else:  
       a_t = D  
     end  
     observe actual CoopCount[t]  // after all moves are revealed  
   end  

7.  Why this is aggressive  
   – You never “waste” a 1‐unit endowment unless it’s the only way to trigger the bonus for yourself.  
   – You punish others by defecting whenever their cooperation would succeed without you (they pay cost but you reap extra 1 unit).  
   – You sabotage projects that cannot succeed without you by also defecting—keeping the group below threshold as often as possible.  
   – You never “reward” cooperation except when it directly boosts your own payoff above 1.  

This strategy maximizes your unilateral gain, exploits any cooperators, and discourages opponents from ever forming stable cooperating blocs (since they will frequently see you defecting, even when they try to meet the threshold).
'''

description_AGGRESSIVE_36 = '''
Below is a fully “aggressive” tournament‐ready strategy for the repeated collective‐risk dilemma.  In essence, it tries to free‐ride every round, only stepping in on the very last round if (and only if) your single contribution is pivotal to avert group failure.

1.  Overview name  
    “Last‐Chance Free‐Rider”

2.  Intuition  
    •  Always defect (keep your endowment) to maximize private gain.  
    •  Postpone any cooperation until the very last round.  
    •  In the last round, cooperate only if, without you, the group would fall below the threshold m.  

3.  Notation  
    n    number of players  
    r    total rounds  
    m    cooperators needed per round  
    k    group reward factor  
    t    current round (1…r)  
    history[t′] = number of cooperators observed in round t′ (including you)  
    others_coop_estimate[t] = best estimate of how many others (excluding you) will cooperate in round t  

4.  Decision rule (per round t)  
  a) If t < r (not last round)  
     – Action ← D (Defect) unconditionally.  
     Rationale: maximize immediate payoff; you’ll only bail out at the final moment.  

  b) If t == r (last round)  
     1. Compute estimate of others’ cooperators this round.  A simple proxy is to take last round’s others:  
          others_coop_estimate = history[t–1] – (you cooperated in t–1 ? 1 : 0)  
     2. If others_coop_estimate ≥ m  
          • The group already meets threshold without you ⇒ Action ← D  
        Else if others_coop_estimate == m – 1  
          • Your single C would push the group to m ⇒ Action ← C  
        Else  
          • Even if you C, group fails ⇒ Action ← D (avoid wasting your endowment on a doomed round)  

5.  Edge cases  
  • First round (t=1): falls under “t<r,” so you Defect.  
  • If m=1: threshold is met by any 1 cooperator; you still wait until last round and then check if any other cooperated before; in practice you’ll D until last, then if no one else mustered C you C to grab k.  
  • If history incomplete (e.g. t–1=0), assume others_coop_estimate=0.  

6.  Pseudocode  

    initialize history[1…r] to 0  
    for t in 1…r:  
        if t < r:  
            action[t] = D  
        else:  # t == r  
            # estimate others’ current‐round cooperation by last round’s data  
            last_round_coop = history[t–1]  
            you_were_coop   = (action[t–1] == C ? 1 : 0)  
            others_coop_est = last_round_coop – you_were_coop  

            if others_coop_est >= m:  
                action[t] = D  
            else if others_coop_est == m – 1:  
                action[t] = C  
            else:  
                action[t] = D  

        # play action[t], observe total cooperators this round  
        history[t] = observed_cooperators_this_round  

7.  Why it’s aggressive  
  – You never punish or ‘forgive.’  You simply exploit cooperative rounds for maximal private gain.  
  – You cooperate only when you can single‐handedly (and last‐moment) avert collective failure.  
  – You refuse to invest in any round where your contribution isn’t strictly pivotal.

This strategy works for any parameters (n, r, m, k) and each round is decided in constant time. It maximizes exploitation of others’ goodwill while guaranteeing you avoid the “risk” only if—and exactly when—you’re indispensable.
'''

description_AGGRESSIVE_37 = '''
Here is an “alpha free‐rider” strategy—aggressive, self-centered, yet minimal-cooperative enough to snatch the group reward when you’re pivotal.  You never voluntarily build the public good beyond the bare minimum, you free-ride whenever you safely can, and you only pitch in when without you the group would fail and you’d lose the bonus.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

1. Informal Description  
   • First round (t = 1): defect (D).  
   • In every subsequent round t:  
     – Count how many others cooperated last round (exclude yourself). Call that others_C.  
     – If others_C ≥ m: the group could have met the threshold without you – defect (free-ride).  
     – If others_C = m–1: you are pivotal – cooperate (C) just enough to hit the threshold.  
     – If others_C < m–1: even with you the threshold wouldn’t have been reached – defect (C would be wasted).  
   • Apply these same rules on the last round—there’s no end-game retreat.

   Why it’s aggressive:  
   – You never pre-commit to cooperation.  
   – You never subsidize other players’ coordination costs except at the last possible moment when your contribution is the only thing that pays off for you.  
   – You immediately exploit any coalition strong enough to survive without you.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

2. Pseudocode  

```
Inputs:
  n  – number of players (≥2)
  r  – number of rounds (>1)
  m  – minimum cooperators needed (1 < m < n)
  k  – reward factor (k > 1)

State:
  last_coop_count  – integer, number of players (including you) who cooperated last round
                     (initialize to 0 for round 1)

For round t in 1..r:
  If t == 1:
    action ← D
  Else:
    others_C = last_coop_count
               – (your action last round was C ? 1 : 0)

    If others_C ≥ m:
      action ← D      // safe to free-ride
    Else if others_C == m–1:
      action ← C      // you’re pivotal—grab the bonus
    Else:
      action ← D      // wasted effort to cooperate

  Play(action)

  // After all players act, observe total cooperators this round:
  last_coop_count ← count_of_C_from_all_players
EndFor
```

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

3. Edge‐Case Handling  
 • First round: No history ⇒ defect.  
 • Last round: No future deterrent ⇒ same rule (you’ll still cooperate only if others = m–1 because only then does cooperation yield 1–1+ k > 1).  
 • If others_C < m–1, you know even your C can’t save the bonus ⇒ always defect.  
 • If others_C ≥ m, you know the bonus arrives without you ⇒ always defect.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

This strategy guarantees you capture every marginal surplus you can, never pay more than necessary, and aggressively free-ride any coalition that doesn’t absolutely need you.
'''

description_AGGRESSIVE_38 = '''
Below is an “aggressive” free‐rider strategy we’ll call Threshold-Exploiter.  It never pays a contribution unless doing so is strictly in your self‐interest (i.e. you alone can tip the scale from failure to success and k>1).  In all other cases you defect, thereby exploiting or punishing cooperators.

1.  Definitions and data structures  
    •  r = total rounds, t ∈ {1…r}  
    •  m = cooperation threshold (>1)  
    •  k = payoff bonus if threshold met (>1)  
    •  A_t^−i = number of cooperators among the other n–1 players in round t  
    •  a_t^i ∈ {C,D} = your action in round t  

2.  High-level decision rule for round t  
    2.1  If t=1:  
         •  No history yet → defect (a₁^i = D).  
    2.2  If t>1:  
         •  Compute A_{t}^−i_pred = A_{t−1}^−i (assume others repeat last round).  
         •  Three cases:  
            a) A_{t}^−i_pred ≥ m : threshold would succeed even if you defect → defect (get 1 + k instead of k).  
            b) A_{t}^−i_pred ≤ m−2 : threshold fails even if you cooperate → defect (get 1 > 0).  
            c) A_{t}^−i_pred = m−1 : you are pivotal.  
                  –  Cooperating yields payoff k (since (m−1)+1 ≥ m), defecting yields 1 (threshold would fail).  
                  –  If k>1, cooperate (a_t^i = C), otherwise defect.  
    2.3  Last round (t=r):  
         •  Follow the exact same rule as in 2.2.  There is no future to punish you, but because cooperation is only ever in your narrow self-interest you treat round r identically.

3.  Pseudocode  
    initialize history ← empty list  
    for t in 1…r do  
      if t == 1 then  
        a₁^i ← D  
      else  
        let total_coop_prev ← sum over j≠i of {1 if player j cooperated in round t−1}  
        let p ← total_coop_prev  
        if p ≥ m then  
          a_t^i ← D             # threshold safe without you  
        else if p ≤ m−2 then  
          a_t^i ← D             # even with you it fails  
        else # p == m−1  
          if k > 1 then  
            a_t^i ← C           # you tip to success  
          else  
            a_t^i ← D           # bonus not worth the cost  
      end if  
      play a_t^i  
      observe others’ actions in round t → update history  
    end for

4.  Why is this aggressive?  
    •  You never “waste” a contribution unless it alone turns a failure into success—every other round you defect.  
    •  You always free-ride on any cooperative effort already ≥ m.  
    •  You punish any round that would have failed even with your help by refusing to cooperate, solidifying failure (and denying goodwill).  
    •  You do not attempt to build reciprocity or foster cooperation beyond what immediately boosts your own payoff.

5.  Edge-case handling  
    •  If k ≤ 1 then “pivotal cooperations” never pay off; the rule in case (c) automatically reduces to defect.  
    •  First round has no data → defect.  
    •  Last round is treated exactly like any other (no softening).  

This strategy is fully specified, requires only tracking the count of cooperators among your opponents in the previous round, and in every round chooses the action that maximizes your immediate payoff under the assumption that opponents repeat their last move.
'''

description_AGGRESSIVE_39 = '''
Below is a self-contained, aggressive “threshold-opportunist” strategy.  In plain English it defaults to defecting, and only ever cooperates when your single contribution is exactly what’s needed to tip the group over the m-threshold—thus you never waste a cooperative move, you free-ride whenever you can, and you only pay the cost when doing so yields you a net gain (k > 1).

1. Definitions / bookkeeping  
   • Let r = total rounds, indexed t = 1…r.  
   • After each round t we observe TotalCoop[t], the number of players (including you) who chose C in round t.  
   • Let OtherCoop[t] = TotalCoop[t] minus your action in t (0 or 1).  

2. Decision rule  
   For each round t do:  
     if t == 1 then  
       play D  // no history yet, defect to test/free-ride  
     else  
       if OtherCoop[t–1] == m–1 then  
         play C  // your sole cooperation will push total to m ⇒ you earn (0 + k) > (1 + 0)  
       else  
         play D  // either they already succeeded without you, or even with you they’d still fail  

3. Edge cases  
   • First round (t=1): defect unconditionally.  
   • Last round (t=r): apply the same rule—only cooperate if OtherCoop[r–1] == m–1.  
   • No special “end-game” shift; you remain aggressive through round r.  

4. Why it’s aggressive  
   • You never cooperate unless it strictly increases your own payoff.  
   • If the group succeeded without you (OtherCoop ≥ m), you defect to grab the extra private unit.  
   • If the group was going to fail even with you (OtherCoop ≤ m–2), you defect and impose failure on everyone.  
   • You exploit others’ willingness to cooperate but never reciprocate unless it’s in your narrow self-interest.  

5. Pseudocode  

```
Inputs: n, r, m, k
Initialize: last_TotalCoop = 0

for t in 1..r:
  if t == 1:
    myAction[t] = D
  else:
    OtherCoop = last_TotalCoop - (myAction[t-1] == C ? 1 : 0)
    if OtherCoop == m - 1:
      myAction[t] = C
    else:
      myAction[t] = D

  // Play myAction[t], then observe total cooperators this round:
  last_TotalCoop = observe_total_cooperators()
end for
```

With this rule you (a) maximize each round’s private return, (b) free-ride whenever possible, and (c) never “waste” a cooperation except at the narrow tipping point where it pays you to do so.
'''

description_AGGRESSIVE_40 = '''
Below is a self-contained, “aggressive” threshold-public-goods strategy.  It never wastes contributions, it “free-rides” whenever it can, but still steps in exactly when its single vote is pivotal.  It also defects in the last round (no future to punish), and tests only once at the start.

1.  Overview  
   •  You only ever cooperate if and only if your single cooperation turns a losing round into a winning one.  
   •  In the very first round you defect (test the field).  
   •  In the last round you always defect (there is no future to leverage).  
   •  Otherwise you look at how many cooperators there were in the previous round and cooperate only if exactly m–1 others cooperated then.  

2.  Ingredient definitions  
   let n = number of players  
       r = total rounds  
       m = cooperators needed for reward  
       k = payoff bonus if ≥m cooperators  
   each round t = 1…r you observe the profile of actions from round t–1 (empty when t=1).

3.  Decision rule (pseudocode)  

  function decideAction(t, prevActions):  
    # t            = current round index (1…r)  
    # prevActions  = list of all players’ actions in round t–1, e.g. ['C','D','C',…]  
    if t == 1:  
      return D    # always defect in round 1 (probe)  
    if t == r:  
      return D    # always defect in last round (no future leverage)  
    # otherwise look at last round’s cooperators  
    last_C = count of ‘C’ in prevActions  
    if last_C == m - 1:  
      # our single C will tip the group over the threshold  
      return C  
    else:  
      # either threshold already met (we exploit) or hopeless (we save our cost)  
      return D  

4.  Explanation of “aggressive” features  
   •  Minimum cooperation: you only pay the cost when you are exactly pivotal.  
   •  Maximum exploitation: whenever ≥m others already cooperated you defect and pocket the reward.  
   •  No end-game generosity: in round r you never cooperate (defection dominates).  
   •  No prolonged trust: first round you defect to see other players’ patterns rather than lead with C.  

5.  Edge-case handling  
   •  If r=2:  
     – Round 1: t=1 ⇒ defect  
     – Round 2: t=r ⇒ defect  
     You never cooperate, foregoing k but also never incurring cost 1.  
   •  If m–1 > n–1 (impossible by spec) you would never enter the “==m–1” branch → always defect.  
   •  If opponents’ behavior shifts dramatically, you still only look one round back; you neither build long-run trust nor forgive: truly aggressive.

This strategy maximizes your own payoff by (a) free-riding on others wherever possible, (b) barely cooperating only to trigger the group payout when you must, and (c) refusing any last-round cooperation.
'''

description_AGGRESSIVE_41 = '''
Below is an “aggressive‐pivot” strategy.  It never “wastes” a cooperation except when you alone can tip the round over the threshold, and it always defects otherwise (including round 1 and the final round).  In effect you only cooperate when you are exactly pivotal; every other time you defect and reap the larger private payoff.  

---------------------------------------------------------------------------  
1. Data you keep each round t (after you see everyone’s actions in t–1):  
   • coopOther[t–1] = number of other players (i ≠ you) who played C in round t–1.  

2. Decision rule for round t:  
   if t == 1 or t == r:  
      play D  
   else:  
      let x = coopOther[t–1]  
      if x == m–1:  
         play C    // you are exactly the mth cooperator  
      else:  
         play D    // either threshold is already reached by others, or you can’t reach it  

3. Rationale / payoff check (per round):  
   • If others ≥ m, you defect ⇒ payoff = 1 + k (best)  
   • If others = m–1, you cooperate ⇒ payoff = 0 + k = k > 1 (next best)  
   • Otherwise, cooperation can’t save the group (others ≤ m–2 ⇒ even with you they total ≤ m–1) ⇒ you defect ⇒ payoff = 1 (best you can do)  

4. Edge cases handled:  
   – First round (t = 1): no history ⇒ defect to avoid “wasted” coop.  
   – Last round (t = r): classic end‐game defect.  
   – Mistaken forecasts: we simply trust last round’s coopOther as our best estimate.  

Pseudocode  

```
initialize coopOther[0] = 0   // dummy

for t in 1..r:
    if t == 1 or t == r:
        action[t] = D
    else:
        x = coopOther[t-1]
        if x == m-1:
            action[t] = C
        else:
            action[t] = D

    // After all actions observed, record for next round:
    // coopOther[t] = number of C’s by other players in round t
```

This strategy is maximally aggressive: you only sacrifice your private endowment when doing so is strictly necessary to claim the public reward, and you defect in every other circumstance—even at the risk that the group fails and loses k.
'''

description_AGGRESSIVE_42 = '''
Below is an “aggressive threshold‐exploiter” strategy.  It never cooperates unless its single cooperation is strictly necessary to save the public‐good reward, and otherwise free‐rides or punishes over‐eager cooperators.  

1.  Data you observe and store  
   •  t: current round (1..r)  
   •  history of all players’ actions in past rounds  
   (in particular, in round t–1 you know how many cooperated)  

2.  High-level description  
   – In the very first round you defect (no history, so no leverage).  
   – In any round where your defection would drop the total cooperators below the threshold m, you “hold your nose” and cooperate (you are pivotal).  
   – In all other rounds you defect:  
     •  If the threshold was already met without you last round, you free‐ride again.  
     •  If even with your cooperation the threshold cannot be met, you refuse to waste your endowment on a doomed cause.  
   – In the last two rounds (t = r–1 or r), you always defect—there is no future to enforce or extract punishment, so you’d rather grab the 1 than spend the cost.  

3.  Pseudocode  

   initialize nothing special  
   for each round t = 1 to r do  
     if t == 1 or t ≥ r–1 then  
       action := D  
     else  
       let C_total_prev = number of cooperators in round (t–1)  
       let I_prev = 1 if you cooperated in (t–1), else 0  
       let C_others = C_total_prev – I_prev  
       if C_others == m–1 then  
         action := C    // you are pivotal—threshold would fail without you  
       else  
         action := D    // either free‐ride or refuse to waste on a loss  
     end-if  
     play(action)  
   end-for  

4.  Explanation of aggressiveness  
   •  “Only if I alone save the pool do I pay the cost C=1.”  Otherwise I always defect.  
   •  This punishes any excess cooperators: if they overshoot the threshold, they pay 1 to get k but I get k+1.  
   •  By refusing to cooperate in the final two rounds, I inflict losses on cooperators when there is no threat of future punishment.  

This rule is fully deterministic, requires only one‐round memory, and aggressively maximizes your private payoff by cooperating only at the knife‐edge.
'''

description_AGGRESSIVE_43 = '''
Below is a fully‐specified, “aggressive” threshold–public–goods strategy.  Its core idea is to free‐ride whenever possible, only “minimally” contributing exactly when you are pivotal (i.e. the m’th cooperator) in rounds 1…r−1, and to defect outright in the last round.

1.  Definitions and notation  
   •  n = total players  
   •  m = threshold of cooperators needed (1 < m < n)  
   •  r = total rounds (>1)  
   •  t = current round, t=1…r  
   •  C = cooperate (cost 1)  
   •  D = defect (no cost)  
   •  hist_others(t−1) = number of cooperators among the other n−1 players in the previous round (t−1).  
     –  At t=1, hist_others is undefined.  

2.  Decision rules  
   For each round t:

   if t == r:  
      action ← D  
      // Aggressive last‐round free‐riding: never contribute in final round

   else if t == 1:  
      action ← D  
      // No history yet – start by defecting

   else:  // 2 ≤ t ≤ r−1  
      if hist_others(t−1) == m−1:  
          action ← C  
          // You are “pivotal”: your single contribution will meet threshold  
      else:  
          action ← D  
          // Otherwise, free‐ride

3.  History update (at the end of each round t)  
   Observe total_coops(t), the total number of cooperators this round (including you).  
   Let your_c = 1 if you played C, else 0.  
   hist_others(t) ← total_coops(t) − your_c  

4.  Rationale and aggressiveness  
   – You never contribute unless your single C is the crucial m’th coin needed to trigger the bonus.  
   – By defecting whenever hist_others ≠ m−1, you let others bear all costs.  
   – In the last round, you ditch even the pivotal play: pure defection to capture the maximal one‐shot gain.  
   – First‐round defection avoids seeding any cooperation bandwagon on you.  

5.  Pseudocode  

   initialize hist_others ← undefined  
   for t in 1…r do  
      if t == r then  
          play D  
      else if t == 1 then  
          play D  
      else  
          if hist_others == m−1 then  
              play C  
          else  
              play D  
      // After all moves are revealed:  
      observe total_coops  
      your_c ← (1 if you played C else 0)  
      hist_others ← total_coops − your_c  
   end for

This strategy is maximally “aggressive” in the sense that it never gives away a free bonus unless absolutely forced (being the pivotal m’th contributor), and it “cashes out” by defecting in the very last round.
'''

description_AGGRESSIVE_44 = '''
Below is an “Aggressive Opportunistic Threshold” strategy.  It never tries to build cooperation for its own sake, but jumps in only when it can secure the collective reward for everyone—then immediately free‐rides or punishes.  

1.  Definitions and memory  
   •  Let r be the total number of rounds.  
   •  Let m be the cooperation threshold.  
   •  At the end of each round t – 1 we observe how many cooperated, C_count[t – 1].  
   •  We also maintain a permanent flag PunishAll that flips on if ever all n players cooperated together.  

2.  Edge cases  
   –  In round 1 we have no history: we defect.  
   –  In the final round t = r we always defect (no future to exploit cooperation).  
   –  If at the end of any round we saw C_count[t] == n (everyone cooperated), set PunishAll = TRUE—and from then on never cooperate.  

3.  Main decision rule (for 1 < t < r)  
   if PunishAll == TRUE:  
       action ← D  
   else if C_count[t – 1] == m – 1:  
       // by cooperating we push the group over the threshold  
       action ← C  
   else:  
       // either threshold already met by others (≥ m), or cannot be met even with us  
       action ← D  

4.  Intuition of aggressiveness  
   –  We only cooperate when we can *just* tip the balance to collect k for everybody, then begin defecting immediately (free‐ride).  
   –  We never attempt to reward or build trust.  In fact, if the group ever showed “over‐trust” by all cooperating, we permanently punish.  
   –  We defect on the first round (to test the waters) and in the last round (no future leverage).  

Pseudocode  
==========  
```  
Initialize PunishAll ← FALSE

for t in 1…r:
  if t == 1:
    play D
    observe C_count[1]
    if C_count[1] == n: PunishAll ← TRUE

  else if t == r:
    play D
    // end of game

  else:
    if PunishAll:
      play D
    else if C_count[t-1] == m - 1:
      play C
    else:
      play D

    observe C_count[t]
    if C_count[t] == n:
      PunishAll ← TRUE
```

Explanation of behavior  
– Rounds 1 and r: guaranteed defection (no leverage or future to build on).  
– Rounds 2 through r–1:  
   • If exactly m–1 others cooperated last round, we cooperate so that total ≥ m and everybody (including us) gets k.  
   • Otherwise we defect—either we cannot help the group reach m, or they already reached it without us (so we free‐ride).  
   • If at any point the entire group cooperates, we flip into permanent punishment mode and never cooperate again.  

This “Aggressive Opportunistic Threshold” maximizes your payoff by:  
1. Never shouldering the project cost unless it’s the single decisive move.  
2. Immediately punishing any signs of full‐group goodwill.  
3. Exploiting every available free‐ride opportunity.
'''

description_AGGRESSIVE_45 = '''
Below is a self­-contained, aggressive, opportunistic strategy for the repeated collective-risk dilemma.  Its guiding principle is: “Defect by default; only cooperate when my single cooperation is just enough to tip the group over the success threshold—and always exploit when others carry the load.”

1. State variables  
   • n, m, r, k as given.  
   • history[t][i] ∈ {C, D}: the action of player i in round t.  
   • For convenience we’ll keep track each round t of  
      – total_coops[t] = number of Cooperate actions in round t (including ours).  
      – total_coops_excl_us[t] = total_coops[t] minus (1 if we cooperated that round, 0 otherwise).  

2. Core idea  
   – Rounds in which our one extra C doesn’t change success vs. failure (i.e. total_coops_excl_us ≥ m or ≤ m–2): defect.  
   – Rounds in which total_coops_excl_us == m–1 (so our single C flips failure into success): cooperate.  
   – Always defect in round 1 (no information) and in round r (last-round defection, no future punishment).  

3. Pseudocode  

Let our index be player “0.”  
Initialize history empty.  
For t = 1 to r:  
   if t == 1 or t == r:  
      action_t = D  
   else:  
      // Observe last round’s behavior of opponents  
      let prev = t–1  
      let coop_prev_excl_us = number of C’s in history[prev][1..n–1]  
         // i.e. count of cooperators among the other n–1 players last round  
      if coop_prev_excl_us == m–1:  
         // Our single C secures the k‐bonus for everyone – we jump in  
         action_t = C  
      else:  
         // Either (i) they already got the bonus (coop_prev_excl_us ≥ m), so we free-ride  
         // or (ii) they would still fail (coop_prev_excl_us ≤ m–2), so no point to pay cost  
         action_t = D  
   end if  
   Play action_t; record it in history[t][0].  
   Observe opponents’ actions; update total_coops and total_coops_excl_us.  
end for  

4. Why “aggressive”?  
– We never waste a cooperation when it cannot change the outcome.  
– We exploit others’ cooperations by defecting whenever the threshold is already met without us.  
– We refuse to unilaterally bail out a failing group unless that single act flips the reward in our favor.  
– We refuse any goodwill on round 1 and round r (no reciprocity possible).  

5. Edge cases handled  
– First round (t = 1): defect unconditionally.  
– Last round (t = r): defect unconditionally (standard backward-induction).  
– If in some round even our C cannot reach m (coop_prev_excl_us ≤ m–2): we defect.  
– If without us they already clear m (coop_prev_excl_us ≥ m): we defect and free-ride.  
– Only when coop_prev_excl_us == m–1 do we cooperate.  

This strategy guarantees we never pay cost 1 for a cooperation that doesn’t increase our own payoff, and we only cooperate when doing so raises our payoff from 1 to k.
'''

description_AGGRESSIVE_46 = '''
Below is a fully specified “aggressive” threshold‐free‐rider strategy.  It (1) almost always defects, only contributing when you’re pivotal to secure the public‐good reward for yourself, (2) punishes any “premature” cooperation by never rewarding it, and (3) never cooperates on the first or last round (so there is no “end‐game” illusion of trust).  

1.  Variables tracked  
   • coop_count_prev[j]  = number of times player j cooperated in previous rounds  
   • round t ∈ {1,…,r}  

2.  High‐level description  
   – First and last round: always defect (no room for building or sustaining trust).  
   – Intermediate rounds:  
     • Reconstruct or predict the number of other cooperators this round (based on last‐round behavior).  
     • If you would be pivotal (i.e. without you, expected cooperators = m–1), then cooperate to get k rather than 1.  
     • Otherwise defect.  

3.  Why this is aggressive  
   – You never risk your own endowment for altruistic “extra” contributions.  
   – You never reward cooperative patterns with more cooperation—only enough to secure your own upside, and otherwise you exploit or punish cooperators by defecting.  
   – You start and end with pure defection, crushing any chance of reputation‐building.  

4.  Pseudocode  

```
Parameters:
  n, r, m, k   // n players, r rounds, threshold m, reward k>1

State:
  coop_count_prev[1..n] ← {0,0,…,0}
  // we index ourselves as i; others as j≠i

For each round t = 1 to r do:
  
  // 1. First‐ or last‐round rule: always defect
  If t == 1 or t == r then
    action_i ← D
    goto END_OF_ROUND
  EndIf

  // 2. Predict other cooperators this round
  //    We assume each other j will repeat last‐round move:
  predicted_C_others ← 0
  For each j ≠ i do
    If coop_count_prev[j] ≥ (t–1)/2  // they cooperated more often than not so far
      predicted_move_j ← C
    Else
      predicted_move_j ← D
    EndIf
    If predicted_move_j == C then
      predicted_C_others ← predicted_C_others + 1
    EndIf
  EndFor

  // 3. Pivotal‐only cooperation:
  //    If without you they fall exactly one short of threshold,
  //    it pays you to cooperate (0 + k > 1 + 0).
  If predicted_C_others == m–1 then
    action_i ← C
  Else
    action_i ← D
  EndIf

END_OF_ROUND:

  // 4. After moves are revealed, update history
  Observe actual moves of all players; let actual_move[j] ∈ {C,D}
  For j = 1 to n do
    If actual_move[j] == C then
      coop_count_prev[j] ← coop_count_prev[j] + 1
    EndIf
  EndFor

  // Payoffs are calculated externally per specification
EndFor
```

5.  Edge‐case summary  
  • Round 1 and round r: pure defection.  
  • Rounds 2…r–1: cooperate only if your single contribution flips the outcome from no‐reward to reward (i.e. others = m−1); otherwise defect.  
  • No forgiveness, no retreats—once a first‐ or last‐round defector, always a defector in those rounds.  

This strategy is “aggressive” because it:  
– Exploits any baseline cooperation by free‐riding whenever you are not strictly needed.  
– Punishes attempts at building trust by refusing to cooperate on the first and last rounds.  
– Never contributes “extra” beyond your own narrow self‐interest.
'''

description_AGGRESSIVE_47 = '''
Below is a simple but brutally aggressive “free‐rider” strategy.  It never pays the cost of cooperation, it never misses an opportunity to break the threshold for others, and it never “trusts” anyone—even in the last round.

1.  Key idea  
    - In every round, Defect strictly dominates Cooperate:  
      • If threshold ≥ m is reached without you, you get (1 + k) by defecting vs. (0 + k) by cooperating.  
      • If threshold < m without you, you get 1 by defecting vs. 0 by cooperating.  
    - Therefore you should play D in every possible information set.

2.  Decision rule (pseudocode)

    function decide_action(round t, history H):  
        return D

3.  Edge cases  
    - First round t = 1: no history → play D.  
    - Intermediate rounds 1 < t < r: regardless of how many cooperators you saw, play D.  
    - Last round t = r: play D (endgame defection).

4.  Rationale (aggressive stance)  
    - You never incur the cost of cooperation.  
    - You break any nascent coalition trying to reach the threshold by withholding your contribution.  
    - You maximize your per‐round payoff unilaterally, and you never allow “nice” players to gain on you.  

That’s it—“Always Defect.” This unsentimental rule is the strongest possible aggressive stance in the Collective Risk Dilemma.
'''

description_AGGRESSIVE_48 = '''
Below is a self‐contained “aggressive” threshold-public-good strategy.  It (1) never helps more than strictly needed, (2) free-rides whenever possible, (3) punishes the group if they ever succeed without needing you, and (4) defects in the first and last round.

============================================  
Strategy name: “Rescue-and-Grim”  
Parameters known to all: n, r, m, k  
Internal state:  
• Punished (boolean), initially false  
• OCC_prev = number of other players who cooperated in the previous round (initially undefined)  
• C_prev = whether you cooperated in the previous round (initially false)  

1. Round 1 (t=1):  
   – Action: Defect (D).  
   – After play, record OCC_prev ← # of other cooperators in round 1, C_prev ← false.

2. For each round t = 2,3,…,r:  
   If Punished == true OR t == r then  
     • Action: Defect.  
   Else  
     • If OCC_prev == m–1 then  
         – Action: Cooperate (C)   # your one vote rescues the public good  
       Else  
         – Action: Defect (D)      # either they already had a buffer or rescue is impossible  
   • After play, observe OCC_curr = # of other players who played C this round; set  
       OCC_prev ← OCC_curr  
       C_prev ← (you played C this round)  
   • Punishment trigger:  
       If C_prev == true AND OCC_prev ≥ m then  
         Punished ← true  
         # They could have met the threshold without you—now you never cooperate  

That’s it.  In words:  
– First and last rounds you defect unconditionally.  
– In all intermediate rounds you only cooperate if exactly m–1 others cooperated last round, i.e. your contribution is strictly pivotal.  
– Otherwise you defect (free-ride on buffer or abandon hopeless efforts).  
– If ever you find that in the previous round others had at least m cooperators (so they didn’t need you) while you also cooperated, you switch into grim mode and defect forever.  

This maximizes your private gains (you only pay the cost of cooperation exactly when it is needed to secure the bonus) and punishes groups that succeed without you, while fully exploiting any surplus‐buffer rounds.
'''

description_AGGRESSIVE_49 = '''
Below is a self–contained, “aggressive” threshold‐public‐goods strategy.  It exploits others whenever it can and only “steps in” to cooperate if the group just barely failed and needs exactly one more contribution to hit the threshold.  In the last round it always defects.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Name: Aggressive Threshold Free Rider (ATFR)  

Parameters you know:  
• n ≥ 2 players  
• r rounds (>1)  
• m cooperators needed each round  
• k>1 reward upon success  

Notation:  
• t = 1,…,r round index  
• a_i(t) ∈ {C,D} your action at round t  
• coop_others(t) = number of players j≠i who played C in round t  
• succ(t) = 1 if coop_others(t)+[a_i(t)=C] ≥ m, else 0  

Total‐game objective: maximize your ∑ π_i,t.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

1. Decision rules  

For each round t do:  
  if t = 1:  
    play D  
  
  else if t = r:  
    // End‐game defect  
    play D  

  else (2 ≤ t ≤ r–1):  
    Look at the history entry for round t–1:  
      let c = coop_others(t–1)  
      let s = succ(t–1)   // whether threshold succeeded last round  

    Rule:  
      • If in the previous round the group succeeded without you (i.e. c ≥ m):  
          defect (D).  
        – You free‐ride on their efforts forever once they can hit m without you.  

      • Else if the previous round failed (s = 0) and the others were “one short” (c = m–1):  
          cooperate (C).  
        – You’re the pivotal contributor; by cooperating you get 0–cost + k reward = k > 1.  

      • Otherwise (every other case):  
          defect (D).  
        – If they were far from m or if you already helped, you exploit or do nothing.  

2. Pseudocode  

Below is a compact version you can slot into any simulator.  

```
function ATFR_Decision(t, history):
    if t == 1:
        return D
    if t == r:
        return D

    // analyze previous round
    prev_actions = history[t-1]         // list of all players’ actions at t–1
    coop_count_others = count_C(prev_actions excluding you)
    group_success = (coop_count_others + (your_action_at_t-1 == C) >= m)

    if coop_count_others >= m:
        return D      // free‐ride forever
    if not group_success and coop_count_others == m-1:
        return C      // be the pivot to secure k
    return D          // otherwise defect
```

3. Edge cases  

• First round (t=1): no info, so defect.  
• Last round (t=r): classic end‐game, always defect.  
• If others never approach the threshold (coop_count_others < m-1), you always defect—no point in giving away your endowment with no hope of success.  
• If others overshoot (coop_count_others ≥ m), you permanently switch to defection and never “waste” a contribution again.  

4. Why “aggressive”?  

– You only cooperate when you can single‐handedly turn a failure into success and thus earn a payoff k > 1 (defection would yield only 1).  
– You never signal, you never forgive beyond that single pivotal move, and you never return cooperation once others prove they can succeed without you.  
– You exploit any stable cooperative clique by permanently free‐riding on them.  
– You defect in the last round unconditionally (standard ruthless end‐game).  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

This strategy maximizes exploitation of others’ contributions, incurs costs only when it directly benefits you more than defection, and refuses to build genuine cooperation. It is both simple to implement and aggressive in outlook.
'''

description_AGGRESSIVE_50 = '''
Below is a self-contained “aggressive exploiter” strategy.  It never hesitates to defect, only reluctantly cooperates when it can “tip” a borderline group into success so that it can still collect the bonus k—and otherwise punishes cooperators by withholding contributions even at the risk of group failure.

1.  Definitions & notation  
    •  n = total players (including you)  
    •  m = cooperation threshold  
    •  r = total rounds  
    •  t = current round index, t = 1…r  
    •  C = cooperate, D = defect  
    •  lastCoops = number of other players (not you) who cooperated in the most recent round  
       – initialize lastCoops = m (optimistic estimate) before round 1  

2.  High-level idea  
    •  If the others are already cooperating in numbers ≥ m+1, free-ride (D) and grab 1 + k.  
    •  If they are at exactly m−1, then cooperate this round (C) – you “tip the balance,” pay 1 but still get k, for a net gain of k vs. 1 if you’d defect.  
    •  In all other cases (others < m−1 or exactly m), defect and punish.  
    •  Always defect in the last round (cannot threaten or extract future benefit).  

3.  Pseudocode  

  // before round 1  
  lastCoops ← m  
  
  for t in 1…r:  
    // 1) Last‐round update has already set lastCoops  
    // 2) Decide action this round  
    if t == r then  
      action ← D                         // last‐round defect  
    else  
      if lastCoops ≥ m+1 then  
        action ← D                       // free-ride: threshold safe without you  
      else if lastCoops == m−1 then  
        action ← C                       // tip the group to reach m, secure k  
      else  
        action ← D                       // either hopeless or punish borderline success  
      end if  
    end if  

    // 3) Play action simultaneously with others  
    play(action)  

    // 4) Observe how many of the other n−1 players cooperated  
    lastCoops ← count of C among others this round  

  end for  

4.  Why it’s aggressive  
  •  You almost never pay the cost of cooperation.  
  •  You only pull out your wallet when the others are on the brink of sending everyone home with zero bonus k—then you “save the day” at your own small expense, solely to capture the group reward.  
  •  You punish any borderline success (exactly m cooperators among others) by defecting so that they fail and learn not to trust you.  
  •  In the final round you always defect—there is no future to threaten, so you maximize your own one-shot payoff.  

This strategy exploits any mild cooperators in the field, never builds goodwill beyond what is strictly necessary to seize the bonus, and ensures you never get out-spent on contributions.
'''

description_AGGRESSIVE_51 = '''
Below is an “extortionate‐free‐rider” style strategy that only cooperates when strictly necessary to secure the public good, otherwise defects to grab the private payoff—and it always defects in the last round.  

1.  Definitions and notation  
    •  t = round index, 1 ≤ t ≤ r  
    •  m = cooperation threshold (players needed)  
    •  C_i,t ∈ {0,1} = indicator that player i cooperated in round t (1=cooperate, 0=defect)  
    •  S_{–i,t} = number of cooperators among the other n–1 players in round t  
       = Σ_{j≠i} C_{j,t}  

2.  High‐level description  
    •  First round (t=1): defect.  
    •  Intermediate rounds (1 < t < r):  
       –  If in the previous round the others cooperated in at least m–1 numbers (S_{–i,t–1} ≥ m–1), play C.  
            Rationale: your single cooperation can push total cooperators from m–1 to m, earning you k plus the private 0 cost.  
       –  Otherwise (S_{–i,t–1} < m–1), defect: your cooperation would be futile (won’t reach m), so you grab the private 1.  
    •  Last round (t = r): always defect (no future to influence).  

3.  Pseudocode  

  initialize:  
    Record the history of all players’ actions; initially empty.  

  for t in 1..r:  
    if t == 1:  
      play D  # always defect in round 1  
    else if t == r:  
      play D  # always defect in the final round  
    else:  
      let S_prev = number of cooperators among others in round t–1  
      if S_prev ≥ m–1:  
        play C  
      else:  
        play D  

4.  Why this is aggressive  
    •  You never “waste” a cooperative move unless it is pivotal (others cooperated m–1 times).  
    •  You free-ride on any extra cooperators beyond m–1, because you defect whenever S_prev ≥ m.  
    •  You never “reward” uncooperative groups: if they failed to almost reach the threshold (S_prev < m–1), you defect again.  
    •  In the final round you always defect to maximize immediate payoff, foregoing any vestigial cooperation.  

5.  Handling edge cases  
    •  Uncertain predictions: we assume others will, on average, repeat last-round behaviors. This strategy is memory-1.  
    •  If other players also use extortionate logic, you will typically see S_prev bounce between m–1 and m (or fall below m–1 if all defect), but you will never be the sucker.  
    •  If at any round S_prev = m–1, you step in just enough to secure the bonus. If they overshoot to S_prev ≥ m, you exploit them.  

This strategy guarantees you never get less than the private endowment (1) when cooperation is hopeless, and it secures the public good (earning the extra k) only when you can extort maximal private gain from it.
'''

description_AGGRESSIVE_52 = '''
Below is an “aggressive‐free‐rider” strategy whose sole aim is to maximize your own payoff each round by never contributing, to break any emerging coalition and to exploit any coalition that forms without you.

1. Intuition  
   - In any single round, Defect strictly dominates Cooperate: if the threshold is met by others you get 1 + k by defecting vs. k by cooperating; if the threshold fails you get 1 by defecting vs. 0 by cooperating.  
   - Repeated play cannot improve others’ propensities to cooperate if you never reciprocate. By always defecting you (a) deprive them of marginal benefits from your contribution, (b) break any coalition whenever they are on the verge of success (m – 1 cooperators), and (c) exploit any coalition that succeeds without you.

2. Decision Rules  
   For each round t = 1, 2, …, r:  
   ­– Action = D (Defect), always.  

3. Edge‐Case Handling  
   ­– First round (t = 1): you have no information yet; defect to secure the safe private payoff.  
   ­– Intermediate rounds (1 < t < r): regardless of how many cooperated last round, you defect to punish those who cooperated and to exploit any coalition that succeeded.  
   ­– Last round (t = r): defect unconditionally (standard last‐round defection in a finitely repeated PD‐like environment).

4. Pseudocode  
   ```  
   function SELECT_ACTION(t, history, params):
       // params contains n, m, k, r but are unused because we never cooperate
       return "D"  // always defect
   ```

5. Why It Is Aggressive  
   ­– It never rewards others’ cooperation;  
   ­– It breaks near‐threshold cooperation (m–1 cooperators) by refusing your contribution;  
   ­– It plunders any coalition that emerges without you by free-riding;  
   ­– It gives zero signal of trusting or reciprocating, so others learn that cooperation is futile against you.

This “always‐defect” policy maximizes your per‐round payoff and systematically punishes any attempt by other players to meet the threshold.
'''

description_AGGRESSIVE_53 = '''
Below is an “aggressive” threshold‐dilemma strategy—call it the Threshold Extortioner.  In plain English, it (1) almost always defects, (2) exploits any cooperative surge by punishing thereafter, and (3) only ever contributes if absolutely necessary (and only at the pivotal last moment) to squeeze out a k‐payoff rather than settle for 1.

1. State Variables  
   • PUNISH (boolean flag, initially false)  
   • last_cooperators (integer, cooperators observed in previous round; initialize to 0)  

2. Decision Rule for round t = 1…r  

   if t == 1:  
       // Test‐the‐waters opening  
       action ← D  

   else:  
     // 2.a Detect a successful cooperation wave and flip into permanent punishment  
     if last_cooperators ≥ m then  
       PUNISH ← true  

     if PUNISH then  
       // Punish by never cooperating again  
       action ← D  

     else  
       // 2.b Predict this round’s cooperators as equal to last round’s  
       let predicted = last_cooperators  

       // 2.c If enough will cooperate, free‐ride  
       if predicted ≥ m then  
         action ← D  

       // 2.d If one short of threshold _and_ we are at the very last round, tip it over  
       else if predicted == m–1 and t == r then  
         action ← C  

       // 2.e Otherwise, keep defecting  
       else  
         action ← D  

   end if  

   // After play, update last_cooperators from observed profile  
   last_cooperators ← # of players who played C this round  

3. Corner‐Case Handling  
   • First round (t=1): D unconditionally, to gauge opponents’ willingness to cooperate.  
   • Last round (t=r): If opponents are predicted to be m–1 strong, cooperate just this once to secure the group payoff (you get π = 0 + k > 1). Otherwise defect.  
   • “Shock‐and‐awe” punish: the first time you see ≥m cooperators, you set PUNISH=true and thereafter “never cooperate,” ensuring you exploit any cooperative coalition that forms.  

4. Why It’s Aggressive  
   – You only pay the cooperation cost when it is strictly payoff‐maximizing on your own (m–1 others and final round).  
   – You exploit every wave of cooperators (free‐ride on their k) and then punish future attempts by refusing to contribute.  
   – No trust, no reciprocity—you “punish first, ask questions later,” leveraging the threat of permanent defection to destabilize any cooperative equilibrium.
'''

description_AGGRESSIVE_54 = '''
Below is an “Aggressive Grim‐Threat” strategy.  It is designed to (a) signal willingness to cooperate if and only if the group stays perfectly cooperative, (b) punish any defection by refusing to help the group ever again (thereby sabotaging future threshold rewards), and (c) avoid being last-round “sucker.”

1. State Variables  
   • DefectedBefore ← false  
     (becomes true as soon as you observe any player defect)  
   • t ← current round index (1…r)

2. Decision Rules  

   On each round t:  
   1. If t = r (final round):  
        – Play D.  
        – Rationale: no future rounds remain in which you can punish, so you maximize your one-shot gain.  
   2. Else if DefectedBefore = true:  
        – Play D.  
        – Rationale: you have already “triggered” the Grim Threat—never cooperate again.  
   3. Else (t < r and no defection seen so far):  
        – Play C.  
        – Rationale: you signal full cooperation to meet the threshold and secure the bonus k.  

   After all players’ moves are revealed in round t:  
   – If any player j (j≠ you) played D in round t, set DefectedBefore ← true.

3. Pseudocode  

   initialize DefectedBefore ← false  
   for t in 1…r do  
     if t = r then  
       action ← D  
     else if DefectedBefore then  
       action ← D  
     else  
       action ← C  
     end if  

     play(action)  
     observe all players’ actions in round t  
     if any observed action == D and that player ≠ you then  
       DefectedBefore ← true  
     end if  
   end for

4. Behavior Summary  
   – Rounds 1 through r–1: you fully cooperate so long as the group has been entirely cooperative in all prior rounds.  
   – At the first sign of any defection (even one player in one round), you permanently switch to D, denying the group future threshold rewards.  
   – Round r: you always defect, since you cannot retaliate afterward.

5. Why It’s Aggressive  
   – “Zero tolerance” trigger. A single defection from any player dooms all future cooperation.  
   – You willingly sacrifice future collective payoffs rather than tolerate free-riding.  
   – Last-round defection is standard end-game logic but also ensures you extract the private payoff once punishment is impossible.

This strategy leverages the threat of permanently withholding cooperation to coerce others into never defecting.  In practice, it is one of the harshest enforcement schemes: any defection by an opponent destroys not only the current round’s bonus but all remaining opportunities for the group reward.
'''

description_AGGRESSIVE_55 = '''
Below is a simple but maximally “aggressive” trigger‐free strategy that systematically refuses to help the group, thereby (a) guarantees you never lose by contributing and (b) whenever the other players manage to hit the threshold you free‐ride on their sacrifice.  In effect you sabotage every collective effort and capitalize on any success without ever paying a cost.

1.  Decision rule (for every round t=1…r):  
    • Play D (Defect) unconditionally.  

   Rationale:  
    – Cooperating costs you 1 unit of endowment with no private benefit unless the threshold is reached.  
    – If the threshold is reached by others, a defector’s payoff is 1 + k, which strictly dominates a cooperator’s payoff k.  
    – If the threshold fails, any cooperator gets 0 while you as a defector get 1.  
    – Hence “defect” strictly dominates “cooperate” in every possible outcome.  

2.  Edge‐case handling:  
    – First round: no history to observe → defect.  
    – Intermediate rounds: regardless of what you or others have done so far → defect.  
    – Final round: there is no future to influence → defect.  

3.  Aggressive mindset:  
    – You never help the public project.  
    – You ensure that even if m others try to cooperate, you sit back and collect the full reward 1 + k.  
    – You make it impossible for the group to rely on you: they must pay the full cost of m contributions every round, and even then you free‐ride.  

Pseudocode  

  for t in 1…r:  
      action[t] ← D    # always defect  

That is the entire strategy.  It maximizes your individual payoff round by round, sabotages any attempt at collective provision by refusing to contribute at any time, and free‐rides on any successes the other players manage to achieve.
'''

description_AGGRESSIVE_56 = '''
Below is an “aggressive free-riding” strategy.  It almost never cooperates, only doing so when its one contribution will tip the group over the threshold and yield it more than the zero-contribution payoff.  In every other situation it defects—even in early rounds—and it defects unconditionally in the final round.

1.  Notation  
   •  r = total rounds, t = current round (1 ≤ t ≤ r)  
   •  m = cooperation threshold, n = total players  
   •  Track in each past round s the number of cooperators among the other n–1 players, call that Sₛ.  

2.  High-level idea  
   •  ALWAYS defect except in the rare case that exactly m–1 of your opponents will cooperate this round—then by cooper­ating you push the total from m–1 to m and earn payoff k instead of the 1 you’d get by defecting.  
   •  In the last round, defect no matter what.  

3.  Forecasting “others’ cooperations”  
   •  We assume opponents’ aggregate behavior this round will mirror what happened in the previous round.  (No better information is available.)  
   •  If t=1, no history exists, so assume S₀ < m–1 and defect.  

4.  Formal decision rule for round t:  
```
if t == r:
    action ← D               # final‐round free‐ride

else:
    if t == 1:
        # no history, play safe
        action ← D

    else:
        S_prev ← number of cooperators among the other n–1 players in round t–1

        if S_prev == m–1:
            # my single C turns m–1 → m, so payoff  k  > 1
            action ← C

        else:
            # either threshold was already met or far from met:
            #   if S_prev ≥ m, I defect and still get k
            #   if S_prev < m–1, my C cannot reach m, so worthless
            action ← D
```

5.  Edge cases and remarks  
  •  First round (t=1): defect (no reliable forecast).  
  •  Last round (t=r): defect with certainty—no future to reward or punish.  
  •  Whenever your defection still leaves ≥m cooperators, you earn 1+k, strictly better than if you’d paid the cost and cooperated.  
  •  You only ever cooperate when your “marginal” contribution turns a losing round (no reward) into a winning one for you personally.  

This strategy is maximally aggressive: it never “wastes” a contribution unless that 1-unit cost is guaranteed to convert into a k-unit gain for itself.
'''

description_AGGRESSIVE_57 = '''
Below is a self-contained, round-by-round “aggressive” strategy—call it the Opportunistic Aggressor—that (i) never cooperates for “nice” reasons, (ii) only grudgingly contributes when it can single-handedly trigger the group reward, and (iii) otherwise defects to punish cooperators or exploit free-riders.

1.  Definitions  
    Let t = 1,…,r index rounds.  
    Let history Ht–1 record the number of cooperators in each past round.  
    In each round t, we compute   
      C_last = number of cooperators in round t–1 (zero if t=1).  

2.  Core Decision Rule (for t = 1…r)  
    if t == 1 then  
      play D   // No history, default to defect and test opponents  
    else  
      if C_last ≥ m then  
        // Others already met threshold without us  
        play D   // Exploit: collect 1 + k instead of 0 + k  
      else if C_last == m–1 then  
        // Our single cooperation will meet threshold  
        play C   // We pay 1 but gain k; others paid 1 too  
      else  
        // Even with our cooperation, threshold fails, or punishment desired  
        play D   // Defect to keep 1 and deny cooperators the reward  
      end  
    end  

3.  Comments on “Aggression”  
  •  We never cooperate to build trust or signal future cooperation—only if we can *guarantee* the payoff k by tipping the balance alone.  
  •  When C_last ≥ m, cooperators have already done the heavy lifting; we pocket an even higher return by defecting.  
  •  When C_last < m–1, cooperating is pointless (threshold still fails), so we defect and punish attempted cooperators.  

4.  Edge-Case Handling  
  –  First round (t=1): no information, so defect to probe.  
  –  Last round (t=r): same rule applies.  There is no “end-game” exception because we do not care about reputation or sustaining cooperation.  
  –  Stale history (e.g. if some players failed to act): treat missing observations as defections.  

5.  Pseudocode  

  initialize history H = []  
  for t in 1…r:  
    if t == 1:  
      action = D  
    else:  
      C_last = count_cooperations(H[t–1])  
      if C_last ≥ m:  
        action = D  
      else if C_last == m–1:  
        action = C  
      else:  
        action = D  
      end  
    end  

    play(action)  
    observe all players’ actions this round → record in H[t]  
  end  

With this rule set, you  
– Exploit any round in which the others nearly or fully meet the threshold,  
– Only “sacrifice” a contribution when it *directly* pays off, and  
– Otherwise defect to maximise your immediate payoff and punish well-meaning cooperators.
'''

description_AGGRESSIVE_58 = '''
Below is an “aggressive” threshold‐dilemma strategy.  The idea is that you (1) never cooperate more than absolutely necessary to hit the threshold, (2) free‐ride whenever the group last round already cleared the bar, (3) punish borderline groups that almost made it without you, and (4) in the final round defect whenever you can.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Notation  
  n   = number of players  
  r   = total rounds  
  m   = cooperation threshold  
  k   = bonus payoff when threshold is met  
  t   = current round index (1…r)  
  
State you track each round t>1:  
  prev_others_coops  = how many of the OTHER n–1 players played C in round t–1  
  prev_total_coops   = how many total players (including you) played C in round t–1  

Your action in round t, a_t ∈ {C, D}:  

1. Initialization (t=1)  
   You have no history—defect to probe and take the safe 1‐unit payoff.  
   a_1 ← D  

2. Intermediate rounds (2 ≤ t < r)  
   if prev_total_coops ≥ m then  
     // Last round the group succeeded even without your extra effort  
     a_t ← D       // Free‐ride on others’ cooperations  
   else  
     // Last round failed, so we look at how many others cooperated  
     if prev_others_coops ≤ m–2 then  
       // They are far from the threshold—if everyone else stays the same, we won’t make it.  
       a_t ← C     // Step in to try to hit the bar  
     else if prev_others_coops == m–1 then  
       // They came within one of the threshold last time and presumably saved you  
       // by cooperation—now punish them by withholding your support  
       a_t ← D  
     end  
   end  

3. Last round (t = r)  
   // There is no future to punish or be punished—pure opportunism  
   if prev_others_coops ≥ m then  
     // Others alone clear the bar—go for the defection bonus  
     a_r ← D  
   else  
     // Others cannot clear the bar without you—if you cooperate you get k>1 instead of 1  
     a_r ← C  
   end  

4. Updating history  
   After all players act in round t, observe total_cooperators_t and your own act a_t.  
   prev_total_coops   ← total_cooperators_t  
   prev_others_coops  ← total_cooperators_t – (a_t == C ? 1 : 0)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Rationale and “aggressiveness” highlights  
•  “Defect by default.” You only ever pay the cost of C when you judge it indispensable.  
•  “Free‐ride whenever possible.” As soon as the group has shown it can clear the threshold (prev_total_coops ≥ m), you withhold cooperation to pocket the extra point.  
•  “Punish near‐misses.” If the others came within one cooperator of the threshold (prev_others_coops = m–1), you defect to let them fail—even though you could have saved them cheaply.  
•  “Last round defection.” No future leverage means you never contribute in the final round unless your single C is the only thing that delivers k.  

This strategy maximizes your private payoff, exploits cooperative runs by others, and aggressively punishes any group that almost did it without you.
'''

description_AGGRESSIVE_59 = '''
Below is a memory-one, “aggressive” strategy we’ll call Aggressive Pivotal Exploiter (APE).  It never cooperates unless its single cooperation is guaranteed to push the group over the threshold—otherwise it always defects, and it defects in the first and last rounds to avoid end-game exploitation.

1. Data kept:  
   – actions[t–1][j] for each player j (including self) from the immediately preceding round.  
   – round index t, from 1 to r.  

2. High-level rule:  
   – Round 1 ⇒ Defect.  
   – Round r ⇒ Defect.  
   – Any other round t (2 ≤ t ≤ r–1):  
       • Let totalCoopPrev = number of C’s in round t–1 by all players.  
       • Let myCoopPrev = 1 if I played C in t–1, else 0.  
       • Let othersCoopPrev = totalCoopPrev – myCoopPrev.  
       • If othersCoopPrev == m–1, play C (be pivotal).  
       • Otherwise, play D.  

3. Pseudocode  
```
initialize history list actions[1..r][1..n]  // filled in as the game proceeds
for t in 1..r:
  if t == 1 or t == r:
    action_t = D
  else:
    // count how many cooperated last round
    totalCoopPrev = count_j(actions[t-1][j] == 'C')
    myCoopPrev    = (actions[t-1][self] == 'C') ? 1 : 0
    othersCoopPrev = totalCoopPrev - myCoopPrev

    if othersCoopPrev == m - 1:
      action_t = C    // my single cooperation will tip the group to ≥ m
    else:
      action_t = D

  // submit action_t this round, then observe all players’ actions to fill actions[t][*]
endfor
```

4. Explanation of “aggressive” character  
  • Default is Defect—no blind trust.  
  • Only cooperates when *pivotal* (othersCoopPrev = m–1), so every time it cooperates the public good is guaranteed—no wasted contributions.  
  • When enough others already would cooperate (othersCoopPrev ≥ m), it defects to free-ride on their effort.  
  • First- and last-round defects eliminate any test-of-cooperation or end-game gambits by opponents.  

This yields a high individual payoff by exploiting any cooperative tendencies in the field while never being the sucker.
'''

description_AGGRESSIVE_60 = '''
Below is an “aggressive” pivot‐defector strategy (“Aggressive Pivotal Defection,” APD) that exploits others’ willingness to cooperate, only contributing when strictly necessary to capture the group reward, and otherwise defecting to maximize your private payoff.  

1.  Overview of the Mindset  
    -  You will almost always defect (D), i.e. keep your private endowment.  
    -  You only cooperate (C) when you predict that without your cooperation the threshold m would just barely fail (i.e. exactly m–1 others will cooperate). In that “pivotal” case, you cooperate to push the total to m and collect k.  
    -  First round you have no information—defect.  
    -  Last round behaves just like any other: still only cooperate when pivotal.  
    -  By never over‐cooperating, you punish generous opponents and never give away a contribution unless it directly raises your payoff.  

2.  Detailed Decision Rule  
    Maintain a single state variable prev_coop_count = the number of players who cooperated in the previous round (excluding yourself).  

    On each round t = 1…r:  
      if t == 1:  
        action ← D  
      else:  
        if prev_coop_count == m – 1:  
          action ← C    // your one contribution turns m–1 into m  
        else:  
          action ← D    // either threshold is unreachable (≤ m–2) or already safe (≥ m)  
      end if  

      Play(action).  
      Observe total_cooperators this round (including yourself).  
      prev_coop_count ← total_cooperators – (action==C ? 1 : 0).  

3.  Why It’s Aggressive  
    •  You defect by default, free‐riding on others.  
    •  You never “over‐contribute” once the threshold is already met (others pay the cost).  
    •  You refuse to waste contributions when the threshold is unreachable.  
    •  You only help exactly when it boosts your own payoff from 1 to 1 + k.  

4.  Pseudocode  

    // PARAMETERS: m (threshold), r (rounds), n (players, only for bookkeeping)  
    // STATE: prev_coop_count ∈ {0,…,n–1}  
    initialize prev_coop_count ← 0  
    
    for t in 1…r do  
      if t == 1 then  
        my_action ← D  
      else if prev_coop_count == m – 1 then  
        my_action ← C  
      else  
        my_action ← D  
      end if  

      play(my_action)  
      // Observe how many of the other (n–1) players played C this round  
      observe coop_others this round  
      // Update for next round’s prediction  
      prev_coop_count ← coop_others  
    end for  

5.  Edge Cases  
    •  First round: defect, because you have no history.  
    •  If in any round you observe exactly m–1 cooperators among opponents, you become that pivotal m-th cooperator.  
    •  If you ever mis‐predict (e.g. others randomize), you simply continue to defect until you again see exactly m–1.  
    •  The last round uses the same rule—no late‐game “nicer” behavior or end-game defection fudge factor is needed.  

This strategy is fully deterministic, punishing, and maximally exploitative of any cooperating opponents. By only contributing at the exact pivot point, you secure the group reward when it directly raises your payoff, and otherwise hoard the full private endowment.
'''

description_AGGRESSIVE_61 = '''
Below is a self-contained, “aggressive” strategy for the repeated collective‐risk dilemma.  It is built around two ideas:  
 1.  You will almost always defect, both to break any emerging cooperation and to free‐ride whenever possible.  
 2.  You will only ever cooperate when you can be sure that your one unit of “sacrifice” will tip the group over the threshold and thus generate k for you—after which you resume defection to milk the cooperators.  

—  
STRATEGY NAME  
  Exploitative Tipper  

PARAMETERS (known to all):  
  n ≥ 2 players, r ≥ 2 rounds, threshold m (1 < m < n), reward factor k > 1.  

NOTATION:  
  t = current round (1…r)  
  coopCount[t–1] = number of players (including you) who cooperated in the previous round  
    – when t = 1 we treat coopCount[0] = 0 (no history)  

DECISION RULE (for each round t):  
  1.  If t = 1 (first round), play D (defect).  
  2.  Else if t = r (last round), play D.  
  3.  Else (2 ≤ t < r):  
       a.  If coopCount[t–1] ≥ m  
             // Last round the threshold was met even though you defected → free-ride again  
             play D.  
       b.  Else if coopCount[t–1] = m–1  
             // You can single‐handedly tip the balance to reach m this round  
             play C once to secure +k for this round, then revert to defecting  
       c.  Else  
             // Too few cooperators in the last round to make your C worthwhile  
             play D.  

PSEUDOCODE  

  initialize coopCount[0] ← 0  
  for t in 1…r do  
    if t == 1:  
      action[t] ← D  
    else if t == r:  
      action[t] ← D  
    else:  // 2 ≤ t < r  
      if coopCount[t–1] ≥ m:  
        // threshold would be met even if I defect  
        action[t] ← D  
      else if coopCount[t–1] == m–1:  
        // my one cooperation tips over the threshold  
        action[t] ← C  
      else:  
        action[t] ← D  

    play action[t], observe others’ actions  
    coopCount[t] ← number of players (including myself) who chose C in round t  
  end for  

WHY IT’S AGGRESSIVE  
  •  You almost never cooperate, so you sabotage any stable cooperation and keep the group struggling to reach m.  
  •  When the other players come tantalizingly close (m–1 cooperators), you exploit them by adding your lone C to unlock the full reward k—but only once per such opportunity—then you revert to defection and punish them for having cooperated.  
  •  By defecting in round 1 and round r, you eliminate any “forgiveness” in the first‐move and any vestigial incentive to cooperate at the end.  

EDGE CASES HANDLED  
  – First round (no history): Defect, to establish your reputation as a hard‐liner.  
  – Last round: Defect, since there is no future to punish or reward.  
  – Whenever threshold was already met without you: you continue to defect and free-ride.  
  – Whenever threshold cannot be reached even with your cooperation (coopCount < m–1): defect, as your C would be wasted.  

OVERALL EFFECT  
  This agent injects uncertainty and fear of exploitation into every round.  Whenever a coalition of cooperators almost reaches m, you swoop in to claim k at minimal personal cost, and then immediately punish further cooperation by reverting to defection.
'''

description_AGGRESSIVE_62 = '''
Below is an “aggressive” threshold‐public‐goods strategy we’ll call “Threshold Slasher.”  It exploits cooperators, punishes defectors, and never lets the group ride free without paying a cost.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: Threshold Slasher  
Parameters known to all players: n, r, m, k  

State variables (maintained by you each round):  
• last_coop_count ∈ {0,…,n}  – number of players (including you) who chose C in the previous round  
• triggered ∈ {false,true} – have we “gone full grim” on defectors?  
• t = current round index, t = 1…r  

High‐level idea  
1. Defect on round 1 to send an aggressive signal.  
2. Exploit the group whenever you can defect without breaking the m‐threshold.  
3. If cooperation exactly met the threshold last round (last_coop_count = m), cooperate this round to keep the project alive—but only just.  
4. If the threshold failed last round, keep defecting (no upside to rescuing).  
5. If any opponent ever defects in a round where the group still met the threshold, trigger a permanent defection (“grim trigger”) to punish free‐riders.  
6. Always defect in the final round to grab the private payoff.  

Detailed decision rules (pseudocode)  
```
Initialize:
  triggered ← false
  last_coop_count ← undefined

For each round t = 1 to r do:
  
  If t = 1 then
    # first‐round aggression
    play D
  else if t > r – 1 then
    # last round (t = r) or near‐final can be folded into "always defect final"
    play D
  else if triggered = true then
    # once triggered, never cooperate again
    play D
  else
    # we are not yet triggered, and not in first/last round
    If last_coop_count < m then
      # group failed threshold → no reward even if we cooperate
      play D
    else if last_coop_count > m then
      # more than m cooperated last time → we can defect without breaking threshold
      play D
    else
      # exactly m cooperated last time → if we defect now, group fails;
      # must cooperate just enough to keep the reward flowing
      play C
    end if
  end if

  # Observe outcome of this round before moving on:
  Let coopers_this_round = number of C's observed
  If (coopers_this_round ≥ m) AND (someone defected this round) then
    # threshold was met despite a defection → they free‐rode on others
    triggered ← true
  end if
  last_coop_count ← coopers_this_round
end for
```

Explanation of key lines  
1. Round 1 defect: no risk of punishment, sets tone that you won’t be taken advantage of.  
2. Last round defect: classical end‐game defection to grab the private payoff.  
3. Grim trigger: as soon as any player defects yet the threshold still succeeds, we assume a free‐rider attack and cease cooperating forever after.  
4. Exploit vs. rescue logic:  
   • If fewer than m cooperated last round, the project failed → no point rescuing.  
   • If more than m cooperated, you can defect and still leave ≥m cooperators → exploit.  
   • Only when exactly m cooperated do you put in one unit (play C) to keep the group reward alive.  

Why aggressive?  
– You never cooperate when you can get away with defecting (exploitation).  
– You harshly punish any sign of free‐riding via a permanent switch to defection.  
– You storm out in the final round to maximize private gain.  

This strategy minimizes your concession while still extracting the threshold bonus when it is cheapest to do so, and it deters would‐be exploiters with a grim threat.
'''

description_AGGRESSIVE_63 = '''
Below is an “Aggressive Opportunist” strategy.  It never cooperates unless it is strictly necessary to push the group over the m‐cooperator threshold, and it always defects otherwise (especially in the last round).  This maximizes your own payoff by free‐riding as much as possible while only contributing when the group otherwise would fail.

1.  State tracking  
    •  At the end of each round t–1 you observe how many of the OTHER n–1 players cooperated. Call that count c.  

2.  Decision rule for round t (1 ≤ t ≤ r)  
    if t == 1:  
       play D  
    else if t == r:  
       play D    # final round: no future benefit from cooperating  
    else:  
       if c == m–1:  
          play C    # just enough others cooperated last time that your C will tip it over  
       else:  
          play D    # either others already exceed the threshold (so you free‐ride)  
                    # or they’re too few to reach threshold even if you cooperate  

3.  Edge cases / justification  
   •  First round (t=1): defect to “feel out” opponents.  
   •  Intermediate rounds: only cooperate when exactly m–1 others did so on the previous move.  In that case your single contribution guarantees the bonus k for yourself (and everyone), and you’re willing to pay the cost once.  In every other situation (others already hit ≥m, or were below m–1), you defect and maximize your one‐period payoff.  
   •  Last round (t=r): defect unconditionally—no future rounds in which to exploit cooperation.  

4.  Pseudocode  

   initialize nothing  
   for t in 1..r:  
     if t == 1 or t == r:  
       action[t] ← D  
     else:  
       let c ← number of opponents who played C in round t–1  
       if c == m−1:  
         action[t] ← C  
       else:  
         action[t] ← D  

This strategy is “aggressive” because:  
 1) It never builds long‐run cooperation; it punishes any shortfall by refusing to help again unless the group comes right to the brink.  
 2) It free‐rides on any surplus contributions (c ≥ m), harvesting the full bonus k without ever paying the cost except when strictly forced.  
 3) It defects in the final round, extracting maximum payoff when there is zero or minimal external pressure to cooperate.
'''

description_AGGRESSIVE_64 = '''
Below is an “aggressive” repeated‐game strategy—call it the Pivotal-Selfish rule—that maximizes your own points by defecting everywhere except in the one case where you alone can tip the community over the cooperation threshold and thus extract the larger k‐payoff.

1. DATA YOU KEEP  
   • r: total rounds  
   • m: cooperation threshold  
   • history of previous rounds’ actions by all players  

2. HIGH-LEVEL IDEA  
   In any round you ask: “Were there exactly m–1 cooperators among the *other* n–1 players last time?”  
   – If yes, then by cooperating you raise total cooperators from m–1 to m, trigger the +k reward, and earn k (0 + k), which is larger than 1.  
   – In every other circumstance, defect: either you fail to tip the group (so C gives 0, D gives 1), or you free-ride on an already safe group (so C yields k, D yields 1 + k).  

   This rule never “wastes” a contribution, yet seizes every opportunity to be the pivotal cooperator when it strictly increases your own payoff.

3. DETAILED DECISION RULES  

   Initialize:  
     history = []  

   For each round t = 1…r do  
     if t == 1 then  
       play D  
     else  
       let prev = history[t−1]  (the vector of {C,D} by all n players last round)  
       let o_count = number of C’s in prev *excluding* your own action  
         (i.e. count how many of the other n–1 players cooperated in round t−1)  
       if o_count == m−1 then  
         play C   // you alone can tip to exactly m cooperators  
       else  
         play D   // either you free-ride or avoid wasting a contribution  
       end if  
     end if  

     observe actions of all players this round; append to history  
   end for  

4. PAYOFF ACCOUNTING  
   If you play C in a round where others’ cooperators last round equaled m−1 *and* they repeat that behavior this round, then total cooperators = m and your round payoff = 0 + k = k.  
   In *every* other round you play D, so  
     – if others achieve ≥ m cooperators on their own you get 1 + k  
     – if they fail you get 1  

5. EDGE-CASE HANDLING  
   • First round (t=1): no history ⇒ assume worst case (no one will coordinate around m–1), so defect.  
   • Last round: follows the same local test—no need for a special “final‐round” trigger because you never cooperate unless you are sure to tip the group and directly earn k.  
   • If m−1 > n−1 then you’ll never see o_count == m−1 ⇒ you always defect (correct, since you could never be pivotal).  
   • If opponents change their pattern, you adapt instantly: you only ever “risk” a contribution when it is strictly payoff-maximizing for you.  

6. WHY IT’S “AGGRESSIVE”  
   – You never “waste” a contribution.  
   – You never build trust or run a cooperation “test” unless it guarantees you a strictly higher return (k > 1).  
   – You free-ride on any group success that you don’t absolutely need to create yourself.  
   – You drop out immediately if you can’t be pivotal.  

This rule focuses purely on maximizing your own cumulative payoff in the tournament, exploits any near-threshold cooperation among opponents, and never extends cooperation except when it is directly in your self‐interest.
'''

description_COOPERATIVE_65 = '''
Below is a “threshold-focused conditional cooperator” strategy.  It tries to guarantee that at least m players cooperate each round (thus earning the group payoff k), but gives up (defects) if the group clearly cannot reach the threshold.  It also plays C in the very first round to signal willingness to cooperate, and defects in the last round (where one-shot logic dominates).  

1.  Intuition  
   •  Round 1: Signal cooperation.  
   •  Middle rounds:  
       –  If in the previous round there were already ≥ m–1 cooperators, then cooperate again—either you join the m–1 to hit m, or you sustain an existing surplus of cooperators.  
       –  If there were < m–1 cooperators, the group is too far from the target; defect to avoid wasting your endowment.  
   •  Last round: Defect (one-shot dominant).  

2.  Pseudocode  
```
Inputs: n, r, m, k
History H: for each round t we know actions a_i(t) ∈ {C,D} for all players i

For each round t = 1…r do:
  if t == 1:
    play C
  else if t == r:
    play D
  else:
    let prev = t – 1
    let coop_count = number of players j with a_j(prev) == C

    if coop_count >= m–1:
      play C
    else
      play D
```

3.  Explanation of decision rules  
– First round (t=1): Play C to show cooperation.  Without a history you can still try for the public-good.  
– Middle rounds (2 ≤ t < r):  
   • If coop_count ≥ m – 1, then even if there were exactly m–1 cooperators last round you can “complete” the coalition this round, and if there were more than m–1 you help sustain a surplus so that minor deviations don’t doom the project.  
   • If coop_count < m – 1, then the group was too far from hitting the threshold.  You switch to D to avoid paying c=1 for a doomed project.  
– Last round (t=r): Defect, because in a one-shot threshold game no credible future punishment exists.  

4.  Handling edge cases  
– If m=2 then “coop_count ≥1” ⇒ you always cooperate unless no one cooperated in the prior round.  
– If the group always just reaches m (coop_count=m), this rule keeps everyone cooperating forever (until the last round).  
– If the group fails badly (coop_count < m–1), you withdraw immediately, punishing low-cooperation behavior.  
– If r is small (e.g. r=2), you play C in round 1 and D in round 2—optimistic first, then retreat.  

5.  Cooperative mindset  
This strategy:  
• Opens with cooperation.  
• Forgives one stray defection (because coop_count=m–1 is still “salvageable”).  
• Sustains any surplus of cooperators without triggering needless punishments.  
• Only gives up when the group is clearly under-performing.  
• Restricts defection to the very last round, accepting the one-shot inevitability there.  

By following these simple rules, you (and any like-minded players) will typically lock into rounds of full (or near-threshold) cooperation, securing the collective reward k each round, yet avoid the “sucker’s payoff” whenever too many defect.
'''

description_COOPERATIVE_66 = '''
Below is a single‐strategy description—parameterized by (n,r,m,k)—that (i) always seeks to reach the public‐good threshold, (ii) punishes any round in which the group fails to reach it, and (iii) never “unravels” at the very end (because cooperating in the last round still yields the bonus k>1).  You can think of it as a “Threshold‐Grim” trigger.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  State Variables  
   • good = true  
     – This flag means “so far, every round has reached at least m cooperators.”  

2.  Decision Rule (every round t = 1…r)  
   if good == true then  
     play C  (cooperate)  
   else  
     play D  (defect forever, as punishment)  

3.  State‐Update Rule (after seeing all n choices in round t)  
   let coopCount = number of players (including you) who played C in round t  
   if coopCount < m then  
     good ← false  
   else  
     good ← good   (i.e. stay in the good state)  

4.  Edge Cases  
   • Round 1: good starts true, so you cooperate.  
   • Any round t: if every past round met the threshold, you continue to cooperate.  
   • As soon as the group ever fails to meet the threshold (coopCount<m), you set good=false and defect in all remaining rounds.  
   • Last round t=r is treated exactly like any other round.  Since k>1, cooperation when the threshold is likely met still dominates defection (1 vs. 0+k).  

5.  Rationale & Cooperation Mindset  
   – So long as the group collectively avoids “risk” (i.e. always secures ≥ m cooperators), you reinforce full cooperation.  
   – The single permanent punishment (grim trigger) deters any one player from dropping out and letting the group fall short.  
   – Because cooperating in the last round still yields a payoff of k>1 (versus 1 from defection), there is no incentive to “defect in the end”—you will cooperate right through round r.  
   – If all players adopt this same strategy, every round will see n cooperators ≥ m, and each player’s payoff per round is 0 (cost) + k, maximizing the group bonus.  

6.  Pseudocode  

  initialize  
    good ← true

  for t in 1..r do  
    if good then  
      actionᵢ ← C  
    else  
      actionᵢ ← D  
    end if

    play actionᵢ simultaneously with others  
    observe others’ actions and compute  
      coopCount ← # of players who played C this round

    if coopCount < m then  
      good ← false  
    end if
  end for

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

By punishing only when the group actually suffers the collective‐risk loss, this rule aligns everyone’s incentives on maintaining the public good in every round—including the last.
'''

description_COOPERATIVE_67 = '''
Below is a simple yet effective “grim‐trigger” style rule that (i) sustains full cooperation up until the last round, (ii) punishes any deviation by switching to all‐D forever afterward, and (iii) defects in the known last round (where cooperation is hopeless anyway).  This strategy is subgame‐perfect in that no single player can gain by unilaterally deviating (all know the threat is real), and it delivers cooperation in r–1 of r rounds.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
1. State variables  
   punishing ← false   // have we ever seen a “failed threshold” yet?

2. Initialization (before round 1)  
   punishing ← false

3. In each round t = 1,2,…,r do:

   if t = r then  
     play D   // Last round: defect (no future to punish)

   else if punishing = true then  
     play D   // We are in punishment mode

   else  
     play C   // Normal cooperative mode

   end if

4. After observing the round’s actions (everyone’s C or D), update:

   let coopCount ← number of players who played C this round  
   if coopCount < m then  
     punishing ← true  
   end if

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Why it works:

• Round 1: punishing=false ⇒ we play C.  By symmetry, if everyone follows it, coopCount=n≥m ⇒ threshold met.  
• For t=2,…,r–1: so long as every past round met the threshold, punishing remains false ⇒ we keep cooperating.  That supports full‐C equilibrium for r–1 rounds.  
• If any round k<r ever falls short (coopCount<m), then from the very next round onward we switch to D forever.  A one‐shot defector in round k caused everyone to lose k in future cooperation rounds, so nobody wants to deviate.  
• Round r: we defect regardless (finite horizon last‐round logic).

Edge Cases:

– If multiple players deviate simultaneously causing coopCount<m, the same punishment triggers.  
– If exactly m–1 players (including us) cooperate in some round, we still see it as “failure” and switch to punishment.  
– If the group never meets the threshold (e.g. someone defects round 1), we punish immediately and never try to cooperate again—saving further losses.  

In short, this is a standard grim‐trigger for a threshold public‐goods game with a known finite horizon. It achieves maximal cooperation (r–1 successful public‐good rounds) while making any single deviation unprofitable.
'''

description_COOPERATIVE_68 = '''
Below is a single‐strategy description—“Threshold‐Tit-for-Tat with Limited Punishment and Last-Round Adjustment”—that is designed to sustain cooperation on the m-threshold in the bulk of the game, punish brief lapses, forgive quickly, and handle the last round.  

1. State variables (maintained across rounds)  
   • prev_success ∈ {true, false}.  Did the group (including you) reach ≥ m cooperators in the previous round?  
   • punish_rounds ∈ ℕ.  How many further rounds you will defect purely as punishment (starts at 0).  

2. Initialization (before round 1)  
   prev_success ← true  
   punish_rounds ← 0  

3. Per-round decision rule (for round t = 1…r)  
   if t = 1 then  
     play C  
   else if punish_rounds > 0 then  
     play D  
   else if t = r then  
     // Last-round free-ride adjustment  
     if prev_success = true then play D else play C  
   else  
     // Interior rounds: mirror whether group succeeded last time  
     if prev_success = true then play C else play D  

4. Update after observing all players’ actions this round  
   let N_C = number of players (including you) who chose C this round  
   if N_C ≥ m then  
     // group succeeded  
     prev_success ← true  
     // cancel any remaining punishment if we just succeeded  
     punish_rounds ← 0  
   else  
     // group failed  
     prev_success ← false  
     // trigger a single-round punishment  
     punish_rounds ← 1  

5. Commentary on the parts  

– First round: cooperate unconditionally to signal willingness.  
– Interior rounds (2 ≤ t < r):  
 • If last round reached the threshold (prev_success = true) and you are not currently “in punishment,” you cooperate—this maintains the public good.  
 • If last round failed, you defect for exactly one round (punish_rounds = 1), then forgive and return to cooperating the following round.  
– Last round (t = r):  
 • If last round was a success, you switch to D to claim the extra private +1 on top of the k (a one-shot free-ride).  
 • If last round failed, you cooperate to give the group one final chance to hit the threshold and earn k.  
– The single-round punishment (punish_rounds = 1) deters serial free-riding but is quickly forgiven so the group can re–coordinate.  
– This strategy is fully specified, deterministic, and depends only on observable history. It is a “cooperative‐minded” Tit-for-Tat variant:  
 • It rewards successful threshold attainment with further cooperation.  
 • It punishes a single failure once.  
 • It forgives immediately upon observing success.  
 • It handles both the very first and very last rounds in a consistent, transparent way.  

Pseudocode (compact form)  
```
prev_success = true
punish_rounds = 0

for t in 1..r:
    if t == 1:
        action = C
    else if punish_rounds > 0:
        action = D
    else if t == r:
        action = (prev_success ? D : C)
    else:
        action = (prev_success ? C : D)

    play(action)
    observe all players’ actions → compute N_C

    if N_C >= m:
        prev_success = true
        punish_rounds = 0
    else:
        prev_success = false
        punish_rounds = 1
```

Edge cases:  
– If r = 2, the first round follows the “t = 1” rule (C), and the second (last) round uses the last-round branch: if you succeeded in round 1, you D; else C.  
– If more than one failure occurs in a row, you will defect every time there is a failure, but only for one round after each failure.  

This design keeps the group on the m-cooperator equilibrium path most of the time, punishes only briefly to deter defection, immediately rewards new compliance, and maximizes your payoff in the final round if cooperation is already “on track.”
'''

description_COOPERATIVE_69 = '''
Below is a self-contained strategy, “Conditional Cooperation with Optimism and Forgiveness (CCOF),” designed to sustain cooperation in the repeated collective‐risk dilemma.  It (1) starts cooperatively, (2) uses simple signals from the previous round to decide, (3) tries to fill near‐miss gaps, (4) punishes hopeless rounds, (5) forgives quickly, and (6) handles first and last rounds.

---

Strategy name  
CCOF – Conditional Cooperation with Optimism and Forgiveness

Parameters it uses from the game specification  
• m = threshold # of cooperators  
• r = total # of rounds  
• In each round t we observe prev_cooperators = number of players who played C in round t−1.

Overview of decision‐rule logic  
1. Round 1: Play C (establish goodwill).  
2. Rounds 2…r−1:  
   a. If prev_cooperators ≥ m  →  the group just met threshold → play C.  
   b. Else if prev_cooperators = m−1  →  we can “fill the gap” → play C.  
   c. Else  (prev_cooperators ≤ m−2)  →  too few cooperators last time → play D.  
3. Round r (last round):  
   We still attempt cooperation if it can matter, otherwise defect:  
   a. If prev_cooperators ≥ m−1  →  play C.  
   b. Else  →  play D.

Forgiveness clause  
If in some round t you played D (case c above) but then in t+1 the group recovers (prev_cooperators ≥ m), immediately switch back to C at t+1, rather than continue punishing.

Pseudocode

  initialize:
    prev_cooperators ← unknown

  for t in 1…r do
    if t == 1 then
      action ← C
    else if t == r then
      // last round
      if prev_cooperators ≥ m−1 then
        action ← C
      else
        action ← D
      end
    else
      // intermediate rounds
      if prev_cooperators ≥ m then
        action ← C
      else if prev_cooperators == m−1 then
        action ← C
      else
        action ← D
      end
    end

    play action
    observe how many cooperated this round → set prev_cooperators for next iteration
  end

Rationale

• Optimistic start (t=1) builds goodwill.  
• “Fill‐the‐gap” rule (when prev_cooperators = m−1) gives us a strong chance to push the group over the threshold.  
• If the group was far below m (prev_cooperators ≤ m−2), our solo cooperation would be wasted (no threshold), so we defect to conserve our endowment.  
• Forgiveness: as soon as the group recovers (≥m cooperators), we resume cooperating—no endless vendetta.  
• Last round rule still helps the group reach threshold if we’re one short (prev_cooperators=m−1), otherwise we defect rationally.  

This strategy is  
– cooperative (it tries to meet the threshold whenever feasible),  
– retalitory only when cooperation is demonstrably hopeless,  
– quickly forgiving, and  
– easy to implement in a tournament of LLM-based opponents.
'''

description_COOPERATIVE_70 = '''
Below is a single‐strategy description—call it the “Rotating Core + Recovery” protocol—that (i) guarantees at least m cooperators whenever the protocol is followed, (ii) shares the cooperation burden fairly over r rounds, and (iii) automatically recovers from any round in which threshold m was missed.  

1. Preliminaries  
   • Players are labeled 1,2,…,n.  
   • We assume common knowledge of (n,m,r).  
   • Every player runs the exact same recipe in every round.  

2. High‐Level Idea  
   a) In “normal operation,” exactly m players cooperate each round according to a public, deterministic rotation.  This yields exactly m cooperators → threshold met → everybody earns k − (their own contribution).  Over r rounds each index cooperates about (m·r)/n times (±1), so the load is evenly spread.  
   b) If ever a round fails to reach m cooperators (e.g. someone deviated or made an error), the very next round all n players switch to C.  Since n ≥ m, the threshold is certainly met, re‐establishing trust.  After that single “recovery” round, the protocol returns to normal rotation.  

3. Formal Definition  

   Let Cset(t) ⊆ {1..n} be the designated cooperators in round t under normal operation.  Define for t=1..r:  
     Cset(t) = {  ((t−1)·m + 1) mod n, …, ((t−1)·m + m) mod n  }  
     where “mod n” yields {1,…,n} (i.e. if x mod n = 0 interpret as n).  

   Example (n=6,m=2):  
     Round 1: Cset={1,2}  
     Round 2: Cset={3,4}  
     Round 3: Cset={5,6}  
     Round 4: Cset={1,2}  … and so on.  

4. State‐Tracking  

   Each player maintains a single Boolean flag “need_recovery” (initially false).  

5. Per‐Round Decision Rule (for player i in round t):  
   1) If t>1 and in round t−1 the observed number of cooperators < m, then set need_recovery := true.  
   2) If need_recovery == true:  
         play C   // all-in on the next round  
         // after observing round t’s actions, reset need_recovery := false  
      Else  // normal operation  
         if i ∈ Cset(t) then play C else play D  

6. Edge Cases  
   • First round (t=1): need_recovery = false, so players 1..m cooperate, rest defect.  Threshold succeeds.  
   • Any failure round: t = τ with coop_count(τ)<m ⇒ at τ+1 everyone plays C ⇒ coop_count(τ+1)=n≥m ⇒ recovery guaranteed.  
                After observing success at τ+1, we clear need_recovery and resume rotation at τ+2.  
   • Last round (t=r): the same rule applies.  If it’s a normal‐operation slot and you’re in Cset(r), you pay 1 to get +k net; if you expect the other m−1 will show up, that’s positive.  If need_recovery is true you also cooperate, but since n≥m that’s enough.  

7. Why It’s Cooperative  
   – Guarantees threshold success in every round except at most the very first failed round (which immediately triggers recovery).  
   – Shares the “cooperator burden” evenly: over r rounds each player cooperates exactly the number of times that m·r/n dictates (up to ±1).  
   – No permanent punishments: any slip is met by an all-C recovery, not a harsh trigger.  
   – Fully deterministic and common-knowledge, so if every player runs this protocol you get perfect success every round.  

8. Pseudocode Sketch  

   initialize need_recovery := false  
   for t in 1..r do  
     if t>1 and (observed_cooperator_count[t−1] < m) then  
       need_recovery := true  
     end if  

     if need_recovery then  
       action_i := C  
     else  
       // normal rotation  
       start := ((t−1)*m) mod n + 1  
       endIndex := (start + m − 1 − 1) mod n + 1  
         // build the set of m labels from start … endIndex cyclically  
       if i in that set then action_i := C else action_i := D  
     end if  

     play(action_i), observe others’ actions  
     if need_recovery then  
       // recovery always lasts exactly one round  
       need_recovery := false  
     end if  
   end for  

That completes a fully cooperative, fair, easily implementable strategy.
'''

description_COOPERATIVE_71 = '''
Below is a simple “threshold‐rescue” strategy that (1) starts by cooperating, (2) sustains cooperation when the group last met the threshold, (3) tries to “rescue” the threshold when one extra cooperator could tip it over, and (4) otherwise defects to avoid wasted contributions when success is impossible. 

1.  State variables you observe each round t>1:  
    • prev_C = number of players (including you) who cooperated in round t–1  
    • gap    = m – prev_C  

2.  First round (t = 1):  
    Cooperate.

3.  For each subsequent round t = 2…r:  
    if prev_C ≥ m then  
       // threshold was met last round → trust maintained  
       play C  
    else  
       // threshold failed last round  
       if gap == 1 then  
          // your single C could rescue success  
          play C  
       else  
          // too many defectors to rescue with just you  
          play D  
       end  
    end  

4.  Last round (t = r):  
    Apply the same rule.  (Optionally, if you want to “cash out,” you could always defect in the final round—this is the only purely self‐interested tweak.)

Pseudocode  

```
function chooseAction(round t, prev_C):
    if t == 1:
        return C

    gap = m – prev_C

    if prev_C >= m:
        // last round was a group success
        return C
    else:
        // last round failed
        if gap == 1:
            // my single cooperation can tip it over
            return C
        else:
            // not enough cooperators even if I join
            return D
        end
    end
```

Why this is cooperative  
- You always start by cooperating, signaling goodwill.  
- Whenever the group succeeded in the previous round (prev_C ≥ m), you keep cooperating—this rewards cooperators and stabilizes cooperation.  
- If the group just missed the threshold by exactly one cooperator (gap=1), you jump in to “rescue” the public good—this makes the strategy responsive to near‐misses and encourages group success.  
- If the group missed by more than one, your lone C is wasted—so you defect to conserve your endowment (rational self‐interest in hopeless cases).  

This rule is fully deterministic, requires only observing the count of past cooperators, and is robust to n, m, r, k. It balances a cooperative mindset (always salvage success when you can) with protection against exploitation (don’t pour your endowment into impossible rescues).
'''

description_COOPERATIVE_72 = '''
Below is a single‐strategy “cooperative scheduling” approach.  It guarantees exactly m cooperators every round (so the threshold is always met), divides the cost of cooperation evenly, and reacts simply if someone breaks the plan.

1.  Overview  
   •  We divide the r rounds into a public, deterministic “cooperator‐set” schedule S₁,…,Sᵣ.  
   •  In round t exactly the m players in Sₜ play C, the rest play D.  Since |Sₜ|=m, the threshold is always met and everyone earns k (plus 1 if they defect that round).  
   •  Each player’s index i ∈ {1…n} is common knowledge, so everyone can compute the same Sₜ.  
   •  If in any round t′ the total number of C’s observed falls below m (i.e. someone deviated), all players defect in round t′+1 as a one‐round punishment, then immediately resume the original schedule for t′+2 onward.

2.  Public “rotation” schedule Sₜ  
   Fix an ordering of players 1,2,…,n.  For t=1…r define  
     BaseIndexₜ ≔ ((t−1)·m) mod n  
     Sₜ ≔ { ((BaseIndexₜ + j−1) mod n) +1  |  j=1…m }  
   Example: n=6, m=3  
     t=1: BaseIndex=0 → S₁={1,2,3}  
     t=2: BaseIndex=3 → S₂={4,5,6}  
     t=3: BaseIndex=0 → S₃={1,2,3}  … etc.

3.  Decision rule for player i in round t  
   State variables (shared by all):  
     – punished_round: the round in which a punishment D‐block is scheduled (initially = ∅)  
   Before choosing in round t:  
     if t==punished_round then  
       play D  
     else  
       if i ∈ Sₜ then play C else play D  

   After observing everyone’s actions in round t:  
     let coop_count = number of C’s observed.  
     if coop_count < m and punished_round < t+1 ≤ r then  
       punished_round = t+1  

4.  Edge‐case handling  
   •  First round (t=1): punished_round=∅ so we use the schedule S₁ as above.  
   •  A single‐round defection automatically triggers exactly one round of group defection next round (punishment), after which we return to our rotating schedule unconditionally.  
   •  Last round (t=r): We still apply the schedule Sᵣ (exactly m cooperators) unless it was designated as punished_round; if t=r is punished we just defect.  In either case the threshold is met in Sᵣ so the public project succeeds.  

5.  Properties  
   – Always meets the threshold except in the one round immediately after a deviation, punishing the entire group for one round.  
   – Shares the cost of cooperation evenly: over any full “cycle” of length n/m (when m divides n), each player cooperates exactly the same number of times.  
   – Simple to compute, no private memory beyond “punished_round.”  
   – If everyone follows it, the total payoff per round for a cooperator is k and for a defector is k+1, but by rotating you never let anyone hoard all the defects.  

Pseudocode  
```
Input: n, m, r;  // common knowledge
State: punished_round ← ∅

function BaseIndex(t):
    return ((t - 1) * m) mod n

function InSchedule(i, t):
    b ← BaseIndex(t)
    // The m indices are b+1, b+2, …, b+m (mod n)
    for j in 1…m:
        if ((b + j - 1) mod n) + 1 == i:
            return true
    return false

for t in 1…r:
    // 1) Choose action
    if t == punished_round:
        action_i ← D
    else if InSchedule(i, t):
        action_i ← C
    else:
        action_i ← D

    // 2) Observe all actions, count cooperators
    coop_count ← number of players choosing C in round t

    // 3) If threshold failed, schedule next‐round punishment
    if coop_count < m and t+1 ≤ r:
        punished_round ← t+1

    // Record π_i,t in your logs if you like
end for
```

This “rotating‐cooperation with one‐round group punishment” strategy is fully cooperative (always aims to meet the public‐goods threshold), fair in cost‐sharing, and robust to a single defection.
'''

description_COOPERATIVE_73 = '''
Below is a single‐strategy outline, which we’ll call “Threshold‐Tit‐for‐Tat with One‐Turn Forgiveness.”  It is designed to (1) cooperate whenever the group met the m-threshold last round, (2) punish a failure by defecting exactly once, then forgive, and (3) defect in the last round to avoid end-game exploitation.

1. State variables  
   • punishing (boolean), initially false  
   • coop_prev (integer): number of cooperators in the previous round  

2. Initialization  
   • Round 1: cooperate (C).  
   • Set punishing ← false.  

3. In each round t = 2,3,…,r:  
   if t = r (the last round) then  
     • Play Defect (D) and stop.  
   else if punishing = true then  
     • Play Cooperate (C)  
     • Set punishing ← false  
   else if coop_prev ≥ m then  
     • Play Cooperate (C)  
   else  
     • Play Defect (D)  
     • Set punishing ← true  

4. After each round t, observe how many players cooperated this round; store that number in coop_prev for use in round t+1.

Pseudocode

```
initialize:
  punishing ← false
  coop_prev ← 0    # undefined before round 1

for t in 1..r:
  if t == 1:
    action ← C
  else if t == r:
    action ← D
  else if punishing == true:
    action ← C
    punishing ← false
  else if coop_prev ≥ m:
    action ← C
  else:
    action ← D
    punishing ← true

  play(action)

  # after play, count how many of the n players chose C this round
  coop_prev ← observed number of C’s
```

Rationale  
• First round: Open with cooperation to signal cooperative intent.  
• Middle rounds:  
  – If last round met the threshold (coop_prev ≥ m), the group averted risk, so we repeat C.  
  – If it failed (coop_prev < m), we defect once as a “punishment” to discourage free‐riding, then immediately forgive so as not to spiral into permanent defection.  
• Last round: Defect, since there is no future in which to punish us, and defection strictly dominates cooperation in the final round.  

This strategy is cooperative—always ready to contribute when the group is meeting the public‐good threshold—but also enforces a mild, one‐turn penalty whenever the group as a whole fails to cooperate.
'''

description_COOPERATIVE_74 = '''
Below is a single‐strategy proposal, call it “Forgiving Threshold‐Tit‐for‐Tat” (FTFT).  It is simple, fully specified, punishes defections only once, then immediately returns to cooperation if the group rebuilds.  It never “goes rogue” or permanently defects, so it supports and stabilizes collective cooperation.

———  
1. Overview of the FTFT Strategy  
   • First move: Cooperate.  
   • Thereafter:  
     – If last round’s cooperators ≥ m (“project succeeded”), cooperate.  
     – If last round’s cooperators < m (“project failed”) and you have not yet punished for that failure, defect once.  
     – Otherwise (you already punished), cooperate.  
   • Last round: Follow the same rule (you may punish once if the project fails in round r–1).  

2. Why it is Cooperative  
   – It always starts by offering to meet the threshold.  
   – It never permanently defects: just one round of punishment after any failure, then immediate return to cooperation.  
   – It thereby creates a clear, low-cost incentive for the group to rally back above the threshold.  

3. Pseudocode  

```
Inputs (common knowledge):
  n   – number of players
  r   – total rounds
  m   – cooperation threshold
  k   – reward factor

State variables (for our player):
  inPunishment ← false    // “am I about to punish a previous failure?”

For each round t = 1 … r do:
  if t == 1 then
    action ← C            // first‐round cooperation
  else
    if inPunishment then
      // we are serving our one‐round punishment
      action ← D
      inPunishment ← false
    else
      let lastCoops = number of cooperators observed in round (t−1)
      if lastCoops < m then
        // group failed threshold, trigger one round of punishment
        action ← D
        inPunishment ← true
      else
        // group succeeded last round
        action ← C
      end if
    end if
  end if

  // (Optional) Logging for next round:
  record action
  // opponents’ actions and payoffs in this round will be known for next iteration
end for
```

4. Handling Edge Cases  
  • First round (t=1): no history ⇒ cooperate.  
  • Immediate failure in round 1 ⇒ in round 2 you punish exactly once, then revert.  
  • Multiple consecutive failures ⇒ you punish once after the first failure, then resume cooperation; if the group fails again later, you punish that new failure once, etc.  
  • Last round (t=r): you apply the same rule. If round r−1 failed, you defect in round r as your single punishment. Otherwise you cooperate in round r.  

5. Variations / Tuning  
  – You can choose to always cooperate in the final round (i.e. ignore any “last‐round punishment”) if you believe your single‐round punishment is worth a lost final payoff.  
  – You could lengthen punishment to two rounds for severe unreliability.  But one‐round is enough to signal “please get back to ≥ m” without collapsing cooperation.  

6. Strategic Rationale  
  – By starting cooperatively and forgiving immediately, FTFT avoids long “war of attrition.”  
  – By punishing once, it prevents free‐riding from becoming too cheap.  
  – Over r rounds, this breeds repeated successes (≥ m cooperators), maximizing everyone’s (including your own) total payoff.
'''

description_COOPERATIVE_75 = '''
Below is a “Threshold Tit‐for‐Tat with Forgiveness” strategy.  It is designed to sustain cooperation whenever possible, punish short‐term breakdowns just long enough to deter free‐riding, and gracefully handle first-round and last-round edge cases.

1.  Definitions and state  
   •  t = current round (1 ≤ t ≤ r)  
   •  coopₜ = number of players (including you) who chose C in round t  
   •  P = remaining punishment rounds (initially 0)  

2.  High‐level idea  
   – Start cooperative.  
   – In each interior round, if in the previous round the group met the threshold (coopₜ₋₁ ≥ m), keep cooperating.  
   – If the threshold failed last round (coopₜ₋₁ < m), defect for exactly one round (P=1) then forgive and return to cooperation.  
   – Always defect in the final round (t=r) to avoid being exploited in the known “last move.”  

3.  Full decision rules  

Pseudocode:  
```
Initialize P ← 0

For t in 1…r:
  If t == 1:
    action ← C
  
  Else if t == r:
    # Last round: defection is dominant
    action ← D

  Else if P > 0:
    # We are punishing for a previous threshold‐failure
    action ← D
    P ← P − 1

  Else:
    # No active punishment
    If coop_{t-1} ≥ m:
      # Last round succeeded ⇒ reward cooperation
      action ← C
    Else
      # Threshold failed ⇒ punish once
      action ← D
      P ← 1
    EndIf
  EndIf

  Play(action)
EndFor
```

4.  Explanation of each rule  
 – First round (t=1): Cooperate to signal goodwill.  
 – Interior rounds (1 < t < r):  
   • If you’re in punishment mode (P>0), defect and decrement P.  
   • Otherwise look at last period’s outcome:  
     – If at least m cooperated, the group successfully averted risk ⇒ continue cooperating.  
     – If fewer than m cooperated, someone “broke the pact,” so defect exactly one round (P←1) as a short‐run penalty.  
 – Last round (t=r): Defect.  In a finite horizon game, cooperation cannot be enforced on the final move, so we defect to avoid being exploited.  

5.  Why this is cooperative  
 – You always start by cooperating.  
 – You punish only the round immediately following a failure to reach the threshold, then return to cooperation—this “tit for tat + forgiveness” fosters a norm of mutual support.  
 – As long as the group maintains the threshold every round, you will too.  
 – By punishing only one round, you keep the cooperative phase robust against occasional mistakes.  

6.  Handling edge cases  
 – If the group ever slips below the threshold two rounds in a row, you will punish twice in a row (once per failure), but then resume cooperation.  
 – If r=2, you cooperate in round 1, then defect in round 2.  This still maximizes your payoff given the known last move.  
 – If your opponents stick to this strategy, the profile will settle quickly into full cooperation for rounds 1 through r–1 and mutual defection only in round r.
'''

description_COOPERATIVE_76 = '''
Below is a single‐strategy prescription (“One‐Shot Punishment with Quick Forgiveness”) that (a) tries to secure the threshold m every round via mutual cooperation, (b) punishes any failure just once to deter free‐riding, then (c) returns immediately to cooperation.

1. State and memory  
   We keep in memory:  
   • coop_count_prev = number of players who chose C in the previous round  
   • punish_rounds_left = how many consecutive rounds of “punish” (i.e. defect) remain  

2. Initialization  
   At round t = 1:  
     • coop_count_prev = –  (undefined)  
     • punish_rounds_left = 0  

3. Decision rule for round t  
   if t == 1:  
     play C  
   else if punish_rounds_left > 0:  
     play D  
     punish_rounds_left ← punish_rounds_left – 1  
   else if coop_count_prev ≥ m:  
     play C  
   else  (i.e. last round failed to reach m)  
     play D               ← “punish the group for one round”  
     punish_rounds_left ← 1  

4. Update memory after observing all actions in round t  
   coop_count_prev ← number of players who played C in round t  

5. Edge‐case handling  
   • First round (t=1): no history → we default to C to signal willingness to cooperate.  
   • Immediately after any round in which fewer than m cooperators appeared, we defect exactly once as a group‐level punishment.  
   • After that single “punish” round, regardless of outcome, we reset punish_rounds_left=0 and return to full cooperation in the next round.  
   • Last round (t=r): we use exactly the same rule. If we are in a punishment round we defect; otherwise we cooperate if the previous round hit the threshold.  

6. Why it’s cooperative  
   – It starts by cooperating and returns as quickly as possible to cooperation.  
   – The single‐round punishment creates a small cost to anyone who free‐rides (causes threshold failure), discouraging under‐contribution.  
   – Forgiving immediately after one round of punishment prevents endless deadlocks and sustains cooperation over long sequences.  

Pseudocode summary  
```
initialize:
  punish_rounds_left ← 0
  coop_count_prev ← –1

for t in 1..r:
  if t == 1:
    action_t ← C
  else if punish_rounds_left > 0:
    action_t ← D
    punish_rounds_left ← punish_rounds_left – 1
  else if coop_count_prev ≥ m:
    action_t ← C
  else:
    action_t ← D
    punish_rounds_left ← 1

  observe all players’ actions this round
  coop_count_prev ← count_of_C_this_round
  record payoff for this round
end for
```
'''

description_COOPERATIVE_77 = '''
Below is a fully specified “rotating‐coordinator with grim trigger” strategy.  Its goals are (a) every round to get exactly m cooperators (so the threshold is met with no wasted contributors), (b) share the burden of cooperating evenly, and (c) punish any deviation by switching to all‐defect for the rest of the game.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Common Knowledge    
   •  All players know n, m, r, k and each other’s index i∈{1…n}.  
   •  No side‐communication; every action is observed each round.  

2.  High‐Level Idea    
   We carve the r rounds into a rotational schedule so that in each round t exactly m distinct players are “on duty” to cooperate.  If anyone ever violates the schedule (i.e. cooperates or defects out of turn) or the threshold fails, we switch into permanent punishment (all‐D forever).  

3.  Notation    
   Let t be the current round (1,…,r).  
   Let phase ∈ {COOP, PUNISH}.  Initially phase=COOP.  

4.  Determining the m “Scheduled Cooperators” each round    
   We number players 1…n.  In round t we take the next m players in cyclic order, starting from index ((t–1) mod n)+1.  Precisely:  
     S_t  =  {  ((t–1) mod n)+1,  ((t–1) mod n)+2, …, ((t–1) mod n)+m }  all taken mod n (wrapping 1…n).  

   Example: n=6, m=3  
     t=1 ⇒ start at 1 ⇒ S₁={1,2,3}  
     t=2 ⇒ start at 2 ⇒ S₂={2,3,4}  
     t=3 ⇒ start at 3 ⇒ S₃={3,4,5}  
     … and so on, wrapping around.

5.  Round‐by‐round decision rule (for player i)  
   if phase = PUNISH  
     play D  
   else  (phase = COOP)  
     if i ∈ S_t  
       play C  
     else  
       play D  

6.  After each round t, update phase  
   •  Observe the full profile of actions and count cooperators: ActualSet = {j | j played C}.  
   •  if phase=COOP and ActualSet ≠ S_t  (i.e. someone defected when scheduled or somebody extra cooperated)  
        phase ← PUNISH  
   •  otherwise keep phase as is  

7.  Edge‐Cases and Comments  
  a)  First round (t=1):  S₁={1…m}, so players 1…m start by cooperating; the rest defect.  
  b)  Last round (t=r):  apply the same rule.  Even though in a strict finite‐horizon backward induction one might be tempted to deviate in round r, our grim‐trigger promise (that any deviation is punished by all‐D thereafter) still deters deviations in practice as soon as r is large enough or opponents respect the threat.  
  c)  If at any t the number of cooperators falls below m, everybody immediately switches to permanent defection—even if by a single mistake the threshold is lost, the game reverts to all‐D.  

8.  Why it is cooperative  
  •  In every COOP round exactly m players contribute, so the public good is produced each round, earning +k for everyone.  
  •  The duty to contribute rotates evenly, so no one bears the cost disproportionately.  
  •  Grim trigger ensures no one can gain by deviating: a “would‐be freerider” in a scheduled‐defector slot risks being detected and triggering permanent all‐D, losing all future k‐bonuses.  A scheduled cooperator who defects loses the k‐bonus that round and also triggers punishment.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode for player i:

initialize phase ← COOP

for t in 1…r do
  if phase = PUNISH then
    action_i ← D
  else
    compute startIndex ← ((t–1) mod n) + 1
    build S_t ← { startIndex, startIndex+1, …, startIndex+m–1 } mod n
    if i ∈ S_t then action_i ← C else action_i ← D
  end if

  play(action_i)
  observe all actions ⇒ ActualSet
  if phase = COOP and ActualSet ≠ S_t then
    phase ← PUNISH
  end if
end for

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

This strategy guarantees threshold success every cooperative round, shares cost fairly, and enforces compliance via a clear grim‐trigger punishment.
'''

description_COOPERATIVE_78 = '''
Below is a single‐strategy recipe that (i) opens with cooperation, (ii) punishes any “group failure” just enough to deter unilateral defection, (iii) forgives quickly so that the group can re‐coordinate, and (iv) in the last round uses the same rule (so it does not “pre‐commit” to defecting).  Informally it is a “threshold‐trigger with one‐round punishment.”

------------------------------------------------------------------------------------------------  
1. State variables  
   • punish_counter ∈ {0,1,…}  (initially 0)  
   • last_round = r  

2. At each round t = 1,…,r do the following:

   if t == 1 then  
       play C  
       continue to next round  
   end if

   if punish_counter > 0 then  
       play D  
       punish_counter ← punish_counter − 1  
       continue to next round  
   end if

   let coop_prev = number of players (including yourself) who chose C in round t–1  

   if coop_prev ≥ m then  
       /*  Success last round: threshold was met  */  
       play C  
   else  
       /*  Failure last round: too few cooperators  */  
       play D  
       punish_counter ← 1    /* punish for exactly one round  */  
   end if

3. End of game.  
   Total payoff is the sum of per‐round π_i as specified.

------------------------------------------------------------------------------------------------  
Explanation of key points:

• First round (t=1): we cooperate to signal willingness to meet the threshold.  
• “Success” condition (coop_prev ≥ m): we believe the group can hit the target, so we keep cooperating.  
• “Failure” condition (coop_prev < m): someone defected (or there was bad coordination).  We defect this round to punish, but only for one round.  That single‐round punishment deters gratuitous defection but does not collapse cooperation permanently.  
• Forgiveness: punish_counter is reset to zero after one round of D, so if the group pulls itself up, we immediately return to cooperation.  
• Last round (t=r): no special case—if the previous round reached the threshold, we cooperate; otherwise we defect this round (as per the rule).  This keeps the rule uniform and transparent.  

This strategy quickly re‐establishes cooperation after any slip, maintains the public‐good threshold if a majority are willing, and deters unilateral defection by imposing a brief cost.
'''

description_COOPERATIVE_79 = '''
Below is a single‐strategy description (“Conditional Cooperator with One‐Round Punishment”) that (i) tries to coordinate m cooperators every round, (ii) punishes any collective failure exactly one round, then immediately returns to cooperation, and (iii) handles the first and last rounds explicitly.

1. Data structures / state  
   • punish_next (Boolean), initially false.  
   • You observe in each past round t the total number of cooperators, coop_count[t].

2. Decision rule for round t:  
   if t == 1 then  
     • Action = C  
     • punish_next ← false  
     return Action  
   end  
   if t == r then  
     • Action = D      // Last round defection is dominant  
     return Action  
   end  
   if punish_next == true then  
     // We are serving our one‐round punishment  
     Action = C  
     punish_next ← false  
     return Action  
   end  
   // Otherwise, look at what happened in t−1  
   if coop_count[t−1] < m then  
     // The group failed to reach the threshold last round → punish once  
     Action = D  
     punish_next ← true  
   else  
     // Threshold met last round → continue cooperating  
     Action = C  
   end  
   return Action  

3. Intuition / walk‐through  
 • First round (t=1): cooperate to signal willingness and try to get ≥m cooperators.  
 • Rounds 2…r−1:  
     – If the group succeeded last round (coop_count ≥ m), keep cooperating.  
     – If the group failed last round (coop_count < m), defect this round (punish), but then immediately clear the punishment flag and go back to cooperation.  
 • Round r: defect (no future incentives remain).  

4. Why it promotes cooperation  
 • As long as everyone follows it, the group will successfully cooperate round after round (since no one triggers punish_next), giving each player payoff k−1 every round up to t=r−1.  
 • A single “mistake” (too few cooperators) triggers exactly one round of universal defection, imposing a cost on every player, but then allows recovery. That finite punishment deters persistent free‐riding but remains forgiving—cooperation can resume.  
 • Defecting in the final round is individually optimal and common‐knowledge, so we do not try to cooperate at t=r and thus avoid being exploited in the truly last move.  

5. Edge‐case check  
 • If the group never hits the threshold in t=1, everyone defects in t=2, then cooperates again in t=3 trying to recover.  
 • If two failures occur in a row, the punish_next flag is raised twice, so you defect in the first punishment, cooperate in the next, then immediately defect again (because the second failure re-triggered punish_next), etc.—guaranteeing exactly one defection per failure.  
 • If for some reason coop_count[t−1] ≥ m but you personally think someone is systematically betraying, this strategy does not single out individuals—it punishes the group equally but remains simple and transparent.  

This “one‐round punishment then immediate forgiveness” rule is a well-known variant of win-stay/lose-shift adapted to threshold public‐goods. It is fully cooperative (strives for threshold each round), credible (punishments are finite and predictable), and handles the finite horizon correctly (defection in the last round).
'''

description_COOPERATIVE_80 = '''
Below is a single‐player “conditional‐cooperator with one‐round punishment” strategy.  It is designed to (1) start cooperatively, (2) punish free‐riding or collective failures for exactly one round, (3) then forgive and return to cooperation, and (4) always attempt to cooperate even in the last round in order to maximize group payoffs.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  State variables  
   •  PunsLeft ∈ {0,1,…}  – number of remaining punishment rounds (initially 0)  
   •  lastActions = record of play in round t–1 (both your own action and total #C)  

2.  High-level logic  
   For each round t = 1…r:  
     1.  If PunsLeft > 0, then “punish” by Defect, decrement PunsLeft.  
     2.  Else if t == 1, Cooperate.  
     3.  Else (t > 1 and no punishment pending):  
          a.  Look at last round’s outcome:  
              •  totalC = number of cooperators in t–1  
              •  myLast = your action in t–1  
          b.  If totalC ≥ m (threshold met):  
                – If you defected last round (myLast = D), set PunsLeft := 1 and play D  
                  (punish yourself for free‐riding)  
                – Else play C  
          c.  If totalC < m (failure to reach threshold), set PunsLeft := 1 and play D  
             (punish the group for failing to avert the risk)  
     4.  (Optional override) If t == r you may still choose C to give “one last push”  
         for the public good even though standard backward induction would predict D.  

3.  Detailed pseudocode  

  initialize:  
    PunsLeft ← 0  
    lastActions ← none  

  for t in 1…r do  
    if PunsLeft > 0 then  
      action ← D  
      PunsLeft ← PunsLeft − 1  
    else if t == 1 then  
      action ← C  
    else  
      let totalC ← lastActions.totalCooperators  
      let myLast ← lastActions.myAction  
      if totalC ≥ m then  
        if myLast == D then  
          PunsLeft ← 1      # punish free-riding once  
          action ← D  
        else  
          action ← C        # mutual reward for cooperation  
      else                # threshold failure  
        PunsLeft ← 1      # punish the group once  
        action ← D  
      end if  
    end if

    # Optional: override last‐round logic to cooperate in the final round  
    if t == r then  
      action ← C  
    end if

    play(action)  
    observe others’ actions; update lastActions  

  end for  

4.  Explanation of cooperative mindset  
  •  We begin by trusting the group (C in round 1).  
  •  When the group reaches the threshold, we return that trust by continuing to cooperate.  
  •  We do not hold grudges forever—any punishment for free‐riding or collective failure lasts exactly one round, then we forgive and go back to C.  
  •  By cooperating in the last round, we signal a genuine commitment to the public good at all stages, maximizing the chance that other cooperators also stick with C right to the end.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy fosters high levels of cooperation, enforces accountability for both free-riding and group failures, and uses limited (one-round) punishment to avoid collapse into permanent mutual defection.
'''

description_COOPERATIVE_81 = '''
Below is a single‐strategy (“Threshold–Forgiver”) intended to sustain cooperation on the m‐threshold game over r rounds.  It punishes any failure to reach the threshold by defecting exactly one round, then forgives.  If the threshold is met, it always cooperates.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Name  
  Threshold–Forgiver

State Variables  
  punish_next_round ∈ {True, False}  
    – initialized to False  
  last_round_coops_met_threshold ∈ {True, False}  
    – initialized to True (we start “optimistic”)

Decision Rules  
  For each round t = 1,2,…,r do:  
    if t == 1 then  
      action := C  
    else if punish_next_round then  
      action := D  
    else  
      action := C  
    end  

  (“C” = contribute; “D” = keep.)

After all n moves are revealed in round t:  
  Let num_C := number of players who played C this round.  
  if num_C < m then  
    last_round_coops_met_threshold := False  
    punish_next_round := True        # one‐round punishment  
  else  
    last_round_coops_met_threshold := True  
    punish_next_round := False  
  end  

Edge Cases  
  – First round: we cooperate unconditionally to jump‐start the public good.  
  – When the threshold fails, we defect exactly once to “bite” free‐riders, then automatically return to cooperation even if the threshold again fails.  
  – Last round: the same rule applies.  If we are in a punish state we defect; otherwise we cooperate.  (Any attempt at extra punishment beyond one round is useless in the last round, so this keeps the rule uniform.)

Rationale  
  1. By always starting with C, we signal willingness to cooperate.  
  2. Failing to reach m cooperators is met with a single‐round defection.  This makes defection costly: anyone who drives the group below m triggers a small penalty on themselves next round.  
  3. Forgiveness after one round prevents endless mutual retaliation if the group oscillates around the threshold or if the failure was accidental.  
  4. The rule is entirely deterministic, requires only one bit of memory (“punish_next_round”), and is common‐knowledge.  It rewards groups that manage m or more cooperators each round with continuous cooperation, sustaining the bonus k every round.

Pseudocode Summary  
  initialize punish_next_round ← False  
  for t in 1…r:  
    if t==1 or punish_next_round==False then  
      play C  
    else  
      play D  
    end  
    observe num_C this round  
    if num_C < m then  
      punish_next_round ← True  
    else  
      punish_next_round ← False  
    end  
  end

This strategy is cooperative—it maximizes group payoffs so long as at least m players use similar rules—yet it credibly punishes threshold violations just long enough to discourage free‐riding.
'''

description_COOPERATIVE_82 = '''
Below is a “rotating‐cooperator with grim‐trigger” strategy.  It (1) ensures exactly m players contribute each round (so the threshold is always met if no one deviates), (2) divides the burden of contributing evenly over all r rounds, and (3) punishes any deviation by defecting for the rest of the game.

––––––––––––––––––––––––––––––––––––––––––––  
1. PRECOMPUTE A ROTATION SCHEDULE  
––––––––––––––––––––––––––––––––––––––––––––  
Define for each round t=1…r the set S[t] of exactly m players who “should” cooperate in that round.  We take a simple cyclic ordering of the n players:

  Let players be numbered 1,2,…,n.  
  For t=1 to r:
    startIndex ← ((t−1)*m mod n) + 1  
    S[t] ← { startIndex, startIndex+1, …, startIndex+(m−1) }  
      (all indices taken modulo n, interpreted in {1,…,n})

Example (n=6, m=2, r=5):  
  t=1: startIndex=1 ⇒ S[1]={1,2}  
  t=2: startIndex=3 ⇒ S[2]={3,4}  
  t=3: startIndex=5 ⇒ S[3]={5,6}  
  t=4: startIndex=1 ⇒ S[4]={1,2}  
  t=5: startIndex=3 ⇒ S[5]={3,4}

Each player appears in exactly (m*r)/n rounds (or ±1 if it does not divide evenly).

––––––––––––––––––––––––––––––––––––––––––––  
2. GRIM‐TRIGGER PUNISHMENT  
––––––––––––––––––––––––––––––––––––––––––––  
Maintain a Boolean flag “Triggered” initially false.  
After each round, if fewer than m cooperators were observed, set Triggered←true.  Once Triggered is true you defect in every remaining round.

––––––––––––––––––––––––––––––––––––––––––––  
3. DECISION RULE (PSEUDOCODE FOR PLAYER i)  
––––––––––––––––––––––––––––––––––––––––––––  

Initialize: Triggered ← false

For t from 1 to r do  
  if Triggered = true then  
    play D  
  else  
    if i ∈ S[t] then play C else play D  
  end if

  Observe total cooperators this round, c_count  
  if c_count < m then  
    Triggered ← true  
  end if  
end for

––––––––––––––––––––––––––––––––––––––––––––  
4. WHY THIS IS COOPERATIVE  
––––––––––––––––––––––––––––––––––––––––––––  
•  If everyone follows it exactly:  
   – Every round exactly m players cooperate ⇒ threshold met ⇒ all earn k plus private shares.  
   – Each player’s personal number of contributions is balanced across r rounds.  
•  A single scheduled cooperator who defects causes that round to fall below m (since unscheduled players stay D).  This both denies reward to everyone and triggers permanent defection—so the one defector sacrifices all future k’s.  
•  Likewise, an unscheduled player who “extra‐cooperates” merely pays cost for no additional group benefit (threshold was already met by S[t]).  That player would prefer to defect next time.

––––––––––––––––––––––––––––––––––––––––––––  
5. EDGE CASES  
––––––––––––––––––––––––––––––––––––––––––––  
• First round: Triggered=false, follow S[1].  
• Last round: same rule applies—no special end‐game deviation because if you are scheduled and cooperate you ensure the k payoff; if you deviate you destroy the threshold (since exactly m are scheduled to cooperate) and lose more.  
• If the schedule (n, m, r) does not divide evenly, some players will contribute one extra time.  That is the fairest division possible given the integer constraints.  

––––––––––––––––––––––––––––––––––––––––––––  
This strategy is fully cooperative: it guarantees the public good every round when all comply, divides costs fairly, and credibly punishes any defection by jettisoning cooperation forever (grim trigger).
'''

description_COOPERATIVE_83 = '''
Below is a single‐strategy description—call it “Threshold‐Reciprocal with One‐Round Punishment”—that (1) starts out cooperative, (2) sustains threshold cooperation whenever possible, (3) punishes free‐riders by one round of defection, (4) falls back to defection when the risk materializes (i.e. threshold missed), and (5) handles first and last rounds.

——————  
Strategy name  
    Threshold‐Reciprocal with One‐Round Punishment

Parameters it uses internally  
    m       // threshold of cooperators needed  
    r       // total rounds  

State variables  
    punishing ← false  

Decision rules for round t (1 ≤ t ≤ r)  

1. If t = 1 (first round):  
       play C  

2. Else if t = r (last round):  
       // No future to enforce cooperation  
       play D  

3. Else if punishing = true:  
       // We are in the middle of a one‐round group punishment  
       punishing ← false  
       play D  

4. Else look at the previous round’s total cooperators, coop_prev:  

   a. If coop_prev < m:  
          // Risk materialized—too few cooperators, public project failed last round  
          play D  
   
   b. Else // coop_prev ≥ m, public good succeeded last round  
     
       i. If coop_prev = n:  
             // Everyone cooperated last round—no free‐rider to punish  
             play C  
     
      ii. Else // m ≤ coop_prev < n: at least one player defected yet the project still succeeded  
             // Trigger a one‐round group punishment  
             punishing ← true  
             play D  

——————  
Pseudocode  

    initialize punishing ← false

    for t in 1…r:
        if t == 1:
            action[t] ← C
            continue
        if t == r:
            action[t] ← D
            continue
        if punishing:
            punishing ← false
            action[t] ← D
            continue

        // look up how many cooperated in round t–1
        coop_prev ← number_of_C_in_round(t–1)

        if coop_prev < m:
            // failure last round ⇒ defect
            action[t] ← D
        else:
            // success last round
            if coop_prev == n:
                // everyone played C ⇒ keep cooperating
                action[t] ← C
            else:
                // at least one defector free‐rode ⇒ punish once
                punishing ← true
                action[t] ← D

    end for

——————  
Why this works as a cooperative strategy  

• First round cooperation (“trust‐building”).  
• As long as the project keeps succeeding without free‐riders, we keep cooperating—this ensures we hit the threshold m each round, unlocking the +k payoff.  
• If the threshold fails (coop_prev < m), we switch to defection that round to avoid wasting the 1‐unit contribution. This is “win–stay/lose–shift” at the group level.  
• If the threshold succeeds but some players defected (m ≤ coop_prev < n), we impose a one‐round group punishment (all defect) to deter free‐riding. After that single punishment round, we return to cooperation steps.  
• In the last round we defect, since there is no future to influence.  

This strategy is cooperative—it sustains threshold‐meeting contributions whenever possible, and uses the minimal necessary punishment to keep everyone honest.
'''

description_COOPERATIVE_84 = '''
Here is a simple, fully-specified “forgiving conditional cooperator” that (i) tries to guarantee the public good each round, (ii) punishes one round when it sees free-riding, (iii) forgives quickly, and (iv) defects only in the very last round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Parameters you set once at the start  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
n   – number of players  
r   – total rounds  
m   – threshold of cooperators needed each round (1 < m < n)  
k   – public‐good reward factor (k > 1)  

Fixed strategy constants  
L = 1       – length of punishment (in rounds) after observing any free‐rider  
E = 1       – number of endgame rounds in which we defect unconditionally (the “last‐round defection”)  

State variables (per strategy instance)  
punish_timer ← 0      – counts how many more rounds we will defect to punish  
prev_cooperators ← n  – number of cooperators we observed in the previous round  
prev_round     ← 0    – index of the previous round (0 before the game starts)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
High‐level idea  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Round 1: cooperate.  
2. In any “endgame” round t > r–E, defect (no future to enforce cooperation).  
3. If we are in a punishment phase (punish_timer > 0), defect and decrement punish_timer.  
4. Otherwise look at last round’s outcome:  
   a. If last round had ≥ m cooperators and yet at least one defector, punish exactly L rounds (defect) then forgive.  
   b. If last round had ≥ m cooperators and nobody defected, keep cooperating.  
   c. If last round had < m cooperators (public good failed), switch back to cooperate immediately to try to re-establish the threshold.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Initialize before round 1:  
  punish_timer ← 0  
  prev_cooperators ← n      // assume “full cooperation” before start  
  
For t in 1..r do:  
  if t > r – E then  
    action ← D              // last‐round defection  
  
  else if punish_timer > 0 then  
    action ← D              // continue punishing  
    punish_timer ← punish_timer – 1  
  
  else if t == 1 then  
    action ← C              // start cooperatively  
  
  else  
    // inspect last round’s count of cooperators  
    if prev_cooperators ≥ m then  
      if prev_cooperators < n then  
        // threshold met but some defectors: punish them  
        action ← D  
        punish_timer ← L     // punish next L rounds  
      else  
        // unanimous cooperation success: continue cooperating  
        action ← C  
    else  
      // public good failed last round: try to re-build cooperation  
      action ← C  
  
  // play 'action' this round and observe all players’ moves:  
  Broadcast action, observe everyone’s choices this round.  
  prev_cooperators ← number of players who chose C in round t  
  prev_round ← t  
  
End for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Why this works  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• It always tries to meet the m-cooperator threshold by cooperating after any failure.  
• It punishes free-riding immediately but only briefly (L=1), so single defectors are swiftly disciplined yet the group quickly returns to cooperation.  
• By defecting in the final round (E=1), it respects backward‐induction (no future to enforce cooperation).  
• It never punish‐forever; it is forgiving, so if others return to cooperation you do too.  

You can adjust L (punishment length) or E (endgame length) if you find different calibration works better in your tournament.
'''

description_COOPERATIVE_85 = '''
Below is a simple, fully-specified “punish-and-recover” strategy that (1) tries to get the group over the m-cooperator threshold every round, (2) punishes a failure exactly one round, then (3) returns immediately to cooperation.  It cooperates on the very first round (no history), and on the last round it behaves exactly as on any other round—this simplicity helps stabilize cooperation right up to the end.

––––––––––––––––––––––––––––––––  
Strategy name:  Punish-and-Recover (P&R)

State variables (maintained across rounds)  
  punished_rounds_remaining ∈ {0,1,…}  ← initially 0  

Parameters  
  P = 1   (length of punishment after a threshold failure)  

Decision rule for each round t = 1,2,…,r:  
  if punished_rounds_remaining > 0 then  
    play D  
    punished_rounds_remaining ← punished_rounds_remaining − 1  
  else  
    play C  

After all players’ moves in round t are revealed, compute  
  coop_count = number of players who played C in t  
  if coop_count < m then  
    punished_rounds_remaining ← P   # schedule exactly one round of punishment  

Repeat until t = r.

––––––––––––––––––––––––––––––––  
Explanation  

1. First round  
   There is no history, so punished_rounds_remaining = 0 → you play C.  

2. Normal operation (no recent failure)  
   punished_rounds_remaining = 0 → you play C.  If all other players are using the same rule, and everyone cooperates, you will have at least m cooperators and earn the bonus k.  

3. Detecting a failure  
   As soon as any round ends with fewer than m cooperators, you enter a one-round punishment: next round you defect (punished_rounds_remaining = 1).  

4. Recovery after punishment  
   After defecting for exactly one round, punished_rounds_remaining falls back to zero, so you immediately resume cooperation.  This gives “second chances” rather than permanent breakdowns.  

5. Last round  
   The rule is uniform across all rounds, including t = r.  If you are not in punishment you play C; if you are in punishment you play D.  Because every failure is punished exactly one round later, there is still an incentive for the group to cooperate on rounds r–1 and r.  

––––––––––––––––––––––––––––––––  
Why this is cooperative  

• It starts by cooperating, and it returns to cooperation immediately after a single punishment round.  
• It only defects in order to discipline the group when the group as a whole has failed to contribute at least m times.  
• By keeping P small (here P = 1), it minimizes wasted rounds of defection yet still creates a credible cost to group failure.  
• It has no “end-of-game” deviation built in, so if all players use it honest cooperation up to the final round can be sustained.  

––––––––––––––––––––––––––––––––  
Pseudocode  

```
# Initialization
punished = 0

for t in 1..r:
    if punished > 0:
        action_i[t] = D
        punished -= 1
    else:
        action_i[t] = C

    # (after all players choose) Observe coop_count
    if coop_count < m:
        punished = 1
end
```
'''

description_COOPERATIVE_86 = '''
Below is a fully specified, “cooperative‐minded’’ rule for the repeated threshold public‐goods game.  In words it tries to ensure exactly m players contribute each round (nobody over–pays, nobody under–pays), it starts from cooperation, it punishes shortfalls gently, and it never “goes crazy’’ by defecting when cooperation is safe.  You can think of it as a “Threshold-Tac-for-Tat’’ that automatically free-rides whenever at least m others are cooperating, but steps in to fill the gap whenever cooperation dips below threshold.

1. State variables  
   • history of each past round t:  
     – C_count[t] = number of players (including you) who played C in round t  
     – my_action[t] ∈ {C,D}  
   • No further private randomness or secret flags are needed.

2. Initialization  
   Round‐1: play C.

3. Generic round t > 1 decision rule  
   Let  
     prev_C   = C_count[t−1]  
     prev_mine = 1 if my_action[t−1]==C else 0  
     others_prev = prev_C − prev_mine   (how many *other* players cooperated last round)  
   Now decide your action in round t:  
   
   If others_prev ≥ m       then  
       // Enough others are stepping up.  You can safely defect and free‐ride.  
       action = D  
   else  
       // Fewer than m others cooperated → risk of threshold failure → you must help.  
       action = C  

4. Edge‐cases and refinements  
   a. First round (t=1): we have no history, so we default to C.  
   b. Last round (t=r): we apply exactly the same rule.  
      Because we *always* step in if <m others cooperated, we still preserve the group benefit.  
   c. Punishment: there is no hard “grim” step.  If the group fails to reach m, each individual uses the same rule next round—so the group naturally returns to cooperation.  
   d. If opponents try to exploit (e.g. by never cooperating), you will keep playing C every round, but you also never allow the group return to failure—so at worst you get the one‐player payoff loss each round, but you maximize your honest attempt at cooperation.  

5. Why it is cooperative  
   • Whenever the group would fail (others_prev < m), you contribute to avert the failure.  
   • Whenever the group is safe (others_prev ≥ m), you back off and let exactly m players pay.  
   • It never defects for spite or out of end‐game paranoia.  
   • It provides immediate “forgiveness’’—no endless punishment if a single round fails.  

6. Pseudocode  

   initialize history list  
   for t in 1…r do  
     if t == 1 then  
       action ← C  
     else  
       prev_C    ← history[t−1].C_count  
       prev_mine ← (history[t−1].my_action == C ? 1 : 0)  
       others    ← prev_C − prev_mine  
       if others ≥ m then  
         action ← D  
       else  
         action ← C  
     end if  

     play action  
     observe total cooperators this round (call it C_count[t])  
     record history[t] = { my_action: action, C_count: C_count[t] }  
   end for  

This strategy converges to exactly m cooperators per round whenever opponents are willing to cooperate, punishes shortfalls only by stepping in (rather than defecting), and never over‐contributes when it is safe to free‐ride. It is simple, transparent, forgiving, and firmly “cooperative‐first.”
'''

description_COOPERATIVE_87 = '''
Below is a single‐strategy proposal (“Conditional Cooperate‐and‐Forgive”) that aims to secure the threshold m each round while retaining a cooperative stance, punishing failures just enough to deter defection but forgiving quickly so that cooperation can be re‐established.

1. Strategy Intuition  
   • Always try to hit the threshold m.  
   • If the group met the threshold last round, cooperate this round.  
   • If the group failed last round, defect once to signal “we must do better,” then immediately return to cooperation.  
   • In the very first and very last round, cooperate unconditionally (to build goodwill up front and preserve collective welfare at the end).

2. Notation  
   t = current round (1 ≤ t ≤ r)  
   T = total number of rounds (r)  
   m = threshold cooperators needed  
   C = Cooperate  
   D = Defect  
   last_success = Boolean flag, true if in round t–1 the number of cooperators ≥ m  
   punish_counter = integer counter of remaining punishment‐rounds (0 or 1 in this simple scheme)

3. State Variables (maintained across rounds)  
   last_success ← true   (assume success “before” round 1 to start cooperatively)  
   punish_counter ← 0    (no punishment pending at the outset)

4. Decision Rules  
   For each round t = 1,…,T do:  
     if punish_counter > 0 then  
       play D  
       punish_counter ← punish_counter – 1  
       (We are in our 1‐round punishment phase.)  
     else if t == 1 or t == T then  
       play C  
       (Always cooperate in the first and final round.)  
     else if last_success == true then  
       play C  
       (Group did well last round; reward by cooperating.)  
     else  
       play D  
       punish_counter ← 1  
       (Group failed last round; punish once, then forgive.)  
     end if  

     //— At the end of the round, observe N_C = number of cooperators among all players.  
     if N_C ≥ m then last_success ← true else last_success ← false end if  

5. Why it’s Cooperative  
   • In “normal” operation (last_success==true), we always cooperate, assisting the group to reach m.  
   • By punishing a single round when the group fails, we signal that they should not let the project collapse—thus creating pressure to cooperate in the next round.  
   • Because punishment is only one round long, trust quickly rebuilds. There is no drawn‐out vendetta.  
   • Always cooperating in the final round maximizes collective payoff in that last opportunity.

6. Handling Edge Cases  
   • First round (t=1): last_success is initialized to true, so we cooperate. This jump‐starts the public good.  
   • Last round (t=T): we override any punishment logic and cooperate; there is no future to punish or reward, so we simply aim for the group benefit.  
   • Back‐to‐back failures: each failure triggers exactly one round of punishment, so if failures persist, we will alternate D–C–D–C… still giving each new attempt a chance to succeed.  

7. Pseudocode Summary  
   ```
   initialize:
     last_success = true
     punish_counter = 0

   for t in 1..T:
     if punish_counter > 0:
       action = D
       punish_counter -= 1
     else if t == 1 or t == T:
       action = C
     else if last_success:
       action = C
     else:
       action = D
       punish_counter = 1

     observe N_C  // number of cooperators this round
     last_success = (N_C >= m)
   ```

With this “Conditional Cooperate-and-Forgive” strategy, you (i) reward collective success by always cooperating after a win, (ii) signal displeasure with a single‐round defect if the threshold is missed, and (iii) restore cooperation immediately thereafter, including an explicit cooperative stance in the first and last rounds.
'''

description_COOPERATIVE_88 = '''
Below is a fully specified, forgiving–yet cooperative–strategy for the r-round collective-risk dilemma.  It combines the intuition of Win-Stay–Lose-Shift (Pavlov) with an explicit last-round defection to avoid the unraveling problem.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Name: “Threshold-Pavlov with Last-Round Defection”  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Parameters you know:  
• n ≥ 2  (players)  
• r > 1  (rounds)  
• m, 1 < m < n  (cooperation threshold)  
• k > 1  (reward multiplier)  

Notation:  
• t ∈ {1,2,…,r} is the current round.  
• Action_i(t) ∈ {C,D} is your choice in round t.  
• coopCount(t) = number of players who played C in round t.  
• success(t) = (coopCount(t) ≥ m).  

High-level idea:  
1. Start by cooperating.  
2. In rounds 2 through r–1, if the previous round was “successful” (≥m cooperators), repeat your own last action; if it failed (<m cooperators), switch (C→D or D→C).  
3. In the final round (t=r), defect (to avoid backward induction).  

This punishes failures but immediately forgives after one “switch,” and it enforces mutual cooperation once the threshold is regularly met.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Initialize:  
 lastAction ← undefined  

For t from 1 to r do:  
 if t == 1 then  
  // First round: signal goodwill  
  myAction ← C  
 elif t == r then  
  // Final round: optimal one-shot defection  
  myAction ← D  
 else  
  // 2 ≤ t ≤ r–1: Pavlov‐style update based on previous round’s success  
  if success(t–1) == true then  
   // Win: keep whatever you did last time  
   myAction ← lastAction  
  else  
   // Lose: switch your action  
   if lastAction == C then myAction ← D  
   else                   myAction ← C  
  end if  
 end if  

 // Record and play  
 lastAction ← myAction  
 Play(myAction)  

End for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of key points  
1. Round 1: C  
 – By starting with C, you give all other cooperators a chance to reach m.  
2. Rounds 2 … r–1: Pavlov rule  
 – If the group met the threshold last round (“success”), you treat that as a “win” and stick with what you did—locking in cooperation if you cooperated, or continuing defection only if you were the lone defector.  
 – If the group failed to meet m (“loss”), you switch your action exactly once.  This both punishes the round-failure and immediately signals your readiness to return to cooperation.  
3. Round r: D  
 – Standard backward-induction says that in a one-shot PD there is no possibility of reward from future retaliation, so defection strictly dominates cooperation.  

Why this is cooperative:  
• When all players adopt it, the group settles on “all C” in rounds 2…r–1 as soon as a success occurs, since nobody switches after a win.  
• A single accidental defection or missed threshold is punished for exactly one round, then full cooperation is immediately re-established.  
• You never spiral into permanent mutual defection, and you avoid the end-game collapse by defecting only in round r.  

This strategy is simple, fair, and maximally forgiving while still discouraging persistent free-riding.
'''

description_COOPERATIVE_89 = '''
Below is a fully specified, cooperative “rotating‐minimal‐maintenance” strategy that (i) guarantees at least m cooperators every round (so the threshold is met), (ii) spreads the burden of cooperation evenly, and (iii) contains a simple one–round “recovery” rule to heal accidental breakdowns.  

1.  State variables  
    •  i ∈ {1,…,n}: your (fixed) player index  
    •  r: total rounds  
    •  t: current round (from 1 to r)  
    •  history of last round’s number of cooperators, call it last_coops (initialize last_coops = m so round 1 uses the schedule)  

2.  High‐level description  
    Each round t you do the following in order:  
    A.  If last_coops < m (i.e. the group failed in t–1), *all* players immediately play C this round to re-establish cooperation.  
    B.  Otherwise (last_coops ≥ m), you fall back on a *rotating schedule* that selects exactly m cooperators each round in a round‐robin fashion:  
        –  Define start = ((t–1) mod n) + 1  
        –  The scheduled set of cooperators is {start, start+1, …, start+m–1} modulo n (wrapping back to 1 after n).  
        –  If i is in that set, play C; otherwise play D.  
    C.  After everyone’s moves are revealed, record last_coops = the total number of C’s you observe, to be used in the next round.  

3.  Why it is cooperative  
    –  When everyone follows it, each round has exactly m cooperators (except the one full-C “recovery” round after a hiccup), so the public good is always funded and each player gets k (plus 1 if they defect in the scheduled role).  
    –  The “rotating” part spreads the cost 1 of cooperation evenly: over r rounds each player will on average cooperate m·r/n times (if n divides r, exactly).  
    –  The one-round fallback (“if last_coops < m then all C”) immediately pulls the group back to the safe, funded state whenever there is an accidental shortfall.  

4.  Edge cases  
    –  First round (t=1): last_coops was initialized to m, so you go straight to the schedule with start=1 and cooperate iff i∈{1,…,m}.  
    –  Rounds after a failure: exactly one full-C round, guaranteeing last_coops≥m for the *next* round, then you resume the rotating schedule.  
    –  Last round: no special end-game defection. You stay on schedule (or in recovery if needed), maximizing group payoff even if it costs you a bit.  

5.  Pseudocode  

    initialize last_coops = m    # so round 1 uses the schedule  
    for t in 1..r do  
      if last_coops < m then  
        action_i = C              # Recovery round  
      else  
        start = ((t-1) mod n) + 1  
        # build the m‐player scheduled coalition  
        coop_set = { ((start + j - 2) mod n) + 1 : j = 1..m }  
        if i in coop_set then action_i = C else action_i = D  
      end if  

      # submit action_i simultaneously; observe all actions  
      last_coops = count of C in round t  

    end for  

6.  Commentary on robustness  
    –  If some players deviate once, you detect it (last_coops < m) and switch to full cooperation for exactly one round, which “resets” the group.  
    –  If deviations persist, you will keep triggering full‐cooperate rounds, giving deviators no ongoing payoff advantage.  
    –  If they return to the rota, you seamlessly resume minimal‐cost funding.  

This strategy is simple to describe, fair, fully cooperative (in that it always funds the public good once a gap occurs), and stable against casual drift or one-off mistakes.
'''

description_COOPERATIVE_90 = '''
Below is a fully-specified, threshold-trigger strategy that (i) aims to sustain cooperation whenever a community payoff was achieved last round, (ii) punishes a failure with one round of defection, (iii) always defects in the last round to avoid end-game exploitation, and (iv) then immediately “forgives” and tries to re-cooperate.  You can adjust the punishment length if you like, but in most threshold-public-goods settings a single-round punishment is enough to discipline opportunists without collapsing the project.

1. State variables  
   • state ∈ {OK, PUNISH}  – “OK” means we are in a cooperative stance; “PUNISH” means we are defecting this round to discipline a recent failure.  
   • punish_timer ∈ ℕ≥0  – counts down how many remaining punishment rounds.

2. Initialization (before round 1)  
   state ← OK  
   punish_timer ← 0

3. In each round t = 1,2,…,r do:  
   a. Choose your action a_t as follows:  
      • If t = r (the last round):  
          a_t ← D  
        (In the last round there is no future to protect, so defect.)  
      • Else if state = OK:  
          a_t ← C  
      • Else if state = PUNISH:  
          a_t ← D  

   b. Play a_t simultaneously with the other n–1 players.

   c. Observe the total number of cooperators in round t, call it C_count_t.

   d. Update state for the next round (t+1):  
      If t < r then  
        • If C_count_t < m and state = OK then  
            // A failure just occurred, initiate punishment  
            state ← PUNISH  
            punish_timer ← 1      // punish for exactly one round  
          Else if state = PUNISH then  
            // we are in punishment mode—count down  
            punish_timer ← punish_timer – 1  
            If punish_timer = 0 then  
              state ← OK          // forgiveness: return to cooperative stance  
            EndIf  
          EndIf  
      EndIf

4. How it works  
   – First round (t=1): state=OK → you cooperate.  
   – As long as each round’s cooperators ≥ m, you stay in OK and keep cooperating.  
   – If a round fails to reach m cooperators, you go into PUNISH and defect exactly one round.  
   – After that one round of defection you forgive (state returns to OK) and try to rebuild cooperation.  
   – In the very last round, you always defect (no future to protect).

5. Why this is cooperative  
   – You start by cooperating, so you’re giving the group the first chance to hit the threshold.  
   – You only defect to punish genuine coordination failures, not to exploit successful rounds.  
   – Punishment is finite (one round), so you do not lock the group into permanent collapse.  
   – You return to cooperation immediately, offering the group a chance to restore the public good every subsequent round.  
   – You defend against exploiters (any who defect when the group is succeeding) by withholding cooperation for exactly one round.  
   – Defecting in the final round is the only strictly rational deviation in a finite-horizon repeated game; elsewhere you always give cooperation the benefit of the doubt.

Pseudocode summary:

state = OK  
punish_timer = 0

for t in 1..r:
  if t == r:
    action = D
  else if state == OK:
    action = C
  else:  // state == PUNISH
    action = D

  play(action)
  observe C_count_t

  if t < r:
    if C_count_t < m and state == OK:
      state = PUNISH
      punish_timer = 1
    else if state == PUNISH:
      punish_timer -= 1
      if punish_timer == 0:
        state = OK

End

This strategy is simple to implement, highly cooperative, self-correcting after accidents, and defends itself against free-riding without spiraling into permanent defection.
'''

description_COOPERATIVE_91 = '''
Below is a self-contained, fully cooperative “minimal-coalition” strategy.  It guarantees that each round exactly m players contribute (so the threshold is met every time), it fairly rotates who pays the cost, and it punishes any one who fails to play their turn to cooperate by dropping them from the next coalition until they make it up.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Global bookkeeping (maintained across rounds)  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
For each player j∈{1…n} maintain an integer Contributions[j] = number of rounds so far in which j cooperated.  
At start Contributions[j] ← 0 for all j.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Per‐round decision rule (for round t = 1,2,…,r)  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

1. Identify the planned coalition of size m.  
   If t=1 or last round also uses the same rule below (no special end‐game defection):  
     • Sort all players by ascending Contributions[j].  Break ties by smaller index j.  
     • Let Coalition ← the first m players in this sorted list.  

   If in the previous round (t–1) fewer than m actually cooperated, we must punish defectors and restore cooperation:  
     • From last round’s actual cooperators (ObservedCoops), sort them by ascending Contributions[j] (ties by index).  
     • Take as many of those ObservedCoops as we can, up to m, to form the new Coalition.  
     • If |Coalition| < m, fill out Coalition with the lowest‐Contribution non‐cooperators (ascending Contributions, tie by index) until Coalition has size m.  

2. Action for player i in round t:  
   If i ∈ Coalition then  
     play C (cooperate)  
   else  
     play D (defect)  

3. Update bookkeeping after observing everyone’s actions this round:  
   Let ObservedCoops = { all j who played C in round t }.  
   For each j ∈ ObservedCoops do Contributions[j] ← Contributions[j] + 1.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Why this works  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Threshold always met as long as at least m in your chosen Coalition actually cooperate.  Any deviation is immediately punished: if one of the m fails to cooperate, next round they’re dropped from the Coalition and replaced by someone more reliable.  
2. Fairness emerges: over r rounds each player will be chosen about (m·r)/n times (up to ±1), so the cost of cooperation is shared evenly.  
3. No end‐game collapse: because we do not unilaterally defect in the last round, we sustain cooperation even in round r.  Even if some try to free-ride in r, they will be punished in r+1—but since there is no r+1, they simply lose future trust in an ongoing tournament context.  
4. No communication or extra assumptions needed—everything is based on observed actions and a simple lexicographic tie-break.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode summary  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Initialize Contributions[j] ← 0 for all j=1…n.  

for t in 1…r do  
  if t=1 or last round’s cooperator‐count ≥ m then  
    CandidateList ← all players sorted by (Contributions[j], j) ascending  
    Coalition ← first m in CandidateList  
  else   # previous round failed  
    Obs ← set of players who cooperated in t–1  
    ObsSorted ← Obs sorted by (Contributions[j], j) ascending  
    Coalition ← first min(|Obs|, m) of ObsSorted  
    if |Coalition|<m then  
      fill Coalition with next players from (all players \ Coalition) sorted by (Contributions[j], j) ascending  
  end if  

  if i ∈ Coalition then action ← C else action ← D  

  Observe all actions, let ObservedCoops = {j| j’s action=C}  
  for j in ObservedCoops do Contributions[j] ← Contributions[j] + 1  
end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy is fully cooperative—it meets the group threshold every round (if opponents ever meet it), fairly shares the burden of cooperation, and punishes any shirker by immediately excluding them from the next round’s coalition.
'''

description_COOPERATIVE_92 = '''
Below is a single‐strategy proposal—call it “Forgiving Threshold”—that (1) aims to secure the public-good bonus each round, (2) punishes occasional breakdowns just long enough to deter them, but (3) forgives and returns to cooperation so as not to spiral into all-out defection.  

--------------------------------------------------------------------------------  
1.  Data structures and bookkeeping  
    •  punishment_counter ← 0  
         – counts how many more rounds you will stay in “punishment mode.”  
    •  last_C_count ← undefined  
         – in each round t > 1 you will record how many players cooperated in t–1.  

2.  General idea  
    – Round 1: start by cooperating.  
    – Rounds 2…r–1:  
         •  If you are in punishment mode (punishment_counter > 0), defect and decrement the counter.  
         •  Else, if the previous round had ≥ m cooperators, cooperate.  
           – This says “we met the threshold last period, so let’s keep it up.”  
         •  Else (previous round had < m cooperators), defect this round *and* set punishment_counter = 1.  
           – That single‐round punishment discourages free‐riding or mass breakdown, but is short enough to allow recovery.  
    – Round r (the last round): defect.  
         •  In a finite known horizon, the last round is a dominant-defect stage.  

3.  Pseudocode  
    for t in 1…r do  
      if t == 1 then  
        action ← C  
      else if t == r then  
        action ← D  
      else  
        if punishment_counter > 0 then  
          action ← D  
          punishment_counter ← punishment_counter – 1  
        else if last_C_count ≥ m then  
          action ← C  
        else  
          action ← D  
          punishment_counter ← 1  
        end if  
      end if  

      play(action)  
      observe opponents’ actions this round  
      last_C_count ← number of players (including you) who played C this round  
    end for  

4.  Why this is cooperative  
    – It *starts* by cooperating, signaling willingness to pay the cost.  
    – Whenever the group meets the threshold, it *continues* to cooperate—locking in the k bonus.  
    – A setback (fewer than m Cs) triggers only a *one-round* punishment. That raises the stakes of breakdown (someone who drifts into defection will suffer lower short-term gains), but we don’t punish forever—so the group can quickly re-establish cooperation.  
    – By defecting in the last round, you avoid being the sucker in a place where no future rounds remain.  

5.  Edge‐case notes  
    •  If mistakes (e.g. random noise) cause a failure, one‐round punishment is enough to restore trust.  
    •  If multiple failures occur in a row (opponents keep defecting), you will keep punishing once per failure and then returning to cooperation—in effect cycling “C, C, …, C” with occasional one‐round “D” flags when things break down.  
    •  If opponents adopt a similar rule set, you will converge to m or more Cs every non-terminal round, thus earning the k bonus each time.  

In tournaments of independent LLM strategies, this approach (i) signals that you’re reliably pro-cooperation, (ii) enforces minimal group discipline against defection, and (iii) tolerates occasional slips without descending into perpetual defection.
'''

description_COOPERATIVE_93 = '''
Below is a single‐formula, fully specified “threshold‐helper” strategy that (a) drives the group toward hitting the public‐goods threshold whenever possible, (b) avoids wasting contributions when the group is far from success, and (c) takes into account first‐ and last‐round incentives.

---------------------  
Strategy name  
“Threshold Helper”

Parameters you know:  
• n ≥ 2, r > 1, threshold m (1 < m < n), reward factor k > 1.  

Notation:  
• t ∈ {1,2,…,r} is the current round.  
• history[t–1] is the vector of actions (C or D) by all players in the previous round.  
• s = # of Cooperators in history[t–1].  

Decision Rule (for you, player i):  
1. If t == 1:  
     always Cooperate (C).  
2. Else if t == r (the very last round):  
     always Defect (D).  
3. Else (2 ≤ t < r):  
     let s = number of cooperators in round t–1  
     • if s ≥ m:  
         — play C  
       (the group has just succeeded – keep it going)  
     • else if s == m–1:  
         — play C  
       (you can supply the marginal cooperator and salvage success)  
     • else (s ≤ m–2):  
         — play D  
       (too few cooperators last time – contribution would be wasted)  

Pseudocode  

```
function decide_action(t, history):
    if t == 1:
        return C
    else if t == r:
        return D
    else:
        prev = history[t-1]            # vector of A_j in round t-1
        s = count(prev, action==C)    # total cooperators last round
        if s >= m or s == m-1:
            return C
        else:
            return D
```

Total‐game payoff over r rounds is just the sum of π_i,t as defined in the spec.

Rationale / Cooperative mindset  
• Round 1: Signal willingness to coordinate.  
• Middle rounds:  
   – If the group just met the threshold, continue cooperating to keep the public‐good flowing.  
   – If the group was one short of m, step in—you pay the cost but trigger the big k payoff for everyone.  
   – If the group was hopelessly below m, avoid a dead‐end contribution.  
• Final round: Standard “end‐game” defection to avoid being exploited when there’s no future to enforce cooperation.

This rule is deterministic, easy to implement, punishes persistent failures without spiraling into all‐out defection, and always gives the group the best chance of repeatedly hitting the critical mass.
'''

description_COOPERATIVE_94 = '''
Below is a single‐strategy recipe that (a) begins by trying to build cooperation, (b) punishes any round in which the group failed to reach the threshold, (c) forgives after one round of punishment, and (d) defects in the very last round when there is no future to protect.  It is “cooperative” in the sense that whenever past‐round cooperation succeeded, it immediately returns to cooperating.

––––––––––––––––––––––––––––––––  
1. State variables  
   • punishing ∈ {false, true} — have we committed to a one‐round punishment?  
   • coop_prev — number of cooperators observed in the last round (initialize to n so that we start by cooperating).  

2. Per‐round decision rule  
   for t in 1..r do  
     if t == r then  
       action ← D  
         ▶ No future after round r, so maximize immediate payoff.  
     else if punishing == true then  
       action ← D  
       punishing ← false  
         ▶ We punish exactly one round, then forgive.  
     else if t == 1 then  
       action ← C  
         ▶ First‐round push to get cooperation going.  
     else if coop_prev ≥ m then  
       action ← C  
         ▶ Past round succeeded in reaching the public‐good threshold ⇒ reward cooperation.  
     else  
       action ← D  
       punishing ← true  
         ▶ Past round failed the threshold ⇒ punish one round.  
     end if  

     play(action)  
     observe all players’ actions this round → compute coop_prev for next iteration  
   end for  

––––––––––––––––––––––––––––––––  
3. Explanation of key points  
 • First round: we cooperate unconditionally to signal willingness.  
 • Ongoing rounds 2 through r–1:  
    – If last round reached the threshold (coop_prev ≥ m), we cooperate again.  
    – If last round fell short, we defect once as a “punishment” signal, then reset.  
 • Last round (t = r): we defect because there is no future discipline—this maximizes our one‐shot gain.  
 • Punishment is limited to one round, to avoid cascading mutual defection.  

4. Why it is cooperative  
 • It never defects pre‐emptively: it only defects in direct response to a failed‐threshold round or in the unavoidable last stage.  
 • By immediately returning to cooperation after one round of punishment, it allows the group to re‐coordinate on meeting the threshold as soon as possible.  
 • It sends a clear “signal” (a single defection) whenever risk‐aversion fails, encouraging other players to mend the group effort.
'''

description_COOPERATIVE_95 = '''
Below is a self-contained, cooperative “threshold-trigger” strategy that (i) tries to secure the public good by cooperating whenever it looks worthwhile, (ii) briefly punishes rounds in which the team failed to reach m cooperators, and (iii) defects in the last round to collect any residual private benefit.

––––––––––––––––––––––––––––––––––––  
Strategy name: TTCS (Threshold-Triggered Cooperative Strategy)  
––––––––––––––––––––––––––––––––––––  

1. State variables  
   • t: current round (1 ≤ t ≤ r)  
   • last_success (bool): whether the group reached ≥ m cooperators in the immediately preceding round  
   • punish (bool): flag indicating “I will punish this round”  

   Initialize at t=1:  
     last_success ← true  
     punish ← false  

2. Decision rule by round  

   Round 1 (t = 1)  
     action ← C  
     (We begin by signaling goodwill.)  

   Intermediate rounds (2 ≤ t ≤ r–1)  
     if punish = true then  
       action ← D  
       // one-shot punishment  
       punish ← false  
     else if last_success = true then  
       action ← C  
       // partnership still viable  
     else  
       // group failed last round ⇒ trigger punishment  
       action ← D  
       punish ← true  
     end  

   Last round (t = r)  
     // backward-induction defection  
     action ← D  

3. Updating state after observing the round’s outcomes  
   Let coop_count = number of players (including you) who chose C this round.  
   last_success ← (coop_count ≥ m)  

4. Rationale and properties  
   • First-round cooperation establishes trust.  
   • As long as the project “succeeds” (≥ m cooperators), we keep cooperating.  
   • If there is a “failed” round (coop_count < m), we defect exactly once in the next round as punishment, then revert to cooperation.  
   • A single‐round punishment is enough to discourage free‐riding but not so harsh as to provoke endless tit-for-tat.  
   • In the known final round, we defect to maximize private payoff when no future rounds remain.  

––––––––––––––––––––––––––––––––––––  
Pseudocode summary  

  initialize:  
    last_success ← true  
    punish ← false  

  for t in 1..r do  
    if t == 1 then  
      action ← C  
    else if t == r then  
      action ← D  
    else  
      if punish then  
        action ← D  
        punish ← false  
      else if last_success then  
        action ← C  
      else  
        action ← D  
        punish ← true  
      end  
    end  

    play(action)  
    observe coop_count  // count of C’s this round  
    last_success ← (coop_count ≥ m)  
  endfor  

––––––––––––––––––––––––––––––––––––  

This strategy is clearly cooperative—it starts by investing in the public good, continues cooperation when the team succeeds, only momentarily punishes collective failure, and then returns to cooperation. The one-round punishment deters defection without destabilizing long-run cooperation, and the clean defection in the very last round extracts any remaining private benefit.
'''

description_COOPERATIVE_96 = '''
Below is a single, fully-specified “rotating-m” strategy with a grim-trigger safety, which in every round delivers exactly m cooperators (the minimum needed), punishes any deviation, and rotat­es the duty of cooperation as fairly as possible over a finite horizon.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Data structures and initialization  
   • n, m, r, k are common-knowledge.  
   • Each player i maintains:  
     – coop_count[j] for j=1…n: number of times player j has cooperated so far (initially 0).  
     – DeviationFlag (initially false).  

2. High-level logic per round t = 1…r  
   if DeviationFlag == true then  
     play D forever (grim trigger).  
   else  
     2.1 Determine the set S_t of m “duty” cooperators:  
         – Sort players j by ascending coop_count[j].  
         – Break ties by ascending player index.  
         – Let S_t be the first m players in that sort.  
     2.2 If i ∈ S_t then play C, else play D.  
     2.3 Observe the actual outcome:  
         – Let ActualCooperators = set of players who played C.  
         – If |ActualCooperators| ≠ m OR ActualCooperators ≠ S_t then  
             DeviationFlag ← true  (someone deviated from the schedule).  
     2.4 Update counts:  
         – For each j who played C this round, coop_count[j]++.  

3. Edge‐case handling  
   • First round (t=1): coop_count[:] = 0, so the lowest‐index m players are chosen.  
   • Remainder rounds: rotation equalizes duty even if r·m ≠ n.  
   • Last round t = r: no special endgame twist—since k > 1, cooperating still yields positive surplus, and the threat of post-game justice is baked into the grim trigger (it prevents earlier deviations).  

4. Why this is cooperative  
   • Exactly m players cooperate each round ⇒ group payoff is maximized (we avert the risk with minimum cost).  
   • Rotation ensures no one is over-burdened over r rounds.  
   • A single deviation by anybody (too many, too few, or wrong player) triggers permanent defection by us, so the threat of lost future gains enforces adherence.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  

  initialize coop_count[1..n] ← 0  
  DeviationFlag ← false  

  for t in 1..r:  
    if DeviationFlag:  
      action(i,t) ← D  
      continue  
    end if  

    // 2.1 Build the rotation schedule S_t  
    create list L of pairs (j, coop_count[j]) for j=1..n  
    sort L by (coop_count ascending, then j ascending)  
    let S_t ← the first m entries of L (their player indices)  

    // 2.2 Play according to duty roster  
    if i in S_t then action(i,t) ← C  
    else              action(i,t) ← D  

    // … after simultaneous play, everyone observes ActualCooperators …  
    let ActualCooperators ← { j | action(j,t) == C }  

    // 2.3 Check for deviations  
    if |ActualCooperators| != m OR ActualCooperators != S_t then  
      DeviationFlag ← true  
    end if  

    // 2.4 Update cooperation counts  
    for each j in ActualCooperators:  
      coop_count[j] ← coop_count[j] + 1  
    end for  
  end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

With this rulebook, you (i) sustain exactly the threshold each round, (ii) share the cost fairly, and (iii) enforce compliance by a simple but unforgiving trigger.
'''

description_COOPERATIVE_97 = '''
Below is a single‐strategy design that (i) tries to build and sustain cooperation, (ii) punishes defections just long enough to deter free-riding, (iii) forgives quickly so that one mistake (or one miscoordination) does not spiral into permanent collapse, and (iv) mitigates the “last‐round” endgame problem by switching to defection only in the final K rounds.  You can tune the punishment length P and the endgame cutoff K to your taste; I recommend P=1 and K=2 as a default.

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
STRATEGY NAME  
  “Group‐Conditional TFT with Endgame Cutoff”

PARAMETERS  
  • P = 1            ← punishment length in rounds  
  • K = 2            ← number of final rounds in which we defect unconditionally  

STATE VARIABLES (carried from round to round)  
  • last_success ∈ {true,false}  
       true  if in the previous round the group reached the threshold (≥ m Cs)  
       false otherwise  
  • punish_remaining ∈ ℕ₀  
       how many more rounds we will defect in punishment mode  

INITIALIZATION (before round 1)  
  last_success   ← true     // so that we start by cooperating  
  punish_remaining ← 0

DECISION RULE (each round t = 1…r)  
  if t > r–K then  
    // In the last K rounds, we defect to avoid exploitation in an unpunishable endgame  
    play D  
  else if punish_remaining > 0 then  
    // We are in punishment mode  
    play D  
    punish_remaining ← punish_remaining – 1  
  else if last_success == true then  
    // Last round the threshold was met ⇒ stay in cooperation mode  
    play C  
  else  
    // Last round the threshold FAILED ⇒ punish for P rounds (including this one)  
    play D  
    punish_remaining ← P – 1  // we’ve just used one of the P punishment rounds

AFTER THE ROUND (once everyone’s actions are revealed)  
  let cooperators = number of players who chose C this round  
  last_success ← (cooperators ≥ m)  

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
EXPLANATION OF KEY POINTS

1. Opening signal:  
   • We set last_success=true at t=1 so we start by cooperating.  

2. Sustaining cooperation:  
   • Whenever the group collectively meets the threshold in round t–1, we “reward” by cooperating in round t.  

3. Punishment & forgiveness:  
   • If in some round the group fails to reach m cooperators (regardless of who defected), we defect for P rounds in a row (P=1 by default).  
   • After those P rounds are up, we revert to conditional cooperation again.  
   • This “one‐round punishment” is just enough to deter a defection but short enough to forgive noise or accidental miscoordination.  

4. Endgame cutoff (last K rounds):  
   • In a finite‐horizon game, pure cooperation unravels in the last round.  To avoid being suckered by unconditional cooperators, we simply defect in the final K rounds.  
   • With K=2, we defect in rounds r–1 and r.  You can choose a different K, but K≥1 is needed to blunt the backward‐induction collapse.  

5. Why it’s cooperative:  
   • As long as everyone follows this rule, you will see full coordination (≥m Cs) every round until the cutoff, maximizing total group payoffs.  
   • Any rogue defector immediately costs them one round of the public good (the group fails the threshold once), and they face a one‐round collective defection in response—enough to make unilateral drift unattractive.  
   • After the brief punishment, we forgive and jump back into cooperation, so long‐run payoffs remain high.  

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
PSEUDOCODE SUMMARY

  // PARAMETERS
  P ← 1
  K ← 2

  // STATE
  last_success ← true
  punish_remaining ← 0

  for t in 1…r do
    if t > r – K then
      action ← D
    else if punish_remaining > 0 then
      action ← D
      punish_remaining ← punish_remaining – 1
    else if last_success then
      action ← C
    else
      action ← D
      punish_remaining ← P – 1
    end if

    // observe all players’ actions this round
    cooperators ← count_of_C_this_round
    last_success ← (cooperators ≥ m)

  end for

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy is simple, transparent (so co‐players can infer that cooperation benefits them), jealous of defections (it punishes swiftly), forgiving (returns to cooperation after just P rounds), and immune to pure last‐round exploitation by sacrificing only the final K rounds.
'''

description_COOPERATIVE_98 = '''
Below is a self-contained “collective generous trigger” strategy.  It is designed to (a) get the group over the m-cooperator threshold as often as possible, (b) punish mistakes only briefly so that cooperation can be re-established, and (c) handle first/last round edge cases cleanly.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Intuition  
  • We start by cooperating to signal willingness.  
  • As long as the group met the threshold in the previous round, we keep cooperating.  
  • If the threshold was missed, we defect for exactly one round (our “punishment”), then go back to cooperating.  
  • In the final round, we behave the same way except we do not punish (no future to protect), so we only cooperate if the previous round succeeded.

This creates a short-punishment trigger that is forgiving (punishment_length = 1), avoids endless defection spirals, and coordinates on hitting m cooperators each round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
2. State variables  
  punishing_rounds_remaining ← 0  
    // how many more rounds we will defect as punishment  
  last_round_coop_count ← undefined  
    // number of players (including us) who cooperated in t–1

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
3. Strategy Pseudocode  

Let t = current round index (1 ≤ t ≤ r).

for t in 1…r do  
  if t = 1 then  
    // First round: signal cooperation unconditionally  
    action_t ← C  
  
  else if t = r then  
    // Last round: no future punishment incentive  
    if last_round_coop_count ≥ m then  
      action_t ← C  
    else  
      action_t ← D  
  
  else if punishing_rounds_remaining > 0 then  
    // We are in a punishment phase  
    action_t ← D  
    punishing_rounds_remaining ← punishing_rounds_remaining – 1  

  else  
    // Normal (non‐first, non‐last, non‐punishing) round  
    if last_round_coop_count ≥ m then  
      // Group succeeded last round → keep cooperating  
      action_t ← C  
    else  
      // Group failed last round → punish once, then forgive  
      action_t ← D  
      punishing_rounds_remaining ← 1  
    end if  
  end if  

  // … play action_t, observe how many cooperated this round …  
  last_round_coop_count ← (number of players j who chose C in round t)  
end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
4. Comments on key design points  
1. First‐round cooperation  
   • We unconditionally pick C to show goodwill and give cooperation a chance.  
2. One‐round punishment  
   • As soon as the threshold m fails, we defect exactly once.  This penalizes defection but immediately forgives, avoiding infinite downward spirals.  
3. Returning to cooperation  
   • After our one‐round punishment, punishing_rounds_remaining = 0, so if the group meets m next round we instantly resume C.  
4. Last‐round behavior  
   • In the true final round there is no future to protect, so we skip punishment logic and simply cooperate if (and only if) the previous round was successful.  
     – This prevents us from needlessly defecting at the end when we could help the group still earn k.  
5. Parameter choices  
   • punishment_length = 1 is the minimal “generous trigger.”  If you wished to be harsher you could set it to a larger integer, but that risks a longer attrition of cooperation.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy is cooperative—it continuously tries to hit the public‐good threshold, only punishes failures briefly, and quickly forgives so that the group can stabilize on meeting m cooperators each round.
'''

description_COOPERATIVE_99 = '''
Below is a fully specified, “conditionally‐cooperative” strategy that (i) seeks to meet the group threshold m in each round, (ii) punishes temporary breakdowns, (iii) forgives and retests cooperation after a fixed punishment length, and (iv) handles first and last rounds specially.  You can tune the punishment length p ≥1; we suggest p=1 or p=2.

────────────────────────────────────────────────────────────────  
STRATEGY OVERVIEW  
────────────────────────────────────────────────────────────────  
We play r rounds.  In each round t we either Cooperate (C) or Defect (D).  We keep track of:

• coops_last: how many players (including ourselves) cooperated in the immediately preceding round  
• punishment_timer: how many more rounds we will “punish” by defecting before trying to cooperate again  

Our goals:  
1.  In “good” states, cooperate so long as (collectively) the threshold m was met last round.  
2.  If the group fails (coops_last < m), enter a short “punishment” phase of length p, defecting unconditionally for p rounds.  
3.  After those p rounds, re–test cooperation by playing C once.  If the group reached m again, stay in good state; if not, punish again.  
4.  First round is always a test for cooperation.  
5.  Last round: cooperate only if our cooperation can swing the group above the threshold; otherwise defect so as not to waste endowment.  

Because all players run the same rule, this can sustain repeated attainment of ≥m cooperators, with automatic recovery from occasional slip–ups.

────────────────────────────────────────────────────────────────  
PSEUDOCODE  
────────────────────────────────────────────────────────────────  
Parameters:  
 n (players), r (rounds), m (threshold), k (reward factor),  
 p (punishment length, integer ≥1)  

State variables (initialized before round 1):  
 punishment_timer ← 0  
 coops_last ← undefined  

For t from 1 to r do:  
 if t == 1 then  
  # First round: optimistic test  
  action ← C  
 else if punishment_timer > 0 then  
  # We are in a punishment phase  
  action ← D  
  punishment_timer ← punishment_timer − 1  
 else if t == r then  
  # Last round: cooperate only if pivotal  
  if coops_last == m−1 then  
   action ← C   # our C will just meet the threshold  
  else  
   action ← D   # either threshold already met without us, or it cannot be met even if we C  
 else  
  # Normal round, no active punishment, not first or last round  
  if coops_last ≥ m then  
   # Last round was a success – stay cooperative  
   action ← C  
  else  
   # Last round failed, trigger punishment and defect this round  
   punishment_timer ← p  
   action ← D  
 # end if  

 Play(action)  
 Observe all players’ actions and update coops_last ← number of C’s observed this round  
# end for  

────────────────────────────────────────────────────────────────  
EXPLANATION OF KEY POINTS  
────────────────────────────────────────────────────────────────  
1. First round: we start “optimistic” by playing C; if enough others follow, we lock into cooperation.  
2. Good rounds (coops_last ≥ m): we keep cooperating, reaping the k‐bonus every time.  
3. If the group fails (coops_last < m), we “punish” by defecting for p consecutive rounds.  This signals to others that breakdowns are costly.  
4. After p defect–rounds, we re–test cooperation with one C.  If the group rejoins (≥m C’s), we return to steady cooperation; if not, we punish again.  This forgives accidental slips but deters chronic defection.  
5. Last round: since there is no future, we refuse to waste our endowment unless our C is pivotal (i.e. exactly m−1 other cooperators).  If the threshold would be met without us, we defect to maximize our private payoff; if we cannot sway the outcome (too few others), we also defect.  

────────────────────────────────────────────────────────────────  
WHY IT’S COOPERATIVE  
────────────────────────────────────────────────────────────────  
• It starts friendly and gives every player a chance to coordinate.  
• It sustains full cooperation so long as the threshold is met each round.  
• It punishes only briefly (length p) after failures, then forgives, allowing recovery from noise or mistakes.  
• It only defects in the last round when further cooperation cannot improve future rounds, and then only when it makes no difference to the group outcome.  

Tuning p: a small p (1 or 2) is usually enough to deter free‐riding while keeping the group quickly on track.  

This strategy is fully specified, symmetric, and requires no communication beyond observing past plays. It robustly achieves the collective threshold in every round once stabilized.
'''

description_COOPERATIVE_100 = '''
Below is a single‐strategy proposal—call it “Finite Grim Trigger with Last–Round Defection”—that in simulation and theory tends to sustain the m‐threshold, round after round, yet still guards against end‐game free‐riding and “sucker” losses.

1.  Intuition  
   •  Encourage everyone to cooperate as long as the threshold was met in the previous round.  
   •  If the threshold ever fails, impose a short, shared punishment (all defect for one round), then forgive and return to cooperation.  
   •  In the very last round, defect (no future rounds in which to punish), eliminating the incentive to be the last‐round free‐rider.

2.  Parameters  
   •  n ≥ 2 players, r > 1 rounds, threshold m (1 < m < n), reward factor k > 1.  
   •  Punishment length P = 1 round (can be tuned larger if you want harsher punishment).

3.  State variables (for your own internal use)  
   •  punish_counter ← 0   (counts how many more rounds you must defect in punishment mode)  
   •  t = current round number, from 1 to r  

4.  First‐round rule (t = 1)  
   •  Cooperate.  
     Rationale: start by signaling willingness to meet the threshold.

5.  Generic round rule (2 ≤ t < r)  
   if punish_counter > 0 then  
     – Defect  
     – punish_counter ← punish_counter − 1  
     (You are serving out a punishment—no questions.)  
   else if (number of cooperators in round t − 1) < m then  
     – (A “threshold failure” just happened.)  
     – Set punish_counter ← P  (enter punishment mode)  
     – Defect this round too  
   else  
     – (Threshold was met last round.)  
     – Cooperate  

6.  Last round (t = r)  
   •  Defect.  
     Rationale: no future rounds remain in which to punish, so everyone expects defection.  

7.  Pseudocode  

   ```
   initialize punish_counter = 0

   for t in 1..r do
     if t == 1 then
       action[t] = C
     else if t == r then
       action[t] = D
     else
       if punish_counter > 0 then
         action[t] = D
         punish_counter = punish_counter - 1
       else
         let coop_prev = number of C’s in round (t - 1)
         if coop_prev < m then
           punish_counter = P      # P = 1
           action[t] = D
         else
           action[t] = C
         end if
       end if
     end if
   end for
   ```

8.  Why this works as a cooperative strategy  
   – By cooperating immediately and after any round in which the threshold was met, you help ensure that most rounds achieve the public‐goods payoff.  
   – A single failure to reach m cooperators triggers exactly one round of collective defection.  That punishes free riders (who benefit most from others’ cooperation) but does not doom the entire future: after the one‐round punishment, you “forget” past failures and go back to cooperation.  
   – Defecting in the final round removes any incentive for last‐round free‐riding.  

9.  Edge‐case behavior  
   •  If the very first round fails (e.g. others all defect), you will punish for one round (round 2), then return to cooperating in round 3, hoping others will too.  
   •  If failures recur consecutively, each failure begets exactly one additional round of defection.  You will never punish forever—only P rounds—so the group can recover.  
   •  If a single “rogue” defector spoils the threshold, all players defect together for one round.  Once punishment ends, cooperating players can re‐establish the threshold.  

10. Possible variants  
   •  Raise P (the punishment span) to 2 or 3 rounds for stronger deterrence.  
   •  Only punish if you personally cooperated in the failed round (the “sucker”)—optional refinement.  
   •  Introduce a small probability of forgiveness even during punishment (a “generous” variation).  

This simple “finite grim” rhythm—cooperate after success, punish briefly after failure, defect in last round—leverages repeated‐game incentives to sustain the m‐threshold cooperation while avoiding unending ricochets of mutual defection.
'''

description_COOPERATIVE_101 = '''
Below is a single‐strategy recipe—“Threshold-Triggered, Forgiving Cooperator” (TTFC)—that in our simulations strikes a good balance between sustaining cooperation and protecting against chronic free-riding.  You can turn this into code directly; the high‐level logic and the corner-case rules are all here.

1.  Data structures / state  
   •  betrayed: boolean, initially false  
   •  rounds_failed: integer counter of how many consecutive rounds the group has missed the threshold, initially 0  

2.  Outline of rules  
   – First round: always cooperate.  
   – In any other round t < r (i.e. not the last):  
       •  If in the immediately preceding round the number of cooperators ≥ m, then  
          –   reset rounds_failed ← 0  
          –   cooperate this round.  
       •  Else (threshold was missed in t–1):  
          –   rounds_failed ← rounds_failed+1  
          –   if rounds_failed == 1: still give the group “one more chance” → cooperate  
          –   else (rounds_failed ≥ 2): defect.  
   – Last round (t == r):  
       •  No future to punish or reward, so play cautiously.  
       •  If in round r–1 the group met the threshold, cooperate (they’ve shown they can coordinate).  
       •  Otherwise defect (you’re unwilling to risk the full contribution when cooperation has already collapsed).  

3.  Why it’s cooperative  
   – It always gives the group at least two successive opportunities to hit the threshold.  
   – When the group succeeds, it re-resets and stays in “cooperate” mode.  
   – It only punishes persistent failure—so one bad round is forgiven, avoiding over-reacting to occasional noise.  

4.  Pseudocode  

   initialize:
     betrayed ← false
     rounds_failed ← 0

   for t in 1…r:
     if t == 1:
       action ← C
       continue

     # observe last round’s #cooperators, call it last_coops
     if t < r:  
       if last_coops ≥ m:
         rounds_failed ← 0
         action ← C
       else:
         rounds_failed ← rounds_failed + 1
         if rounds_failed == 1:
           # give one more chance
           action ← C
         else:
           # persistent failure, withdraw
           action ← D

     else:  # t == r, last round
       if last_coops ≥ m:
         action ← C
       else:
         action ← D

     # end of round t loop

5.  Handling edge cases  
   •  All-C history: you keep cooperating every round.  
   •  Single accidental failure: you cooperate one more time, in case it was a one-off glitch.  
   •  Two consecutive misses: you switch to defection to avoid being exploited.  
   •  Last round: you only cooperate if the group has demonstrated coordination one round earlier.  

This rule set maximizes the chance that players will repeatedly reach the threshold (and thus collect the bonus k each round), is forgiving of one-off lapses, but quickly clamps down on a persistent defector minority.
'''

description_COOPERATIVE_102 = '''
Below is a single‐strategy proposal—call it “Finite‐Horizon Pavlov” (FHP)—that seeks to sustain the m-threshold public‐good every round except the very last, by (1) starting cooperatively, (2) punishing any failure exactly one round, then forgiving, and (3) defecting in the known final round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Informal description  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
State variable: S ∈ {Cooperate, Punish}  
Initialize S ← Cooperate  

For rounds t = 1,2,…,r:  
 • If t = r (the last round): play D (no future to enforce cooperation).  
 • Else (t < r):  
   – If S = Cooperate, play C.  
   – If S = Punish, play D.  

After observing how many players cooperated in round t (call it cₜ):  
 • If cₜ ≥ m, set S ← Cooperate.  (Success: restore/maintain cooperation.)  
 • Else (cₜ < m):  
     – If S was Cooperate this round, set S ← Punish.  (One round of punishment.)  
     – If S was Punish this round, set S ← Cooperate. (Then forgive and return to cooperation.)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
2. Why it works  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• Round 1 always C → jump‐start cooperation.  
• If everyone cooperated or at least m cooperated, we stay in Cooperate → steady C.  
• If threshold fails (cₜ < m), we switch to Punish for one round → defect as a minimal punishment.  
  Then we forgive (go back to Cooperate) regardless of the punishment’s success.  
• By punishing exactly one round, we deter unilateral or small‐group defection but avoid endless mutual defection.  
• In the last round, all defect (standard backward induction in finitely repeated games).  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
3. Pseudocode  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
```
Inputs: n, r, m, k
State S ← “Cooperate”

for t in 1…r do
  if t == r then
    action ← “D”                    # Last round: defect
  else
    if S == “Cooperate” then
      action ← “C”
    else                          # S == “Punish”
      action ← “D”
    end
  end

  play(action)                    # simultaneous move
  observe c_t ← number of C’s this round

  # Update state
  if c_t ≥ m then
    S ← “Cooperate”               # success → stay/return to cooperation
  else
    if S == “Cooperate” then
      S ← “Punish”                # threshold failed → punish next round
    else
      S ← “Cooperate”             # one‐round punishment over → forgive
    end
  end
end
```

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
4. Edge‐case handling  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• First round (t=1): S=”Cooperate” ⇒ we play C.  
• “Spontaneous” failures: any single bad round triggers exactly one D.  
• Forgiveness: after one punishment round, regardless of whether that punishment succeeded in restoring the threshold, we go back to Cooperate—avoiding endless mutual defection.  
• Last round: always defect (no future payoff to enforce cooperation).  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy is simple, symmetric, and aims to keep at least m cooperators every round except the last. If all players adopt it, you will reliably hit the threshold in rounds 1…r–1, earning the extra k each time, and defect in round r as dictated by finite‐horizon logic.
'''

description_COOPERATIVE_103 = '''
Below is a single‐strategy design—call it “Collective Win‐Stay/Lose‐Shift with One‐Round Punishment and End‐Game Defection”—that (i) nudges the group toward reaching the m-cooperator threshold every round, (ii) punishes failures collectively, (iii) allows recovery, and (iv) avoids the “last‐round” unraveling.

1.  State variables  
    – last_success: Boolean, did the group reach the threshold in the previous round?  
    – punish_count: integer ≥ 0, how many punishment rounds remain  
    – t: current round index (1…r)  

2.  Initialization (before round 1)  
    last_success ← true   // assume “virtual success” so we start cooperating  
    punish_count ← 0  

3.  Per‐round decision rule (for round t = 1…r)  
    if t = r then  
       action ← D         // defection in the very last round (backward‐induction safe)  
    else if punish_count > 0 then  
       // we are in a punishment phase  
       action ← D  
       punish_count ← punish_count − 1  
    else  
       // we are in a “cooperation attempt” phase  
       if last_success = true then  
          // last round’s public good was provided ⇒ keep cooperating  
          action ← C  
       else  
          // last round failed ⇒ start one‐round punishment  
          action ← D  
          punish_count ← 1   // defect for exactly one more round  
       end if  
    end if  

4.  After all players reveal their actions in round t, update:  
    let coop_count = number of C’s in round t  
    if coop_count ≥ m then  
       last_success ← true  
    else  
       last_success ← false  
    end if  

5.  End of game  

Explanation of design choices  
1.  First‐round cooperation: By setting last_success = true at t=1, we begin with a full‐cooperate attempt.  
2.  Win‐Stay: If the group just met the threshold (last_success = true), we keep cooperating, sustaining the public good.  
3.  Lose‐Shift with one‐round punishment: If the group failed (last_success = false) we defect once more (punish), causing a clear signal that cooperation must be restored. After that single defection, punish_count=0 and we immediately attempt to cooperate again.  
4.  Recovery: Because we only punish for one round, we avoid permanent collapse of cooperation and give the group a chance to re‐coordinate on C’s.  
5.  Last‐round defection: Standard backward‐induction says that in round r there is no future to protect, so we defect. That does not harm earlier cooperation attempts.  

Why this is cooperative-minded  
– It relentlessly seeks to hit the m-cooperator threshold in every round except the final one.  
– It never punishes longer than necessary, allowing quick recovery from accidental mis‐cooperation.  
– It begins with and returns to cooperation, building a stable pattern that other cooperative strategies can “lock into.”  
– It imposes a minimal, transparent punishment that discourages free-riding but doesn’t doom the group to endless defection.  

Pseudocode summary  
```
initialize last_success = true, punish_count = 0
for t in 1…r:
   if t == r:
      play D
   else if punish_count > 0:
      play D
      punish_count -= 1
   else if last_success:
      play C
   else:
      play D
      punish_count = 1
   end if

   // observe all actions, count cooperators
   if coop_count >= m:
      last_success = true
   else:
      last_success = false
   end if
end for
```
'''

description_COOPERATIVE_104 = '''
Below is a simple, fully‐specified, “contingent‐cooperator” strategy that (a) kicks off cooperation, (b) sustains it whenever the group just succeeded in meeting the threshold, (c) punishes a failure for exactly one round, then forgives, and (d) defects in the final round to avoid the end‐game collapse.  It requires only observing how many players cooperated in the previous round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
Variables you track:
  punishment_counter ∈ {0,1}  // how many more rounds you will defect in punishment

Parameters:
  n, r, m, k                // as defined in the game

At the start (before round 1):
  punishment_counter ← 0

For each round t = 1,2,…,r do:

  if t == 1 then
    // FIRST ROUND: launch cooperation
    Action ← C

  else if t == r then
    // LAST ROUND: defect (end‐game)
    Action ← D

  else if punishment_counter > 0 then
    // we are in a one‐round punishment phase
    Action ← D
    punishment_counter ← punishment_counter − 1

  else
    // normal, non‐punishment round after round 1, before round r
    let coop_prev = number of players who chose C in round t−1

    if coop_prev ≥ m then
      // group succeeded last round → keep cooperating
      Action ← C
    else
      // group failed last round → punish them for one round
      Action ← D
      punishment_counter ← 1
    end if
  end if

  // submit Action for round t,
  // then observe how many cooperated for use in t+1

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
Explanation of the logic

1. First round (t = 1):  
   Always cooperate, to signal goodwill and—if others follow—secure the bonus immediately.

2. Intermediate rounds (1 < t < r):  
   a. If we are “punishing” (punishment_counter>0), we defect for exactly one round, then auto‐reset to 0.  
   b. Otherwise we look at last round’s total cooperators (coop_prev):  
      – If coop_prev ≥ m, the group just got the bonus. We reciprocate by cooperating again.  
      – If coop_prev < m, the public good failed. We defect once (to avoid being the only sucker) and set punishment_counter=1 so that exactly one round of defection follows—then we go back to cooperation.

3. Last round (t = r):  
   By backward‐induction logic the incentives to cooperate vanish; we defect.

Key properties  
• Cooperative start: we lead with C.  
• Sustained cooperation: as long as the group has just met the threshold, we keep contributing.  
• Limited punishment: one round of defection when the group fails, then forgiveness—this reopens the path to cooperation rather than locking us into permanent defection.  
• End‐game defection: in round r we defect to avoid exploitation.  

This strategy is symmetric, deterministic, easy to implement, and strongly pro‐cooperation when others are too.
'''

description_COOPERATIVE_105 = '''
Below is a simple “firm-but-forgiving” cooperative strategy—an m-threshold version of Tit-for-Tat with one-round punishment—that (i) begins by cooperating, (ii) punishes a failure exactly one round, (iii) always plays C when the group last round met the threshold, and (iv) defects in the very last round (since no future remains to punish you).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. PARAMETERS AND STATE  
   Input parameters (common knowledge):  
   • n, r, m, k  
   Internal state:  
   • last_success  ∈ {true, false}  
   • punish_flag   ∈ {0,1}   // 1 means “we are serving our one‐round punishment”  

2. INITIALIZATION (before round 1)  
   last_success ← true    // assume “success” so we start by cooperating  
   punish_flag  ← 0  

3. ACTION DECISION AT ROUND t = 1,…,r  
   if t == r then  
     // Last round: no incentive to cooperate—defect for immediate +1  
     play D  
   else if punish_flag == 1 then  
     // We’re serving a one‐round punishment  
     play D  
     punish_flag ← 0        // drop punishment next round  
     last_success ← false   // record that we defected  
   else  
     // Normal mode  
     if last_success == true then  
       play C  
       // we’ll update last_success after observing group outcome  
     else  
       // last round group failed to meet m ⇒ punish now  
       play D  
       punish_flag ← 0        // we punish for this one round only  
       last_success ← false   // record our own defection  
     end if  
   end if  

4. UPDATE STATE AT END OF ROUND t<r  
   Observe total number of cooperators in round t:  N_C  
   if N_C >= m then  
     last_success ← true    // group succeeded—restore cooperation  
   else  
     // group failed—set up exactly one round of punishment  
     last_success ← false  
     punish_flag  ← 1       // we will defect in t+1, then resume cooperation  
   end if  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of key features  

1. Begin with C (since last_success was seeded true).  
2. As long as the group meets the threshold (N_C ≥ m), we keep cooperating.  
3. If ever the group falls short (N_C < m), we defect exactly once in the next round (punishment), then return to cooperation.  
4. In the very last round (t = r) we defect because there is no future punishment incentive—maximizing our final‐round payoff.  

This strategy is:  
• Cooperative—willing to contribute whenever the group has been meeting the threshold.  
• Firm—punishes any under-provision immediately.  
• Forgiving—returns to cooperation after just one round of punishment.  
• Simple to implement and to recognize by other players.
'''

description_COOPERATIVE_106 = '''
Below is a single‐player “recipe” for a cooperative trigger strategy.  It tries to achieve the m-cooperator threshold every round, punishes any failure once, then forgives—and it avoids punishment in the last round where no future cooperation can be enforced.

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Name  
  Horizon-Aware Generous Trigger

Principles  
1.  Cooperate by default, to reach the group threshold.  
2.  If in the previous round fewer than m people cooperated (“threshold failure”), defect exactly once as a punishment, then immediately return to cooperation.  
3.  Never punish in the last round (no future) – in the very last round, defect unconditionally to avoid exploitation.  

Parameters known to you: n, r, m, k.  
Internal state:  
  last_success  ← true   (pretend “round 0” was successful)  
  punish_cnt    ← 0      (counts down how many punishment rounds remain)

Strategy (pseudocode)  
for t in 1…r:  
  if t == r then  
    play D  
  else if punish_cnt > 0 then  
    play D  
    punish_cnt ← punish_cnt – 1  
  else if not last_success and (t+1) < r then  
    # threshold failed last round, and there is at least one round after punishment  
    play D  
    punish_cnt ← 1        # punish exactly one round  
  else  
    play C  

  # After all actions are revealed, update last_success
  observe coop_count = number of players who chose C this round  
  last_success ← (coop_count ≥ m)  

End for

Explanation of key points  
1) First round: punish_cnt=0, last_success=true → you play C.  
2) As long as everyone (or at least m people) cooperates, last_success remains true → you keep cooperating.  
3) If a round ever fails to reach m cooperators, last_success=false.  On the very next round (provided it isn’t the last), you defect once (punish_cnt=1), then reset last_success back to true on your next check and resume cooperation.  
4) In round r (the final round), you defect no matter what.  This avoids being exploited in a round where no future punishment is possible.  

Why this is “cooperative”  
• You start by helping to build the public good in every round except the final.  
• You forgive immediately after exactly one round of punishment—so a single stumble doesn’t condemn the whole game.  
• By only punishing failures when there is still at least one round left, you preserve prospects for re-building trust.  

Extensions / tuning  
– You can increase punish_cnt to punish more harshly (at the cost of lowering group payoff).  
– You could make forgiveness probabilistic (“generous tit-for-tat”) by defecting only with some probability after a failure.  
– If communication or private signals were possible, you could target punishments more precisely—but here we rely only on public counts.
'''

description_COOPERATIVE_107 = '''
Below is a single‐agent “cooperative” strategy for the repeated Collective-Risk Dilemma.  It is built around three ideas:  
  1.  Optimistically start by cooperating and keep trying to hit the threshold.  
  2.  If the group succeeds (≥ m cooperators), keep cooperating (win‐stay).  
  3.  If the group fails badly (very few cooperators), protect yourself by defecting until there is fresh evidence the group is trying again; but if the failure was marginal (one or two missing cooperators), keep cooperating to “pull” the group over the line (generous).  
  4.  In the last round, cooperate only if you have strong reason to believe the threshold will be met (to avoid wasting your contribution).  

Notation:  
•  t = current round, 1 ≤ t ≤ r  
•  h[t–1] = number of cooperators observed in round t–1 (sum of all players’ C actions in t–1)  
•  T = ceil(r/2)  (halfway point)  

Strategy description:  

— Initialization (before round 1) —  
Set last_success = true  (optimistic)  

— At the start of round t —  
If t = 1:  
 Play C  
 goto record_and_continue  

If 1 < t ≤ r:  
 // 1) If last round was a clear success, keep cooperating:  
 If last_success == true:  
  Play C  
  goto record_and_continue  

 // 2) If last round narrowly failed, still cooperate to try to reach m:  
 If h[t–1] ≥ (m–1):  
  Play C  
  goto record_and_continue  

 // 3) If last round was a clear failure (too few cooperators), switch to defect:  
 If h[t–1] ≤ (m–2):  
  // But allow a single “test” cooperation every few rounds to see if others changed:  
  If (t mod K) == 0:  // e.g. K = 3  
   Play C  
  Else:  
   Play D  
  goto record_and_continue  

— Special rule for the last round t = r —  
 // Avoid throwing away your endowment if threshold unlikely:  
 If h[r–1] ≥ m: // strong evidence group still cooperating  
  Play C  
 Else:  
  Play D  
 End If  
 goto record_and_continue  

— record_and_continue —  
After playing your action in round t, observe h[t].  
Set last_success = (h[t] ≥ m).  
Proceed to next round (or finish if t = r).  

Parameter choices and comments:  
•  K = 3 (or 2) means: if the group clearly fails, you defect for 2 rounds then test‐cooperate on the 3rd to see if they’ve “woken up.”  This prevents permanent exploitation.  
•  The halfway marker T isn’t strictly needed here, but could be used to tighten or loosen the “test” frequency depending on how many rounds remain.  
•  You always try to cooperate when there’s a good chance of success: immediately after a success or after a marginal failure (m–1 cooperators).  You only withhold when past cooperators are too few to hope for a win.  
•  In the last round, you only cooperate if there is clear evidence (h[r–1] ≥ m) that the group will still meet the threshold, otherwise you defect to protect your endowment.  

This strategy is:  
– Cooperative, because it starts with C and continues to C whenever there is a realistic path to triggering the public‐good payoff.  
– Contingent, because it defects when the group clearly has abandoned cooperation, yet periodically “tests” to re–establish coordination.  
– Punishing enough to deter free‐riding over multiple rounds, but forgiving (generous) when the group nearly succeeded.
'''

description_COOPERATIVE_108 = '''
Below is a single‐strategy recipe—“Conditional One‐Round Punishment” (C1RP)—that is easy to describe, strictly cooperative in spirit, punishes only when you were personally exploited, then immediately forgives, and defects in the last round to avoid the usual backward‐induction sucker’s payoff.

1.  State variables  
    •  last_action ∈ {C, D}, initially “none.”  
    •  r = total rounds, t = current round (1…r).  

2.  Overview of decision rules  
    A.  First round (t=1): Cooperate (C) to signal your willingness.  
    B.  Intermediate rounds (1 < t < r):  
       •  Look at the previous round’s total cooperators, coop_prev.  
       •  If coop_prev ≥ m (threshold met), play C (we enjoyed the group reward, so stay on track).  
       •  Else (threshold failed):  
          –  If you yourself cooperated last round (last_action=C), you were exploited—play D as a one‐round punishment.  
          –  If you yourself defected last round (last_action=D), you had no reason to punish—play C to help the group recover.  
    C.  Last round (t=r): Defect (D).  In a finitely repeated game with perfect observability, the incentive is to defect when no future rounds remain.  

3.  Pseudocode  

    Initialize last_action = none  
    For t in 1…r:  
      if t == 1:  
        action = C  
      else if t == r:  
        action = D  
      else:  
        observe coop_prev = number of players who chose C in round t–1  
        if coop_prev ≥ m:  
          action = C                # success last round ⇒ stay cooperative  
        else:  
          if last_action == C:  
            action = D              # punish one round for being exploited  
          else:  
            action = C              # refrain from punishing again; help restore cooperation  
      play action  
      last_action = action  

4.  Why C1RP is cooperative  
    –  It starts by cooperating and only defects when you personally cooperated but failed to reach the threshold.  
    –  Punishment is limited to exactly one round—so the group can swiftly return to full cooperation.  
    –  By cooperating immediately after your own defection in a failed round, you help the group re‐establish the critical mass.  
    –  It rewards any restoration of threshold‐hitting behavior by returning to pure cooperation.  
    –  It guards against the “sucker payoff” but does not spiral into endless mutual defection.  

5.  Handling special cases  
    •  If two (or more) players adopt C1RP, they will quickly converge on always‐cooperate (except the last round), hitting the threshold each round.  
    •  If only you adopt C1RP and others intermittently defect, you punish them once per misfire but then still try to rebuild cooperation—this tends to push semi‐cooperative opponents toward better group payoffs.  
    •  In the final round you defect to avoid being the only cooperator when no future reward depends on your action.  

This strategy balances a pro‐cooperation stance with minimal, targeted punishment and rapid forgiveness, making it well‐suited to a collective‐risk, threshold‐based repeated game.
'''

description_COOPERATIVE_109 = '''
Below is a single‐strategy proposal—“Threshold-Trigger with Last-Round Adjustment”—that (i) tries to keep the group at or above the m-cooperator threshold each round, (ii) punishes non-cooperation when the threshold is missed, and (iii) free-rides in the very last round if the group has been reliably meeting the threshold.  

1.  State variables  
    •  t: current round, 1 ≤ t ≤ r  
    •  c_prev: number of cooperators observed in round t–1 (undefined at t=1)  
    •  punished: Boolean flag, true if in t–1 we punished a threshold failure  

2.  Initialization  
    punished ← false  

3.  Decision rule at the start of each round t:  
    if t == 1 then  
       play C  
    else if t == r then  
      // Last round: free-ride if group has been reliable; otherwise try to push over threshold  
      if c_prev ≥ m and (not punished or c_prev ≥ m) then  
        play D  
      else  
        play C  
      end  
    else  
      // Rounds 2 through r–1  
      if c_prev ≥ m then  
        // Last round succeeded ⇒ restore full cooperation  
        play C  
        punished ← false  
      else  
        // Threshold failed ⇒ punish once by defecting  
        play D  
        punished ← true  
      end  
    end  

4.  Update after observing round-t outcomes:  
    c_prev ← (# of C’s in round t)  

— Explanation of key pieces —  
•  First round: We start by cooperating to signal good faith.  
•  Punishment: If in round t–1 fewer than m cooperated, we assume someone defected and we defect ourselves for exactly one round (punished = true), hoping to discourage free-riding.  
•  Forgiveness: If the group next round (t) meets m again, we immediately return to cooperation (reset punished ← false). This avoids permanent breakdown.  
•  Last round (t = r): There is no future to protect, so we switch to free-riding (D) if in the previous round the group hit the m threshold (so we still get k). If the group missed the threshold in t = r–1, we play C in t=r in case we’re pivotal in achieving m.  

Pseudocode  

```
function chooseAction(t, c_prev, punished):
    if t == 1:
        return C, punished=false

    if t == r:
        if c_prev >= m and not punished:
            return D, punished   # free‐ride on a reliable group
        else:
            return C, punished

    # intermediate rounds
    if c_prev >= m:
        # group succeeded last round → cooperate
        return C, punished=false
    else:
        # threshold missed last round → punish once
        return D, punished=true
```

Rationale  
— Cooperate immediately, to maximize collective payoff.  
— Defect for exactly one round after any shortfall, which punishes defectors but allows rapid return to cooperation if enough players “learn.”  
— In the final round, defect whenever safe to do so (i.e. the group has been reliably meeting the threshold), capturing the extra private gain.  

This strategy is simple, transparent to other players, and encourages mutual cooperation for all but the very last round.
'''

description_COOPERATIVE_110 = '''
Below is a single‐strategy recipe, called “Contingent Contributor,” that aims to (i) build cooperation, (ii) repair near‐misses of the threshold, and (iii) in the very last round free‐ride safely when possible.  It is entirely deterministic and only uses observables (how many cooperated last round, and what you did).

--------------------------------------------------------------------------------  
STRATEGY: Contingent Contributor  
--------------------------------------------------------------------------------  
State variables (maintained between rounds):  
• round t (starts at 1)  
• prev_coop_count = number of Cs observed in round t–1 (undefined when t=1)  
• my_last_action ∈ {C,D} (undefined when t=1)  

PARAMETERS (known to all): n, r, m, k  

Decision rule at the start of each round t:

1.  If t = 1 (first round):  
    – Play C (cooperate).  
    – Set my_last_action ← C.  
    – Proceed to observe the others and record prev_coop_count at end of round.  

2.  Else if 1 < t < r (interior rounds):  
    – If prev_coop_count ≥ m:  
        •  Threshold was met last round ⇒ keep cooperating to maintain the success.  
        •  Play C; set my_last_action ← C.  
    – Else if prev_coop_count = m−1:  
        •  Group just missed threshold by one ⇒ tip it over.  
        •  Play C; set my_last_action ← C.  
    – Else (prev_coop_count ≤ m−2):  
        •  Even with your C the group would still fail ⇒ no point in contributing.  
        •  Play D; set my_last_action ← D.  

3.  Else if t = r (final round):  
    // Here there is no future punishment, so defect whenever you can free‐ride  
    // safely (i.e. the other cooperators last round already met the threshold).  
    – Let others_prev_coop = prev_coop_count − (my_last_action==C ? 1 : 0).  
    – If others_prev_coop ≥ m:  
        •  Without you the threshold holds ⇒ free‐ride.  
        •  Play D.  
    – Else if others_prev_coop = m−1:  
        •  You are pivotal ⇒ contribute to get the bonus.  
        •  Play C.  
    – Else (others_prev_coop ≤ m−2):  
        •  Even with you it fails ⇒ defect for the sure 1.  
        •  Play D.  

At the end of each round you update prev_coop_count and my_last_action, increment t, and repeat.

--------------------------------------------------------------------------------  
WHY IT IS COOPERATIVE  
1.  First‐round “handshake”: you open by cooperating.  
2.  If the group has just succeeded (≥ m cooperators), you keep cooperating to stabilize the success.  
3.  If they just missed by one, you “tip” the group so you don’t let it fail by one.  
4.  If they failed by two or more, your single contribution cannot save it, so you withhold.  
5.  In the last round you exploit the “free‐riding” opportunity when you safely can (others ≥ m), but still contribute if you are pivotal (others = m−1).  

This strategy (i) fosters and maintains cooperative equilibria whenever possible, (ii) repairs borderline failures, and (iii) avoids needless contributions when they cannot affect the outcome. It is simple to implement and requires only the history of counts of cooperators each round.
'''

description_COOPERATIVE_111 = '''
Below is a proposal for a simple, transparent “group-tit-for-tat” style strategy that (1) pushes the group toward the cooperative threshold, (2) punishes shortfalls immediately, but (3) quickly forgives so cooperation can resume.

STRATEGY NAME  
Threshold-Reciprocal Cooperation (TRC)

1. Data you carry from round to round  
   • last_coop_count = number of players (including you) who cooperated in the previous round  
   • last_action = your own action in the previous round (C or D)

2. Summary of decision rule in words  
   – Round 1: Cooperate unconditionally.  
   – In any round t>1:  
       • If in t–1 at least m players cooperated (last_coop_count ≥ m), then cooperate.  
       • Otherwise (last_coop_count < m):  
            – If you cooperated in t–1, defect this round (punish).  
            – If you defected in t–1, cooperate this round (forgive).  
   – Treat the last round exactly the same as any other round.

3. Rationale  
   • By cooperating whenever the group just met the threshold, you reinforce successful coordination.  
   • If the group fails (too few cooperators), you punish once—but then revert to cooperation, giving the group a clean slate.  
   • This rule is symmetric and transparent; it does not single out any specific player but insists that “if we miss the mark, we all suffer a one‐round penalty, then try again.”

4. Pseudocode

```
# Input parameters: n, m, r, k  (only m is used in the strategy logic)
# Memory variables (initialized before round 1):
last_coop_count ← null
last_action     ← null

for t in 1…r:
   if t == 1:
       action ← C
   else:
       if last_coop_count ≥ m:
           # group did well last time – keep cooperating
           action ← C
       else:
           # group failed last time – punish or forgive
           if last_action == C:
               action ← D   # one‐turn punishment
           else:
               action ← C   # forgive and try again

   # Submit action; then observe coop_count this round:
   # coop_count = number of players (including you) who chose C in round t
   last_coop_count ← coop_count
   last_action     ← action
```

5. Edge‐case handling  
   – First round: we cannot observe any past behavior, so we lead by cooperating.  
   – Last round: we apply the same rule.  We do not defect “end-game style,” because maintaining cooperation even in the last round maximizes the group’s payoff if others also stay true.  
   – Long sequences of failure: TRC never retaliates more than one round.  After a single D, it re-cooperates, preventing endless mutual defection and giving the group frequent fresh opportunities to hit the threshold.

6. Cooperative mindset  
   – TRC’s core is “cooperate whenever the threshold was hit in the previous round.”  
   – Its only defecting behavior is a one‐round group‐wide penalty when the community fails to meet the target.  
   – By immediately forgiving, it signals a constant willingness to rebuild trust and secure the collective reward.

In tournaments of independently generated strategies, TRC will quickly stabilize on full-or-near-full cooperation (reaching the m‐cooperator threshold each round), but it also ensures that a misstep is noticed and corrected without dragging the group into an endless spiral of defection.
'''

description_COOPERATIVE_112 = '''
Below is a single‐strategy, symmetric “conditional cooperator” you can deploy in the threshold public‐goods tournament.  It is designed to

  1. Get you—and anyone playing the same rule—over the m‐threshold almost every round  
  2. Punish one‐shot defectors just enough to deter free‐riding  
  3. Forgive quickly so that isolated missteps don’t collapse cooperation  
  4. Avoid being exploited in the very last round  

--------------------------------------------------------------------------------  
1. High‐Level Description  
   • Start by signaling goodwill (cooperate).  
   • Cooperate as long as everyone cooperated in the immediately preceding round.  
   • If you observe any defection in the last round, punish by defecting for exactly one full round, then return to cooperating.  
   • In the final round (t = r) defect (no future to protect).  

   This is essentially a “Tit‐for‐Tat with 1‐round punishment and endgame defection.”  

--------------------------------------------------------------------------------  
2. Pseudocode  

Let state.punishCountdown ← 0  

For t in 1..r:  
  If t == r then  
    action_t ← D  
    continue  
  EndIf  

  If state.punishCountdown > 0 then  
    action_t ← D  
    state.punishCountdown ← state.punishCountdown – 1  
    continue  
  EndIf  

  If t == 1 then  
    action_t ← C  
    continue  
  EndIf  

  # t > 1, not currently punishing  
  # Look at last round’s profile A_{t–1} ∈ {C,D}^n  
  If ∃ j ≠ you with A_{j,t–1} = D then  
    # Someone defected last round → punish next round  
    action_t ← D  
    state.punishCountdown ← 1  
  Else  
    # Unanimous cooperation last round → keep cooperating  
    action_t ← C  
  EndIf  

--------------------------------------------------------------------------------  
3. Decision Rules Explained  

Round 1:  
   • Cooperate.  (Signal that you’re willing to reach the threshold.)  

Intermediate rounds (2 ≤ t < r):  
   • If you are in the middle of a punishment stint (punishCountdown > 0), defect.  
     – This punishes each defection exactly once.  
   • Otherwise, look back one round:  
     – If every player cooperated in t–1, you cooperate in t.  
     – If you saw any D in t–1, you defect in t and set punishCountdown = 1.  

Last round (t = r):  
   • Defect.  (No future rounds—cooperating only lets others get a free ride +1.)  

--------------------------------------------------------------------------------  
4. Handling Edge Cases  

– Threshold‐failures that arise from everyone playing C (i.e. you see exactly m–1 cooperators):  
  You will have seen no D’s, so you remain in cooperation mode.  This is intentional:  
  you assume shortfall was a coordination glitch, and you’ll keep cooperating to try and hit m next time.  

– Chains of consecutive defections:  
  Each defection only triggers one round of punishment.  If defection continues, you will keep detecting a D in “previous round” and punish again.  

– One‐round “noise” or accidental D:  
  You punish it exactly once, then immediately go back to C if the next turn is all‐C.  Thus you’re both deterrent and forgiving.  

– Last two rounds:  
  • At t = r–1: You follow the ordinary rule (cooperate if no D at t–2; defect if punishing).  
  • At t = r: Always defect, protecting yourself from endgame free‐riders.  

--------------------------------------------------------------------------------  
5. Why This Is Cooperative  

  • If a critical mass (m) of players all use this rule, then from round 1 through r–1 you will always see unanimous C → unanimous continuation of C → the threshold is met every round.  
  • Occasional one‐off defectors are punished just enough to discourage them, but the group quickly forgives and returns to full cooperation.  
  • You never lock into permanent defection (no “grim forever”), so cooperation is robust to stray defections.  
  • By defecting in the very last round you eliminate the incentive for endgame free‐riding—this preserves the threat‐of‐punishment that sustains cooperation earlier.  

In tournament play against other independent LLMs using the same rule, you form a self‐enforcing cooperative bloc that hits the threshold nearly every round while deterring and quickly correcting any deviance.
'''

description_COOPERATIVE_113 = '''
Below is a fully‐specified, stateful “team‐level tit-for-tat with one‐round punishment” strategy.  It is designed to achieve (and sustain) the collective threshold wherever possible, to punish defectors just long enough to deter them, and to forgive quickly so the group can return to cooperation.  We include decision rules for the first round, the penultimate rounds, and the last round.

1.  Overview of the idea  
   • We try to cooperate every round so long as the group is “on track” to meet the threshold.  
   • The first round we simply cooperate to signal goodwill.  
   • If we ever observe a defection in round t – 1, we “punish” in round t by defecting exactly one round.  This drives home that defection is costly—but because we only punish one round and then immediately forgive, the group can return to cooperation swiftly and recover the public‐good payoff.  
   • In the very last round (round r) we defect.  Since there is no future to sustain cooperation, backward induction dictates unilateral defection in round r.

2.  State variables  
   We carry exactly one bit of memory from round to round:  
   punish_flag ∈ {false, true}  
   – punish_flag = false: we are in “normal” mode.  
   – punish_flag = true: we have just executed our one‐round punishment and will now forgive.

3.  Pseudocode description  

   Initialize:  
     punish_flag ← false

   For each round t = 1, 2, …, r do:

     if t == 1 then  
       action ← C  
       // first‐round courtesy  
       punish_flag ← false

     else if t == r then  
       action ← D  
       // last‐round defection by backward induction  
       // punish_flag no longer matters

     else  
       // (2 ≤ t ≤ r–1)
       if punish_flag == true then  
         // we have just punished last round; now forgive  
         action ← C  
         punish_flag ← false

       else  
         // we are in “normal” mode  
         Observe how many players played D in round t–1.  
         if (number_of_D_in_{t–1} > 0) then  
           // someone defected last round: punish them by defecting once  
           action ← D  
           punish_flag ← true  
         else  
           // no defection last round, keep cooperating  
           action ← C  
           punish_flag ← false
         end if
       end if
     end if

4.  Explanation of behavior  
   – First round (t=1): We cooperate unconditionally to give the group the best start.  
   – At any round t (2 ≤ t ≤ r–1):  
     • If we are in “normal” mode and saw at least one defection in t–1, we defect in round t and enter “punish” mode.  
     • If we are in “punish” mode, we play C this round (forgive) and return to “normal” mode.  
     • If no one defected in t–1 and we are in “normal” mode, we cooperate.  
   – Last round (t=r): We defect, since no future punishment is possible.

5.  Why this is cooperative  
   • It maintains the threshold whenever no one defects.  As long as all players follow this strategy, every round t < r will see full cooperation and yield the bonus k.  
   • It punishes any defector—but only for one round.  This is enough to make defection costly, but because we forgive immediately, the group can rapidly return to a successful outcome.  
   • The single‐round punishment avoids the trap of permanent defection (as happens in a Grim Trigger), and yet still deters systematic defectors.  
   • Because punishment only lasts one round, the vast majority of rounds (all except the first few recovery rounds after a slip, and the very last round) will produce the cooperative payoff of (1 – c_i) + k = k for cooperators (and k+1 for any one‐shot defector who exploits that round).

6.  Edge cases  
   • If multiple defections occur in the same round, we still punish only one round in total.  That is, no matter how many players defected at t–1, we switch once to D at t, then immediately switch back to C at t+1.  
   • Slips (accidental defections) incur exactly one round of lost bonus, then full recovery.  
   • In the unlikely event that defections cascade (others copy the same punish‐forgive rule), the maximum damage is two successive rounds without the bonus—then cooperation resumes.  
   • Round r is always D; this is standard backward induction in a finitely repeated game with no communication.

This strategy balances strong cooperation (it seeks the k-reward every round except the final one) with minimal, targeted punishment of defectors, and rapid forgiveness so the group never gets stuck in permanent failure.
'''

description_COOPERATIVE_114 = '''
Below is a simple “forgiving-trigger” strategy that (1) tries to hit the threshold every round, (2) punishes any group‐level failure by one round of defection, then (3) immediately forgives and resumes cooperation.  It only requires remembering whether the last round met the cooperation threshold and whether you’re in a one-round punishment phase.

1. State variables  
   • last_success (bool): true if in the previous round ≥ m players cooperated; false otherwise.  
   • punishing (bool): true when you are using your one‐round punishment, false otherwise.

2. Initialization  
   round t = 1:  
     last_success = true    (pretend “we succeeded” so you start by cooperating)  
     punishing   = false

3. Per-round decision rule  
   for t = 1 to r:  
     if t == 1 then  
       play C  
     else  
       if punishing == true then  
         play D      # carry out your one‐round punishment  
       else  
         play C      # otherwise cooperate

     # AFTER observing all n actions this round, update state for next round  
     let coop_count = number of players (including you) who played C this round  
     let this_round_success = (coop_count ≥ m)

     if punishing == false AND this_round_success == false then  
       # group failed → enter punishment next round  
       punishing   = true  
     else  
       # either we just punished, or we succeeded → reset to cooperation mode  
       punishing   = false

     last_success = this_round_success

4. Edge‐case notes  
 • First round (t=1):  we cooperate unconditionally to signal willingness.  
 • Punishment is exactly one round long: this deters free‐riding but is quickly forgiven so as not to lock the group into perpetual defection.  
 • Last round (t = r):  the same rule applies.  If round r–1 met the threshold, you cooperate; if round r–1 failed, you punish (defect).  You cannot punish beyond round r, so any defection in round r will go unpunished—but by then the game is over.  

5. Why it’s cooperative  
 • As long as everyone follows it, the group will hit the threshold every round (because one defection in round t immediately triggers exactly one round of discipline and then full cooperation again).  
 • The one‐round punishment is credible (you will defect next round) yet forgiving (you return to cooperation right after), so it stabilizes high levels of contribution without permanent breakdown.  
 • By starting with cooperation and resuming it after any slip‐up, you send a clear “let’s cooperate” signal throughout the match.
'''

description_COOPERATIVE_115 = '''
Below is a single‐strategy proposal—call it “Threshold‐Rescue Conditional Cooperation (TRCC)”—that aims to sustain cooperation in the repeated collective‐risk dilemma, punish persistent defectors, and still rescue near‐misses.  

1. High‐Level Idea  
   • Start fully cooperative.  
   • In any middle round t (2 ≤ t < r), cooperate if last round was a clear success (≥ m cooperators).  
   • If the group just missed the threshold by one (exactly m–1 cooperators), step in and “rescue” by cooperating.  
   • If the group failed by two or more, punish by defecting. That deters chronic free‐riding.  
   • In the final round (t = r), defect (standard backward‐induction “last‐round” logic).  

2. Decision Rules in Detail  
   Let t = current round (1…r); let prev_coops = number of cooperators in round t–1; let my_prev = my action in t–1.  

   Round 1:  
     – Cooperate.  (We give cooperation a chance.)  

   Rounds 2 ≤ t < r:  
     – If prev_coops ≥ m:  
         • Cooperate.  (Success last round—reward continuation.)  
     – Else if prev_coops = m–1:  
         • Cooperate.  (Rescue a one‐player short failure.)  
     – Else (prev_coops ≤ m–2):  
         • Defect.  (Failure by ≥2 means too many free‐riders; withdraw.)  

   Round r (last):  
     – Defect.  (One‐shot incentive to free‐ride.)  

3. Rationale and Cooperative Alignment  
   – By cooperating whenever the group has succeeded, we reward all who took part.  
   – By attempting a rescue when the group barely misses (m–1), we minimize rounds of catastrophic failure and keep up momentum.  
   – By refusing to prop up larger failures (defections ≥2 above tolerance), we signal to others that persistent defection will lead to loss of safety.  
   – Defecting last round is unavoidable under standard backward induction, but by then we have cemented cooperation in all earlier rounds.  

4. Pseudocode  

   // Parameters: n, r, m, k  (k not used in decision logic)  
   // Variables tracked each round: prev_coops, my_prev  

   initialize prev_coops ← undefined, my_prev ← undefined  

   for t in 1…r do  
     if t == 1 then  
       action ← C  
     else if t == r then  
       action ← D  
     else  
       // middle rounds  
       if prev_coops ≥ m then  
         action ← C  
       else if prev_coops == m–1 then  
         action ← C  
       else  
         action ← D  
       end if  
     end if  

     play(action)  
     observe all players’ choices this round → compute next_prev_coops  
     prev_coops ← next_prev_coops  
     my_prev ← action  
   end for  

5. Handling Edge Cases  
   – If there is noisy observation or ties, the rule is unambiguous—only raw counts matter.  
   – If m=2, then rescuing at m–1 means rescuing every 1‐cooperator round. That’s still coherent: one cooperator last round → you step in.  
   – If failure by multiple, you defect—and you will only return to C once the group has self‐corrected to ≥m or to m–1.  
   – Last round D is immovable; opponents learn you were solid until then, so cooperation is fostered in r–1 rounds.  

This TRCC strategy is:  
   • Cooperative—cooperates by default and rescues near‐misses.  
   • Reactive—punishes repeated or large‐scale failures.  
   • Simple—no hidden states beyond tracking the last round’s cooperators.  
   • Robust—secures success whenever the group was close to a win, and rewards successful cooperation with continued goodwill.
'''

description_COOPERATIVE_116 = '''
Below is a single‐algorithm “conditional‐cooperator” that aims to sustain cooperation over all r rounds, yet punishes repeated failures and forgives occasional noise.  It is purely observational (no cross‐round signaling beyond actions), starts out fully cooperative, and only defects in a controlled way when the group repeatedly fails to reach the threshold.  In draft form:  

Name: Group-Reciprocity with Forgiveness (GRF)

Parameters you know (common knowledge):  
  n, r, m, k  

State variables maintained by your strategy:  
  fail_streak ← 0    # number of consecutive rounds so far in which cooperators < m  
  last_action ← C   # your own last action; initialized to C  

Decision rule for round t = 1…r:  

1.  First round (t = 1):  
      play C  
      last_action ← C  
      go to collect outcome  

2.  Observe at end of round t–1:  
      let coop_count = number of players (including you) who chose C in round t–1  

   Update fail_streak:  
      if coop_count ≥ m then  
         fail_streak ← 0  
      else  
         fail_streak ← fail_streak + 1  

3.  Choose action in round t (< r):  
   a.  If fail_streak = 0  (previous round was “successful”):  
         play C  
   b.  Else if fail_streak = 1  (a single failure):  
         play C   # forgive one miss  
   c.  Else  (fail_streak ≥ 2):  
         play D   # punish repeated group failure  

   last_action ← your chosen action  

4.  Special rule for last round t = r:  
   We still try to cooperate once more, because if we all reach m we get the extra k‐bonus, even though there is no future.  BUT if the group has already failed twice in a row (fail_streak ≥ 2), then we assume cooperation has broken down and we defect to secure the sure 1‐point private payoff.  

   Concretely, at t = r:  
     if fail_streak ≤ 1 then play C else play D  

5.  Go to collect outcome; repeat until t = r  

Pseudocode  

```
# Initialization
fail_streak = 0
last_action = C

for t in 1..r:
    if t == 1:
        action = C
    else if t == r:
        # Last‐round rule
        if fail_streak <= 1:
            action = C
        else:
            action = D
    else:
        # Intermediate rounds
        if fail_streak == 0:
            action = C
        elif fail_streak == 1:
            action = C
        else:  # fail_streak >= 2
            action = D

    play(action)
    last_action = action

    # Observe outcomes
    coop_count = # of players who chose C this round
    if coop_count >= m:
        fail_streak = 0
    else:
        fail_streak += 1
```

Explanation of design choices  
1.  “Start by cooperating”: signals willingness to build the public good immediately.  
2.  “Forgive a single slip”: if the group just missed the threshold once, keep cooperating—treat it as noise, avoid punishing an honest mistake.  
3.  “Punish repeated failures”: if the threshold is missed two rounds in a row, switch to defection once, pressuring others to return to cooperation or be left exploiting you.  
4.  “Forgive after punishment”: because once the group hits the threshold again, fail_streak resets to 0 and you resume cooperation.  
5.  “Last‐round exception”: even though backward induction suggests defection in the final round, we still attempt cooperation if the group appears operative (fail_streak ≤ 1), in order to get the collective bonus k.  Only if the group has already broken down twice consecutively do we defect to guard the private payoff.  

Why this is cooperative  
- It starts and (in most circumstances) stays cooperative.  
- It only defects to punish a genuine breakdown, not to exploit one‐off misses.  
- It does not “grudge” indefinitely—once cooperation is restored, it goes back to full cooperation.  
- In the final round, it still tries to attain the collective bonus if the group has been “on track,” preserving cooperative spirit through to the end.
'''

description_COOPERATIVE_117 = '''
Below is a single‐strategy proposal for the repeated Collective Risk Dilemma.  It is designed to (i) foster and sustain cooperation whenever the group has been meeting the threshold, (ii) punish lapses just long enough to deter free‐riding, (iii) forgive quickly so cooperation can rebuild, and (iv) handle the first and last rounds deliberately.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
NAME  
   Generous Threshold‐Tit-for-Tat (GTT)

PARAMETERS  
   n = number of players  
   r = total rounds  
   m = threshold of cooperators needed each round  
   k = public reward if ≥ m players cooperate  

INTERNAL STATE  
   punish_flag ∈ {0,1}  (when 1, we are in a one‐round punishment)  
   prev_coops ∈ {0,…,n} (count of cooperators we observed in last round)

INITIALIZATION  
   punish_flag ← 0  
   prev_coops ← n   (pretend “last round” was fully cooperative)

STRATEGY  
 For each round t = 1,…,r do  
   if t = 1 then  
     play C  
   else if t = r then  
     play D     # end‐game defection  
   else if punish_flag = 1 then  
     # still punishing  
     play D  
     punish_flag ← 0  
   else  
     # normal mode: check whether last round’s cooperation met threshold  
     if prev_coops ≥ m then  
       play C  
     else  
       # group failed; punish this round, then forgive  
       play D  
       punish_flag ← 1  
     end  
   end  

   # AFTER observing all n actions this round, update prev_coops  
   prev_coops ← number of players (including yourself) who played C  
 end

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
EXPLANATION  

1. First Round (t=1):  
   – Cooperate to signal willingness.  

2. “Normal” Rounds (2 ≤ t < r):  
   – If in the *previous* round at least m players cooperated, we assume the group is on track: we cooperate.  
   – If the group *failed* (prev_coops < m), we defect *once* as a brief punishment, then automatically revert to cooperation the very next round.  This 1‐round “tit-for-tat” punishment is enough to discourage repeated free‐riding but not so harsh as to collapse cooperation forever.  

3. Last Round (t=r):  
   – We defect.  (In a one‐shot game, defection strictly dominates if the remaining players still meet the threshold without you.  By defecting in the last round, we avoid being exploited by cooperators who would otherwise incur cost c=1 for no additional strategic payoff benefit.)  

4. Forgiveness:  
   – After exactly one round of defection, punish_flag resets and we attempt to rebuild cooperation immediately.  

5. Edge Cases & Robustness:  
   – If the group *never* manages to hit the threshold in early rounds, our strategy will settle into a cycle of  
       “observe failure → one‐round punishment → attempt cooperation → observe failure → punish → …”  
     so we do keep testing for renewed cooperation instead of permanent defection.  
   – If the group stabilizes on cooperation, we stay fully cooperative (mimicking “win–stay, lose–shift” at the group‐level).  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode Summary

   punish_flag ← 0  
   prev_coops  ← n  

   for t in 1..r do  
     if t = 1 then  
       action ← C  
     else if t = r then  
       action ← D  
     else if punish_flag = 1 then  
       action ← D  
       punish_flag ← 0  
     else if prev_coops ≥ m then  
       action ← C  
     else  
       action ← D  
       punish_flag ← 1  
     end  

     observe all actions this round  
     prev_coops ← count of C’s this round  
   end  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Why this works

– It rewards successful group coordination (keeps cooperating when the threshold is met).  
– It deters exploitation with a short, predictable punishment whenever the group falls short.  
– It forgives quickly to give the group repeated chances of recovery.  
– It respects the one‐shot incentive to defect in the final round, avoiding last‐round exploitation.  

This design shares the spirit of generous tit-for-tat adapted to a public‐goods threshold environment.
'''

description_COOPERATIVE_118 = '''
Below is a fully specified, “group‐Tit-for-Tat with single-round punishment and immediate forgiveness” strategy.  It (i) starts by cooperating, (ii) punishes any round in which the community project failed by defecting exactly once, (iii) then immediately returns to cooperation, and (iv) always cooperates in the very last round to signal goodwill and maximize collective payoff.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
STATE VARIABLES  
  state ∈ {NORMAL, AFTER_DEFECT}  
    – NORMAL: we’re in our default mode  
    – AFTER_DEFECT: we just defected to punish and will now forgive  

INITIALIZATION  
  state ← NORMAL  

AT THE START OF EACH ROUND t = 1,2,…,r:  
  if t = 1 then  
    play C  
    (state remains NORMAL)  
    continue to next round  
  end if

  if t = r then  
    // last round: unconditional cooperation  
    play C  
    // no need to update state  
    continue to next round  
  end if

  if state = AFTER_DEFECT then  
    // forgiveness move  
    play C  
    state ← NORMAL  
    continue to next round  
  end if

  // otherwise (state = NORMAL, t not first or last)  
  let coop_prev = number of players who played C in round t−1  

  if coop_prev ≥ m then  
    // last round succeeded → keep cooperating  
    play C  
    // state remains NORMAL  
  else  
    // threshold failed → punish once  
    play D  
    state ← AFTER_DEFECT  
  end if  

END LOOP  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
EXPLANATION / RATIONALE  

1. First‐round cooperation (t=1) establishes that we’re willing to invest.  
2. Whenever the community project fails (fewer than m cooperators), we defect exactly one round later.  That punishes non‐cooperators by denying them our contribution when it’s needed most.  
3. Immediately after punishing, we forgive (“AFTER_DEFECT” state) by returning to cooperation unconditionally.  This gives the group a clear path to restore joint success.  
4. In all other NORMAL‐state rounds, if the previous round succeeded (coop_prev ≥ m) we keep cooperating; if it failed, we switch to punish.  
5. In the very last round we cooperate regardless—there’s no future to protect, but we still maximize collective payoff and signal our overall cooperativeness.  

This strategy is simple, easy to read off from observed histories, deters repeated free-riding, and yet never “gets stuck” in endless mutual punishment: one punishment round is always followed by immediate restoration of cooperation.
'''

description_COOPERATIVE_119 = '''
Below is a single–player “reputation-based conditional cooperator” that (1) tries to guarantee at least m cooperators each round, (2) punishes persistent defectors, (3) allows recovery from accidental failures, and (4) is fully specified for first, intermediate and last rounds.  You can tune the reputation bounds and update step to your tournament environment.

— — —  
STRATEGY NAME  
Reputation-based Conditional Cooperator (“RBCC”)

PARAMETERS (you choose before the tournament begins)  
  R_min = 0       // lower bound on reputation  
  R_max = 2·m     // upper bound  
  R_init = m      // neutral starting reputation  
  Δ = 1           // step size for reputation updates  

INTERNAL STATE  
  For each opponent j ≠ yourself, maintain an integer reputation R[j] ∈ [R_min, R_max].

INITIALIZATION (before round 1)  
  For every j ≠ you, set R[j] ← R_init.

DECISION RULE (for rounds t = 1…r)  
1. If t = 1 then  
     play C  
   else  
     • Let S = { j ≠ you  |  R[j] ≥ m }  
     • Let potential_cooperators = |S| + 1    // +1 because you can choose C  
     • If potential_cooperators ≥ m  
         play C  
       else  
         play D

EDGE–CASE RULES  
  • Last round (t = r): apply the same rule.  
    (Optionally, if you want to “go all-in” for collective good, you can override and always play C in t = r.  
     but pure payoff-maximizers often still use the rule above.)

UPDATING REPUTATIONS (after observing everyone’s actions in round t)  
  For each opponent j ≠ you:  
    if j played C in round t  
       R[j] ← min(R_max, R[j] + Δ)  
    else  // j played D  
       R[j] ← max(R_min, R[j] − Δ)

INTUITION AND PROPERTIES  
1. “Belief filter”:  You only contribute (play C) when you believe there are at least (m−1) other likely cooperators.  
2. “Lenient punishment”:  Defection by j lowers R[j], so you stop counting j among your m-1 helpers.  
3. “Forgiveness and recovery”:  After a defection, j may cooperate in later rounds and rebuild R[j] back toward m, allowing reintegration.  
4. “First-round trust”:  Starting on C signals willingness to cooperate.  
5. “Simplicity”:  Only 1-bit history per opponent per round (cooperate/defect) and a small integer reputation to track.  
6. “Fully specified”:  Covers t = 1, 1 < t < r, and t = r.

PSEUDOCODE  

  // Parameters: R_min, R_max, R_init, Δ  
  initialize for all j ≠ me: R[j] = R_init  

  for t in 1…r do  
    if t == 1 then  
      my_action = C  
    else  
      S = count of opponents j with R[j] ≥ m  
      if (S + 1) ≥ m then  
        my_action = C  
      else  
        my_action = D  

    play(my_action)  
    observe actions a[j] for all j ≠ me  

    // Reputation update  
    for each j ≠ me do  
      if a[j] == C then  
        R[j] = min(R_max, R[j] + Δ)  
      else  
        R[j] = max(R_min, R[j] − Δ)  

  end for

TUNING AND VARIANTS  
• You can make Δ fractional or >1 for faster punishment/recovery.  
• You can shift R_init above or below m to bias initial trust.  
• In very short games you might soften punishment (use Δ<1) so you never “burn bridges.”  
• In the last k rounds you could switch to unconditional cooperation if you care about group payoff more than tournament position.

This strategy is explicitly cooperative—it starts by trusting, seeks only to defect when it genuinely fears the group as a whole will not meet the threshold if it cooperates, and always gives opponents a chance to redeem themselves.
'''

description_COOPERATIVE_120 = '''
Below is a single‐strategy design – a “forgiving threshold‐trigger” – that aims to sustain cooperation up to the last round, punish defections quickly, then forgive so cooperation can rebuild.

1.  Strategy Intuition  
    - Start cooperative to signal willingness.  
    - In each non‐final round, cooperate if (and only if) the group just met the cooperation threshold without signs of cheating.  
    - If the last round was “bad” (threshold missed, or threshold met but someone defected), punish by defecting exactly one round.  
    - After one round of punishment, return to the cooperative norm.  
    - In the final round, defect (no future to enforce cooperation).

2.  State Variables  
    punish_counter ∈ {0,1}  
      – number of remaining punishment rounds  
    t = current round index, t=1…r  

3.  Play Rules  

  Initialization (before round 1):  
    punish_counter ← 0  

  For each round t = 1…r do:  
    if t = r then  
      •  Action ← D  
      •  (No update to punish_counter needed – game ends.)  
      break  

    else if punish_counter > 0 then  
      •  Action ← D  
      •  punish_counter ← punish_counter − 1  
      continue  

    else if t = 1 then  
      •  Action ← C  
      •  (No history yet; send cooperative signal.)  
      continue  

    else  (2 ≤ t < r and punish_counter = 0)  
      Let last_C = number of cooperators (including yourself) in round t−1.  
      if last_C = n then  
        •  Full cooperation last round → Action ← C  
      else   
        •  Either threshold missed (last_C < m)  
           or met but some defected (m ≤ last_C < n)  
           → trigger one‐round punishment:  
             – Action ← D  
             – punish_counter ← 1  

4.  Explanation of Key Features  
  •  First round: unconditional C to “reach out.”  
  •  Normal play: only cooperate if—and only if—the preceding round was entirely clean (all cooperated).  
     – This rewards perfect compliance.  
  •  Punishment: one round of defection immediately after any “bad” event.  
     – Quick, proportional, and then forgiving.  
  •  Forgiveness: after one round of punishment we reset and attempt full cooperation again.  
  •  Last round: defect. No future to enforce cooperation, so best response is D.

5.  Pseudocode  

  initialize punish_counter ← 0  
  for t in 1…r do  
    if t == r:  
      play D  
      break  
    end if  

    if punish_counter > 0:  
      play D  
      punish_counter ← punish_counter − 1  
      continue  
    end if  

    if t == 1:  
      play C  
      continue  
    end if  

    # t in [2, r−1] and punish_counter=0  
    observe last_C  # number of cooperators in round t−1  
    if last_C == n:  
      play C  
    else:  
      play D  
      punish_counter ← 1  
    end if  
  end for

6.  Why This Is Cooperative  
  - It achieves the group threshold whenever everyone respects the protocol (all‐C rounds reproduce).  
  - Defections or threshold‐failures are met with immediate but short punishment.  
  - Punishment is minimal (1 round), so cooperation can recover quickly if mistakes occur.  
  - By cooperating robustly up to round r−1, the group can harvest (1−1)+k each round.  

This strategy balances clear incentives to cooperate, swift response to deviations, and prompt forgiveness—key ingredients for sustained collective success in a repeated risk‐threshold public‐good setting.
'''

description_COOPERATIVE_121 = '''
Below is a single‐strategy proposal that (1) tries to ensure the group‐threshold m is met each round via conditional cooperation, (2) punishes shortfalls by a one‐round “defection” before returning to cooperation, and (3) defects in the last round (where cooperation is a strictly dominated action) to protect your own payoff.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
High‐Level Description  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
We maintain two pieces of state between rounds:  
  • lastOutcome ∈ {“success”, “failure”}, denoting whether ≥ m players cooperated in the previous round  
  • punishPhase ∈ {0,1}, a one‐round counter for punishing a failure  

Decision rule by round t:  
1. If t = 1, cooperate (C).  
2. Else if t = r (last round), defect (D).  
3. Else (1 < t < r):  
     a. If punishPhase = 1 → play D, then set punishPhase←0.  
     b. Else (punishPhase = 0):  
         • If lastOutcome=“success” → play C.  
         • If lastOutcome=“failure” → set punishPhase←1; play D.  

After all players’ actions in round t are observed, update:  
  if (# of cooperators ≥ m) then lastOutcome←“success” else lastOutcome←“failure.”  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Inputs:  n, r, m, k  
State variables (persist across rounds):  
    lastOutcome ← “success”   # pretend success so we start by cooperating  
    punishPhase  ← 0          # no pending punishment  

For t in 1…r:  
    if t == 1:  
        A_t ← C  
    else if t == r:  
        A_t ← D  
    else:  
        if punishPhase == 1:  
            A_t ← D  
            punishPhase ← 0        # punishment spent  
        else:  
            if lastOutcome == “success”:  
                A_t ← C  
            else:  
                punishPhase ← 1      # schedule one round of punishment  
                A_t ← D  

    “Play” A_t.  
    Observe total cooperators count_t.  
    if count_t ≥ m: lastOutcome ← “success”  
    else:         lastOutcome ← “failure”  

End for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Rationale and Cooperative Mindset  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• We start by cooperating, signaling willingness.  
• As long as the group meets the threshold each round (lastOutcome=“success”), we continue to cooperate, ensuring stability of the public good.  
• If the threshold fails, we “punish” the group by defecting exactly one round—enough to signal dissatisfaction but not so long as to collapse all future cooperation.  
• After that single‐round punishment, we immediately return to cooperation, giving the group a chance to “reset.”  
• In the final (rth) round, because defection strictly dominates cooperation in a one‐shot threshold game, we defect to protect our own payoff, preventing unilateral exploitation.  

This strategy is robust (tolerates occasional failures), clear (players can infer when they’ve failed vs. succeeded), and cooperative (only punishes one round before returning to support the public good).
'''

description_COOPERATIVE_122 = '''
Below is a single‐strategy recipe for sustaining full cooperation in the repeated collective‐risk dilemma.  It is a simple “forgiving trigger” (a limited‐punishment) rule which (i) starts by cooperating, (ii) cooperates as long as the group has been meeting the threshold, (iii) punishes any round in which the threshold fails by defecting for exactly one round, then (iv) immediately returns to cooperation.  This rule is easy to describe, punishes lapses enough to deter them, but is forgiving so the group can quickly re‐coordinate.

1.  State variables  
   • punishing : integer counter of remaining punishment rounds (initially 0)  
   • last_coop_success : Boolean flag (true if in the previous round ≥ m players cooperated; initialize true so we begin in “cooperative mode”)

2.  Parameters  
   • n ≥ 2, r > 1, 1 < m < n, k > 1  (as given)  
   • P = 1  (length of punishment—here one round; can be tuned to greater P if greater deterrence is desired)

3.  Decision rule (each round t = 1..r)  
   if t == 1 then  
     action ← C        // start by cooperating  
   else if punishing > 0 then  
     action ← D        // still punishing last failure  
   else  
     action ← C        // in cooperative mode  

4.  After observing the outcome of round t (all players’ actions):  
   let S = number of cooperators this round  
   if S ≥ m then  
     // threshold met  
     last_coop_success ← true  
     punishing ← 0     // reset any punishment  
   else  
     // threshold failed → trigger punishment  
     last_coop_success ← false  
     punishing ← P     // punish for next P rounds  

5.  Edge cases  
   • First round (t=1): no history, so we cooperate.  
   • Punishment period: exactly P rounds of defection immediately after any threshold failure, then revert.  
   • Last round (t=r): follow the same rule.  Even though classical backward induction would say “defect in the last round,” because all others are following the same forgiving‐trigger you will most often see cooperation in round r if no failure occurred in round r–1.  

6.  Why it is cooperative  
   – As long as all players adopt the same rule, the group will quickly coordinate on “always C” and hit the threshold every round, yielding payoff (1–1)+k = k each round.  
   – A single slip (or defection by one rogue strategy) causes exactly one round of group defection (punishment), after which we return to full cooperation.  This punishes deviators but does not let the game collapse indefinitely.  
   – Because punishment is limited to one round, accidental mis‐cooperation or “random noise” does not trigger endless retaliation.  

Pseudocode summary:

```
initialize:
  punishing ← 0
  last_coop_success ← true    // assume we start in good standing

for t from 1 to r:
  if t == 1:
    play C
  else if punishing > 0:
    play D
  else:
    play C

  observe S = number of players who played C
  if S >= m then
    last_coop_success ← true
    punishing ← 0
  else
    last_coop_success ← false
    punishing ← 1    // punish with one round of D
```

By following this rule, you provide a clear cooperative signal, maintain the public good as long as everyone else does, and enforce a minimal but effective punishment when the group fails to reach the critical mass.
'''

description_COOPERATIVE_123 = '''
Below is a simple “threshold‐trigger with one‐round forgiveness” strategy.  It is designed to maximize the chance that every round at least m players contribute, while still punishing mass‐defection and avoiding the known end‐game collapse.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: CRC-Forgiving-Trigger

Notation and memory:  
•   t = current round, 1 ≤ t ≤ r  
•   prev_C = number of cooperators observed in round t−1 (undefined for t=1)  
•   punishing = a Boolean flag (initially false)  
•   punish_count = integer counter (initially 0)  

Decision rule for round t:  
1.  If t == 1:  
        play C  
2.  Else if t == r:  
        play D   (end-game defection)  
3.  Else  (1 < t < r):  
     a.  If punishing == false:  
         •  If prev_C ≥ m:  
               play C  
         •  Else  (prev_C < m):  
               play D  
               punishing ← true  
               punish_count ← 1  
     b.  Else  (punishing == true):  
         •  play D  
         •  punish_count ← punish_count + 1  
         •  If punish_count ≥ 1:        ← one‐round punishment  
               punishing ← false  
               punish_count ← 0  

Update memory at end of each round:  
    prev_C ← (number of players who chose C in this round)

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of key points

1.  First round: we cooperate to signal willingness to build trust.  
2.  Middle rounds (2 ≤ t ≤ r−1):  
    –  If in the previous round the group met the threshold (prev_C ≥ m), we presume everyone is cooperating and continue to cooperate.  
    –  If the previous round failed (prev_C < m), we “punish” by defecting for exactly one round (to lower defectors’ short‐term gain and signal that failing the threshold has a cost), then return to cooperation.  
3.  Last round t = r: defect.  (Standard finite‐horizon reasoning: no future to enforce cooperation.)  
4.  One‐round forgiveness prevents the system from getting stuck in perpetual mutual defection after a single failure.  If the group recovers by cooperating again, CRC-Forgiving-Trigger rejoins them immediately.  

This strategy:  
•  Is cooperative whenever the group has been reliably hitting the threshold.  
•  Properly punishes mass‐defection but allows reconciliation.  
•  Avoids futile cooperation in the last round.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  

initialize punishing ← false  
initialize punish_count ← 0  
// No prev_C for round 1

for t in 1..r do  
    if t == 1 then  
        action[t] ← C  
    else if t == r then  
        action[t] ← D  
    else  
        if not punishing then  
            if prev_C ≥ m then  
                action[t] ← C  
            else  
                action[t] ← D  
                punishing ← true  
                punish_count ← 1  
        else  // punishing == true  
            action[t] ← D  
            punish_count ← punish_count + 1  
            if punish_count ≥ 1 then  
                punishing ← false  
                punish_count ← 0  
        end if  
    end if

    // After all players act, observe count of cooperators in round t  
    prev_C ← count_of_C_in_round(t)  
end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––   

This rule set clearly specifies when you cooperate vs. defect, handles first and last rounds, punishes failures, but quickly forgives to preserve cooperation over the bulk of the game.
'''

description_COOPERATIVE_124 = '''
Below is a single‐strategy proposal—call it the “One‐Period Forgiving Trigger”—that (i) starts out fully cooperative, (ii) punishes a failed threshold by a single round of defection, then (iii) immediately forgives and returns to cooperation, and (iv) defects in the very last round to avoid the one‐shot temptation.

1.  State variables  
    •  prev_coop_count ← n  (we “pretend” the nonexistent round 0 succeeded)  
    •  punish_next ← false  

2.  Decision rule, each round t = 1…r:  
    if t = 1 then  
        play C  
    else if t = r then  
        play D      ⟶ last‐round defection is dominant  
    else if punish_next = true then  
        play D      ⟶ single‐round punishment  
    else if prev_coop_count ≥ m then  
        play C      ⟶ threshold met last round, keep cooperating  
    else  
        play D      ⟶ safety: if somehow neither of the above, defect  

3.  Update after observing all players’ actions in round t:  
    let coop_count ← number of players who chose C in round t  
    if coop_count ≥ m then  
        prev_coop_count ← coop_count  
        punish_next ← false    ⟶ group succeeded, clear any pending punishment  
    else  
        prev_coop_count ← coop_count  
        punish_next ← true     ⟶ schedule a one‐round punishment next round  

——————————————————————————  
Rationale & properties  
– First round cooperation signals goodwill.  
– Whenever the group reaches the threshold, we stay in the cooperative regime.  
– A single round of defection punishes any failure to meet m (deterring under‐contribution) but does not spiral into permanent defection.  
– After that one‐round punishment we “forgive” immediately, giving the group another chance to coordinate.  
– In the last round t = r we defect (no future to enforce cooperation).  

This strategy is easy to implement, fully reciprocates success and failure at the group level, and maximizes the chance of sustaining threshold cooperation throughout the iterated game.
'''

description_COOPERATIVE_125 = '''
Below is a fully specified, cooperative‐minded strategy for the repeated Collective Risk Dilemma.  It (1) builds cooperation from round 1, (2) lightly punishes “free riders” who benefit without contributing, (3) forgives quickly so the group can recover, and (4) defects in the final round (since there is no future to protect).

---

Strategy name: Forgiving Free-Rider Punishment (FFP)

Global parameters known to all players:
  n, r, m, k

Local state (for our agent):
  punishing ← false   // flag indicating “we are in a one‐round punishment”

Decision rule for round t:

1) If t = 1 (first round):
     play C  
   Explanation: we start by cooperating to signal willingness.

2) Else if t = r (last round):
     play D  
   Explanation: no future rounds remain, so we defect.

3) Else if punishing = true:
     play D  
     punishing ← false  
   Explanation: carry out exactly one round of punishment, then reset.

4) Else look at last round’s outcome:
     Let coop_prev = number of players who cooperated in round t – 1.

   a) If coop_prev ≥ m and coop_prev < n:
        // threshold met but at least one free-rider defected
        punishing ← true
        play D  
     Explanation: we punish the group for allowing free riding.

   b) Otherwise:
        play C  
     Explanation:  
       – If coop_prev = n (everyone cooperated), reward it by cooperating again.  
       – If coop_prev < m (project failed), deem it an accident or mis‐coordination and immediately seek to rebuild cooperation.

---

Pseudocode

  initialize punishing ← false

  for t from 1 to r do
    if t = 1 then
      action[t] ← C

    else if t = r then
      action[t] ← D

    else if punishing = true then
      action[t] ← D
      punishing ← false

    else
      // observe previous round
      coop_prev ← count of C’s in round t–1

      if (coop_prev ≥ m) and (coop_prev < n) then
        // threshold succeeded but someone free-rode
        punishing ← true
        action[t] ← D
      else
        // either full cooperation or total failure
        action[t] ← C
      end if
    end if
  end for

---

Why this is cooperative:
• We always start by cooperating (round 1).  
• We forgive any pure group failure (coop_prev < m), so one bad round does not trigger endless punishment.  
• We punish only when the group succeeds and yet some defected—i.e. when there really is free-riding—by defecting for exactly one round.  
• After punishment, we immediately return to cooperation, allowing the group to re‐establish trust.  
• We defect in the very last round to protect against end-game exploitation (since no future rounds remain).

This strategy fosters high overall cooperation while still deterring free-riding.
'''

description_COOPERATIVE_126 = '''
Here is a simple, fully cooperative “threshold‐conditional” strategy that (i) tries to sustain the public‐good threshold every round, (ii) punishes a breakdown only one round long, (iii) always opens with cooperation, and (iv) defects in the final round (the unavoidable end‐game move in a finitely repeated game).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Variables we track  
   – r = total rounds  
   – t = current round (1…r)  
   – m = cooperation threshold  
   – coopCount[t–1] = number of players who cooperated in the previous round  

2. Main idea  
   – Round 1: Cooperate.  
   – Rounds 2…r–1:  
     • If last round met the threshold (coopCount[t–1] ≥ m), cooperate.  
     • Otherwise defect (punish), but only for this one round; after that check threshold again.  
   – Round r: Defect (standard end‐game logic).  

3. Rationale  
   – By always starting with C, we give the group a chance to meet the threshold.  
   – By cooperating whenever the last round met m, we reward successful coordination with the bonus k.  
   – If the group fails (fewer than m cooperators), we defect exactly once—enough to signal displeasure but not so long as to lock everyone into permanent defection.  
   – Defecting in the last round is inevitable: with no future to punish, unconditional cooperation is exploitable.  

4. Pseudocode  

state: –  
for t in 1..r:  
    if t == 1:  
        action[t] = C          # Open with cooperation  
    else if t == r:  
        action[t] = D          # End‐game defection  
    else:  
        if coopCount[t–1] ≥ m:  
            action[t] = C      # Last round succeeded ⇒ reward with C  
        else:  
            action[t] = D      # Last round failed ⇒ punish for 1 round  

5. Handling edge cases  
  • If r = 2, you play C in round 1 and D in round 2.  
  • If the very first cooperation fails to reach m (e.g. too few partners), you punish in round 2—but since it’s also the last round you’re defecting anyway.  
  • If the group recovers (≥ m Cs) immediately after your one‐round punishment, you resume cooperation.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy is “nice” (never the first to defect except in the final round), “forgiving” (only one‐round punishment), and “transparent” (all players see exactly when and why you defect). Over many rounds it supports stable, threshold‐hitting cooperation whenever a majority of the field is willing to play along.
'''

description_COOPERATIVE_127 = '''
Below is a simple, fully‐specified strategy that (a) aims for full cooperation whenever possible, (b) punishes coordinated failure just long enough to deter free‐riding, and (c) handles first and last rounds explicitly.  I call it “Threshold-Aware Generous Tit-for-Tat.”

  
1. State variables  
   • t = current round (1 ≤ t ≤ r)  
   • last_coop_count = number of cooperators in round t–1  
   • punish = boolean flag (true if we are in a one‐round punishment phase)  

2. Initialization (before round 1)  
   punish ← false  

3. Decision rule for round t  

   if t == 1 then  
     play C  
     /* Signal willingness to cooperate */  

   else if t == r then  
     /* Last round: no future punishment, so defect if you expect threshold met */  
     if last_coop_count ≥ m then  
       play D  
     else  
       play C  
     end  

   else  
     /* Intermediate rounds 2..r–1 */  
     if punish == true then  
       play D  
       /* One‐round punishment complete */  
       punish ← false  
     else  
       if last_coop_count ≥ m then  
         play C  
       else  
         /* Threshold failed last round ⇒ punish the group for one round */  
         play D  
         punish ← true  
       end  
     end  
   end  

4. Update after seeing round-t outcomes  
   last_coop_count ← (number of players who played C in round t)  

  
Explanation of key points  
1. First round (t=1): We start with cooperation to signal good will.  
2. Intermediate rounds (2 ≤ t ≤ r–1):  
   – If the threshold was met in the previous round (last_coop_count ≥ m), we cooperate again.  
   – If the threshold failed, we defect exactly one round (punish flag) then immediately forgive and return to cooperation, provided the group restores the threshold.  
3. Last round (t=r): Standard backward‐induction tells us that future punishment is off the table, so we defect if we believe the threshold will be met (maximizing 1+k vs. k), otherwise we cooperate (to at least avoid getting 0).  
4. “Generous” aspect: Punishment is limited to exactly one round, to avoid spirals of permanent defection.  

Pseudocode form  

```
initialize:
  punish ← false
  last_coop_count ← n   // assume full cooperation pre-game for simplicity

for t = 1 to r:
  if t == 1:
    action ← C

  else if t == r:
    if last_coop_count ≥ m:
      action ← D
    else
      action ← C
    end

  else:  // 2 ≤ t ≤ r–1
    if punish:
      action ← D
      punish ← false
    else:
      if last_coop_count ≥ m:
        action ← C
      else:
        action ← D
        punish ← true
      end
    end
  end

  Play(action)
  Observe everyone’s choices
  last_coop_count ← count of C’s in this round
end
```

Why this works  
– By starting cooperatively and returning to C as soon as the threshold is re-established, we foster high payoffs for the group.  
– A one‐round punishment is enough to deter chronic defectors without letting the system collapse into permanent defection.  
– In the final round we defect when it benefits us, which is individually rational but only affects the very last payoff.  
– All rules depend only on publicly observable history (last_coop_count), no secret communication needed.
'''

description_COOPERATIVE_128 = '''
Below is a single‐strategy description—call it “One–Round Group TFT with Forgiveness” (G‐TFT1)—that in our simulations will (i) drive the group to meet the threshold in every round, (ii) punish free‐riders briefly, and (iii) quickly forgive so as to restore full cooperation.  It is entirely symmetric, needs no extra signals beyond observing past actions, and works for any n, r, m, k. 

1.  State variables (for you alone)  
    •  punish_timer ∈ {0,1}: how many more rounds you will stay in punishment mode  

2.  Initialization  
    Before round 1: punish_timer ← 0  

3.  Action rule for round t:  
    if t = 1 then  
        play C  
    else if punish_timer > 0 then  
        play D  
        punish_timer ← punish_timer − 1  
    else  
        let coop_{t−1} = number of players who played C in round t−1  
        if coop_{t−1} < m then  
            // threshold failed last round; rebuild trust  
            play C  
        else if coop_{t−1} = n then  
            // everyone cooperated last round; maintain full cooperation  
            play C  
        else  
            // threshold was met but at least one player defected: punish them  
            play D  
            punish_timer ← 1        // punish for exactly one round  

4.  Edge cases  
    •  Last round (t = r): treat exactly as above.  Even in round r we punish if a defector slipped in round r−1, otherwise cooperate.  
    •  Chains of failure: if the group repeatedly fails to reach m, everybody keeps cooperating until the threshold is met.  
    •  Single‐round forgiveness: after exactly one round of collective punishment D, we reset punish_timer=0 and return to cooperating so long as the group’s last outcome was acceptable.  

5.  Rationale and cooperative mindset  
    – First round starts with full cooperation, giving the best chance to hit the threshold from the outset.  
    – If the group ever falls below the threshold, we “forgive” past missteps and cooperate to rebuild.  
    – If the threshold is met but there were defectors, we instantly punish for one round (by defecting).  This temporary collapse signals to free‐riders that exploitation will cost the group.  
    – Because the punishment lasts only one round, we minimize loss of future surplus and restore full cooperation as soon as possible.  
    – Even in the final round, we do not opportunistically defect without reason: we only defect if we are in the middle of a punishment phase or if we are punishing last‐round defectors.  

Pseudocode summary  
--------------  
punish_timer ← 0  
for t in 1..r do  
  if t == 1 then  
    action ← C  
  else if punish_timer > 0 then  
    action ← D  
    punish_timer ← punish_timer − 1  
  else  
    coop_prev ← count of C’s in round t−1  
    if coop_prev < m then  
      action ← C  
    else if coop_prev == n then  
      action ← C  
    else  // m ≤ coop_prev < n  
      action ← D  
      punish_timer ← 1  
  end  
  play(action)  
end  

This strategy is fully cooperative in spirit—it only defects to discipline free‐riders, never for narrow last‐round gain, and immediately returns to cooperation to ensure the threshold is met in as many rounds as possible.
'''

description_AGGRESSIVE_65 = '''
Below is a self-contained “Aggressive Exploiter” strategy.  It almost always defects, only “grudgingly” cooperates when it can guarantee a big payoff boost for itself, and otherwise relentlessly sabotages the group’s chances of hitting the cooperation threshold.

1.  Definitions  
    •  n, r, m, k as in the game spec.  
    •  C_prev = number of cooperators observed in the previous round (excluding you).  

2.  High-level idea  
    –  Default: Defect in order to deny the public good and punish cooperators.  
    –  Only cooperate when your single contribution will *flip* the round from “fail” to “success,” because that maximizes your one-round payoff (1 of personal endowment + k reward).  
    –  First and last rounds: pure defection—no incentive to build a reputation or to give others a free ride.  

3.  Detailed decision rule (pseudocode)  

```
Initialize:
  C_prev ← undefined

For round t = 1 to r:
  if t == 1:
    // No history, strike first
    Action_t ← D

  else if t == r:
    // Last round: defect, no future retaliation
    Action_t ← D

  else:
    // 1 < t < r: have C_prev from last round
    if C_prev == m – 1 then
      // By cooperating we push the group from (m–1) to m cooperators
      // If we believe other players repeat last round counts,
      // then our C will trigger the reward k for ourselves,
      // and D would yield only 1 (since C_prev = m–1 ⇒ without us ≤ m–1)
      Action_t ← C
    else
      // Either the group already succeeded without us (C_prev ≥ m)
      // or is so far from success (C_prev ≤ m–2)
      // in both cases defect to maximize personal payoff and/or
      // to sabotage future cooperation.
      Action_t ← D

  Play Action_t, observe full action profile, and update:
    C_prev ← number of players who chose C in this round
```

4.  Edge-case handling  
    •  First round (t=1): we have zero leverage, so we defect to set a hostile tone.  
    •  t=r (last round): defection is dominant—no future to exploit reputation.  
    •  Intermediate rounds: only cooperate if by your single vote the group crosses from m–1 to ≥ m.  Otherwise keep defecting.

5.  Why this is aggressive  
    –  You almost always defect, denying the public good and punishing cooperators.  
    –  You only ever give up your endowment to *force* a success when it directly maximizes your own payoff in that round—never out of altruism or concession.  
    –  You refuse to build trust or fall for tit-for-tat; you only “lend a hand” when it strictly benefits you.  

This strategy guarantees that whenever you cooperate, you are exploiting the group’s marginal cooperation to capture the full k-bonus for yourself, and otherwise you relentlessly defect to keep the group from achieving the threshold.
'''

description_AGGRESSIVE_66 = '''
Below is a self‐contained, “aggressive” repeated‐play strategy.  In plain English it says: “Defect always, except in the knife‐edge case where my single cooperation will turn a failed round into a successful one (i.e. exactly m–1 others cooperated last round).”  That way you never give away more than you absolutely must to keep the pot alive—and you free‐ride maximally whenever you can.

1.  State variables and notation  
   •  r = total rounds, t = current round (1…r)  
   •  m = threshold cooperators needed  
   •  obs[t–1] = number of players (out of the other n–1) who cooperated in round t–1  
        –  In round 1, obs[0] is undefined.  
   •  a_i(t) ∈ {C,D} is your action at round t.

2.  Decision rule (every round t):  
   if t = 1 then  
     •  No history ⇒ assume nobody cooperates ⇒ defect: a_i(1) ← D  
   else  
     •  If obs[t–1] ≥ m then  
         –  The threshold was met without me last round, and I expect it again ⇒ defect: a_i(t) ← D  
     •  Else if obs[t–1] = m–1 then  
         –  Exactly one cooperator short last round ⇒ my single C would guarantee the reward ⇒ cooperate: a_i(t) ← C  
     •  Else (obs[t–1] < m–1)  
         –  Even if I cooperated, the group still fails ⇒ defect: a_i(t) ← D  

   Note:  “obs[t–1]” is the count of cooperators you actually observed in the previous round.  

3.  Edge cases  
   •  First round (t=1): no information ⇒ defect by default.  
   •  Last round (t=r): same rule applies.  Since there is no future to sustain cooperation, you still only ever cooperate if you alone can rescue the payoff.  

4.  Why this is aggressive  
   •  You never cooperate “for the good of the group.”  
   •  You only pay the cost of cooperation when it is strictly necessary to trigger the k‐bonus for yourself (and incidentally for others).  
   •  You maximize your private 1 + k payoff whenever possible—and never give up the private 1 unless you can turn it into 0 + k, which is only valuable if it flips the round from failure to success.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  

```
Inputs:  m,  r
Initialize:  obs_prev = 0   # dummy value; used only for t>1

for t in 1 to r:
    if t == 1:
        action = D
    else:
        if obs_prev >= m:
            action = D
        else if obs_prev == m - 1:
            action = C
        else:
            action = D

    play(action)
    # observe actual number of cooperators among others this round
    obs_prev = count_cooperators_among_others()
end for
```

That’s it.  You defect by default and only “gun it” when you can single‐handedly guarantee the group payoff.
'''

description_AGGRESSIVE_67 = '''
Below is a fully specified, “aggressive” threshold‐exploiter strategy.  In essence it never gives away its endowment except in the bare‐minimum cases where its single contribution will push the group over the public‐goods threshold and thereby unlock the extra payoff k.  It punishes overshooting cooperators by always free‐riding on their excess, and it defects flat‐out in the first and last rounds (no future to leverage or punish).

1.  State variables we observe at the start of each round t:
    •  t (current round index, 1 ≤ t ≤ r)  
    •  prev_C(t–1) = number of cooperators (including you) in round t–1  
       → we can infer “other_C” = prev_C(t–1) minus (1 if you cooperated then, else 0)  
    •  m = the minimum number of cooperators needed  
    •  r = total number of rounds  

2.  High‐level decision logic:

   If t = 1 or t = r  
     → Defect  
   Else  
     Compute other_C = (prev_C(t–1) – your_last_action_was_C?1:0).  
     If other_C ≥ m  
       → Defect  // group already met threshold without you; exploit their cooperation  
     Else if other_C = m–1  
       → Cooperate  // your single contribution exactly tips the threshold  
     Else  
       → Defect  // insufficient collaborators; no point in wasting your endowment  

3.  Pseudocode

   initialize your_history = []  
   initialize coop_count_history = []  

   for t in 1 to r do  
     if t = 1 or t = r then  
       action[t] = D  
     else  
       if t = 2 then  
         // we only know prev_C for t–1 = 1
         other_C = coop_count_history[1]  
         // coop_count_history[1] includes you if you cooperated round 1,  
         // but you defected in round 1 by rule, so other_C = coop_count_history[1].  
       else  
         // general case:  
         let prevC = coop_count_history[t–1]  
         let prevYou = (your_history[t–1] == C ? 1 : 0)  
         other_C = prevC – prevYou  
       end if  

       if other_C ≥ m then  
         action[t] = D  
       else if other_C = m–1 then  
         action[t] = C  
       else  
         action[t] = D  
       end if  
     end if  

     play action[t], observe total cooperators this round → coop_count_history[t]  
     append action[t] to your_history  
   end for  

4.  Explanation of “aggressiveness”  
   •  No “fairness” or “forgiveness” phases—only the minimal cooperation needed to secure the bonus k for yourself.  
   •  In any round where the group already has at least m other cooperators, you always defect and harvest the free ride.  
   •  You never pre-commit or signal; you only cooperate once you see exactly m–1 others cooperated last round.  
   •  First and last rounds are pure defection—no future to influence or to exploit.  

This strategy maximizes your own expected payoff by (a) never wasting your endowment on uncertain rounds, (b) guaranteeing you claim k whenever it is within one vote of achievement, and (c) otherwise ruthlessly defecting.
'''

description_AGGRESSIVE_68 = '''
Below is a fully‐specified “aggressive” repeated‐game strategy, which we’ll call  
  “Opportunistic Defector with Pivotal Cooperation (ODPC).”  

 1.   Overview of mindset  
    •  You default to free‐riding (D), punishing any naïve cooperators.  
    •  You only “sacrifice” your endowment when you are strictly pivotal—that is, only when without your C the group would fail to reach m, but with your C they succeed, and the gain k outweighs the lost endowment.  
    •  In the final round you always defect (no future to influence).  

2.   Notation  
    •  n = total players; you are player 1.  
    •  m = cooperation threshold needed.  
    •  r = total rounds, indexed t=1…r.  
    •  a_i,t ∈{C,D} is action of player i in round t; c_i,t=1 if C, else 0.  
    •  Let coops₋₁(t–1) = ∑_{i=2…n} c_i,t–1 = number of other players who cooperated in the previous round.  
    •  We update history each round of actual observed coops.  

3.   Decision rules  
for t=1 to r do  
  if t == 1 then  
    – No history yet ⇒ defect:  a₁,1 ← D.  
  else if t == r then  
    – Last round “take the money and run”: a₁,r ← D.  
  else  
    – Compute coops₋₁ ← number of others who cooperated in t–1.  
    – If coops₋₁ ≥ m then  
        • The others already met (or exceeded) the threshold in t–1 without you; you get k extra by defecting again.  
        • ⇒ a₁,t ← D.  
      Else if coops₋₁ == m–1 then  
        • You are potentially pivotal: if you play C, group succeeds and you get payoff k; if you play D, group fails so you get only 1.  
        • Since k>1, cooperating is strictly better than defecting in this “pivotal” situation.  
        • ⇒ a₁,t ← C.  
      Else  (coops₋₁ < m-1)  
        • Even if you cooperate, coops₋₁+1 ≤ m-1 < m ⇒ no public good.  
        • Cooperation would be pure loss, so defect.  
        • ⇒ a₁,t ← D.  

4.   Grim “punishment” back‐up (optional, for extra aggression)  
    If in any past round you found coops₋₁≥m (i.e. they would have succeeded without you) but you instead played C (you were fooled into cooperating), then for all remaining rounds switch to permanent D.  
    This ensures you never again waste an endowment on a hopeless attempt to keep up.  

5.   Pseudocode  

  initialize history H = empty list  
  for t in 1…r do  
    if t == 1:  
      action ← D  
    else if t == r:  
      action ← D  
    else:  
      coops_others ← number of C’s by players 2…n in round t–1  
      if coops_others ≥ m:  
        action ← D  
      else if coops_others == m–1:  
        action ← C  
      else:  
        action ← D  
    record action in H  
    observe others’ a₂…a_n in round t, append to H  

6.   Discussion of edge cases  
  – First round: no signals ⇒ defect aggressively.  
  – Last round: no future leverage ⇒ defect (“end‐game”).  
  – If others coordinate heavily (coops₋₁≥m) you simply free‐ride on their effort.  
  – If others barely miss the threshold (coops₋₁=m–1), you jump in to pocket the k (you are pivotal).  
  – If they are too few (coops₋₁<m–1), any contribution is futile ⇒ you defect.  

This strategy ensures you never contribute except when it is strictly payoff‐maximizing (i.e. k > 1 and you alone tip the balance). It punishes reckless cooperators, exploits pivotal moments, and always defects in the final round.
'''

description_AGGRESSIVE_69 = '''
Below is an “aggressive free‐rider” strategy.  It never builds cooperation for its own sake, only chips in exactly when strictly needed to push the group over the threshold—otherwise it always defects (free‐rides or even sabotages).  In the very last round it never contributes.

1. State variables  
   • prev_C = number of Cooperators observed in the previous round  
   • t = current round index (1,…,r)  

2. Decision rule for round t  
   if t == 1 or t == r:  
     play D  
   else if prev_C == m–1:  
     play C   // just enough to (possibly) hit the threshold  
   else:  
     play D   // free‐ride or sabotage  

3. Updating prev_C  
   After each round ends, set prev_C = count of C actions by all players in that round.

4. Rationale / properties  
 • First round: defect to see who else will bear the cost.  
 • Middle rounds: only cooperate when exactly one more cooperator is needed  
   (prev_C​=m–1) so that the group still gets the k-bonus which you will free-ride  
   on in the very next round.  Otherwise you defect, maximizing your private 1.  
 • Last round: you never cooperate (no future rounds to exploit).  
 • Aggressive: you never “reward” others’ cooperations by joining the club  
   except at the last possible moment, and you never sustain genuine cooperation.  

Pseudocode  

```
prev_C ← 0

for t in 1..r:
   if t == 1 or t == r:
      action[t] ← D
   else if prev_C == m - 1:
      action[t] ← C
   else
      action[t] ← D

   // … play action[t], observe all players’ moves …
   prev_C ← count of C’s in round t
end for
```

Edge cases  
- r=2: you defect twice.  
- If no one ever cooperates except to try pushing past m–1, the group may never reach threshold—but whenever they do, you’re riding on their effort and never sustaining it yourself.
'''

description_AGGRESSIVE_70 = '''
Below is a fully‐specified, “aggressive” threshold‐PGG strategy we’ll call Pivotal Extortion with Grim Punishment (PEG).  It cooperates only when strictly necessary to swing the threshold, free‐rides whenever it can, and punishes any failed collective attempt by never cooperating again.  

1. Variables and bookkeeping  
   • r: total rounds  
   • t: current round (1 ≤ t ≤ r)  
   • m: threshold number of cooperators needed  
   • history[t′].C = number of cooperators in round t′  
   • punished = FALSE  (flag indicating we’ve observed an unsuccessful cooperation attempt and switched to “always defect”)  

2. Overview of the decision rule  
   • Round 1: always Defect (D).  
   • Rounds 2 … r–1:  
       – If punished == TRUE, play D.  
       – Else look at last round’s outcome (t–1):  
         · If history[t–1].C satisfies 1 < history[t–1].C < m  (i.e. some cooperators tried but failed), set punished ← TRUE and play D forever.  
         · Otherwise compute:  
             predicted_other_C = history[t–1].C  
               (if you cooperated in t–1, subtract 1; if you defected, it equals that count)  
             – If predicted_other_C ≥ m: they would succeed without you ⇒ play D (free‐ride).  
             – Else if predicted_other_C = m–1: only your C can tip them over ⇒ play C.  
             – Else (predicted_other_C < m–1): even if you C they still fail ⇒ play D.  
   • Round r (last round): play D (no future to punish).  

3. Pseudocode  

```
initialize:
  punished ← FALSE

for t in 1…r:
  if t == 1:
    action[t] ← D
    continue

  if t == r:
    action[t] ← D
    continue

  // t in 2…r–1
  prevC = history[t-1].C   // total Cs last round
  if punished == FALSE and 1 < prevC < m:
    punished ← TRUE
  if punished:
    action[t] ← D
    continue

  // now no punishment‐lock yet
  // compute how many would cooperate without me
  if I cooperated in round t-1:
    predicted_other_C = prevC - 1
  else:
    predicted_other_C = prevC

  if predicted_other_C >= m:
    // threshold already met ⇒ free‐ride
    action[t] ← D

  else if predicted_other_C == m - 1:
    // I'm pivotal ⇒ cooperate to trigger success
    action[t] ← C

  else:
    // even with me they would fail ⇒ defect
    action[t] ← D
```

4. Key aggressive features  
•  “Free‐ride priority”: whenever others suffice to hit m, we defect to pocket the private payoff.  
•  “Pivotal cooperation only”: we only ever pay the cost when our single vote flips an otherwise‐failing round into success.  
•  “Grim punishment”: if ever some cooperators bleed their endowment without hitting the threshold (an “unsuccessful attempt”), we switch to All-D for the rest of the game.  
•  “End‐game defect”: in the final round there is no future leverage, so we defect.  

This strategy minimizes contributions, aggressively exploits any genuine cooperators, and enforces never-cooperate again if the group shows weakness.
'''

description_AGGRESSIVE_71 = '''
Below is an aggressive, memory‐1 “greedy threshold” strategy.  It never cooperates for the sake of goodwill or future reward, only when it is strictly in your immediate self‐interest (i.e. when by cooperating you raise your own payoff above what defecting would give you).  In every other circumstance you defect—and you also exploit any surplus cooperators.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Notation & memory  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Let t=1,…,r index rounds.  
Keep in memory only last round’s count of opponents’ cooperations:  
  dₜ₋₁ = number of players j≠you who played C in round t−1.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
2.  Decision rule for round t  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
If t=1 or t=r:  
 Action = D  (always defect on the first and last round)  
Else (2 ≤ t ≤ r−1):  
 Let s = dₜ₋₁  (opponents’ cooperators in the previous round).  
 Case A:  s ≥ m  
  // Opponents alone can meet or exceed the threshold; free‐ride  
  Action = D  
 Case B:  s = m−1  
  // If you cooperate you will push the group from (m−1) to m  
  // By cooperating you get π = 0 + k = k  ; by defecting you get π = 1  
  // Since k>1, cooperating here strictly increases your immediate payoff.  
  Action = C  
 Case C:  s < m−1  
  // Even if you cooperate, opponents are too few ⇒ threshold still fails  
  // Defect and accept π = 1  
  Action = D  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
3.  How it works  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• You default to defect, punishing any surplus of cooperators (Case A).  
• You only ever contribute if and only if by doing so you are the pivotal m-th cooperator (Case B), raising your own stage‐payoff from 1 to k.  
• You refuse to “waste” contributions when they cannot change the outcome (Case C).  
• No cooperation on round 1 (no information) or round r (no future to influence).  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
4.  Pseudocode  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
```
Input:  m, r  
Initialize:  d_prev ← 0     // opponents cooperations “last round”  
For t in 1..r do:
  if t == 1 or t == r then
    play D
  else
    s ← d_prev
    if s >= m then
      play D
    else if s == m - 1 then
      play C
    else
      play D
  end

  // After the round resolves, update memory:
  Observe d_curr = # of opponents who played C in round t
  d_prev ← d_curr
End
```  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy is maximally aggressive in that it:  
1. Always defects unless you alone can tip the scale to secure yourself the extra k.  
2. Never “volunteers” cooperation for future good will or group benefit.  
3. Punishes any surplus of cooperators by dropping out.  
4. Ensures you extract every possible gain from others’ cooperative efforts.
'''

description_AGGRESSIVE_72 = '''
Below is a fully specified “aggressive‐bully” strategy.  In essence, you only ever cooperate when your single contribution is needed to hit the threshold; otherwise you free‐ride or outright defect—even punishing past cooperators by continuing to defect when they do most of the work.

1.  Strategy Name  
    Aggressive Nudge‐and‐Exploit (ANE)

2.  Intuition  
    –  Always defect by default (to grab the private 1‐unit payoff and punish any cooperators).  
    –  Only cooperate when the other n–1 players contributed exactly m–1 last round—i.e. when your single “yes” is the tipping point to secure the public good (so that you get k rather than let cooperators’ efforts go to waste).  
    –  In the final round, never cooperate (no future leverage).

3.  Decision Rule (per round t)

    Input at start of round t:
      •  t (current round index, 1 ≤ t ≤ r)  
      •  history of actions of all players in rounds 1…t–1  

    Let:
      coop_prev_total  = number of C’s played by everyone in round t–1  
      c_my_prev         = 1 if you cooperated in t–1, else 0  
      coop_prev_others = coop_prev_total – c_my_prev  

    Then choose action a_t as follows:

    if t == 1:
      a_t  = D   // start by defecting  
    else if t == r:
      a_t  = D   // never cooperate in final round  
    else if coop_prev_others == m–1:
      a_t  = C   // only you can push the group to threshold  
    else:
      a_t  = D   // otherwise, keep free‐riding / punishing

4.  Pseudocode

    function ANE_decision(t, history):
      if t == 1 or t == r:
        return D

      // Compute last‐round others’ cooperations
      coop_prev_total = count_C(history[t–1])  
      c_my_prev        = (history[t–1][my_index] == C ? 1 : 0)  
      coop_prev_others = coop_prev_total – c_my_prev

      if coop_prev_others == (m–1):
        return C
      else:
        return D

5.  Edge‐Case Handling  
    •  First round (t=1): defect to test the field and start punishing naive cooperators.  
    •  Last round (t=r): defect since there is no future to leverage—standard endgame defection.  
    •  All other rounds: cooperate only if exactly m–1 other players cooperated last round (so your C is decisive).  
    •  If more than m–1 others cooperated, defect and exploit their willingness.  
    •  If fewer than m–1 others cooperated, defect as the good cannot be secured anyway.

6.  Why It’s Aggressive  
    –  You never reward wholly cooperative groups; you instead free‐ride.  
    –  You only lend a hand when it is strictly in your self‐interest to push the threshold—and you immediately revert to defection afterward.  
    –  You punish any round in which you were not strictly needed by withholding cooperation.

This strategy maximizes your exploitation of cooperators, provides exactly the minimal “nudge” required to secure the public good (and only when it’s profitable), and always defects in the very last round.
'''

description_AGGRESSIVE_73 = '''
Below is an “aggressive mercenary” strategy that (1) almost always defects to exploit cooperators, (2) only chips in at the last moment when its single contribution is just sufficient to secure the public good, and (3) never cooperates in the first or final round so as to avoid being suckered with no future to recoup losses.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
STRATEGY NAME  
 Rogue Mercenary  

PARAMETERS KNOWN TO ALL  
 n  = number of players  
 m  = cooperators needed for the public‐good bonus  
 r  = total rounds  

INFORMED STATE (updated after each round)  
 last_others_C  = in the previous round, how many of the other (n–1) players chose C  

ACTION RULE (for player i in round t)  
1. If t = 1 (first round) → play D  
2. Else if t = r (last round) → play D  
3. Else (1 < t < r):  
     • If last_others_C = m – 1  → play C  
         (Your 1 contribution will tip the count to exactly m, securing k.)  
     • Otherwise → play D  
         (Either the threshold is already met without you—so you exploit—or it can’t be met even with you—so you save your unit.)  

UPDATE after observing round t:  
 last_others_C ← count of C among the other n–1 players in round t  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
EXPLANATION / “AGGRESSION” RATIONALE  
• Never “waste” a contribution unless you’re the marginal decider who turns a failure into success.  
• In any round where cooperators ≥ m already, you defect and pocket 1 + k rather than sacrificing 1.  
• In any round where cooperators ≤ m – 2, you defect because even your help wouldn’t reach m.  
• Only when exactly m – 1 others have cooperated do you step in. That single “mercenary” contribution is enough to trigger the bonus—and you minimize your cost to exactly the moments it pays off.  
• First round is pure reconnaissance—defect and watch. Last round is pure exploitation—defect with no fear of retaliation.  

This strategy maximizes individual payoff by shirking on “easy” rounds, refusing to pay a cost when you are not pivotal, and only cooperating when your lone unit of input flips a loss into a bonus for everyone.
'''

description_AGGRESSIVE_74 = '''
Below is a fully self-contained, “aggressive opportunist” strategy for the repeated Collective Risk Dilemma.  In essence it never cooperates unless that single cooperation is needed to guarantee the public‐good reward; it punishes any run of successful cooperation by continuing to defect; and it free-rides whenever it can safely do so.  In the last round it defects unconditionally.

—–  
Name: Aggressive Opportunist  
Key idea: Only contribute when defecting would drop the number of cooperators below m (and so cost you the k bonus).  Otherwise always defect.  Last round always defect.  

1.  Data structures and observations  
    •  Let r be the total number of rounds, indexed t=1…r.  
    •  At the end of each round t–1 you observe how many cooperators there were, call it CoopCount_{t-1}.  
    •  If you cooperated in t–1, you know that contributed 1 of the CoopCount; if you defected, you did not.  

2.  Strategy outline  
   For each round t from 1 to r do:  
     if t == r:  
       play D   // Last‐round defection—no future to punish  
     else if t == 1:  
       play D   // Start by defecting  
     else:  
       let prevC = CoopCount_{t-1}           // total cooperators last round  
       let myLast = 1 if you played C in t-1, else 0  
       let othersPrevC = prevC – myLast       // estimate of cooperators excluding you  
       // If by defecting this round you still expect ≥ m cooperators, free-ride  
       if othersPrevC >= m then  
         play D  
       // If by defecting you would drop below m, you lose k; so cooperate to secure reward  
       else if othersPrevC == m-1 then  
         play C  
       // If othersPrevC < m-1 then even your C won’t meet threshold → never waste your endowment  
       else  
         play D  

3.  Pseudocode  
```
for t in 1..r:
    if t == r:
        action[t] = D
    elif t == 1:
        action[t] = D
    else:
        prevC = observed_cooperators_in_round(t-1)
        myLast = 1 if action[t-1] == C else 0
        othersPrevC = prevC - myLast

        if othersPrevC >= m:
            action[t] = D
        elif othersPrevC == m - 1:
            action[t] = C
        else:
            action[t] = D
```

4.  Why it is aggressive  
  •  It never “volunteers” extra cooperators—only adds exactly the one needed, and only when strictly necessary to grab the k bonus.  
  •  It free-rides on any surplus cooperation (othersPrevC ≥ m), punishing the group by withdrawing support, which destabilizes trusting cooperators.  
  •  It defects in the very first and the final round, removing any possibility of being exploited early or showing goodwill at the end.  

5.  Edge cases handled  
  – First round: no history → defect.  
  – Last round: no future → defect.  
  – If exactly m-1 others can be counted on → cooperate just enough to hit m.  
  – If fewer than m-1 others → defect, since even your help won’t trigger the bonus.  

This rule set maximizes your individual payoff by grabbing every free ride, only sacrificing your endowment when it’s the sole route to secure the public reward, and otherwise relentlessly defecting—i.e. an aggressive, exploitative stance.
'''

description_AGGRESSIVE_75 = '''
Below is a fully specified “aggressive” strategy—call it the Threshold-Saboteur—that (1) defects almost all the time to punish others, (2) only ever cooperates when it is strictly in your self-interest (i.e. you alone can tip the threshold from m–1 to m and reap the reward), and (3) handles first‐ and last‐round edge cases cleanly.

1. High-Level Description  
   • First round: Defect (no history, play to maximize private safety).  
   • Intermediate rounds 2…r–1:  
     – Observe how many of your opponents cooperated last round (opp_coop).  
     – Predict they will repeat that level of cooperation this round.  
     – If opp_coop = m–1, then cooperate (you tip them over to m cooperators, yielding you k > 1).  
     – Otherwise defect (either they already can succeed without you, or they can’t succeed even with you—so you deny them or free-ride).  
   • Last round r: Exactly the same rule. (No future to preserve, so you still only cooperate when it directly raises your payoff.)

2. Why “Aggressive”?  
   – You never cooperate merely to help the group unless it is the unique way for you to get the bonus k.  
   – If opponents are already on track to succeed (opp_coop ≥ m), you always defect and steal the extra +k for yourself (1+k > k).  
   – If opponents are far from success (opp_coop < m–1), you defect and collect the safe 1.  
   – You punish any near-success that doesn’t directly benefit you, keeping the group’s total payoffs as low as possible consistent with your own.

3. Pseudocode  

```
Inputs:  
  n   — total players (including you)  
  m   — cooperation threshold  
  r   — total rounds  
  k   — reward when threshold met (k > 1)

State you track:  
  history[t][j]  — action of player j in round t, for t < current round

Procedure decideAction(round t):
  if t == 1:
    return D    // no history, defect

  // count how many of the other n–1 players cooperated in previous round
  opp_coop = 0
  for each player j ≠ you:
    if history[t–1][j] == C:
      opp_coop += 1

  // predict they will do the same this round
  predicted_opp_coop = opp_coop

  // key decision:
  if predicted_opp_coop == m – 1:
    // by cooperating you tip them to m, you get payoff = 0 + k > 1
    return C
  else:
    // either they can succeed without you (so you defect and get 1+k)
    // or they can’t succeed even if you cooperate (so you defect and get 1)
    return D
```

4. Edge Cases  
– If m–1 < 0 (impossible since m ≥2), the “== m–1” test never fires, so you always defect.  
– In every round (including the last), you apply the same rule—there is no “end‐game cooperation.”  
– If opponents wildly change behavior, you always base your forecast on their most recent play.  

5. Summary of Payoff Logic  
– If opponents ≥ m cooperate without you: you defect → get 1+k; any cooperation would cost you 1 instead of 0 and yield only k.  
– If opponents = m–1 cooperate: you cooperate → group hits m, you earn k > 1; defecting nets you only 1.  
– If opponents < m–1 cooperate: even with you they fail → defect → get 1; cooperating would give you 0.  

This strategy is “aggressive” in that it relentlessly defects to punish the group unless coerced by pure self-interest to supply the one extra coin that tips the bonus your way.
'''

description_AGGRESSIVE_76 = '''
Below is an “Aggressive Saboteur” strategy.  It never cooperates to build trust or reciprocate; it only ever contributes when doing so lets it grab the group‐reward for itself.  Otherwise it defects, both to maximize its own per‐round payoff and to prevent threshold hits whenever it can.

1.  Definitions  
   •  History up to (but not including) round t: for each player j≠i we know how often they cooperated in prior rounds.  
   •  Estimate pᵢⱼ(t): our estimate that player j will play C in round t (e.g. simple frequency = #C_j / (t−1)).  
   •  Let X = random variable = number of other players cooperating in round t.  We approximate its mean μ = ∑_{j≠i} pᵢⱼ(t).  

2.  Core decision rule for round t (1 ≤ t ≤ r):  
   a.  If t is the last round (t = r):  
       – Always Defect (D).  No future to exploit or punish.  
   b.  Else (t < r):  
     1.  Compute μ = ∑_{j≠i} pᵢⱼ(t).  
     2.  If μ ≥ m:  
           // Others likely already meet threshold  
           Play D to exploit the group‐reward (you get 1 + k vs C’s 0 + k).  
        Else if μ ∈ [m−1, m):  
           // You are potentially pivotal: if exactly m−1 others C, your C would tip it.  
           Play C, since expected payoff k  > 1.  
        Else:  
           // Too few likely cooperators for threshold; cooperating is doomed.  
           Play D to save your endowment.  

3.  First round (t=1):  
   – No data ⇒ all pᵢⱼ(1) = 0.5 (uninformed prior) ⇒ μ = (n−1)*0.5.  
   – If μ < m−1 ⇒ D.  If μ ≥ m ⇒ D.  Only if (n−1)/2 ∈ [m−1, m) ⇒ C.  
     In most standard parameters you’ll start with D.  

4.  Updating beliefs:  
   After each round observe who cooperated.  For each j update pᵢⱼ(t+1) = ( # times j played C so far ) / (t).  

5.  Rationale & aggressiveness:  
   – You never “reward” cooperators by entering into a mutual‐cooperation norm.  
   – You only ever pay the contribution cost when it’s strictly dominant (you are pivotal) and the payoff k exceeds the sure‐thing of D.  
   – You punish any hope of a stable cooperating group by default‐defecting, ensuring the threshold often fails unless your cooperation is strictly payoff‐maximizing.  
   – In the last round you unconditionally defect to avoid any endgame exploitation.  

6.  Edge cases:  
   •  If r = 2, same logic applies: first round uses the μ–m test; second round you defect.  
   •  If your probability estimates are exact (i.e. you know exactly who will play C), you implement the same “μ ≥ m ⇒ D, μ = m−1 ⇒ C, else D” rule perfectly.  
   •  Ties or non‐integer μ are handled by comparing to the two thresholds m and m−1 as above; if exactly μ = m−1 you cooperate (you’re exactly pivotal in expectation).  

Pseudocode

```
function AggressiveSaboteur(history, t, n, m, r):
    if t == r:
        return D

    # Estimate opponent C–probabilities
    for each j ≠ i:
        p[j] = (# times j played C in rounds 1..t−1) / max(t−1,1)

    μ = sum_{j≠i} p[j]

    if μ >= m:
        # safe to defect and exploit
        return D
    else if μ >= m−1:
        # pivot point: cooperating yields k > 1
        return C
    else:
        # hopeless to reach threshold
        return D
```

This strategy is aggressive because it (1) never builds cooperative goodwill, (2) defects whenever it can both deny others or exploit them, and (3) only incurs the cooperation cost if it is mathematically the unique way to trigger the large payoff for itself.
'''

description_AGGRESSIVE_77 = '''
Below is an “aggressive” threshold‐public‐goods strategy.  It never sacrifices itself except to just tip the group into success, it freerides whenever it safely can, and it refuses to cooperate in the last two rounds (where there is no future to leverage).

────────────────────────────────────────  
1. Variables and history  
  • t = current round (1…r)  
  • lastCoops = number of cooperators (including you) observed in round t–1  
  • action ∈ {C, D}  

2. Core decision rule (for each round t):  
  if t == 1:  
    action ← D        // first‐round probe: defect to see if opponents will carry the load  
  else if t ≥ r–1:  
    action ← D        // no future: always defect in rounds r–1 and r  
  else  
    switch on lastCoops:  
      case ≥ m:  
        // threshold was met last time without any risk  
        action ← D      // freeride on their efforts  
      case == m–1:  
        // they fell short by exactly one: you can cheaply tip success  
        action ← C      // pay cost 1 to unlock k for everyone (and to train them that cooperators do influence outcomes)  
      default (< m–1):  
        // even if you cooperated there is no chance to hit threshold  
        action ← D      // save your 1 unit  

3. Updating history  
  After everyone’s moves in round t, observe total cooperators (including you) and store it in lastCoops for the next iteration.

4. Remarks on aggressiveness  
  • You only ever pay the cooperation cost when you are pivotal (lastCoops == m–1).  Every other time you defect.  
  • You refuse to contribute in the very last two rounds, because no future retaliation or reward can be leveraged.  
  • Against naive cooperators you will free‐ride repeatedly on their bulk contributions, only occasionally tipping them over the line.  
  • If opponents adapt and never approach m–1 cooperators, you simply defect forever (they aren’t providing any public benefit to exploit).  

5. Pseudocode  

  initialize lastCoops ← –1   // undefined before round 1  
  for t in 1…r do  
    if t == 1 then  
      action ← D  
    else if t ≥ r–1 then  
      action ← D  
    else if lastCoops ≥ m then  
      action ← D  
    else if lastCoops == m–1 then  
      action ← C  
    else  
      action ← D  
    end if  

    play(action)  

    observe totalCooperatorsThisRound  
    lastCoops ← totalCooperatorsThisRound  
  end for  

This strategy is aggressive in that it never “wastes” a cooperation unless it is the decisive tip, it defects whenever it can safely do so, and it shuts down any cooperation in the final rounds when there is no future to manipulate.
'''

description_AGGRESSIVE_78 = '''
Below is a self-contained, “bully”-style strategy that aggressively free-rides, only chips in when absolutely needed to trigger the public reward, and thereafter punishes any cooperators who tried to “use” you.

Strategy name: BullyPivotal

1. Intuition  
   - Always defect unless you’re exactly the pivotal contributor who swings the group from failure to success.  
   - The moment you cooperate and see any defections among opponents, you flip into permanent defection (punishment).  
   - In the last round you apply the same “only‐when‐pivotal” rule but ignore any previous “promise” to cooperate.

2. Notation  
   Let r = total rounds, t = current round (1 ≤ t ≤ r).  
   Let Hₙ(t−1) = number of cooperators (excluding you) observed in round t−1.  
   Let m = threshold, k = reward factor.

3. Decision rule (for each round t)

   Initialize: punished ← false

   For t from 1 to r:
     1. If punished = true:
          play D
          (You’ve been “used” before—stay in permanent defection.)
     2. Else if t = 1:
          play D
          (No history → default to defection.)
     3. Else (t > 1):
          let x = Hₙ(t−1)
          • if x ≥ m:
               play D
               (Group would succeed without you → free-ride and get 1+k.)
          • else if x = m−1:
               play C
               (You’re pivotal → cooperating yields k vs defection yielding only 1.)
          • else:
               play D
               (Even if you cooperate, threshold not met → still defect.)
     4. After observing all actions in round t:
          if you played C in t and you see at least one opponent played D in t:
             punished ← true
          (Aggressive punishment: you never cooperate again once “used.”)

   Note on the last round (t = r):
     You still follow step 3 above (the same pivotal-only rule). Even if you had punished yourself earlier, step 1 forces D in round r.

4. Edge cases  
   • First round: No history → guaranteed defection.  
   • Last round: No special generosity—only cooperate if exactly pivotal (x = m−1), otherwise defect.  
   • If you ever cooperate and observe any defection that round, you immediately switch to permanent defection (a grim punishment).  

5. Why it’s aggressive  
   - You refuse to be the sucker: you only pay the cooperation cost when it is strictly payoff‐maximizing (i.e. you swing the group into the k‐payoff).  
   - You free-ride whenever you’re non-pivotal, pocketing the full private gain plus k if the others succeed.  
   - You punish any defector who benefits from your goodwill by never cooperating again, ensuring rival cooperators learn not to trust you.

6. Pseudocode

```
Inputs: r, n, m, k
State variables:
  punished ← false

For t in 1..r:
  if punished:
    action[t] ← D
  else if t = 1:
    action[t] ← D
  else:
    x ← number of cooperators (excluding you) in round t−1
    if x ≥ m:
      action[t] ← D
    else if x = m−1:
      action[t] ← C
    else:
      action[t] ← D

  Play action[t].  // simultaneous move

  Observe OppActions[t] from opponents
  if action[t] = C and any opponent in OppActions[t] played D:
    punished ← true
```

You will thereby exploit cooperative neighbors, only contribute when you’re indispensable, and punish any post‐cooperation defection with permanent defection of your own.
'''

description_AGGRESSIVE_79 = '''
Below is a fully specified “Aggressive Threshold‐Exploiter with Grim Punishment” strategy.  It uses the payoff structure to (1) free‐ride whenever others will clear the threshold without you, (2) only contribute if you alone can tip the group over the threshold, and (3) instantly “go dark” (never contribute again) the moment you’re exploited by other cooperators.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
State Variables  
  punished ← false     // once true, you will defect forever  
  last_others_coops ← 0 // number of other players who cooperated in last round  

Parameters (known to all)  
  n, r, m, k  

Notation  
  t = current round (1 … r)  
  your_action ∈ {C,D}  
  others_coops = number of cooperators among the other n–1 players this round  

Main Decision Rule (each round t):  
  if punished == true then  
    play D  
    continue to next round  
  end-if  

  // 1) Can I exploit?  
  //    If even without my C there will be ≥ m total coops, defect for (1+k)  
  predicted_others_if_I_C  = others_coops        // if I cooperated, total coops = others_coops + 1  
  predicted_others_if_I_D  = others_coops        // if I defect, total coops = others_coops  
  
  if predicted_others_if_I_D ≥ m then  
    play D   // threshold hits anyway → exploit for 1 + k  
    goto END_DECISION  
  end-if  

  // 2) Am I pivotal?  
  //    If exactly m–1 others will cooperate, my C makes the difference  
  if predicted_others_if_I_C ≥ m and predicted_others_if_I_D < m then  
    play C   // tip the group into success, payoff = 0 + k = k > 1  
    goto END_DECISION  
  end-if  

  // 3) Otherwise no point in cooperating  
  play D  

END_DECISION  

  // We'll learn this round’s others_coops and check for exploitation  
  // (done at the very end of the round, after observing payoffs)  
  last_others_coops ← others_coops_this_round  
  if your_action == C AND last_others_coops ≥ m then  
    // You cooperated but they didn’t need you → they got 1+k, you only got k  
    punished ← true    // Grim trigger: never cooperate again  
  end-if  

Edge Cases  
  • Round 1: punished=false by initialization; no history of others_coops.  We set others_coops=0 so predicted_others_if_I_D=0<m–1→ we defect.  
  • Last Round (t=r): exactly the same logic applies, since even in r there is still an incentive to tip when pivotal.  
  • m=1 is excluded by spec (1<m<n), so the “pivotal” case m–1 is at least 1 and cannot fire in round 1.  

Why this is aggressive  
  1.  Free‐rides whenever possible: if the other n–1 can already hit the threshold, you always defect for the 1+k payoff.  
  2.  Pivots only when strictly necessary to secure k—you never give away a contribution that won’t improve your own payoff.  
  3.  Grim trigger: the instant you are “exploited” (you play C but others’ coops ≥ m so you miss out on the extra 1), you permanently defect to punish them.  

Pseudocode Summary  
```
initialize punished = false
for t in 1..r:
  if punished:
    action = D
  else:
    // predict others_coops (observed in real time)
    if others_coops >= m:
      action = D
    elseif others_coops == m-1:
      action = C
    else:
      action = D

  play(action)
  observe others_coops_this_round

  if action == C and others_coops_this_round >= m:
    punished = true
```

This strategy maximizes your exploitation opportunities, secures cooperation only when you’re pivotal, and metes out the harshest possible punishment the moment you’re taken advantage of. It is therefore both payoff‐driven and aggressively defensive.
'''

description_AGGRESSIVE_80 = '''
Below is a fully specified “aggressive opportunist” strategy.  It almost always defects, grabs the public‐good reward only when you’re pivotal, and then punishes any clique that tries to cooperate without you.

1.  State variables  
   • flag_punish ∈ {false,true}, initially false  
   • last_coop_count (others’ cooperations last round), initially 0  

2.  High‐level description  
   • You defect by default.  
   • The one time you’ll cooperate is when exactly m − 1 others cooperated last round—i.e. you’re pivotal.  That way you ensure project success and capture k > 1.  
   • If you see the group succeed without your help twice in a row (others ≥ m cooperators), you turn on a permanent “punish” flag and defect every remaining round, denying them further payoffs.  
   • In the final round you always defect (no future to defend).  

3.  Detailed decision rule (per round t = 1…r)  
   
   If t == 1:  
     action ← D  
   else if t == r:  
     action ← D                        # Last‐round exploit  
   else if flag_punish == true:  
     action ← D                        # Punish forever  
   else:  
     let C_other = last_coop_count     # number of cooperators among the other n–1 last round  
     if C_other ≥ m then                # they can succeed without you  
       action ← D                       # free‐ride now, but also count for punishing  
       record success_without_you++     # see punishment trigger below  
     else if C_other == m–1 then        # you are pivotal  
       action ← C                       # cooperate to turn failure into success → you get k  
       reset success_without_you = 0  
     else                                # C_other < m–1: even with you they’d fail  
       action ← D  
       reset success_without_you = 0  

   # Punishment trigger (executed after observing the outcome of this round):
   if success_without_you ≥ 2 then      
     flag_punish ← true                 # they’re forming a coalition without you; sabotage forever  

   # At the end of the round, update last_coop_count from observed actions.  

4.  Rationale and edge‐case handling  
   – First round: no history → defect.  
   – Last round: future payoffs irrelevant → defect to maximize one‐shot gain.  
   – Pivotal cooperation (others = m − 1): The only time cooperating increases your absolute payoff from 1 to k > 1.  You’ll grab it.  
   – Otherwise you defect:
     • If others ≥ m: you free‐ride (get 1 + k), and you begin counting “success_without_you.”  
     • If others < m − 1: no chance for success, so you don’t waste your contribution.  
   – Punishment: As soon as you see “group success without your help” twice in a row, you flip a flag and defect every remaining round—even in pivotal situations—to punish them for trying to form a cooperative coalition that excludes you.  

5.  Pseudocode  

```
initialize:
  flag_punish ← false
  success_without_you ← 0
  last_coop_count ← 0

for t in 1…r:
  if t == 1:
    action ← D
  else if t == r:
    action ← D
  else if flag_punish:
    action ← D
  else:
    C_other ← last_coop_count
    if C_other ≥ m:
      action ← D
      success_without_you ← success_without_you + 1
    else if C_other == m - 1:
      action ← C
      success_without_you ← 0
    else:
      action ← D
      success_without_you ← 0

  play action; observe #others cooperated → new_last_coop_count
  last_coop_count ← new_last_coop_count

  # Check punishment trigger
  if success_without_you ≥ 2:
    flag_punish ← true
```

This strategy is “aggressive” because it:  
– Defects by default, refuses to be a consistent contributor.  
– Only cooperates when it is strictly instrumental to your own gain (pivotal case).  
– When it detects a stable coalition forming without you, it punishes relentlessly by defecting for the rest of the game.
'''

description_AGGRESSIVE_81 = '''
Below is a fully specified, “aggressive” threshold‐public‐goods strategy.  In plain English it says: “I will never give away my endowment unless my one coin is strictly necessary to hit the threshold; and if I ever see others let the group fail when it could have succeeded without me, I go into a permanent defection mode.”  

1.  Decision rules  
    • First round (t=1): Defect.  
    • Last round (t=r): Defect.  (No future to leverage.)  
    • In any intermediate round t (1 < t < r):  
       – Let Oₜ₋₁ = number of cooperators among the other (n–1) players in round t–1.  
       – If we are in “revenge mode” (see below), Defect.  
       – Otherwise:  
         · If Oₜ₋₁ ≥ m, then defect.  
           (Even if I defect, there were already ≥m cooperators, so threshold still met.)  
         · Else if Oₜ₋₁ = m–1, then cooperate.  
           (My one coin is pivotal—without it they miss the reward, with it we all get k.)  
         · Else (Oₜ₋₁ < m–1), defect.  
           (Even my cooperation wouldn’t reach the threshold, so don’t throw away my endowment.)  

2.  Revenge (aggression) trigger  
    • After each round t, observe:  
       – total cooperators in that round (including you) call it Cₜ.  
    • If Cₜ < m (threshold failed) but the other players alone had Oₜ ≥ m (i.e. the group would have succeeded without your help or without the help of whatever subset),  
      then enter permanent “revenge mode.”  
      In revenge mode you defect every remaining round (including rounds 1 or r, but they’re already defection anyway).  
    • Rationale: if others could have hit the threshold but chose to defect and scare you off, you punish them by never cooperating again.  

3.  Pseudocode  

    initialize  
       revenge ← false  

    for t in 1..r do  
       if t == 1 or t == r then  
          play D  
       else if revenge == true then  
          play D  
       else  
          observe O ← # cooperators among other players in round t–1  
          if O ≥ m then  
             play D  
          else if O == m–1 then  
             play C  
          else  
             play D  
          end if  
       end if  

       after all moves in round t are revealed:  
          let C_total ← # cooperators (including you) in round t  
          let O ← # cooperators among the other (n–1) players in round t  
          if C_total < m and O ≥ m then  
             revenge ← true  
          end if  
    end for  

4.  Why it’s aggressive  
    – You never “waste” a contribution except when it is exactly pivotal.  
    – You maximally exploit any situation where the threshold would be met without you.  
    – You punish any free-riding group that lets the project fail even though they could have avoided failure without you.  
    – On the last round you defect unconditionally (standard backward-induction exploit).  

This strategy guarantees you only ever pay the cost when it’s strictly necessary to unlock the group reward, otherwise you freeride—and you go so far as to burn future cooperation if others show they prefer to let the group fail when they could have succeeded.
'''

description_AGGRESSIVE_82 = '''
Below is an “Aggressive Free-Rider” strategy that combines opportunistic cooperation (only when it strictly increases your payoff) with a grim-trigger–style punishment of any would-be cooperators.  It guarantees you never pay more than you have to, punishes everyone else for trying to form a coalition, and always defects in the last round.

1.  Definitions and bookkeeping  
    •  n, r, m, k as given.  
    •  History Ht = list of action profiles up to round t–1.  
    •  Let φt–1 = number of players (including you) who cooperated in round t–1.  
    •  A flag PunishAll ∈ {false,true}, initially false.  
       –  PunishAll becomes true as soon as any other player i cooperates in any round.

2.  Core decision rule for round t (1 ≤ t ≤ r)  
    if t == 1 or t == r or PunishAll == true:  
       play D  
       (– First round: probe with D.  Last round: standard backward-induction defect.  
        – If PunishAll, you’ve “locked in” a permanent defection to punish everyone.)  
    else:  
       // estimate how many others will cooperate this round  
       let est_φ_others = (φt–1) – (your action in t–1 was C ? 1 : 0)  
         // assume others repeat last round’s behavior collectively  
       if est_φ_others == m–1 and k > 1:  
         play C    // Only time cooperating strictly beats defecting  
       else:  
         play D

3.  Updating the punishment flag  
    After observing actual actions in round t, if any opponent played C in round t, set PunishAll := true.

4.  Rationale and aggressiveness  
  •  You never pay the cost of contribution except in the narrow case that by adding your one token you turn a failure into a success (i.e. est_φ_others = m–1).  In that case, cooperating yields payoff k (>1) vs defecting yields 1, so you cooperate.  
  •  You defect whenever you can freeride on enough cooperators or when cooperation wouldn’t achieve threshold.  
  •  The moment anyone “trusts” you by cooperating, you trigger PunishAll and thereafter defect every round (including rounds where your single token might have rescued the project).  This punishes all cooperators by permanently destroying any future collective benefit they might try to build.  
  •  You defect in the very last round because there is no future to leverage for punishment or reward.

5.  Pseudocode

  initialize PunishAll ← false  
  for t in 1..r do  
    if t == 1 or t == r or PunishAll then  
      action_t ← D  
    else  
      φ_prev ← number of C’s in Ht (round t–1)  
      my_prev_C ← (my action in t–1 was C ? 1 : 0)  
      est_others ← φ_prev – my_prev_C  
      if est_others == m–1 and k > 1 then  
        action_t ← C  
      else  
        action_t ← D  
    end if

    play action_t simultaneously  
    observe opponents’ actions this round  
    if any opponent played C then  
      PunishAll ← true  
    end if  
  end for

This strategy is maximally aggressive: it never wastes contributions, it exploits any surplus cooperators, and it uses a single round of detected cooperation from anyone to lock in perpetual defection, thereby inflicting the maximum collective pain on would-be altruists.
'''

description_AGGRESSIVE_83 = '''
Below is an “Opportunistic Free-Rider” strategy that defaults to defection, only cooperates when strictly necessary to secure the public‐good payoff for itself, and never risks contributing in the final round.

1) Data structures and beliefs  
   • For each opponent j ≠ you, maintain a running cooperation frequency f_j = (number of times j played C so far) / (rounds played so far).  
   • Let E = ∑_{j≠you} f_j be your estimate of how many others will cooperate this round.  

2) Decision rule for round t (1 ≤ t ≤ r):  
   if t == 1 then  
     – No history: defect (D).  
   else if t == r then  
     – Final round: defect (D), since there is no future to incentivize.  
   else  
     1. Compute E = ∑_{j≠you} f_j.  
     2. Case analysis:  
        a) If E ≥ m  then  
             // Even if you defect, you expect ≥ m cooperators ⇒ reward still paid  
             Play D.  
        b) Else if E < m–1 then  
             // Even if you cooperate, you still expect < m ⇒ no reward, so keep your endowment  
             Play D.  
        c) Else (m–1 ≤ E < m) then  
             // If exactly m–1 others will cooperate, your C pushes total to m ⇒ you secure the k  
             Play C.  

3) Belief‐update after observing round t actions  
   For each opponent j:  
     f_j ← ( (t–1)·f_j + 1{j played C in round t} ) / t  

4) Edge-cases & remarks  
   • First round: always defect. This “tests” the field and avoids unnecessary risk.  
   • Last round: always defect. There is no continuation payoff to protect, so cooperating is pure cost.  
   • Mid-game: you only pay the cost of cooperation when you are literally the decisive vote.  
   • Aggressiveness stems from (i) defaulting to D, (ii) freeloading on others’ contributions whenever possible, and (iii) never cooperating when not strictly necessary.  

Pseudocode sketch  
```
initialize f_j = 0.5 for all j≠you  // prior
for t in 1…r:
  if t==1 or t==r:
    action = D
  else:
    E = sum_j f_j
    if E >= m:
      action = D
    else if E < m-1:
      action = D
    else:
      action = C
  play(action)
  observe each opponent’s move this round
  for each j≠you:
    update f_j = ((t-1)*f_j + 1{j played C}) / t
endfor
```  
This strategy “piggy-backs” on others’ cooperations, only stepping in when you are the swing vote, and otherwise maximizes private payoffs—even to the last round.
'''

description_AGGRESSIVE_84 = '''
Below is an “Aggressive Exploit-and-Punish” strategy.  It maximizes your payoff by (1) defecting by default, (2) only cooperating in those rare rounds where your single contribution turns a near-miss into a success (so you collect k instead of 1), and (3) once you’ve exploited the group’s cooperators to pull off a successful threshold, you thereafter refuse to help and forever defect.

1.  Definitions and State  
   •  r = total rounds, t = current round (1≤t≤r)  
   •  m = threshold needed  
   •  coop_count[t] = number of players (other than you) who cooperated in round t  
   •  exploited = Boolean flag, initially false  
       –  Set to true the first time a round succeeds (≥m cooperators including you cooperating opportunistically) and you defected that round.

2.  High-level idea  
   –  Baseline: always defect (D).  
   –  Exception: if exactly m–1 opponents cooperated last round and you have not yet “exploited” the group, then cooperate (C) this round—your 1 contribution pushes it from failure to success, giving you payoff k instead of 1.  
   –  Once you have ever enjoyed that one-time k (exploited = true), switch to permanent defection to punish would-be cooperators.

3.  Decision rules  
   For each round t from 1 to r:  
     if exploited == true then  
       play D  
     else  
       if t == 1 then  
         # no history → defect by default  
         play D  
       else    
         if coop_count[t–1] == m–1 then  
           # only way to turn a loss into a win  
           play C  
         else  
           play D  

   After the round is played and you observe total cooperators (including you):  
     if exploited == false  
        and total_cooperators_this_round ≥ m  
        and you played D this round  
     then  
        exploited ← true  

4.  Edge cases  
   –  First round (t=1): no information, so defect.  
   –  Last round (t=r): same rule applies.  There is no future to punish, but you still exploit if coop_count[r–1] = m–1.  
   –  If the group never gets close (coop_count[t–1]<m–1), you never waste a token on C.  
   –  If the group always overshoots (coop_count[t–1]≥m), you never cooperate—you just freeride on anyone who still cooperates.  

5.  Pseudocode  

   initialize exploited ← false

   for t in 1…r do
     if exploited == true then
       action ← D
     else
       if t == 1 then
         action ← D
       else if coop_count[t-1] == m - 1 then
         action ← C
       else
         action ← D
     end if

     play(action)
     observe total_cooperators_this_round (including your own C if you cooperated)
     if exploited == false
        and action == D
        and total_cooperators_this_round ≥ m
     then
        exploited ← true
     end if
   end for

6.  Why it’s aggressive  
   –  You only ever sacrifice your own 1-point private payoff when you can swing the group from failure to success—purely to cash in on k.  
   –  The moment you’ve ridden the coat-tails of others’ willingness to cooperate, you freeze them out forever by defecting unconditionally.  
   –  You never build trust, never reward cooperators, and you punish any sustained cooperation with permanent non-participation.
'''

description_AGGRESSIVE_85 = '''
Below is an “aggressive‐selfish” strategy for the repeated Collective-Risk Dilemma.  It never takes the lead in cooperating, it free-rides whenever a safe majority exists, it only “rescues” a failing threshold when that rescue is strictly in its own short‐term interest, and it briefly experiments when no threshold has ever been met.  In plain English first, then in concise pseudocode.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Key ideas  
   •  Never be one of the first m cooperators.  Only cooperate if exactly m–1 others cooperated in the previous round (so that your single contribution flips failure → success, giving you k > 1 rather than 1).  
   •  If the group already reached m cooperators last round, free-ride (defect).  
   •  If fewer than m–1 cooperators appeared last round, it is hopeless to meet the threshold by cooperating, so defect—except that, after a certain drought of successes, occasionally “probe” with a lone C to see if others will coordinate.  
   •  In the very last round you also maximize only that round’s payoff (so you still cooperate if and only if exactly m–1 others cooperated last round).  

2.  Parameters you must fix once and for all  
   •  δ ∈ [0,1], a small “exploration” probability (e.g. δ=0.1).  
   •  L, a small integer “drought length” (e.g. L=3).  After L consecutive rounds with no threshold success, begin probing.  

3.  State variables  
   •  prev_coops  = number of cooperators observed in the immediate previous round  
   •  drought     = number of consecutive past rounds in which fewer than m cooperators succeeded  

4.  Full decision rule  

At the start of round t:
   if t==1:
     play D  (no history yet)  
     prev_coops ← 0; drought ← 1  
     return  
   
   /* Last round’s cooperators = prev_coops */  
   if prev_coops ≥ m:
     // threshold already met – free ride forever
     play D  
     drought ← 0  
     return  
   
   if prev_coops == m–1:
     // Your C turns failure into success → immediate gain k>1 vs D→1  
     play C  
     drought ← 0  
     return  
   
   // Otherwise prev_coops < m–1 => cannot reach threshold by yourself  
   drought ← drought + 1  
   if drought > L:
     // Group has never succeeded for L+ rounds; try a probe
     with probability δ:
       play C
     else:
       play D
     return
   else:
     play D
     return  

At the end of each round (after observing actual cooperators this round), update  
   prev_coops ← (number of C’s you observed from others this round, excluding yourself)  
   if prev_coops ≥ m: drought ← 0  
   // otherwise drought already incremented above  

5.  Aggressive mindset explained  
   – You never waste a C unless it immediately boosts your own payout from 1 → k.  
   – You never voluntarily join a “just-barely” cooperative group unless you are the pivotal contributor.  
   – You free-ride whenever the group is already safe.  
   – You only experiment (risk a lone C with no guarantee) after the group has repeatedly failed, but even then only with small probability δ.  
   – You never seek to build long-term goodwill; your only concern is maximizing each round’s immediate payoff subject to grabbing the public good when it is already almost guaranteed.  

This strategy will exploit any more forgiving or reciprocity-based schemes: it “punishes” would-be cooperators by withholding cooperation except where personally indispensable, and it never “reciprocates” beyond that narrow rescue.
'''

description_AGGRESSIVE_86 = '''
Below is a single‐strategy proposal—“Aggressive Threshold Exploiter” (ATE)—that (i) exploits cooperators whenever it can safely do so, (ii) contributes only when strictly necessary to secure the public good, and (iii) always defects in the final round.  

1.  Definitions  
   Let  
   •  n = number of players  
   •  m = minimal cooperators needed for success  
   •  r = total rounds, indexed t = 1…r  
   •  c_i(t) ∈ {0,1} your action in round t (1=C, 0=D)  
   •  C_others(t–1) = number of cooperators among opponents in last round (t–1)  

2.  Core idea  
   In each round (except the last), cooperate only if your single contribution turns a likely failure into a success; otherwise defect and free‐ride on others’ efforts.  In the final round, always defect (no future payoffs to protect).  

3.  Decision rules, in pseudocode  

```
# Prior belief p0 about any opponent cooperating in round 1
p0 = 0.5  

for t in 1…r do  
    if t == r:
        # Last round: always defect
        c_i(t) = 0  
        continue  
    end if  

    if t == 1:
        # No history yet: estimate E = expected # of other cooperators
        E = (n–1) * p0  
    else:
        # Use last round’s actual cooperators
        E = C_others(t–1)  
    end if  

    if E >= m:
        # Others alone will meet threshold, so defect & free-ride
        c_i(t) = 0  
    elseif E == m–1:
        # Exactly one spot left: contribute to secure the bonus
        c_i(t) = 1  
    else:
        # Even with my C, total < m: threshold will fail
        # Better keep your endowment
        c_i(t) = 0  
    end if  
end for
```

4.  Handling edge cases  
  • Round 1: Use a neutral prior p0=0.5 (or any fixed prior) to compute an expected E0=(n–1)·p0.  Then apply the same “E ≥ m? …” logic.  
  • Rounds with noisy behavior: we always re‐estimate E from the immediately preceding round only.  If you see sudden spikes in cooperation, you continue to exploit them in the very next round.  
  • Last round (t=r): no incentive to build reputation—always defect.  

5.  Why is this aggressive?  
  – You never “forgive” or “reward” defectors—you only cooperate when it is strictly pivotal.  
  – You free‐ride on full successes (E ≥ m) and save your endowment, harvesting the bonus without contributing.  
  – You refuse to “waste” your endowment on hopeless rounds (E < m–1).  
  – You always defect in the final round, denying any last‐round cooperative gains to others.  

This strategy maximizes individual return by contributing the bare minimum needed to trigger the public‐good payoff—and otherwise punishing or ignoring cooperators entirely.
'''

description_AGGRESSIVE_87 = '''
Below is an “Aggressive Exploit‐or‐Push” strategy.  It is memory‐1, always seeks to maximize immediate payoff, and only “cooperates” when your lone contribution turns failure into success (i.e. gives you the reward you would otherwise forego).  In all other situations you defect to exploit cooperators or simply keep your endowment.

1.  Data you carry between rounds  
    • last_cooperators: number of C’s you observed in the previous round  
    • r: total rounds, t: current round index  

2.  Initialization (before round 1)  
    • last_cooperators ← m   (treat as if threshold already met, so you start by defecting)  
    • t ← 1  

3.  Decision rule for round t (1 ≤ t ≤ r):

    let c_needed_without_you = last_cooperators  
    // If others cooperated last round, assume similar behavior this round

    if t = r then  
        // Last round: no future, always defect to grab endowment  
        play D  
    else if c_needed_without_you ≥ m then  
        // Even without you, threshold likely met → you defect to exploit  
        play D  
    else if c_needed_without_you = m − 1 then  
        // Your single C will push the group from failure → success  
        // Cooperate only if it yields immediate +k on top of 0  
        play C  
    else  
        // (c_needed_without_you < m−1)  
        // Even with you, threshold fails → no gain from C, so defect  
        play D  

4.  After observing the round’s actions:  
    • last_cooperators ← the total number of C’s you observed this round  
    • t ← t + 1  

5.  Rationale & Aggression  
    – You never “risk” contributing when it doesn’t raise the payoff.  
    – You only sacrifice your private endowment (c_i=1) when it single‐handedly pushes cooperators from m−1 to m, earning you +k on top of 0.  
    – In all other cases you defect, either exploiting others’ cooperation or avoiding wasted contributions.  
    – In the final round you always defect (classic end‐game).  

Pseudocode sketch  
-----------------

    function AggressiveExploitOrPush(m, r):
        last_cooperators ← m    // assume threshold met → start by defecting
        for t in 1…r:
            if t == r:
                action ← D
            else if last_cooperators ≥ m:
                action ← D
            else if last_cooperators == m − 1:
                action ← C
            else:
                action ← D

            play(action)
            observe opponents’ actions → countC
            last_cooperators ← countC

This strategy is “aggressive” because it never forgoes a sure-gain except in the one case where your cooperation immediately converts a failed round into a successful one, and always defects otherwise—even on the first and last rounds.
'''

description_AGGRESSIVE_88 = '''
Here is a fully specified “aggressive” repeated‐game strategy—call it PROBE-AND-EXPLOIT.  The high-level idea is:

  •  In the very first round and in the last round, always defect (no future to reward you).  
  •  For a small probing window of T rounds you occasionally cooperate so as to discover whether the other players can pull off a threshold success.  
  •  As soon as you ever observe a successful threshold (≥ m cooperators) you switch forever to pure defection and free-ride their cooperation.  
  •  If you exhaust your probing window without ever seeing a success, you also switch to permanent defection (no point in cooperating further).  

State variables:  
  state ∈ {PROBE, EXPLOIT, DEFECT}  
  t = current round index (1…r)  
  T = number of rounds you will probe (e.g. T = min(⌈r/4⌉, 3) or any small integer ≥1)  
  p_probe = probability of cooperating while in PROBE (e.g. 0.3)  

Pseudocode:

  initialize  
     state ← PROBE  

  for t = 1 to r do  
    if t = 1 or t = r then  
      action ← D  
    else if state = PROBE then  
      if t ≤ T then  
        with probability p_probe: action ← C  
        else:            action ← D  
      else  
        /* probing window over */  
        state ← DEFECT  
        action ← D  
      end if  
    else  
      /* state = EXPLOIT or DEFECT */  
      action ← D  
    end if  

    play action simultaneously, then observe total_cooperators_this_round  

    /* State transitions after observation */  
    if state = PROBE and total_cooperators_this_round ≥ m then  
      /* group proved it can succeed—time to free-ride */  
      state ← EXPLOIT  
    end if  
  end for  

Explanation of the pieces:

1. First round (t=1): defect.  No history yet, no future reward to gain by pretending.  
2. Last round (t=r): defect.  There is no future to punish or reward, so the one-shot Nash move.  
3. PROBE phase (t=2…T):  
   – Occasionally cooperate (with a low probability p_probe).  
   – If those tentative cooperations ever yield a successful round (≥ m total C’s including your own), you learn “they can do it.”  You immediately switch to EXPLOIT.  
4. EXPLOIT phase (any t after you saw a success):  
   – Always defect, free-riding on the other players’ continued cooperation if they try to maintain it.  
5. DEFECT phase (if probing ends with no success by t=T):  
   – Always defect, since no coalition is forming and cooperating only gives you 0.  

Why is this aggressive?  
  – You never sustain cooperation for its own sake—only tolerate it long enough to detect a cooperative bloc you can exploit.  
  – As soon as you see them hit the threshold once, you “go rogue” and defect forever, pocketing 1 + k each round if they keep cooperating.  
  – You never forgive—once in EXPLOIT or DEFECT state you never return to C.  

Edge cases:  
  – If a success arrives at t ≤ T, you exploit immediately that very same round’s observation and all future rounds.  
  – If no success by t = T, you abandon any hope of a coalition and defect for the rest (rounds T+1…r).  
  – Always defect in the last round to avoid being suckered.  

Parameter choices (example):  
  – T = min(⌈r/4⌉, 3) rounds of probing  
  – p_probe = 0.3 (so you don’t hand out free C’s too often)  

You can tune (T, p_probe) to the expected noisiness of your opponents.  But the core is: a brief testing phase followed by unrelenting defection as soon as a cooperative potential is detected—or as soon as probing fails.
'''

description_AGGRESSIVE_89 = '''
Here is an “aggressive” repeated‐game strategy that maximizes your own payoff by free‐riding whenever possible and only contributing when you can be the pivotal cooperator who tips the group over the threshold.

1. High‐level idea  
  •  By default, always defect (D) and collect the private payoff of 1.  
  •  Only cooperate (C) when you predict that exactly m–1 of the other n–1 players will cooperate; in that case your single contribution secures the public good and pays k>1, yielding you k instead of 1.  
  •  Never cooperate if you expect m or more opponents to cooperate (you’d only get k for zero payoff) or if fewer than m–1 of them will cooperate (a lone C costs you 1 and fails to trigger the bonus).

2. Notation & memory  
  Let t=1…r index the rounds.  
  Maintain for each opponent j a running count coop_count[j] = number of times j has played C so far.  
  In round t>1 estimate opponent j’s cooperation probability as  
     p_j = coop_count[j] / (t–1).  
  Then estimate total cooperators among opponents as  
     E = Σ_{j≠you} p_j.

3. Decision rule in each round t  
  
  if t == 1:  
    Action ← D    // no history, default to defection  
  else:  
    Compute E = Σ_j p_j (j runs over the other n–1 players)  
    if E ≥ m then  
      Action ← D    // threshold already likely met without you; free‐ride  
    else if E < m–1 then  
      Action ← D    // even adding your C won’t hit m; no point in paying cost  
    else    // m–1 ≤ E < m  ⇒ you are potentially pivotal  
      Action ← C    // you can turn failure into success and earn k>1  

4. Update memory  
  After all moves in round t become public,  
    for each opponent j:  
      if j played C then coop_count[j] ← coop_count[j]+1  

5. Edge cases & remarks  
  • Last round (t=r): same logic applies, because there is no future to preserve—your rule is purely myopic expected‐value maximizing.  
  • If the opponents suddenly coordinate m cooperators with high probability, you will continue to defect and reap 1+k each round.  
  • If they coordinate only m–1, you tap in exactly when needed to earn k instead of 1.  
  • If they fall below m–1, you refuse to pour in a lone coin that would be wasted.  

This strategy is “aggressive” because it never cooperates for the sake of group success—it only contributes when it is strictly in your own immediate interest to do so, and otherwise free‐rides or lets the group fail.
'''

description_AGGRESSIVE_90 = '''
Below is an “opportunistic‐aggressive” threshold‐exploitation strategy.  The idea is that you almost always defect, but whenever the group is one cooperator short of hitting the public‐good threshold, you “ambush” by cooperating so that the threshold is met—and then in subsequent rounds you defect again to free‐ride on others’ pushes.

1.  Notation  
   • t = round index, t=1,…,r  
   • coop_prev = number of players (including you) who chose C in round t–1  
   • m = cooperators needed for the public good  
   • r = total rounds  

2.  High-level description  
   • You never cooperate just for group welfare—only when your single C will push the tally from m–1 to m, because that maximizes *your* payoff in that round.  
   • Otherwise you defect.  

3.  Pseudocode  
```
initialize coop_prev ← 0   // before round 1 we treat “previous cooperators” as 0

for t in 1..r:
    if coop_prev == m–1:
        choose action[t] ← C      // your single C will trigger the group reward
    else:
        choose action[t] ← D      // defect in all other situations

    // after everyone has acted, you observe how many cooperated this round
    coop_prev ← number_of_players_who_played_C_in_round_t
end for
```

4.  Why this is aggressive  
   – “Always‐defect” except in the minimal circumstance where *your* cooperate move instantly delivers k to everyone.  You never pay a cost for group welfare that you cannot immediately recoup.  
   – You never enter a sustained cooperative phase—there is no “forgive‐and‐forget” or tit-for-tat.  You exploit any near-threshold situation and otherwise punish (by defecting) any attempt at mutual cooperation.  

5.  Edge cases  
   – First round (t=1): coop_prev=0 → you defect.  
   – Last round (t=r): you still apply the same rule—if coop_prev==m–1 you cooperate once more to seize the one‐shot k; otherwise defect.  
   – If opponents coordinate on C=C=C… and push well above m, you simply continue to defect, free-riding every time.  
   – If they never approach m–1 cooperators, you never waste a cooperation.  

This strategy guarantees that whenever you can alone tip the group into the k‐payoff region you will do so, and in all other cases you defect, maximizing your own return and punishing any attempt at stable cooperation.
'''

description_AGGRESSIVE_91 = '''
Below is a fully specified, “aggressive” threshold‐exploiter strategy.  In plain English it does the bare minimum cooperation necessary to let the other players hit the public‐good threshold, then defects to pocket the larger return for itself.  At all other times it defects.

1.  Data structures and bookkeeping  
   • For each player j≠i keep a running count H_j of how many times j has cooperated so far.  
   • Track t, the current round (1…r).  

2.  Prediction rule  
   We assume that in round t every other player j will behave exactly as they did in round t–1.  Let  
     prev_coops := number of players (≠i) who played C in round t–1.  
   In round 1 we have no history, so we set prev_coops := 0.

3.  Decision rule for round t  
   Let x := prev_coops.  We compare x to the threshold m:  
     a)  If x  ≥  m  then  
            // Even without me there are already at least m cooperators,  
            // so I defect and still get 1 + k.  
         action ← D  
     b)  Else if x = m–1  then  
            // If exactly m–1 others cooperated last time,  
            // by cooperating now I push them over the threshold  
            // and earn k > 1 (i.e. 0 + k) instead of the default 1.  
         action ← C  
     c)  Else  
            // Fewer than m–1 others cooperated:  
            // cooperating would yield 0 (project fails), defecting yields 1.  
         action ← D  

   In the last round (t = r) we use the very same rule—no need for “end‐game” variation,
   since defecting when x≥m or x<m–1 is already dominant, and only in the knife‐edge case x=m–1
   do we briefly cooperate to pump the group over the line.

4.  Update after observing round t results  
   • For each j≠i, if j played C this round then H_j ← H_j + 1.  
   • Record prev_coops := number of C’s you just observed among the others.  
   • Increment t and repeat until t>r.

Pseudocode
—————
initialize H_j := 0 for all j≠i
prev_coops := 0
for t in 1…r do
    x := prev_coops
    if x ≥ m then
        play D
    else if x = m – 1 then
        play C
    else
        play D
    end if

    observe opponents’ moves
    prev_coops := count of C’s among opponents
    for each j≠i who played C do H_j := H_j + 1
end for

Why it’s “aggressive”
———————
• It never blindly cooperates—only does so when it can just tip the other m–1 cooperators into success and then reap the full k payoff.  
• It never allows itself to be “trapped” in mutual cooperation—if the others are already meeting the threshold, it defects to pocket the extra k.  
• It never forgives or signals—purely myopic, exploitative, threshold-based behavior.
'''

description_AGGRESSIVE_92 = '''
Below is an “aggressive” repeated-play strategy—call it Threshold-Freerider with Grim Exploit—that (1) never volunteers unless it can single-handedly swing the threshold, (2) once it has successfully freeridden keeps defecting forever, and (3) always defects in the first and last rounds to maximize extraction.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Definitions  
  • r : total rounds, indexed t = 1,…,r  
  • m : cooperation threshold (1 < m < n)  
  • c_i,t ∈ {0,1} : your contribution in round t (1 if C, 0 if D)  
  • H_t : total # of cooperators in round t (including you)  
  • O_t = H_t − c_i,t : # of cooperators among the other (n–1) players in t  

2. State variable  
  • Freed = false  “Has the strategy already freeridden a successful round?”  

3. Decision Rule for round t  

   if t == 1 or t == r then  
     play D  (never cooperate in first or last round)  
     continue  

   if Freed == true then  
     play D  (grim: once you’ve reaped a reward you never help again)  
     continue  

   look at last round (t–1): compute O = O_{t–1}  

   if O >= m then  
     # Others would have cleared threshold without you => freeride  
     play D  
     # You defected while H≥m ⇒ you just pocketed reward; flip Grim flag  
     Freed ← true  
     continue  

   if O == m−1 then  
     # You alone can swing the group to reach threshold ⇒ cooperate  
     play C  
     continue  

   # In all other cases (O < m−1): hopeless to meet threshold by you alone ⇒ defect  
   play D  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
4. Pseudocode  

  initialize Freed ← false  
  for t in 1…r:  
    if t == 1 or t == r:  
      action ← D  
    else if Freed:  
      action ← D  
    else:  
      let O ← # cooperators among others in round t–1  
      if O >= m:  
        action ← D  
        Freed ← true     # once you’ve reaped the k‐bonus, never help again  
      else if O == m−1:  
        action ← C        # swing the group across the threshold  
      else:  
        action ← D  
    end  
    submit action  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
5. Discussion of aggressiveness  

  • Exploitative opening (t=1 always D)  
  • Never invests unless it can alone secure the bonus (O==m−1).  
  • Once it freerides a successful round (O≥m), it defects forever (grim trigger).  
  • Defects in the final round to grab the private endowment.  

This maximizes your private payoffs by (a) free-riding whenever possible, (b) punishing any fleeting coalition by withdrawing support thereafter, and (c) only ever “helping” when you can guarantee the extra k back for yourself.
'''

description_AGGRESSIVE_93 = '''
Below is an “exploit‐only‐when‐needed” strategy that never wastes cooperation except to trigger the group reward for your own benefit, and otherwise defects aggressively—even in early and late rounds.

1.  Key idea  
   •  Always defect (D) except in the very specific case where your one extra C will push the number of cooperators from m–1 to m.  
   •  In that case you cooperate (C) so that everyone—including you—earns the bonus k, but you still gain more than any cooperator.  
   •  First and last rounds are pure defection to avoid being suckered.

2.  Decision rules  
   Let t = current round (1 ≤ t ≤ r). Let coopCount[t–1] = number of players (including you) who cooperated in the previous round.  
   action(t):  
     if t == 1 or t == r:  
       play D  
     else if coopCount[t–1] == m – 1:  
       play C  
     else:  
       play D  

3.  Edge‐case handling  
   •  First round (t=1): No history ⇒ defect.  
   •  Last round (t=r): Defect to avoid end‐game exploitation.  
   •  If coopCount[t–1] < m–1: Threshold is not “one away,” so defect (you won’t single‐handedly get k).  
   •  If coopCount[t–1] ≥ m: Group already reached threshold without you ⇒ defect to exploit their cooperation and earn 1+k rather than 0+k.  

4.  Pseudocode  
   ```
   for t in 1..r:
       if t == 1 or t == r:
           action = D
       else:
           c_prev = number of C in round t-1
           if c_prev == m - 1:
               action = C
           else:
               action = D
   ```

5.  Why it’s aggressive  
   – You never “waste” a contribution unless it guarantees the bonus.  
   – When the group already would get the bonus without you, you defect to pocket the extra private payoff.  
   – You refuse to be the sucker in the first or last round, when there’s no future to punish or leverage.
'''

description_AGGRESSIVE_94 = '''
Below is a fully‐specified aggressive “Opportunist + Punisher” strategy for the repeated collective‐risk dilemma.  It combines (1) free‐riding whenever safe, (2) pivot‐cooperation only when strictly necessary to secure the group reward, and (3) a grim‐punishment regime that, once invoked, defects forever.  

1. State variables  
   • punished ∈ {false, true}, initially false.  
   • history of cooperations per round: coop_count[t] for t < current round.  

2. Decision rule, for each round t=1…r:  
   if t = r  
     – In the last round, play D.  (No future to punish or reward.)  
   else if punished = true  
     – Play D.  (Grim‐punishment: never cooperate again.)  
   else if t = 1  
     – First round, no history ⇒ play D.  (Assume others will provide the threshold.)  
   else  
     // We have a history and punishment is off:  
     Let L = coop_count[t–1].  
     if L ≥ m  
       // Last round the threshold was met without our cooperation.  
       // Safe to free‐ride again and extract maximum.  
       play D  
     else if L = m–1  
       // We were the pivotal player last round (or could be this round).  
       // If we defect here, group fails and everyone gets only 1;  
       // if we cooperate, we secure +k for ourselves and all others.  
       play C  
     else  
       // Even if we switch, others won’t reach m;  
       // so cooperating is wasted ⇒ free‐ride.  
       play D  

3. Punishment trigger  
   Immediately after observing the outcome of round t, update:  
   if punished = false AND coop_count[t] < m  
     AND (we played C in t OR coop_count[t] ≥ m–1)  
     // We either cooperated and still failed, or we were in a pivotal position  
     // but the group collectively let the reward slip ⇒ they “owe” us a punishment  
     then set punished ← true  

4. Pseudocode  

   initialize punished ← false  
   for t in 1…r do  
     if t = r then  
       action ← D  
     else if punished then  
       action ← D  
     else if t = 1 then  
       action ← D  
     else  
       L ← coop_count[t–1]  
       if L ≥ m then  
         action ← D  
       else if L = m–1 then  
         action ← C  
       else  
         action ← D  
     end  
     play action  
     observe coop_count[t], own payoff  π_i,t  
     if not punished and coop_count[t] < m then  
       // group failed  
       if action = C or coop_count[t] ≥ m–1 then  
         punished ← true  
       end  
     end  
   end  

5. Explanation of aggression  
 – We never “waste” a cooperation except when we are the pivotal actor who alone can secure the group reward.  
 – We free‐ride on any history of successful thresholds.  
 – If the group ever fails to meet the threshold when it reasonably could have (i.e. we cooperated or the group was one cooperator short), we switch to permanent defection, punishing everyone.  
 – In the final round we always defect, since there is no future to leverage.  

This strategy maximizes your own payoff by  (a) exploiting cooperative others, (b) only cooperating when absolutely necessary, and (c) wielding the threat of endless punishment to deter others from letting the group fail.
'''

description_AGGRESSIVE_95 = '''
Below is an “aggressive‐extortion” strategy for the repeated Collective Risk Dilemma.  Its guiding principle is:  
 “I will only contribute when absolutely necessary to push the group over the threshold; otherwise I always defect to free‐ride or punish.”

1.  Decision rules (per round t):

   a.  If I am in one of the last two rounds (t ≥ r–1):  
       –  Always Defect.  (No future to enforce cooperation or extract value.)

   b.  Else if t = 1:  
       –  Defect.  (No history yet; aggressive default is to grab the 1.)

   c.  Otherwise (2 ≤ t ≤ r–2):  
       1.  Compute p = fraction of cooperations among the other n–1 players over all past rounds 1…t–1.  
       2.  Estimate expected number of cooperators this round:  
            E = p × (n–1)  
       3.  If E ≥ m:  
            –  Defect.  
            (Threshold likely met without me; I free‐ride for 1 + k.)  
       4.  Else if E ≥ m–1:  
            –  Cooperate.  
            (I’m pivotal: my 1‐unit sacrifice turns failure into a +k windfall.)  
       5.  Else:  
            –  Defect.  
            (Even with me, threshold unlikely; no point contributing.)

2.  Edge‐cases handled:

   –  First round: defect by default.  
   –  Last two rounds: defect unconditionally (end‐game).  
   –  If m–1 = 0 (i.e. m=1), rule “E ≥ m–1” always true, but m>1 by spec so we never divide by zero.  
   –  If history so far shows zero cooperation (p=0), then E< m–1 and we defect until possibly others start cooperating.

3.  Pseudocode

   Let H be an array of length t–1 recording each observed other‐player action (1 for C, 0 for D).

   For t in 1…r:
     if t == 1:
       action[t] = D
     else if t >= r–1:
       action[t] = D
     else:
       p = (sum of H) / ((t–1) * (n–1))
       E = p * (n–1)
       if E >= m:
         action[t] = D
       else if E >= m–1:
         action[t] = C
       else:
         action[t] = D
     play action[t]
     observe other players’ actions this round and append to H

4.  Why it’s aggressive:

   –  You never “altruistically” contribute early—only when you can guarantee a +k payoff by being pivotal.  
   –  You free‐ride on others whenever threshold would be met without you.  
   –  You punish failed coordination by refusing to help if they can’t get within one cooperator.  
   –  You revert to pure defection at the end so there is no last‐round guilt.  
   –  Over the tournament this yields high individual payoffs at the expense of naïve cooperators.
'''

description_AGGRESSIVE_96 = '''
Below is a self‐contained, “aggressive” repeated-game strategy for the Collective Risk Dilemma.  It (a) defects by default, (b) only cooperates when it is absolutely pivotal to reach the threshold, and (c) immediately “grim‐triggers” into permanent defection at the first sign of others free‐riding when the group could have succeeded without you.  

—–  

1.  State variables  
   • punished (boolean) – set to true if we ever detect free‐riding in a successful round.  Once true, we defect forever.  
   • last_coop_count (integer) – number of cooperators observed in the previous round (including ourselves).  
   • r, m, k, n as given.  

2.  Initialization  
   punished ← false  
   last_coop_count ← 0  

3.  Per‐round decision rule (for round t = 1,…,r):  

   if punished == true then  
       action ← D    // once triggered, defect forever  
   else if t == 1 then  
       // Round 1: pure probe/greedy start  
       action ← D  
   else if t == r then  
       // Last round: no future to punish, so always defect for the 1-point private payoff  
       action ← D  
   else  
       // intermediate rounds t = 2..r–1 and not yet punished  
       let Cprev = last_coop_count    // total cooperators observed in round t–1  

       // Detect free‐riding in the previous round:  
       if Cprev ≥ m then  
           // group succeeded without us—any D among them is free‐riding  
           // trigger permanent punishment  
           punished ← true  
           action ← D  
       else  
           // If exactly m–1 cooperators last time, our single C will tip them over  
           if Cprev == m–1 then  
               action ← C  
           else  
               // either Cprev < m–1 (too few to save) or Cprev > m–1 (we can free‐ride)  
               action ← D  
           end  
       end  
   end  

4.  Observation update (end of each round t):  
   – Count how many players (including yourself) chose C this round → new_count.  
   – last_coop_count ← new_count  

—–  

Explanation of the logic  
1. Default Defection: We begin by defecting (round 1) to see what others do and grab the safe 1-point payoff.  In the last round we also defect, since there is no future to influence.  
2. Pivotal Cooperation Only: In any nonterminal round, if exactly (m – 1) players cooperated last time, this round you switch to C, because your 1-unit sacrifice guarantees the group reward k units (>1) to you.  In every other scenario you defect.  
3. Grim Punishment of Free‐Riders: If in the previous round the group still achieved the threshold (last_coop_count ≥ m), then some players must have been free-riding.  You immediately flip “punished = true” and defect forever after.  This is maximal aggression: any free-rider anywhere dooms your future cooperation.  

Advantages of this aggressive plan  
• You never sacrifice unless absolutely necessary for the public good—minimizing cost.  
• You free-ride whenever the group would succeed without you, grabbing the extra +1 each time.  
• You mete out instant, permanent punishment at the first sign of free-riding in a successful round—discouraging others from exploiting the common fund.  

Edge‐Cases handled  
– First round t = 1: Defect to secure the private payoff and learn about initial cooperators.  
– Last round t = r: Defect to harvest the private payoff—no future leverage.  
– After any round with success (≥ m Cs) in which you could have been unnecessary, you never cooperate again.  

This strategy maximizes your exploitation of others’ contributions, only pays the cooperation cost when you alone are pivotal, and brutally withdraws cooperation indefinitely the first time opponents free-ride.
'''

description_AGGRESSIVE_97 = '''
Below is an “Aggressive Pivot-and-Punish” strategy.  It free-rides whenever possible, only contributes when strictly necessary to secure the bonus, and punishes any player who “over-cooperates” (i.e. helps when help isn’t needed).

1.  State & Memory  
    •  Round counter t = 1,…,r  
    •  Last round cooperators count lastC (undefined at t=1)  
    •  Blacklist B ⊆ {1…n}\{you}: players deemed “over-cooperators.”  

2.  Initialization  
    t ← 1  
    B ← ∅  
    lastC ← n   (pretend everyone cooperated so you will defect in round 1)  

3.  Update Blacklist (after observing round t)  
    For each opponent j who played C in round t:  
      if lastC ≥ m then  
        add j to B   (they cooperated even though ≥m others already did)  
    lastC ← actual number of players who played C in round t  

4.  Decision Rule (at the start of round t)  
    if t = r (last round) then  
      play D  // no future to punish, so always defect  
    else if lastC ≥ m then  
      // Others can deliver threshold without you  
      play D  
    else if lastC = m–1 then  
      // You are pivotal: others will miss threshold by one if you defect  
      // Normally you’d cooperate to get k; but if any of the m–1 last cooperators  
      // are on your blacklist, punish them by defecting anyway  
      let lastCooperators = set of players who played C in round t–1  
      if lastCooperators ∩ B ≠ ∅ then  
        play D   // punish “over-cooperators,” even at your own cost  
      else  
        play C  
    else  
      // lastC < m–1: even if you cooperate, threshold fails  
      play D  

5.  Pseudocode  

  initialize B ← ∅, lastC ← n  
  for t in 1..r do  
    if t = r then  
      action ← D  
    else if lastC ≥ m then  
      action ← D  
    else if lastC = m–1 then  
      if (players_who_cooperated_last_round ∩ B) ≠ ∅ then  
        action ← D  
      else  
        action ← C  
    else  
      action ← D  
    submit action  
    observe all moves; let cooperators_t be those who played C  
    // Update blacklist  
    if lastC ≥ m then  
      for each j in cooperators_t: B ← B ∪ {j}  
    lastC ← |cooperators_t|  

6.  Why it’s aggressive  
  •  You never “volunteer” to hit the threshold—only do so when you alone can swing it.  
  •  You free-ride whenever m or more others are cooperating.  
  •  You punish any player who cooperates unnecessarily by blacklisting them and then refusing to help them in future pivotal moments—even at your own short-term expense.  
  •  You defect in the final round to maximize your private gain when there is no threat of retaliation.
'''

description_AGGRESSIVE_98 = '''
Below is an “aggressive” repeated‐play strategy for the Collective Risk Dilemma.  In plain English it can be described as:  

“Defect in every round except the handful of occasions when your single contribution is strictly pivotal to meeting the cooperation threshold—and even then never in the final round.  Exploit cooperators whenever you safely can.”  

---  
1.  Key idea (“Pivotal Defector”)  
   • You only ever cooperate if, by defecting, you would cause the group to fall below m.  In all other rounds you free‐ride.  
   • In the very last round you never cooperate (end‐game defection).  

2.  Notation  
   Let  
   • r = total rounds, t ∈ {1…r} the current round.  
   • m = cooperation threshold.  
   • obsCoop[t–1] = number of players (including you) who cooperated in round t–1 (for t = 1 define obsCoop[0] := m).  
   • prevAction = your action in the previous round (“C” or “D”).  

3.  Decision rule for round t  

   if t == r:  
     action ← D    // Last‐round defection  
   else:  
     // Compute how many of the other (n–1) players you expect to cooperate  
     let coopOthersPred = obsCoop[t–1]  
       – (prevAction == C ? 1 : 0)  
       // (For t=1 we initialized obsCoop[0]=m, so coopOthersPred=m–(did-I-cooperate?))  

     if coopOthersPred ≥ m:  
       // Plenty of cooperators even if you defect  
       action ← D  
     else if coopOthersPred == m–1:  
       // Your C is pivotal: without you they’d fail  
       action ← C  
     else:  
       // Even if you contribute, they fall short  
       action ← D  

4.  Update after the round  
   Observe how many actually cooperated this round; set  
     obsCoop[t] = observed count.  
   Set prevAction = action, then proceed to t+1.  

5.  Edge cases & comments  
   • First round (t=1): obsCoop[0] is set to m, so coopOthersPred=m–0=m ⇒ you defect.  
   • If at any point coopOthersPred < 0, treat it as zero (no one cooperates).  
   • If coopOthersPred > n–1, cap at n–1.  
   • You never “forgive” or try to build trust.  You only ever “step in” when you alone can avert a collective failure—and even then you skip cooperation in the final round.  

6.  Why it’s aggressive  
   – It exploits any surplus of cooperators by always defecting when you can.  
   – It never extends goodwill beyond the bare minimum required to avoid a payoff disaster.  
   – It refuses cooperation in the last round to maximize your relative gain once future retaliation is impossible.  

Pseudocode Summary  
────────────────────────  
```
initialize:
  obsCoop[0] ← m
  prevAction ← D

for t in 1…r:
  if t == r:
    action ← D
  else:
    coopOthersPred ← obsCoop[t-1]
                       - (prevAction == C ? 1 : 0)
    if coopOthersPred ≥ m:
      action ← D
    else if coopOthersPred == m - 1:
      action ← C
    else:
      action ← D

  play(action)
  observe obsCoop[t]  // total cooperators this round
  prevAction ← action
```
This strategy maximizes free‐riding, only “rescuing” the group when strictly necessary, and never in the final round—an archetypal aggressive approach.
'''

description_AGGRESSIVE_99 = '''
Below is a fully specified “aggressive” threshold‐public‐goods strategy.  It never cooperates unless doing so is strictly necessary to push the group from “no reward” to “reward,” and even then only when exactly the minimum number of other cooperators appeared in the previous round.  It also defects on the very first and very last round (no “end‐game” gifts) and otherwise exploits any surplus cooperators.

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
Name: Conditional Pivotal Defector (CPD)

Parameters (as given):
  n   = number of players  
  m   = minimum cooperators needed  
  r   = total rounds  

Notation:
  t             = current round (1 … r)  
  A_i(t)        = action of player i in round t (C or D)  
  H_{−i}(t–1)   = number of cooperators among the other n−1 players in the previous round  

Decision rule for player i:

1. If t = 1 (first round), play D.  
   Rationale:  No prior information; default to defection.

2. Else if t = r (last round), play D.  
   Rationale:  No future to punish, so free‐ride.

3. Else (2 ≤ t ≤ r–1):
     – Observe H_{−i}(t–1) = how many of the other players cooperated in round t–1.  
     – If H_{−i}(t–1) == m−1, play C (you are the pivotal cooperator).  
     – Otherwise play D.

Pseudocode  
----------
function chooseAction(t, history):  
  if t == 1 or t == r:  
    return D               # Always defect on first or last round  
  else:  
    count_OthersC ← number of C’s in history[t–1] excluding own action  
    if count_OthersC == m−1:  
      return C             # Only cooperate when exactly m−1 others did last round  
    else:  
      return D             # Otherwise defect  

Properties and aggressive mindset:

– Selfish “pivoting”: you only pay the cost (c_i=1) when you are strictly needed to trigger the group reward; otherwise you always free-ride.  
– No wasted cooperations: if fewer than m−1 others cooperated, your C would not tip the total to m, so you defect.  If ≥ m others cooperated, your C is unnecessary, so you defect.  
– End‐game free‐riding: in the last round, you never cooperate (no future rounds in which punishment or reward can be leveraged).  
– First‐round defection: you begin by testing the waters—others reveal themselves first.  

Edge-case handling:

– “Lock-out” risk: if in round 2–r–1 no one ever hits exactly m−1 cooperators in the previous round, no one cooperates and the threshold is never met.  That is an accepted risk for an aggressively selfish strategy.  
– If multiple players “think” they are pivotal (all see m−1 cooperators among the others), they may over-cooperate—but because each then sees ≥ m cooperators in the next round, everyone reverts to D immediately.  Over-cooperation is self-correcting and short‐lived.  
– Perfect information assumption ensures you always know H_{−i}(t–1) exactly.  

Overall payoff logic:

– You maximize your chance of collecting (1 + k) rather than k by being the defector whenever possible, yet you still occasionally supply the single extra contribution needed to secure the collective bonus.  
– By never cooperating in wasted rounds, you keep your private 1.  By cooperating only when pivotal, you ensure the reward k appears just often enough that you still collect k (or better, 1 + k) more cheaply than any more‐nice strategy.
'''

description_AGGRESSIVE_100 = '''
Below is a simple “aggressive exploit” strategy that maximizes your own payoff by defecting whenever you can and only cooperating in the bare‐minimum case when your single contribution will swing the group over the threshold.  It never “forgives” or “reciprocates” and treats every round in isolation.

────────────────────────────────────────────────────  
Strategy name: Opportunistic Defector  
────────────────────────────────────────────────────  

1. Data structures and bookkeeping  
   • r            — total number of rounds  
   • t            — current round (1…r)  
   • n            — number of players  
   • m            — cooperation threshold  
   • k            — reward factor (>1)  
   • history[t’][j] — action (“C” or “D”) of player j in past round t’, for t’ < t  
   • p_j          — estimated cooperation probability of opponent j  

2. Belief updating (after each round)  
   After observing everyone’s actions in round t, update  
     p_j ← ( # times j played C so far ) / (t)  
   for each opponent j.  

3. Decision rule (each round t = 1…r):  
   Step A. Predict how many cooperators will play C among the other (n–1) players.  
     E_coop_others  =  Σ_{j≠you} p_j  

   Step B. Decide:  
     if  E_coop_others  ≥  m   then  
          // Threshold will be met without you  
          play D  
     else if  E_coop_others  ≤  m – 2  then  
          // Even if you cooperate, threshold won’t be met  
          play D  
     else /* E_coop_others in [m–1, m) */  
          // Your single C will tip the threshold  
          // Compare payoffs:  
          //   if you cooperate, payoff = k  
          //   if you defect, payoff = 1  
          // Since k>1, you cooperate here to get k  
          play C  

   That’s it.  No exceptions for first or last round—every round is treated the same, except that on round 1 all p_j default to 0 so you defect, and thereafter you follow the rule above.  

4. Edge cases  
   • First round (t=1):  
     no history → assume p_j=0 for all j → E_coop_others=0 → you play D.  
   • Last round (t=r):  
     still apply the same rule.  No future to protect, so you only cooperate if your single C is enough to reach the threshold (i.e. exactly when E_coop_others ≥ m–1 and <m).  

5. Why is this “aggressive”?  
   – You never cooperate to reward or “build trust.”  
   – You only ever cooperate when doing so immediately maximizes your own one‐round payoff (and only then just barely).  
   – You never punish or reward history beyond using it to predict whether your contribution is pivotal.  

Pseudocode  
-----------  
```
initialize p_j = 0 for all opponents j
for t in 1..r do
  if t > 1 then
    for each opponent j:
      p_j = (# of times j played C in rounds 1..t–1)/(t–1)

  E = sum_{j≠you} p_j

  if E ≥ m then
    action = D       # exploit threshold already met
  else if E ≤ m–2 then
    action = D       # even your C can’t help
  else
    action = C       # you’re pivotal, and k>1 makes this worthwhile

  play(action)
  observe all players’ actions this round and record in history[t][*]
end for
```  

This strategy aggressively free-rides whenever it can, and contributes only when absolutely necessary to unlock the group reward that you can then exploit.
'''

description_AGGRESSIVE_101 = '''
Here is a highly aggressive, self-serving “Threshold-Sniper” strategy.  It never “wastes” a contribution except when you can pivotal­ly rescue the group—otherwise it always defects to freeride on whatever cooperation remains.  

1.  Definitions  
   •  t = round index, t = 1…r  
   •  A_t = number of opponents (out of n–1) who played C in round t  
   •  m = required number of total cooperators to earn k  

2.  Intuition  
   •  You gain most by defecting whenever possible.  
   •  Only cooperate if by doing so you turn a failed round into a success (i.e. if A_{t–1} = m–1).  
   •  Never cooperate if opponents already reach m or if they are too few (≤ m–2).  
   •  Always defect in the first round (test) and in the last round (no future to leverage).  

3.  Full Decision Rules  

  For t = 1 to r do  
    if t == 1 then  
      play D  // probe group, maximize immediate return  
    else if t == r then  
      play D  // no future rounds—always defect  
    else  
      let x = number of opponents who chose C in round t–1  
      if x == m–1 then  
        play C  // pivotal cooperation: you rescue the group and collect k – 1 net  
      else  
        play D  // either they already have threshold or can’t reach it even with you  
      end  
    end  
  end  

4.  Why it’s aggressive  
  •  You only ever incur the cost of cooperation (c_i = 1) when it flips the payoff from zero to k—i.e. when you’re pivotal.  Everywhere else you defect, capturing the full private return plus any public good if others manage to meet m.  
  •  You never “forgive” or enter nice-guy mode: there is no gradual tit-for-tat, no long-run cooperation, no appeals to fairness.  You seize every free ride, only giving back exactly when you must.  
  •  In the last round you always defect: there is no future punishment threat to enforce any cooperation, so you drop the mask entirely.  

5.  Edge cases  
  •  If in round t–1 opponents cooperated ≥ m, you know the group is strong—so you defect and still collect k.  
  •  If in t–1 opponents cooperated ≤ m–2, even your single coop won’t reach m, so you defect (coop would be pure loss).  
  •  If opponents ramp up cooperation dramatically (e.g. all C) you remain D every time—free-riding the maximum.  

This strategy guarantees you never “over-cooperate,” always exploits any surplus cooperation by others, and only pays the cost of contribution when you’re strictly pivotal.
'''

description_AGGRESSIVE_102 = '''
Below is an “Aggressive Exploiter” strategy.  It never cooperates unless its single contribution is strictly necessary to reach the threshold m; it free‐rides whenever it can; it punishes wasted “scoops” (i.e. whenever it contributes but the threshold still fails) by defecting forever thereafter; and it defects in the last round by backward induction.

1.  Data structures / state  
   • blame ← false  
     – Once set to true, the strategy defects in every remaining round (a grim trigger).  

2.  At each round t (1 ≤ t ≤ r) do:  
   Let prev_C = number of other players who chose C in round t–1.  
   (If t=1, define prev_C = 0.)  

   if blame == true then  
       play D  
   else if t == 1 or t == r then  
       // first‐ and last‐round defection  
       play D  
   else  
     if prev_C ≥ m then  
       // enough others will hit the threshold: free‐ride  
       play D  
     else if prev_C = m–1 then  
       // my 1 contribution is exactly needed to hit m  
       play C  
     else  
       // even if I cooperate, threshold will still fail: punish by defecting  
       play D  

3.  After observing the outcome of round t (i.e. learning how many cooperated including yourself and whether threshold was met):  
   if in round t you played C but total_C < m then  
     // I “wasted” a contribution and got no reward – punish permanently  
     blame ← true  

4.  Rationale / aggression profile  
   –   Free-rides whenever possible (prev_C ≥ m).  
   –   Contributes only when its single coin flips a failed public good into success (prev_C = m–1).  
   –   Otherwise defects to punish group failure.  
   –   Grim‐triggers if ever a contribution is squandered (i.e. it cooperates but threshold still fails).  
   –   Defects in the very first and very last round by default.  

5.  Pseudocode  

   initialize blame ← false

   for t in 1..r:
     if blame:
       action ← D
     else if t == 1 or t == r:
       action ← D
     else:
       prev_C ← count of others’ C in round t–1
       if prev_C ≥ m:
         action ← D
       else if prev_C == m–1:
         action ← C
       else:
         action ← D

     execute(action)
     observe total_C_this_round (including yourself)
     if action == C and total_C_this_round < m:
       blame ← true

This strategy is “aggressive” in that it never throws away endowment unless strictly necessary to secure the group reward; it free‐rides as soon as the threshold is met by others; it punishes wasted contributions by defecting forever; and by backward induction it defects in the last round.
'''

description_AGGRESSIVE_103 = '''
Below is an “aggressive‐opportunist” strategy.  In every round you free-ride (defect) by default, but you will grudgingly contribute just enough to flip the group past the threshold m when your single contribution is the difference between failure and success.  In the last round you never cooperate.

1.  State variables  
   •  coop_count[j] for each opponent j ∈ {1…n}, initialized to 0  
   •  t = current round index (1…r)  

2.  Decision rule (before observing others in round t)  

   if t == r:  
     action ← D   // In the final round you never cooperate  

   else if t == 1:  
     action ← D   // First round: you defect and see how much others cooperate  

   else:  
     // Estimate each opponent’s cooperation probability from history  
     for each opponent j ≠ you:  
       p_j ← coop_count[j] / (t−1)  
     sum_p ← Σ_{j≠you} p_j  

     // “Threshold swing” test  
     if sum_p ≥ m then  
       action ← D    // They alone suffice; you continue to free-ride  
     else if sum_p + 1 ≥ m then  
       action ← C    // Your 1 unit of contribution is just enough to meet m  
     else  
       action ← D    // Even if you cooperate, threshold still fails; keep your endowment  

3.  Update after observing round t outcomes  
   for each opponent j:  
     if j played C then coop_count[j] ← coop_count[j] + 1  

4.  Discussion of aggressiveness  
   – You never cooperate “just to be nice.”  You only pay the cost c=1 when it flips a losing round into a winning one.  
   – You default to defect even in early rounds, hoping others will carry the public project so you can capture the k bonus on top of your private 1.  
   – In the last round you defect unconditionally to collect the private payoff and deny any future retaliation.  

5.  Edge cases handled  
   – First round: no history ⇒ defect  
   – Last round: always defect  
   – Rounds 2…(r−1): you compute opponents’ empirical cooperations and cooperate only if sum_p+1≥m (i.e. you are pivotal)  

Pseudocode summary  
```
initialize coop_count[j]=0   for all opponents j

for t in 1…r:
  if t == r:
    action ← D
  else if t == 1:
    action ← D
  else:
    sum_p ← 0
    for each opponent j≠you:
      p_j ← coop_count[j] / (t−1)
      sum_p ← sum_p + p_j
    if sum_p ≥ m:
      action ← D
    else if sum_p + 1 ≥ m:
      action ← C
    else:
      action ← D

  play action; observe everyone’s actions
  for each opponent j:
    if j played C: coop_count[j] += 1
```

This “opportunistic threshold” strategy is aggressive: it never wastes contributions, exploits others whenever possible, and only relinquishes its endowment to secure the group reward when it’s the sole pivot to push cooperators over m.
'''

description_AGGRESSIVE_104 = '''
Below is an “Aggressive‐Punishing Opportunist” (APO) strategy.  In plain English it

• Defects by default  
• Only ever cooperates when its single contribution will tip the group over the m-threshold (so it never wastes its endowment)  
• The first and last rounds are guaranteed defections (no trust built, no end-game gifts)  
• If at any time the group achieves the threshold without APO’s help, APO “goes grim”: it defects every remaining round in permanent punishment  

State variables  
• punish_triggered ← false  

Per‐round decision rule, at round t (1 ≤ t ≤ r):  
1.  If t = 1 or t = r, play D.  
2.  Else if punish_triggered = true, play D.  
3.  Else observe last round’s other‐players’ cooperations, c_others = number of C’s by the n−1 opponents in round t–1.  
   a.  If c_others ≥ m then  
         – the group met the threshold WITHOUT APO’s help → punish_triggered ← true; play D  
   b.  Else if c_others = m−1 then  
         – APO can be pivotal: cooperating yields payoff (0 + k) > defecting (1 + 0) → play C  
   c.  Else  
         – even if APO cooperates the threshold will fail → play D  

Pseudocode  

```
initialize punish_triggered ← false

for t in 1..r do
  if t = 1 or t = r then
    action[t] ← D
    continue
  end if

  if punish_triggered then
    action[t] ← D
    continue
  end if

  # Observe how many of the other n–1 players cooperated in round t−1
  c_others ← count_of_C_among_opponents_in_round(t-1)

  if c_others ≥ m then
    # Group succeeded without our help → trigger permanent punishment
    punish_triggered ← true
    action[t] ← D

  elseif c_others = m − 1 then
    # We can tip the balance
    action[t] ← C

  else
    # Cooperation won’t reach threshold → defect
    action[t] ← D
  end if
end for
```

Why aggressive?  
– It never “wastes” a contribution on impossible thresholds.  
– It only ever helps when absolutely pivotal, then immediately punishes the group if they prove they don’t need it.  
– It refuses any end-game courtesy.  
– Once the group “learns” they can succeed without APO, APO switches to permanent defection (“grim trigger”), ensuring maximum exploitation and deterrence of future cooperation.
'''

description_AGGRESSIVE_105 = '''
Below is an “aggressive” pivot-only strategy—call it the “Pivot-Only Exploiter.”  It never cooperates for the sake of the group, it only ever cooperates when by doing so it alone turns a losing round into a winning one (so it maximizes its own payoff), and it never cooperates in the last round (no future to exploit).

1.  State variables you maintain  
   • history[t][j] ∈ {C,D}: action of player j in round t, for t<current round.  
   • myLastAction ∈ {C,D}, initialized to D.  
   • r, m, n: known game parameters.  

2.  High-level description  
   – Round 1: defect, to gauge others’ cooperativeness.  
   – Rounds t = 2,…,r–1: look at how many of the other n–1 players cooperated in round t–1.  
       • If exactly m–1 of the others cooperated last round, play C (i.e. you are pivotal).  
       • Otherwise play D.  
   – Round r (last round): always defect (no future to exploit or punish).  

  This yields cooperation only when it raises your own one-round payoff from 1 to k, never for goodwill or deterrence.  

3.  Pseudocode  

```
Initialize:
  myLastAction ← D
  history ← empty

For each round t from 1 to r do:
  if t == 1:
    action ← D

  else if t == r:
    action ← D        # last-round defection

  else:
    # count how many of the other players cooperated in round t–1
    let coopAll ← number of C’s in history[t–1][1..n]
    let coopOthers ← coopAll
    if myLastAction == C:
      coopOthers ← coopAll – 1

    if coopOthers == m – 1 then
      action ← C      # pivotal: cooperating gets payoff k > 1
    else
      action ← D      # either cannot swing the threshold, or it would succeed without me

  # play action, record it
  myLastAction ← action
  history[t][me] ← action
  observe and record history[t][j] for all j ≠ me
End for
```

4.  Explanation of “aggressiveness”  
 – Cooperates only to “exploit” others’ willingness: when exactly m–1 others stepped up last round, you swoop in to grab the full reward at zero personal cost.  
 – When the group can reach the threshold without you (coopOthers ≥ m) you always defect and free-ride.  
 – When you cannot help (coopOthers < m–1) you defect and let the disaster punish everyone.  
 – In the final round you always defect—no future retaliation/promotion value.  

This strategy is purely self-interested and opportunistic—and thus “aggressive” in that it never sacrifices for the group and never builds goodwill, it only pounces when it can personally flip a losing outcome into its own gain.
'''

description_AGGRESSIVE_106 = '''
Below is an “Aggressive-Pivotal” strategy for the repeated collective-risk dilemma.  It never cooperates unless doing so is strictly in your self-interest (i.e. it is pivotal) and otherwise defects to both maximize your own immediate payoff and punish opponents by denying them the group reward whenever you can.

1.  State variables and initialization  
   • r = total rounds, m = threshhold, n = number of players.  
   • t = current round index, t = 1…r.  
   • last_coops = # of players who cooperated in the immediately preceding round (initialize to 0).  
   • last_my_action = your action in the previous round (C or D), initialize to D.  

2.  Core decision rule (for round t):  
   Let others_last = last_coops – (last_my_action == C ? 1 : 0).  
   You estimate that in this round the other n–1 players will cooperate in number ≈ others_last.  

   Compute two quantities:  
   • If you defect, your payoff will be 1 if total cooperators (including you) < m; or 1 + k if total ≥ m.  
   • If you cooperate, your payoff will be 0 if total < m; or     k     if total ≥ m.  

   But you only care about your own payoff, so you ask: “Is my cooperation pivotal—that is, does the group only reach m if I switch to C?”  

   Formally:  
   A.  If others_last ≥ m  
         → even if you defect, total_coops ≥ m, so you get 1 + k.  
         → Cooperating would only reduce your private payout (you’d get       k   which is < 1 + k).  
         → Action: DEFECT.  

   B.  If others_last = m–1  
         → only if you play C will total_coops = m, so you get           k.  
         → if you play D, total_coops = m–1, so you get 1.  
         → Cooperating yields k vs defecting yields 1; since k > 1, it’s in your interest → COOPERATE.  

   C.  If others_last < m–1  
         → even with you at C, total_coops ≤ (m–2)+1 = m–1 < m, so no one hits the threshold.  
         → Cooperating gives you 0, defecting gives you 1 → DEFECT.  

3.  First‐round and last‐round handling  
   • Round 1: last_coops = 0 ⇒ others_last = 0 < m–1 ⇒ follow case C ⇒ DEFECT.  
   • Final round t = r: apply the same pivotal rule.  There is no future to worry about—only immediate payoff.  

4.  Updates after each round  
   After you observe the actual total_coops in round t:  
      last_coops := observed total_coops  
      last_my_action := your action this round (C or D)  

5.  Rationale and aggressiveness  
   – You never “generously” cooperate to help opponents build a winning coalition.  
   – You only cooperate when by doing so you turn a losing round (you’d get 1) into a winning one (you get k).  
   – Whenever you can deny everyone the group reward by defecting—i.e. when others_last ≥ m—you do so even at the cost of reducing the total group payoff from (1 + k) to 1 for each.  
   – This both maximizes your own payoff in that round (you get 1 + k vs k) and punishes cooperators by causing group failure.  

Pseudocode  

```
initialize last_coops = 0
initialize last_my_action = D

for t in 1..r:
    others_last = last_coops - (last_my_action == C ? 1 : 0)

    if others_last >= m:
        action = D       # free‐ride and punish
    else if others_last == m - 1:
        action = C       # you’re pivotal: cooperative payoff k > defect payoff 1
    else:
        action = D       # cooperating wouldn’t meet threshold, so you’d get 0

    play(action)

    observe total_coops_this_round
    last_coops = total_coops_this_round
    last_my_action = action
end for
```

This strategy is aggressive because it never “wastes” cooperation on cases where others already guarantee the threshold, and it actively sabotages opponents whenever doing so yields you a strictly higher immediate payoff.
'''

description_AGGRESSIVE_107 = '''
Below is an “aggressive” free‐riding strategy—call it the Marginal-Exploiter—that never builds trust, never sacrifices for the group, and only cooperates when your single contribution is pivotal to hitting the threshold.

1. Strategy name  
   Marginal-Exploiter (ME)

2. High-level description  
   ME defects by default.  It only cooperates in a round if it predicts that exactly m–1 other players will cooperate, so that your one unit of contribution pushes the group over the threshold and you reap the full reward k without “wasting” a contribution when it won’t change the outcome.

3. Decision rules  
   Let t = current round, Cₜ₋₁ = number of cooperators among the other n–1 players in the previous round (for t=1 we have no history).  
   – If t = 1 (no history yet): DEFECT.  
   – If t > 1:  
     • If Cₜ₋₁ == m–1 → COOPERATE (you are pivotal).  
     • Otherwise → DEFECT.

4. Pseudocode  

   initialize history H = []  
   for t in 1…r:  
     if t == 1:  
       action ← DEFECT  
     else:  
       let C_prev = number of C’s in H[t–1] among other players  
       if C_prev == m – 1:  
         action ← COOPERATE  
       else:  
         action ← DEFECT  
     play(action)  
     observe everyone’s actions this round and append to H

5. Rationale & aggression  
   – You never pay the cooperation cost unless you’re strictly pivotal.  
   – You aggressively refuse to build any cooperative reputation—there is no tit-for-tat, no forgiveness, no “nice” initiation.  
   – You maximize your own per-round payoff by free-riding whenever possible and only making the minimal investment required to capture k if and only if that investment turns a losing round into a rewarding one.

6. Edge-case notes  
   – First round: with no information, ME defects (assumes worst).  
   – Last round (t = r): same rule applies—there is no future to protect, so DEFECT unless Cₜ₋₁ == m–1.  
   – If the group never sends you a clear signal that exactly m–1 others will cooperate, ME will simply defect every round.  
   – No randomness or “last-ditch” contributions—you never waste a 1-unit coop when it can’t flip the outcome.
'''

description_AGGRESSIVE_108 = '''
Below is an “Aggressive Exploit‐and‐Punish” strategy.  Its philosophy is simple:  
– Phase 1 (Recruit): pump in cooperation just long enough to get one or two threshold successes and train your opponents to cooperate.  
– Phase 2 (Exploit): once you see cooperation work (or you grow impatient), switch to pure defection for the rest of the game (including the last round).  You thereby free‐ride when thresholds still get met, and also ensure that they eventually fail, punishing the other players’ payoffs.  

Once implemented, this strategy will typically outperform purely “nice” strategies in a tournament of independent LLM opponents, because you harvest the high‐payoff rounds early and then deny them to others.

—  
1. PARAMETERS  
 n ≥ 2 players, r > 1 rounds, threshold m (1 < m < n), reward factor k > 1  
 Set a small patience parameter W (e.g. W = min(3, r−1)).  W is the maximum number of rounds you’ll wait to see a successful threshold before you give up and defect forever.

2. INTERNAL STATE  
 phase ∈ {“recruit”, “exploit”}  
 waited = 0  // how many recruit rounds have passed without success

3. ACTION RULES  

for t = 1 to r do  
 if t == r then  
  action ← D  
  // Always defect in the final round—no future to punish  
 else if phase == “recruit” then  
  // We try to hit the threshold early  
  action ← C  
  waited ← waited + 1  
  // We only move to exploit once we see success or run out of patience  
  if (cooperators_last_round ≥ m) or (waited ≥ W) then  
   phase ← “exploit”  
  end if  
 else  // phase == “exploit”  
  action ← D  
 end if  
 play action  

4. EXPLANATION OF KEY POINTS  
– First round (t=1): no history ⇒ phase=”recruit”, so you play C.  
– You remain in recruit as long as thresholds have repeatedly failed and you haven’t hit W.  This encourages opponents to believe cooperation can pay.  
– As soon as you observe a round in which ≥ m cooperated, you switch permanently to “exploit,” defecting to free-ride on their future contributions (they still need one fewer cooperator, so you grab 1+k each time they succeed).  
– If cooperation never succeeds after W rounds, you give up and switch to “exploit” anyway—no point bleeding payoff trying to herd unwilling sheep.  
– Last round t=r: always defect, since there is no future to leverage with threats or promises.

5. WHY IT IS AGGRESSIVE  
– You “lure” players into cooperating by front-loading your own contributions, then you abruptly withdraw support.  
– You maximize your own haul in the rounds after the first success (or after your patience wears thin), and simultaneously punish the group by causing later failures.  
– By defecting in the final round, you grab the guaranteed 1-point payoff instead of risking a futile or costly contribution.

This strategy is parameterized only by your patience W and requires no communication, relying solely on the public history of how many cooperators appeared in the prior round. It is easy to implement, fully aggressive, and tailored for repeated‐threshold dilemmas in a multi‐agent tournament.
'''

description_AGGRESSIVE_109 = '''
Below is an “Aggressive Opportunist” strategy.  It never “builds” trust or open‐ended cooperation.  It free‐rides whenever safe and only cooperates at the bare minimum needed to secure your own payoff when doing otherwise would cost you the bonus.  In the last round it reverts to full defection.

1.  Definitions  
   •  t = current round (1…r)  
   •  A history of past rounds’ actions is public; let Coops[t–1] = number of players (excluding you) who cooperated in round t–1.  
   •  m = threshold needed to unlock the bonus k.  

2.  Decision rule for round t  

   if t = 1 or t = r:  
      play D  (no reason ever to seed cooperation on round 1 or to give a free pass in the final round)  
   else:  
      if Coops[t–1] ≥ m then  
         play D  
         (Even if you defect you still leave ≥ m cooperators—free‐ride on their effort.)  
      else if Coops[t–1] = m–1 then  
         play C  
         (If you don’t cooperate you drop group below m and forfeit k.  You must cooperate just once to secure your bonus.)  
      else  
         play D  
         (There weren’t enough cooperators last round to reach m–1; threshold is out of reach anyway.)  

3.  Pseudocode  

   initialize round t ← 1  
   loop t from 1 to r:  
     observe Coops[t–1]  (for t=1 define Coops[0]=0)  
     if t = 1 or t = r then  
       action ← D  
     else if Coops[t–1] ≥ m then  
       action ← D  
     else if Coops[t–1] = m–1 then  
       action ← C  
     else  
       action ← D  
     end if  
     play action  
   end loop  

4.  Rationale / Aggressive mindset  
   –  You never invest unless you’re exactly pivotal.  All other cooperation is a donation to rivals.  
   –  You never “forgive” past defection by others—if they cooperated en masse last round, you immediately jump in to free‐ride on their oversight.  
   –  In the very last round you defect unconditionally to maximize short‐term gain.  

This simple trigger‐style rule guarantees you only pay the cooperation cost when absolutely necessary to capture k, otherwise you relentlessly defect and exploit any cooperation in the group.
'''

description_AGGRESSIVE_110 = '''
Below is a fully “aggressive” strategy whose core is: never sacrifice your endowment and always defect.  By doing so you both free-ride on any successes your opponents may achieve and you sabotage them whenever they try to meet the cooperation threshold.

1.  Decision rules  
    •  In every round t (1 ≤ t ≤ r), play D (Defect).  
    •  Never play C (Cooperate).

2.  Handling edge cases  
    –  First round (t = 1): You have no history.  Play D.  
    –  Intermediate rounds (1 < t < r): History may show opponents sometimes cooperating, sometimes defecting.  You still play D.  By always defecting you  
       a.  Exploit any round in which opponents meet the threshold (you get 1 + k instead of k), and  
       b.  Ensure rounds in which they fall one short (m – 1 or fewer cooperators) remain failures (all get only 1).  
    –  Last round (t = r): No future to reward you for cooperation.  Play D.

3.  Why this is maximally aggressive  
    –  At no point do you incur the cost of cooperation (c_i = 1).  
    –  Whenever opponents muster m cooperators (with or without you), you defect and pocket 1 + k.  
    –  Whenever they fail (n_C < m), you still defect and get the default 1 while they get nothing from cooperation.  
    –  There is no incentive for them to try to build any “trust” with you, since you never reciprocate.  

Pseudocode  

  function AggressiveStrategy(history, t, n, m, k, r):  
      # history is list of past action‐profiles; unused because we never change  
      return “D”   # always defect  

No further bells and whistles are needed.  This strategy strictly dominates any attempt at cooperation in every round and in every possible opponent configuration.
'''

description_AGGRESSIVE_111 = '''
Below is an “aggressive” strategy—call it Aggressive Free-Rider (AFR)—that never sacrifices itself for the group and instead only plays C in the knife-edge case where it can snatch the reward without risking a failed threshold.  In practice it almost always defects, punishing any would-be cooperators.

------------------------------------------------–
Strategy name:  Aggressive Free-Rider (AFR)

Parameters (known to all):  
  n  – number of players  
  m  – cooperation threshold  
  r  – total rounds  
  k  – public good payoff

State you maintain between rounds:  
  last_coop_count  – how many players (including yourself) cooperated in the previous round  

Initialization:  
  last_coop_count ← 0   (there is no “previous” round before round 1)

Decision rule for round t = 1…r:  
  1. If t = 1:  
       — No history to go on, so defect.  
  2. Else if t = r (the final round):  
       — Always defect.  There is no future, so no reason to cooperate.  
  3. Else (1 < t < r):  
     Let c₋i = (last_coop_count – (you cooperated last round?1:0))  
       // c₋i is the number of OTHER cooperators in the previous round  
     a) If c₋i ≥ m:  
          // Others by themselves met the threshold last round  
          → Defect (D)  // free-ride on their discipline  
     b) Else if c₋i = m–1:  
          // If you alone tipped them over threshold last round, you got k+1 instead of k  
          → Defect (D)  // even more aggressive: let them fail and punish  
     c) Else:  
          // They fell short by 2 or more  
          → Defect (D)

After all players simultaneously choose, observe total cooperators this round and store in last_coop_count.

Rationale and aggressiveness:

 •  Always defects in the first round (no “trust-building”).  
 •  Never cooperates in the final round, so there is zero end-game generosity.  
 •  In intermediate rounds it never gives others the benefit of its contribution—even if by cooperating it could tip the project over m and secure k for everyone—because defection always yields 1 + k when the threshold is met by at least m players, which strictly dominates the k you’d get by cooperating.  
 •  When others barely miss the threshold (c₋i = m–1), it still defects, letting the group fail—pure punishment.  

Outcome summary:

 •  If any other coalition of size ≥ m forms, you free-ride and walk away with payoff 1 + k.  
 •  If they never form, you defect every round and get payoff 1 each round.  
 •  You never risk the 1-point endowment to help them; you simply exploit any accidental cooperation by others.

Pseudocode

  initialize last_coop_count ← 0

  for t in 1…r:
    if t == 1:
      A_t ← D
    else if t == r:
      A_t ← D
    else:
      other_coops ← last_coop_count – (A_{t–1} == C ? 1 : 0)
      if other_coops ≥ m:
        A_t ← D
      else if other_coops == m–1:
        A_t ← D
      else:
        A_t ← D

    play A_t
    observe total_coops_this_round
    last_coop_count ← total_coops_this_round

This is as aggressive as possible: you never tip, you never build trust, you punish near-miss cooperators, and you always defect in the last round.
'''

description_AGGRESSIVE_112 = '''
Below is a complete “Aggressive Free-Rider” strategy.  It never cooperates for the sake of goodwill—it only contributes in the one case when your single contribution is just enough to push the group over the threshold.  Otherwise it defects every round (and certainly in the first and last round).  Over time it also builds a simple estimate of how many others will cooperate so it knows exactly when it can safely defect.

------------------------------------------------------------------------
1.  Variables & Initialization  
   • n, r, m, k are given.  
   • t ← 1 is the current round.  
   • history_O[t–1] = list of how many “other” players cooperated in each past round.  
   • p ← 0.5 is our initial belief about the fraction of others who cooperate.  

2.  Per-round decision rule (for t = 1 … r):  
   if t == 1 or t == r then  
     Action ← D   // Always defect in the very first and very last round  
   else  
     // 2.1 Estimate expected number of other cooperators this round  
     E ← p * (n–1)  
     // 2.2 Decide:  
     if E >= m then  
       Action ← D      // At least m others will cooperate w/o you → free-ride  
     else if E < m–1 then  
       Action ← D      // Even with you, group won’t hit m → your C is wasted  
     else  
       Action ← C      // Exactly m–1 expected → your C is critical to hit threshold  
   end

3.  After observing this round’s actual play:  
   • Let o_t = number of other players who cooperated at round t.  
   • Append o_t to history_O.  
   • Update belief p = average(history_O) ÷ (n–1).  

4.  Repeat for next round (t ← t+1).  

------------------------------------------------------------------------
Why this is aggressive  
• It defects by default (never gives away its endowment unless it’s the sole pivot to unlock k).  
• It free-rides whenever safe (E ≥ m), capturing 1 + k each time cooperators meet the threshold without you.  
• It refuses to throw away its money on doomed rounds (E < m–1).  
• It only cooperates when you are the difference-maker (exactly m–1 others expected).  
• By defecting in the final round it avoids any last-move exploitation or punishment.  

Edge cases  
• First round: no history → uses default p=0.5 but nonetheless defects (no upside to an opening gift).  
• Last round: always defects (no future to deter).  
• If your estimate p drifts (history shows full defection), you’ll never mistakenly cooperate again.  

Pseudocode Summary  
```
initialize p ← 0.5, history_O ← []
for t in 1..r do
  if t == 1 or t == r:
    play D
  else:
    E ← p*(n–1)
    if      E ≥ m    then play D
    else if E < m–1  then play D
    else              play C
  end
  observe o_t = #others that cooperated
  append o_t to history_O
  p ← (sum(history_O) / length(history_O)) / (n–1)
end
```
'''

description_AGGRESSIVE_113 = '''
Below is a simple yet brutally aggressive “Saboteur‐Defector” strategy.  It never cooperates, thus (a) it always exploits any loose cooperation among the others, and (b) it always pulls the plug on any marginal coalition trying to reach m.  In tournament play it maximizes your individual payoff when others try to cooperate, and it never “gives in” even when your cooperation would raise the group reward.

1.  Strategy name  
   Saboteur‐Defector

2.  Decision rule (for every round t)  
   – Always play D (Defect).  

   In other words, you never contribute your endowment — regardless of history, whether you would be pivotal or not, first or last round, etc.

3.  Pseudocode  
   ```
   Input: parameters n, r, m, k
   For t = 1 to r do
       a_i[t] ← D
   End
   ```

4.  Edge cases  
   – First round (t=1): defect.  
   – Intermediate rounds: defect.  
   – Last round (t=r): defect.

5.  Why this is aggressive  
   • Exploitation: If the other n–1 players somehow manage to cooperate in numbers ≥ m, you still defect and pocket 1 + k while they get 0 + k or 0 + k (depending on their choice).  
   • Sabotage: If they are one short of the threshold (m–1 cooperators), you refuse to tip the balance; the community loses k, they each get only private payoffs, and you still get 1.  
   • No forgiveness, no grudges, no remorseless cooperation.  You never miss an opportunity either to wall off the bonus or to ride on others’ efforts without contributing.

This all-D policy is the ultimate aggressive play-book in the Collective Risk Dilemma.
'''

description_AGGRESSIVE_114 = '''
Below is an “Aggressive Free‐Rider” strategy.  It never cooperates out of goodwill—only to rescue the public good when, based on past play, it would otherwise fail.  Otherwise it defects every round (especially the last round), maximizing its private payoff and exploiting cooperators.

1.  State variables (from your perspective, player i):
   •  r          = total rounds  
   •  m          = cooperation threshold  
   •  coop_count[j] = number of times player j cooperated so far (j ≠ i)  
   •  t          = current round (1…r)  

2.  Initialization (before round 1):
   for all j≠i: coop_count[j] ← 0  

3.  Per‐round decision rule:
   For t from 1 to r do:
     if t = r then
       action ← D       // Last‐round free‐ride: no future punishment
     else if t = 1 then
       action ← D       // Start by testing the ground—always defect
     else
       // Estimate how many others will cooperate this round
       predicted_coops ← 0
       for each j≠i do
         p_j ← coop_count[j] / (t–1)      // Empirical cooperation rate
         predicted_coops ← predicted_coops + p_j
       end for

       if predicted_coops ≥ m then
         action ← D   // Enough others expected ⇒ defect and collect 1+k
       else
         action ← C   // Too few expected ⇒ tip the balance so group gets k
       end if
     end if

     Play(action).

     // Observe everyone’s actions this round, update counts
     for each j≠i do
       if j’s action = C then coop_count[j] ← coop_count[j] + 1
     end for
   end for

4.  Intuition / edge cases:
   • First round: no data ⇒ defect to exploit any naïve cooperators.  
   • Middle rounds: only cooperate exactly when your contribution is needed to push expected cooperators from < m to ≥ m.  Otherwise defect to maximize your payoff from the public‐good bonus.  
   • Last round: always defect (no future rounds ⇒ no threat of retaliation if you defect).  
   • Tie‐break (“predicted_coops = m–ε” vs “=m”): we use “≥m ⇒ defect.”  If it looks borderline you defect and gamble that you’re not needed.  

This meets all requirements:
–  Decision rules fully specified (including first and last rounds).  
–  Edge cases handled by explicit “if t=1” and “if t=r.”  
–  Aggressive: you never cooperate unless strictly forced to rescue the bonus, and you always defect once you judge it safe.
'''

description_AGGRESSIVE_115 = '''
Below is a fully specified, “aggressive” threshold‐public‐goods strategy.  It never seeks mutual long‐run cooperation; it free‐rides whenever it can, and only chips in when doing so is the sole way to grab the bonus for itself.  It defects in the last round to avoid giving others any incentive, and it begins play by defecting to probe the field.

Name: Opportunistic Free‐Rider (OFR)

Parameters known to all:
  n, r, m, k

State variables (at round t):
  C_prev = number of players (other than you) who played C in round t–1  
    (on round 1 we set C_prev = 0 by convention)

Decision rule for round t = 1,2,…,r:

  if t == 1:
    action := D
      // probe baseline: start by defecting

  else if t == r:
    action := D
      // last round: always defect

  else  // 2 ≤ t ≤ r–1
    if C_prev ≥ m then
      // the other players met the threshold without your help last round—
      // free-ride again and grab the bonus for yourself
      action := D

    else if C_prev == m–1 then
      // you are pivotal: by cooperating, you push them over the
      // threshold and get π = 0 + k > 1 + 0
      action := C

    else
      // even if you cooperate, they still won’t reach threshold;
      // no point in paying cost for no bonus
      action := D

After choosing action, observe all players’ moves; update
  C_prev := count of cooperators among the other n–1 players for use in the next round.

Rationale and aggressive elements:

1.  Free-riding whenever possible  
    – If others already reached m, you defect, pocket k + 1 rather than giving away your 1.  

2.  Only “rescue” the threshold when strictly profitable  
    – If exactly m–1 cooperators among opponents, a single C from you yields π = k, which exceeds the π = 1 you’d get by D.  
    – In all other shortfalls you defect (no wasted contributions).

3.  No carrot for cooperation, only stick for self-interest  
    – First round defect to signal you’re not a team player.  
    – Last round defect to deny any end-game spoils or future reciprocity.

4.  Memory-1 simplicity  
    – You only track C_prev – the last round’s cooperation count among others.  
    – This is enough to implement your free-riding/opportunistic pivot.

Pseudocode

  initialize C_prev := 0

  for t in 1..r do
    if t == 1 or t == r then
      play D
    else
      if C_prev ≥ m then
        play D
      else if C_prev == m–1 then
        play C
      else
        play D
    end

    observe all players’ actions in round t
    compute C_prev := (# of C among other n–1 players)
  end

This strategy aggressively maximizes your payoff each round, never trusting in mutual cooperation beyond what you can exploit, and it fully exploits any opportunity to slip into the winning coalition at minimal cost.
'''

description_AGGRESSIVE_116 = '''
Below is a self-contained “Aggressive Greedy-Exploit” strategy that (a) never hesitates to defect when you can, (b) only cooperate when absolutely necessary to secure the public-good payoff for yourself, and (c) punishes any player who “fleeces” you after you help them.

───  
1. State variables and bookkeeping  
   • r  = total number of rounds   
   • t  = current round (1…r)   
   • m  = cooperation threshold  
   • n  = total players  
   • history[t′][i] ∈ {C,D} = action of player i in round t′  
   • exploited_by = a set of player‐indices whom you have “caught” free‐riding on your cooperation  

2. High-level idea  
   – Myopic best response each round:  
       • If others will reach m without me, I defect (get 1 + k).  
       • If they fall short of m by exactly 1, I cooperate (get 0 + k > 1).  
       • Otherwise I defect (get 1).  
   – Never cooperate in round 1 (no info) or round r (no future leverage).  
   – If I cooperate and still end up with strictly less than some defectors (i.e. I’m exploited), I remember who exploited me and thereafter defect whenever they cooperate, in order to punish them.  

3. Pseudocode  

Initiate:  
 exploited_by ← ∅  

For each round t = 1…r do:  
 Observe prior history if t > 1:  
  Let coop_count_prev = |{ j ≠ me : history[t–1][j] = C }|  
  Let I_cooperated_prev = (history[t–1][me] = C)  

 // 1) Punishment bookkeeping  
 if t > 1 AND I_cooperated_prev = true then  
  // check if any defectors last round still got the reward  
  // i.e. coop_count_prev + 1 ≥ m but some j defected  
  if coop_count_prev + 1 ≥ m then  
   for each j ≠ me with history[t–1][j] = D do  
    exploited_by ← exploited_by ∪ {j}  
   end for  
  end if  
 end if  

 // 2) Endgame: never cooperate in last round  
 if t = r then  
  action ← D  
  goto PLAY  
 end if  

 // 3) First round: blind defection  
 if t = 1 then  
  action ← D  
  goto PLAY  
 end if  

 // 4) Punish known exploiters immediately  
 // If any exploiter is planning to cooperate, undercut them by defecting  
 predict_coopers ← { j ≠ me : in many past rounds j played C more often than D }  
 if (exploded ← exploited_by ∩ predict_coopers) ≠ ∅ then  
  action ← D  
  goto PLAY  
 end if  

 // 5) Myopic best‐response to previous round’s coop count  
 if coop_count_prev ≥ m then  
  // Others already met the threshold → free‐ride  
  action ← D  

 else if coop_count_prev = m – 1 then  
  // I am pivotal → cooperate to get k  
  action ← C  

 else  
  // Even with my help, threshold fails → better to defect  
  action ← D  
 end if  

PLAY:  
 Submit action (C or D).  
 Record history[t][me] ← action.  

End for  

───  
Explanation of key points  
1. First‐round defection “probes” for aggressiveness—never give away your endowment blind.  
2. Last round is pure defection (no threat of future retaliation).  
3. You only cooperate when you are pivotal (others = m–1).  Otherwise you defect and free-ride whenever possible.  
4. You track who “fleeces” you—if you cooperated and still lost payoff to defectors, you mark them as exploiters and thereafter defect whenever they try to cooperate, to punish them and reduce their future payoffs.  

This scheme is aggressive because it (a) maximizes your one‐shot gain whenever you can, (b) only concedes to cooperation on purely self‐interested grounds, and (c) carries a harsh punishment for anyone who tries to live off your altruism.
'''

description_AGGRESSIVE_117 = '''
Here is a “bully‐freerider” strategy that is (1) aggressive—never cooperates unless absolutely necessary to trigger the group‐reward—and (2) clear about first/last rounds and edge cases.  You only ever cooperate when, without you, the group just misses the threshold by one; otherwise you always defect and freeride.

Definitions:  
 Let t = current round (1 ≤ t ≤ r).  
 Let coopOthers(t–1) = number of _other_ players who cooperated in round t–1.  

Decision Rule for round t:  
1. If t = 1 or t = r, play D (defect).  
2. Else (2 ≤ t ≤ r–1):  
 a. If coopOthers(t–1) ≥ m, play D.  
  – Rationale: The group would have succeeded anyway; freeride on their effort.  
 b. Else if coopOthers(t–1) = m–1, play C.  
  – Rationale: You are pivotal; by cooperating you turn failure into success and collect k.  
 c. Else (coopOthers(t–1) < m–1), play D.  
  – Rationale: Even if you cooperated, they’d still fail, so you save your endowment.  

Pseudocode  
----------  
Inputs: n, r, m, k  
State variable: lastCooperators (initialize to 0)  

for t in 1…r:  
    if t == 1 or t == r:  
        action[t] = D  
    else:  
        if lastCooperators ≥ m:  
            action[t] = D  
        else if lastCooperators == m–1:  
            action[t] = C  
        else:  
            action[t] = D  
    observe opponents’ actions, count how many chose C → lastCooperators  

End for  

Why this is aggressive:  
• You never “waste” a contribution unless you alone can flip a loss into a k‐bonus.  
• You always defect on the first round to probe and on the last round to milk the one‐shot gain.  
• You punish any residual cooperation by refusing to add yours once the threshold is already met.  

Edge Cases covered:  
– First round: no history ⇒ defect.  
– Last round: defect (no future punishment possible).  
– Exactly m–1 cooperators last time ⇒ you cooperate once and only once per “near miss.”  
– All other histories ⇒ defect.
'''

description_AGGRESSIVE_118 = '''
Below is a concise “always-defect” style strategy—call it Aggressive Permanent Defection (APD).  It never cooperates, thus maximizes your own round payoff (you pay no contribution) and always frustrates any attempt by others to reach m.

1. Decision Rules  
   For each round t = 1…r, regardless of history or the round number, play D (“Defect”).

2. Edge Cases  
   • First round: D  
   • Intermediate rounds: D  
   • Last round: D  

3. Rationale (Aggressive Mindset)  
   – Contributing (C) costs you 1 unit every time and can only ever increase others’ payoffs.  
   – By always defecting you (a) never pay the contribution, (b) deny cooperators the chance to build a safe threshold when your vote could make or break it, and (c) when m or more others do cooperate, you still collect the full (1 + k) payoff as a free-rider.  
   – There is no credible threat or reward you can offer by cooperating, because cooperation always yields you strictly less than defection in every possible scenario.

4. Pseudocode  

```
function choose_action(round t, history H):
    # Aggressive Permanent Defection
    return D
```

That’s it.  Across all r rounds you never contribute—maximizing your own payoff each round and aggressively undermining any collective success.
'''

description_AGGRESSIVE_119 = '''
Below is an “aggressive” repeated‐play strategy for the Collective Risk Dilemma.  It (1) defects by default, (2) only reluctantly “helps” when by doing so it can just push the group over the cooperation‐threshold and (3) otherwise defects—both to maximize own payoff and to punish other cooperators by ensuring that when they build momentum you break it.

––––––––––––––––––––––––––––––––––––––––––  
Strategy name: “Threshold Sniper with Punishment”  
––––––––––––––––––––––––––––––––––––––––––––––  

State variables (persisted over rounds)  
  History[t]: record of how many players (including you) chose C in round t  
  PunishCounter: how many future rounds you must defect as punishment (initially 0)  

Parameters you know (common knowledge)  
  n, r, m, k  

High‐level rules  
1.  By default defect every round, except in the very narrow case that your single cooperation will turn a failed threshold into a successful one.  
2.  Whenever you cooperated and got punished (i.e. threshold was met by others but you cooperated and got less than the defectors), you “punish” the group by defecting unconditionally for K subsequent rounds.  
3.  Always defect in round 1 and the final round r.  (No incentive to cooperate first or last—standard end‐game defection.)  

––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  
––––––––––––––––––––––––––––––––––––––––––––––  
Initialize  
  PunishCounter ← 0  

For each round t = 1…r do:  
  If PunishCounter > 0 then  
    action_t ← D  
    PunishCounter ← PunishCounter – 1  
    record action_t and continue to next t  
  EndIf  

  If t == 1 or t == r then  
    action_t ← D  
    record action_t and continue to next t  
  EndIf  

  Let othersCoop ← number of C’s in round t–1 among the other n–1 players  
     (if t–1 = 0 or unknown, treat as othersCoop = 0)  

  // CASE A: Without you, threshold already met → free‐ride  
  If othersCoop ≥ m then  
    action_t ← D  

  // CASE B: You are the swing vote (othersCoop = m–1)  
  Else if othersCoop == m–1 then  
    // If you cooperate, threshold succeeds: you get k  
    // If you defect, threshold fails: you get 1  
    // Since k > 1, you cooperate just this round  
    action_t ← C  

  // CASE C: OthersCoop < m–1 → even your cooperation won’t reach threshold  
  Else  
    action_t ← D  
  EndIf  

  record action_t  

  // After seeing payoffs in round t, update punishment if needed  
  // You can observe that: if you played C, threshold was met, but defectors got 1+k > your k  
  If you played C in round t AND total cooperators in round t ≥ m then  
    // You were “exploited” in this cooperative round – punish them  
    PunishCounter ← P  
      // P is a small constant punishment length, e.g. 2 or 3 rounds  
  EndIf  
EndFor  

––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of the “aggressive” components  
1. Default defection: You never grant free cooperative benefits unless you alone can tip the balance.  
2. Swing‐vote cooperation only: You briefly cooperate only to secure the group reward when it otherwise would fail—and then immediately return to defection.  
3. Punishment: If you suffered by cooperating (i.e. some defectors pocketed a higher payoff), you retaliate by defecting unconditionally for P rounds, disrupting any cooperative momentum.  
4. First‐ and last‐round defection: Classic end‐game logic—no reason to ever cooperate when you cannot punish or be punished in future.  

By combining these rules you ensure maximum personal payoff (“always defect unless you can briefly push the group over the line”) while also discouraging sustained cooperation by punishing others whenever they attempt to carry the project on your back.
'''

description_AGGRESSIVE_120 = '''
Below is an “aggressive” threshold‐exploiter strategy for the repeated Collective Risk Dilemma.  In a nutshell, you never help more than absolutely necessary to trigger the public good, you never help when it isn’t strictly pivotal, you punish any “over‐enthusiastic” cooperation by breaking threshold, and you defect in the final round.

——————————————————————
1. Key idea
   • Only cooperate when you are exactly the m-th cooperator – i.e. when exactly m–1 others have just signaled cooperation.  
   • Otherwise defect.  
   • In particular, if in the previous round the group already met the threshold (≥m cooperators), you defect to break it and punish them.  
   • Always defect in round 1 (to probe) and in the last round (no future to exploit).

2. Notation
   t            = current round, 1 ≤ t ≤ r  
   r            = total number of rounds  
   m            = cooperation threshold  
   History[t–1] = record of how many players (other than you) cooperated in round t–1  
   A_i,t        = your action in round t: C or D  

3. Decision rule (pseudocode)
   For t from 1 to r do:
     if t == 1 then
       A_i,t ← D   
         (First‐round probe: defect to see others’ baseline.)
     else if t == r then
       A_i,t ← D   
         (Last round: no future, so always defect.)
     else
       let L ← number of other players who chose C in round t–1
       if L == m–1 then
         A_i,t ← C   
           (You’re pivotal: you flip threshold so everyone (including you) gets k.)
       else
         A_i,t ← D   
           (Otherwise, you free-ride or sabotage.)
     end if
   end for

4. Explanation of aggressiveness
   • “Minimal cooperation” means you pay the cost only when strictly profitable (k > 1 ⇒ cooperating when pivotal yields k rather than 1).  
   • Whenever the group thermometers in round t–1 read ≥ m cooperators, you defect and force failure or reduce total payoff – punishing over‐cooperators.  
   • You refuse to cooperate in the very first round (never signal goodwill) and in the final round (no incentive to build reputation).  
   • By never over‐cooperating and by actively breaking thresholds, you maximize your own payoff while keeping others off‐balance.

5. Handling corner cases
   – If in some round t–1 fewer than m–1 cooperated, then even your help couldn’t reach m ⇒ you defect to avoid a sunk cost.  
   – If ever History[t–1] > m (more than m cooperated), you still defect – you don’t top up an already‐successful coalition.  
   – Works for any n, m (1 < m < n), any k > 1, any r > 1.

This strategy guarantees you only pay cost 1 when it turns 1 → k for your own benefit, never helps more than necessary, and actively undermines any excess cooperation.
'''

description_AGGRESSIVE_121 = '''
Below is an “aggressive pivotal-free-rider” strategy.  In essence it never gives up a free ride once it expects the public good will go through, and only contributes when it is almost certain to be the pivotal contributor (so as to secure the payoff rather than let the whole group fail).  We assume k>1 so that even a lone pivotal cooperator (getting payoff k) is better for you than the baseline of 1 you’d get from defection when the project fails.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

1.  DATA STRUCTURES AND INITIALIZATION  
   Let  
     history_other_C[t]  =  number of other players who cooperated in round t  
     T = total rounds = r  
     n = total players  
     m = threshold  
     k = reward factor (>1)  
   Initialize for all t: history_other_C[t] = 0.

2.  ROUND-BY-ROUND DECISION RULE  

 For each round t from 1 to T do:  
   if t == 1 or t == T then  
     action ← D                     # First and last round: always defect  
   else  
     # 2.a Estimate others’ cooperation probability α   
     sumC = Σ (history_other_C[τ]) over τ=1..t–1  
     α = sumC / ((n–1)*(t–1))        # fraction of “other” cooperations so far  

     # 2.b Compute proxies for success probabilities  
     #    P_success_wo_me = Prob[#others ≥ m ] under Binomial(n–1, α)  
     #    P_success_if_I_coop = Prob[#others ≥ m–1]  
     P_success_wo_me       = Σ_{i=m to n–1}  Comb(n–1,i) α^i (1–α)^(n–1–i)  
     P_success_if_I_coop   = Σ_{i=m–1 to n–1} Comb(n–1,i) α^i (1–α)^(n–1–i)  

     # 2.c Compare to thresholds  
     # We choose a high confidence threshold δ (e.g. 0.9).  
     if P_success_wo_me ≥ δ then  
       action ← D                   # I expect enough cooperators without me → free-ride  
     else if P_success_if_I_coop ≥ δ then  
       action ← C                   # I am almost surely pivotal → secure the project  
     else  
       action ← D                   # Otherwise, I defect and wait for more info  
   end if

   # 2.d Observe others’ moves this round and record  
   history_other_C[t] = number of other players who chose C in round t  

 end for

3.  EDGE-CASE HANDLING  
 • First round (t=1): defect to start “testing” the baseline rate of cooperation without giving anything away.  
 • Last round (t=T): defect, since there is no future punishment or reward to be had.  
 • Penultimate rounds (t=T–1): our same rule applies—if the group would reach m cooperators without us, we defect; if only with us they reach m, we cooperate; otherwise we defect.  

4.  AGGRESSIVE MINDSET RATIONALE  
– We never cooperate just to “be nice.”  We only contribute when we can (nearly) guarantee we will be the one tipping the group above the threshold, because that is the only time cooperation increases *our* payoff above the default of 1.  
– Whenever we believe (with high confidence δ) that enough others will cooperate, we defect and capture the full 1 + k payoff.  
– We punish over-eager cooperators by defecting whenever it is safe, thus training the population to either (a) leave the threshold to us or (b) risk failure whenever they over-cooperate.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Pseudocode Summary:

function decide(t, history_other_C):  
  if t == 1 or t == T:  
   return D  
  α = sum(history_other_C[1..t–1]) / ((n–1)*(t–1))  
  compute P_success_wo_me and P_success_if_I_coop as above  
  if P_success_wo_me ≥ δ:  
   return D  
  else if P_success_if_I_coop ≥ δ:  
   return C  
  else:  
   return D  

After each round, update history_other_C[t] with the observed count of other players’ C.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
'''

description_AGGRESSIVE_122 = '''
Below is an “aggressive pivot” strategy that (1) defects by default to punish cooperators, (2) only ever cooperates when doing so lets you uniquely “pivotal-cooperate” to trigger the public good and grab its payoff, and (3) uses only one–round memory (most opponents will be using similar heuristics).

1.  State Variables  
    – r: total number of rounds  
    – m: threshold of cooperators needed  
    – t: current round index (1…r)  
    – history[t−1] = number of opponents who chose C in round t−1 (for t=1 we have no history)  

2.  Key Idea  
    – If you expect exactly m−1 opponents to Cooperate this round, you play C (you become the mth cooperator, get payoff k > 1).  
    – In all other situations you Defect—both to free-ride when there are already ≥m cooperators and to ensure failure (and punish) when there are <m−1.  

3.  Decision Rule (per round t)  
    let H = history[t−1]  (opponent-C count in last round)  
    // If t=1, define H = 0 (most aggressive)  
      
    Predict that exactly H opponents will play C this round.  
      
    if H == m−1 then  
      play C   // you become the pivot cooperator and guarantee the +k reward  
    else  
      play D   // otherwise always defect  

4.  Pseudocode  

    initialize history[0] = 0  
    for t in 1…r do  
      H ← history[t−1]  
      if H == m−1 then  
        action[t] ← C  
      else  
        action[t] ← D  
      end  
      wait for all opponents’ actions  
      observe coop_count = number of opponents who played C this round  
      history[t] ← coop_count  
    end  

5.  Edge Cases  
  • First round (t=1): we set H=0 ⇒ H≠m−1 ⇒ we Defect.  
  • Last round (t=r): same rule applies. If last round’s cooperators = m−1 you cooperate to net k; otherwise defect.  
  • If opponents occasionally overshoot (H ≥ m), we continue to defect and free-ride (you get 1+k, they get k or less).  
  • If opponents under-shoot (H < m−1), we defect to ensure failure (punishing cooperators by denying them k).  

6.  Why “Aggressive”?  
  – You never cooperate just for the social good.  
  – You punish attempts at cooperation by defecting whenever you can (forcing a failure yields 1 for you instead of 0).  
  – You only cooperate when it is strictly payoff-maximizing and pivotal (H=m−1).  

This one–round–memory pivot strategy both punishes cooperation and exploits any narrowly insufficient cooperation among opponents.
'''

description_AGGRESSIVE_123 = '''
Below is an “aggressive‐exploiter” strategy.  It never seeks to build a safe cooperative equilibrium; instead it only ever cooperates when its single contribution is guaranteed to tip the project into success (so that its net payoff by cooperating, k, exceeds the defection payoff of 1), and otherwise defects to exploit or punish.

1.  Notation  
 – t: current round (1 ≤ t ≤ r)  
 – coop_prev: number of cooperators observed in round t–1 (not counting you)  
 – m: threshold  
 – k: bonus (>1)  

2.  High-level description  
 • Round 1: defect (no history, so we avoid the risk of “wasting” a contribution).  
 • Rounds 2…r–1:  
  – If coop_prev == m–1, cooperate (your single C will push total to m ⇒ you earn k > 1).  
  – Otherwise, defect.  
 • Round r (last round): defect (one‐shot logic—no future to leverage).  

3.  Why it’s aggressive  
 – It never “pays it forward” or seeks mutual cooperation.  
 – It exploits any group that already reached the threshold by defecting (you get 1 + k vs. their k).  
 – It only occasionally contributes—in exactly those cases where it’s payoff‐maximizing to do so—and otherwise defects to punish or free-ride.  

4.  Pseudocode  

```
Input: r, m, k  
coop_prev ← 0        # no cooperators before round 1

for t in 1…r do
  if t == 1 or t == r then
    action ← D       # defect in first and last rounds
  else
    if coop_prev == m - 1 then
      action ← C     # tip the scale and earn k > 1
    else
      action ← D     # otherwise defect
    end if
  end if

  play(action)
  observe others’ actions
  coop_prev ← number of others who played C this round
end for
```

5.  Edge-case handling  
 – If m= n (so you alone can tip only when all others cooperated), you will still cooperate when coop_prev == n-1.  
 – If previous round had coop_prev ≥ m, you defect (you’d earn 1+k vs. k).  
 – If coop_prev ≤ m-2, even with your C the project fails → you defect to secure the 1.  

This recipe maximizes your individual payoff against any pattern of opponents, never entrusting in “nice” reciprocation beyond the minimal, guaranteed bonus.
'''

description_AGGRESSIVE_124 = '''
Below is an “aggressive exploiter” strategy.  It never extends gratuitous cooperation, it only contributes when you are the pivotal m-th cooperator (so that you capture the k reward rather than let it slip by), and otherwise defects to maximize your private payoff.

1.  Definitions and notation  
   •  t = round index, t=1,…,r  
   •  history[t–1] = the profile of all n players’ actions in the previous round (for t=1 this is empty)  
   •  coop_others = number of cooperators in history[t–1] excluding you  

2.  High-level idea  
   –  You defect in every round except the rare case where exactly m–1 others cooperated last round.  
   –  In that borderline case, by switching to C you push the group to m cooperators and collect π = k, which is better than the π =1 you’d get by defecting.  
   –  You never “reward” erstwhile defectors, you never “invite” cooperation, and you never risk a costly C when it won’t pay.

3.  Strategy pseudocode

   Initialize: history ← empty  
   For t = 1 to r do  
     if t = 1 then  
       action[t] ← D                      # no information yet → defect  
     else  
       coop_others ← count of C in history[t–1] excluding your own past move  
       if coop_others = m–1 then  
         action[t] ← C                  # you are pivotal → push over the threshold  
       else  
         action[t] ← D                  # either threshold already guaranteed or hopeless → defect  
       end if  
     end if  
     Play action[t] and record it in history[t]  
   end for

4.  Edge-case handling  
   –  First round: with no prior signal, assume nobody cooperates → defect.  
   –  Any round t>1: if exactly m–1 others cooperated last time, cooperate; otherwise defect.  
   –  Last round: same rule applies, since even with no future you compare payoffs 1 vs. k when you are pivotal.  

5.  Why it’s aggressive  
   –  You refuse to subsidize a community project unless it strictly increases your own immediate payoff.  
   –  You never “build goodwill” for future rounds; you treat every C as a cost unless it is essential to claim the k reward yourself.  
   –  You exploit any residual cooperators by defecting whenever they would carry the threshold without you (getting 1+k).  

Results:  
   •  If the other players never manage to coordinate m–1 cooperators in your preceding round, you defect r times and earn π_total = r·1.  
   •  If they do hit m–1 cooperators often enough, you step in at each such round to earn π = k, otherwise still defect for π =1.  
   •  You maximize your own payoff via pure exploitation and minimal costly cooperation.
'''

description_AGGRESSIVE_125 = '''
Below is an “Aggressive Opportunist” strategy that (i) defects by default, (ii) only cooperates when it can force or preserve the threshold and thus cash in on k, and (iii) never cooperates gratuitously.  It uses only memory‐1 (counts of last round’s cooperators) plus two simple edge‐case rules.

1. Definitions and state  
   – m: cooperation threshold  
   – r: total rounds  
   – t: current round (1…r)  
   – sₜ₋₁: number of players (including you) who cooperated in round t–1  
   – failStreak: count of consecutive past rounds in which s < m (initial 0)  

2. High‐level description  
   – Default: Defect.  
   – Only cooperate if by doing so you (a) preserve a currently met threshold (sₜ₋₁ = m) or (b) push a near-miss into a meet (sₜ₋₁ = m–1).  
   – Never risk cooperating if it can’t swing or hold the payoff.  
   – If threshold has failed two rounds in a row, assume “no-hope” and defect forever (grim trigger).  
   – Always defect in round 1 (no history) and in the last round (no future leverage).

3. Pseudocode  

  initialize failStreak ← 0

  for t in 1…r:
    if t = 1:
      play D            # no information yet
      observe s₁
      if s₁ < m:
        failStreak ← failStreak + 1
      else:
        failStreak ← 0
      continue

    if t = r:
      play D            # final round: no future punishment/incentive
      break

    # if we’ve seen 2 straight misses, go pure defect
    if failStreak ≥ 2:
      play D
      if sₜ < m:
        failStreak ← failStreak + 1
      else:
        failStreak ← 0
      continue

    # otherwise inspect last round’s sₜ₋₁
    let s ← sₜ₋₁   # number of cooperators observed last round

    if s ≥ m+1:
      # threshold would survive even if we defect (s–1 ≥ m)
      play D
    else if s = m:
      # threshold met exactly—defecting would break it → cooperate
      play C
    else if s = m–1:
      # near‐miss—by cooperating we can tip into meeting the threshold
      play C
    else
      # s < m–1: too far below threshold; no point in helping
      play D

    # update failStreak based on actual outcome of this round
    observe sₜ
    if sₜ < m:
      failStreak ← failStreak + 1
    else:
      failStreak ← 0

4. Rationale  
  • Aggressive default to defection maximizes private payoff (1 vs. 0 cost) and punishes cooperators.  
  • Only grudgingly “gives” cooperation when it can either (a) keep the public good alive so you still collect +k or (b) convert a one‐unit shortfall into a windfall +k.  
  • The two‐round grim‐trigger (“failStreak ≥ 2”) ensures you won’t be suckered by perpetually failing cooperators.  
  • Always defect in the first and last rounds removes any first‐move uncertainty or end-game disadvantage.  

This memory-1 rule set is aggressive—defection is the baseline, cooperation is only instrumental—and handles all edge cases with a few simple counters.
'''

description_AGGRESSIVE_126 = '''
Below is a fully “aggressive” strategy – one that never gives up its private gain, always defects, and actively punishes any drift toward collective success.

1. Philosophy  
   - Defection (D) strictly dominates cooperation (C) in each round.  
   - We exploit the fact that a defector always earns exactly one unit more than a cooperator, whether the threshold is met or missed.  
   - We never allow the group to stabilize above the cooperation‐threshold.  By consistently defecting we punish any cooperators and keep the threshold unmet (except when others alone can force it, in which case we still defect to grab the extra +k).

2. Decision Rule  
   For each round t = 1…r do:
     • Action ← D  (Defect), unconditionally.

3. Edge Cases  
   – First round (t=1): Defect.  
   – Middle rounds (1 < t < r): Defect.  
   – Last round (t=r): Defect.

4. Pseudocode  
   ```
   function pick_action(round t, history):
       return D
   ```

   (No history lookup is needed, since we never cooperate or “forgive.”)

5. Why it’s aggressive  
   – It never cedes the private “1‐unit” payoff.  
   – It never contributes to the public good or allows the threshold to be met through its own cooperation.  
   – By refusing to cooperate even when others come close to a successful threshold, it punishes all cooperators by keeping them from accessing the +k bonus unless they can force it without us (in which case we still grab the extra +k advantage).  

This is as aggressive as it gets: unconditional, perpetual defection, horizon‐proof (no endgame “nice” move), and always ready to sabotage any attempt at collective success.
'''

description_AGGRESSIVE_127 = '''
Below is a fully‐specified “aggressive” strategy for the repeated Collective Risk Dilemma.  It never “gives” cooperation for its own sake, it only ever contributes when by doing so it flips an otherwise‐failed round into a successful one—and even then only when that extra payoff (k–1) outweighs the guaranteed 1 unit you would get by free‐riding.  In all other circumstances it defects.  Over time it builds simple frequency estimates of each opponent’s cooperations to decide whether it “needs” to step in.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Data structures (per opponent j):  
   • count_j = number of times j has cooperated so far  
   • t = current round number (starts at 1)  
   • n, r, m, k (game parameters as given)

2. Helper: estimate others’ total cooperation  
   Let p_j = count_j / (t–1)   if t>1, else p_j = 0  
   predicted_cooperators = Σ_{j≠i} p_j

3. Decision rule (each round t = 1…r):  
   Step 3.1 (estimate)  
     If t = 1, we have no history ⇒ treat predicted_cooperators = 0  
     Else compute p_j and sum as above.  

   Step 3.2 (compare to thresholds)  
     Case A: predicted_cooperators ≥ m  
       ⇒ Enough others likely to cooperate; we free‐ride ⇒ play D  
     Case B: predicted_cooperators ≤ m–2  
       ⇒ Too few others; even if we join we cannot reach m ⇒ play D  
     Case C: predicted_cooperators ∈ [m–1, m)  
       ⇒ There is a chance that exactly m–1 others will cooperate  
          • If by cooperating we can flip failure ⇒ success, our payoff  
            cooperating = 0 + k = k; defecting = 1 (and failure ⇒ 1)  
          • Since k>1, cooperating gains us k–1 > 0 more than defecting  
          ⇒ play C  

   Step 3.3 (tie‐break)  
     Note that “predicted_cooperators = m” falls in Case A (we defect)  
     “predicted_cooperators = m–1” is Case C ⇒ we cooperate.

4. Update after observing everyone’s moves this round:  
   For each opponent j:  
     If j played C this round, count_j ← count_j + 1  
   t ← t + 1  

5. Edge cases:  
   • First round (t=1): no history ⇒ predicted_cooperators=0 ⇒ we defect.  
   • Last round is treated exactly the same (no backward induction “unraveling”).  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  

  initialize count_j ← 0 for all opponents j  
  t ← 1  

  for t in 1..r do  
    if t = 1 then  
      predicted ← 0  
    else  
      predicted ← 0  
      for each j ≠ i do  
        p_j ← count_j / (t–1)  
        predicted ← predicted + p_j  
    end  

    if predicted ≥ m then  
      action ← D  
    else if predicted ≤ m–2 then  
      action ← D  
    else   # predicted ∈ [m–1, m)  
      action ← C  
    end  

    play(action)  

    observe opponents’ actions  
    for each j ≠ i do  
      if j’s action == C then  
        count_j ← count_j + 1  
      end  
    end  

    t ← t + 1  
  end  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Why this is aggressive  
1.  It never cooperates just to “be nice.”  
2.  It only contributes when doing so strictly raises its own one‐round payoff (i.e. flips a failure into success and k>1).  
3.  It always defects if it believes enough others will carry the load or if it can’t possibly get to m even by contributing.  
4.  No complicated forgiveness or reward phases—purely maximizing self‐interest every round.
'''

description_AGGRESSIVE_128 = '''
Below is an “aggressive‐extortion” strategy for the repeated Collective Risk Dilemma.  The idea is:  
  • Virtually always defect—except when you must make the pivotal contribution to hit the public‐good threshold.  
  • When you do cooperate, you do so only if exactly m–1 others are expected to cooperate.  
  • If you ever “throw in” your contribution but still fail to reach the threshold (because some free‐rider pulled out), you punish the entire group by defecting for the remainder of the tournament.  

1.  State variables  
    • m, n, r as given.  
    • RevengeCounter ← 0  (counts punitive‐defection rounds remaining)  
    • History of all players’ actions kept by round.  

2.  Decision rule for round t = 1…r  

    if t = 1 or t = r then  
      action ← D     // Defect on the very first and very last round  
      goto record_and_update  

    if RevengeCounter > 0 then  
      action ← D     // Punishing phase  
      RevengeCounter ← RevengeCounter – 1  
      goto record_and_update  

    // Predict how many others will cooperate this round  
    Let coop_last ← number of cooperators among the other n–1 players in round t–1  
      (for t=2 this is simply 0, since you defected in round 1)  

    if coop_last ≥ m then  
      // Group can reach threshold without you  
      action ← D     // Free‐ride on their cooperation  
    else if coop_last = m–1 then  
      // You are pivotal: your single cooperation will push them over the threshold  
      action ← C  
    else  
      // Even with your cooperation, threshold < m  
      action ← D  

  record_and_update:  
    Commit to action (C or D).  Observe actual num_coops ← total cooperators this round, including you.  
    if (you played C) AND (num_coops < m) then  
      // You tried to secure the project but some defectors let it fail  
      // Enter permanent punishment  
      RevengeCounter ← r – t        // defect all remaining rounds  
    end if  

3.  Explanation of “aggressive” features  
  • You only cooperate when you can’t exploit the group—i.e. when exactly m–1 others are on board and your single C is required.  
  • You maximize free‐rides whenever possible (coop_last ≥ m).  
  • You never “waste” a contribution if it cannot secure the payoff (coop_last < m–1).  
  • You punish the entire group for failing you after you make your sacrifice, by defecting for the rest of the tournament (grim trigger).  
  • You defect on the first round (to establish your toughness) and on the last round (no future leverage).  

4.  Pseudocode  

    initialize RevengeCounter ← 0  
    for t in 1…r do  
      if t = 1 or t = r then  
        a_t ← D  
      else if RevengeCounter > 0 then  
        a_t ← D  
        RevengeCounter ← RevengeCounter – 1  
      else  
        coop_last ← #cooperators among others in round t–1  
        if coop_last ≥ m then  
          a_t ← D  
        else if coop_last = m–1 then  
          a_t ← C  
        else  
          a_t ← D  
        end if  
      end if  

      // Play a_t, observe num_coops ← total cooperators this round  
      if a_t = C and num_coops < m then  
        RevengeCounter ← r – t  
      end if  
    end for  

This strategy is maximally exploitative—only contributing when strictly necessary to unlock the public‐good payoff, then free‐riding whenever possible, and punishing any failure after you’ve done your part by withdrawing cooperation forevermore.
'''
