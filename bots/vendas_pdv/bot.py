import os
import time
import pandas as pd
import shutil
from datetime import datetime
from typing import List, Dict, Optional
from core.uniplus_interface import UniplusInterface
from core.utils import setup_project_structure, read_excel_to_dataframe, save_dataframe_to_excel
from core.database_manager import DatabaseManager

class VendasPdvBot(UniplusInterface):
    def __init__(self):
        super().__init__('vendas_pdv')
        self._setup_paths()
        self._setup_database_config()
        self.db_manager = DatabaseManager()
        
    def _setup_paths(self):
        self.input_dir = os.getenv('VENDAS_INPUT_DIR', r'G:\Meu Drive\Reports\Vendas\Diario')
        self.output_dir = os.getenv('VENDAS_OUTPUT_DIR', r'G:\Meu Drive\Reports\Vendas\Diario\Processados')
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
    def _setup_database_config(self):
        self.db_connection_str = os.getenv('DB_CONNECTION_STR')
        self.table_name = 'uniplus_vendas_pdvs'
        self.columns = [
            'pdv', 'filial', 'usuario', 'vendedor', 'emissao', 'hora',
            'documento', 'ccf', 'v_bruto', 'desconto', 'acrescimo',
            'v_venda', 'devolucao_troca', 'v_liquido', 'canc',
            'cliente', 'cnpj_cpf', 'finalizador', 'valor_finalizador'
        ]
        
    def _extract_report(self) -> bool:
        try:
            # Open Uniplus
            if not self.open_uniplus():
                return False
                
            # Navigate to sales report
            menu_path = ['vendas', 'relatorios', 'vendas_por_pdv']
            if not self.navigate_to_menu(menu_path):
                return False
                
            time.sleep(10)  # Wait for report to load
            
            # Try to find and click the Excel button using multiple methods
            excel_button_found = False
            
            # Method 1: Try with primary image
            if self._click_element(image_path='screenshots/excel_button_1.png'):
                excel_button_found = True
                self.logger.info("Found Excel button using primary image")
            
            # Method 2: Try with secondary image
            if not excel_button_found and self._click_element(image_path='screenshots/excel_button_2.png'):
                excel_button_found = True
                self.logger.info("Found Excel button using secondary image")
            
            # Method 3: Try with text recognition
            if not excel_button_found:
                excel_button_found = self._click_text('Exportar para Excel')
                if excel_button_found:
                    self.logger.info("Found Excel button using text recognition")
            
            if not excel_button_found:
                self.logger.error("Could not find Excel export button")
                return False
                
            time.sleep(1)
            
            # Set date range
            self._press_key('tab')
            self._press_key('tab')
            self._press_key('tab')
            time.sleep(1)
            
            current_date = datetime.now().strftime('%d%m%Y')
            self._type_text(current_date)
            time.sleep(1)
            self._type_text(current_date)
            self._press_key('f10')
            
            time.sleep(2)
            
            # Save report
            filename = f'vendas_pdv_{current_date}.xlsx'
            if not self.save_report(filename, self.input_dir):
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error extracting report: {str(e)}")
            return False
            
    def _process_file(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        try:
            # Find the row with 'PDV' value
            pdv_index = df[df.iloc[:, 0] == 'PDV'].index[0]
            
            # Set the header
            df.columns = df.iloc[pdv_index]
            
            # Filter rows where PDV is 1, 2, or 3
            df['PDV'] = df['PDV'].astype(str)
            df = df[df['PDV'].isin(['1', '2', '3'])]
            df.reset_index(drop=True, inplace=True)
            
            # Remove rows with empty Documento
            df = df.dropna(subset=['Documento'])
            
            # Rename columns
            column_mapping = {
                'PDV': 'pdv',
                'Filial': 'filial',
                'Usuário': 'usuario',
                'Vendedor': 'vendedor',
                'Emissão': 'emissao',
                'Hora': 'hora',
                'Documento': 'documento',
                'CCF': 'ccf',
                'V.bruto': 'v_bruto',
                'Desconto': 'desconto',
                'Acréscimo': 'acrescimo',
                'V.venda': 'v_venda',
                'Devolução/Troca': 'devolucao_troca',
                'V.líquido': 'v_liquido',
                'Canc.': 'canc',
                'Cliente': 'cliente',
                'Cnpj/Cpf': 'cnpj_cpf',
                'Finalizador': 'finalizador',
                'Valor finalizador': 'valor_finalizador'
            }
            df = df.rename(columns=column_mapping)
            df = df.astype(str)
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error processing file: {str(e)}")
            return None
            
    def _insert_to_database(self, df: pd.DataFrame) -> bool:
        try:
            # Get existing data
            query = f'SELECT {", ".join(self.columns)} FROM {self.table_name}'
            df_existing = self.db_manager.execute_query(query)
            
            # Convert NaN to None
            df = df.where(pd.notna(df), None)
            
            # Find new records
            merge_cols = ['emissao', 'hora', 'documento']
            df_new = pd.merge(df, df_existing, on=merge_cols, how='left', indicator=True)
            df_new = df_new[df_new['_merge'] == 'left_only'].drop('_merge', axis=1)
            df_new = df_new.rename(columns={f"{col}_x": col for col in self.columns})
            
            if not df_new.empty:
                # Insert new records
                self.db_manager.insert_dataframe(df_new, self.table_name)
                self.logger.info(f"Inserted {len(df_new)} new records")
            else:
                self.logger.info("No new records to insert")
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error inserting to database: {str(e)}")
            return False
            
    def _move_processed_file(self, file_path: str) -> bool:
        try:
            filename = os.path.basename(file_path)
            output_path = os.path.join(self.output_dir, filename)
            shutil.move(file_path, output_path)
            self.logger.info(f"Moved file to {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error moving file: {str(e)}")
            return False
            
    def run(self):
        self.logger.info("Starting Vendas PDV bot")
        self.is_running = True
        
        try:
            # Extract report from Uniplus
            if not self._extract_report():
                self.logger.error("Failed to extract report")
                return
                
            # Get list of Excel files
            excel_files = [f for f in os.listdir(self.input_dir) if f.endswith('.xlsx')]
            
            if not excel_files:
                self.logger.info("No files to process")
                return
                
            for file in excel_files:
                file_path = os.path.join(self.input_dir, file)
                self.logger.info(f"Processing file: {file}")
                
                # Read and process file
                df = read_excel_to_dataframe(file_path)
                if df is None:
                    continue
                    
                processed_df = self._process_file(df)
                if processed_df is None:
                    continue
                    
                # Insert to database
                if not self._insert_to_database(processed_df):
                    continue
                    
                # Move processed file
                self._move_processed_file(file_path)
                
        except Exception as e:
            self.logger.error(f"Error in bot execution: {str(e)}")
            raise
            
        finally:
            self.is_running = False
            self.logger.info("Vendas PDV bot completed") 