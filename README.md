# FASTAPI Simple Board

단순 CRUD 게시판 서비스로, 현대적인 백엔드 아키텍처와 성능 최적화를 적용한 프로젝트입니다.  
FastAPI를 기반으로 구현하였으며, Redis 캐싱, 메시지 큐, 다중 서버 배포, 성능 테스트 등을 포함합니다.


## 기술 스택

- **Backend**: Python, FastAPI
- **Database**: MySQL
- **Caching**: Redis (조회 캐싱 + Refresh Token 관리)
- **Message Queue**: Kafka
- **Web Server**: Nginx, Uvicorn
- **Testing**: Pytest, Locust (성능 테스트)
- **Containerization**: Docker, Docker Compose

## 아키텍처

[Client] <---> [Nginx] <---> [FastAPI App x N] <---> [DB]
|
+--> [Redis Cache]
+--> [Message Queue]


## Prometheus Monitoring
```markdown
---
Redis hit ratio
---
redis_cache_hits_total / (redis_cache_hits_total + redis_cache_misses_total)

---
요청 성공률 (SLO 체크 핵심)

설명:
전체 응답 중 2xx 비율.
SLO 99% 확인용.
---
sum(rate(http_responses_total{status=~"2.."}[1m]))
/
sum(rate(http_responses_total[1m]))

---
에러 비율 (5xx만 따로 감지)

설명:
5xx 비율은 장애 탐지의 가장 핵심 지표.
---
sum(rate(http_responses_total{status=~"5.."}[5m]))
/
sum(rate(http_responses_total[5m]))

---
요청 지연 분포 (p90, p95, p99)

설명:
평균 대신 p95/p99 사용 → 실제 사용자 느린 요청 감지에 필수.
---
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

---
CPU 사용률 (%)
---
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)

---
메모리 사용률 (%)
---
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
/
node_memory_MemTotal_bytes

---
디스크 사용률 (%)
---
(node_filesystem_size_bytes{fstype!~"tmpfs|overlay"} - node_filesystem_free_bytes{fstype!~"tmpfs|overlay"})
/
node_filesystem_size_bytes{fstype!~"tmpfs|overlay"}


```