# Воспроизведение HCA-DSE

Канонический набор статьи: `results/v1.1-submission-results/data/`.
`manifest.json` фиксирует SHA-256 исходников и данных, окружение и время выполнения.
`source/` — отдельная копия исходников, реально использованная для расчёта; `logs/` — журналы.
CSV непосредственно в `results/` являются историческими и не используются статьёй.

## Окружение

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-lock.txt
```

Зафиксированное окружение использует Python 3.12. Для сборки PDF требуется TeX Live/MacTeX
с elsarticle; для стенда — запущенный Docker Desktop с Compose и Linux network shaping.

## Проверить и пересобрать текущий результат

```bash
make assets
make verify
cd manuscript
latexmk -pdf main.tex
latexmk -pdf supplement.tex
```

`verify` повторно вычисляет детерминированные счётчики, проверяет реальные бюджеты всех
960 stochastic runs, пересчитывает статистические сравнения и проверяет хеши.
Точные сравнения фронтов S1–S3 входят в полный прогон. Времена, память и физические
измерения не обязаны совпадать побитно.

## Новый независимый полный прогон

Сохранённый release не перезаписывается. Для нового прогона задайте новое имя:

```bash
make reproduce RELEASE=verification-run
```

Команда создаёт новую копию исходников, выполняет correctness tests и E1–E8, E10, E11,
проверяет результаты и сохраняет неизменяемый manifest. Ожидаются те же дискретные
счётчики и результаты при фиксированных исходниках/версиях; времена будут отличаться.
Экспериментальные скрипты запускаются последовательно, без конкурирующих CPU-нагрузок.

Для независимого Docker round сохраните фиксированный `testbed/specs/designs.json`:

```bash
python3 testbed/run_testbed.py --repeats 3 --run-dir testbed/run-validation \
  --out /private/tmp/hcadse-validation.csv
make reproduce RELEASE=validation-run TESTBED=/private/tmp/hcadse-validation.csv
make assets RELEASE=validation-run
```

При необходимости отдельного Buildx state используйте
`BUILDX_CONFIG=/private/tmp/hcadse-buildx` перед Docker-командой.
Вначале выполняется Docker round, затем computational run, чтобы не смешивать нагрузки.
Раннер не повторно подбирает модель или конфигурации. Все 108 успешных повторов обязательны
для анализа; неудачные измерения не отбрасываются молча. Строятся отдельные summaries
для mean и p50. `make assets` для полного manuscript требует release с testbed-данными.

Артефакты документа находятся в `manuscript/`; генераторы читают только выбранный
release через `HCADSE_RESULTS`. При смене release пересоберите оба PDF.
