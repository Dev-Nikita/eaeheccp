# Manuscript

Сборка (нужен texlive с elsarticle, algorithm2e/algorithmicx, tikz, booktabs):

```bash
cd manuscript
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Все рисунки (`figures/*.pdf`) и все числовые таблицы (`tables/*.tex`) генерируются
из результатов одной командой из корня проекта:

```bash
python3 experiments/make_paper_assets.py
```

Ни одно число в статье не набрано вручную. Таблица 1 (related work) и текст —
единственное, что редактируется руками.

Структура: `main.tex` (преамбула, титул, abstract) + `sections/01..09` +
`refs.bib`. Текущая сборка: 24 страницы, 7 рисунков, 9 таблиц, 21 ссылка.
