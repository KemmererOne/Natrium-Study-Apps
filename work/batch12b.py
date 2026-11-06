#!/usr/bin/env python3
"""Batch 12, part 2: NA-02, built from Plugging Temperature Indicators.docx, with a Natrium page from the PSAR by decision of Nov 5, 2026. There is no handbook module."""
import sys; sys.path.insert(0, "work")
import lessonlib
from lessonlib import build
lessonlib.ROTATE = True
F = "Plugging Temperature Indicators.docx"
W = lambda s: f"Word: {F}, slide {s}"
T1, T2, TH, PT, CT, ADV = W("1.1 TLO 7: Sodium Purity Monitors"), W("1.2 TLO 7: Enabling Objectives"), W("1.5 Sodium Purity Monitoring Theory"), W("1.7 Plugging Temperature Indicator"), W("1.8 Cold Trap"), W("1.11 Advantages of PTI Fill-in-blank")
SENS = ("Components", "Sensors and Detectors")
AUX = ("PSAR design basis", "PSAR: Reactor Auxiliary Systems")
PP = "PSAR Rev 1, ML25276A288, Sec. 7.2.4.3.1, p. 7.2-51"
eo = lambda n, t: dict(number=str(n), text=t, items=[], cite=T2)
OBJ = [dict(number="TLO 7", text="Sodium Purity Monitors", items=[], cite=T1, enabling=[
 eo(1, "Describe the theory of operation of a sodium purity monitor."),
 eo(2, "Describe the basic construction of a plugging temperature indicator."),
 eo(3, "List the advantages of using plugging temperature indicators.")])]

build("NA-02", SENS, [
 ("corr", "The purity of the coolant plays a critical role in preventing corrosion of structural materials within the reactor system", "x", TH),
 ("ht", "maintaining purity facilitates optimal heat transfer efficiency", "x", TH),
 ("act", "uncontaminated sodium coolant minimizes the risk of material activation by neutron irradiation", "x", TH),
 ("stable", "a pure coolant contributes to predictable and stable reactor performance", "x", TH),
 ("flow", "When the flow rate decrease is detected by a flow meter the temperature of the sodium is noted.", "x", TH),
 ("send", "Impurities in the sodium will begin to precipitate on an orifice.", "x", TH),
 ("more", "The more the impurities the higher the temperature a decrease in flow rate will be detected.", "x", TH),
 ("cryst", "impurities will precipitate out of solution and begin to crystallize", "x", PT),
 ("rise", "As impurities build up in the coolant, the temperature at which crystallization occurs rises.", "x", PT),
 ("orif", "A plugging temperature indicator measures flow past an orifice.", "x", PT),
 ("mon", "Monitoring changes in the plugging temperature helps determine the level of impurities present in the sodium coolant.", "x", PT),
 ("ctuse", "Plugging temperature indicators can be used to determine the effectiveness of cold traps, and when they should be placed in service if not operated continuously.", "x", CT),
 ("spec", "does not discriminate the species of the plugging impurity", "x", ADV),
 ("a1", "on-line systems avoid contamination of the sample by air or other foreign agents", "x", ADV),
 ("a2", "on-line systems are not subject to analytical errors caused by segregation of impurities to the walls of a container during cooling of sodium samples", "x", ADV),
 ("a4", "eliminate the need for transporting radioactive samples or for using remote handling equipment during analysis", "x", ADV),
 ("a6", "the precision of a measurement is more readily obtained from a continuous or semi-continuous signal", "x", ADV),
 ("ebr", "have been used since the initial fill of sodium in the primary and secondary systems of EBR-II in 1963", "x", ADV),
 ("key", "The key process indicator for sodium purity is the saturation temperature which correlates directly with impurity concentration.", "x", PP),
 ("corr2", "PTI operation requires correlating flow rate of the sodium through a plugging orifice at a given temperature to the impurity concentrations.", "x", PP),
 ("above", "The SPS operates with the sodium above this saturation temperature to avoid plugging passageways in the system.", "x", PP),
 ("traps", "The saturation temperature is also used in conjunction with the traps to adjust processing temperatures for impurity removal.", "x", PP),
 ("cu", "The source of the copper was found to be the exposed bus bars of the primary auxiliary pump.", "x", ADV),
], [
 dict(title="Why sodium purity is monitored", eo=["1"], body=[
  ("q", "corr"),
  ("q", "ht"),
  ("q", "act"),
  ("p", "That reduces radiation exposure hazards for personnel.", TH),
  ("q", "stable"),
  ("p", "Plugging temperature indicators (PTIs) are one way to monitor sodium purity.", TH),
 ], checks=[
  dict(eo="1", q="Which of these is NOT a reason given for keeping sodium coolant pure in a sodium fast reactor?", o=["To reduce the cost of reactor operation", "To prevent corrosion of structural materials", "To enhance heat transfer efficiency", "To minimize the risk of material activation by neutron irradiation"], a=0, x="The lesson plan's reasons are preventing corrosion, enhancing heat transfer and minimizing material activation. Reducing the cost of reactor operation is the wrong choice on its question.", p="corr"),
 ]),
 dict(title="Theory of operation", eo=["1"], body=[
  ("p", "As sodium gets colder and approaches its freezing point:", PT),
  ("q", "cryst"),
  ("q", "rise"),
  ("p", "A PTI uses this to measure the level of impurities in the sodium. Sodium is sent through the PTI and gradually cooled.", TH),
  ("p", "When the sodium at the orifice reaches the impurity saturation temperature, impurities such as oxygen and hydrogen begin to precipitate and deposit on the orifice surface, which changes the sodium flow rate. The temperature measured when the flow begins to decrease is the plugging temperature.", PT),
  ("q", "more"),
  ("q", "mon"),
 ], checks=[
  dict(existing="Q265", eo="1"),
  dict(eo="1", q="At what moment is the plugging temperature measured in a plugging temperature indicator?", o=["When the flow past the orifice begins to decrease", "When the sodium first enters the indicator", "When the flow stops completely", "When the sodium reaches its boiling point"], a=0, x="The temperature measured at the moment the flow begins to decrease is the plugging temperature.", p="flow"),
 ]),
 dict(title="Basic construction", eo=["2"], body=[
  ("q", "orif"),
  ("q", "send"),
  ("q", "flow"),
  ("p", "So the lesson plan's text names two parts: the orifice, where the impurities deposit, and the flow meter, which detects the flow decrease. The diagrams of the rest of the indicator are pictures in the lesson plan and are not used.", TH),
 ], checks=[
  dict(eo="2", q="Which device detects the flow decrease in a plugging temperature indicator?", o=["A flow meter", "A pressure relief valve", "A cesium trap", "An ion chamber"], a=0, x="When a flow meter detects the flow rate decrease, the temperature of the sodium is noted.", p="flow"),
 ]),
 dict(title="Use with cold traps", eo=[], body=[
  ("q", "ctuse"),
  ("p", "A cold trap cools a small fraction of the main flow to just above the sodium freezing point, so impurities precipitate and adhere to the mesh packing and walls. The clean sodium returns to the main loop.", CT),
 ], checks=[
  dict(eo="1", q="How can plugging temperature indicators support cold trap operation?", o=["They show cold trap effectiveness and when a trap should be placed in service", "They provide the cooling flow to the trap", "They regenerate a saturated trap", "They remove cesium ahead of the trap"], a=0, x="PTIs can be used to determine the effectiveness of cold traps, and when they should be placed in service if not operated continuously.", p="ctuse"),
 ]),
 dict(title="PTIs at Natrium", eo=["1"], body=[
  ("p", "The Natrium Sodium Processing System (SPS) uses plugging temperature indicators. The PSAR describes them this way:", PP),
  ("q", "key"), ("q", "corr2"), ("q", "above"), ("q", "traps"),
 ], checks=[
  dict(eo="1", q="Why does the Natrium Sodium Processing System operate with the sodium above the saturation temperature?", o=["To avoid plugging passageways in the system", "To keep the sodium from boiling", "To increase cesium removal", "To reduce pump power"], a=0, x="The SPS operates with the sodium above this saturation temperature to avoid plugging passageways in the system.", p="above", place=AUX),
 ]),
 dict(title="Advantages of PTIs", eo=["3"], body=[
  ("p", "A PTI has one limit. It:", ADV),
  ("q", "spec"),
  ("p", "It does detect the impurity's presence, and it offers these principal advantages over grab sampling:", ADV),
  ("q", "a1"),
  ("q", "a2"),
  ("p", "PTI analysis is not delayed by radioactive decay periods before a sample can be removed, which were up to five days on the EBR-II primary sodium system.", ADV),
  ("p", "PTIs also:", ADV),
  ("q", "a4"),
  ("p", "PTIs give a continuous measurement, or one that can be repeated at short intervals. This helps identify the cause of unexpected changes in impurity concentrations after operations such as reactor shutdown, cold trap isolation or fuel handling.", ADV),
  ("q", "a6"),
 ], checks=[
  dict(existing="Q266", eo="3"),
  dict(eo="3", q="Why are on-line plugging temperature indicators free from the error of impurity segregation seen in grab samples?", o=["No sample cools in a container, where impurities can segregate to the walls", "The sample is diluted with argon first", "The sample is held for five days first", "The indicator identifies each impurity species"], a=0, x="On-line systems are not subject to analytical errors caused by segregation of impurities to the walls of a container during cooling of sodium samples.", p="a2"),
 ]),
 dict(title="EBR-II experience", eo=[], body=[
  ("p", "At EBR-II, PTIs:", ADV),
  ("q", "ebr"),
  ("p", "From 1964 to 1967 they were the principal indicators of sodium purity. The practice was to run without cold trapping until the plugging temperature exceeded 149°C, then run the cold trap until it fell below 107°C, then shut the trap off again.", ADV),
  ("p", "More-or-less continuous cold trap operation began in 1967, with plugging temperature measurements made once per day.", ADV),
  ("p", "Copper in the primary sodium was discovered in 1967 by the irreversible plugging of the PTI.", ADV),
  ("q", "cu"),
 ], checks=[
  dict(eo="3", q="At EBR-II, what was found to be the source of the copper that irreversibly plugged the PTI in 1967?", o=["Exposed bus bars of the primary auxiliary pump", "Heat exchanger tubing", "Fuel cladding", "The cold trap mesh"], a=0, x="The source of the copper was found to be the exposed bus bars of the primary auxiliary pump.", p="cu"),
 ]),
], [
 dict(title="Reading a PTI during the EBR-II years", eo="1", page=ADV,
  problem="It is 1965 at EBR-II, the cold trap is off, and the indicated plugging temperature has just exceeded 149°C. Using the practice of those years, what happens next?",
  steps=["A plugging temperature above 149°C meant it was time to operate the cold trap.", "The cold trap ran until the indicated plugging temperature was below 107°C.", "The cold trap was then shut off again."],
  answer="Run the cold trap until the plugging temperature is below 107°C, then shut it off."),
], [
 ("What part of a plugging temperature indicator do impurities deposit on?", "An orifice. The deposit reduces the flow, which a flow meter detects.", "send"),
 ("What can plugging temperature indicators tell you about a cold trap?", "How effective it is, and when it should be placed in service if it is not operated continuously.", "ctuse"),
 ("How did EBR-II discover copper in its primary sodium?", "By the irreversible plugging of the PTI in 1967. The source was the exposed bus bars of the primary auxiliary pump.", "cu"),
 ("Since when have PTIs been used at EBR-II?", "Since the initial fill of sodium in the primary and secondary systems in 1963.", "ebr"),
 ("What is the key process indicator for sodium purity at Natrium?", "The saturation temperature, which correlates directly with impurity concentration.", "key", AUX),
 ("How do on-line PTIs avoid sample contamination?", "On-line systems avoid contamination of the sample by air or other foreign agents.", "a1"),
], [
 ("Sodium purity protects against corrosion, keeps heat transfer efficient, limits activation and supports stable performance.", TH),
 ("As impurities build up, the temperature at which crystallization occurs rises.", PT),
 ("A PTI cools sodium past an orifice. The temperature when flow begins to decrease is the plugging temperature.", PT),
 ("A PTI detects the presence of a plugging impurity but not its species.", ADV),
 ("PTIs avoid sample contamination, segregation errors, decay delays and sample transport, and they can measure continuously.", ADV),
 ("PTIs show how effective cold traps are and when to place them in service.", CT),
], [
 ("Word typo", "Slides 1.11 and 1.12 print the Fahrenheit values as 3O0°F and 22S°F, which look like scanning errors. Only the Celsius values 149°C and 107°C are shown.", ADV),
 ("Coverage", "Objective 2 asks for basic construction, but the construction is in pictures. The page gives only the orifice and flow meter from the text. The PSAR page added by decision of Nov 5, 2026 does not describe more parts.", TH),
 ("Duplicate", "Slide 1.9 repeats the notes of slide 1.7, and slide 1.12 repeats slide 1.11. Each is cited once.", W("1.9 PTI in a Purification Loop")),
 ("Draft note", "Slide 1.3 says a short essay quiz is still to be developed, and slide 1.7 lists an image as needing creation. SOURCES.md lists the file as an approved lesson plan, so no Draft source tag is applied.", W("1.3 Purity Monitors")),
 ("Multiple response", "Slide 1.4 is a select-all question. Its wrong choice is reused as a single-answer check.", TH),
], word=[("1.5 Sodium Purity Monitoring Theory", "Why purity matters and how a PTI works"), ("1.7 Plugging Temperature Indicator", "Plugging temperature"), ("1.8 Cold Trap", "Use with cold traps"), ("1.11 Advantages of PTI Fill-in-blank", "Advantages and EBR-II experience")],
 word_file=F, objectives=OBJ)
