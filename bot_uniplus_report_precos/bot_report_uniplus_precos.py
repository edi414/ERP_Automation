import sys
import time
import pyautogui
from botcity.core import DesktopBot
from datetime import datetime
import os
import logging
import pandas as pd
import psycopg2
from tqdm import tqdm

#CREATE LOG FILE IN MEMORY
# log_dir = r"G:\Meu Drive\Reports\Vendas\Diario\Log" ## alterar
# log_filename = f'log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
# log_file_path = os.path.join(log_dir, log_filename)
# logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para adicionar uma entrada ao log
def log_entry(message):
    logging.info(message)

#CURRENT_DATE = datetime.date.today()
#WEEK = datetime.date.today() - timedelta(days=7)
logging.warning("Iniciando Script: %s \n", datetime.now())

output_folder = r'G:\Meu Drive\Reports\Estoque\precos_servidor'
data_rel = datetime.now().strftime('%d_%m_%Y')
data_rel_file = str(data_rel).replace('/','')
file_name = f'precos_{data_rel_file}'
print(file_name)

class Bot(DesktopBot):
    def action(self, execution=None):

        def executar_com_repeticao(funcao, *args, tentativas=3, **kwargs):
            for _ in range(tentativas):
                try:
                    resultado = funcao(*args, **kwargs)
                    return resultado
                except Exception as e:
                    print(f"Erro: {e}. Tentando novamente...")
            return None  # ou levantar uma exceção ou retornar um valor padrão

        def extracao_uniplus():
            def open_system():
                try:
                    self.execute(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Uniplus\Uniplus.lnk")
                    self.execute(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Uniplus\Uniplus.lnk")
                    time.sleep(1)
                    self.key_esc()
                    self.key_esc()
                    self.key_esc()
                    self.key_esc()
                    self.key_esc()
                    self.key_esc()
                    self.key_esc()
                    self.key_esc()
                    self.key_esc()
                    logging.warning("Inicializacao Uniplus completa: %s \n", datetime.now())
                except:
                    logging.error("Erro na inicializacao do Uniplus: %s \n", datetime.now())

            executar_com_repeticao(open_system)

            def open_produtos():
                if not self.find( "click_image_produtos", matching=0.97, waiting_time=10000):
                    if not self.find_text( "click_text_produtos", threshold=230, waiting_time=10000):
                        self.not_found("click_text_produtos")
                    self.click()
                self.click()

            executar_com_repeticao(open_produtos)
            time.sleep(10)

            def ajuste_relatorio():
                try:
                    time.sleep(1)
                    self.tab()
                    time.sleep(1)
                    self.kb_type('report_precos')
                    time.sleep(1)
                    self.enter()
                    time.sleep(1)
                    pyautogui.click(x=456, y=141) ## carregando a visão
                    time.sleep(15)
                    self.tab()
                    self.tab()
                    self.tab()
                    time.sleep(1)
                    self.enter()
                    time.sleep(1)
                    pyautogui.click(x=1901, y=134) ## carregando a grade
                    time.sleep(15)
                    logging.warning("Sucesso ao configurar o template do relatório: %s \n", datetime.now())
                except:
                    logging.error("Erro ao tentar ajustar o template do relatório: %s \n", datetime.now())

            executar_com_repeticao(ajuste_relatorio)

            def imprimir_relatorio():
                try:
                    self.control_p()
                    time.sleep(1)
                    if not self.find( "click_imagem_excel", matching=0.97, waiting_time=10000):
                        if not self.find_text( "click_excel_texto", threshold=230, waiting_time=10000):
                            self.not_found("click_excel_texto")
                        self.click()
                    self.click()
                    self.key_f10()
                    logging.warning("Sucesso ao imprimir o relatório em xlsx: %s \n", datetime.now())
                except:
                    logging.error("Erro ao tentar imprimir o relatório: %s \n", datetime.now())

            if self.find_text( "valor_ultima_compra", threshold=230, waiting_time=10000):
                executar_com_repeticao(imprimir_relatorio)
            else:
                self.not_found("valor_ultima_compra")

            ##################### salvar o arquivo
            def salvando_xlsx(file_name, output_folder):
                try:
                    time.sleep(5)
                    ## val
                    # if not self.find( "find_arquivo", matching=0.97, waiting_time=10000):
                    #     if not self.find_text( "find_text_arquivo", threshold=230, waiting_time=10000):
                    #         self.not_found("find_text_arquivo")
                    time.sleep(0.5)
                    self.key_f12()
                    time.sleep(0.5)
                    self.kb_type(file_name)
                    time.sleep(0.5)
                    self.key_f4()
                    time.sleep(0.5)
                    self.control_a()
                    time.sleep(0.5)
                    self.kb_type(output_folder)
                    time.sleep(0.5)
                    self.enter()
                    time.sleep(0.5)
                    self.type_keys(['alt', 's'])
                    # if not self.find( "confirmar_salvar_como", matching=0.97, waiting_time=10000):
                    #     if not self.find_text( "confirma_salvar_como", threshold=230, waiting_time=10000):
                    #         print('Não existe um arquivo igual')
                    time.sleep(0.5)
                    # self.kb_type('s')
                    logging.warning("Relatório salvo com sucesso: %s \n", datetime.now())
                except:
                    logging.error("Erro ao salvar relatório na pasta do Google Drive: %s \n", datetime.now())
                time.sleep(3)

                try:
                    self.alt_f4()
                except:
                    logging.error("Erro ao tentar fechar o arquivo excel: %s \n", datetime.now())

            if self.find_text( "find_cadastro_produtos", threshold=230, waiting_time=10000):
                executar_com_repeticao(salvando_xlsx,file_name, output_folder)
            else:
                self.not_found("find_cadastro_produtos")
                sys.exit()

        executar_com_repeticao(extracao_uniplus)

        def process_file(file_name, output_folder):
            file_path = os.path.join(output_folder, file_name +'.xlsx')
            if file_path.endswith('.xls') or file_path.endswith('.xlsx'):
                # Lê o arquivo Excel e carrega-o em um DataFrame
                df = pd.read_excel(file_path)
                # Define a segunda linha como cabeçalho
                df.columns = df.iloc[0]
                # Remove a primeira e as duas últimas linhas
                df = df.iloc[1:-2]
                os.remove(file_path)
                print(df.columns)
                return df
            else:
                # Se o arquivo não for um arquivo Excel, imprime uma mensagem de erro
                executar_com_repeticao(extracao_uniplus)
                print("O arquivo não é um arquivo Excel válido.")


        df = executar_com_repeticao(process_file, file_name, output_folder)
        print(df)

        def importar_df_railway(dataframe):
            if dataframe is not None:
                try:
                    # Conectar ao banco de dados
                    postgres_conn = psycopg2.connect(
                        ####conexão com o banco
                    )
                    with postgres_conn.cursor() as cursor:
                        ## deleta todas as linhas da tabela
                        cursor.execute("DELETE FROM precos_api")

                        dataframe['id'] = dataframe.index #id
                        dataframe['date_insert'] = datetime.now() #tag com hora
                        dataframe = dataframe.astype(str)
                        print(dataframe)


                        # Iterar sobre as linhas do DataFrame e inserir os dados no banco de dados
                        for index, row in tqdm(dataframe.iterrows(), total=len(dataframe)):
                            data_tuple = (
                                row['id'], row['date_insert'], row['Código'], row['Código de barras'],
                                row['Preço unit.'],
                                row['Valor do preço na última compra']
                            )
                            cursor.execute("""
                                 INSERT INTO precos_api (
                                     id, date_insert, sku, ean, preco_ultima_compra, preco_venda
                                 ) VALUES (%s, %s, %s, %s, %s, %s)
                             """, data_tuple)

                    postgres_conn.commit()
                    postgres_conn.close()
                    logging.warning("Relatório inserido no banco com sucesso: %s \n", datetime.now())
                except:
                    logging.error("Erro ao inserir o relatório no banco de dados: %s \n", datetime.now())
            else:
                logging.warning("Dataframe vazio, nada a inserir no banco: %s \n", datetime.now())

        try:
            executar_com_repeticao(importar_df_railway,df)
            logging.warning("Processo finalizado com sucesso: %s \n", datetime.now())
        except:
            logging.error("Erro de importação no banco: %s \n", datetime.now())

    def not_found(self, label):
        print(f"Element not found: {label}")

if __name__ == '__main__':
    try:
        Bot.main()
    except RuntimeError as e:
        print(f'Erro: {e}')
















