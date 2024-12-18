## Overview
Writestack is a mini-version of Substack for observability-learning purposes.

The idea with this is to teach the 3 signals of observability (metrics, traces and logs) from the ground up and eventually look into Observability 2.0

The relevant blog series for this is on my [Substack](http://obakeng.substack.com).

Following those blog posts, you can learn:
- Metrics
    - Setting Up Grafana & Prometheus
    - Sending metrics data to Prometheus
    - Setting and analyse important metric data (RED metrics)
- Logs
    - Implementing canonical log lines
    - Forwarding app logs to Clickhouse via Vector
    - Analysing the data via Grafana
    - Using Loki
- Traces
    - Adding trace instrumentation
    - Setting up Tempo
- SLOs/SLIs
    - Creating SLOs/SLIs
    - Using them to prioritize what to work on next
- Alerting
    - Designing alerts using SLOs.

## The architecture
It has a very simple architecture.
![data-diagram](https://github.com/user-attachments/assets/d485a713-734b-44c2-bc89-4c3a14699f13)

- Backend
    - FastAPI
- Frontend:
    - TBD
- Store
    - Postgres

## The data model
![umd](https://github.com/user-attachments/assets/2a23c2d1-7682-4c12-a890-3983e85c27f5)
