import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class Logger:
    """统一日志管理类"""
    
    def __init__(self, name: str = "ai_chat_service", log_dir: str = "logs"):
        """
        初始化日志器
        
        参数:
            name: 日志器名称
            log_dir: 日志文件目录
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 确保日志目录存在
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 日志文件名（包含日期）
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(log_dir, f"{name}_{today}.log")
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # 文件处理器（带轮转）
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=7  # 保留7天的日志
            )
            file_handler.setLevel(logging.INFO)
            
            # 日志格式
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            
            # 设置格式
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)
            
            # 添加处理器
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
    
    def get_logger(self) -> logging.Logger:
        """
        获取配置好的日志器实例
        
        返回:
            logging.Logger实例
        """
        return self.logger

# 创建全局日志器实例
def get_logger(name: str = "ai_chat_service") -> logging.Logger:
    """
    获取或创建日志器实例
    
    参数:
        name: 日志器名称
        
    返回:
        logging.Logger实例
    """
    # 检查日志器是否已经存在
    existing_logger = logging.getLogger(name)
    if existing_logger.handlers:
        return existing_logger
    
    # 创建新的日志器实例
    logger_instance = Logger(name).get_logger()
    return logger_instance