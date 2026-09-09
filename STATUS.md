# HCA-DSE — статус реализации (Gate 1-5 пройдены)

Дата: 2026-09-09. Target: Journal of Systems Architecture (Elsevier).

## Что уже работает
- `hcadse/model.py` — формальная модель: 3 tier (edge/gateway/cloud), классы узлов и
  каналов, 3 workload (telemetry / control / sensing), 4 масштаба design space
  S1=1 296, S2=5 832, S3=51 840, S4=345 600 кандидатов.
- `hcadse/evaluate.py` — полная (дорогая) оценка design point: M/M/1-очереди,
  latency по пути, энергия, стоимость, объём трафика + 6 типов constraints.
- `hcadse/bounds.py` — admissible нижние оценки LB(partial) для L/E/C/D,
  Proposition 1 (infeasibility pruning) и Proposition 2 (dominance pruning).
- `hcadse/search.py` — exhaustive ground truth, HCA-DSE (DFS по префиксному дереву),
  random baseline, Pareto extraction.
- `hcadse/metrics.py` — recall / precision / hypervolume / IGD+ (pymoo).
- `tests/test_core.py` — Gate 2 и Gate 5.

## Проверенные результаты (реальные прогоны, не оценки)
Bound admissibility: LB_i(partial) <= f_i(x) проверено исчерпывающе для ВСЕХ
префиксов и ВСЕХ 1 296 завершений на S1 x 3 workload — нарушений нет.

Точное сохранение Парето-множества (P_HCA == P_exhaustive по векторам целей):

| Scale | Workload  | \|X\|   | exhaustive evals | HCA evals | экономия |
|-------|-----------|--------:|-----------------:|----------:|---------:|
| S1    | telemetry |   1 296 |            1 080 |        31 |   97.1 % |
| S1    | control   |   1 296 |            1 080 |        34 |   96.9 % |
| S1    | sensing   |   1 296 |            1 080 |        18 |   98.3 % |
| S2    | telemetry |   5 832 |            3 888 |        47 |   98.8 % |
| S2    | control   |   5 832 |            3 888 |        49 |   98.7 % |
| S2    | sensing   |   5 832 |            3 888 |        24 |   99.4 % |
| S3    | telemetry |  51 840 |           34 560 |        53 |   99.85 %|
| S3    | control   |  51 840 |           34 560 |        63 |   99.82 %|
| S3    | sensing   |  51 840 |           34 560 |        41 |   99.88 %|
| S4    | telemetry | 345 600 |     (не считался)|        58 |        — |

S3: совпадение с exhaustive Парето-фронтом = True для всех трёх workload.

## Главная проблема, которую надо закрыть до сабмита
Экономия оценок ~99 %, но wall-clock speedup только 1.1-1.8x, потому что
аналитическая evaluation сама по себе дешёвая, а вычисление bounds стоит дорого.
Два действия:
1. кэшировать доменные min/max в bounds (ожидаемо 5-10x по времени HCA);
2. ввести модель стоимости оценки C_E (аналитика / discrete-event simulation /
   измерение на стенде) и показывать speedup как функцию C_E — это и есть
   реальный сценарий JSA (дорогая симуляция design point).
