from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

import pandas as pd
import numpy as np
import requests
import os
import hashlib
from datetime import datetime

# Configurações globais
URL_DADOS = "https://raw.githubusercontent.com/SF-DataScience/datasciencecourse/master/data/superstore_sales.csv"
DIRETORIO_DADOS_BRUTOS = "/opt/airflow/data/raw"
DIRETORIO_DADOS_PROCESSADOS = "/opt/airflow/data/processado"

# Argumentos padrão do DAG
args_padrao = {
    'owner': 'aluno',
    'depends_on_past': False,
    'email': ['aluno@bpkedu.com.br'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Definição do DAG
dag = DAG(
    'pipeline_etl_aluno',
    default_args=args_padrao,
    description='Pipeline ETL para implementação pelos alunos',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['etl', 'vendas', 'superstore', 'aluno']
)

def inicializar_banco():
    """
    Inicializa o banco de dados com a estrutura necessária para o modelo dimensional.
    Cria os esquemas, tabelas dimensionais e tabela fato.
    
    Esta função já está implementada para você. Ela cria todas as tabelas
    necessárias conforme o schema descrito no arquivo atividades_etl.md.
    """
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    
    # Criar esquemas
    comandos_sql = [
        "CREATE SCHEMA IF NOT EXISTS dim;",
        "CREATE SCHEMA IF NOT EXISTS fato;",
        "CREATE SCHEMA IF NOT EXISTS stage;",
        
        # Tabela dimensão data
        """

        """,
        
        # Tabela dimensão localização
        """

        """,
        
        # Tabela dimensão produto
        """

        """,
        
        # Tabela dimensão cliente
        """

        """,
        
        # Tabela fato vendas
        """

        """,
        
        # Tabela de staging
        """

        """
    ]
    
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    
    for comando in comandos_sql:
        cursor.execute(comando)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Banco de dados inicializado com sucesso!")

def limpar_dados(df, colunas_data=None, colunas_numericas=None, colunas_texto=None):
    """
    Realiza operações de limpeza de dados comuns.
    
    Args:
        df: DataFrame a ser limpo
        colunas_data: Lista de colunas para converter para datetime
        colunas_numericas: Lista de colunas para converter para numérico
        colunas_texto: Lista de colunas de texto para limpar
        
    Returns:
        DataFrame limpo
    
    TODO: Implemente esta função para realizar a limpeza de dados
    """
    # Faça uma cópia para não modificar o DataFrame original
    df_limpo = df.copy()
    
    # TODO: Implemente o tratamento de valores nulos
    
    # TODO: Implemente a conversão de colunas de data
    
    # TODO: Implemente a conversão de colunas numéricas
    
    # TODO: Implemente a limpeza de colunas de texto
    
    return df_limpo

def extrair_dados(**kwargs):
    """
    Extrai dados da fonte e salva localmente.
    
    Args:
        **kwargs: Argumentos do contexto do Airflow
        
    Returns:
        caminho_arquivo: Caminho do arquivo salvo
    
    TODO: Implemente esta função para extrair os dados da URL
    """
    # TODO: Garanta que o diretório exista
    
    # TODO: Defina o caminho do arquivo com timestamp
    
    # TODO: Faça o download do arquivo
    
    # TODO: Salve o arquivo localmente
    
    # TODO: Valide o arquivo baixado
    
    return "caminho_para_o_arquivo"  

def carregar_staging(**kwargs):
    """
    Carrega dados brutos na tabela de staging.
    
    Args:
        **kwargs: Argumentos do contexto do Airflow
        
    Returns:
        caminho_arquivo_processado: Caminho do arquivo processado
    
    TODO: Implemente esta função para carregar os dados no staging
    """
    # TODO: Obtenha o caminho do arquivo extraído
    
    # TODO: Leia o arquivo CSV
    
    # TODO: Mapeie as colunas para o formato do banco de dados
    
    # TODO: Limpe os dados usando a função limpar_dados
    
    # TODO: Salve os dados processados localmente
    
    # TODO: Conecte ao PostgreSQL
    
    # TODO: Trunce a tabela de staging antes de carregar novos dados
    
    # TODO: Carregue os dados no PostgreSQL
    
    return "caminho_para_o_arquivo_processado" 

def transformar_carregar_dimensoes(**kwargs):
    """
    Transforma dados e carrega nas tabelas dimensionais.
    
    Args:
        **kwargs: Argumentos do contexto do Airflow
        
    Returns:
        mensagem: Mensagem indicando o sucesso da operação
    
    TODO: Implemente esta função para transformar e carregar as dimensões
    """
    # TODO: Conecte ao banco de dados
    
    # TODO: Carregue os dados do staging
    
    # ------- Dimensão Data ------- #
    # TODO: Extraia datas únicas
    
    # TODO: Crie atributos para a dimensão de data
    
    # TODO: Carregue a dimensão de data
    
    # ------- Dimensão Localização ------- #
    # TODO: Extraia locais únicos
    
    # TODO: Transforme para o formato da dimensão
    
    # TODO: Salve na dimensão localização
    
    # ------- Dimensão Produto ------- #
    # TODO: Extraia produtos únicos
    
    # TODO: Calcule atributos derivados
    
    # TODO: Salve na dimensão produto
    
    # ------- Dimensão Cliente ------- #
    # TODO: Extraia clientes únicos
    
    # TODO: Gere campos derivados
    
    # TODO: Salve na dimensão cliente
    
    return "Dimensões carregadas com sucesso"

def transformar_carregar_fatos(**kwargs):
    """
    Transforma e carrega dados na tabela fato.
    
    Args:
        **kwargs: Argumentos do contexto do Airflow
        
    Returns:
        mensagem: Mensagem indicando o sucesso da operação
    
    TODO: Implemente esta função para transformar e carregar a tabela fato
    """
    # TODO: Conecte ao banco de dados
    
    # TODO: Carregue os dados do staging
    
    # TODO: Carregue as dimensões para obter as chaves
    
    # TODO: Crie o dataframe para a tabela fato
    
    # TODO: Adicione chaves estrangeiras (joins com as dimensões)
    
    # TODO: Selecione colunas relevantes para a tabela fato
    
    # TODO: Adicione métricas derivadas
    
    # TODO: Limpe valores nulos nas chaves
    
    # TODO: Converta chaves para inteiros
    
    # TODO: Carregue na tabela fato
    
    return "Tabela fato carregada com sucesso"

# Definir as tasks do DAG
inicio = DummyOperator(
    task_id='inicio',
    dag=dag
)

iniciar_banco = PythonOperator(
    task_id='iniciar_banco',
    python_callable=inicializar_banco,
    dag=dag
)

extrair = PythonOperator(
    task_id='extrair_dados',
    python_callable=extrair_dados,
    dag=dag
)

carregar_staging_task = PythonOperator(
    task_id='carregar_staging',
    python_callable=carregar_staging,
    dag=dag
)

transformar_dimensoes = PythonOperator(
    task_id='transformar_dimensoes',
    python_callable=transformar_carregar_dimensoes,
    dag=dag
)

transformar_fatos = PythonOperator(
    task_id='transformar_fatos',
    python_callable=transformar_carregar_fatos,
    dag=dag
)

fim = DummyOperator(
    task_id='fim',
    dag=dag
)

# Definir a ordem de execução das tasks
inicio >> iniciar_banco >> extrair >> carregar_staging_task >> transformar_dimensoes >> transformar_fatos >> fim 