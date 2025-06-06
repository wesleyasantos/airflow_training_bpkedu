# Projeto de Demonstração ETL com Airflow e PostgreSQL

Este é um projeto de demonstração para ensinar conceitos de ETL (Extract, Transform, Load) utilizando Apache Airflow e PostgreSQL.

## Estrutura do Projeto

```
Airflow - Pipeline de Dados/
│
├── dags/                      # DAGs do Airflow
│   ├── exemplo_dag_basico.py  # DAG de exemplo básico
│   ├── exemplo_dag_postgres.py # DAG com integração PostgreSQL
│   └── pipeline_etl_esqueleto.py # Esqueleto para implementação dos alunos
│
├── scripts/                   # Scripts úteis
│   ├── init_db_demonstracao.sql # Script para inicialização do banco
│   └── inicializar_banco.bat    # Script para inicializar o banco de dados
│
├── data/                      # Diretório para armazenar dados
│   ├── raw/                   # Dados brutos extraídos 
│   ├── processado/            # Dados após processamento
│   └── transformed/           # Dados transformados para análise
│
├── docker-compose.yml         # Configuração Docker para o ambiente
├── iniciar_airflow_windows.bat # Script para iniciar Airflow no Windows
└── atividades_etl.md          # Atividades para os alunos
```

## Pré-requisitos

- Docker e Docker Compose
- Git
- Windows 10 ou superior

## Configuração do Ambiente no Windows

Para iniciar o ambiente com os caminhos específicos do Windows:

```bash
iniciar_airflow_windows.bat
```

Este script:
1. Cria todos os diretórios necessários em `caminho_seu_computador`
2. Inicia os contêineres Docker com mapeamento correto para Windows e WSL
3. Mostra instruções para acessar o Airflow e PgAdmin


### Inicialização do Banco de Dados

Após iniciar os contêineres, execute o script para inicializar o banco de dados:

```bash
cd scripts
inicializar_banco.bat
```

## Exemplos Disponíveis

### 1. DAG Básico

O arquivo `dags/exemplo_dag_basico.py` contém um exemplo simples de um DAG do Airflow que:
- Gera um conjunto de dados fictícios (salvo em `/data/processado/`)
- Realiza análises simples
- Salva os resultados (em `/data/transformed/`)

### 2. DAG com PostgreSQL

O arquivo `dags/exemplo_dag_postgres.py` contém um exemplo mais avançado que:
- Gera dados mais complexos (salvos em `/data/raw/`)
- Realiza transformações (resultados em `/data/processado/`)
- Calcula estatísticas (salvas em `/data/transformed/`)
- Salva os resultados no PostgreSQL
- Verifica os dados carregados

## Configuração da Conexão ao PostgreSQL no Airflow

Para que os DAGs funcionem corretamente com o PostgreSQL, é necessário configurar uma conexão:

1. No Airflow, navegue até Admin > Connections
2. Clique em "+" para adicionar uma nova conexão
3. Preencha:
   - Conn Id: postgres_default
   - Conn Type: Postgres
   - Host: postgres
   - Schema: etl_demo
   - Login: app_etl
   - Password: etl123
   - Port: 5432
4. Clique em "Save"

## Problemas Comuns no Windows

### 1. Erro de mapeamento de volumes

Se você encontrar erros como "cannot start service airflow-webserver: path not found", verifique:
- Verifique se o Docker Desktop tem permissão para acessar as pastas

### 2. Problemas com WSL

Se encontrar problemas relacionados ao WSL:
- Verifique se o WSL está instalado e funcionando corretamente
- O caminho do WSL deve ser acessível via `\\wsl.localhost\Ubuntu\opt\airflow\`

### 3. Permissões de arquivos

Se houver problemas de permissão:
- Execute o prompt de comando como administrador
- Verifique as configurações de compartilhamento de arquivos no Docker Desktop

## Passos para Execução da Demonstração

1. Execute `iniciar_airflow_windows.bat`
2. Execute `scripts\inicializar_banco.bat`
3. Acesse o Airflow em http://localhost:8080
4. Configure a conexão com o PostgreSQL
5. Ative e execute o DAG básico (`exemplo_basico`)
6. Ative e execute o DAG com PostgreSQL (`exemplo_postgres`)
7. Verifique os arquivos gerados nos diretórios:
   - `C:\Users\TI-00\Desktop\Airflow - Pipeline de Dados\data\raw\`
   - `C:\Users\TI-00\Desktop\Airflow - Pipeline de Dados\data\processado\`
   - `C:\Users\TI-00\Desktop\Airflow - Pipeline de Dados\data\transformed\`
