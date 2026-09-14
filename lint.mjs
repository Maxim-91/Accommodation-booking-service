import { spawnSync } from "node:child_process";

const files = ["server.mjs", "app.mjs", "app.test.mjs", "build.mjs"];
for (const file of files) {
  const result = spawnSync(process.execPath, ["--check", file], {
    stdio: "inherit"
  });
  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}

console.log("Syntax checks passed.");
