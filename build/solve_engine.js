/* ======================================================================
   SOLVE ENGINE — plain English in, a ranked plan out
   · tokenise    lowercase, split, stem, drop stopwords
   · score       authored triggers (weighted) + IDF text overlap
   · band        pattern / composed / weak, with the floor under it
   · language    inferred from wording, overridable by the caller
   · plan        the ordered steps, the evidence, the runner-up

   This file ships twice and is written once. build/build_bridge.py inlines its
   text into bridge.html; build/verify_approach.py runs the same file under
   node against the fixtures. The rule that is proved is therefore literally
   the rule that runs — bridge_check.py and the drill's JS check() are the same
   rule written twice, which is survivable for a whitespace comparison and is
   not survivable for a ranking function with weights and thresholds.
   ====================================================================== */
(function (root) {
  "use strict";

  /* Thresholds. Every one of these is a number the fixture suite in
     build/verify_approach.py exercises: 66 labelled real questions that must
     rank correctly, and 21 out-of-scope problems that must fall under the
     floor. Moving one of these without re-running that script is how the tool
     starts bluffing. */
  var W_PHRASE = 2.0;   /* a multi-word trigger: this, plus W_PER_WORD per word */
  var W_PER_WORD = 1.2; /* so "how many times" outscores "how many" — the longer
                           phrase is the more specific claim, and specificity is
                           the whole reason a trigger list beats word overlap */
  var W_WORD = 2.4;     /* a single-word trigger */
  var W_TEXT = 1.0;     /* multiplier on the IDF overlap with the candidate's own text */
  var PAT_STRONG = 6.0; /* at or above: the plan is that pattern's */
  var ROW_MIN = 2.4;    /* a row has to clear this to become a step */
  var ROWS_MIN = 2;     /* and there have to be this many, or there is no plan */
  var COMPOSED_MIN = 6.5; /* and together they have to clear this. Two lone
                             trigger words is what "tune the database index so
                             the query stops doing a full scan" scores — index,
                             table — and a two-step plan built out of that is
                             the tool bluffing about a problem it has never
                             seen. */
  var CH_STRONG = 9.0;  /* at or above: name the challenge */
  var CH_WORDS = 5;     /* and on at least this many distinct words of its task */
  var MAX_STEPS = 8;

  /* Stemming has one job here and it is not linguistic accuracy: the same word
     written two ways has to reduce to the same key. The rules therefore run in
     a fixed order — plural first, then the verb ending — so that "string" and
     "strings" both land on "str". An earlier version stripped -ing before the
     plural and sent "string" to "str" while "strings" stopped at "string",
     which silently cost every date-parsing question its step. */
  function stem(w) {
    if (w.length > 4 && /(ses|xes|zes|ches|shes)$/.test(w)) w = w.slice(0, -2);
    else if (w.length > 3 && /ies$/.test(w)) w = w.slice(0, -3) + "y";
    else if (w.length > 3 && /s$/.test(w) && !/ss$/.test(w)) w = w.slice(0, -1);
    if (w.length > 5 && /ing$/.test(w)) return w.slice(0, -3);
    if (w.length > 4 && /ed$/.test(w)) return w.slice(0, -2);
    return w;
  }

  function words(text) {
    return String(text || "")
      .toLowerCase()
      .replace(/<[^>]+>/g, " ")
      .replace(/[^a-z0-9]+/g, " ")
      .trim()
      .split(/\s+/)
      .filter(function (w) { return w.length > 0; });
  }

  function createEngine(DATA) {
    var STOP = {};
    (DATA.stop || []).forEach(function (w) { STOP[stem(w)] = true; });

    var STAGE_IX = {};
    DATA.stages.forEach(function (s, i) { STAGE_IX[s.id] = i; });

    var ENT = {};
    DATA.entries.forEach(function (e) { ENT[e.id] = e; });

    /* Prepare each candidate once: its stemmed trigger phrases and the token
       set of its own text. Done at construction because the page rebuilds a
       plan on every keystroke of the example buttons and on every history
       re-open. */
    function prep(list, textOf) {
      return list.map(function (c) {
        var trig = (c.trig || []).map(function (t) {
          var ws = words(t).map(stem);
          var core = ws.filter(function (w) { return !STOP[w]; });
          /* The stop-filtered form is only usable as a phrase while it is
             still a phrase. "by category" reduces to "category", and matching
             that as a phrase would quietly turn a two-word trigger into a
             one-word one — which is how p-split-apply started answering a BMI
             question. Below two words, the full phrase is what has to match,
             and the weight stays on the original length either way. */
          return { raw: t, key: ws.join(" "),
                   core: core.length >= 2 ? core.join(" ") : "",
                   n: ws.length };
        }).filter(function (t) { return t.key.length > 0; });
        var toks = {};
        words(textOf(c)).map(stem).forEach(function (w) {
          if (!STOP[w] && w.length > 2) toks[w] = true;
        });
        return { c: c, trig: trig, toks: toks };
      });
    }

    var P_ENT = prep(DATA.entries, function (e) { return e.en; });
    var P_PAT = prep(DATA.patterns, function (p) {
      return p.name + " " + p.when + " " + p.shape;
    });
    var P_CH = prep(DATA.challenges, function (c) { return c.text; });

    /* IDF over the phrasebook entries and the patterns together. A word that
       appears in sixty candidates ("array") tells you far less than one that
       appears in two ("armstrong"), and without this the long candidates win
       every comparison by sheer surface area. */
    function idfTable(sets) {
      var df = {}, n = sets.length;
      sets.forEach(function (s) {
        for (var w in s.toks) df[w] = (df[w] || 0) + 1;
      });
      var idf = {};
      for (var w in df) idf[w] = Math.log(n / (1 + df[w])) + 0.35;
      return idf;
    }

    var IDF_ENT = idfTable(P_ENT);
    var IDF_PAT = idfTable(P_PAT);
    var IDF_CH = idfTable(P_CH);

    /* The gate: a candidate scores nothing on word overlap alone.
       "Robin decides between two dining halls" shares the word "two" with
       `conc-2` — "Protect a shared value from two writers" — and "two" is rare
       enough across 115 short sentences that IDF alone made that a step. A
       candidate has to be named by at least one authored trigger before its
       text overlap counts for anything; overlap then decides between
       candidates that all cleared the gate, and never lets one in on its own. */
    function scoreOne(p, q, idf, gate) {
      var hit = [], s = 0, i;
      for (i = 0; i < p.trig.length; i++) {
        var t = p.trig[i];
        if (t.n > 1) {
          /* Matched against the sentence with its function words removed as
             well as against the sentence as typed. "reverse a string" and
             "reverse a given string" are the same claim, and a phrase matcher
             that misses on the word "given" is a matcher that misses on how
             people actually write. */
          if (q.joined.indexOf(" " + t.key + " ") > -1 ||
              (t.core && q.core.indexOf(" " + t.core + " ") > -1)) {
            s += W_PHRASE + W_PER_WORD * t.n; hit.push(t.raw);
          }
        } else if (q.set[t.key]) {
          s += W_WORD; hit.push(t.raw);
        }
      }
      if (gate !== false && !hit.length) return { score: 0, hit: [], overlap: 0, n: 0 };
      var overlap = 0, n = 0;
      for (var w in q.set) {
        if (p.toks[w]) { overlap += (idf[w] || 0.35); n++; }
      }
      s += W_TEXT * overlap;
      return { score: s, hit: hit, overlap: overlap, n: n };
    }

    function rank(prepped, q, idf, gate) {
      var out = prepped.map(function (p) {
        var r = scoreOne(p, q, idf, gate);
        return { id: p.c.id, c: p.c, score: r.score, hit: r.hit, n: r.n };
      });
      out.sort(function (a, b) {
        return b.score - a.score || (a.id < b.id ? -1 : 1);
      });
      return out;
    }

    function query(text) {
      var toks = words(text).map(stem);
      var set = {};
      toks.forEach(function (w) { if (!STOP[w] && w.length > 2) set[w] = true; });
      var core = toks.filter(function (w) { return !STOP[w]; });
      return { raw: String(text || ""), toks: toks, set: set,
               joined: " " + toks.join(" ") + " ",
               core: " " + core.join(" ") + " " };
    }

    /* Language. Order of authority: what the caller pinned, then a word in the
       problem that only one language uses, then the group of the pattern that
       won, then whatever was remembered. Every one of these reports its reason
       — a language switched silently is the same defect as a setting switched
       silently. */
    function inferLang(q, winner, rows, fallback) {
      var counts = { c: 0, py: 0, r: 0 }, why = { c: "", py: "", r: "" };
      (DATA.hints || []).forEach(function (h) {
        var key = words(h.w).map(stem).join(" ");
        var found = key.indexOf(" ") > -1
          ? q.joined.indexOf(" " + key + " ") > -1
          : !!q.set[key] || q.toks.indexOf(key) > -1;
        if (found) { counts[h.lang] += 1; if (!why[h.lang]) why[h.lang] = h.why; }
      });
      var best = null;
      ["c", "py", "r"].forEach(function (l) {
        if (counts[l] > 0 && (!best || counts[l] > counts[best])) best = l;
      });
      if (best) return { lang: best, why: why[best], from: "wording" };
      if (winner && winner.c && winner.c.group) {
        if (winner.c.group.indexOf("Python") > -1) {
          return { lang: fallback === "r" ? "r" : "py",
                   why: "the pattern it matched is a Python and R pattern",
                   from: "pattern" };
        }
        return { lang: "c", why: "the pattern it matched is a C pattern",
                 from: "pattern" };
      }
      /* Nothing in the wording, no pattern. Then the steps themselves decide:
         "print the mean and the standard deviation" matches two entries with
         no C cell at all, and defaulting to C would drop both steps and leave
         a plan that says less than the sentence did. */
      if (rows && rows.length) {
        var cov = { c: 0, py: 0, r: 0 }, any = false;
        rows.forEach(function (e) {
          ["c", "py", "r"].forEach(function (l) {
            if (DATA.cells[e.id] && DATA.cells[e.id][l]) { cov[l] += e.score; any = true; }
          });
        });
        if (any) {
          var pick = fallback && cov[fallback] >= cov.c && cov[fallback] >= cov.py
                     && cov[fallback] >= cov.r ? fallback : null;
          if (!pick) {
            pick = "c";
            ["py", "r"].forEach(function (l) { if (cov[l] > cov[pick]) pick = l; });
          }
          if (cov[pick] > cov.c) {
            return { lang: pick,
                     why: "the steps it found have no C equivalent",
                     from: "steps" };
          }
        }
      }
      return { lang: fallback || "c", why: "nothing in the problem named a language",
               from: "default" };
    }

    function stepOf(row, text, stage, lang) {
      var have = row && DATA.cells[row] ? DATA.cells[row][lang] : false;
      return {
        text: text,
        row: row || null,
        stage: stage,
        en: row && ENT[row] ? ENT[row].en : "",
        code: have ? DATA.code[row][lang] : "",
        src: have ? DATA.src[row][lang] : "",
        note: row && DATA.note[row] ? DATA.note[row] : "",
        absent: !!row && !have
      };
    }

    function plan(text, opts) {
      opts = opts || {};
      var q = query(text);
      if (!q.toks.length) {
        return { band: "empty", steps: [], words: [], lang: opts.lang || "c" };
      }

      var pats = rank(P_PAT, q, IDF_PAT);
      var ents = rank(P_ENT, q, IDF_ENT);
      /* Challenges are scored without the trigger gate: they have no
         authored trigger list, because writing one per solution would be 130
         more lists to keep in step with the tasks themselves. Their own task
         text is long enough for word overlap to mean something — but only
         with a count floor under it, so a single shared rare word can never
         name a challenge. */
      var chs = rank(P_CH, q, IDF_CH, false);

      var winner = pats[0];
      var band = winner && winner.score >= PAT_STRONG ? "pattern" : null;

      var rows = ents.filter(function (e) { return e.score >= ROW_MIN; });
      if (!band) band = rows.length >= ROWS_MIN ? "composed" : "weak";

      var li = opts.lang
        ? { lang: opts.lang, why: "you chose it", from: "chosen" }
        : inferLang(q, band === "pattern" ? winner : null, rows, opts.remembered);
      var lang = li.lang;

      var steps = [], evidence = [], mismatch = null;

      if (band === "pattern") {
        var p = winner.c;
        evidence = winner.hit.slice(0, 8);
        steps = p.steps.map(function (s) {
          return stepOf(s.row, s.text, s.stage, lang);
        });
        if (p.group.indexOf("Python") > -1 && lang === "c") {
          mismatch = "This is a Python and R pattern; you are looking at C, " +
                     "where the shape does not exist in the same form.";
        }
        if (p.group.indexOf("Python") === -1 && lang !== "c") {
          mismatch = "This is a C pattern. In " +
                     (lang === "py" ? "Python" : "R") +
                     " most of it is one library call, so read the shape and " +
                     "not the line count.";
        }
      } else if (band === "composed") {
        var seen = {};
        var usable = rows.filter(function (e) {
          if (seen[e.id]) return false;
          seen[e.id] = true;
          return DATA.cells[e.id] && DATA.cells[e.id][lang];
        });
        usable.sort(function (a, b) {
          var sa = STAGE_IX[a.c.stage], sb = STAGE_IX[b.c.stage];
          return sa - sb || b.score - a.score;
        });
        usable = usable.slice(0, MAX_STEPS);
        var mass = usable.reduce(function (a, e) { return a + e.score; }, 0);
        if (usable.length < ROWS_MIN || mass < COMPOSED_MIN) {
          band = "weak";
        } else {
          steps = usable.map(function (e) {
            e.hit.forEach(function (h) {
              if (evidence.indexOf(h) === -1) evidence.push(h);
            });
            return stepOf(e.id, e.c.en, e.c.stage, lang);
          });
        }
      }

      /* The challenge line. Only on a strong match, and only in the language
         being shown — the 130 solutions are the most grounded thing in these
         files, and pointing at the wrong one spends a problem you could have
         worked. */
      var challenge = null;
      for (var i = 0; i < chs.length; i++) {
        if (chs[i].score < CH_STRONG || chs[i].n < CH_WORDS) break;
        if (chs[i].c.lang === lang || (lang === "r" && chs[i].c.lang === "py")) {
          challenge = { id: chs[i].c.id, name: chs[i].c.name,
                        score: chs[i].score, lang: chs[i].c.lang };
          break;
        }
      }

      /* The runner-up. When two patterns score close, hiding the second is the
         tool being more certain than it is. */
      var runner = null;
      if (band === "pattern" && pats[1] && pats[1].score > 0.45 * pats[0].score) {
        runner = { kind: "pattern", id: pats[1].id, name: pats[1].c.name,
                   score: pats[1].score };
      } else if (band === "composed" && pats[0] && pats[0].score > 0) {
        runner = { kind: "pattern", id: pats[0].id, name: pats[0].c.name,
                   score: pats[0].score, near: pats[0].score >= PAT_STRONG * 0.6 };
      }

      return {
        band: band,
        pattern: band === "pattern" ? { id: winner.id, name: winner.c.name,
                                        group: winner.c.group, shape: winner.c.shape,
                                        seen: winner.c.seen, code: winner.c.code,
                                        score: winner.score } : null,
        steps: steps,
        stages: DATA.stages,
        words: evidence,
        lang: lang,
        langWhy: li.why,
        langFrom: li.from,
        mismatch: mismatch,
        challenge: challenge,
        runner: runner,
        nearest: {
          patterns: pats.slice(0, 3).map(function (x) {
            return { id: x.id, name: x.c.name, score: Math.round(x.score * 10) / 10 };
          }),
          entries: ents.slice(0, 6).map(function (x) {
            return { id: x.id, en: x.c.en, score: Math.round(x.score * 10) / 10 };
          })
        },
        scores: { pattern: winner ? winner.score : 0,
                  rows: rows.length,
                  challenge: chs[0] ? chs[0].score : 0 },
        thresholds: { pattern: PAT_STRONG, row: ROW_MIN, rows: ROWS_MIN,
                      challenge: CH_STRONG }
      };
    }

    return { plan: plan, query: query, words: words, stem: stem };
  }

  var api = { createEngine: createEngine, words: words, stem: stem };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.SolveEngine = api;
})(typeof window !== "undefined" ? window : this);
