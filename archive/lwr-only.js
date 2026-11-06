// Flashcards moved out of the sodium fast reactor deck because they depend on thermal-spectrum physics. Same format as flashcards/cards.js: [category, question, answer, source].
const LWR_CARDS = [
  ["Neutrons", "What is a thermal neutron?", "A neutron in energy equilibrium with the surrounding material, so its kinetic energy is about that of the medium.", "DOE-HDBK-1019"],
  ["Neutrons", "What is the resonance absorption region, and why does it matter?", "Roughly 1 eV to 1 keV, where U-238 absorbs strongly at resonance peaks. Resonance absorption reduces neutrons available for fission.", "NRC bank 292001"],
  ["Neutrons", "What shape does a thermal reactor's neutron flux spectrum have in the intermediate region?", "Roughly 1/E, because neutrons lose a constant fraction of energy per collision and pile up at lower energies.", "DOE-HDBK-1019"],
  ["Neutrons", "List the three desirable characteristics of a moderator.", "Large scattering cross section, small absorption cross section, and large energy loss per collision.", "DOE-HDBK-1019"],
  ["Neutrons", "What is the average logarithmic energy decrement?", "The average change in the logarithm of neutron energy per collision.", "DOE-HDBK-1019"],
  ["Life cycle", "Write the six-factor formula.", "keff = epsilon x p x f x eta x P_FNL x P_TNL, where epsilon is fast fission, p resonance escape, f thermal utilization, eta reproduction, and P_FNL and P_TNL are fast and thermal non-leakage.", "DOE-HDBK-1019"],
  ["Life cycle", "What is resonance escape probability?", "The fraction of fast neutrons that slow to thermal energy without being absorbed in resonance peaks.", "DOE-HDBK-1019"],
  ["Life cycle", "What is the thermal utilization factor?", "The fraction of thermal neutrons absorbed in fuel, compared with absorption in all reactor materials.", "DOE-HDBK-1019"],
  ["Reactivity", "What is an Estimated Critical Position (ECP)?", "A reactivity balance that adds basic reactivity, direct and indirect xenon, and temperature reactivity to find the rod position for criticality.", "DOE-HDBK-1019"],
  ["Reactivity", "What is a burnable neutron poison?", "A material whose high absorption cross section converts to a much lower value by absorbing neutrons. It offsets excess fuel reactivity early in core life.", "DOE-HDBK-1019"],
  ["Reactivity", "What is chemical shim?", "A soluble poison circulated in the coolant. It has a spatially uniform effect and can be adjusted during operation.", "DOE-HDBK-1019"],
  ["Reactivity", "What advantage do fixed burnable poisons have over chemical shim?", "They can shape the flux profile and do not affect the moderator temperature coefficient.", "DOE-HDBK-1019"],
  ["Fission products", "How is Xe-135 produced in a reactor?", "Directly as a fission product, and from the decay of I-135.", "DOE-HDBK-1019"],
  ["Fission products", "What happens to Xe-135 concentration immediately after a power increase?", "It decreases first, because burnout rises. It reaches a minimum about 5 hours later, then rises to a higher equilibrium.", "DOE-HDBK-1019"],
  ["Fission products", "At what flux does equilibrium Xe-135 peak?", "About 10^15 neutrons per cm^2 per second.", "DOE-HDBK-1019"],
  ["Fission products", "Does equilibrium Sm-149 depend on power?", "No. Sm-149 equilibrium is independent of power level. After shutdown it rises from Pm-149 decay.", "DOE-HDBK-1019"],
  ["Fission products", "When does He-3 become a significant poison?", "When significant tritium is left in the reactor during shutdowns lasting several months or more.", "DOE-HDBK-1019"],
  ["Heat generation", "What is core power directly proportional to?", "The fission rate of the fuel and the thermal neutron flux present.", "DOE-HDBK-1012"],
  ["Reactivity", "Why are resonance absorbers sometimes preferred to thermal absorbers for control rods?", "They have a larger area of influence and give a flatter flux profile.", "DOE-HDBK-1019/2-93, Control Rods, NP-03 p. 58"]
];
