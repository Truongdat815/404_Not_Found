"""
Logging configuration cho ứng dụng
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

# Tạo logs directory
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Log file với timestamp
log_file = logs_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create logger
logger = logging.getLogger("requirements_analyzer")

# Set log levels cho different modules
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

