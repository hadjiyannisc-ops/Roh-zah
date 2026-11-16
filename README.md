# Roh-zah

**A study system for Claude.** Say "Roh-zah", attach your slides or notes, and Claude turns them into a course: it finds exactly where your understanding stops, teaches each idea from first principles, then drills you until you've proven you know it, right up to a mock exam.

It's a single [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) (`roh-zah/SKILL.md`). There's no app and no API key: it runs inside Claude on your normal subscription.

## What it combines

| From | Idea | What it gives you |
|---|---|---|
| Amos Blomqvist's [learn](https://github.com/amosblomqvist/learn) | Find the edge of your knowledge; build from unconditional truths; make every step feel discovered | Real understanding, not memorized facts |
| Jane Street's [socratic-tutor](https://github.com/janestreet/agent_skills) | One question at a time, no answers handed over, strict 0-5 levels, spaced review, final exam | Proof that you actually know it |
| [nuwaves/socratic-tutor](https://github.com/nuwaves/socratic-tutor) | Stuck valve, review intervals, saved progress | Less frustration, a real schedule |
| Learning science (also behind Amos's [LearnHarness](https://github.com/amosblomqvist/learnharness)) | Predict before teaching, confidence ratings, interleaved practice that never names the idea, hint ladder | Knowledge that comes to mind on its own in the exam |

Plus things none of them have:

- **Built around your material.** It reads your slides first, follows your lecturer's notation, cites slide numbers, and prioritizes what the lecturer stresses and past papers test.
- **Exam-aware.** Review intervals compress to your exam date. "Exam mode" runs timed mocks in your exam's real format and marks them.
- **Visuals.** Diagrams, interactive demos and step-throughs whenever an idea is clearer as a picture.
- **Cheat sheets** for each topic once you've mastered it.
- **A PDF study report** when you're done: your readiness per topic, what you covered, your strengths and weaknesses (what you thought vs. what's true), flashcards, and every problem you got wrong to redo, with solutions at the back. See [the example](examples/sample-report.pdf).

## How a session goes

1. **Intake:** Claude reads your whole document, builds a map of every claim and how they depend on each other, and asks about your exam (date, format, target).
2. **Measure:** quick questions, one at a time, until it finds where your knowledge runs out on every topic.
3. **Plan:** a dependency map from what you already know to what the exam needs. You approve it before any teaching.
4. **Teach:** for each idea: you predict, Claude explains (answering your prediction), you're checked.
5. **Practice:** mixed problems that never say which idea they need, with hints given one step at a time.
6. **Review and exam:** spaced review of earlier topics, mock exams, and a final assessment.
7. **Report:** say `done` and you get the PDF study report to print and keep.

## Install

### Claude app (claude.ai, desktop, mobile)

1. Download [`dist/roh-zah.zip`](dist/roh-zah.zip).
2. In Claude, open **Settings** and find **Skills** (under Capabilities or Customize, depending on your app version).
3. Choose **Upload skill** and select `roh-zah.zip`.
4. Make sure the skill is switched on, and that code execution / file creation is enabled in Settings (needed to build the PDF report).

The zip includes the report builder and its fonts, so your PDFs come out exactly like the example.

### Claude Code

```bash
git clone https://github.com/YOUR-USERNAME/Roh-zah.git
mkdir -p ~/.claude/skills
cp -r Roh-zah/roh-zah ~/.claude/skills/
```

Restart Claude Code. Claude Code can also save your progress as a file in your study folder.

## Use

Start a new chat, attach your material, and say:

```
Roh-zah
```

Or be more specific:

```
Roh-zah: these are my thermodynamics slides, exam is Dec 12, written problems.
```

Commands you can use anytime:

| Command | What it does |
|---|---|
| `show progress` | Shows your skill map |
| `practice` | Mixed practice problems on what you've learned |
| `review due` | Drills only topics due for review |
| `exam mode` | Timed mock exam in your exam's format |
| `harder` / `easier` | Adjusts difficulty |
| `just tell me` | Skips the questioning for the current question only |
| `cheat sheet` | Compressed summary of a mastered topic |
| `save state` | Prints your progress so you can continue later |
| `done` / `report` | Builds the PDF study report |
| `Roh-zah resume from:` + saved block | Continues where you left off in a new chat |

## Tips

- **Give it past papers.** They're the single most useful extra: they tell it exactly what to train.
- **Use confidence honestly.** "I'm 90% sure" when you're wrong is the most useful signal it gets.
- **Resist "just tell me".** Working the answer out is what makes it stick.
- **Save state at the end of every session**, or ask Claude to keep a progress page if your app supports it.

## Limitations

It's a prompt: the model grades your answers, so levels are only as reliable as the model. Check anything that matters against your course material. It can't remind you about reviews by itself; start a session and it will tell you what's due.

## Credits and license

Roh-zah's instructions are written fresh, but the ideas come from the projects above. Thanks to Amos Blomqvist, Jane Street and nuwaves. Portions derive from Jane Street's socratic-tutor (MIT, Copyright (c) 2026 Jane Street Group, LLC).

Released under the [MIT License](LICENSE). The bundled IBM Plex fonts are under the [SIL Open Font License](roh-zah/scripts/fonts/OFL.txt).
