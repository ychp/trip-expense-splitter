import logging
import sys
from pathlib import Path


def setup_logging(
    level: int = logging.INFO,
    log_dir: Path = None,
    app_name: str = "trip_expense"
) -> None:
    """配置应用日志系统"""
    
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(
            log_dir / f"{app_name}.log",
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """获取指定名称的logger"""
    return logging.getLogger(name)
