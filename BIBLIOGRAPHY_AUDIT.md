# Аудит библиографии — 9 сентября 2026

Проверено 30 записей в refs.bib (не все цитируются). Все 27 DOI текущей библиографии
возвращают метаданные, соответствующие названию работы. Проверка выполнена через
DOI content negotiation (CSL JSON); HTTP 200 означает доступность записи метаданных,
а не гарантированный доступ к полному тексту. Исходные ответы сохранены в review/.

## Исправленные ошибки

- Herget 2022: DOI оканчивался на 00068 вместо 00090; исправлено имя Faezeh Sadat Saadatmand, добавлены страницы 632–640.
- SPACE4AI-D: DOI 3479926 вёл на Tango. Исправлен на 3479935; добавлены 17(6), 4324–4339 по университетскому архиву.
- Lukasiewycz 2008: 4484047 вёл на работу об NBTI. Правильный DOI: 4484040.
- Haubelt/Teich 2003: 1119876 вёл на carry select adder. Правильный DOI: 1119882.
- CompDSE: удалён placeholder, исправлен неверный первый автор, добавлены все пять авторов и 10(1):e70019.
- ContrArc: заменено неверное название работы, добавлены DOI и страницы 1–6.
- Kouloumpris 2026: оформлена опубликованная статья FGCS 180:108414 вместо смеси journal/preprint; это подтверждает [авторская запись arXiv](https://arxiv.org/abs/2602.18158).
- Palermo 2005: добавлен существующий DOI.
- Y-chart и IGD+: исправлены типы записей (глава / конференционная работа).
- Добавлена непосредственно релевантная работа Neubauer et al. 2020 о consistent approximations. Произвольное расширение до 40–50 ссылок не выполнялось.

## Результаты по каждой записи

| Ключ | Ссылка | Проверка |
|---|---|---|
| neubauer2018exact | [DOI](https://doi.org/10.23919/DATE.2018.8342014) | 200; Exact multi-objective design space exploration using ASPmT |
| haubelt2018asp | [DOI](https://doi.org/10.1007/s13218-018-0530-3) | 200; Design Space Exploration with Answer Set Programming |
| herget2022dse | [DOI](https://doi.org/10.1109/DSD57027.2022.00090) | 200; Design Space Exploration for Distributed Cyber-Physical Systems: State-of-the-art, Challenges, and Directions |
| saadatmand2025compdse | [DOI](https://doi.org/10.1049/cps2.70019) | 200; CompDSE: A Methodology for Design Space Exploration of Computing Subsystems Within Complex Cyber‐Physical Systems |
| xiao2024contrarc | [DOI](https://doi.org/10.23919/DATE58400.2024.10546764) | 200; Efficient Exploration of Cyber-Physical System Architectures Using Contracts and Subgraph Isomorphism |
| sedghani2024space4aid | [DOI](https://doi.org/10.1109/TSC.2024.3479935) | 200; SPACE4AI-D: A Design-time Tool for AI applications Resource Selection in Computing Continua |
| deb2002nsga2 | [DOI](https://doi.org/10.1109/4235.996017) | 200; A fast and elitist multiobjective genetic algorithm: NSGA-II |
| blank2020pymoo | [DOI](https://doi.org/10.1109/ACCESS.2020.2990567) | 200; Pymoo: Multi-Objective Optimization in Python |
| paretopruning2022 | [DOI](https://doi.org/10.1016/j.cie.2022.108022) | 200; A review of Pareto pruning methods for multi-objective optimization |
| mandow2010namoa | [DOI](https://doi.org/10.1145/1754399.1754400) | 200; Multiobjective A * search with consistent heuristics |
| stewart1991moa | [DOI](https://doi.org/10.1145/115234.115368) | 200; Multiobjective A* |
| kienhuis2002ychart | [DOI](https://doi.org/10.1007/3-540-45874-3_2) | 200; A Methodology to Design Programmable Embedded Systems |
| pimentel2017exploring | [DOI](https://doi.org/10.1109/MDAT.2016.2626445) | 200; Exploring Exploration: A Tutorial Introduction to Embedded Systems Design Space Exploration |
| palermo2005mo | [DOI](https://doi.org/10.3233/EMC-2005-00034) | 200; Multi-objective design space exploration of embedded systems |
| kleinrock1975queueing | без DOI | См. ограничения ниже |
| zitzler1999hv | [DOI](https://doi.org/10.1109/4235.797969) | 200; Multiobjective evolutionary algorithms: a comparative case study and the strength Pareto approach |
| ishibuchi2015igdplus | [DOI](https://doi.org/10.1007/978-3-319-15892-1_8) | 200; Modified Distance Calculation in Generational Distance and Inverted Generational Distance |
| cliff1993delta | [DOI](https://doi.org/10.1037/0033-2909.114.3.494) | 200; Dominance statistics: Ordinal analyses to answer ordinal questions. |
| mann1947whitney | [DOI](https://doi.org/10.1214/aoms/1177730491) | 200; On a Test of Whether one of Two Random Variables is Stochastically Larger than the Other |
| varga2008omnet | [DOI](https://doi.org/10.4108/ICST.SIMUTOOLS2008.3027) | 200; AN OVERVIEW OF THE OMNeT++ SIMULATION ENVIRONMENT |
| hemminger2005netem | без DOI | См. ограничения ниже |
| lukasiewycz2008symbolic | [DOI](https://doi.org/10.1109/ASPDAC.2008.4484040) | 200; Efficient symbolic multi-objective design space exploration |
| haubelt2003pareto | [DOI](https://doi.org/10.1145/1119772.1119882) | 200; Accelerating design space exploration using pareto-front arithmetics |
| kouloumpris2024optimization | [DOI](https://doi.org/10.1016/j.future.2024.02.005) | 200; An optimization framework for task allocation in the edge/hub/cloud paradigm |
| kouloumpris2026reliability | [DOI](https://doi.org/10.1016/j.future.2026.108414) | 200; A reliability- and latency-driven task allocation framework for workflow applications in the edge-hub-cloud continuum |
| audet2021indicators | [DOI](https://doi.org/10.1016/j.ejor.2020.11.016) | 200; Performance indicators in multiobjective optimization |
| harchol2013performance | [DOI](https://doi.org/10.1017/CBO9781139226424) | 200; Performance Modeling and Design of Computer Systems |
| blickle1998system | [DOI](https://doi.org/10.1023/A:1008899229802) | 200; System-Level Synthesis Using Evolutionary Algorithms |
| sedlak2026orchestration | без DOI | arXiv проверен |
| neubauer2020consistent | [DOI](https://doi.org/10.3390/electronics9071057) | 200; Exact Design Space Exploration Based on Consistent Approximations |

## Ограничения и содержательная проверка

- Kleinrock 1975: книга существует; сведения подтверждает [рецензия издателя](https://onlinelibrary.wiley.com/doi/abs/10.1002/net.3230060210). DOI рецензии не присвоен книге.
- Hemminger 2005: автор, название и дата подтверждаются оригинальным текстом и [документацией netem](https://manpages.ubuntu.com/manpages/resolute/man8/tc-netem.8.html). Диапазон страниц 18–23 независимо не подтверждён, поэтому удалён из записи.
- Sedlak 2026: [arXiv](https://arxiv.org/abs/2602.15794) подтверждает авторов и название; остаётся препринтом.
- Обзор Petchrompo 2022 рассматривает отбор представителей уже найденного Pareto-фронта, а не доказательство безопасного отсечения ветвей поиска. Его использование в Related Work исправлено.
- Neubauer 2020 уже ставит задачу уменьшения числа дорогих оценок с сохранением точности. Универсальное заявление о новизне evaluator avoidance было бы неверным.
- Проверка метаданных всех ссылок не равнозначна построчной проверке содержания всех цитируемых полных текстов. Детальная сравнительная таблица prior work всё ещё требует экспертной проверки, особенно трактовка «exact front» у взвешенной BILP-оптимизации.


## Дополнение: независимый revision round, 2026-09-09

Метаданные следующих 11 записей получены через DOI content negotiation и сохранены в `review/round2/new-refs.json`. В основном тексте добавлены содержательные ссылки, а не просто записи в BibTeX.

- `casini2025edge`: [Managing real-time constraints through monitoring and analysis-driven edge orchestration](https://doi.org/10.1016/j.sysarc.2025.103403).
- `amir2020pareto`: [Pareto optimal design space exploration of cyber-physical systems](https://doi.org/10.1016/j.iot.2020.100308).
- `cloud2026coopt`: [A co-optimization framework toward energy-efficient cloud–edge inference with stochastic computing and precision-compensating NAS](https://doi.org/10.1016/j.sysarc.2026.103693).
- `filippini2026replica`: [Distributed replica allocation and load balancing for Edge–Cloud FaaS](https://doi.org/10.1016/j.sysarc.2026.103787).
- `predictive2026`: [Predictively controlling the computing continuum with distributed energy-aware orchestration](https://doi.org/10.1016/j.sysarc.2026.103752).
- `gene2024`: [A gene-inspired metaheuristic for scheduling workflow tasks in mobile edge computing-supported cyber–physical systems](https://doi.org/10.1016/j.sysarc.2024.103136).
- `ali2026icn`: [Dependency-aware microservices offloading in ICN-based edge computing testbed](https://doi.org/10.1016/j.sysarc.2025.103663).
- `guo2023`: [Automated Exploration and Implementation of Distributed CNN Inference at the Edge](https://doi.org/10.1109/jiot.2023.3237572).
- `guo2025`: [Model and system robustness in distributed CNN inference at the edge](https://doi.org/10.1016/j.vlsi.2024.102299).
- `saadatmand2024workload`: [Automated Derivation of Application Workload Models for Design Space Exploration of Industrial Distributed Cyber-Physical Systems](https://doi.org/10.1109/icps59941.2024.10639941).
- `demoura2008z3`: [Z3: An Efficient SMT Solver](https://doi.org/10.1007/978-3-540-78800-3_24).

Ali et al. имеют online date 2025 и выпуск JSA 171 (2026); в записи используется год выпуска. Для ICPS 2024 принята пагинация 1–8 из DOI record, не неподтверждённые 76–83.

Уточнена сравнительная таблица: [Kouloumpris 2026](https://www.sciencedirect.com/science/article/pii/S0167739X26000488) получает Pareto-optimal solution для заданных весов. Это не доказательство перечисления полного дискретного Pareto front. У работы 2024 один objective, поэтому колонка полного фронта — n/a.
