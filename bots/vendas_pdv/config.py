import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Uniplus configuration
UNIPLUS_PATH = os.getenv('UNIPLUS_PATH', 'C:\\Uniplus\\Uniplus.exe')
UNIPLUS_USER = os.getenv('UNIPLUS_USER', 'admin')
UNIPLUS_PASSWORD = os.getenv('UNIPLUS_PASSWORD', 'admin')
UNIPLUS_COMPANY = os.getenv('UNIPLUS_COMPANY', '1')

# Database configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'erp_automation')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')

# File paths
INPUT_DIR = os.getenv('INPUT_DIR', 'C:\\ERP_Automation\\input')
OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'C:\\ERP_Automation\\output')
SCREENSHOT_DIR = os.getenv('SCREENSHOT_DIR', 'C:\\ERP_Automation\\screenshots')

# Report configuration
REPORT_NAME = 'vendas_por_pdv'
REPORT_SAVE_PATH = os.path.join(INPUT_DIR, f'{REPORT_NAME}.xlsx')

# Database table configuration
TABLE_NAME = 'vendas_pdv' 