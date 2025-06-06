# Atividades Práticas de ETL com Airflow e PostgreSQL

## Objetivo

Você deverá implementar um pipeline ETL completo que extraia dados de vendas de uma fonte web, realize transformações e carregue os dados em um modelo dimensional no PostgreSQL.

## Estrutura do Banco de Dados

Abaixo está o schema do banco de dados que você deverá utilizar. Este schema já está configurado no arquivo `dags/pipeline_etl_esqueleto.py`.

### Esquemas
- `dim`: Tabelas dimensionais
- `fato`: Tabelas de fatos
- `stage`: Tabelas de staging

### Tabelas Dimensionais
```sql
-- Dimensão Data
CREATE TABLE dim.data (
    chave_data SERIAL PRIMARY KEY,
    data_completa DATE NOT NULL,
    ano INT NOT NULL,
    mes INT NOT NULL,
    nome_mes VARCHAR(20) NOT NULL,
    dia INT NOT NULL,
    dia_semana INT NOT NULL,
    nome_dia VARCHAR(20) NOT NULL,
    trimestre INT NOT NULL,
    eh_fim_semana BOOLEAN NOT NULL
);

-- Dimensão Localização
CREATE TABLE dim.localizacao (
    chave_localizacao SERIAL PRIMARY KEY,
    cidade VARCHAR(100),
    estado VARCHAR(100),
    pais VARCHAR(100),
    continente VARCHAR(100),
    regiao VARCHAR(100),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimensão Produto
CREATE TABLE dim.produto (
    chave_produto SERIAL PRIMARY KEY,
    id_produto VARCHAR(50) NOT NULL,
    nome_produto VARCHAR(200) NOT NULL,
    categoria VARCHAR(100),
    subcategoria VARCHAR(100),
    preco DECIMAL(10,2),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimensão Cliente
CREATE TABLE dim.cliente (
    chave_cliente SERIAL PRIMARY KEY,
    id_cliente VARCHAR(50) NOT NULL,
    nome_cliente VARCHAR(200),
    email VARCHAR(200),
    telefone VARCHAR(50),
    segmento VARCHAR(50),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela Fato
```sql
-- Tabela Fato Vendas
CREATE TABLE fato.vendas (
    chave_venda SERIAL PRIMARY KEY,
    id_pedido VARCHAR(50) NOT NULL,
    chave_data INT REFERENCES dim.data(chave_data),
    chave_cliente INT REFERENCES dim.cliente(chave_cliente),
    chave_produto INT REFERENCES dim.produto(chave_produto),
    chave_localizacao INT REFERENCES dim.localizacao(chave_localizacao),
    quantidade INT NOT NULL,
    valor_venda DECIMAL(12,2) NOT NULL,
    lucro DECIMAL(12,2),
    desconto DECIMAL(4,2),
    custo_envio DECIMAL(10,2),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela de Staging
```sql
-- Tabela de Staging para dados brutos
CREATE TABLE stage.vendas_brutas (
    id SERIAL PRIMARY KEY,
    id_pedido VARCHAR(50),
    data_pedido DATE,
    data_envio DATE,
    modo_envio VARCHAR(50),
    id_cliente VARCHAR(50),
    nome_cliente VARCHAR(200),
    segmento VARCHAR(50),
    pais VARCHAR(100),
    cidade VARCHAR(100),
    estado VARCHAR(100),
    cep VARCHAR(20),
    regiao VARCHAR(50),
    id_produto VARCHAR(50),
    categoria VARCHAR(100),
    subcategoria VARCHAR(100),
    nome_produto VARCHAR(200),
    vendas DECIMAL(12,2),
    quantidade INT,
    desconto DECIMAL(4,2),
    lucro DECIMAL(12,2),
    data_importacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Atividades a Implementar

Você deverá implementar as seguintes partes do pipeline ETL no arquivo `pipeline_etl_esqueleto.py`:

### 1. Extração de Dados
- Implemente a função `extrair_dados()` para baixar o dataset de vendas Superstore da URL fornecida
- Salve os dados brutos localmente com um timestamp para controle de versão

### 2. Transformação de Dados - Staging
- Implemente a função `carregar_staging()` para:
  - Mapear as colunas do CSV para o formato esperado no banco
  - Realizar limpeza básica (tratar valores nulos, converter tipos de dados)
  - Carregar os dados na tabela de staging

### 3. Transformação e Carga - Dimensões
- Implemente a função `transformar_carregar_dimensoes()` para:
  - Extrair, transformar e carregar a dimensão Data
  - Extrair, transformar e carregar a dimensão Localização
  - Extrair, transformar e carregar a dimensão Produto
  - Extrair, transformar e carregar a dimensão Cliente

### 4. Transformação e Carga - Fatos
- Implemente a função `transformar_carregar_fatos()` para:
  - Juntar os dados do staging com as dimensões carregadas
  - Obter as chaves estrangeiras para cada dimensão
  - Calcular métricas adicionais (ex: custo de envio)
  - Carregar os dados na tabela fato

## Técnicas de Transformação a Implementar

Durante a implementação, você deve utilizar as seguintes técnicas:

1. **Limpeza de Dados**
   - Tratamento de valores nulos
   - Conversão de tipos de dados
   - Padronização de textos

2. **Modelagem Dimensional**
   - Identificação de dimensões e fatos
   - Criação de chaves surrogate
   - Implementação de relacionamentos

3. **Técnicas Avançadas**
   - Aplicação de Slowly Changing Dimensions (SCD) Tipo 2
   - Criação de atributos derivados
   - Agregações e sumarizações

## Extensões Opcionais

Após implementar o pipeline básico, você pode implementar estas melhorias:

1. **Dimensão Tempo** para capturar detalhes temporais (hora do dia, período, etc.)
2. **Hierarquias nas dimensões** (ex: produto -> subcategoria -> categoria)
3. **Indicadores de qualidade de dados** para detectar anomalias
4. **Carga incremental** em vez de truncar e recarregar
5. **Paralelização** de tarefas independentes no DAG

## Instruções para Execução

1. Utilize o arquivo `pipeline_etl_esqueleto.py` como base
2. Implemente cada função marcada com `# TODO: Implemente esta função`
3. Execute o DAG no Airflow para testar sua implementação
4. Verifique os resultados no banco de dados PostgreSQL

## Fonte de Dados

O dataset a ser utilizado está disponível na seguinte URL:
```
https://raw.githubusercontent.com/SF-DataScience/datasciencecourse/master/data/superstore_sales.csv
```