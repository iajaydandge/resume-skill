---
name: resume-skill
description: Crafts, audits, tailors, and compiles ATS-compliant engineering resumes following strict 30-second elevator pitch standards and XeLaTeX Jinja2 templates. Use when creating, reviewing, improving, or tailoring engineering resumes, auditing bullet points for Google XYZ/STAR formulas, fixing action verbs, editing YAML data, or compiling PDFs with build.py via uv and XeLaTeX.
compatibility: Requires uv and MiKTeX/TeX Live with XeLaTeX on PATH.
metadata:
  standard: "https://agentskills.io"
  version: "1.0.0"
---

# Resume Skill for Coding Agents

> A resume is a 30-second elevator pitch on paper. Its sole job is to convince the hiring team to schedule an interview.

This skill equips any AI coding agent (Antigravity, Claude Code, OpenAI Codex, OpenCode, Cursor, Windsurf, Amp, Goose, Factory, etc.) adhering to the Agent Skills standard to act as an expert engineering resume reviewer, writer, and compiler. The agent directly audits candidate experience against strict engineering resume guidelines, drafts high-impact bullet points using Google XYZ and STAR frameworks, tailors applications, and compiles print-ready PDFs using Jinja2 and XeLaTeX via `uv`.

______________________________________________________________________

## Requirements

- [uv](https://docs.astral.sh/uv/) (handles Python and package dependencies automatically)
- [MiKTeX](https://miktex.org/) or TeX Live (`xelatex` must be on `PATH`). The default template uses Latin Modern (`lmodern`), the standard vector Computer Modern font included in all standard TeX distributions.

______________________________________________________________________

## Core Capabilities & Agent Workflows

### 1. Generating & Initializing Resume Files (`data/base.yaml` & Template)

When the skill is newly installed in a project directory:

1. Initialize the project files (both `data/base.yaml` and the shipped default `resume.tex.jinja2` template) by running:
   ```bash
   uv run python scripts/build.py --init
   ```
   *(or copy them directly from `assets/data/base.yaml` and `assets/resume.tex.jinja2`)*.
1. Prompt the user for their background, past work experience, technical projects, and skills, or ingest their LinkedIn/resume notes.
1. Populate `data/base.yaml` adhering strictly to the schema in `assets/data/base.yaml` and the [Strict Engineering Guidelines](#strict-engineering-guidelines).

### 2. Resume Audit & Review

As an intelligent coding agent, you directly inspect the candidate's resume (whether in YAML, Markdown, or text format) and verify it against the [Common Mistakes Checklist](#common-mistakes-checklist):

1. **Bullet Points**: Check that **NO bullet ends in a period**, no personal pronouns (`I`, `we`, `my`, `our`) are used, numbers are written as digits (`8` not `eight`), and lines do not spill over with 1–4 trailing words.
1. **Action Verbs**: Verify that every bullet starts with a strong past-tense action verb. Flag any weak verbs (`assisted`, `helped`, `worked on`, `utilized`) and superfluous buzzwords (`orchestrated`, `revolutionized`, `spearheaded`) using [references/action-verbs.md](references/action-verbs.md).
1. **Formulas**: Ensure bullets follow Google XYZ ("Accomplished X as measured by Y by doing Z") or STAR frameworks with quantified metrics near the start (see [references/bullet-formulas.md](references/bullet-formulas.md)).
1. **Dates**: Ensure ranges use en dashes with spaces (`–`), "Present" (not Current/Now), and months with full years.
1. **Formatting**: Enforce single-column layout, no icons, no graphics, no contact prefixes (`Email:`, `Phone:`), and plain text URLs without `https://www.`.
1. **Report**: Deliver an actionable assessment: Score (0–100), Critical Fixes, and Before & After rewritten bullet points.

### 3. Tailoring to a Job Description

When the user provides a job description:

1. Extract key technical requirements, system architectures, and engineering problems from the JD.
1. Review the candidate's master data in `data/base.yaml`.
1. Create a tailored application file under `applications/<company-role>/base.yaml`.
1. Reorder and sharpen bullet points to emphasize relevant achievements that directly match the JD. *Never fabricate experience; highlight genuine overlapping engineering judgment.*
1. Optional per-application template: An application can override the default template by placing `applications/<company-role>/resume.tex.jinja2` or passing `--template`.
1. Compile the tailored application:
   ```bash
   uv run --with jinja2 --with pyyaml python scripts/build.py --application <company-role>
   ```

### 4. Compiling Resume to PDF via XeLaTeX

Compile the resume using `uv` on the fly:

```bash
# Build master resume (from data/base.yaml -> resume.pdf & [Name]-Resume.pdf)
uv run --with jinja2 --with pyyaml python scripts/build.py

# Build tailored application (from applications/<id>/base.yaml -> applications/<id>/resume.pdf)
uv run --with jinja2 --with pyyaml python scripts/build.py --application <id>
```

The script resolves templates automatically: CLI flag (`--template`) > YAML `template` key > `applications/<id>/resume.tex.jinja2` > project root `resume.tex.jinja2` > skill default `assets/resume.tex.jinja2`. It renders LaTeX with proper escaping and compiles twice with XeLaTeX to ensure layout metrics resolve cleanly.

______________________________________________________________________

## Strict Engineering Guidelines

Agents must strictly enforce these rules without exception:

### 1. Formatting & Layout

- **Single-column only**: Never generate or recommend two-column, multi-column, or grid layouts. ATS parsers read left-to-right across columns, scrambling content.
- **No graphics**: Zero icons, images, headshots, skill bars, or decorative lines.
- **Alignment**: Text must be left-aligned. Never justify text (justification causes uneven word spacing).
- **Indentation**: No indenting sections or bullets (bullet points already provide indent).
- **Fonts**: Black font only (no grey, printable in greyscale). Minimum 10.5pt, minimum 1.07 line spacing, minimum 0.4 inch margins.
- **Page length**: 1 page per decade of experience (1 page for \<10 years; strictly 1 page for students/early/mid-career).

### 2. Dates

- **Alignment**: Right-aligned to the margin.
- **Separators**: Use en dashes with spaces (`–`), not hyphens (`-`), and not "to".
- **Present**: Use `Present` (never `Current`, `Now`, or `Ongoing`).
- **Format**: Month and full year (`Mar 2022 – Aug 2022`). Never use seasons (`Winter 2022`), numbers only (`9/2022`), or two-digit years (`'23`).
- **Abbreviations**: Jan, Feb, Mar, Apr, May, June, July, Aug, Sept, Oct, Nov, Dec (no trailing periods).

### 3. Contact Information

- **Include**: Name, email (Gmail or Outlook), GitHub (if populated with good READMEs), portfolio (if current).
- **Optional**: Phone, LinkedIn.
- **Omit**: Physical street address, ZIP code, city/state (unless applying locally), country codes (+1).
- **Plain text URLs**: No hyperlink masking (write `github.com/username`, not a link masked as `GitHub`). Don't include `https://www.`.
- **No prefixes**: Do NOT write `Email:`, `Phone:`, `GitHub:`.

### 4. Section Order

| Situation | Order |
| ------------------------------------ | ---------------------------------------------------------- |
| Graduated + full-time job | Work Experience → Skills → Education |
| Student / new grad, some experience | Education → Work Experience → Skills |
| Student / new grad, limited work exp | Education → Work Experience → Projects → Skills |
| No technical work experience | Education → Projects → Work Experience → Skills |
| No work experience at all | Education → Projects → Volunteer/Extracurriculars → Skills |
| Senior engineer (10+ YoE) | Summary → Work Experience → Skills → Education |
| Career changer | Summary → Work Experience → Projects → Skills → Education |

*Note: Omit Summary unless senior (10+ YoE) or making a career change. Never include references.*

### 5. Bullet Points

- **Length**: 1–2 lines each (target 1 sentence). Never spill onto a next line with only 1–4 words.
- **Verb**: Begin with a strong past-tense action verb (e.g., `Architected`, `Automated`, `Reduced`, `Implemented`).
- **No periods**: Never end bullet points with periods.
- **No pronouns**: Never use `I`, `we`, `my`, or `our`.
- **Digits**: Always use digits for numbers (`8` not `eight`, `3` not `three`).
- **Punctuation**: Avoid apostrophes, ampersands (`&`), and slashes (`/`).
- **No fluff adjectives/adverbs**: Eliminate `excellent`, `innovative`, `meticulously`, `successfully`.
- **No sub-bullets**: Avoid nested bullets.
- **No bolding keywords inside bullets**: Let accomplishments speak for themselves.

### 6. Verbs & Terminology

- **Strong action verbs**: `analyzed`, `architected`, `automated`, `built`, `created`, `decreased`, `designed`, `developed`, `implemented`, `improved`, `integrated`, `optimized`, `published`, `reduced`, `refactored`, `validated`, `tested`, `modeled`, `simulated`, `characterized`, `fabricated`, `assembled`, `calibrated`, `diagnosed`, `prototyped`.
- **Weak verbs to avoid**: `aided`, `assisted`, `coded`, `collaborated`, `communicated`, `executed`, `exposed to`, `gained experience`, `helped`, `participated`, `programmed`, `ran`, `used`, `utilized`, `worked on`.
- **Superfluous buzzwords to avoid**: `amplified`, `conceptualized`, `crafted`, `elevated`, `employed`, `engaged`, `engineered`, `enhanced`, `ensured`, `fostered`, `honed`, `innovated`, `mastered`, `orchestrated`, `perfected`, `pioneered`, `revolutionized`, `spearheaded`, `transformed`.
- **Misused terms**:
  - `utilize` → avoid (almost always just means "use").
  - `leverage` → avoid (jargon for "use").
  - `enhance` → often confused with "improve" (enhance = add features; improve = make better).
- See [references/action-verbs.md](references/action-verbs.md) for complete substitutions.

### 7. Education & Skills Sections

- **Education**: Reverse chronological. Graduation date only (no start dates). Include GPA only if ≥ 3.75 (two decimal places) and remove once full-time experience is gained. Degrees: `Bachelor of Science`, `Master of Science` (no apostrophe-s). High school omitted.
- **Skills**: Section titled `Skills` (not "Technical Skills"). Max 3 lines, single column, comma-separated, grouped logically (`Languages`, `Technologies`, `Tools`). Correct capitalization (`C, C++` not `C/C++`; `Git` not `GitHub/GitLab`). Soft skills omitted.

______________________________________________________________________

## Progressive Disclosure: Reference Guides

When more detail is required, consult these specialized guides:

- [references/engineering-guidelines.md](references/engineering-guidelines.md) — The complete master specification and rationale.
- [references/action-verbs.md](references/action-verbs.md) — Exhaustive verb index with before/after replacements.
- [references/bullet-formulas.md](references/bullet-formulas.md) — Google XYZ, STAR, CAR formulas with engineering examples.

______________________________________________________________________

## Common Mistakes Checklist

Before approving any resume, verify this checklist:

- [ ] Single column layout (no tables or multi-column grids)
- [ ] No icons, images, headshots, or graphics
- [ ] Left-aligned text (never justified)
- [ ] No extra indentation on bullets or section titles
- [ ] Black font only (no grey, readable weight >= 10.5pt)
- [ ] No bold keywords within bullet points
- [ ] **No periods at the end of bullets**
- [ ] No personal pronouns (`I`, `we`, `my`, `our`)
- [ ] No weak verbs (`utilized`, `assisted`, `helped`, `worked on`)
- [ ] No 1–4 word line spillover at the end of bullets
- [ ] Exactly 1 page (unless 10+ years of full-time experience)
- [ ] No high school listed
- [ ] No soft skills in the Skills section
- [ ] Date ranges use en dashes with spaces (`–`), not hyphens (`-`)
- [ ] Dates are right-aligned
- [ ] "Present" used instead of "Current", "Now", or "Ongoing"
- [ ] Months and full years used (no seasons, no two-digit years like `'23`)
- [ ] No contact prefixes (`Email:`, `Phone:`, `GitHub:`)
- [ ] URLs written as plain text without `https://www.` and without hyperlink masking
