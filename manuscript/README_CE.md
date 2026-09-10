# Версия под Communications Engineering (Nature Portfolio)

`main.tex` — версия под Journal of Systems Architecture, **не тронута**.
`main_ce.tex` — версия под Communications Engineering. Общие ресурсы (figures/,
tables/, generated_numbers.tex, refs.bib) используются обеими версиями, поэтому
пересчёт результатов автоматически обновляет обе.

Сборка:

```bash
cd manuscript
pdflatex main_ce && bibtex main_ce && pdflatex main_ce && pdflatex main_ce
pdflatex supplement_ce && pdflatex supplement_ce
```

Структура CE-версии: Introduction -> Results -> Discussion -> Methods -> back matter,
как требует Nature Portfolio. Текст основной части (без Methods) ~2 400 слов при лимите
5 000; display items ровно 10 (7 рисунков + 3 таблицы) при лимите 10.
Всё остальное — в `supplement_ce.tex`: Supplementary Note 1 (полные доказательства),
Supplementary Note 2 (полная модель) и Supplementary Tables S1-S13.

Файлы: `COVER_LETTER_CE.md` (новое письмо), `COVER_LETTER.md` (старое, под JSA),
`HIGHLIGHTS.txt` (нужен только для JSA — Nature Portfolio highlights не просит).
