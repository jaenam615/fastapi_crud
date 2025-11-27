from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_fastapi_instrumentator.metrics import latency


def setup_metrics(app):
    instrumentator = Instrumentator()
    instrumentator.add(
        latency(
            buckets=[
                0.005,
                0.01,
                0.025,
                0.05,
                0.1,
                0.2,
                0.5,
                1.0,
                2.0,
                5.0,
                10.0,
                20.0,
                30.0,
            ]
        )
    )
    instrumentator.instrument(app)
    instrumentator.expose(app, endpoint="/metrics")

    return instrumentator
