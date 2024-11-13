## Overview
Writestack is a mini-version of Substack for observability-learning purposes.

The idea with this is to teach the 3 signals of observability (metrics, traces and logs) from the ground up.

The relevant blog series for this is on my [Substack](http://obakeng.substack.com).

Following those blog posts, you can learn:
- Metrics
    - Setting Up Grafana & Prometheus
    - Sending metrics data to Prometheus
    - Setting and analyse important metric data (RED metrics)
- Logs
    - Setting up Vector & Clickhouse
    - Forwarding app logs to Clickhouse
    - Analysing the data via Grafana
- Traces
    - Adding trace instrumentation
    - Setting up Tempo/Jaeger
- SLOs/SLIs
    - Creating SLOs/SLIs
    - Using them to prioritize what to work on next

## The architecture
It has a very simple architecture.
![composition](https://github.com/user-attachments/assets/a3320abe-3098-46a0-96d4-a25194ebda09)

Backend: FastAPI
Frontend: Svelte
Store: Postgres

## The data model
![writestack](https://github.com/user-attachments/assets/d5b81c12-d188-45cc-a25f-e6de17b8e3fd)
