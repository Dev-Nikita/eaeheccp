# Как запустить — по шагам

Все команды выполняются в **Terminal.app на Mac** (не в Claude). Путь с пробелами,
поэтому кавычки обязательны.

```bash
cd "/Users/nikitatarasov/Science Article 2025-/Hierarchical Constraint-Aware Design-Space"
```

---

## Шаг 0. Проверка окружения (10 секунд)

```bash
python3 -V && docker info >/dev/null 2>&1 && echo "Docker OK" || echo "ЗАПУСТИТЕ Docker Desktop"
```

Нужен Python 3.9+ и запущенный Docker Desktop. Больше ничего ставить не нужно:
`run_testbed.py` использует только стандартную библиотеку.

---

## Шаг 1. Что уже посчитано (ничего запускать не надо)

Всё, что относится к самому методу, уже прогнано мной и лежит в `results/` и
`figures/`. Проверить, что расчёты воспроизводятся, можно так (~3 минуты):

```bash
python3 tests/test_regression.py      # P_HCA == P_exhaustive на S1-S3
python3 tests/test_core.py            # исчерпывающая проверка корректности bounds
```

Для этих двух команд ничего кроме Python не нужно.

---

## Шаг 2. Единственное, что осталось запустить: стенд на Docker

Он даст те же измерения, что я снял, но на большем числе ядер — войдут
конфигурации до 4 edge + 2 gateway вместо 2 + 1.

```bash
python3 testbed/select_designs.py --max-edge 4 --max-gw 2 --out testbed/specs/designs.json
python3 testbed/run_testbed.py --repeats 3
```

- первая команда: выбирает 36 архитектур (Pareto / dominated / boundary), ~5 сек;
- вторая: собирает Docker-образ и прогоняет 36 x 3 = 108 запусков, **40-70 минут**.

Прогресс печатается построчно (`model=… measured p50=…`). Прогон можно прервать
Ctrl+C и запустить ту же команду позже — уже сделанные запуски пропускаются.
Результат пишется в `results/e9_testbed.csv`.

Если Docker жалуется на нехватку ресурсов: Docker Desktop → Settings → Resources,
поставьте не меньше 6 CPU и 6 GB RAM.

---

## Шаг 3. Анализ

Скажите мне «стенд отработал» — CSV лежит в общей папке, и я сам построю MAPE,
Spearman, согласие пар и рисунок. Если хотите сделать это сами, нужны две
библиотеки:

```bash
pip3 install --user scipy matplotlib
python3 testbed/analyze.py --input results/e9_testbed.csv \
        --designs testbed/specs/designs.json --tag docker
```

---

## Необязательное: пересчитать всё остальное самому

Нужны `numpy pandas scipy matplotlib pymoo`:

```bash
pip3 install --user numpy pandas scipy matplotlib pymoo
python3 experiments/e1_pruning.py        # воронка отсечения, ~1 мин
python3 experiments/e2_costsweep.py      # окупаемость по стоимости evaluation
python3 experiments/e3_baselines.py      # NSGA-II и random, 20 seeds, ~10 мин
python3 experiments/e4_ablation.py       # вклад каждого уровня отсечения
python3 experiments/e5_scalability.py    # до 8.3e7 кандидатов
python3 experiments/e6_simvalidation.py  # модель против DES
python3 experiments/e8_stats.py          # Mann-Whitney U, Cliff's delta
python3 experiments/make_figures.py      # figures/fig1..fig6
```

---

## Что где лежит

| Путь | Что это |
|---|---|
| `hcadse/` | сам метод: модель, evaluator, bounds, поиск, метрики |
| `experiments/` | эксперименты E1-E8 |
| `testbed/` | стенд: Go-сервисы, Dockerfile, раннеры, анализ |
| `results/` | все CSV с результатами |
| `figures/` | рисунки fig1-fig7 |
| `STATUS.md` | текущий статус со всеми числами |
| `RUN.md` | этот файл |
