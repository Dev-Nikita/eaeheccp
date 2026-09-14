# Версия под Communications Engineering (Nature Portfolio)

В репозитории две действующие версии статьи:

- `main.tex` + `sections/` + `supplement.tex` — Journal of Systems Architecture
  (elsarticle), **не тронута**, лежит на всякий случай;
- `sn_main.tex` + `sections_sn/` + `supplement_sn.tex` — Communications Engineering,
  свёрстана официальным шаблоном Springer Nature. Готовый пакет подачи —
  `manuscript/sn-manuscript/` (генерируется скриптом, см. ниже).

Общие ресурсы (`figures/`, `tables/`, `generated/`, `generated_numbers.tex`,
`refs.bib`) используются обеими версиями, поэтому пересчёт результатов обновляет обе.
Промежуточная elsarticle-версия под CE (`main_ce.tex`, `sections_ce/`,
`supplement_ce.tex`) удалена как устаревшая — она осталась в истории git.

## Вариант в шаблоне Springer Nature (sn-jnl)

`sn_main.tex` + `supplement_sn.tex` — та же CE-версия, свёрстанная официальным
шаблоном Springer Nature (`sn-jnl.cls`, стиль ссылок `sn-nature.bst`; оба файла
скопированы в `manuscript/`, скачанная папка шаблона удалена как дубликат).

```bash
cd manuscript
pdflatex sn_main && bibtex sn_main && pdflatex sn_main && pdflatex sn_main
pdflatex supplement_sn && pdflatex supplement_sn
```

Текст берётся из `sections_sn/`: разделы без звёздочек (в шаблоне SN они нумеруются)
плюс вынесенные в отдельные файлы
display items: `fig1.tex`, `tab1.tex`, `displays.tex`. Рисунки, таблицы, числа и
библиография общие со всеми версиями.

Особенность шаблона: `sn-jnl.cls` ломается, если tabular обернуть в `\resizebox`
или `adjustbox` (ошибка `Missing \endgroup`). Поэтому широкие таблицы уменьшены
через `{\let\scriptsize\tiny\setlength{\tabcolsep}{2pt}...}` — не менять на
resizebox.

Текущая сборка: main 19 страниц, supplement 8 страниц, 0 ошибок, 0 undefined
ссылок, ни одного overfull больше 10 pt, **41 источник** в списке.

Библиография у всех версий одна — `manuscript/refs.bib`. В `sn-nature.bst` из
официального шаблона (2024/07/19 v1.1) сломана функция `format.in.ed.booktitle`:
она читает название сборника с пустого стека, поэтому BibTeX падает с
`You can't pop an empty literal stack` на каждом @inproceedings/@incollection,
обрывает сборку (в latexmk/Overleaf это и даёт `???` вместо номеров ссылок) и
выбрасывает название конференции. В `manuscript/sn-nature.bst` эта одна функция
исправлена, правка помечена комментарием `LOCAL FIX`; больше в стиле ничего не
менялось. Ранее для обхода генерировался `refs_sn.bib` с полем `series` —
он и скрипт `make_sn_bib.py` удалены.

Аудит числовых утверждений: `python3 experiments/check_claims.py` проверяет, что
каждое эмпирическое число в тексте встречается в `generated/`, `tables/` или в
сырых CSV. Сейчас проходит чисто.

Включена нумерация строк (опция класса `lineno`) — как просит Nature Portfolio для
рецензирования.

Файлы: `COVER_LETTER_CE.md` (новое письмо), `COVER_LETTER.md` (старое, под JSA),
`HIGHLIGHTS.txt` (нужен только для JSA — Nature Portfolio highlights не просит).

## Пакет подачи

`python3 experiments/make_submission_package.py` собирает `manuscript/sn-manuscript/`:
`main.tex` и `supplement.tex` со всеми развёрнутыми `\input`, `refs.bib`, `main.bbl`,
`sn-jnl.cls`, `sn-nature.bst`, `figures/`. Именно эту папку загружать в редакцию.
