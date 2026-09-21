Communications Engineering -- what to upload
============================================

1_Manuscript/
  main.pdf         manuscript PDF (the file reviewers read)
  main.tex         LaTeX source, all sections and tables inlined
  main.bbl         pre-built reference list (upload with the source)
  refs.bib         bibliography, 41 entries
  sn-jnl.cls       Springer Nature class
  sn-nature.bst    reference style, with a one-function local fix of
                   format.in.ed.booktitle (see the comment in the file)
  figures/*.pdf    vector figure source files

2_Supplementary_Information/
  Supplementary_Information.pdf   upload as 'Supplementary Information'
  supplement.tex, sn-jnl.cls      source, if the system asks for it

3_Cover_letter/
  Cover_letter.docx (or .md)      paste or upload as the cover letter

Rebuild:  cd 1_Manuscript && pdflatex main && bibtex main && pdflatex main && pdflatex main
          cd 2_Supplementary_Information && pdflatex supplement && pdflatex supplement
Regenerate the .tex files from the sources:  python3 experiments/make_submission_package.py
