const steps = [
  {
    title: "Tunnista tilanne",
    body: "Valitse synteettinen tilanne, joka tuntuu tutulta.",
    actions: ["Kiireinen alku", "Yksi virhe jäi mieleen"]
  },
  {
    title: "Tee yksi valinta",
    body: "Mihin suuntaat huomiosi seuraavaksi?",
    actions: ["Hengitä ja rajaa", "Palaa tavoitteeseen"]
  },
  {
    title: "Jatka tai ohita",
    body: "Tässä demossa ei käsitellä henkilötietoja eikä tehdä diagnoosia.",
    actions: ["Jatka kartoituksen prototyyppiin", "Ohita"]
  }
];

export function nextIndex(current, length = steps.length) {
  return Math.min(current + 1, length - 1);
}

export function getStep(index) {
  return steps[index] ?? steps[0];
}

export function createState() {
  return { index: 0, choices: [] };
}

export function selectChoice(state, choice) {
  return {
    index: nextIndex(state.index),
    choices: [...state.choices, choice]
  };
}

function render(state) {
  const step = getStep(state.index);
  document.querySelector("#progress").textContent =
    `Vaihe ${state.index + 1} / ${steps.length}`;
  document.querySelector("#step-title").textContent = step.title;
  document.querySelector("#step-body").textContent = step.body;

  const actions = document.querySelector("#actions");
  actions.replaceChildren();

  step.actions.forEach((label) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.addEventListener("click", () => {
      state = selectChoice(state, label);
      document.querySelector("#status").textContent =
        `Valinta tallennettu synteettiseen istuntoon: ${label}`;
      render(state);
    });
    actions.append(button);
  });
}

if (typeof document !== "undefined") {
  let state = createState();
  render(state);
}
