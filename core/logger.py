import logging
import os
from datetime import datetime
from typing import Optional
import sys

class RpaLogHandler(logging.Handler):
    """Custom logging handler for RPA bots"""
    
    def __init__(self, log_dir: str = 'logs'):
        super().__init__()
        self.log_dir = log_dir
        self._setup_log_dir()
        self._setup_formatter()
        
    def _setup_log_dir(self):
        """Create logs directory if it doesn't exist"""
        os.makedirs(self.log_dir, exist_ok=True)
        
    def _setup_formatter(self):
        """Setup the formatter for log messages"""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.setFormatter(formatter)
        
    def emit(self, record):
        """Emit a record to both file and console"""
        try:
            # Create log file path with current date
            log_file = os.path.join(
                self.log_dir,
                f'{record.name}_{datetime.now().strftime("%Y%m%d")}.log'
            )
            
            # Write to file
            with open(log_file, 'a') as f:
                f.write(self.format(record) + '\n')
                
            # Write to console
            print(self.format(record))
            
        except Exception as e:
            print(f"Error in logging handler: {str(e)}", file=sys.stderr)

def setup_logger(name: str, log_level: int = logging.INFO) -> logging.Logger:
    """
    Setup a logger with the custom RPA handler
    
    Args:
        name: Name of the logger
        log_level: Logging level (default: INFO)
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Clear any existing handlers
    logger.handlers = []
    
    # Add our custom handler
    handler = RpaLogHandler()
    logger.addHandler(handler)
    
    return logger

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get or create a logger instance
    
    Args:
        name: Name of the logger (if None, returns root logger)
        
    Returns:
        Logger instance
    """
    if name is None:
        return logging.getLogger()
    return logging.getLogger(name) 