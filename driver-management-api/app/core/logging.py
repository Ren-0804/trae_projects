import logging
import sys
from pathlib import Path


def setup_logging():
    """配置日志系统"""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 创建logs目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 配置根日志记录器
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "app.log", encoding="utf-8")
        ]
    )
    
    # 配置访问日志
    access_logger = logging.getLogger("access")
    access_handler = logging.FileHandler(log_dir / "access.log", encoding="utf-8")
    access_handler.setFormatter(logging.Formatter(log_format))
    access_logger.addHandler(access_handler)
    access_logger.setLevel(logging.INFO)
    
    # 配置错误日志
    error_logger = logging.getLogger("error")
    error_handler = logging.FileHandler(log_dir / "error.log", encoding="utf-8")
    error_handler.setFormatter(logging.Formatter(log_format))
    error_logger.addHandler(error_handler)
    error_logger.setLevel(logging.ERROR)


# 全局日志记录器
logger = logging.getLogger(__name__)