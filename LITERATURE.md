# Literature review и позиционирование новизны (2026-09-09)

Поиск: Google/Scholar-запросы по multi-objective branch-and-bound DSE, exact Pareto
DSE, safe pruning в HW/SW co-design, edge/cloud design-time placement, обзоры DSE
для distributed CPS. Проверено, что ключевые работы существуют и прочитаны по
полным текстам (PDF), а не по абстрактам.

---

## 1. Главный вывод

**Идея "safe pruning частичных архитектур по admissible bounds" НЕ нова сама по
себе.** Она существует минимум в трёх формах: multi-objective branch-and-bound,
multi-objective A*/NAMOA* с допустимыми эвристиками, и символический exact DSE
(Neubauer/Haubelt). Если подавать HCA-DSE как "мы придумали безопасное отсечение",
рецензент JSA снимет статью за novelty.

**Что действительно свободно.** Все известные exact-подходы к DSE предполагают, что
цели *аддитивны по решениям* (каждое назначение добавляет стоимость/площадь/энергию).
Neubauer et al. прямо называют это условие *assignment monotonous* — только для таких
задач корректны dominance-проверки на неполных решениях. В heterogeneous edge-cloud
CPS главная цель — сквозная задержка — **contention-dependent**: она зависит от
загрузки тира, а загрузка определяется только после того, как назначены размещение,
репликация И количество узлов. Такая цель НЕ является assignment monotonous.

Отсюда формулировка, которую можно защищать:

> **Мы строим admissible bounds для contention-зависимых целей (задержка с
> очередями, энергия с загрузкой) над частичными архитектурами edge-cloud CPS и
> показываем, что exact Pareto preservation сохраняется; кроме того, мы
> количественно определяем, при какой стоимости оценки design point такое
> отсечение окупается.**

Второй, независимый вклад — **эмпирический**: у всех рассмотренных exact-работ
валидация чисто модельная. У нас 108 запусков на реальном контейнерном стенде,
согласие порядка 98 % на парах, разделённых моделью более чем на 25 %.

---

## 2. Кластеры prior art

### 2.1 Exact multi-objective DSE (самый опасный кластер)

**Neubauer, Wanko, Schaub, Haubelt. "Exact multi-objective design space exploration
using ASPmT." DATE 2018.** Символический подход (ASP modulo theories, clingo):
theory propagators проверяют ограничения и Парето-доминирование **на частичных
решениях** и возвращают conflict clauses — прямой аналог наших Proposition 1 и 2.
Модель: гетерогенные мультипроцессоры, задачи, маршрутизация; цели — latency, area,
energy. Масштаб: 30 инстансов до 166 задач / 200 сообщений. Ограничение, заявленное
авторами: "a complex communication model hinders the exploration performance
significantly" (при arbitrary length routing решение не найдено в 11 инстансах).

Как отличаться:
- их отсечение опирается на assignment-monotone цели; contention-зависимой задержки
  с очередями у них нет;
- у них solver-based символическое отсечение, у нас — замкнутые аналитические
  оценки, которые считаются за микросекунды и не требуют solver;
- у них дешёвая оценка design point внутри solver; мы явно нацелены на случай
  дорогого evaluator (симуляция) и даём кривую окупаемости.

**Cluster-соседи:** обзор Pareto-pruning методов (Computers & Industrial
Engineering, 2022) — показывает, что bound-based Pareto pruning это целое
семейство; multi-objective A*/NAMOA* с admissible heuristics — теоретический предок
Proposition 2. Обе группы обязательно цитировать, иначе выглядит как незнание поля.

### 2.2 DSE для distributed CPS (наш прямой контекст, и там есть цитируемый gap)

**Herget, Saadatmand, Bor, González Alonso, Stefanov, Akesson, Pimentel. "Design
Space Exploration for Distributed Cyber-Physical Systems: State-of-the-art,
Challenges, and Directions." Euromicro DSD 2022.** Прямая цитата для Introduction:

> "efficient and scalable DSE technology for dCPS is more or less non-existing and
> constitutes a largely unchartered research area"

и там же: "design point evaluations take longer for dCPS compared to classical DSE".
Это ровно наша посылка, причём сформулированная не нами.

**Saadatmand et al. "CompDSE." IET Cyber-Physical Systems, 2025.
doi:10.1049/cps2.70019.** Y-chart: workload / platform / mapping модели из трасс,
оценка через OMNeT++ (по их словам, "evaluating each design point takes under a
minute"), кейс ASML TWINSCAN: 8 хостов, 445 процессов, 2057 каналов, пространство
маппингов > 8^445. Ключевое: **"the primary focus of our work is on creating abstract
models"**, отсечения пространства нет, а интеграция поисковых алгоритмов "is out of
the scope of this paper". То есть CompDSE — это дорогой evaluator без стратегии
обхода, а HCA-DSE — стратегия обхода для дорогого evaluator. Формулировка для
Discussion: CompDSE отвечает "как оценить design point", HCA-DSE — "какие design
points не оценивать вовсе". При C_E около 60 с наша кривая окупаемости даёт
выигрыш в сотни раз.

**Xiao, Oh, Lora, Nuzzo. "ContrArc: Contract-Based Architecture Exploration."
DATE 2024.** MILP + проверка refinement контрактов + отсечение изоморфных подграфов.
Одноцелевая (минимизация стоимости при ограничениях), Парето-фронт не строится.
Отличие очевидно и его легко сформулировать.

### 2.3 Design-time размещение в edge-cloud continuum

**Sedghani, Filippini, Ardagna. "SPACE4AI-D: A Design-Time Tool for AI Applications
Resource Selection in Computing Continua." IEEE Trans. (2024).** Ближайшая работа по
постановке задачи: design-time выбор ресурсов и размещения компонентов на
edge/cloud/FaaS. Но: MINLP, **одноцелевая** (минимум стоимости при QoS-ограничениях),
решается эвристиками (random greedy, local search, tabu, SA, GA), exact-гарантий нет.
Валидация: 7 компонентов на Raspberry Pi / Odroid / EC2 / Lambda, отклонение
предсказания 12 % по стоимости и 20 % по времени выполнения.

Это, кстати, полезный ориентир для нашей точности: у них 20 % по времени на реальном
развёртывании, у нас MAPE 15.7-20.3 % на control/telemetry — то есть мы в том же
диапазоне, что уже опубликовано в рецензируемом IEEE-журнале. **Это надо явно
написать в Discussion** — снимает претензию "MAPE 29 % это много".

### 2.4 Эволюционные и метаэвристические DSE

Многочисленные NSGA-II/MOEA работы по task allocation и offloading в edge-cloud
(FGCS 2024, Simulation Modelling Practice 2025 и т. д. — уже в вашем списке).
Позиционирование: они approximate при фиксированном бюджете оценок; наш NSGA-II
baseline (20 seeds, бюджеты 100-1000) это подтверждает численно, и вывод не
"NSGA-II плохой", а "exactness достижима, когда есть admissible bounds".

---

## 3. Таблица различий (черновик Table 1)

| Работа | Класс системы | Целей | Exact Pareto | Отсечение | Contention-зависимые цели | Дорогой evaluator учтён | Реальные измерения |
|---|---|---|:--:|---|:--:|:--:|---|
| Neubauer et al., DATE 2018 | гетерогенный MPSoC | 3 | да | символическое, conflict clauses на частичных решениях | нет (assignment monotone) | нет | нет |
| CompDSE, IET CPS 2025 | industrial dCPS | perf. | — | нет | да (симуляция) | нет (нет поиска) | промышленные трассы |
| ContrArc, DATE 2024 | CPS архитектуры | 1 | — | MILP + изоморфизм подграфов | нет | нет | нет |
| SPACE4AI-D, IEEE 2024 | edge-cloud continuum | 1 | нет | эвристики | частично | нет | да (7 компонентов) |
| NSGA-II/MOEA (2024-2025) | edge-cloud | 2-4 | нет | нет | частично | нет | обычно нет |
| **HCA-DSE (наша)** | гетерогенный edge-cloud CPS | 4 | **да, проверено против exhaustive** | иерархическое: структурное + feasibility + dominance по admissible bounds | **да** | **да, кривая окупаемости по C_E** | **да, 108 запусков, rho = 0.97** |

---

## 4. Что рецензент спросит и что отвечать

**"Это просто multi-objective branch-and-bound."** Да, семейство то же. Вклад — в
построении admissible bounds для contention-зависимых целей, где стандартное
условие assignment monotonicity не выполняется, и в доказательстве, что exactness
при этом сохраняется. Плюс исчерпывающая проверка admissibility и совпадение с
exhaustive на S1-S3.

**"Почему не MILP / epsilon-constraint, почему не ASPmT?"** Это самый опасный
вопрос, и сейчас у нас на него нет экспериментального ответа. Формулировка задачи
содержит нелинейные члены (rho/(2(1-rho)) от загрузки, которая сама дробно-линейна
по числу узлов), поэтому прямая MILP-формулировка требует линеаризации и теряет
точность модели. **Рекомендация: добавить в Related Work явный параграф об этом, а в
Experiments — либо epsilon-constraint MILP на линеаризованной версии как ещё один
baseline, либо честно вынести это в Limitations.** Я бы сделал параграф + Limitations;
полноценный MILP-baseline это +2-3 недели.

**"MAPE 29 % — модель неточная."** Ответ: (1) главная метрика для DSE — порядок, а не
абсолют: 98 % согласия на парах, разделённых более чем на 25 %; (2) опубликованный
SPACE4AI-D даёт 20 % отклонения по времени на реальном развёртывании — мы в том же
диапазоне; (3) смещение для sensing систематическое (~0.70), а не случайное.

**"Пространство искусственное."** Ответ: экспериментальная часть покрывает 4 масштаба
до 8.3e7 логических кандидатов, три качественно разных workload, и проверена против
exhaustive там, где exhaustive вычислим.

---

## 5. Что изменить в тексте статьи прямо сейчас

1. Introduction строить от цитаты DSD 2022 ("more or less non-existing") и от того,
   что в dCPS оценка design point дорогая (подтверждается CompDSE: до минуты на точку).
2. Novelty statement заменить на формулировку из раздела 1 (contention-dependent
   admissible bounds), нигде не заявлять изобретение safe pruning.
3. Обязательно процитировать: Neubauer DATE 2018; обзор Pareto pruning 2022;
   NAMOA*/multi-objective A*; DSD 2022; CompDSE 2025; ContrArc 2024; SPACE4AI-D 2024.
4. В Discussion добавить сравнение точности с SPACE4AI-D (12 % / 20 %).
5. В Limitations добавить: отсутствие MILP/symbolic exact baseline и нестабильность
   измерений вблизи rho >= 0.75.

---

## 6. Библиография (проверенные ссылки)

- K. Neubauer, P. Wanko, T. Schaub, C. Haubelt. Exact multi-objective design space
  exploration using ASPmT. DATE 2018. https://ieeexplore.ieee.org/document/8342014/
  (PDF: https://www.cs.uni-potsdam.de/wv/publications/DBLP_conf/date/NeubauerWSH18.pdf)
- C. Haubelt, K. Neubauer, T. Schaub, P. Wanko. Design Space Exploration with Answer
  Set Programming. KI - Künstliche Intelligenz 32:205-206, 2018.
  doi:10.1007/s13218-018-0530-3
- M. Herget, M. Saadatmand, M. Bor, I. González Alonso, T. Stefanov, B. Akesson,
  A. Pimentel. Design Space Exploration for Distributed Cyber-Physical Systems:
  State-of-the-art, Challenges, and Directions. Euromicro DSD 2022.
  https://ieeexplore.ieee.org/document/9996862/
  (PDF: https://liacs.leidenuniv.nl/~stefanovtp/pdf/DSD_22.pdf)
- M. Saadatmand et al. CompDSE: A Methodology for Design Space Exploration of
  Computing Subsystems Within Complex Cyber-Physical Systems. IET Cyber-Physical
  Systems: Theory & Applications, 2025. doi:10.1049/cps2.70019
- Y. Xiao, C. Oh, M. Lora, P. Nuzzo. ContrArc: Contract-Based Architecture
  Exploration. DATE 2024.
  https://past.date-conference.com/proceedings-archive/2024/DATA/664_pdf_upload.pdf
- H. Sedghani, F. Filippini, D. Ardagna. SPACE4AI-D: A Design-Time Tool for AI
  Applications Resource Selection in Computing Continua. IEEE, 2024.
  https://ieeexplore.ieee.org/document/10715700/
- A review of Pareto pruning methods for multi-objective optimization. Computers &
  Industrial Engineering, 2022.
  https://www.sciencedirect.com/science/article/abs/pii/S0360835222000924
- Multi-objective A* / NAMOA* с допустимыми эвристиками (Stewart & White;
  Mandow & Pérez-de-la-Cruz) — теоретический предок Proposition 2; точные выходные
  данные подставить при оформлении списка литературы.
- Pareto optimal design space exploration of cyber-physical systems.
  https://www.sciencedirect.com/science/article/pii/S2542660520301402
