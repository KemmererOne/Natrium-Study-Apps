# Terminal objective coverage

Checked 2026-11-04. This report maps each terminal objective in the fundamentals documents to quiz questions (Q) and flashcards (C). IDs are the permanent id stored on each item in quiz/questions.js and flashcards/cards.js, and they show on the item in each app.

## Result

- **Objectives checked:** 138 (74 from the DOE handbooks, 64 from the lesson plans).
- **Coverage now:** every objective has at least one quiz question and one flashcard.
- **Added for gaps:** 32 quiz questions and 25 flashcards. Each is logged with its source quote in CHANGELOG.md.
- **Topic placement:** new items use the existing 26 fundamentals topics. Chemistry items are in Demineralizers and Ion Exchangers and print-reading items are in Valves or Controllers and Positioners, the same as earlier handbook items.

## How the check worked

- **DOE handbooks:** objectives came from each module's OBJECTIVES pages.
- **Lesson plans:** most objective slides are pictures, so their text was read with on-device OCR. Wording below is cleaned up where OCR was garbled.
- **Matching:** items were matched by source module and keywords. Every objective with two or fewer matches on either side was read by hand, and false matches were removed. Objectives with more matches were only spot-checked, so a few counts may be high.
- **Depth:** this checks that each objective has items, not that an item tests every enabling objective under it.

## Open points

- **Unregistered document:** `MG Complete Lesson Plan.pdf` (Motors and Generators, USO-IT-I-FND-MG) is not in SOURCES.md, so nothing was taken from it. It has two terminal objectives on AC motor theory and AC motor operation. DOE-1011-V4 items cover AC motors, but they were not checked against this plan's objectives.
- **Partly legible objective:** Valve Fundamentals TLO 2 is partly hidden on its slide. LP-V2 uses a reconstruction based on ELOs 2.1 to 2.5.
- **Headings only:** Breakers, Relays, and Disconnects lists its terminal objectives as three topic headings, not full statements.
- **Calculation objectives:** several handbook objectives ask for calculations (for example pH, reaction rate, heat balance). The new items test the definitions and relationships in the sources, not worked calculations.

## DOE handbooks

| ID | Handbook | Terminal objective | Quiz | Cards | Sample items |
|---|---|---|---:|---:|---|
| CP-01 | 1010 Classical Physics | Given appropriate conversion tables, CONVERT between English and SI system units of measurement. | 1 | 2 | Q486; C433, C599 |
| CP-02 | 1010 | Using vectors, DETERMINE the net force acting on an object. | 2 | 1 | Q412, Q487; C600 |
| CP-03 | 1010 | APPLY Newton's laws of motion to a body. | 2 | 1 | Q410, Q411; C434 |
| CP-04 | 1010 | From memory, APPLY the principles of force to stationary or moving bodies. | 4 | 1 | Q412, Q413, Q414, Q415; C601 |
| CP-05 | 1010 | Given necessary information about a system, CALCULATE the work performed and/or power produced or used by that system. | 2 | 6 | Q488, Q489; C427, C428, C429, C430 (+2) |
| ES-01 | 1011 V1 | Given a simple electrical circuit, APPLY basic electrical theory fundamental principles to describe circuit operation. | 3 | 6 | Q236, Q416, Q417; C250, C270, C439, C442 (+2) |
| ES-02 | 1011 V1 | Using the rules associated with basic DC circuit characteristics, ANALYZE various DC circuits to find resistances, currents, and voltages at any given point within the circuit. | 3 | 6 | Q418, Q419, Q420; C435, C436, C437, C438 (+2) |
| ES-03 | 1011 V2 | Using the rules associated with inductors and capacitors, DESCRIBE the characteristics of these elements when they are placed in a DC circuit. | 2 | 3 | Q421, Q422; C602, C603, C604 |
| ES-04 | 1011 V2 | DESCRIBE the operating characteristics of a lead-acid battery to include methods of voltage production, state of charge, and hazards associated with storage batteries. | 2 | 2 | Q425, Q426; C447, C448 |
| ES-05 | 1011 V2 | Given the type and application of a direct current (DC) generator, DESCRIBE the operating characteristics of that generator including methods of voltage production, advantages of each type, and voltage-vs-load characteristics. | 1 | 3 | Q423; C442, C443, C444 |
| ES-06 | 1011 V2 | Given the type and application of a DC motor, DESCRIBE the operating characteristics of that motor to include methods of speed variation, advantages of each type, and torque vs speed characteristics. | 1 | 3 | Q424; C444, C445, C446 |
| ES-07 | 1011 V3 | Given an alternating current (AC) waveform, DESCRIBE the relationship between average and RMS values of voltage and current, and the angular velocity within that waveform. | 1 | 2 | Q490; C605, C606 |
| ES-08 | 1011 V3 | Using the rules associated with inductors and capacitors, DESCRIBE the characteristics of these elements when they are placed in an AC circuit. | 10 | 4 | Q17, Q18, Q52, Q57 (+6); C42, C43, C161, C453 |
| ES-09 | 1011 V3 | Given an AC single-phase or three-phase circuit, DESCRIBE the power characteristics in the circuit. | 3 | 5 | Q279, Q428, Q438; C266, C267, C268, C454 (+1) |
| ES-10 | 1011 V3 | Given the type and application of an AC generator, DESCRIBE the operating characteristics of that generator including methods of voltage production, advantages of each type, and methods for paralleling. | 4 | 4 | Q279, Q429, Q430, Q431; C449, C450, C451, C452 |
| ES-11 | 1011 V3 | Given a block diagram, DESCRIBE the operation of a typical voltage regulator. | 1 | 1 | Q432; C455 |
| ES-12 | 1011 V4 | Given the type and application of an AC motor, DESCRIBE the operating characteristics of that motor including methods of torque production and advantages of that type. | 3 | 3 | Q436, Q437, Q438; C456, C457, C458 |
| ES-13 | 1011 V4 | Given the type of a transformer, DESCRIBE the operating characteristics and applications for that transformer type. | 1 | 3 | Q451; C271, C459, C479 |
| ES-14 | 1011 V4 | Given a piece of test equipment or measuring device, DESCRIBE the use of that piece of electrical equipment, to include the meter movement, electrical parameter measurement, and connection of the device to a circuit. | 4 | 9 | Q263, Q264, Q280, Q439; C247, C248, C249, C250 (+5) |
| ES-15 | 1011 V4 | Given the functional characteristics of an AC power source and the intended load, DESCRIBE the necessary components and the wiring scheme to provide a safe Electrical Distribution System. | 8 | 7 | Q270, Q274, Q275, Q278 (+4); C263, C343, C462, C463 (+3) |
| HT-01 | 1012 V1 | Given operating conditions of a system, EVALUATE the thermodynamic state of the system. | 21 | 21 | Q38, Q46, Q58, Q59 (+17); C55, C64, C81, C82 (+17) |
| HT-02a | 1012 V2 | Given the operating conditions of a thermodynamic system and the necessary formulas, EVALUATE the heat transfer processes which are occurring. | 7 | 8 | Q20, Q44, Q60, Q61 (+3); C45, C47, C48, C111 (+4) |
| HT-02b | 1012 V2 | Given the operating conditions of a typical nuclear reactor, DESCRIBE the heat transfer processes which are occurring. | 16 | 21 | Q5, Q20, Q45, Q46 (+12); C54, C55, C56, C57 (+17) |
| HT-03 | 1012 V3 | Given conditions affecting the fluid flow in a system, EVALUATE the effects on the operation of the system. | 25 | 27 | Q4, Q19, Q33, Q35 (+21); C58, C59, C75, C77 (+23) |
| IC-01 | 1013 V1 | Given a temperature instrument, RELATE the associated fundamental principles, including possible failure modes, to that instrument. | 4 | 8 | Q246, Q247, Q256, Q389; C234, C235, C237, C238 (+4) |
| IC-02 | 1013 V1 | Given a pressure instrument, RELATE the fundamental principles, including possible failure modes, to that specific instrument. | 1 | 7 | Q245; C230, C231, C232, C233 (+3) |
| IC-03 | 1013 V1 | Given a level instrument, RELATE the associated fundamental principles, including possible failure modes, to that instrument. | 6 | 5 | Q267, Q268, Q269, Q315 (+2); C257, C259, C404, C405 (+1) |
| IC-04 | 1013 V1 | Given a flow instrument, RELATE the associated fundamental principles, including possible failure modes, to that instrument. | 9 | 8 | Q120, Q265, Q310, Q325 (+5); C76, C85, C252, C328 (+4) |
| IC-05 | 1013 V1 | Given a position indicating instrument, RELATE the associated fundamental principles, including possible failure modes, to that instrument. | 4 | 9 | Q282, Q392, Q393, Q438; C251, C269, C270, C271 (+5) |
| IC-06a | 1013 V2 | SUMMARIZE radiation protection principles to include definition of terms, types of radiation, and the basic operation of a gas-filled detector. | 2 | 2 | Q491, Q492; C409, C410 |
| IC-06b | 1013 V2 | SUMMARIZE the principles of operation of various types of radiation detectors. | 9 | 6 | Q238, Q239, Q240, Q360 (+5); C219, C363, C364, C411 (+2) |
| IC-06c | 1013 V2 | SUMMARIZE the operation of typical source, intermediate, and power range nuclear instruments. | 4 | 5 | Q244, Q294, Q360, Q399; C227, C228, C290, C368 (+1) |
| IC-07 | 1013 V2 | Given a process control system, SUMMARIZE the operation of the system based on changing system inputs. | 17 | 15 | Q17, Q18, Q26, Q108 (+13); C41, C43, C163, C186 (+11) |
| CH-01a | 1015 V1 | Without references, DESCRIBE the characteristics of an atom. | 2 | 3 | Q493, Q494; C607, C608, C609 |
| CH-01b | 1015 V1 | Given an incomplete chemical equation, BALANCE the equation by the method presented. | 1 | 1 | Q494; C608 |
| CH-01c | 1015 V1 | Given sufficient information about a solution, CALCULATE the pH and pOH of the solution. | 5 | 1 | Q253, Q444, Q445, Q447 (+1); C609 |
| CH-02 | 1015 V1 | Without references, DESCRIBE the causes and effects of corrosion on metals and the type of chemistry used in a plant to minimize corrosion. | 7 | 9 | Q124, Q319, Q440, Q441 (+3); C133, C254, C327, C465 (+5) |
| CH-03 | 1015 V2 | Without references, DESCRIBE the effects of radiation on reactor water and methods of treatment for the products. | 3 | 1 | Q445, Q446, Q495; C476 |
| CH-04 | 1015 V2 | Without references, EXPLAIN the concept and application of ion exchange in water purification. | 9 | 8 | Q250, Q251, Q252, Q253 (+5); C243, C244, C245, C471 (+4) |
| CH-05 | 1015 V2 | Without references, DISCUSS the hazards associated with chemicals (liquid and gas) found in a nuclear plant. | 2 | 2 | Q496, Q497; C610, C611 |
| PR-01 | 1016 V1 | Given an engineering print, READ and INTERPRET the information contained in the title block, the notes and legend, the revision block, and the drawing grid. | 2 | 2 | Q498, Q499; C612, C613 |
| PR-02 | 1016 V1 | Given an engineering print, READ and INTERPRET facility engineering Piping and Instrument Drawings. | 1 | 2 | Q450; C477, C478 |
| PR-03 | 1016 V1 | Given an electrical print, READ and INTERPRET facility electrical diagrams and schematics. | 2 | 2 | Q451, Q452; C479, C480 |
| PR-04 | 1016 V2 | Given a block diagram, print, or schematic, IDENTIFY the basic component symbols as presented in this module. | 1 | 2 | Q500; C481, C482 |
| PR-05 | 1016 V2 | Given a logic diagram, READ and INTERPRET the diagrams. | 3 | 2 | Q453, Q454, Q455; C483, C484 |
| PR-06 | 1016 V2 | Given an engineering fabrication, construction, or architectural drawing, READ and INTERPRET basic dimensional and tolerance symbology, and basic fabrication, construction, or architectural symbology. | 1 | 1 | Q501; C614 |
| MS-01 | 1017 V1 | Without references, DESCRIBE the bonding and patterns that effect the structure of a metal. | 8 | 3 | Q97, Q124, Q265, Q379 (+4); C426, C470, C615 |
| MS-02 | 1017 V1 | Without references, DESCRIBE how changes in stress, strain, and physical and chemical properties effect the materials used in a reactor plant. | 6 | 7 | Q404, Q405, Q406, Q407 (+2); C394, C420, C421, C422 (+3) |
| MS-03 | 1017 V2 | Without references, DESCRIBE the importance of minimizing thermal shock (stress). | 3 | 6 | Q285, Q383, Q384; C279, C389, C390, C391 (+2) |
| MS-04 | 1017 V2 | Without references, EXPLAIN the importance of controlling heatup and cooldown rates of the primary coolant system. | 5 | 6 | Q379, Q380, Q381, Q382 (+1); C389, C391, C392, C393 (+2) |
| MS-05 | 1017 V2 | Without references, DESCRIBE the considerations commonly used when selecting material for use in a reactor plant. | 1 | 6 | Q386; C21, C171, C199, C396 (+2) |
| ME-01 | 1018 V1 | Without references, DESCRIBE the components and theory of operation for a diesel engine. | 1 | 4 | Q71; C94, C95, C127, C361 |
| ME-02 | 1018 V1 | Without references, DESCRIBE the purpose, construction, and principles of operation for each major type of heat exchanger: parallel flow, counter flow, and cross flow. | 11 | 19 | Q43, Q119, Q151, Q283 (+7); C50, C51, C52, C57 (+15) |
| ME-03a | 1018 V1 | Without references, DESCRIBE the purpose, construction, and principles of operation for centrifugal pumps. | 11 | 6 | Q40, Q66, Q67, Q68 (+7); C84, C122, C123, C126 (+2) |
| ME-03b | 1018 V1 | Without references, DESCRIBE the purpose, construction, and principle of operation for positive displacement pumps. | 6 | 2 | Q69, Q70, Q344, Q345 (+2); C124, C125 |
| ME-04 | 1018 V2 | Without references, DESCRIBE the construction and operation of a given type of valve, valve component, or valve actuator, as presented in this module. | 5 | 12 | Q41, Q42, Q72, Q73 (+1); C86, C87, C88, C90 (+8) |
| ME-05 | 1018 V2 | Without references, DESCRIBE the purpose, construction, and operation of miscellaneous mechanical components. | 10 | 10 | Q71, Q74, Q75, Q76 (+6); C90, C133, C134, C304 (+6) |
| NP-01a | 1019 V1 | Given sufficient information, DESCRIBE atoms, including components, structure, and nomenclature. | 8 | 15 | Q17, Q28, Q29, Q47 (+4); C1, C2, C3, C4 (+11) |
| NP-01b | 1019 V1 | Given necessary references, DESCRIBE the various modes of radioactive decay. | 7 | 5 | Q28, Q47, Q51, Q146 (+3); C6, C21, C96, C204 (+1) |
| NP-01c | 1019 V1 | Without references, DESCRIBE the different nuclear interactions initiated by neutrons. | 5 | 4 | Q27, Q48, Q291, Q506 (+1); C12, C14, C15, C99 |
| NP-01d | 1019 V1 | Without references, DESCRIBE the fission process. | 4 | 5 | Q49, Q104, Q289, Q568; C98, C99, C100, C239 (+1) |
| NP-01e | 1019 V1 | Without references, DESCRIBE how the various types of radiation interact with matter. | 6 | 7 | Q48, Q240, Q361, Q394 (+2); C12, C97, C285, C409 (+3) |
| NP-02a | 1019 V1 | Without references, EXPLAIN how neutron sources produce neutrons. | 3 | 5 | Q244, Q566, Q567; C16, C17, C35, C227 (+1) |
| NP-02b | 1019 V1 | Given the necessary information for calculations, EXPLAIN basic concepts in reactor physics and perform calculations. | 10 | 21 | Q36, Q52, Q57, Q103 (+6); C41, C78, C101, C102 (+17) |
| NP-02c | 1019 V1 | Without references, EXPLAIN the production process and effects on fission of prompt and delayed neutrons. | 16 | 17 | Q7, Q8, Q14, Q15 (+12); C20, C21, C22, C29 (+13) |
| NP-02d | 1019 V1 | Without references, DESCRIBE the neutron energy spectrum for the type of reactor presented in this module. | 4 | 5 | Q9, Q18, Q364, Q365; C22, C100, C155, C173 (+1) |
| NP-03a | 1019 V2 | Using appropriate references, DESCRIBE the neutron life cycle discussed in this module. | 10 | 7 | Q1, Q10, Q11, Q12 (+6); C24, C32, C33, C36 (+3) |
| NP-03b | 1019 V2 | From memory, EXPLAIN how reactivity varies with the thermodynamic properties of the moderator and the fuel. | 23 | 8 | Q5, Q17, Q18, Q25 (+19); C38, C40, C41, C42 (+4) |
| NP-03c | 1019 V2 | Without references, DESCRIBE the use of neutron poisons. | 4 | 6 | Q52, Q475, Q476, Q477; C106, C466, C467, C504 (+2) |
| NP-03d | 1019 V2 | Without references, DESCRIBE the effects of fission product poisons on a reactor. | 9 | 11 | Q142, Q467, Q468, Q469 (+5); C174, C179, C206, C497 (+7) |
| NP-03e | 1019 V2 | Without references, DESCRIBE how control rods affect the reactor core. | 12 | 17 | Q52, Q53, Q55, Q132 (+8); C44, C102, C105, C160 (+13) |
| NP-04a | 1019 V2 | Given the necessary information and equations, EXPLAIN how subcritical multiplication occurs. | 5 | 4 | Q24, Q292, Q293, Q294 (+1); C32, C35, C229, C288 |
| NP-04b | 1019 V2 | Given the necessary information and equations, DESCRIBE how power changes in a reactor that is near criticality. | 4 | 6 | Q22, Q54, Q139, Q377; C26, C28, C103, C104 (+2) |
| NP-04c | 1019 V2 | Without references, EXPLAIN the concepts concerning reactor startup, operation, and shutdown. | 11 | 18 | Q55, Q56, Q129, Q134 (+7); C28, C56, C57, C105 (+14) |

## Lesson plans

| ID | Lesson plan | Terminal objective | Quiz | Cards | Sample items |
|---|---|---|---:|---:|---|
| LP-ACG1 | AC Generator Theory | Describe the construction, operating characteristics, and limitations for an AC generator. | 5 | 8 | Q237, Q279, Q429, Q430 (+1); C215, C216, C217, C348 (+4) |
| LP-ACG2 | AC Generator Theory | Analyze the operating characteristics and interactions between two A/C generators operating in parallel. | 2 | 2 | Q429, Q432; C452, C455 |
| LP-ALIP | ALIP Pumps | TLO #4: Annular Linear Induction Pump (objectives 4.1 to 4.4) | 2 | 4 | Q236, Q237; C214, C215, C216, C217 |
| LP-BEC1 | Basic Energy Concepts | Describe the First and Second Laws of Thermodynamics as they apply to the secondary steam cycle. | 9 | 11 | Q58, Q59, Q312, Q410 (+5); C68, C110, C111, C314 (+7) |
| LP-BEC2 | Basic Energy Concepts | Describe the application of enthalpy in the monitoring of plant processes. | 5 | 5 | Q46, Q58, Q311, Q318 (+1); C55, C64, C310, C323 (+1) |
| LP-BRK1 | Breakers, Relays, Disconnects | Circuit Interrupting and Circuit Switching Devices Basics | 10 | 9 | Q133, Q270, Q271, Q272 (+6); C260, C261, C262, C263 (+5) |
| LP-BRK2 | Breakers, Relays, Disconnects | Circuit Breaker Indications and Operations | 5 | 2 | Q7, Q275, Q276, Q277 (+1); C616, C617 |
| LP-BRK3 | Breakers, Relays, Disconnects | Generator Paralleling Requirements | 1 | 2 | Q429; C251, C452 |
| LP-COLD | Cold Traps | Gain an understanding of cold traps, and the sodium coolant purification process in Sodium Fast Reactor (SFR) plants | 7 | 5 | Q124, Q319, Q320, Q321 (+3); C178, C256, C324, C325 (+1) |
| LP-CR1 | Control Rods | Explain the concept of control rod worth and how it is affected by control rod design and changes in core parameters. | 3 | 2 | Q53, Q375, Q376; C102, C380 |
| LP-CR2 | Control Rods | Explain how control rods affect plant operation and the core power distribution. | 2 | 3 | Q564, Q565; C107, C381, C382 |
| LP-CTRL | Controllers and Positioners | Describe the arrangement and operation of typical controllers and positioners within process control systems. | 9 | 10 | Q259, Q262, Q356, Q357 (+5); C357, C358, C359, C360 (+6) |
| LP-CTL | Core Thermal Limits | Describe the reason for reactor core thermal limits and factors affecting them. | 6 | 2 | Q45, Q46, Q241, Q242 (+2); C54, C55 |
| LP-DCS | Distributed Control Systems | Describe the purpose, construction, and principles of operation for Distributed Control Systems. | 7 | 2 | Q256, Q257, Q258, Q259 (+3); C618, C619 |
| LP-DNI | Delayed Neutron Importance | Explain the factors that affect reactor period and startup rate and their effect on reactor control. (TO 3) | 1 | 4 | Q22; C26, C28, C292, C385 |
| LP-DEM | Demineralizers | Explain demineralizer operation and its effect on power plant operations. | 6 | 5 | Q250, Q251, Q252, Q253 (+2); C243, C244, C245, C473 (+1) |
| LP-ETE | Electrical Test Equipment | Describe the basic operation of a voltmeter, ammeter, frequency detector (synchroscope), and a ground detector. | 3 | 8 | Q263, Q264, Q280; C247, C248, C249, C250 (+4) |
| LP-FFD | Failed Fuel Detectors | Describe the operation of neutron detectors and failed fuel detectors and conditions that effect their accuracy and reliability. (TLO 9) | 4 | 7 | Q125, Q238, Q239, Q240; C174, C175, C179, C219 (+3) |
| LP-FLOW | Flow Detectors | Describe the operation of flow detectors and conditions that affect their accuracy and reliability. (TO 4) | 8 | 9 | Q120, Q265, Q310, Q325 (+4); C76, C85, C252, C306 (+5) |
| LP-FSD1 | Fluid Statics and Dynamics | Explain the fundamental properties of fluids and closed fluid systems. | 8 | 6 | Q4, Q61, Q62, Q317 (+4); C116, C121, C150, C333 (+2) |
| LP-FSD2 | Fluid Statics and Dynamics | Describe laminar and turbulent flows. | 5 | 10 | Q34, Q63, Q70, Q305 (+1); C72, C73, C74, C117 (+6) |
| LP-FSD3 | Fluid Statics and Dynamics | Explain Bernoulli's equation then use it to determine fluid properties at different points in a system. | 3 | 3 | Q35, Q334, Q335; C75, C118, C126 |
| LP-FSD4 | Fluid Statics and Dynamics | Explain the various changes in fluid flow, their effect on plant operation, and methods of control. | 14 | 13 | Q19, Q36, Q38, Q42 (+10); C77, C80, C82, C87 (+9) |
| LP-FD | Fuel Depletion | Describe how fuel depletion and burnable poison concentration affect reactivity in a reactor core. | 10 | 8 | Q12, Q52, Q105, Q111 (+6); C206, C239, C240, C241 (+4) |
| LP-HX | Heat Exchangers | Describe the purpose, construction, and principles of operation for each major type of heat exchanger. | 10 | 19 | Q119, Q151, Q283, Q284 (+6); C50, C51, C52, C57 (+15) |
| LP-HT1 | Heat Transfer | Describe heat transfer mechanisms and associated terminology. | 10 | 6 | Q20, Q44, Q45, Q60 (+6); C45, C46, C47, C48 (+2) |
| LP-HT2 | Heat Transfer | Describe the heat transfer process in heat exchangers and factors that reduce heat transfer. | 5 | 5 | Q43, Q114, Q284, Q286 (+1); C50, C91, C276, C280 (+1) |
| LP-HT3 | Heat Transfer | Explain core thermal power and calculate its value using a simplified heat balance. | 2 | 2 | Q502, Q503; C620, C621 |
| LP-LVL | Level Detectors | Describe the operation of level detectors and conditions that affect their accuracy and reliability. (TO 3) | 6 | 4 | Q267, Q268, Q269, Q315 (+2); C257, C259, C404, C406 |
| LP-N1 | Neutrons | Describe atoms, including components, structure, and nomenclature. | 7 | 10 | Q17, Q28, Q47, Q148 (+3); C1, C2, C3, C4 (+6) |
| LP-N2 | Neutrons | Describe Mass Defect and Binding Energy and their relationship to one another. | 1 | 1 | Q31; C5 |
| LP-N3 | Neutrons | Describe neutron interactions with matter. | 4 | 3 | Q27, Q48, Q291, Q506; C12, C14, C15 |
| LP-N4 | Neutrons | Describe the process of nuclear fission and the types of material that can undergo fission. | 2 | 3 | Q49, Q568; C99, C239, C240 |
| LP-N5 | Neutrons | Explain the production of heat from fission. | 1 | 4 | Q290; C100, C282, C283, C296 |
| LP-N6 | Neutrons | Describe the production of prompt and delayed neutrons from fission as well as the differences between them. | 16 | 17 | Q7, Q8, Q14, Q15 (+12); C20, C21, C22, C29 (+13) |
| LP-N7 | Neutrons | Explain the relationship between neutron flux, microscopic and macroscopic cross-sections, and their effect on neutron reaction rates. | 3 | 2 | Q504, Q505, Q506; C622, C623 |
| LP-PTI | Plugging Temperature Indicators | Describe the operation of Plugging Temperature Indicators. (TLO 7) | 2 | 5 | Q265, Q266; C252, C253, C254, C255 (+1) |
| LP-POS | Position Indicators | Describe the operation of position detectors and conditions that affect their accuracy and reliability. | 6 | 6 | Q278, Q280, Q281, Q282 (+2); C269, C270, C271, C272 (+2) |
| LP-PWR | Power Changes | Explain the factors that affect reactor period and startup rate and their effect on reactor control. (TO 3) | 4 | 7 | Q22, Q54, Q139, Q377; C26, C28, C103, C104 (+3) |
| LP-PRES | Pressure Detectors | TLO 2: pressure detectors (Enabling objectives 1 to 3) | 4 | 10 | Q72, Q73, Q245, Q348; C85, C90, C130, C230 (+6) |
| LP-P1 | Pumps | Describe the purpose, construction, and principles of operation of centrifugal and jet pumps. | 11 | 6 | Q40, Q66, Q67, Q68 (+7); C84, C122, C123, C126 (+2) |
| LP-P2 | Pumps | Use centrifugal pump laws and curves to demonstrate the effect of changing pump speeds and pump configuration on pump flow, head, and power consumption. | 8 | 3 | Q39, Q40, Q66, Q136 (+4); C83, C84, C604 |
| LP-P3 | Pumps | Describe the purpose, construction, and principles of operation of positive displacement pumps. | 6 | 2 | Q69, Q70, Q344, Q345 (+2); C124, C125 |
| LP-RC1 | Reactivity Coefficients | Describe coolant, void, and pressure reactivity coefficients and how they are affected by changing reactor conditions. | 8 | 1 | Q5, Q57, Q109, Q142 (+4); C371 |
| LP-RC2 | Reactivity Coefficients | Describe the fuel temperature and power reactivity coefficients and how they are affected by changing reactor conditions. | 18 | 5 | Q17, Q18, Q26, Q57 (+14); C41, C42, C161, C373 (+1) |
| LP-RN1 | Reactor Neutrons | Describe reactivity, Keff, Kexcess, and shutdown margin. | 13 | 13 | Q1, Q10, Q11, Q12 (+9); C24, C32, C33, C36 (+9) |
| LP-RN2 | Reactor Neutrons | Describe how core design in a fast reactor affects reactivity. | 71 | 43 | Q5, Q6, Q9, Q17 (+67); C22, C24, C87, C132 (+39) |
| LP-SD1 | Sensors and Detectors Part 2 | Describe the operation of radiation detectors and conditions which effect their accuracy and reliability. | 9 | 6 | Q238, Q239, Q240, Q360 (+5); C219, C363, C364, C411 (+2) |
| LP-SD2 | Sensors and Detectors Part 2 | Describe the operation of personal radiation monitoring instruments and conditions which effect their accuracy and reliability. | 2 | 3 | Q507, Q508; C365, C366, C367 |
| LP-SD3 | Sensors and Detectors Part 2 | Describe the operation of neutron and failed fuel detectors and conditions which effect their accuracy and reliability. | 5 | 6 | Q125, Q238, Q239, Q240 (+1); C174, C179, C219, C220 (+2) |
| LP-SLD | Sodium Leak Detectors | TLO 6: Sodium Leak Detectors (theory of operation; basic construction of the contact detector) | 1 | 1 | Q509; C218 |
| LP-SN | Source Neutrons | Describe intrinsic and installed neutron sources and their contribution to source neutron strength over core life. | 3 | 5 | Q244, Q566, Q567; C16, C17, C35, C227 (+1) |
| LP-SCM | Subcritical Multiplication | Describe subcritical multiplication for a nuclear reactor and describe how subcritical multiplication affects reactor operation. (TO 2) | 5 | 5 | Q24, Q292, Q293, Q294 (+1); C32, C34, C35, C229 (+1) |
| LP-TEMP | Temperature Detectors | Describe the operation of temperature detectors and conditions that effect their accuracy and reliability. | 4 | 8 | Q246, Q247, Q256, Q389; C234, C235, C236, C237 (+4) |
| LP-TH1 | Thermal Hydraulics | Describe the basic reactor core thermal hydraulic properties. | 3 | 2 | Q114, Q305, Q306; C47, C305 |
| LP-TH2 | Thermal Hydraulics | Explain natural circulation and methods to enhance its effectiveness. | 9 | 13 | Q4, Q33, Q65, Q136 (+5); C58, C59, C120, C150 (+9) |
| LP-TUP1 | Thermo Units and Properties | Describe thermodynamic properties and methods of measuring intensive and extensive properties. | 5 | 5 | Q313, Q314, Q316, Q464 (+1); C60, C61, C64, C317 (+1) |
| LP-TUP2 | Thermo Units and Properties | Explain the concepts of heat, work, and energy. | 6 | 10 | Q27, Q35, Q289, Q290 (+2); C64, C65, C75, C93 (+6) |
| LP-TD1 | Thermodynamics | Apply the first law of thermodynamics to analyze thermodynamic systems and processes. | 14 | 11 | Q41, Q42, Q58, Q59 (+10); C68, C70, C86, C87 (+7) |
| LP-TD2 | Thermodynamics | Apply the second law of thermodynamics to analyze real and ideal systems and components. | 7 | 10 | Q3, Q58, Q59, Q312 (+3); C69, C110, C111, C312 (+6) |
| LP-V1 | Valve Fundamentals | Identify the major types of valves and actuators and applications for each, and identify valve parts and their functions. | 4 | 10 | Q41, Q42, Q73, Q348; C85, C86, C87, C90 (+6) |
| LP-V2 | Valve Fundamentals | Explain how to operate valves, and required equipment operating precautions. (partly illegible on slide; ELOs 2.1 to 2.5) | 4 | 7 | Q282, Q350, Q359, Q450; C90, C271, C272, C273 (+3) |
| LP-V3 | Valve Fundamentals | Explain the operation of safety valves and relief valves and analyze the response of these valves in system applications. | 3 | 5 | Q510, Q511, Q512; C89, C125, C349, C350 (+1) |
| LP-VFD | Variable Frequency Drives | Given a variable frequency drive (VFD), EXPLAIN the principles of operation in accordance with electrical theory (objectives 1 to 4) | 5 | 2 | Q351, Q352, Q353, Q354 (+1); C354, C356 |
