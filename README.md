# Resume Skill

An open, portable Agent Skill adhering strictly to the [Agent Skills Specification](https://agentskills.io) and compatible with all standard-compliant AI agent clients:

- **Antigravity** (Google / Gemini CLI)
- **Claude Code** (Anthropic)
- **OpenAI Codex**
- **OpenCode**
- **Cursor**
- **Windsurf**
- **Amp**
- **OpenHands**, **Goose**, **Factory**, and more

It empowers coding agents to write, audit, tailor, and compile high-impact, ATS-compliant engineering resumes following strict 30-second elevator pitch standards ([r/EngineeringResumes](https://reddit.com/r/EngineeringResumes) guidelines) and XeLaTeX Jinja2 templates.

______________________________________________________________________

## Requirements

- [**uv**](https://docs.astral.sh/uv/) (handles Python and environment dependencies on the fly)
- [**MiKTeX**](https://miktex.org/) or TeX Live (`xelatex` must be on `PATH`). The default template uses Latin Modern (`lmodern`), the standard vector Computer Modern font included in all TeX distributions—requiring no separate font installation.

______________________________________________________________________

## Directory Structure

Conforms strictly to the [Agent Skills standard](https://agentskills.io/specification):

```
resume-skill/
├── SKILL.md                          # Main skill instructions loaded by the agent
├── scripts/
│   └── build.py                      # Renders Jinja2/LaTeX & compiles via XeLaTeX using uv
├── references/
│   ├── engineering-guidelines.md     # Complete r/EngineeringResumes guidelines & rules
│   ├── action-verbs.md               # High-impact verbs, weak verbs, and words to avoid
│   └── bullet-formulas.md            # Google XYZ, STAR, CAR formulas & examples
└── assets/
    ├── resume.tex.jinja2             # Production-ready, ATS-compliant XeLaTeX Jinja2 template
    └── data/
        └── base.yaml                 # Master resume data schema & starter content
```

______________________________________________________________________

## Installation

Following the [Agent Skills specification](https://agentskills.io/client-implementation/adding-skills-support.md), you can install this skill **per-project** (inside a dedicated resume directory) or **globally** (for all projects on your machine).

### Option A: Universal Cross-Agent Installation (Recommended)

Most compliant agents automatically scan `.agents/skills/`:

```bash
# 1. Navigate to your resume project directory
mkdir resume-project
cd resume-project

# 2. Clone into the universal cross-client skills directory
git clone https://github.com/iajaydandge/resume-skill.git .agents/skills/resume-skill
```

Or install it globally for all projects:

```bash
git clone https://github.com/iajaydandge/resume-skill.git ~/.agents/skills/resume-skill
```

### Option B: Client-Native Locations

If your agent prioritizes its client-specific configuration directory:

- **Universal / Agent Skills Standard (Recommended for all agents)**:
  - Project: `.agents/skills/resume-skill`
  - Global: `~/.agents/skills/resume-skill`
- **Claude Code**:
  - Project: `.claude/skills/resume-skill`
  - Global: `~/.claude/skills/resume-skill`
- **Antigravity (Google / Gemini CLI)**:
  - Project: `.agents/skills/resume-skill` or `.gemini/skills/resume-skill`
  - Global: `~/.gemini/antigravity-cli/skills/resume-skill` or `~/.agents/skills/resume-skill`
- **OpenCode**:
  - Project: `.opencode/skills/resume-skill` or `.agents/skills/resume-skill`
  - Global: `~/.config/opencode/skills/resume-skill` or `~/.agents/skills/resume-skill`
- **Cursor / Windsurf / VS Code Copilot**:
  - Project: `.agents/skills/resume-skill` or `.cursor/skills/resume-skill`
- **OpenAI Codex / Goose / Factory / Amp / OpenHands**:
  - Project: `.agents/skills/resume-skill`
  - Global: `~/.agents/skills/resume-skill`

______________________________________________________________________

## Working with AI Coding Agents

Once installed, launch your preferred AI coding agent inside your resume project directory:

```bash
# Launch via your terminal or IDE:
agy           # Antigravity CLI
claude        # Claude Code
opencode      # OpenCode
codex         # OpenAI Codex CLI
goose session # Goose
amp           # Amp
# Or open the workspace directly in Cursor, Windsurf, or VS Code
```


### Example Prompts to Give the Agent:

1. **Initialize Base Resume**:

   > *"Initialize my resume in `data/base.yaml` using the resume skill template. Here is my current background: [paste background/LinkedIn/notes]"*

   *(Or run directly: `uv run python .agents/skills/resume-skill/scripts/build.py --init` to generate both `data/base.yaml` and the default `resume.tex.jinja2` template)*

1. **Audit & Improve Bullets**:

   > *"Review my resume in `data/base.yaml` against the engineering resume guidelines. Check for weak verbs, missing metrics, periods at the end of bullets, and suggest Google XYZ rewrites."*

1. **Tailor for a Specific Job**:

   > *"Here is a job description for a Senior Infrastructure Engineer at Acme Corp: [paste JD]. Create `applications/acme-infra/base.yaml` tailored to this role and compile it."*

1. **Compile to PDF**:

   > *"Compile my resume to PDF."*
   > The agent will run:

   ```bash
   uv run --with jinja2 --with pyyaml python .agents/skills/resume-skill/scripts/build.py
   ```

   Or for tailored applications:

   ```bash
   uv run --with jinja2 --with pyyaml python .agents/skills/resume-skill/scripts/build.py --application acme-infra
   ```

   *(Note: Template can optionally vary per application. Place `applications/<id>/resume.tex.jinja2` or pass `--template`)*

______________________________________________________________________

## Expected Project Layout in Your Resume Directory

```
resume-project/
├── .agents/skills/resume-skill/      # Installed skill
├── data/
│   └── base.yaml                     # Master resume content (identity + experience)
├── applications/                     # Tailored applications
│   └── google-sre/
│       ├── base.yaml                 # Tailored content for this role
│       └── resume.pdf                # Generated application PDF
├── build/                            # Auto-generated intermediate XeLaTeX files
├── resume.pdf                        # Output master PDF
└── John-Doe-Resume.pdf               # Auto-named copy
```
