/* Runs solve_engine.js outside the browser so verify_approach.py can assert on
   it. Reads {data, cases:[{text, lang}]} as JSON on stdin, writes one result
   per case as JSON on stdout. No logic of its own — if this file decided
   anything, the thing being verified would stop being the thing that ships. */
"use strict";

const fs = require("fs");
const path = require("path");
const { createEngine } = require(path.join(__dirname, "solve_engine.js"));

let raw = "";
process.stdin.on("data", (d) => { raw += d; });
process.stdin.on("end", () => {
  const req = JSON.parse(raw);
  const eng = createEngine(req.data);
  const out = req.cases.map((c) => {
    const p = eng.plan(c.text, c.lang ? { lang: c.lang } : {});
    return {
      band: p.band,
      pattern: p.pattern ? p.pattern.id : null,
      patternScore: p.scores.pattern,
      rows: p.steps.map((s) => s.row).filter(Boolean),
      lang: p.lang,
      langFrom: p.langFrom,
      challenge: p.challenge ? p.challenge.id : null,
      words: p.words,
      nearest: p.nearest.patterns
    };
  });
  process.stdout.write(JSON.stringify(out));
});
