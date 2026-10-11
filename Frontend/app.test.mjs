import assert from "node:assert/strict";
import test from "node:test";
import {
  createState,
  getStep,
  nextIndex,
  selectChoice
} from "./app.mjs";

test("state starts from the first step", () => {
  const state = createState();
  assert.equal(state.index, 0);
  assert.equal(getStep(state.index).title, "Tunnista tilanne");
});

test("choice advances and remains traceable", () => {
  const state = selectChoice(createState(), "Synteettinen valinta");
  assert.equal(state.index, 1);
  assert.deepEqual(state.choices, ["Synteettinen valinta"]);
});

test("nextIndex does not exceed the last step", () => {
  assert.equal(nextIndex(2, 3), 2);
});
