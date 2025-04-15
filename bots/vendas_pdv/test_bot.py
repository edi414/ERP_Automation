import os
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime
from bots.vendas_pdv.bot import VendasPdvBot

class TestVendasPdvBot(unittest.TestCase):
    def setUp(self):
        self.bot = VendasPdvBot()
        
    @patch('core.uniplus_interface.UniplusInterface._click_element')
    @patch('core.uniplus_interface.UniplusInterface._press_key')
    @patch('core.uniplus_interface.UniplusInterface._type_text')
    @patch('core.uniplus_interface.UniplusInterface.save_report')
    @patch('core.uniplus_interface.UniplusInterface.navigate_to_menu')
    @patch('core.uniplus_interface.UniplusInterface.open_uniplus')
    def test_extract_report(self, mock_open_uniplus, mock_navigate_menu, mock_save_report, 
                          mock_type_text, mock_press_key, mock_click_element):
        # Configure mocks
        mock_open_uniplus.return_value = True
        mock_navigate_menu.return_value = True
        mock_click_element.return_value = True
        mock_save_report.return_value = True
        
        # Test successful extraction
        result = self.bot._extract_report()
        self.assertTrue(result)
        
        # Verify method calls
        mock_open_uniplus.assert_called_once()
        mock_navigate_menu.assert_called_once_with(['vendas', 'relatorios', 'vendas_por_pdv'])
        mock_click_element.assert_called_once()
        self.assertEqual(mock_press_key.call_count, 4)  # 3 tabs + F10
        self.assertEqual(mock_type_text.call_count, 2)  # Start and end date
        
    def test_process_file(self):
        # Create test DataFrame
        data = {
            'PDV': ['1', '2', '3', '4', 'PDV'],
            'Filial': ['001', '001', '001', '001', ''],
            'Documento': ['123', '456', '789', '012', ''],
            'V.bruto': ['100', '200', '300', '400', ''],
            'V.venda': ['90', '180', '270', '360', ''],
            'V.líquido': ['90', '180', '270', '360', ''],
            'Cliente': ['A', 'B', 'C', 'D', ''],
            'Cnpj/Cpf': ['1', '2', '3', '4', ''],
            'Finalizador': ['Dinheiro', 'Cartão', 'PIX', 'Boleto', ''],
            'Valor finalizador': ['90', '180', '270', '360', '']
        }
        df = pd.DataFrame(data)
        
        # Process file
        result = self.bot._process_file(df)
        
        # Verify results
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)  # Only PDVs 1, 2, and 3
        self.assertIn('pdv', result.columns)
        self.assertIn('v_bruto', result.columns)
        self.assertIn('v_venda', result.columns)
        
    @patch('psycopg2.connect')
    @patch('pandas.read_sql_query')
    def test_insert_to_database(self, mock_read_sql, mock_connect):
        # Create test DataFrame
        data = {
            'pdv': ['1', '2'],
            'filial': ['001', '001'],
            'documento': ['123', '456'],
            'v_bruto': ['100', '200'],
            'v_venda': ['90', '180'],
            'v_liquido': ['90', '180']
        }
        df = pd.DataFrame(data)
        
        # Configure mocks
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_read_sql.return_value = pd.DataFrame()  # No existing data
        
        # Test insertion
        result = self.bot._insert_to_database(df)
        self.assertTrue(result)
        
        # Verify database operations
        mock_connect.assert_called_once()
        mock_read_sql.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
        
    @patch('shutil.move')
    def test_move_processed_file(self, mock_move):
        # Test file moving
        test_file = 'test.xlsx'
        result = self.bot._move_processed_file(test_file)
        
        # Verify results
        self.assertTrue(result)
        mock_move.assert_called_once_with(
            test_file,
            os.path.join(self.bot.output_dir, os.path.basename(test_file))
        )
        
    @patch('bots.vendas_pdv.bot.VendasPdvBot._extract_report')
    @patch('bots.vendas_pdv.bot.VendasPdvBot._process_file')
    @patch('bots.vendas_pdv.bot.VendasPdvBot._insert_to_database')
    @patch('bots.vendas_pdv.bot.VendasPdvBot._move_processed_file')
    def test_run(self, mock_move, mock_insert, mock_process, mock_extract):
        # Configure mocks
        mock_extract.return_value = True
        mock_process.return_value = pd.DataFrame()
        mock_insert.return_value = True
        mock_move.return_value = True
        
        # Test run method
        self.bot.run()
        
        # Verify method calls
        mock_extract.assert_called_once()
        mock_process.assert_called()
        mock_insert.assert_called()
        mock_move.assert_called()

if __name__ == '__main__':
    unittest.main() 