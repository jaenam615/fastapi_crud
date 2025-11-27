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