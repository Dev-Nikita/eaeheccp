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

## Вариант в шаблоне Springer Nature (sn-jnl)

`sn_main.tex` + `supplement_sn.tex` — та же CE-версия, свёрстанная официальным
шаблоном Springer Nature (`sn-jnl.cls`, стиль ссылок `sn-nature.bst`; оба файла
скопированы в `manuscript/`, папка `sn-article-template/` осталась нетронутой).

```bash
cd manuscript
pdflatex sn_main && bibtex sn_main && pdflatex sn_main && pdflatex sn_main
pdflatex supplement_sn && pdflatex supplement_sn
```

Текст берётся из `sections_sn/` — это копии `sections_ce/` со снятыми звёздочками в
заголовках (в шаблоне SN разделы нумеруются) плюс вынесенные в отдельные файлы
display items: `fig1.tex`, `tab1.tex`, `displays.tex`. Рисунки, таблицы, числа и
библиография общие со всеми версиями.

Особенность шаблона: `sn-jnl.cls` ломается, если tabular обернуть в `\resizebox`
или `adjustbox` (ошибка `Missing \endgroup`). Поэтому широкие таблицы уменьшены
через `{\let\scriptsize\tiny\setlength{\tabcolsep}{2pt}...}` — не менять на
resizebox.

Текущая сборка: main 16 страниц, supplement 8 страниц, 0 ошибок, 0 undefined
ссылок, ни одного overfull больше 10 pt, 19 источников в списке.

Файлы: `COVER_LETTER_CE.md` (новое письмо), `COVER_LETTER.md` (старое, под JSA),
`HIGHLIGHTS.txt` (нужен только для JSA — Nature Portfolio highlights не просит).
