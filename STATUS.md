# HCA-DSE — статус (Gates 1-9 пройдены; осталcя testbed)

Target: Journal of Systems Architecture (Elsevier). Обновлено 2026-09-09.

## Терминология (важно для рукописи)
Везде пишем **"reduction in full design-point evaluations"**, а НЕ "computational
saving": экономия времени зависит от стоимости evaluation и отражена отдельно (E2).

## Gate 1-5 (зафиксировано тегом v0.1-exact-pruning)
Модель, аналитический evaluator, admissible bounds, HCA-DSE, exhaustive ground truth.
- Bound admissibility: LB_i(partial) <= f_i(x) проверено исчерпывающе (S1 x 3 workload,
  все префиксы x все завершения) — 0 нарушений.
- P_HCA = P_exhaustive на S1-S3 для всех workload и для всех вариантов pruning.

## Gate 6 — профилирование и кэшированные bounds
Профиль до оптимизации: bounds 74 % времени. Введён `hcadse/bounder.py` (мемоизация
всех термов, зависящих только от достижимых классов). Регрессия
`cached == reference` в тестах. Wall-clock speedup при дешёвом аналитическом
evaluator вырос с 1.3x до **2.1-3.3x** (S3), exactness сохранена.
Остаточный профиль S3: bounds ~50 %, dominance ~37 %, full evaluation < 1 %.

## Gate 6b — когда pruning реально окупается (E2)
T(C_E) = overhead + N_eval * C_E, overhead и N_eval измерены.
- Break-even стоимость evaluation: **1-3 мкс** (то есть выигрыш есть практически
  для любого нетривиального evaluator).
- Реально измеренная стоимость discrete-event evaluator: **19.5 мс/design point**.
  При ней на S1: T_exhaustive = 21.1 с против T_HCA = 0.6 с → **34x**;
  на S3 отношение N_eval 34 560 / 53 даёт ~2 орядка.

## Gate 7 — сравнение с baselines (E3, 20 seeds, S2 и S3)
| Метод | Бюджет | Recall (медиана) | HV ratio | IGD+ |
|---|---:|---:|---:|---:|
| random | 1000 | 0.00-0.20 | 0.48-0.88 | 0.07-0.14 |
| NSGA-II | 500 | 0.19-0.26 | 0.77-0.84 | 0.06-0.08 |
| NSGA-II | 1000 | 0.64-0.96 | 0.94-0.999 | 0.0002-0.086 |
| **HCA-DSE** | **24-64 оценок** | **1.00** | **1.00** | **0** |
Статистика (E8): Mann-Whitney U + Cliff's delta для NSGA-II vs random по 20 seeds.
Формулировка для статьи: NSGA-II даёт approximate front при фиксированном бюджете;
HCA-DSE даёт exact front, когда admissible bounds доступны.

## Gate 8 — ablation (E4, S3)
| Вариант | full evaluations (telemetry) | exact |
|---|---:|:--:|
| structural only | 34 560 | да |
| struct + feasibility bounds | 12 487 | да |
| struct + dominance | 325 | да |
| **HCA-full** | **53** | да |
Вывод: основной вклад даёт dominance pruning, но feasibility bounds сокращают его
работу ещё в 6 раз. Сигнатуры pruning различаются по workload (sensing — bound-driven,
telemetry — dominance-driven), что и нужно для Discussion.

## Gate 9 — масштабируемость (E5)
Пространство никогда не материализуется.
| raw \|X\| | посещено partial states | full evals | время | пик памяти |
|---:|---:|---:|---:|---:|
| 1 296 | 658 | 42 | 0.07 с | 86 KiB |
| 51 840 | 7 290 | 59 | 0.94 с | 51 KiB |
| 345 600 | 10 345 | 60 | 1.39 с | 55 KiB |
| **82 944 000** | **16 847** | **58** | **1.9 с** | **80 KiB** |
Доля посещённых состояний падает с 0.51 до 2.0e-4.

## Внутренняя валидация модели (E6/E7)
Аналитическая модель против discrete-event simulation (5 повторов, 35-40 архитектур):
| workload | MAPE | Spearman rho |
|---|---:|---:|
| telemetry | 42.5 % | 0.923 |
| control | 50.8 % | 0.962 |
| sensing | 20.8 % | 0.951 |
Линейная калибровка (holdout 50/50) помогает для telemetry (44 -> 17 %) и control
(52 -> 9 %), но ухудшает sensing (15 -> 52 %) — то есть калибровка не переносится
между режимами, а переносится **ранжирование**. Это и есть тезис для Discussion:
для DSE достаточно корректного порядка архитектур.

## Что осталось до manuscript v0.1
1. Docker/Go testbed (Gate 10) — 30-60 архитектур, p50/p95, MAPE, Spearman.
2. Literature review по multi-objective branch-and-bound DSE / safe Pareto pruning
   в HW/SW co-design (JSA, TECS, TCAD, DATE, DAC) — зафиксировать реальную новизну.
3. Формальные Proposition 1, Proposition 2, Theorem 1 (Pareto preservation) с proofs.

## Файлы
`results/e1_pruning.csv, e2_costsweep.csv, e3_baselines.csv, e4_ablation.csv,
e5_scalability.csv, e6_simvalidation.csv, e7_calibration.csv, e8_stats.csv`
`figures/fig1..fig6 .png`; тесты: `tests/test_core.py`, `tests/test_regression.py`.
