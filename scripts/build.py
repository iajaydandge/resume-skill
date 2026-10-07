"""
build.py — Renders resume.tex.jinja2 with YAML data and compiles to PDF via XeLaTeX.

Designed to be run as an Agent Skill script:
  uv run --with jinja2 --with pyyaml python scripts/build.py [options]

Default Search Order for Data & Template:
  1. Current working directory (project level):
     - data/base.yaml or applications/<id>/base.yaml
     - resume.tex.jinja2 (if custom template provided in workspace)
  2. Fallback to skill assets/:
     - assets/resume.tex.jinja2
     - assets/data/base.yaml

Usage Examples:
  # Master resume in current workspace:
  uv run --with jinja2 --with pyyaml python scripts/build.py

  # Specific application:
  uv run --with jinja2 --with pyyaml python scripts/build.py --application google-swe

  # Explicit paths:
  uv run --with jinja2 --with pyyaml python scripts/build.py --data data/base.yaml --out resume.pdf
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

# Locations relative to this script
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSETS_DIR = SKILL_DIR / "assets"

# Default workspace root is current working directory
CWD = Path.cwd()


def latex_escape(value):
    """Escape special LaTeX characters in a string value."""
    if not isinstance(value, str):
        return value
    return (
        value.replace("\\", r"\textbackslash{}")
        .replace("&", r"\&")
        .replace("%", r"\%")
        .replace("$", r"\$")
        .replace("#", r"\#")
        .replace("_", r"\_")
        .replace("{", r"\{")
        .replace("}", r"\}")
        .replace("~", r"\textasciitilde{}")
        .replace("^", r"\textasciicircum{}")
    )


def resolve_paths(args):
    # Determine project root
    project_root = Path(args.project_root).resolve() if args.project_root else CWD

    # Determine data file
    if args.data:
        data_path = Path(args.data).resolve()
    elif args.application:
        data_path = project_root / "applications" / args.application / "base.yaml"
    else:
        # Check project data/base.yaml first, then fallback to skill assets/data/base.yaml
        local_data = project_root / "data" / "base.yaml"
        if local_data.exists():
            data_path = local_data
        else:
            data_path = ASSETS_DIR / "data" / "base.yaml"

    # Determine destination PDF
    if args.out:
        pdf_dst = Path(args.out).resolve()
    elif args.application:
        app_dir = project_root / "applications" / args.application
        app_dir.mkdir(parents=True, exist_ok=True)
        pdf_dst = app_dir / "resume.pdf"
    else:
        pdf_dst = project_root / "resume.pdf"

    build_dir = project_root / "build"
    build_dir.mkdir(parents=True, exist_ok=True)

    return project_root, data_path, pdf_dst, build_dir


def resolve_template(args, project_root, content, application_id=None):
    """
    Resolves template with precedence:
      1. Explicit CLI flag: --template <path>
      2. YAML content key: template: "custom.tex.jinja2" (supports per-application template)
      3. Application folder: applications/<id>/resume.tex.jinja2
      4. Project root: resume.tex.jinja2
      5. Skill assets: assets/resume.tex.jinja2 (default fallback)
    """
    if args.template:
        candidate = Path(args.template)
        if candidate.is_absolute():
            return candidate
        if (project_root / candidate).exists():
            return project_root / candidate
        if (ASSETS_DIR / candidate).exists():
            return ASSETS_DIR / candidate
        return project_root / candidate

    template_val = content.get("template")
    if template_val:
        t_name = str(template_val).strip()
        candidate = Path(t_name)
        if candidate.is_absolute():
            return candidate
        if (
            application_id
            and (project_root / "applications" / application_id / candidate).exists()
        ):
            return project_root / "applications" / application_id / candidate
        if (project_root / candidate).exists():
            return project_root / candidate
        if (ASSETS_DIR / candidate).exists():
            return ASSETS_DIR / candidate
        return project_root / candidate

    if application_id:
        app_template = (
            project_root / "applications" / application_id / "resume.tex.jinja2"
        )
        if app_template.exists():
            return app_template

    if (project_root / "resume.tex.jinja2").exists():
        return project_root / "resume.tex.jinja2"

    return ASSETS_DIR / "resume.tex.jinja2"


def main():
    parser = argparse.ArgumentParser(
        description="Compile ATS-compliant engineering resume using XeLaTeX and Jinja2."
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="Initialize data/base.yaml in current workspace from skill template.",
    )
    parser.add_argument(
        "--application",
        default=None,
        help="Application ID (subfolder under applications/). Reads applications/<id>/base.yaml",
    )
    parser.add_argument(
        "--data",
        default=None,
        help="Path to YAML data file. Defaults to data/base.yaml or applications/<id>/base.yaml",
    )
    parser.add_argument(
        "--template",
        default=None,
        help="LaTeX Jinja2 template file. Defaults to resume.tex.jinja2 or assets/resume.tex.jinja2",
    )
    parser.add_argument(
        "--project-root",
        default=None,
        help="Target workspace root directory. Defaults to current working directory.",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output PDF path. Defaults to resume.pdf or applications/<id>/resume.pdf",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve() if args.project_root else CWD

    if args.init:
        # 1. Initialize data/base.yaml
        target_dir = project_root / "data"
        target_dir.mkdir(parents=True, exist_ok=True)
        target_yaml = target_dir / "base.yaml"
        if target_yaml.exists():
            print(f"Notice: data/base.yaml already exists at {target_yaml}")
        else:
            sample_yaml = ASSETS_DIR / "data" / "base.yaml"
            if sample_yaml.exists():
                shutil.copy2(str(sample_yaml), str(target_yaml))
                print(
                    f"Successfully created: {target_yaml.relative_to(project_root) if project_root in target_yaml.parents else target_yaml}"
                )
            else:
                print(f"Error: Sample YAML not found at {sample_yaml}", file=sys.stderr)
                sys.exit(1)

        # 2. Initialize default resume.tex.jinja2 template
        target_template = project_root / "resume.tex.jinja2"
        if target_template.exists():
            print(f"Notice: resume.tex.jinja2 already exists at {target_template}")
        else:
            sample_template = ASSETS_DIR / "resume.tex.jinja2"
            if sample_template.exists():
                shutil.copy2(str(sample_template), str(target_template))
                print(
                    f"Successfully copied default template: {target_template.relative_to(project_root) if project_root in target_template.parents else target_template}"
                )
            else:
                print(
                    f"Error: Default template not found at {sample_template}",
                    file=sys.stderr,
                )
                sys.exit(1)

        print("\nInitialization complete! You now have:")
        print("  - data/base.yaml (edit your experience & contact info)")
        print("  - resume.tex.jinja2 (default LaTeX Jinja2 template)")
        return

    project_root, data_path, pdf_dst, build_dir = resolve_paths(args)

    if not data_path.exists():
        print(f"Error: Data file not found at: {data_path}", file=sys.stderr)
        print(
            "Tip: Run from your project directory containing data/base.yaml or pass --data",
            file=sys.stderr,
        )
        sys.exit(1)

    # Load YAML content first so it can specify a custom template
    content = yaml.safe_load(data_path.read_text(encoding="utf-8")) or {}
    identity = content.get("identity", {})

    # Resolve template (CLI flag > YAML template key > application folder > project root > skill default)
    template_path = resolve_template(args, project_root, content, args.application)

    if not template_path.exists():
        print(f"Error: Template not found at: {template_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading data from: {data_path}")
    print(f"Using template: {template_path}")

    context = {
        "identity": identity,
        "content": content,
    }

    # Setup Jinja Environment (searches template parent dir, project root, and skill assets)
    search_dirs = [str(template_path.parent), str(project_root), str(ASSETS_DIR)]
    seen = set()
    loader_dirs = [d for d in search_dirs if not (d in seen or seen.add(d))]

    env = Environment(
        loader=FileSystemLoader(loader_dirs),
        autoescape=False,
    )
    env.filters["latex"] = latex_escape

    template = env.get_template(template_path.name)
    tex_output = template.render(context)

    tex_path = build_dir / "resume.tex"
    tex_path.write_text(tex_output, encoding="utf-8")
    print(f"Rendered LaTeX written to: {tex_path}")

    xelatex_cmd = shutil.which("xelatex")
    if not xelatex_cmd:
        print("\nNotice: 'xelatex' command not found on system PATH.")
        print(f"The rendered LaTeX source is saved at: {tex_path}")
        print("Install TeX Live or MiKTeX to compile the PDF directly.\n")
        return

    print("Compiling XeLaTeX (pass 1/2)...")
    subprocess.run(
        [
            "xelatex",
            "-interaction=nonstopmode",
            "-output-directory",
            str(build_dir),
            str(tex_path),
        ],
        check=True,
    )

    print("Compiling XeLaTeX (pass 2/2)...")
    subprocess.run(
        [
            "xelatex",
            "-interaction=nonstopmode",
            "-output-directory",
            str(build_dir),
            str(tex_path),
        ],
        check=True,
    )

    compiled_pdf = build_dir / "resume.pdf"
    if compiled_pdf.exists():
        pdf_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(compiled_pdf), str(pdf_dst))

        # If candidate name is available, also create a named copy
        name = identity.get("name", "").strip().replace(" ", "-")
        if name:
            named_pdf = pdf_dst.parent / f"{name}-Resume.pdf"
            shutil.copy2(str(pdf_dst), str(named_pdf))
            print(f"Created named copy: {named_pdf}")

        print(f"Successfully generated: {pdf_dst}")
    else:
        print("Error: Compilation failed to generate resume.pdf", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
