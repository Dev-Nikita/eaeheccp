# Supplementary material (описание для сабмита)

Основная статья содержит агрегированные результаты. В supplementary/replication package
входит следующее.

## S1. Код
`hcadse/` — модель, аналитический evaluator, admissible bounds (референсная и кэшированная
реализации), поиск (exhaustive / HCA-DSE / random), NSGA-II baseline, метрики,
discrete-event evaluator.

## S2. Эксперименты и сырые результаты
`experiments/e1..e8`, `results/*.csv`:

| Файл | Содержание |
|---|---|
| e1_pruning.csv | воронка отсечения по всем масштабам и workload |
| e2_costsweep.csv | проекция ускорения по стоимости evaluation |
| e3_baselines.csv | 972 строки: все seeds, бюджеты, recall/HV/IGD+/время |
| e4_ablation.csv | вклад каждого уровня отсечения |
| e5_scalability.csv | до 8.3e7 логических кандидатов |
| e6_simvalidation.csv | аналитическая модель против DES |
| e7_calibration.csv | линейная калибровка на holdout |
| e8_stats.csv | Mann-Whitney U и Cliff's delta по 20 seeds |
| e9_testbed.csv | 108 запусков на Docker-стенде |
| e9_per_design_docker.csv | агрегаты по архитектурам, включая разброс повторов |
| e9_testbed_local*.csv | namespace-вариант стенда и сравнение M/M/1 против M/D/1 |

## S3. Стенд
`testbed/`: Go-сервисы, Dockerfile, генерация compose-топологии на архитектуру,
`tc netem` профили, раннеры для Docker и для network namespace, анализ.

## S4. Проверки корректности
`tests/test_core.py` — исчерпывающая проверка admissibility bounds;
`tests/test_pruning_safety.py` — для каждого отсечённого префикса перебираются все
завершения и проверяется утверждение соответствующего предложения;
`tests/test_regression.py` — равенство фронтов и совпадение кэшированных оценок с
референсными.

## S5. Воспроизведение таблиц и рисунков
`python3 experiments/make_paper_assets.py` заново собирает все `manuscript/figures/*.pdf`
и `manuscript/tables/*.tex` из CSV. Ни одно число в статье не набрано вручную.

## S6. Окружение
Python 3.10+, NumPy, SciPy, pymoo, matplotlib; Go 1.22 и Docker Compose для стенда.
Измерения стенда получены на MacBook Pro (Docker Desktop) и на Linux-VM для
namespace-варианта.
