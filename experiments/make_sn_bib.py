"""Generate manuscript/refs_sn.bib from manuscript/refs.bib.

sn-nature.bst silently drops `booktitle` for @inproceedings, so conference venues
disappear from the reference list; it does print `series`. elsarticle-num, used by the
Elsevier-format versions, prints BOTH, which would duplicate the venue there. The two
bibliographies are therefore generated from one source instead of being maintained twice.
"""
import re, os, sys

SRC = "manuscript/refs.bib"
DST = "manuscript/refs_sn.bib"


def main():
    src = open(SRC).read()
    out, n = [], 0
    for chunk in re.split(r"(?=@\w+\{)", src):
        if chunk.strip().startswith("@inproceedings") and "series" not in chunk:
            m = re.search(r"booktitle\s*=\s*\{(.+?)\},?\s*\n", chunk, re.S)
            if m:
                venue = " ".join(m.group(1).split())
                if not venue.lower().startswith(("proc", "in ")):
                    venue = "Proc. " + venue
                chunk = chunk.replace(m.group(0),
                                      m.group(0).rstrip() + f"\n  series    = {{{venue}}},\n")
                n += 1
        out.append(chunk)
    open(DST, "w").write(
        "%% GENERATED from refs.bib by experiments/make_sn_bib.py -- do not edit.\n"
        + "".join(out))
    print(f"wrote {DST}: {n} conference entries given an explicit series/venue field")


if __name__ == "__main__":
    main()
