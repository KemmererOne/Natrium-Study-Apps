#!/usr/bin/env python3
"""Batch 12, part 3: NA-03. The Word file holds only two knowledge checks in text, so by decision of
Nov 5, 2026 the lesson also uses the NRC training slides and the PSAR. The ammeter item stays off."""
import sys; sys.path.insert(0, "work")
import lessonlib
from lessonlib import build
lessonlib.ROTATE = True
F = "Sodium Leak Detectors.docx"
W = lambda s: f"Word: {F}, slide {s}"
KC, T = W("1.5 Knowledge Check 1"), W("1.1 TLO 6: Sodium Leak Detectors")
OV, OP, FI = "NRC slides ML19149A378, slide 25", "NRC slides ML19149A433, slide 21", "NRC slides ML19149A618, slide 22"
P = lambda sec, pg: f"PSAR Rev 1, ML25276A288, Sec. {sec}, p. {pg}"
NNA1, NNA2, DET, SPS, ANN = P("7.5.2.1", "7.5-10"), P("7.5.2.2", "7.5-12"), P("7.5.2.3.4", "7.5-16"), P("7.2.4.2.2", "7.2-47"), P("7.2.3.2.1", "7.2-28")
FP, FP2 = P("8.2.1.8", "8.2-3"), P("8.2.2", "8.2-4")
SENS = ("Components", "Sensors and Detectors")
ANC = ("PSAR design basis", "PSAR: Ancillary Systems")
OBJ = [dict(number="TLO 6", text="Sodium Leak Detectors", items=[], cite=T, enabling=[])]

build("NA-03", SENS, [
 ("rad", "Primary sodium is radioactive", "x", OV),
 ("burn", "Liquid sodium will burn in air", "x", OV),
 ("loss", "Loss of sodium could impair heat transport systems", "x", OV),
 ("cond", "Leaks can be detected by conductivity probes (usually in low spots below sodium-containing tanks) or by sensing of sodium aerosols", "x", OV),
 ("lbb", "Due to low pressure, sodium leaks are generally small and can be detected before larger piping breaks occur", "x", OP),
 ("contact", "Contact detectors (spark plugs)", "x", OP),
 ("trip", "automatically trips SPS-P pumps", "x", NNA2),
 ("spark", "spark plug type leak detectors function on the principal of fluid completing an open circuit.", "x", KC),
 ("sps", "SPS leak detection uses devices such as wire and cable, spark plugs, and mutual inductance type sensors.", "x", SPS),
 ("nna", "detects, collects, and contains sodium leaks to mitigate sodium fires", "x", NNA1),
 ("type", "The specific type of sodium leak detector is based on the needs of the installation location and configuration.", "x", DET),
 ("where", "Sodium leak detectors are located within leak mitigative features, at vulnerable valves, and inside catch pans.", "x", DET),
 ("self", "Detectors will generally be based on conductivity detection with a self-test function.", "x", DET),
 ("smoke", "In areas where sodium reactions may occur (e.g., Intermediate Air Cooling stacks), smoke detection is provided.", "x", DET),
 ("mcr", "The sodium leak detectors activate an alarm within the MCR upon detection of sodium.", "x", DET),
 ("pts", "Leak detection is provided at multiple points between pipe supports along all normally sodium containing systems", "x", FP),
 ("len", "The leak detectors are capable of detecting leaks within the entire length of pipe it covers.", "x", FP),
 ("small", "Detection of small leaks helps prevent large leaks from occurring.", "x", FP2),
 ("ann", "Annulus gas is recirculated and monitored for sodium buildup via absolute filter differential pressure changes, oxygen concentrations, and radiation levels.", "x", ANN),
], [
 dict(title="Why sodium leaks must be detected", eo=[], body=[
  ("p", "Sodium leak detection is important for three reasons:", OV),
  ("q", "rad"), ("q", "burn"), ("q", "loss"),
  ("p", "Sodium systems run at low pressure, so under the leak before break approach:", OP),
  ("q", "lbb"),
  ("q", "small"),
 ], checks=[
  dict(eo="", q="Why does the leak before break approach suit sodium piping?", o=["Low pressure makes leaks generally small, so they can be detected before larger breaks", "Sodium piping cannot leak at all", "Sodium freezes at every leak and seals it", "Water systems are routed beside the piping to detect leaks"], a=0, x="Because of the low pressure, sodium leaks are generally small and can be detected before larger piping breaks occur.", p="lbb"),
 ]),
 dict(title="Types of sodium leak detectors", eo=[], body=[
  ("p", "NRC training slides list these ways of detecting sodium leaks:", OP),
  ("l", ["Smoke detectors", "Contact detectors (spark plugs)", "Cable detectors", "Aerosol monitors", "Inspections"], OP),
  ("q", "cond"),
  ("p", "Double-walled piping may also carry leak detectors in the gap between the walls.", OP),
 ], checks=[
  dict(eo="", q="Where are sodium conductivity probes usually located?", o=["In low spots below sodium-containing tanks", "At the top of the cover gas space", "Inside the fuel assemblies", "On the outside of the containment wall"], a=0, x="Leaks can be detected by conductivity probes, usually in low spots below sodium-containing tanks.", p="cond"),
 ]),
 dict(title="Spark plug type detectors", eo=[], body=[
  ("q", "spark"),
  ("p", "So the detector's circuit is normally open, and leaking fluid closes it. The lesson plan's diagrams are pictures and are not used.", KC),
 ], checks=[
  dict(existing="Q509", eo=""),
 ]),
 dict(title="Leak detection at Natrium", eo=[], body=[
  ("p", "The Sodium Leak Detection, Collection, and Containment System (NNA):", NNA1),
  ("q", "nna"),
  ("q", "type"),
  ("q", "where"),
  ("q", "self"),
  ("q", "smoke"),
  ("q", "mcr"),
  ("q", "pts"),
  ("q", "len"),
  ("q", "sps"),
  ("p", "Sodium leakage from the reactor vessel into the guard vessel is watched through the cover gas system.", ANN),
  ("q", "ann"),
 ], checks=[
  dict(existing="Q84", eo=""),
  dict(eo="", q="What detection principle will Natrium sodium leak detectors generally be based on?", o=["Conductivity detection with a self-test function", "Ultrasonic detection", "Neutron detection", "Thermal expansion of a bimetal strip"], a=0, x="The PSAR says detectors will generally be based on conductivity detection with a self-test function.", p="self", place=ANC),
  dict(eo="", q="In the Natrium design, where are sodium leak detectors located?", o=["Within leak mitigative features, at vulnerable valves, and inside catch pans", "Only on the reactor head", "Only in the main control room", "Only in the turbine building"], a=0, x="Sodium leak detectors are located within leak mitigative features, at vulnerable valves, and inside catch pans.", p="where", place=ANC),
  dict(eo="", q="What do Natrium sodium leak detectors activate on detection of sodium?", o=["An alarm within the main control room", "A reactor scram", "A water fire suppression system", "A sodium dump to the guard vessel"], a=0, x="The sodium leak detectors activate an alarm within the MCR upon detection of sodium.", p="mcr", place=ANC),
 ]),
 dict(title="What a leak signal does", eo=[], body=[
  ("p", "NNA leak detection signals support automatic actions for the primary Sodium Processing System (SPS-P):", NNA2),
  ("l", ["NNA sends a signal to the Auxiliary Monitoring and Control System (AMC), which automatically closes the SPS-P supply valve.", "AMC automatically trips the SPS-P pumps.", "NNA sends a signal to the Utility Monitoring and Control System (UMC), which automatically closes NI HVAC dampers to isolate the SPS cells."], NNA2),
 ], checks=[
  dict(eo="", q="At Natrium, which system automatically trips the SPS-P pumps on a sodium leak detection signal from NNA?", o=["The Auxiliary Monitoring and Control System (AMC)", "The Reactor Protection System", "The Utility Monitoring and Control System (UMC)", "The Nuclear Island Fire Water Distribution System"], a=0, x="NNA sends the leak detection signal to AMC, and AMC automatically trips the SPS-P pumps.", p="trip", place=ANC),
 ]),
], [], [
 ("Name five ways of detecting sodium leaks listed in the NRC training slides.", "Smoke detectors, contact detectors (spark plugs), cable detectors, aerosol monitors and inspections.", "contact"),
 ("What devices does Natrium SPS leak detection use?", "Devices such as wire and cable, spark plugs, and mutual inductance type sensors.", "sps", ANC),
 ("What decides the type of sodium leak detector used at Natrium?", "The needs of the installation location and configuration.", "type", ANC),
 ("Where is smoke detection used for Natrium sodium leaks?", "In areas where sodium reactions may occur, such as Intermediate Air Cooling stacks.", "smoke", ANC),
 ("How is sodium buildup in the RV-GV annulus gas monitored?", "Through absolute filter differential pressure changes, oxygen concentrations and radiation levels.", "ann", ANC),
], [
 ("Leak detection matters because primary sodium is radioactive, sodium burns in air, and sodium loss could impair heat transport.", OV),
 ("Detection methods include smoke, contact (spark plug), cable and aerosol detectors, and inspections.", OP),
 ("In a spark plug type detector, leaking fluid completes an open circuit.", KC),
 ("Natrium detectors will generally use conductivity detection with a self-test function, and they alarm in the main control room.", DET),
 ("Detection of small leaks helps prevent large leaks from occurring.", FP2),
 ("NNA signals drive automatic SPS-P valve closure, pump trip and cell damper closure.", NNA2),
], [
 ("Source decision", "The Word file holds only two knowledge checks in text. By decision of Nov 5, 2026 this lesson also uses the NRC training slides and the PSAR.", KC),
 ("Objectives", "The Word file gives only the title TLO 6: Sodium Leak Detectors, with no enabling objectives. No objectives were written for it.", T),
 ("Missing text", "Knowledge Check 2 has an answer of Low and feedback that the ammeter will read lower than normal, but its question is not in the text. It is left off.", W("1.6 Knowledge Check 2")),
 ("Picture content", "Slides 1.2, 1.3 and 1.4 have no text and are not used.", W("1.4 Failure modes")),
], word=[("1.5 Knowledge Check 1", "Spark plug type detector operation")], word_file=F, objectives=OBJ)
