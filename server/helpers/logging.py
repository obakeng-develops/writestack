import structlog
import fastapi
import sys

# configure structlog
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ],
)

logger = structlog.get_logger()
python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
fastapi_version = fastapi.__version__
