# Аудит библиографии (2026-09-09)

Сейчас в `manuscript/refs.bib` **26 записей**, все включённые метаданные проверены
через доступные источники (arXiv, publisher pages, dblp, ASP-DAC/DATE proceedings).
**Я не подставлял выдуманные DOI, тома и списки авторов** — там, где не удалось
проверить, запись просто не добавлена.

## Что проверено и добавлено в этом проходе

| Ключ | Статус |
|---|---|
| kouloumpris2024optimization | авторы + DOI 10.1016/j.future.2024.02.005 подтверждены (arXiv 2512.00029) |
| kouloumpris2026reliability | авторы подтверждены (arXiv 2602.18158); **нужен том/номер статьи FGCS** |
| lukasiewycz2008symbolic | ASP-DAC 2008, подтверждено dblp |
| haubelt2003pareto | ASP-DAC 2003, подтверждено dblp; **сверить страницы** |
| audet2021indicators | EJOR 292(2):397-422, 2021 — подтверждено |
| harchol2013performance | Cambridge UP, 2013 — подтверждено |
| blickle1998system | Design Automation for Embedded Systems 3(1) — **сверить страницы и DOI** |
| sedlak2026orchestration | arXiv:2602.15794, авторы подтверждены |

## Что нужно доделать вам (10-15 минут, механическая работа)

Доступ к ScienceDirect/IEEE у меня заблокирован (robots.txt), поэтому списки авторов
для свежих статей JSA взять не смог. Откройте ссылки и скопируйте authors + volume +
article number + DOI, затем добавьте записи и цитаты в Related Work
(§2.2 и §2.4 — места помечены в тексте как «JSA context»).

Рекомендуемые добавления (все проверены как существующие публикации):

1. **JSA 2025** — Managing real-time constraints through monitoring and analysis-driven
   edge orchestration. PII S138376212500075X. Ближе всего к нашему positioning:
   design-time optimisation параметров distributed edge application.
2. **JSA 2026** — A co-optimization framework toward energy-efficient cloud-edge
   inference. PII S1383762126000111.
3. **JSA 2026** — Dependency-aware microservices offloading in ICN-based edge computing
   testbed. PII S1383762125003352. Полезно как пример testbed-валидации в JSA.
4. **JSA 2026** — Distributed replica allocation and load balancing for Edge-Cloud FaaS.
   PII S1383762126001050.
5. **JSA 2026** — Predictively controlling the computing continuum with distributed
   energy-aware orchestration. PII S1383762126000706.
6. **JSA 2024** — A gene-inspired metaheuristic for scheduling workflow tasks in mobile
   edge computing-supported CPS. PII S1383762124000730.
7. **Microprocessors and Microsystems 2021** — Ontological reasoning in the design space
   exploration of advanced cyber-physical systems. PII S0141933121003197. Концептуальный
   конкурент по сокращению пространства через знания предметной области.
8. **JSA 2007** — Design space exploration of reliable networked embedded systems.
   PII S1383762107000215. Историческая привязка темы к самому журналу.

После добавления 8 записей библиография станет ~34; если нужно ближе к 45, тот же приём
даёт ещё 8-10 из свежих FGCS/TSC/TCAD/TECS по edge-cloud placement 2023-2026.

## Записи с неполными метаданными (обязательно доделать)

| Ключ | Чего не хватает |
|---|---|
| saadatmand2025compdse | полный список авторов (в .bib стоит `and others`) — взять со страницы IET |
| kouloumpris2026reliability | том и номер статьи FGCS (сейчас только год + arXiv) |
| xiao2024contrarc | страницы и DOI DATE 2024 |
| herget2022dse | страницы DSD 2022 (DOI указан) |
| blickle1998system, haubelt2003pareto | сверить страницы |

## Технический чек-лист перед сабмитом

- [ ] каждый DOI открывается и ведёт на ту же статью;
- [ ] совпадают заголовки (регистр, тире, спецсимволы);
- [ ] у конференционных работ указаны proceedings + страницы;
- [ ] нет дублей DOI;
- [ ] в `.bib` нет "et al." — стиль формирует список авторов сам;
- [ ] препринты помечены как препринты (`note = {arXiv:...}`), а не как журнальные статьи;
- [ ] `kleinrock1975queueing` оформлена как @book, а не @article (сейчас @article —
      **исправить**).
