# Bot de Automação de Vendas PDV

Este bot automatiza o processo de vendas no PDV, integrando com o sistema Uniplus.

## Configuração

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure as variáveis de ambiente:
   - Copie o arquivo `.env.example` para `.env`
   - Edite o arquivo `.env` com suas configurações:
     - `UNIPLUS_PATH`: Caminho para o executável do Uniplus
     - `UNIPLUS_USER`: Usuário do Uniplus
     - `UNIPLUS_PASSWORD`: Senha do Uniplus
     - `UNIPLUS_COMPANY`: Código da empresa no Uniplus
     - `DB_HOST`: Host do banco de dados
     - `DB_PORT`: Porta do banco de dados
     - `DB_NAME`: Nome do banco de dados
     - `DB_USER`: Usuário do banco de dados
     - `DB_PASSWORD`: Senha do banco de dados
     - `INPUT_DIR`: Diretório de entrada para arquivos
     - `OUTPUT_DIR`: Diretório de saída para arquivos
     - `SCREENSHOT_DIR`: Diretório para armazenar screenshots

3. Execute o bot:
```bash
python main.py
```

## Estrutura do Projeto

- `main.py`: Ponto de entrada do bot
- `config.py`: Configurações e variáveis de ambiente
- `uniply_interface.py`: Interface com o sistema Uniplus
- `database.py`: Interface com o banco de dados
- `utils/`: Utilitários e funções auxiliares
- `tests/`: Testes unitários

## Funcionalidades

- Automação de vendas no PDV
- Integração com sistema Uniplus
- Armazenamento de dados em banco de dados
- Geração de relatórios
- Captura de screenshots para auditoria

## Requisitos

- Python 3.8+
- Uniplus instalado
- PostgreSQL
- Bibliotecas listadas em `requirements.txt` 