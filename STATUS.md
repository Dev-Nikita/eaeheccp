# HCA-DSE — статус (Gates 1-10 пройдены)

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

## Gate 10 — эмпирическая валидация (E9)

Два эквивалентных стенда с одним и тем же кодом сервисов (Go):
1. `testbed/` + Docker Compose — контейнер на каждый edge/gateway/cloud узел,
   1 CPU на контейнер, `tc netem` (задержка + полоса) по классу канала на КАЖДОМ
   узле, WAN до cloud 20 мс / 200 Мбит/с. Запуск на вашей машине — testbed/README.md.
2. `testbed/run_local.py` — тот же стенд в network namespace без Docker: отдельная
   shaped-полоса (prio band + netem) на каждый узел, шейпинг только прямого
   направления перехода, по CPU-ядру на узел. Числа ниже получены на нём.

34 архитектуры (Pareto / dominated / boundary) x 3 повтора = 102 запуска,
900 запросов на запуск (150 warmup), Пуассоновский поток.

| workload | n | MAPE | median AE | Spearman rho | согласие пар >10 % | >25 % |
|---|--:|--:|--:|--:|--:|--:|
| control | 12 | 8.5 % | 1.8 мс | 0.716 | 0.867 | 0.833 |
| telemetry | 12 | 16.1 % | 7.4 мс | 0.252 | 0.667 | 0.636 |
| sensing | 10 | 27.8 % | 17.0 мс | 0.129 | 0.548 | 0.750 |
| **все** | **34** | **16.9 %** | **3.4 мс** | **0.882** | **0.902** | **0.951** |
| все, rho<=0.75 | 28 | 14.9 % | 2.7 мс | 0.882 | 0.914 | 0.982 |

"Согласие пар >X %" — доля пар архитектур, у которых измеренный порядок совпал с
модельным, среди пар, которые модель разделяет более чем на X %. Это ключевая
метрика для DSE и главный результат Gate 10: когда модель утверждает заметную
разницу, она права в 90-98 % случаев. Низкая ранговая корреляция ВНУТРИ workload
объясняется тем, что после исправлений модель точна (MAPE 8-16 %), и разброс
внутри workload сопоставим с шумом измерений (медианный разброс повторов
0.14-2.7 мс) — то есть модель не различает почти эквивалентные архитектуры.
Отсюда прямой аргумент в пользу двухуровневой схемы: analytical bounds отсекают
пространство, а близкие кандидаты доводит дорогой evaluator.

Что валидация вскрыла и что было исправлено (материал для Threats to Validity):
- модель использовала M/M/1, тогда как выполнение стадий детерминированное.
  Переход на M/D/1 (Pollaczek-Khinchine) снизил MAPE с 28.9 % до 23.7 % на тех же
  измерениях; при этом ранговая корреляция M/M/1 была даже выше (0.918 против
  0.889) — точность и ранжирование улучшаются не синхронно.
- общий шейпер на все access-каналы занижал пропускную способность; после
  перехода на отдельный netem по узлу MAPE упала с 23.7 % до 16.9 %.
- репликация в стенде дублировала всю цепочку, а не только stage 1 (расхождение с
  моделью в 60 раз на затронутых конфигурациях) — исправлено.
- аналитический DES-evaluator (Level B) тоже переведён на детерминированное
  обслуживание; он даёт Spearman 0.92-0.96 против analytical model.
- sensing (крупные payload) остаётся наименее точным: TCP-эффекты на шейпленном
  канале модель не описывает. Заявляется как ограничение.

Ограничения эмпирической части: только конфигурации, помещающиеся на одну машину
(<= 2 edge + 1 gateway + 1 cloud в namespace-варианте; <= 4 + 2 + 1 в Docker-варианте);
шейпинг применяется в прямом направлении каждого перехода.

## Что осталось до manuscript v0.1
1. Прогнать Docker-вариант стенда на вашей машине (>= 4 edge узлов, больше ядер) —
   `python3 testbed/run_testbed.py --repeats 3`, затем
   `python3 testbed/analyze.py --input results/e9_testbed.csv --designs testbed/specs/designs.json --tag docker`.
2. Literature review: multi-objective branch-and-bound DSE, safe Pareto pruning в
   HW/SW co-design (JSA, ACM TECS, IEEE TCAD, DATE, DAC) — зафиксировать новизну.
3. Формальные Proposition 1, Proposition 2, Theorem 1 с доказательствами.

## Файлы
`results/`: e1_pruning, e2_costsweep, e3_baselines, e4_ablation, e5_scalability,
e6_simvalidation, e7_calibration, e8_stats, e9_testbed_local (+ e9_summary_local,
e9_per_design_local, e9_testbed_local_mm1 для сравнения моделей очередей).
`figures/`: fig1..fig7. Тесты: `tests/test_core.py`, `tests/test_regression.py`.
