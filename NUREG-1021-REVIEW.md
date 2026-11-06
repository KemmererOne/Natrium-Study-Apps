# NUREG-1021 review of quiz and flashcard format

Source: NUREG-1021, Rev. 12, Operator Licensing Examination Standards for Power Reactors (ML21256A276.pdf, Sep 2021). Page numbers are ES-4.2 page N of 29. IDs: Q = position in quiz/questions.js, C = position in flashcards/cards.js, counted from 1.

## Rules checked

| Rule | Section | Quote | Finding | Result |
|---|---|---|---|---|
| D1 | ES-4.2 D.1, p. 10 | "Use four answer options." | All 378 have 4 options and one key | Pass |
| D1 | ES-4.2 D.1, p. 10 | "Do not use test items with multiple correct answers from which examinees must select the "most correct" answer" | Q250, Q271, Q302, Q332 say "best"/"most likely" but have one correct option | Pass |
| D3 | ES-4.2 D.3, p. 11 | "Do not use "all of the above" or "none of the above."" | None found (also checked "both", "neither", "all of these") | Pass |
| D4 | ES-4.2 D.4, p. 11 | "Do not present a collection of true/false (T/F) statements as a multiple-choice item." | Q295, Q312 | Proposed |
| D5 | ES-4.2 D.5, p. 11 | "Define the question, task, or problem in the stem of the question." | All stems end in a question or a lead-in colon | Pass |
| D6 | ES-4.2 D.6, p. 12 | "Include as much necessary information as possible about the problem or situation in the stem, leaving only the solution, action, or effect for the answer options." | Q14, Q45 fixed; Q122 proposed | Fixed / proposed |
| D7 | ES-4.2 D.7, p. 12 | "If a negative stem is necessary, highlight the negative word (e.g., not, never, least)." | 5 stems, 5 card fronts | Fixed |
| D7 | ES-4.2 D.7, p. 13 | "never use a negatively stated stem with a negatively stated answer option" | Q55, Q248 | Proposed |
| D10 | ES-4.2 D.10, p. 14 | "Make all answer options homogeneous. Ensure there is only one correct answer and that the distractors are highly plausible." | Q31 (one option in different units) | Proposed |
| D11 | ES-4.2 D.11, p. 15 | "If the answer options have a logical or a timeline sequence, put them in order" | 14 reordered; 21 marked seq so the app keeps the order | Fixed |
| D12 | ES-4.2 D.12, p. 15 | "Avoid overlapping answer options" | No overlapping ranges found | Pass |
| D14 | ES-4.2 D.14, p. 16 | "Vary the position of the correct answer; avoid a pattern." | Stored keys were 117/100/84/77 (A-D); now 95/95/93/95. The app also shuffles at display | Fixed |
| D15c,d | ES-4.2 D.15.c-d, p. 16 | "equivalent or synonymous options" | No duplicate or subset options found | Pass |
| D15f | ES-4.2 D.15.f, p. 16 | "a correct answer that is longer or shorter than the distractors" | 74 items (correct is at least 1.5x the longest distractor, or 0.6x the shortest) | Proposed |
| D15g | ES-4.2 D.15.g, p. 16 | "qualifiers in the correct answer (e.g., probably and ordinarily) unless they are also used in the distractors" | Q282, Q363 (covered by their length fixes); Q22, Q57, Q67, Q107, Q150, Q202, Q266 use "about"/"may"/"can"/"mainly" as part of the fact | Proposed |
| D15h | ES-4.2 D.15.h, p. 16 | "words such as "never" or "always" that suggest an incorrect option" | Q56, Q122, Q149, Q231, Q284, Q335, Q356, Q363, Q367 (and Q55, Q312 under other rules) | Proposed |
| D15i | ES-4.2 D.15.i, p. 17 | "a correct option that differs from the distractors in favorableness, style, or terminology" | 7 capitalization differences, all symbols or proper nouns (Keff, Reynolds, digits) | Pass |
| C7 | ES-4.2 C.7, p. 9 | "Avoid copying text directly from training or other reference material." | Conflicts with this project's verbatim-quote rule; see note | Not changed |

Not checkable by script and not reviewed item by item: D.15.b (options judged without the stem), C.8 (backward logic), C.5 (difficulty). Flashcards are not multiple choice, so only D.7 and the general C rules apply to them.

**C.7 note:** every item in this project is written from a verbatim source quote, as the content rules require. ES-4.2 C.7 discourages that for exam questions because it rewards memorized wording. Nothing was changed for C.7, since it conflicts with your sourcing rule. Your call.

## Content changes (applied 2026-11-02 at your confirmation)

Each row replaces one stem or option. Unless noted, the correct answer is untouched. Most length fixes lengthen one distractor so the options form NUREG Model D pairs ("two long and two short options", D.2). Q108, Q142, Q167, Q186 and Q194 instead shorten a distractor to pair with a short correct answer. Q122 and Q295 change the correct answer's wording but not its fact.

| ID | Rule | Current | Proposed |
|---|---|---|---|
| Q2 | D15f | Measure turbine output | Measure the fuel temperature rise as rods are withdrawn toward criticality |
| Q3 | D15f | Coolant pressure only | The pressure ratio across the turbine and the mass flow rate of the working fluid |
| Q4 | D15f | Pump head | Pressure differences maintained by the cover gas system |
| Q35 | D15f | friction as the dominant term | friction losses that convert flow energy into internal energy |
| Q38 | D15f | pump speed exceeds design | discharge pressure rises above the shutoff head, forcing flow back through the impeller |
| Q41 | D15f | good throttling | precise throttling of flow with the disk held at mid-travel |
| Q44 | D15f | viscosity and velocity only | fluid viscosity, flow velocity, and the bulk temperature of the coolant |
| Q45 | D15f | average to maximum heat flux | the average heat flux in the hottest channel to the minimum core heat flux |
| Q46 | D15f | fast flux to thermal flux | peak heat flux on the hottest fuel rod to the average heat flux of the coolest fuel rod |
| Q66 | D15f | From the point where the pump curve meets zero flow | From the point where the pump curve meets zero flow, known as the shutoff head of the pump |
| Q67 | D15f | The pump develops its maximum head at a set speed | The pump develops its maximum head at a set speed because the discharge valve is fully shut |
| Q80 | D15f | The Sodium Cover Gas System | The Sodium Cover Gas System (argon cover gas above the primary sodium pool) |
| Q90 | D15f | It is hydraulically driven by the primary sodium pumps | It is hydraulically driven by the primary sodium pumps and fails as-is on loss of electrical power |
| Q98 | D15f | During normal full-power operation | During any loss of offsite power with the primary pumps coasting down |
| Q107 | D15f | Control rods move radially | Control rods sit at the core edge, so radial expansion changes their worth more than axial expansion |
| Q108 | D15f | No feedback, because fuel temperature is constant | No feedback |
| Q114 | D15f | A higher melting point than oxide fuel | A higher melting point than oxide fuel, so a larger margin to fuel melting |
| Q115 | D15f | To moderate neutrons before they reach the core | To keep the steam generator outside containment so its tubes can be inspected at power |
| Q116 | D15f | Its primary system runs at high pressure | Its primary system runs at high pressure, which raises the sodium boiling point |
| Q117 | D15f | To reduce pumping power | To keep the pipes cooler by placing them in the cover gas region |
| Q125 | D15f | Each pin carries a unique radioactive tracer detected in the sodium | Each pin carries a unique radioactive tracer that delayed neutron detectors find in the sodium |
| Q127 | D15f | Pressurizer level instruments | Thermocouples on the steam outlet and flow meters on the feedwater line |
| Q128 | D15f | To support the piping weight | To support the piping weight and allow for thermal expansion of the lines |
| Q129 | D15f | Steam generator tube leaks | Sodium-water reaction detection in full-scale steam generator tubes |
| Q130 | D15f | A control rod ejection | Sodium boiling caused by a stuck-open bypass valve in the primary loop |
| Q134 | D15f | The operators inserted the control rods | The control rods inserted automatically on low primary flow, bringing power to decay heat |
| Q136 | D15f | Loss of all primary flow | A complete stagnation of primary flow followed by a delayed start of natural circulation |
| Q142 | D15f | Sodium voiding in the center of the core | Core sodium voiding |
| Q144 | D15f | To cool the sodium faster | To cool the remaining sodium faster and allow the tubes to be inspected |
| Q145 | D15f | Sodium boiling in the upper plenum | Sodium boiling in the upper plenum, which voids the center of the core |
| Q148 | D15f | Hydrogen recombiners | Hydrogen recombiners that keep the containment atmosphere below flammability limits |
| Q149 | D15h | Offsite consequences are always zero for SFRs | CDF and LRF cannot be calculated for a pool-type reactor with unpressurized coolant |
| Q150 | D15f | A loss of flow with the reactor kept at power | A loss of flow with the reactor kept at 5% power for about 30 hours on pony motors |
| Q151 | D15f | To vent the cover gas | To raise the sodium temperature so the pony motors could be restarted |
| Q167 | D15f | Provide HVAC for personnel comfort, freeze protection and equipment operability | Provide Nuclear Island HVAC |
| Q186 | D15f | Provide a controlled sodium environment for temporary storage of new and irradiated core assemblies | Store new and irradiated core assemblies in sodium |
| Q194 | D15f | Process cover gas waste streams and hold them up so radioactive isotopes such as argon-41 decay | Process and hold up gaseous radwaste |
| Q198 | D15f | Suppress and control fire with water, clean agents and chemical means | Suppress and control fire with water, clean agents and chemical means, and detect fires with smoke and heat detectors |
| Q217 | D15f | Manual start of the RAC blowers by operators | Manual start of the RAC blowers by operators from the main control room after the reactor trip |
| Q218 | D15f | Its primary sodium pumps run at full speed on backup power | Its primary sodium pumps run at reduced speed on backup power to force sodium through the intermediate heat exchangers |
| Q222 | D15f | To keep the cesium trap in service | To keep the fuel assemblies aligned with the IVTM so damaged assemblies can be removed after the accident |
| Q223 | D15f | It inserts control rods with its own drive motors | It inserts the control rods with its own drive motors, independent of the RPS and the trip breakers |
| Q225 | D15f | Steam generator tube leak detection | Steam generator tube leak detection from hydrogen meters in the sodium outlet |
| Q229 | D15f | Reactivity control and reactor scram | Reactivity control, criticality monitoring, and a path for emergency sodium makeup |
| Q230 | D15f | Sodium purification, cover gas supply, and leak detection | Sodium purification, cover gas supply, leak detection, and transfer of assemblies back to the reactor |
| Q231 | D15h | None; it has no safety classification | Controlling reactivity |
| Q232 | D15f | It stores emergency makeup sodium | It stores emergency makeup sodium that drains to the reactor vessel if the level falls |
| Q236 | D15f | The coils | The copper windings of the stator coils |
| Q238 | D15f | Gas keeps the detector from overheating | Gas keeps the detector from overheating when it is exposed to high radiation fields |
| Q239 | D15f | Neutrons directly ionize the gas | Neutrons directly ionize the gas because they carry a charge as they enter |
| Q240 | D15f | Gamma rays are blocked by the U-235 coating | Gamma rays are absorbed by the U-235 coating before they can reach the argon fill gas |
| Q242 | D15f | Peak fuel centerline temperature | Keeping peak fuel centerline temperature below the melting point of the metal fuel |
| Q247 | D15f | High | To the maximum of the indicated range |
| Q248 | D7 | Why do gaseous fission product poisons NOT pose a significant negative reactivity factor in a sodium fast reactor? (stem) | Why do gaseous fission product poisons have little negative reactivity effect in a sodium fast reactor? |
| Q248 | D15f | They are burned out by fast neutrons | They are burned out quickly by the high fast neutron flux in the core |
| Q249 | D15f | From the change in core inlet temperature | From the change in core inlet temperature and the primary sodium flow rate over the cycle |
| Q266 | D15f | It removes impurities from the sodium | It removes impurities from the sodium, like a cold trap, while it measures them |
| Q274 | D15f | Guides the arc away from the breaker operator | Guides the arc away from the breaker operator and vents the hot gases out of the case |
| Q282 | D15f | Full closed | Full closed, normally the spring-return position of the valve |
| Q283 | D15f | Plates transfer less heat than tubes | Plates transfer less heat than tubes for the same surface area and flow rate |
| Q289 | D15f | A delayed neutron, because it is born later | A delayed neutron, because it is born with more kinetic energy than a prompt neutron |
| Q310 | D15f | A process with no heat transfer into or out of the system | A process with no heat transfer into or out of the system, such as flow through a well-insulated turbine |
| Q319 | D15f | To regulate reactor temperature | To regulate reactor temperature by removing heat from the primary sodium |
| Q340 | D15f | Discharge pressure minus saturation pressure | Discharge pressure minus the saturation pressure of the fluid being pumped |
| Q350 | D15f | Turn the handwheel in the open direction to confirm it moves | Turn the handwheel a short distance in the open direction; checking toward open avoids disturbing an isolation |
| Q356 | D15h | It always overshoots setpoint | It overshoots setpoint on large step changes in the process variable |
| Q359 | D15f | Senses valve position for the control room only | Senses valve stem position and sends it to the control room for indication |
| Q360 | D15f | It uses a compensating chamber to subtract gamma current | It uses a compensating chamber to subtract the gamma-induced current from the total detector current |
| Q363 | D15f | Reactivity increase from higher coolant temperature, always positive | Reactivity change per degree of fuel temperature, which is negative because of Doppler broadening of U-238 resonances |
| Q364 | D15f | Reduced neutron leakage | Reduced neutron leakage from the core as the sodium density falls |
| Q366 | D15f | Reactivity change per degree of fuel temperature; positive at end of life | Reactivity change per degree of fuel temperature; positive at end of life because Pu-239 builds up in the fuel |
| Q371 | D15f | So that control rods can be withdrawn faster | So that control rods can be withdrawn faster during a startup without a period trip |
| Q372 | D15f | The worth of the most reactive control rod | The worth of the most reactive control rod during a rod withdrawal accident |
| Q374 | D15f | The coolant density increases | The coolant density increases as the rods leave the core, so more neutrons are moderated |
| Q376 | D15f | Control rod absorber burns out | Control rod absorber burns out faster at higher temperature |
| Q31 | D10 | 3.7 x 10^10 per second | 1.67 x 10^-24 MeV per amu |
| Q55 | D7 | None; every rod is assumed fully inserted | The two rods with the highest integral worth, which are assumed fully withdrawn |
| Q56 | D15h | None, because heat production stops when fission stops | About 20% immediately, falling to about 5% within one hour |
| Q284 | D15h | Its hottest cold-fluid temperature is always below the coldest hot-fluid temperature | Its hottest cold-fluid temperature stays below the coldest hot-fluid temperature |
| Q335 | D15h | Elevation head always exceeds velocity and pressure heads combined | Elevation head exceeds velocity and pressure heads combined |
| Q367 | D15h | Removes them entirely | Shifts them to higher energy with no change in capture |
| Q122 | D6 | How does SFR refueling differ from LWR refueling? (stem) | Compared with LWR refueling, how is SFR refueling done? |
| Q122 | D6 | It is done with the vessel head in place (correct) | With the vessel head in place |
| Q122 | D6 | It is done with the core drained of sodium | With the core drained of sodium |
| Q122 | D15h | It is done only at power | With the reactor at power |
| Q122 | D6 | It is done with the vessel head removed | With the vessel head removed |
| Q295 | D4 | Which statement about a subcritical reactor is correct? (stem) | In a subcritical reactor, how does the steady-state subcritical neutron level relate to the neutron source strength? |
| Q295 | D4 | Doubling count rate reduces the margin to criticality by about one quarter | It is inversely proportional to the source strength |
| Q295 | D4 | The subcritical neutron level is directly proportional to the neutron source strength (correct) | It is directly proportional to the source strength |
| Q295 | D4 | A given rod withdrawal gives the same count rate increase at keff 0.88 or 0.92 | It is proportional to the square of the source strength |
| Q295 | D4 | Equal reactivity additions reach equilibrium count rate faster as keff approaches 1 | It does not depend on the source strength |
| Q312 | D4 | Which statement about entropy is correct? (stem) | What does a change in entropy indicate? |
| Q312 | D4 | Entropy always decreases, so order naturally increases | The amount of energy that disappears in the process |
| Q312 | D4 | Entropy shows that energy disappears in every process | The rate at which the process proceeds toward equilibrium |
| Q312 | D4 | Entropy means all processes lead to chaos | The work the process does on its surroundings during a cycle |


## Topic distribution (ES-4.1)

NUREG-1021 does have a distribution rule, in ES-4.1 "Developing Written Examination Outlines." It sets point totals per tier for one 75-question RO exam. These quotes are from ES-4.1, pp. 3-4 of 28:

- "The final RO examination must total 75 points, and the SRO-only examination must total 25 points." (B.5.k)
- "sample every system or evolution in the group before selecting a second topic for any system or evolution" (B.5.h)
- "avoid selecting more than two K/A topics from a given system unless they relate to plant-specific priorities" (B.5.d)
- "For Tier 4 of the examination outline, randomly select K/As from Section 6, "Theory," of the applicable K/A catalog so that the K/A categories "Reactor Theory" and "Thermodynamics" have three items each." (B.6)

Form 4.1-BWR (p. 7 of 28) sets the RO points per tier: Tier 1 Emergency and Abnormal Plant Evolutions 26, Tier 2 Plant Systems 37, Tier 3 Generic Knowledge and Abilities 6, Tier 4 Theory 6.

The current 378 quiz questions, mapped to tiers by my own judgment (the app's topics are not K/A categories):

| Tier | Quiz topics | Questions | Share | NUREG share |
|---|---|---|---|---|
| 1 Emergency/abnormal | Safety functions 9, PSAR: Fundamental Safety Functions 7, Operating experience 6 | 22 | 6% | 35% (26/75) |
| 2 Plant systems | Sodium 24 and the 9 PSAR system topics 96 | 120 | 32% | 49% (37/75) |
| 2 Components (Tier 2 "G" column, Section 5; no fixed count) | Instrumentation 33, Pumps 20, Electrical 14, Mechanical components 11, Valves 7, Heat exchangers 7 | 92 | 24% | (part of Tier 2) |
| 3 Generic (conduct of operations, equipment control, radiation control, emergency plan) | none | 0 | 0% | 8% (6/75) |
| 4 Theory | Reactivity 34, Reactor kinetics 19, Neutron physics 15, Radiation physics 8, Neutron life cycle 5, Fluid flow 19, Heat transfer 13, Thermodynamics 12, Fuel 10, Decay heat removal 9 | 144 | 38% | 8% (6/75) |

Differences: the bank is theory-heavy (38% vs 8%), light on emergency and abnormal evolutions (6% vs 35%), and has no Tier 3 generic topics. These tiers come from LWR K/A catalogs, and there is no Natrium K/A catalog among the Included sources, so this is a rough comparison. Nothing was changed.

The quiz launch screen's equal-share rule is unchanged. It fits B.5.d: a set smaller than the topic count draws each topic at most once.

## Open item

Q295's explanation (x) no longer fits its new stem. Proposed replacement from the Power Changes lesson plan feedback: "If source strength (So) is doubled (for a given keff), total neutron population (Nt) would also double (directly proportional)." Applied 2026-11-02 at your confirmation.
