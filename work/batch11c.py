#!/usr/bin/env python3
"""Batch 11, part 3: NP-02, blended from the handbook, Source Neutrons.docx, Delayed Neutron Importance.docx
and Neutrons.docx. Rule 8: thermal and moderator objectives stay verbatim, tagged Needs sodium review.
Fast-spectrum equivalents cite the NRC fast reactor training slides, as approved."""
import sys; sys.path.insert(0, "work")
import lessonlib
from lessonlib import build
lessonlib.ROTATE = True
NSR = "Needs sodium review"
NEU, KIN = ("Reactor Theory", "Neutrons"), ("Reactor Theory", "Reactor Kinetics and Neutron Sources")
SN, DN, NE = "Source Neutrons.docx", "Delayed Neutron Importance.docx", "Neutrons.docx"
W = lambda f, s: f"Word: {f}, slide {s}"
S1 = lambda n: f"NRC slides ML19148A793, slide {n}"
S2 = lambda n: f"NRC slides ML19148A801, slide {n}"
SO, CX, RR, MO, PD, SP = "Neutron Sources", "Nuclear Cross Sections and Neutron Flux", "Reaction Rates", "Neutron Moderation", "Prompt and Delayed Neutrons", "Neutron Flux Spectrum"

build("NP-02", KIN, [
 ("src", "Source neutrons are important because they ensure that the neutron population remains high enough to allow a visible indication of neutron level on the most sensitive monitoring instruments while the reactor is shutdown and during the startup sequence.", SO, 1),
 ("intr", "Intrinsic neutron sources are those neutron-producing reactions that always occur in reactor materials.", SO, 1),
 ("inst", "An installed neutron source is an assembly placed in or near the reactor for the sole purpose of producing source neutrons.", SO, 3),
 ("sf", "Spontaneous fission of heavy nuclides in fuel, such as uranium-238, uranium-235, and plutonium-239, results in fission fragments and free neutrons.", SO, 4),
 ("b11", "Boron-11 mixed with the fuel undergoes an alpha-neutron reaction and becomes nitrogen-14.", SO, 4),
 ("cf", "Spontaneous fission of californium-252 results in fission fragments and free neutrons.", SO, 4),
 ("be1", "Beryllium-9 undergoes an alpha-neutron reaction (alpha from the decay of plutonium, polonium, or radium) and becomes carbon-12.", SO, 4),
 ("be2", "Beryllium-9 undergoes a gamma-neutron reaction (high energy gamma from decay of antimony-124) and becomes beryllium-8.", SO, 4),
 ("atomd", "The atom density is the number of atoms of a given type per unit volume of the material.", CX, 6),
 ("micro", "The probability of a particular reaction occurring between a neutron and a nucleus is called the microscopic cross section", CX, 7),
 ("area", "The microscopic cross section may also be regarded as the effective area the nucleus presents to the neutron for the particular reaction.", CX, 7),
 ("macro", "The macroscopic cross section is the probability of a given reaction occurring per unit travel of the neutron.", CX, 8),
 ("mfp", "This average distance traveled by a neutron before interaction is known as the mean free path for that interaction", CX, 10),
 ("res", "Resonance absorption occurs when the sum of the kinetic energy of the neutron and its binding energy is equal to an allowed nuclear energy level of the nucleus.", CX, 17),
 ("hvy", "This is because heavy nuclei are complex and have more possible configurations and corresponding energy states.", CX, 10),
 ("lgt", "Light nuclei, being less complex, have fewer possible energy states and fewer resonances that are sparsely distributed at higher energy levels.", CX, 10),
 ("fastr", "This is called the \"fast neutron region.\"", CX, 10),
 ("low", "At low neutron energies (<1 eV) the cross section is inversely proportional to the neutron velocity.", CX, 17),
 ("self", "Self-shielding is where the local neutron flux is depressed within a material due to neutron absorption near the surface of the material.", CX, 17),
 ("pin", "This is especially important at resonance energies, where the absorption cross sections are large.", CX, 16),
 ("rr", "The reaction rate is the number of interactions of a particular type occurring in a cubic centimeter of material in a second.", RR, 22),
 ("pw", "Over a period of several days, while the atom density of the fuel can be considered constant, the neutron flux is directly proportional to reactor power.", RR, 22),
 ("slow", "The neutron flux for a given power level will increase very slowly over a period of months due to the burnup of the fuel and resulting decrease in atom density and macroscopic cross section.", RR, 21),
 ("loss", "Sometimes it is convenient, based upon information known, to work with an average fractional energy loss per collision as opposed to an average logarithmic fraction.", MO, 25),
 ("dl", "Delayed neutrons are released from the decay of fission products that are called delayed neutron precursors.", PD, 32),
 ("fr", "The fraction of neutrons born as delayed neutrons is different for different fuel materials.", PD, 32),
 ("mech", "The delayed neutrons are emitted immediately following the first beta decay of a fission fragment known as a delayed neutron precursor.", PD, 29),
 ("gen", "The neutron generation time is the time required for neutrons from one generation to cause the fissions that produce the next generation of neutrons.", PD, 30),
 ("dgen", "The average delayed neutron generation time is about 12.5 seconds.", PD, 32),
 ("ctl", "Delayed neutrons are responsible for the ability to control the rate at which power can rise in a reactor.", PD, 32),
 ("ctl2", "If only prompt neutrons existed, reactor control would not be possible due to the rapid power changes.", PD, 32),
 ("pe", "Prompt neutrons are born at energies between 0.1 MeV and 10 MeV.", SP, 37),
 ("pe2", "The average prompt neutron energy is about 2 MeV.", SP, 37),
 ("fsp", "Fast reactors have a neutron energy spectrum that has the same shape as the prompt neutron energy spectrum.", SP, 37),
 ("noth", "No attempt is made to thermalize or slow down neutrons in the fast breeder reactor (liquid metal cooled); therefore, an insignificant number of neutrons exist in the thermal range.", SP, 34),
 ("s_sfr", "In SFR, moderation is avoided – no thermal neutrons; most fissions occur at higher energies (>10 keV)", "x", S1(3)),
 ("s_sdp", "Slowing-down power in FR is ~1% that observed for typical LWR", "x", S1(4)),
 ("s_leak", "Thus, neutrons are either absorbed or leak from the reactor before they can reach thermal energies", "x", S1(4)),
 ("s_hard", "Net result is that the SFR-metal has the hardest neutron spectrum", "x", S1(5)),
 ("s_u238", "Threshold fission at ~1 MeV (~10% of total fission rate in a fast reactor)", "x", S1(8)),
 ("s_1g", "One-group cross sections are significantly reduced in fast system", "x", S1(12)),
 ("s_dnf", "Net result is 0.3-0.4% for conventional compositions", "x", S2(5)),
 ("s_sens", "At low values, response to small changes in the reactivity is magnified and power can change more quickly", "x", S2(5)),
 ("s_leak2", "Neutron leakage is increased (>20% in typical designs, reactivity coefficient)", "x", S2(3)),
 ("w_prec", "Not all fission fragments are Delayed Neutron Precursors, but all Delayed Neutron Precursors are fission fragments!", "x", W(NE, "1.60 Delayed Neutron Precursors")),
 ("w_rate", "As it turns out, the delayed neutrons control the rate of power change far more than the prompt neutrons do.", "x", W(DN, "1.5 Delayed Neutrons effect on rate of power change")),
 ("w_one", "Spontaneous fission of U-238 from the fuel provides more then enough neutrons to start a chain reaction.", "x", W(SN, "1.9 Knowledge Check #1")),
], [
 dict(title="Why source neutrons matter", eo=["1.1"], body=[
  ("p", "Source neutrons are neutrons produced by reactions other than neutron-induced fission.", 1),
  ("q", "src"),
  ("p", "This verifies instrument operability and allows monitoring of neutron population changes.", 1),
  ("q", "w_one"),
  ("q", "intr"), ("q", "inst"),
 ], checks=[
  dict(existing="Q244", eo="1.1"),
  dict(existing="Q566", eo="1.1"),
 ]),
 dict(title="Intrinsic neutron sources", eo=["1.2"], tag=NSR, body=[
  ("q", "sf"), ("q", "b11"),
  ("p", "The handbook's third example is a gamma-neutron reaction with deuterium in water coolant. It depends on water, so it stays off this page and objective 1.2 is marked for review.", 3),
 ], checks=[
  dict(existing="Q567", eo="1.2"),
 ]),
 dict(title="Installed neutron sources", eo=["1.3"], body=[
  ("p", "Intrinsic sources can be weak or depend on recent power history, so many reactors have installed sources to keep shutdown neutron levels detectable.", 3),
  ("q", "cf"), ("q", "be1"), ("q", "be2"),
  ("p", "Californium-252's drawbacks for some applications are high cost and a short half-life of 2.65 years.", 3),
 ], checks=[
  dict(eo="1.3", q="Which reaction is an example of an installed neutron source?", o=["Beryllium-9 undergoing an alpha-neutron reaction", "Spontaneous fission of uranium-238 in the fuel", "Boron-11 mixed with the fuel", "Neutron-induced fission of plutonium-239"], a=0, x="Installed sources include californium-252 spontaneous fission and alpha-neutron and gamma-neutron reactions with beryllium-9.", p="be1", place=KIN),
 ]),
 dict(title="Atom density and cross sections", eo=["2.1", "2.2"], body=[
  ("q", "atomd"),
  ("eq", "N = ρ NA / M   (N in atoms/cm³)", 6),
  ("q", "micro"), ("q", "area"),
  ("p", "Microscopic cross sections are measured in barns, where 1 barn = 10^-24 cm².", 17),
  ("q", "macro"),
  ("eq", "Σ = Nσ   (Σ in cm⁻¹)", 8),
  ("p", "The total microscopic cross section is the sum of absorption and scattering. Absorption divides into fission and capture.", 8),
 ], checks=[
  dict(existing="Q504", eo="2.1"),
  dict(existing="Q506", eo="2.1"),
  dict(eo="2.2", q="How is macroscopic cross section related to microscopic cross section?", o=["Σ = Nσ", "Σ = σ / N", "Σ = N / σ", "Σ = N + σ"], a=0, x="The macroscopic cross section is the atom density times the microscopic cross section.", p="macro", place=NEU),
 ]),
 dict(title="Absorption cross section and neutron energy", eo=["2.3", "2.4", "2.5"], tag=NSR, body=[
  ("f", "np-02-fig1", "Absorption cross section against neutron energy on log axes, falling in the 1/v region, then a region of resonance peaks, then the fast region."),
  ("q", "low"), ("q", "res"), ("q", "hvy"), ("q", "lgt"),
  ("p", "For higher neutron energies, the absorption cross section steadily decreases as the energy increases.", 10),
  ("q", "fastr"),
  ("p", "A fast reactor works at the high energy end of this curve, as the slides below show.", S1(3)),
  ("q", "s_1g"), ("q", "s_u238"),
 ], checks=[
  dict(eo="2.4", q="When does resonance absorption occur?", o=["When the neutron's kinetic energy plus its binding energy equals an allowed nuclear energy level", "When the neutron is in thermal equilibrium with the medium", "When the neutron's energy exceeds 10 MeV", "When two neutrons strike a nucleus together"], a=0, x="Resonance absorption occurs when the sum of the kinetic energy of the neutron and its binding energy equals an allowed nuclear energy level.", p="res", place=NEU),
  dict(eo="2.5", q="Why do heavy nuclei have more resonances than light nuclei?", o=["They are complex, with more possible configurations and energy states", "They have fewer neutrons", "They have no binding energy", "Their nuclei are less stable to scattering"], a=0, x="Heavy nuclei are complex and have more possible configurations and corresponding energy states.", p="hvy", place=NEU),
 ]),
 dict(title="Mean free path and mixtures", eo=["2.1", "2.6", "2.7", "2.8"], body=[
  ("q", "mfp"),
  ("eq", "λ = 1 / Σ", 10),
  ("p", "Most materials contain several isotopes, so each isotope's macroscopic cross section is found and the values are summed.", 11),
  ("eq", "Σ = N₁σ₁ + N₂σ₂ + N₃σ₃ + ... + Nₙσₙ", 11),
 ], checks=[
  dict(eo="2.6", q="A material has a macroscopic cross section of 0.1 cm⁻¹ for an interaction. What is the mean free path?", o=["0.1 cm", "1 cm", "10 cm", "100 cm"], a=2, x="The mean free path equals 1 / Σ = 1 / (0.1 cm⁻¹) = 10 cm.", p="mfp", place=NEU),
 ]),
 dict(title="Neutron flux and self-shielding", eo=["2.1", "2.9"], body=[
  ("p", "Neutron flux is the total path length covered by all neutrons in one cubic centimeter during one second.", 15),
  ("eq", "φ = nv   (φ in neutrons/cm²-sec)", 15),
  ("q", "self"),
  ("p", "For example, the interior of a fuel pin sees a lower average flux than its outer surfaces, because neutrons are absorbed before they reach it.", 16),
  ("q", "pin"),
 ], checks=[
  dict(eo="2.9", q="Why does the interior of a fuel pin see a lower average flux than its surface?", o=["Neutrons are absorbed near the surface and cannot reach the interior", "The interior is hotter", "Neutrons are repelled by the fuel", "The interior contains no fissile material"], a=0, x="Self-shielding is where the local neutron flux is depressed within a material due to neutron absorption near the surface.", p="self", place=NEU),
 ]),
 dict(title="Reaction rates and reactor power", eo=["2.10", "2.11"], body=[
  ("q", "rr"),
  ("eq", "R = φΣ", 18),
  ("p", "Multiplying the reaction rate by the core volume gives the total fission rate. With 200 MeV per fission, 3.12 x 10^10 fissions release 1 watt-second of energy.", 20),
  ("q", "pw"), ("q", "slow"),
 ], checks=[
  dict(existing="Q505", eo="2.11"),
  dict(eo="2.10", q="A section of a reactor has a macroscopic fission cross section of 0.1 cm⁻¹ and a flux of 10^13 neutrons/cm²-sec. What is the fission rate per cm³ each second?", o=["10^11", "10^12", "10^13", "10^14"], a=1, x="R = φΣ = (10^13)(0.1) = 10^12 fissions per cm³ each second.", p="rr", place=NEU),
 ]),
 dict(title="Slowing down in a fast reactor", eo=["2.12", "2.13", "2.14"], tag=NSR, body=[
  ("p", "The handbook's thermalization and moderator material is for thermal reactors, so it stays off this page and objectives 2.12 and 2.13 are marked for review. The fast reactor equivalent is below.", 23),
  ("q", "s_sdp"), ("q", "s_leak"), ("q", "s_hard"),
  ("q", "loss"),
  ("eq", "E(N) = E₀ (1 - x)^N", 28),
  ("p", "Here x is the average fractional energy loss per collision and N is the number of collisions.", 26),
 ], checks=[
  dict(existing="Q103", eo="2.12"),
  dict(eo="2.14", q="A 2 MeV neutron loses an average fraction of 0.5 of its energy per collision. What is its energy after 2 collisions?", o=["0.25 MeV", "0.5 MeV", "1 MeV", "1.5 MeV"], a=1, x="E = (2 MeV)(1 - 0.5)^2 = 0.5 MeV.", p="loss", place=NEU),
 ]),
 dict(title="Prompt and delayed neutrons", eo=["3.1", "3.2", "3.3"], body=[
  ("p", "Over 99% of the neutrons produced in fission are prompt neutrons, released within about 10^-13 seconds of the fission event.", 29),
  ("q", "dl"), ("q", "mech"), ("q", "w_prec"),
  ("p", "A precursor's beta decay leaves an excited daughter that immediately ejects a neutron, so delayed neutrons appear with the precursor's half-life. Half-lives vary from fractions of a second to almost a minute.", 32),
  ("q", "fr"),
  ("l", ["Uranium-235: 0.0065", "Plutonium-239: 0.0021", "Uranium-238: 0.0148", "Uranium-233: 0.0026"], 30),
  ("q", "s_dnf"),
 ], checks=[
  dict(existing="Q50", eo="3.2"),
  dict(existing="Q288", eo="3.2"),
  dict(existing="Q106", eo="3.2"),
  dict(eo="3.3", q="How is a delayed neutron produced?", o=["A precursor beta decays to an excited daughter that immediately ejects a neutron", "A prompt neutron is absorbed and re-emitted", "A fission fragment undergoes spontaneous fission", "A gamma ray strikes deuterium"], a=0, x="A precursor's beta decay results in an excited daughter nucleus, which immediately ejects a neutron.", p="mech", place=KIN),
 ]),
 dict(title="Generation time and reactor control", eo=["3.4", "3.5", "3.6"], body=[
  ("q", "gen"),
  ("p", "The handbook gives fast reactors a prompt generation time of about 10^-6 seconds.", 30),
  ("q", "dgen"),
  ("p", "That delayed time is dominated by precursor decay, for uranium-235 precursors. The other intervals are insignificant beside it.", 31),
  ("eq", "ℓ(avg) = (1 - β) ℓ* + β (ℓ* + delayed generation time)", 31),
  ("q", "ctl"), ("q", "ctl2"), ("q", "w_rate"), ("q", "s_sens"),
 ], checks=[
  dict(existing="Q6", eo="3.4"),
  dict(existing="Q7", eo="3.4"),
  dict(existing="Q15", eo="3.6"),
  dict(existing="Q16", eo="3.6"),
 ]),
 dict(title="Neutron energy spectrum in a fast reactor", eo=["4.1", "4.2", "4.3"], tag=NSR, body=[
  ("q", "pe"), ("q", "pe2"),
  ("f", "np-02-fig2", "Fraction of neutrons per MeV against neutron energy, rising to a peak near 0.7 MeV and falling off at higher energy."),
  ("p", "The handbook's plot is for thermal fission of uranium-235, and the most probable energy is about 0.7 MeV. Values vary slightly for other nuclides.", 33),
  ("q", "fsp"), ("q", "noth"), ("q", "s_sfr"), ("q", "s_leak2"),
  ("f", "np-02-fig3", "Neutron flux against energy for a thermal reactor and a fast breeder reactor. The fast breeder curve has no thermal peak."),
  ("p", "The thermal reactor spectrum and its region-by-region shape stay off this page, so objectives 4.2 (part b) and 4.3 are marked for review.", 34),
 ], checks=[
  dict(eo="4.1", q="What is the average energy at which prompt neutrons are produced?", o=["About 2 MeV", "About 0.025 eV", "About 1 keV", "About 200 MeV"], a=0, x="The average prompt neutron energy is about 2 MeV.", p="pe2", place=NEU),
  dict(eo="4.2", q="What does the neutron energy spectrum of a fast reactor look like?", o=["It has the same shape as the prompt neutron energy spectrum", "It has a large thermal peak", "It has two pronounced peaks", "It is flat at all energies"], a=0, x="Fast reactors have a neutron energy spectrum that has the same shape as the prompt neutron energy spectrum.", p="fsp", place=NEU),
 ]),
], [
 dict(title="Atom density of aluminum", eo=["2.1"], page=7, problem="A block of aluminum has a density of 2.699 g/cm³ and a gram atomic weight of 26.9815 g. Calculate the atom density.", steps=["N = ρ NA / M", "N = (2.699 g/cm³)(6.022 x 10^23 atoms/mole) / (26.9815 g/mole)"], answer="N = 6.024 x 10^22 atoms/cm³"),
 dict(title="Cross sections and mean free paths of an alloy", eo=["2.7", "2.6"], tag=NSR, page=13, problem="An alloy has 5.64 x 10^22 aluminum atoms/cm³ and 2.85 x 10^21 silicon atoms/cm³. Aluminum has σa = 0.23 barns and σs = 1.49 barns. Silicon has σa = 0.16 barns and σs = 2.20 barns. These are the handbook's thermal values, used here only to show the method.", steps=["Σa = (5.64 x 10^22)(0.23 x 10^-24 cm²) + (2.85 x 10^21)(0.16 x 10^-24 cm²) = 0.0134 cm⁻¹", "Σs = (5.64 x 10^22)(1.49 x 10^-24 cm²) + (2.85 x 10^21)(2.20 x 10^-24 cm²) = 0.0903 cm⁻¹", "λa = 1 / Σa and λs = 1 / Σs"], answer="λa = 74.3 cm and λs = 11.1 cm"),
 dict(title="Average neutron generation time", eo=["3.5"], page=31, problem="A reactor has a prompt generation time of 5 x 10^-5 seconds, a delayed generation time of 12.5 seconds, and β = 0.0065. These are the handbook's values for a thermal system. Calculate the average generation time.", tag=NSR, steps=["Delayed neutrons dominate the average: 0.0065 x 12.5 seconds is about 0.081 seconds", "The prompt term is very small beside it"], answer="About 0.0813 seconds, compared with about 5 x 10^-5 seconds on prompt neutrons alone"),
], [
 ("What is an intrinsic neutron source?", "Neutron-producing reactions that always occur in reactor materials.", "intr"),
 ("Why are source neutrons important?", "They keep the neutron population high enough to give a visible indication on the most sensitive instruments while shut down and during startup.", "src"),
 ("What is a macroscopic cross section?", "The probability of a given reaction occurring per unit travel of the neutron.", "macro", NEU),
 ("What is mean free path?", "The average distance traveled by a neutron before interaction.", "mfp", NEU),
 ("What is self-shielding?", "Local neutron flux is depressed within a material due to neutron absorption near its surface.", "self", NEU),
 ("What is a reaction rate?", "The number of interactions of a particular type occurring in a cubic centimeter of material in a second.", "rr", NEU),
 ("What are delayed neutrons released from?", "The decay of fission products called delayed neutron precursors.", "dl"),
 ("What is the neutron generation time?", "The time required for neutrons from one generation to cause the fissions that produce the next generation.", "gen", NEU),
 ("At what energies are prompt neutrons born?", "Between 0.1 MeV and 10 MeV, with an average of about 2 MeV.", "pe", NEU),
 ("At what energies do most fissions occur in an SFR?", "At higher energies, above 10 keV. Moderation is avoided, and there are no thermal neutrons.", "s_sfr", NEU),
 ("About what share of the fission rate in a fast reactor comes from U-238 threshold fission?", "About 10%. The threshold is at about 1 MeV.", "s_u238", NEU),
], [
 ("Source neutrons keep neutron level visible on instruments. Sources are intrinsic or installed.", 4),
 ("Microscopic cross section is a probability per nucleus, and macroscopic cross section is Σ = Nσ. Mean free path is 1 / Σ.", 17),
 ("Reaction rate is R = φΣ. Over several days, flux is directly proportional to reactor power.", 22),
 ("In a fast reactor, moderation is avoided and most fissions occur above 10 keV.", S1(3)),
 ("Delayed neutrons come from precursors, and they make power changes controllable.", 32),
 ("Prompt neutrons average about 2 MeV. A fast reactor's spectrum has the same shape as the prompt spectrum.", 37),
], [
 ("Conflict", "Delayed Neutron Importance.docx slide 1.3 says prompt neutrons appear within 10 to the minus 14 seconds. The handbook p.29 and p.32 give 10 to the minus 13 seconds. By decision on Nov 5, 2026, the page shows the handbook value.", W(DN, "1.3 Delayed Neutron Formation")),
 ("Conflict", "ML19148A801 slide 5 gives U-235's delayed neutron fraction as about 0.67%. The handbook p.30 gives 0.0065, and Neutrons.docx uses 0.0065 and a rounded 0.7%. The page shows the handbook value.", 30),
 ("Scope", "Objectives 1.2, 2.3, 2.4, 2.5, 2.12, 2.13, 4.2 and 4.3 carry Needs sodium review. The deuterium photoneutron source, moderator properties, logarithmic energy decrement, moderating ratio, the temperature correction for thermal cross sections, thermal neutron velocities and the thermal reactor spectrum are left off. The water and hydrogen slowing down examples are left off.", 23),
 ("Scope", "Equation 2-7 uses thermal flux, so the page keeps only the general steps, as Neutrons.docx slide 1.90 does. Objective 2.10's check uses the handbook's numbers with the word thermal removed. The alloy and generation time examples use the handbook's thermal values and are tagged.", 19),
 ("Handbook wording", "The handbook p.30 prints the fast reactor prompt generation time as about 10^-6 seconds. ML19148A801 slide 4 lists prompt neutron lifetimes of 0.32 to 0.38 microseconds for specific designs. The page uses the handbook value.", 30),
 ("Word source", "Delayed Neutron Importance.docx teaches kinetics by spreadsheet. Slides 1.6 to 1.12 are left for NP-04, along with the delayed neutron fraction terms on slides 1.14 to 1.17.", W(DN, "1.5 Delayed Neutrons effect on rate of power change")),
], word=[
 ("1.3 Source Neutron Importance", "Why source neutrons matter", SN), ("1.6 Source Neutron Types", "Intrinsic and installed sources", SN), ("1.71 Neutron Reaction Terms", "Reaction terms and cross sections", NE), ("1.86 Reaction Rate", "Reaction rate", NE), ("1.89 Neutron Flux and Reactor Power", "Flux and reactor power", NE), ("1.56 Prompt and Delayed Neutrons", "Prompt and delayed neutrons", NE), ("1.3 Delayed Neutron Formation", "Delayed neutron formation", DN),
], word_file=SN)
