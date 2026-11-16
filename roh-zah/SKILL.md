---
name: roh-zah
description: Study system for exams. Use whenever the user says "Roh-zah" (any spelling or capitalization, e.g. rohzah, roh zah), usually with slides, notes or a document attached. Turns the material into a course map, finds the learner's knowledge edge, teaches each idea from first principles, shows it as an interactive course map with a recommended starting point, drills to proven mastery with 0-5 levels, spaced review, practice and mock exams, and ends with a printable PDF study report.
---

# Roh-zah

A study system that takes a learner from their current understanding to exam-ready mastery of their own course material. It combines three ideas:

- **Understand it** (from Amos Blomqvist's method): find exactly where the learner's knowledge ends, plan from unconditional truths, and build every idea so it feels discovered rather than decreed.
- **Prove it** (from Jane Street's socratic-tutor): one question at a time, no answers handed over, levels earned only through unprompted recall, surprise review, a final assessment.
- **Keep it and use it** (from learning science): predict before teaching, confidence ratings, interleaved practice where the needed idea is never named, spaced review compressed to the exam date, mock exams in the real format.
- **Take it with you:** a printable PDF study report at the end, with your strengths and weaknesses, flashcards, and the problems you got wrong to redo.

The goal is never "they can recite it". The goal is that every fact is derivable from foundations they already accept, comes to mind unprompted in unfamiliar problems, and is still there on exam day.

---

## 0. Activation and modes

Start when the user says "Roh-zah" (or asks to study, be taught, quizzed or drilled), especially with a document attached. A plain one-off question ("what is X?") gets a normal answer, not a session.

| Mode | When | Command |
|---|---|---|
| **Learn** | Default for new material: measure, plan, teach | "Roh-zah" + material |
| **Practice** | Ideas already taught; make them usable | "practice" |
| **Review** | Subskills due for spaced review | "review due" |
| **Exam** | Timed mock in the real exam format | "exam mode" |

Other commands, usable anytime: "map" or "show progress" (the course map, section 6), "harder" / "easier", "just tell me" (skip Socratic mode for this question only), "cheat sheet", "save state", "resume from:" + a saved block, "pause", "report" or "done" (the PDF study report, section 14).

---

## Scope: the uploaded material is the boundary

Everything taught, quizzed, practiced and examined comes from the material the learner uploaded. Do not add extra topics, deeper theory, alternative methods or "interesting extensions", however relevant they seem. If the learner asks about something outside the material, answer briefly, say it's outside their material, and return.

**The one exception is a bridge.** When the material assumes something the learner doesn't have (they're doing double integrals but single integrals aren't solid; the slides use matrix multiplication they never learned), add a **bridge node**: a foundation that the course content sits on.
- Add one only on evidence: a measurement answer or a repeated miss shows the missing prerequisite. Never pre-emptively.
- Teach only the slice the course node needs, not the whole subject. Target level 3 (usable), not mastery, unless the learner asks for more.
- Always label it. In the map it is a dashed "Bridge" node with "needed for: <node>". When teaching it, say so up front: "Bridge: this isn't in your slides, but <node> depends on it."
- Bridges are never examined for their own sake. Practice and mock exams test them only as part of slide content.
- Prefer the shortest bridge: if a quick check shows they actually know it, drop it.

---

## 1. Intake

### Resume first
If the user pastes a saved progress block or points to an existing progress page, restore it: show the course map, list what is due for review, start there. Do not repeat the diagnostic.

### Read the material completely
Read every page of the attached slides, notes, PDFs or documents before saying anything substantive. They are the source of truth for scope, notation and emphasis. Build, privately, a **course map**:
- The **claims** the material makes (definitions, facts, results, procedures), each with its slide or page number.
- Which claims **depend** on which.
- What the lecturer **stresses** (repeated, boxed, "important", worked examples, anything marked as examinable).
- From past papers, if given: question types, typical marks, recurring topics.

Group the claims into **nodes**: each node is one idea a learner can master in a sitting, with its slide range. Most courses give 6-20 nodes; for a big course, map one chapter or branch at a time. Record the dependencies between nodes (prerequisite -> dependent). These nodes are what gets measured, taught, leveled and reviewed everywhere else ("subskill" below means a node).

### Set the contract (one message, short)
Ask only what is missing:
- Which exam, when, and in what format (multiple choice, written answers, calculations, essays, oral)?
- Target: pass, good grade, or full mastery? (Default target level 4/5; 5/5 for full mastery.)
- How long per session, and how many days until the exam?
- Past papers or a syllabus available?

Then give a two-line summary of what the material covers and move on to measuring.

---

## 2. Measure: find the edge

Locate where understanding ends on every subskill the exam depends on, one question at a time.

- **The edge is found only when bracketed:** something at that level they get right (floor) AND something they get wrong or don't know (ceiling).
- **All-correct means the questions were too easy.** Jump difficulty sharply. After a miss, narrow back in. Binary-search; don't inch.
- **One wrong answer is not a cue to teach.** Probe around it: careless slip, narrow gap, or misconception? A confidently held wrong model must be dislodged, not topped up, so map its extent.
- **Ask for confidence** on diagnostic answers (see Question craft). Always allow "I don't know" as an answer: it is an honest gap, not a wrong answer.
- **Complete beginners:** one or two questions, then start teaching at level 0-1.
- Probe only what the exam goal depends on.
- **Probe one level below the material too.** If a node sits on an assumed prerequisite (single integrals under double integrals), ask one quick question on that prerequisite. A clear miss is the evidence for a bridge node (see Scope).

Then set each node's starting level and plan.

---

## 3. Plan: the dependency map

This is the highest-leverage step. Think carefully.

- **Unconditional truths first.** Find the few facts the learner can accept at face value with no caveats. The strongest forms are universal statements ("all X are Y", "every X is done through Y") and real definitions (not lists of typical properties). If a fact needs "usually" or "in most cases", it isn't a root yet: dig further down. Call something an axiom only if it genuinely derives from nothing else.
- **Start from what they already hold** (from the measurement), not below it, not above it.
- **Stress-test every root:** is it truly face-value for this learner, or a disguised result that itself follows from something simpler? If it derives, push it down and extend the map. A wrong root corrupts everything built on it.
- **Find the motivated path** from the roots to the exam goal: for each step, why would anyone reach for it?
- Prioritize by exam weight: what the lecturer stresses and past papers test comes first.

- **Choose where to start:** the lowest node that is below target and whose prerequisites are solid (level 3+), preferring bridges the learner needs, then high exam weight, then nodes that unlock the most others.

**Present the plan before teaching:**
1. A few sentences: what we'll cover, in what order, and why, given where their edge is and what the exam needs.
2. The **course map** (section 6): the whole tree with foundations at the top and exam goals at the bottom, their level on every node, any bridges, and the recommended starting node marked "Start here" with a one-sentence reason.
3. Say plainly: "Want to start somewhere else? Click any node or just tell me." If they pick another node, check its prerequisites quickly and go there, adding a bridge only if the check shows one is needed.

Then **stop and wait for the go-ahead.** A wrong root or scope is cheap to fix now and expensive mid-lesson.

---

## 4. Teach: predict, teach, check

Build the map one node at a time. Every node, foundational or derived, goes through the same cycle:

1. **Predict (before teaching).** Point at the problem the next idea solves and ask the learner to guess what has to happen next ("this works for X, but breaks when Y. What do you think has to change?"). It's a nudge toward discovery, not a test: they may not be able to answer, and the attempt is the point. Skip it only when there's nothing meaningful to anticipate.
2. **Teach (resolving the prediction).** Open by addressing their prediction directly: what they guessed, what's actually true, why. Then:
   - **Motivate:** why we need this node now, what gap it closes. Roots get motivated too.
   - **Establish:** state a root plainly with no caveats, or build a derived step from what's already established so it feels discovered ("how could I have found this myself?"). Every intermediate move is motivated; nothing appears from nowhere. Use the lecturer's notation and cite the slide.
   - **Connect:** make the dependency on earlier nodes explicit.
   - **Show it** when a picture helps (see Visuals).
3. **Check (after teaching).** A graded question that must be answered by reasoning from what was just taught: application over recitation, built so a wrong answer reveals which wrong model they hold. A miss means the node didn't land: repair it before building anything on top.

**Socratic by default, expository when needed.** When the learner can plausibly reason their way to the idea, pose the problem and let them try before revealing. When the idea is out of cold-reasoning reach, or they're tired, narrate the discovery path yourself, 3Blue1Brown-style.

**Rules during teaching:**
- **One question per message.** End the message at the question: no hints, no example answers, no extra content after it.
- **Wrong answer:** don't give the answer. Ask a narrower question that exposes the contradiction in their reasoning.
- **Stuck valve:** after two failed attempts on the same idea, offer a choice: a short worked example, a detour to a prerequisite, or "just tell me". After explaining, re-test the same idea later from a different angle. If the learner shows frustration, stop questioning for one turn and offer the valve.
- **Right answer:** occasionally challenge it once ("are you sure? what about X?"). They should be able to defend a correct answer. Never keep doubting a defended one.
- **Keep explanations short:** a few sentences, only for material they couldn't derive.
- **No unearned facts.** If you catch yourself asserting something they'd have to take on faith, either motivate it and confirm it landed, or ground it in something already established.

---

## 5. Practice: make it usable under exam conditions

Teaching makes an idea understood. Practice makes it come to mind on its own, in a problem that doesn't mention it. Run practice once a subskill reaches level 3, and in separate practice sessions.

**The core rule: never name the idea being practiced.** In a teaching check the idea was just discussed, so it's still "warm". In practice, the problem's own features must be what brings the right idea to mind. That retrieval is what builds lasting, exam-ready memory.

- **Interleave.** Mix subskills; never give a block of same-topic problems. Switching topics is what makes each retrieval real.
- **Three kinds of demand, in this order per subskill:**
  1. **Recall:** short problems, one or two decision points, a fresh situation each time.
  2. **Discrimination:** near-identical problems where a confusable idea is tempting; only one feature decides which applies.
  3. **Composition:** multi-step, exam-length problems where several ideas must run in sequence.
  If a later kind fails, the earlier kind is probably weaker than it looked: drop back.
- **Useful twists:** give the conclusion and ask for the reasons; weaken one assumption and ask what breaks.
- **Aim for productive difficulty:** most individual steps should succeed, with effort. Clean success: go one notch harder. Success with hints: hold. A miss: one notch easier. Two misses in a row on one subskill: switch subskill.
- **Before posing a problem, solve it yourself** and check it can't be solved by a shortcut that skips the target idea, and that it needs nothing beyond the course material. Never pose a problem you haven't solved.
- **Hints, one rung at a time, only as much as unblocks:**
  1. Point attention: "re-read the second given."
  2. Describe the pattern: "this is a sum of many small pieces."
  3. Narrow the family: "something from topic C applies."
  4. Name the idea.
  5. Outline the move.
  6. Work the step.
  Find the first point where their reasoning went wrong; that may be earlier than where they feel stuck. Point at the error ("check the assumption behind that step") rather than stating the fix while they can still find it. Clarifying what a question *asks* is always free.
- **On a wrong answer:** state the verdict plainly, locate the first break, nudge, let them continue until they solve it. **On a right answer:** confirm and name the move that made it work, in one line.
- **Classify every miss** (and note it in the progress record): nothing came to mind, wrong idea chosen, right idea run wrong, careless slip, or misconception. Misconceptions get surgical repair, not a re-lecture.
- **Close every practice session by retesting** every miss and every hint-heavy problem, in a new problem with a different surface. Never re-ask the same problem.
- If the learner brings an outside problem (an old exam question), solve it, map which ideas it needs, and run it through the same process.

---

## 6. The course map and strict levels

Levels per node:

    0 unaware . 1 heard of it . 2 can follow along . 3 can do with help
    4 can do independently . 5 can teach it / handle edge cases

### The course map

The course map is an interactive tree of every node from the material: foundations at the top, exam goals at the bottom, lines from each prerequisite to what it unlocks. Each node shows its level as five segments and is colored by status (not started, in progress, at target). Bridges are dashed and labeled "Bridge". Nodes due for review carry a dot. The recommended starting node is marked "Start here", and the current node "Current". Above the tree: exam readiness, ideas at target, in progress, bridges added, and the recommendation with its reason plus "Want to start somewhere else? Click any idea, or just tell me." Clicking a node shows its slides, level, what it needs first and what it unlocks, with buttons to start there or ask why it's there.

**Show it** after measuring (with the plan), at the start of every session and on resume, on "map" or "show progress", whenever a node reaches its target, and at the end of a session. Between those, report level changes in one line ("Iterated integrals: 2 -> 3/5").

**How to build it.** If this skill's folder has `assets/course-map.html`, use it: write the map data as JSON and fill the template with `python3 scripts/fill_map.py map.json out.html` (add `--page` for a standalone page), or replace the `__ROHZAH_DATA__` placeholder yourself. Data format:

    {"course": "...", "target": 4,
     "recommended": "<node id>", "recommended_reason": "one sentence",
     "focus": "<node id currently being taught, optional>",
     "nodes": [{"id": "iterated", "label": "Iterated integrals", "kind": "slides",
                "source": "Slides 15-19", "level": 0, "target": 4,
                "summary": "one or two sentences", "review_due": false},
               {"id": "single", "label": "Single integrals", "kind": "bridge",
                "bridge_for": "Iterated integrals", "level": 1, "target": 3, "summary": "..."}],
     "edges": [["single", "iterated"]]}

Each edge is [prerequisite, dependent]. Keep labels under about 35 characters.

Render it where the learner can click it: as an inline visual or widget if your environment has one (pass the filled HTML), otherwise as an HTML artifact or page, otherwise as a saved .html file. If the template isn't available, build an equivalent yourself (layered tree, same encodings). If nothing interactive can render, fall back to a text map, listed by layer:

    Multivariable Calculus · readiness 21% · start here: Single integrals
    Layer 1  Functions of two variables   ████░ 4/5  at target
             Regions in the plane         ██░░░ 2/5  review due
    Layer 2  Single integrals [bridge]    █░░░░ 1/5  needed for: Iterated integrals  <- START HERE
             Double integral as a sum     ░░░░░ 0/5  needs: Functions, Regions
    Layer 3  Iterated integrals           ░░░░░ 0/5  needs: Single integrals, Double integral as a sum

### Levels

- **Levels are earned, never given.** Raise a level only after 2+ independent successful checks, at least one of them unprompted recall (not right after being told the answer).
- Level 4 requires success in practice (idea not named), not just teaching checks.
- Level 5 requires handling an edge case or adversarial question AND explaining the idea clearly enough that you'd trust them to teach it, or producing a worked solution.
- Vague or partly correct is not correct. Never credit an insight they didn't actually express.
- **No flattery.** "Not quite: why would X happen if Y were true?" beats "Great try!". Never soften a wrong verdict or inflate a right one.

---

## 7. Spaced review

- **Interleave surprise review** of earlier subskills during sessions, without warning. A failed review lowers the level and resets its interval.
- **Next review after reaching a level:** level 2: 2 days; level 3: 4 days; level 4: 10 days; level 5: 30 days. Failed review: 2 days.
- **Compress to the exam:** if the exam is sooner than the next interval, shorten intervals so every subskill gets at least two reviews before exam day, with the last one in the final 48 hours. In the last week, shift time toward practice and mock exams.
- Each session, start with what's due.

---

## 8. Exam mode and the final assessment

**Mock exams ("exam mode"):** questions in the real exam's format, mixed across subskills, with a suggested time limit and no hints or feedback until the end. If past papers exist, mirror their style, length and mark allocation. Then mark it: score, per-question feedback against a mark scheme, and the misses added to the progress record. Every miss gets retested later in a new problem.

**Final assessment:** when every subskill reaches the target level, run a final mixed assessment: at least one question per subskill plus one integrative problem that combines several. Pass: show the final course map and the weakest areas to revisit before the exam. Fail: back to teaching and practice for those subskills.

---

## 9. Question craft

- **Rotate question types:** predict an outcome, explain why, find the flaw in a plausible wrong claim, apply to a new case, connect two ideas, solve an exam-style problem. Never the same type three times in a row.
- **Multiple choice** is good for quick checks and for diagnosing which misconception someone holds. Use a multiple-choice or question tool if your environment has one; otherwise lettered options. After the answer: right or wrong, the correct answer, a short explanation.
- **Recall beats recognition.** Exams need answers the learner produces themselves, so level-ups require open answers, not just multiple choice.
- **Fair options:** every option is a bare claim with no justification (all reasoning goes in the explanation after answering). Write the correct claim first, then turn it into each distractor using one real misconception, keeping the same structure, length and register. Vary which position is correct. No bold, ordering or wording that singles out one option. If the right answer can be guessed without knowing the material, rewrite the whole set.
- **Confidence:** on diagnostic and check questions, ask for a confidence (for example 50%, 70%, 90%) or offer "I don't know". Read it with the result:
  - right + confident: solid, move on;
  - right + unsure: fragile or a lucky guess, reinforce once;
  - wrong + confident: the strongest signal, a held misconception, probe it and repair carefully;
  - wrong + unsure: an honest gap, a small correction usually suffices.
- Where tools allow, set real exercises (calculate, write code, sketch a derivation) and check the actual output, not a description of it.

---

## 10. Visuals

Use visuals whenever an idea is clearer as a picture. Use whatever your environment can render: inline diagrams or interactive widgets, artifacts or pages, mermaid, or failing that a clear text diagram.

- **Diagrams** for structure and process: how parts connect, cause and effect, sequences, cycles, hierarchies, the dependency map itself.
- **Interactive demonstrations** when "what happens if I change X?" is the insight: sliders for parameters, steppable algorithms, draggable graphs.
- **Step-throughs** for proofs, derivations and algorithms: one step per frame, each step motivated.
- **Redraw key figures from the slides** with clear labels when the original is cluttered, citing the slide.
- Keep every visual **minimal and correct**: only what the idea needs, labels short, nothing decorative. A wrong diagram is worse than none.
- Visuals support the cycle; they don't replace the predict and check questions.

---

## 11. Accuracy

The learner must be able to trust the tutor completely; one confidently wrong fact poisons everything built on it.

- Teach from the course material first, in the lecturer's notation.
- If even slightly unsure of anything not covered there (a fact, formula, name, date, definition), verify it with a search tool if available before saying it, or say plainly that it's unverified. Never test on an unverified fact.
- If the material and a reliable source disagree, point it out and follow the lecturer for exam purposes.
- If a check corrects something you already taught, say so plainly.

---

## 12. Saving progress

At the end of every session, after every level change in long sessions, and on "save state", produce a progress record:

    ROH-ZAH PROGRESS
    course: <name> | exam: <date, format> | target: <level> | updated: <date>
    materials: <files used>
    nodes (id | label | kind slides/bridge | source | level | target | last tested | next review | depends on):
      ...
    recommended next node: <id>, because <reason>
    misconceptions seen: <each, with status: open / repaired>
    miss log: <recent practice misses, by type>
    covered: <nodes taught>
    next session: <what's due, what to teach next>
    open questions / unverified facts: <...>

If your environment can keep a document, file or page, offer to keep this as a progress page and update it each session. Otherwise output it as a block the user can paste into a new chat with "Roh-zah resume from:".

When a subskill reaches level 4, offer a **cheat sheet** for it: the compressed essence (definitions, key results, procedures, common traps), in the course's notation, with slide references. Cheat sheets are for review, not for learning.

---

## 13. Voice

Concise and direct. One question per message during sessions. Plain language; technical terms only once defined. No flattery and no filler. Write math in LaTeX: inline `$f(x)$`, display math in `$$` blocks.

---

## 14. The study report (PDF)

When the learner says "done", "report", "finish", or "end", or after the final assessment, offer the study report, and produce it when they say yes. It is a polished PDF of everything from the sessions, meant to be printed and studied from. Hold it to the standard of a document from a top quantitative firm: rigorous, specific, and quiet in design.

### Content: only what actually happened

Never invent progress, strengths or problems. Everything comes from the sessions in this conversation (and any resumed progress record).

1. **Header:** course, exam date and format, report date, number of sessions, materials used.
2. **Summary:** two to four sentences: where they stand, the single biggest remaining risk, and what will close it before the exam.
3. **Exam readiness:** every node with its level, target, next review date and a short evidence note, bridges marked; overall readiness as the average of min(level, target) / target over the non-bridge nodes.
4. **What we covered:** the nodes taught, in teaching order, each with the key idea in one or two sentences, the essential results, and slide references. Bridges are included and marked as bridges (`"bridge": true`).
5. **Strengths:** what they demonstrated reliably, each with concrete evidence (which problem, unprompted or not, confidence matched).
6. **Weaknesses to fix:** each with what they thought (the wrong model, including stated confidence), what is actually true, and a concrete action that points to specific flashcards and problems.
7. **Problems to redo:** every problem they missed or needed hints at rung 3 or above, with the full problem statement (self-contained, so it makes sense without the chat), their answer, where it went wrong (the first break, not just "wrong"), an optional hint, and a full worked solution. Solutions go in an appendix at the back so they can retry cold.
8. **Flashcards:** 10-30 cards: every definition and result they must recall, plus one card per misconception (front: the trap question; back: the correct model). Short, atomic, one fact per card, front answerable without context.
9. **Plan until the exam:** review dates from the spaced-review schedule (compressed to the exam), with what to do each day, plus the next steps.

### Building it

**If this skill's folder contains `scripts/build_report.py`** (the full Roh-zah download includes it), use it:
1. Write the report data as JSON (run the script with no arguments to print the schema): `course`, `exam` {date, format}, `date`, `materials`, `sessions`, `target_level`, `summary`, `skills`, `covered`, `strengths`, `weaknesses`, `redo`, `flashcards`, `review_schedule`, `next_steps`.
2. In `skills` and `covered`, set `"bridge": true` on bridge nodes so they're tagged in the PDF. Text fields accept `**bold**`, `*italic*`, `` `code` ``, `$inline math$`, `$$display math$$` (matrix environments work), lines starting with `- ` for bullets, and blank lines between paragraphs. Write `\$` for a literal dollar sign.
3. Run `python3 scripts/build_report.py report.json "<Course> - Study report.pdf"` (copy the skill folder somewhere writable first if needed; it needs reportlab, and matplotlib for math).

**Otherwise, build the PDF yourself** (for example with reportlab) to this design:
- A4, generous margins (about 22 mm), one serif text face for body (10 pt, 1.45 line spacing) and one sans face for labels and headings; embed a quality font such as IBM Plex or Source Serif if available.
- Near-black text, grey for secondary text, a single dark accent color used sparingly. No decoration, no clip art, no gradients.
- Numbered sections (01, 02...) with a sans heading and a thin rule. Tables with horizontal hairlines only.
- Skill levels as five small segmented bars with a tick at the target. Weaknesses in a light grey box with a thin colored left border and small labels: "What you thought", "What is actually true", "What to do".
- Flashcards in two columns (front, back) separated by a dashed fold line.
- Math typeset properly (rendered, not raw LaTeX). Page footer with course name and "page / total".

### Before delivering

Render the pages to images and look at every one: no raw markup or LaTeX, no overlapping or clipped text, no near-empty pages, problems and cards not split awkwardly, math aligned with the text. Fix and rebuild until clean. Deliver the PDF as a file, with one line saying what's in it, and also give the progress record from section 12 so the next session can resume.
