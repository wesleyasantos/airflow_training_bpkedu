from datetime import datetime, timedelta
import os
import logging
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

# Definir caminhos base como variáveis para facilitar a configuração
DATA_DIR = '/opt/airflow/data'
RAW_DIR = f'{DATA_DIR}/raw'
PROCESSADO_DIR = f'{DATA_DIR}/processado'
TRANSFORMED_DIR = f'{DATA_DIR}/transformed'

# Arquivo para armazenar o caminho (alternativa ao Variable)
CAMINHO_INFO = f'{DATA_DIR}/caminho_arquivo.txt'

# Argumentos padrão para o DAG
args_padrao = {
    'owner': 'instrutor',
    'depends_on_past': False,
    'email': ['wesley@bpkedu.com.br'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

# Definindo o DAG
dag = DAG(
    'etl_basico_dag',
    default_args=args_padrao,
    description='Exemplo básico corrigido de DAG para demonstração',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['exemplo', 'demonstracao', 'corrigido']
)


inicio = DummyOperator(
    task_id='inicio',
    dag=dag
)


def verificar_diretorios(**kwargs):
    """
    Verifica e cria os diretórios necessários para o pipeline.
    """
    diretorios = [DATA_DIR, RAW_DIR, PROCESSADO_DIR, TRANSFORMED_DIR]
    
    for diretorio in diretorios:
        try:
            os.makedirs(diretorio, exist_ok=True)
            logging.info(f"Diretório verificado/criado: {diretorio}")
        except Exception as e:
            logging.error(f"Erro ao criar diretório {diretorio}: {str(e)}")
            raise
    
    # Verificar permissões
    for diretorio in diretorios:
        if os.access(diretorio, os.W_OK):
            logging.info(f"Permissão de escrita confirmada para: {diretorio}")
        else:
            logging.warning(f"Sem permissão de escrita para: {diretorio}")
    
    return True

verificar_dirs = PythonOperator(
    task_id='verificar_diretorios',
    python_callable=verificar_diretorios,
    dag=dag
)


verificar_ambiente = BashOperator(
    task_id='verificar_ambiente',
    bash_command=f'echo "Data atual: $(date)" > {DATA_DIR}/verificacao_ambiente.txt && echo "Ambiente verificado com sucesso!"',
    dag=dag
)


def gerar_dados_exemplo(**kwargs):
    """
    Gera um arquivo de dados de exemplo simples.
    """
    try:
        import pandas as pd
        
        logging.info("Iniciando geração de dados de exemplo")
        
        # Garantir que o diretório exista
        os.makedirs(PROCESSADO_DIR, exist_ok=True)
        

        dados = {
            'id': range(1, 11),
            'nome': ['Produto ' + str(i) for i in range(1, 11)],
            'preco': [10.5, 20.3, 15.2, 25.0, 30.1, 22.7, 19.9, 35.2, 42.5, 17.8],
            'quantidade': [100, 150, 200, 75, 90, 120, 300, 250, 80, 110]
        }

        df = pd.DataFrame(dados)

        caminho_arquivo = f'{PROCESSADO_DIR}/dados_exemplo.csv'
        df.to_csv(caminho_arquivo, index=False)
        
        logging.info(f"Arquivo de exemplo gerado: {caminho_arquivo}")
        logging.info(f"Total de {len(df)} registros criados")
        
        # Armazenar o caminho em um arquivo de texto
        with open(CAMINHO_INFO, 'w') as f:
            f.write(caminho_arquivo)
        logging.info(f"Caminho do arquivo salvo em: {CAMINHO_INFO}")
        
        # Retornar o caminho do arquivo para uso em tasks subsequentes via XCom
        return caminho_arquivo
        
    except Exception as e:
        logging.error(f"Erro ao gerar dados: {str(e)}")
        raise

gerar_dados = PythonOperator(
    task_id='gerar_dados',
    python_callable=gerar_dados_exemplo,
    dag=dag
)


def analisar_dados(**kwargs):
    """
    Lê o arquivo de dados e calcula estatísticas básicas.
    """
    try:
        import pandas as pd
        import numpy as np
        
        logging.info("Iniciando análise de dados")
        
        # Recuperar o caminho do arquivo da task anterior via XCom
        ti = kwargs['ti']
        caminho_arquivo = ti.xcom_pull(task_ids='gerar_dados')
        
        if not caminho_arquivo:
            logging.warning("Não foi possível obter o caminho do arquivo via XCom, tentando via arquivo")
            try:
                if os.path.exists(CAMINHO_INFO):
                    with open(CAMINHO_INFO, 'r') as f:
                        caminho_arquivo = f.read().strip()
                    logging.info(f"Caminho recuperado do arquivo: {caminho_arquivo}")
                else:
                    # Se ainda não funcionar, use o caminho padrão
                    caminho_arquivo = f'{PROCESSADO_DIR}/dados_exemplo.csv'
                    logging.warning(f"Usando caminho padrão: {caminho_arquivo}")
            except Exception as e:
                logging.error(f"Erro ao ler arquivo de caminho: {str(e)}")
                # Use o caminho padrão como fallback
                caminho_arquivo = f'{PROCESSADO_DIR}/dados_exemplo.csv'
                logging.warning(f"Usando caminho padrão após erro: {caminho_arquivo}")
        
        logging.info(f"Caminho do arquivo a ser analisado: {caminho_arquivo}")
        
        # Verificar se o arquivo existe
        if not os.path.exists(caminho_arquivo):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
        
        df = pd.read_csv(caminho_arquivo)
        
        # Verificar se o DataFrame tem os dados esperados
        colunas_esperadas = ['id', 'nome', 'preco', 'quantidade']
        for coluna in colunas_esperadas:
            if coluna not in df.columns:
                raise ValueError(f"Coluna esperada '{coluna}' não encontrada no arquivo")
        
        # Calcular estatísticas básicas - convertendo explicitamente para tipos nativos do Python
        estatisticas = {
            'total_produtos': int(len(df)),
            'preco_medio': float(round(df['preco'].mean(), 2)),
            'preco_maximo': float(df['preco'].max()),
            'preco_minimo': float(df['preco'].min()),
            'quantidade_total': int(df['quantidade'].sum())
        }
        
        # Exibir estatísticas para logs
        for chave, valor in estatisticas.items():
            logging.info(f"{chave}: {valor}")
        
        os.makedirs(TRANSFORMED_DIR, exist_ok=True)
        
        # Salvar estatísticas em um arquivo no diretório de dados transformados
        caminho_estatisticas = f'{TRANSFORMED_DIR}/estatisticas.txt'
        with open(caminho_estatisticas, 'w') as f:
            for chave, valor in estatisticas.items():
                f.write(f"{chave}: {valor}\n")
        
        logging.info(f"Estatísticas salvas em: {caminho_estatisticas}")
        
        # Converter o DataFrame para tipos nativos antes de salvar como CSV
        df_estatisticas = pd.DataFrame(
            [{'metrica': str(k), 'valor': float(v) if isinstance(v, (float, np.float64)) else int(v)} 
             for k, v in estatisticas.items()]
        )
        df_estatisticas.to_csv(f'{TRANSFORMED_DIR}/estatisticas.csv', index=False)
        
        # Retornar dicionário com valores convertidos para tipos Python nativos
        return estatisticas
        
    except Exception as e:
        logging.error(f"Erro ao analisar dados: {str(e)}")
        raise

analisar_dados = PythonOperator(
    task_id='analisar_dados',
    python_callable=analisar_dados,
    dag=dag
)


def verificar_resultado(**kwargs):
    """
    Verifica se todos os arquivos foram criados corretamente.
    """
    try:
        arquivos_esperados = [
            f'{DATA_DIR}/verificacao_ambiente.txt',
            f'{PROCESSADO_DIR}/dados_exemplo.csv',
            f'{TRANSFORMED_DIR}/estatisticas.txt',
            f'{TRANSFORMED_DIR}/estatisticas.csv'
        ]
        
        arquivos_faltando = []
        for arquivo in arquivos_esperados:
            if not os.path.exists(arquivo):
                arquivos_faltando.append(arquivo)
        
        if arquivos_faltando:
            logging.warning(f"Os seguintes arquivos não foram encontrados: {arquivos_faltando}")
            return False
        
        logging.info("Todos os arquivos foram criados com sucesso!")
        return True
        
    except Exception as e:
        logging.error(f"Erro ao verificar resultados: {str(e)}")
        raise

verificar_resultado = PythonOperator(
    task_id='verificar_resultado',
    python_callable=verificar_resultado,
    dag=dag
)


fim = DummyOperator(
    task_id='fim',
    dag=dag
)

# Definir dependências entre as tasks
inicio >> verificar_dirs >> verificar_ambiente >> gerar_dados >> analisar_dados >> verificar_resultado >> fim