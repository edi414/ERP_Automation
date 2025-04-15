import os
import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

def setup_project_structure():
    """Create necessary directories for the project"""
    directories = [
        'logs',
        'bots',
        'core',
        'screenshots'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def read_excel_to_dataframe(file_path: str, header_row: int = 0) -> Optional[pd.DataFrame]:
    """
    Read an Excel file into a pandas DataFrame
    
    Args:
        file_path: Path to the Excel file
        header_row: Row number to use as header (0-based)
        
    Returns:
        DataFrame if successful, None otherwise
    """
    try:
        df = pd.read_excel(file_path, header=header_row)
        return df
    except Exception as e:
        logging.error(f"Error reading Excel file: {str(e)}")
        return None

def save_dataframe_to_excel(df: pd.DataFrame, file_path: str) -> bool:
    """
    Save a pandas DataFrame to an Excel file
    
    Args:
        df: DataFrame to save
        file_path: Path where to save the file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        df.to_excel(file_path, index=False)
        return True
    except Exception as e:
        logging.error(f"Error saving DataFrame to Excel: {str(e)}")
        return False

def get_timestamp() -> str:
    """Get current timestamp in YYYYMMDD_HHMMSS format"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def validate_required_files(file_paths: List[str]) -> bool:
    """
    Validate that all required files exist
    
    Args:
        file_paths: List of file paths to check
        
    Returns:
        bool: True if all files exist, False otherwise
    """
    for file_path in file_paths:
        if not os.path.exists(file_path):
            logging.error(f"Required file not found: {file_path}")
            return False
    return True

def create_screenshot_dir(bot_name: str) -> str:
    """
    Create a directory for bot screenshots
    
    Args:
        bot_name: Name of the bot
        
    Returns:
        str: Path to the created directory
    """
    screenshot_dir = os.path.join('bots', bot_name, 'screenshots')
    os.makedirs(screenshot_dir, exist_ok=True)
    return screenshot_dir 