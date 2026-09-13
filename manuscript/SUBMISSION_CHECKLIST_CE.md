# Чек-лист перед подачей в Communications Engineering

Статус на 2026-09-13. Отмечайте по мере закрытия.

## Готово
- [x] структура Introduction → Results → Discussion → Methods → Declarations → References;
- [x] основной текст до Methods 3 416 слов (лимит ~5 000), 10 display items (лимит 10);
- [x] abstract ~205 слов, без ссылок и аббревиатур;
- [x] нумерация строк (опция класса `lineno`);
- [x] Declarations: Data availability, Code availability, Author contributions, Funding,
      Competing interests;
- [x] 41 цитируемый источник, у конференций видно venue (исправлена функция
      `format.in.ed.booktitle` в `sn-nature.bst`, из-за которой BibTeX падал и ссылки
      выводились как `???`);
- [x] Supplementary Information: Notes 1–2 + Tables S1–S13, ссылки из main совпадают;
- [x] аудит числовых утверждений `python3 experiments/check_claims.py` — проходит;
- [x] сборка без ошибок: main 19 стр., supplement 8 стр., 0 undefined, нет overfull > 10 pt;
- [x] Zenodo DOI 10.5281/zenodo.22729667 и GitHub Dev-Nikita/eaeheccp вписаны в Data
      availability и Code availability; ORCID обоих авторов — в титульном блоке;
- [x] добавлено заявление «Use of AI tools» (только языковая правка, без генерации
      содержания, кода или результатов);
- [x] канонический порядок переменных в коде и в тексте совпадает (determinants-early);
      все числа main и SI пересчитаны из одного набора результатов;
- [x] чистая папка подачи `manuscript/sn-manuscript/`: main.tex, supplement.tex,
      refs.bib, sn-jnl.cls, sn-nature.bst, figures/ — все \input развёрнуты,
      генерируется `python3 experiments/make_submission_package.py`;
- [x] cover letter переписан под CE (~400 слов, без bold-заголовков, с абзацем про fit и
      с фразой о том, что работа заранее не обсуждалась с редактором).

## Осталось сделать вам
- [ ] **ORCID** обоих авторов ввести в самой системе подачи (в тексте они уже стоят);
- [ ] **опечатать новый релиз результатов на Mac** (там есть z3 и Python 3.12):
      `python3 experiments/reproduce.py --release v1.2-canonical-order --testbed results/e9_testbed_round2.csv`,
      затем `python3 experiments/verify_manuscript_numbers.py`. Сейчас числа в рукописи
      взяты из живой папки `results/`, а запечатанный релиз `v1.1-submission-results`
      относится к прежнему порядку переменных;
- [ ] после опечатывания обновить версию архива на Zenodo (новый DOI версии, concept DOI
      10.5281/zenodo.22729667 остаётся прежним);
- [ ] прогон воспроизведения с чистого клона: `python3 tests/test_regression.py`,
      `python3 tests/test_pruning_safety.py`, `python3 experiments/make_paper_assets.py`,
      затем пересборка обоих PDF;
- [ ] проверить DOI и метаданные всех 41 источника (см. `BIBLIOGRAPHY_AUDIT.md`);
      отдельно: ссылка на препринт arXiv 2026 — не вышла ли уже журнальная версия;
- [ ] сверить Author contributions с реальным вкладом соавтора;
- [ ] исходники рисунков: у CE требуется загрузка figure source files (PDF/EPS — у нас
      векторные PDF в `manuscript/figures/`, они подойдут);
- [ ] Supplementary файл назвать по требованию системы (обычно
      `Supplementary Information.pdf`);
- [ ] решить вопрос APC (~€1990) или waiver — заявляется на этапе подачи, не после.

## Формулировки, которые нельзя усиливать при подаче
- не «physically validated multi-objective model», а «physically validated latency
  ranking within a four-objective analytical framework»: энергия и стоимость
  измерениями не проверялись;
- не «works for robotics / industrial edge», а «the mechanism applies to problems of
  this shape; demonstrated on one template»;
- не «measured speed-up 771×», а «projected from the measured evaluator cost».
