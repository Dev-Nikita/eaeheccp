"""Build the two submission sets under SUBMISSION/.

    SUBMISSION/Communications_Engineering/   Springer Nature template (sn-jnl)
        1_Manuscript/                  main.tex, refs.bib, main.bbl, class, style, figures
        2_Supplementary_Information/   supplement.tex, class
        3_Cover_letter/                hand-written, never touched by this script
    SUBMISSION/JSA/                          Elsevier template (elsarticle)
        1_Manuscript/                  main.tex, refs.bib, main.bbl, figures
        2_Supplementary/               supplement.tex
        3_Cover_letter/, Highlights.txt  hand-written, never touched by this script

Every \\input (sections, generated prose, generated tables, generated numbers) is resolved
in place, so each folder compiles on its own. The LaTeX sources live in manuscript/
(sn_main.tex + sections_sn/ + supplement_sn.tex for Communications Engineering,
main.tex + sections/ + supplement.tex for JSA); edit those, never the flattened copies.
PDFs and .bbl files are produced by compiling inside each folder and are kept.
"""
import re, shutil
from pathlib import Path

M = Path("manuscript")
S = Path("SUBMISSION")
INPUT = re.compile(r"\\input\{([^}]+)\}")
BUILD_JUNK = {".aux", ".log", ".fls", ".fdb_latexmk", ".out", ".blg", ".spl", ".gz", ".toc"}


def flatten(path: Path, skip_refdefs: bool, depth: int = 0) -> str:
    if depth > 8:
        raise RuntimeError("input nesting too deep: " + str(path))

    def sub(m):
        name = m.group(1)
        # In the Springer Nature version every cross-reference macro is defined in the
        # preamble with \newcommand, so the \providecommand defaults carried by each
        # generated snippet are inert duplicates. The JSA version needs them.
        if skip_refdefs and name.rstrip(".tex").endswith("refdefs"):
            return ""
        target = M / (name if name.endswith(".tex") else name + ".tex")
        if not target.exists():
            raise FileNotFoundError(target)
        return flatten(target, skip_refdefs, depth + 1).rstrip("\n")

    return INPUT.sub(sub, path.read_text())


def clean(folder: Path):
    folder.mkdir(parents=True, exist_ok=True)
    for f in folder.glob("*"):
        if f.is_file() and (f.suffix in BUILD_JUNK or f.name == ".DS_Store"):
            f.unlink()


def write_tex(src: str, folder: Path, dst: str, skip_refdefs: bool):
    body = flatten(M / src, skip_refdefs)
    assert "\\input{" not in body, f"unresolved input in {src}"
    (folder / dst).write_text(body)
    print(f"  {src:22s} -> {folder}/{dst} ({len(body.splitlines())} lines)")
    return body


def copy_figures(body: str, folder: Path):
    figs = folder / "figures"
    figs.mkdir(exist_ok=True)
    used = set(re.findall(r"includegraphics(?:\[[^\]]*\])?\{figures/([^}]+)\}", body))
    for f in figs.glob("*"):
        if f.name not in used:
            f.unlink()
    for name in sorted(used):
        shutil.copyfile(M / "figures" / name, figs / name)
    return sorted(used)


def build_ce():
    root = S / "Communications_Engineering"
    ms, si = root / "1_Manuscript", root / "2_Supplementary_Information"
    for d in (ms, si, root / "3_Cover_letter"):
        clean(d)
    print("Communications Engineering")
    body = write_tex("sn_main.tex", ms, "main.tex", True)
    sbody = write_tex("supplement_sn.tex", si, "supplement.tex", True)
    assert "includegraphics" not in sbody
    for f in ("sn-jnl.cls", "sn-nature.bst", "refs.bib"):
        shutil.copyfile(M / f, ms / f)
    shutil.copyfile(M / "sn-jnl.cls", si / "sn-jnl.cls")
    print("  figures:", copy_figures(body, ms))
    (root / "README.txt").write_text(
        "Communications Engineering -- what to upload\n"
        "============================================\n\n"
        "1_Manuscript/\n"
        "  main.pdf         manuscript PDF (the file reviewers read)\n"
        "  main.tex         LaTeX source, all sections and tables inlined\n"
        "  main.bbl         pre-built reference list (upload with the source)\n"
        "  refs.bib         bibliography, 41 entries\n"
        "  sn-jnl.cls       Springer Nature class\n"
        "  sn-nature.bst    reference style, with a one-function local fix of\n"
        "                   format.in.ed.booktitle (see the comment in the file)\n"
        "  figures/*.pdf    vector figure source files\n\n"
        "2_Supplementary_Information/\n"
        "  Supplementary_Information.pdf   upload as 'Supplementary Information'\n"
        "  supplement.tex, sn-jnl.cls      source, if the system asks for it\n\n"
        "3_Cover_letter/\n"
        "  Cover_letter.docx (or .md)      paste or upload as the cover letter\n\n"
        "Rebuild:  cd 1_Manuscript && pdflatex main && bibtex main && pdflatex main && pdflatex main\n"
        "          cd 2_Supplementary_Information && pdflatex supplement && pdflatex supplement\n"
        "Regenerate the .tex files from the sources:  python3 experiments/make_submission_package.py\n")


def build_jsa():
    root = S / "JSA"
    ms, si = root / "1_Manuscript", root / "2_Supplementary"
    for d in (ms, si, root / "3_Cover_letter"):
        clean(d)
    print("JSA")
    body = write_tex("main.tex", ms, "main.tex", False)
    sbody = write_tex("supplement.tex", si, "supplement.tex", False)
    assert "includegraphics" not in sbody
    shutil.copyfile(M / "refs.bib", ms / "refs.bib")
    print("  figures:", copy_figures(body, ms))
    (root / "README.txt").write_text(
        "Journal of Systems Architecture (Elsevier) -- kept as a fallback version\n"
        "=========================================================================\n\n"
        "1_Manuscript/     main.pdf, main.tex (flattened), main.bbl, refs.bib, figures/\n"
        "                  elsarticle.cls and elsarticle-num.bst come with TeX Live\n"
        "2_Supplementary/  supplement.pdf, supplement.tex\n"
        "3_Cover_letter/   Cover_letter.md\n"
        "Highlights.txt    Elsevier highlights\n")


if __name__ == "__main__":
    build_ce()
    build_jsa()
