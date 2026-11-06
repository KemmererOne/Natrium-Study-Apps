#!/usr/bin/env python3
"""Batch 11, part 5: NP-04, blended from the handbook, Subcritical Multiplication.docx, Power Changes.docx
and supporting files. Xenon, moderator and chemical shim operating content stays off under Rule 8."""
import sys; sys.path.insert(0, "work")
import lessonlib
from lessonlib import build
lessonlib.ROTATE = True
NSR = "Needs sodium review"
KIN, OPS = ("Reactor Theory", "Reactor Kinetics and Neutron Sources"), ("Reactor Theory", "Reactor Operational Physics")
SM, PC, DN, RN = "Subcritical Multiplication.docx", "Power Changes.docx", "Delayed Neutron Importance.docx", "Reactor Neutrons.docx"
W = lambda f, s: f"Word: {f}, slide {s}"
S2 = lambda n: f"NRC slides ML19148A801, slide {n}"
SU, RK, RO = "Subcritical Multiplication", "Reactor Kinetics", "Reactor Operation"

build("NP-04", KIN, [
 ("scm", "Subcritical multiplication is the effect of fissions in the fuel increasing the effective source strength of a reactor with a keff less than one.", SU, 9),
 ("m", "Subcritical multiplication factor is the factor that relates the source level to the steady-state neutron level of the core.", SU, 9),
 ("ex", "A neutron source strength of 100 neutrons per generation will result in 250 neutrons per generation being produced from a combination of sources and fission in a shutdown reactor with a keff of 0.6.", SU, 2),
 ("half", "Notice from this example that the count rate doubled as the reactivity was halved (e.g., reactivity was changed from -1000 pcm to -500 pcm).", SU, 6),
 ("mplot", "For a critical reactor, 1/M is equal to zero.", SU, 7),
 ("mpred", "1/M plots can be used to predict the point of criticality.", SU, 9),
 ("stab", "The neutron population will typically reach its new steady-state value within 1-2 minutes, but the closer the reactor is to criticality, the longer the time will be to stabilize the neutron population.", SU, 7),
 ("per", "Reactor period is the time required for reactor power to change by a factor of e (2.718).", RK, 21),
 ("dt", "Doubling time is the time required for reactor power to double.", RK, 21),
 ("sur", "Reactor startup rate is the number of factors of ten that reactor power changes in one minute.", RK, 21),
 ("sign", "If the reactor period is positive, reactor power is increasing.", RK, 11),
 ("bbar", "is the weighted average of the total delayed neutron fractions of the different types of fuel used in a particular reactor.", RK, 21),
 ("imp", "delayed neutrons are born at lower average energies than fast neutrons.", RK, 21),
 ("jump", "Prompt jump is the small, immediate power increase that follows a positive reactivity insertion related to an increase in the prompt neutron population.", RK, 22),
 ("drop", "Prompt drop is the small, immediate power decrease that follows a negative reactivity insertion related to a decrease in the prompt neutron population.", RK, 22),
 ("pc", "Prompt critical is the condition when the reactor is critical on prompt neutrons alone.", RK, 22),
 ("pcb", "When a reactor is prompt critical, the neutron population, and hence power, can increase as quickly as the prompt neutron generation time allows.", RK, 22),
 ("dmg", "A reactor whose reactivity even approaches prompt critical is likely to suffer damage due to the rapid rise in power to a very high level.", RK, 16),
 ("dol", "Measuring reactivity in units of dollars is useful when determining if a reactor is prompt critical.", RK, 22),
 ("cent", "A reactivity unit related to the dollar is the cent, where one cent is one-hundredth of a dollar.", RK, 16),
 ("fuel", "Because the effective delayed neutron fraction is dependent upon the nuclides used as fuel, the value of the dollar is also dependent on the nuclides used as fuel.", RK, 16),
 ("src", "An installed neutron source, together with the subcritical multiplication process, may be needed to increase the neutron population to a level where it can be monitored throughout the startup procedure.", RO, 33),
 ("nosrc", "Without the installed source, it may be possible to withdraw the control rods to the point of criticality, and then continue withdrawal without detecting criticality because the reactor goes critical below the indicating range.", RO, 24),
 ("alt", "An alternative to using a startup source is to limit the rate of rod withdrawal, or require waiting periods between rod withdrawal increments.", RO, 24),
 ("ecp", "A reactivity balance called an Estimated Critical Position is used to predict the position of the control rods at which criticality will be achieved during a startup.", RO, 33),
 ("ecps", "This process provides an added margin of safety because a large discrepancy between actual and estimated critical rod positions would indicate that the core was not performing as designed.", RO, 24),
 ("refl", "In fast reactor systems, reflectors are not composed of moderating materials because it is desired to keep neutron energy high.", RO, 25),
 ("refl2", "The reflector functions by scattering some of the neutrons, which would have leaked from a bare (unreflected) core, back into the fuel to produce additional fissions.", RO, 25),
 ("zone", "Varying fuel concentrations or poison loading for flux shaping is frequently referred to as zoning.", RO, 26),
 ("tilt", "Power tilt is a non-symmetrical variation of core power in one quadrant of the core relative to the other quadrants.", RO, 34),
 ("sdm", "Shutdown margin is the instantaneous amount of reactivity by which a reactor is subcritical or would be subcritical from its present condition assuming all control rods are fully inserted except for the single rod with the highest integral worth, which is assumed to be fully withdrawn.", RO, 34),
 ("stuck", "The stuck rod criterion is applied to the shutdown margin to ensure that the failure of a single control rod will not prevent the control rod system from shutting down the reactor.", RO, 34),
 ("all", "Shutdown margin is required to exist at all times, even when the reactor is critical.", RO, 28),
 ("poah", "The inherent stability and power turning ability of a negative temperature coefficient are ineffective below the point of adding heat.", RO, 29),
 ("eighty", "The half-life of the longest lived delayed neutron precursor results in a reactor period of around -80 seconds or a startup rate of -1/3 DPM for most reactors after a reactor shutdown.", RO, 32),
 ("dh", "Decay heat is always present following reactor operation due to energy resulting from the decay of fission products.", RO, 34),
 ("dhist", "The amount of decay heat production after shutdown is directly influenced by the power history of the reactor prior to shutdown.", RO, 33),
 ("dh1", "This decay heat generation rate diminishes to less than 1% approximately one hour after shutdown.", RO, 33),
 ("dhlong", "Decay heat is a long-term consideration and impacts spent fuel handling, reprocessing, waste management, and reactor safety.", RO, 33),
 ("w_m", "It is the factor by which source neutrons are multiplied to get neutron population", "x", W(SM, "1.15 Subcritical Multiplication factor (M)")),
 ("w_drop", "A prompt drop is often associated with a reactor scram where a very large amount of negative reactivity is added.", "x", W(PC, "1.23 Step Insertion – Prompt Drop")),
 ("w_pc", "Some of the worst accidents in the history of nuclear power involve reactors that have achieved prompt criticality.", "x", W(PC, "1.28 Prompt Criticality")),
 ("s_sens", "At low values, response to small changes in the reactivity is magnified and power can change more quickly", "x", S2(5)),
], [
 dict(title="Subcritical multiplication", eo=["1.1", "1.2"], body=[
  ("q", "scm"), ("q", "m"), ("q", "w_m"),
  ("eq", "M = 1 / (1 - keff)   and   N = S / (1 - keff)", 9),
  ("q", "ex"),
  ("p", "The factor rises as positive reactivity is added to a shutdown reactor.", 3),
 ], checks=[dict(existing="Q24", eo="1.2"), dict(existing="Q292", eo="1.1"), dict(existing="Q293", eo="1.1"), dict(existing="Q295", eo="1.2")]),
 dict(title="Count rate and 1/M plots", eo=["1.3", "1.4"], body=[
  ("eq", "CR1 / CR2 = (1 - k2) / (1 - k1)", 5),
  ("p", "Instrument count rate is proportional to neutron level, so the source strength cancels out of the equation.", 5),
  ("q", "half"),
  ("p", "M grows without limit near criticality, so its inverse is plotted, using 1/M = CRo / CR with a reference count rate.", 7),
  ("q", "mplot"),
  ("f", "np-04-fig1", "1/M plotted against rod withdrawal in inches, falling toward zero, with an extrapolation showing the point of criticality."),
  ("q", "mpred"), ("q", "stab"),
 ], checks=[dict(existing="Q294", eo="1.3"),
  dict(eo="1.4", q="On a 1/M plot, what value of 1/M marks criticality?", o=["Zero", "One", "Infinity", "0.5"], a=0, x="For a critical reactor, 1/M is equal to zero.", p="mplot")]),
 dict(title="Period, doubling time and startup rate", eo=["2.1", "2.5", "2.6"], body=[
  ("q", "per"), ("q", "dt"), ("q", "sur"), ("q", "sign"),
  ("eq", "P = Po e^(t/τ)", 11), ("eq", "P = Po 10^(SUR t)", 17), ("eq", "P = Po 2^(t/DT)", 18),
  ("eq", "SUR = 26.06 / τ   and   DT = τ (ln 2)", 22),
 ], checks=[dict(existing="Q22", eo="2.1"), dict(existing="Q23", eo="2.1"),
  dict(eo="2.5", q="A reactor at 1000 watts has a doubling time of 2 minutes. What is its power 4 minutes later?", o=["2,000 W", "4,000 W", "8,000 W", "16,000 W"], a=1, x="P = (1000 W)(2)^(4/2) = 4000 W.", p="dt")]),
 dict(title="Delayed neutron fractions", eo=["2.2"], body=[
  ("p", "β is the fraction of all fission neutrons born delayed for a particular type of fuel.", 21),
  ("q", "bbar"),
  ("p", "The effective fraction is the average fraction multiplied by an importance factor, which accounts for the fact that", 21),
  ("q", "imp"),
  ("p", "Delayed neutrons average about 0.5 MeV, compared with about 2 MeV for prompt neutrons.", 12),
  ("q", "s_sens"),
 ], checks=[dict(existing="Q296", eo="2.2"), dict(existing="Q297", eo="2.2"), dict(existing="Q139", eo="2.2")]),
 dict(title="The period equation", eo=["2.3", "2.4"], body=[
  ("eq", "τ = ℓ*/ρ + (β̄eff - ρ) / (λeff ρ + ρ̇)   (prompt term plus delayed term)", 21),
  ("p", "τ is reactor period, ℓ* is prompt generation lifetime, β̄eff is the effective delayed neutron fraction, ρ is reactivity, λeff is the effective precursor decay constant, and ρ̇ is the rate of change of reactivity.", 21),
  ("eq", "Stable period: τ = (β̄eff - ρ) / (λeff ρ)", 22),
  ("p", "Approximate values for λeff are 0.08 per second at steady state, 0.1 per second for a power increase, and 0.05 per second for a power decrease.", 13),
 ], checks=[dict(existing="Q378", eo="2.4"),
  dict(eo="2.4", q="If a stable reactor period is 26.06 seconds, what is the startup rate?", o=["0.26 DPM", "1 DPM", "2.6 DPM", "26 DPM"], a=1, x="SUR = 26.06 / τ = 26.06 / 26.06 = 1 DPM.", p="sur")]),
 dict(title="Prompt jump and prompt drop", eo=["2.7"], body=[
  ("q", "jump"),
  ("f", "np-04-fig2", "Reactor power against time after a positive reactivity addition: a small immediate jump, then a slower rise."),
  ("q", "drop"),
  ("f", "np-04-fig3", "Reactor power against time after a negative reactivity addition: a small immediate drop, then a slower fall."),
  ("q", "w_drop"),
 ], checks=[dict(eo="2.7", q="What is a prompt jump?", o=["A small, immediate power increase after a positive reactivity insertion", "A sudden rise to prompt critical", "A rise in delayed neutron precursors after a scram", "A step change in coolant temperature"], a=0, x="Prompt jump is the small, immediate power increase that follows a positive reactivity insertion, related to an increase in the prompt neutron population.", p="jump")]),
 dict(title="Prompt critical and dollars", eo=["2.8", "2.9", "2.10"], body=[
  ("q", "pc"), ("q", "pcb"), ("q", "dmg"), ("q", "w_pc"), ("q", "dol"),
  ("p", "One dollar of reactivity is equal to the effective delayed neutron fraction, so a reactor with one dollar of positive reactivity is prompt critical.", 22),
  ("q", "cent"), ("q", "fuel"),
 ], checks=[dict(existing="Q54", eo="2.8"), dict(existing="Q377", eo="2.8"),
  dict(eo="2.10", q="A reactor has one dollar of positive reactivity. What is its condition?", o=["Prompt critical", "Exactly critical on delayed neutrons", "Subcritical", "Shut down"], a=0, x="One dollar of reactivity is equivalent to the effective delayed neutron fraction, so the reactor is prompt critical.", p="dol")]),
 dict(title="Startup and reactivity balance", eo=["3.1", "3.2", "3.3"], tag=NSR, body=[
  ("q", "src"), ("q", "nosrc"), ("q", "alt"), ("q", "ecp"), ("q", "ecps"),
  ("p", "The handbook's balance combines basic core reactivity, temperature reactivity, and two xenon terms. The xenon terms are thermal reactor content, so they stay off this page and objective 3.2 is marked for review.", 25),
 ], checks=[dict(existing="Q244", eo="3.1"),
  dict(eo="3.3", q="Why is an Estimated Critical Position calculated before startup?", o=["A large difference from the actual position would show the core was not performing as designed", "It sets the source strength", "It replaces the 1/M plot", "It sets the scram setpoints"], a=0, x="It provides an added margin of safety because a large discrepancy between actual and estimated positions would indicate that the core was not performing as designed.", p="ecps", place=OPS)]),
 dict(title="Core power distribution", eo=["3.4", "3.5"], body=[
  ("p", "Three methods are used to shape or flatten core power: reflectors, neutron poisons, and axial or radial variation of fuel enrichment.", 34),
  ("q", "refl"), ("q", "refl2"), ("q", "zone"),
  ("f", "np-04-fig5", "Radial flux shape for uniform and non-uniform enrichment, with higher enrichment in the outer regions reducing the central peak."),
  ("q", "tilt"),
  ("p", "Over-insertion of control rods in one part of the core is one cause.", 27),
 ], checks=[dict(existing="Q564", eo="3.4"),
  dict(eo="3.4", q="Why are fast reactor reflectors not made of moderating materials?", o=["It is desired to keep neutron energy high", "Moderators melt in sodium", "Moderating materials cannot scatter neutrons", "They would raise the delayed neutron fraction"], a=0, x="In fast reactor systems, reflectors are not composed of moderating materials because it is desired to keep neutron energy high.", p="refl", place=OPS)]),
 dict(title="Shutdown margin", eo=["3.6", "3.7"], body=[
  ("q", "sdm"), ("q", "all"), ("q", "stuck"),
 ], checks=[dict(existing="Q55", eo="3.6"),
  dict(eo="3.7", q="What is the reason for the stuck rod criterion?", o=["So the failure of a single control rod will not prevent shutting down the reactor", "To limit rod withdrawal speed", "To set the startup rate limit", "To size the neutron source"], a=0, x="The stuck rod criterion ensures that the failure of a single control rod will not prevent the control rod system from shutting down the reactor.", p="stuck", place=OPS)]),
 dict(title="Shutdown behavior", eo=["3.8"], tag=NSR, body=[
  ("p", "Factors that change during and after shutdown include control rod position and the temperature of the fuel and coolant.", 34),
  ("p", "The objective asks for five changes. The handbook's summary lists three, one of which is soluble poison, so objective 3.8 is marked for review.", 34),
  ("q", "poah"),
  ("p", "After a large negative reactivity addition, the neutron level falls about two decades in a prompt drop, then falls as the precursors decay.", 31),
  ("q", "eighty"),
 ], checks=[dict(existing="Q300", eo="3.8"), dict(existing="Q301", eo="3.8"),
  dict(eo="3.8", q="What reactor period is typical shortly after a reactor shutdown?", o=["About -80 seconds", "About -8 seconds", "About -800 seconds", "About +80 seconds"], a=0, x="The longest lived delayed neutron precursor results in a period of around -80 seconds, or a startup rate of -1/3 DPM.", p="eighty", place=OPS)]),
 dict(title="Decay heat", eo=["3.9", "3.10", "3.11"], body=[
  ("q", "dh"), ("q", "dhist"),
  ("p", "The amount depends on three factors: the pre-shutdown power level, how long the reactor operated, and the time since shutdown.", 34),
  ("q", "dh1"), ("q", "dhlong"),
 ], checks=[dict(eo="3.10", q="Which three variables affect the amount of decay heat after shutdown?", o=["Pre-shutdown power level, how long the reactor operated, and time since shutdown", "Coolant flow, rod position, and source strength", "Fuel enrichment, reflector type, and core size", "Startup rate, period, and doubling time"], a=0, x="Decay heat depends on the pre-shutdown power level, how long the reactor operated, and the amount of time since shutdown.", p="dhist", place=OPS),
  dict(eo="3.11", q="About how much decay heat exists one hour after a shutdown from full power?", o=["Less than 1%", "About 3%", "About 10%", "About 25%"], a=0, x="The decay heat generation rate diminishes to less than 1% approximately one hour after shutdown.", p="dh1", place=OPS)]),
], [
 dict(title="Subcritical multiplication factor", eo=["1.1"], page=3, problem="Calculate M for keff = 0.6, and the neutron level with a source of 1000 neutrons/sec.", steps=["M = 1 / (1 - 0.6) = 2.5", "N = S x M = (1000 neutrons/sec)(2.5)"], answer="2500 neutrons/sec"),
 dict(title="Steady-state neutron level", eo=["1.2"], page=4, problem="A source produces 110,000 neutrons per second and keff is 0.986. Calculate the stable total neutron production rate.", steps=["N = S / (1 - keff)", "N = (110,000 neutrons/sec) / (1 - 0.986)"], answer="7.86 x 10^6 neutrons per second"),
 dict(title="Count rate after a reactivity addition", eo=["1.3"], page=6, problem="A reactor at -1000 pcm reads 42 cps. Find the count rate after adding 500 pcm from control rod withdrawal.", steps=["k1 = 1 / (1 + 0.01000) and k2 = 1 / (1 + 0.00500)", "CR2 = CR1 (1 - k1) / (1 - k2)"], answer="83 cps"),
 dict(title="Stable period and startup rate", eo=["2.4"], page=18, problem="A reactor has λeff of 0.10 per second and an effective delayed neutron fraction of 0.0070. If keff is 1.0025, find the stable period and SUR.", steps=["ρ = (keff - 1) / keff = 0.00249 Δk/k", "τ = (0.0070 - 0.00249) / ((0.10 per sec)(0.00249)) = 18.1 sec", "SUR = 26.06 / 18.1 sec"], answer="τ = 18.1 sec and SUR = 1.44 DPM"),
 dict(title="Power after a negative reactivity addition", eo=["2.6"], page=19, problem="130 pcm of negative reactivity is added to a reactor critical at 100 watts. The reactor period is -124.6 seconds. Find power 2 minutes later.", steps=["P = Po e^(t/τ)", "P = (100 W) e^(120 s / -124.6 s)"], answer="38.2 W"),
 dict(title="Power from doubling time", eo=["2.5"], page=20, problem="A reactor has a power level of 1000 watts and a doubling time of 2 minutes. What is the power 10 minutes later?", steps=["P = Po 2^(t/DT)", "P = (1000 W)(2)^(10 min / 2 min)"], answer="32,000 W"),
], [
 ("What is subcritical multiplication?", "The effect of fissions in the fuel increasing the effective source strength of a reactor with a keff less than one.", "scm"),
 ("What is reactor startup rate?", "The number of factors of ten that reactor power changes in one minute.", "sur"),
 ("What is doubling time?", "The time required for reactor power to double.", "dt"),
 ("What is prompt drop?", "The small, immediate power decrease that follows a negative reactivity insertion.", "drop"),
 ("What does a dollar of reactivity equal?", "The effective delayed neutron fraction.", "dol"),
 ("What is shutdown margin?", "The reactivity by which a reactor is or would be subcritical with all rods fully inserted except the highest worth rod, which is assumed fully withdrawn.", "sdm", OPS),
 ("What is power tilt?", "A non-symmetrical variation of core power in one quadrant of the core relative to the others.", "tilt", OPS),
 ("What reactor period follows a shutdown for most reactors?", "Around -80 seconds, or a startup rate of -1/3 DPM.", "eighty", OPS),
 ("Why is a negative temperature coefficient ineffective at very low power?", "It is ineffective below the point of adding heat, because power changes there do not change temperature.", "poah", OPS),
], [
 ("A subcritical reactor multiplies its source by M = 1 / (1 - keff). 1/M plots predict criticality.", 9),
 ("Period, doubling time and startup rate describe power change.", 21),
 ("Prompt jump and prompt drop are small, immediate changes. One dollar of reactivity is prompt critical.", 22),
 ("Fast reactor reflectors are not moderating materials.", 25),
 ("Shutdown margin assumes the highest worth rod is fully withdrawn.", 34),
 ("Decay heat comes from fission product decay and falls to less than 1% about one hour after shutdown.", 33),
], [
 ("Conflict", "The handbook p.33 and p.34 say decay heat right after shutdown is about 5 to 6%. The Batch 5 decision says the handbook's 7%, taken from the HT material, and hides 6%. The two handbook statements differ, so neither starting value is on this page. NP-01 p.62's seven percent is a share of fission energy. Existing Q56 says 5-6%.", 33),
 ("Handbook wording", "Delayed neutron totals differ inside the handbook: NP-04 Table 1 gives U-238 0.0157 and Pu-239 0.00200, p.31 gives U-235 0.0064, and NP-02 p.30 gives 0.0148, 0.0021 and 0.0065. The page gives no fractions and sends the learner to NP-02.", 12),
 ("Handbook wording", "Objective 3.8 asks for five changes, and the handbook's summary lists three.", 34),
 ("Scope", "Objectives 3.2, 3.3 and 3.8 carry Needs sodium review. The manifest did not flag this module, so this is reported. Xenon terms, chemical shim, moderator pressure and flow effects, BWR flow control, heavy water behavior and burnup effects on the moderator coefficient are left off. Figures 4 and 6 show thermal flux and are not used.", 25),
 ("Word claim", "Power Changes.docx slide 1.24 gives a decay constant of 0.0124 per second for the -80 second period. The handbook does not give that value, so it is left off.", W(PC, "1.24 Step Insertion – Reactor Trip")),
 ("Word source", "The Word files teach with tables and practice problems that use plant-specific beta values, which are left off. Their prompt jump equation is on slide 1.20 as a picture.", W(PC, "1.20 Prompt change in power")),
], word=[
 ("1.3 Subcritical Multiplication", "Subcritical multiplication", SM), ("1.15 Subcritical Multiplication factor (M)", "Subcritical multiplication factor", SM), ("1.18 Count Rates and Keff", "Count rates", SM), ("1.3 Reactor Period", "Reactor period", PC), ("1.12 Startup Rate", "Startup rate", PC), ("1.19 Step Insertion – Prompt Jump", "Prompt jump", PC), ("1.23 Step Insertion – Prompt Drop", "Prompt drop", PC), ("1.28 Prompt Criticality", "Prompt criticality", PC), ("1.14 Delayed neutron Fraction", "Delayed neutron fractions", DN),
], word_file=SM)
