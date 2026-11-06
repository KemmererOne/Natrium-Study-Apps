// Quiz questions moved out because no supporting quote was found in the Included sources (2026-11-02 re-check). Same format as quiz/questions.js.
const NO_QUOTE_QS = [
  { t: "Reactor theory", topic: "Reactivity", q: "Why is a control rod's worth greatest when it sits in the region of highest neutron flux?",
    o: ["Neutrons there are most likely to be absorbed by the rod", "Fuel burnup is highest there", "Coolant flow is lowest there", "Decay heat is generated only there"], a: 0,
    x: "A rod removes neutrons in proportion to the flux at its location, so it has the most effect where the flux is highest.",
    src: "DOE-HDBK-1019 (Nuclear Physics and Reactor Theory), summary sections." },
  { t: "Heat transfer", topic: "Heat transfer", q: "Liquid sodium has a very low Prandtl number. What does that imply for heat transfer?",
    o: ["Momentum diffuses much faster than heat", "Heat diffuses much faster than momentum, so conduction dominates", "Heat transfer is impossible", "Flow is always laminar"], a: 1,
    x: "Liquid metals conduct heat very well relative to their momentum diffusion. Correlations for them differ from those for water and gases.",
    src: "DOE-HDBK-1012 (Thermodynamics, Heat Transfer and Fluid Flow), summary sections." },
  { t: "Heat transfer", topic: "Heat transfer", q: "Sodium's high thermal conductivity and heat capacity mainly help the plant by:",
    o: ["Increasing neutron leakage", "Slowing temperature changes during transients, giving thermal inertia", "Reducing the need for instrumentation", "Eliminating decay heat"], a: 1,
    x: "Large heat capacity and good conduction spread heat quickly and damp rapid temperature swings, which buys operators time during transients.",
    src: "DOE-HDBK-1012 (Thermodynamics, Heat Transfer and Fluid Flow), summary sections." }
];
