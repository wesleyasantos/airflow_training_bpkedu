# Guia de Configuração Rápida

Este guia explica como configurar e iniciar rapidamente o ambiente para o pipeline ETL com Airflow e PostgreSQL.

## Pré-requisitos

- [Docker](https://www.docker.com/products/docker-desktop/) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) instalado
- Aproximadamente 4GB de RAM disponível para os contêineres Docker
- 2GB de espaço em disco para imagens e volumes

## Passos para Configuração

### 1. Preparar o ambiente

1. Clone ou baixe este repositório para sua máquina local
2. Abra um terminal e navegue até a pasta do projeto

### 2. Iniciar os contêineres Docker

Execute o seguinte comando para iniciar todos os serviços:

```bash
docker-compose up -d
```

Este comando iniciará:
- Um contêiner PostgreSQL (banco de dados)
- Um contêiner Airflow (plataforma de orquestração)

> **Nota:** Na primeira execução, o Docker irá baixar as imagens necessárias, o que pode levar alguns minutos dependendo da sua conexão de internet.

### 3. Verificar se os serviços estão funcionando

Após alguns instantes, verifique se os contêineres estão em execução:

```bash
docker ps
```

Você deverá ver algo semelhante a:
```
CONTAINER ID   IMAGE                 COMMAND                  STATUS          PORTS                    NAMES
abc123def456   apache/airflow:2.7.1  "bash -c 'airflow db…"   Up 2 minutes    0.0.0.0:8080->8080/tcp   airflow
xyz789uvw321   postgres:14           "docker-entrypoint.s…"   Up 2 minutes    0.0.0.0:5432->5432/tcp   postgres
```

### 4. Acessar o Airflow

1. Abra seu navegador web
2. Acesse: http://localhost:8080
3. Faça login com as credenciais:
   - Usuário: `admin`
   - Senha: `admin`

### 5. Conectar ao Banco de Dados PostgreSQL

Você pode conectar-se ao PostgreSQL usando qualquer cliente SQL (como DBeaver, pgAdmin, etc.) com as seguintes configurações:

- Host: `localhost`
- Porta: `5432`
- Usuário: `airflow`
- Senha: `airflow`
- Banco de dados: `airflow`

### 6. Executar o Pipeline ETL

1. No Airflow, localize o DAG chamado `pipeline_etl_esqueleto`
2. Ative o DAG clicando no botão de toggle à esquerda do nome
3. Clique no nome do DAG para ver os detalhes
4. Execute o DAG manualmente clicando no botão "Trigger DAG"

### 7. Verificar a execução

1. Acompanhe o progresso na interface do Airflow
2. Verifique as logs de cada tarefa para entender o processo
3. Após a conclusão bem-sucedida, explore os dados no PostgreSQL

## Resolução de Problemas

### O Airflow não está acessível

- Verifique se os contêineres estão em execução: `docker ps`
- Verifique as logs do contêiner: `docker logs airflow`
- Reinicie os serviços: `docker-compose restart`

### Erros na execução do DAG

- Verifique as logs da tarefa específica no Airflow
- Certifique-se de que o banco de dados PostgreSQL está acessível
- Verifique se a URL do conjunto de dados está disponível

### Falta de memória

Se o Docker apresentar problemas de memória:
- Aumente a alocação de memória nas configurações do Docker
- Feche aplicações desnecessárias antes de iniciar os contêineres

## Desligando o Ambiente

Quando terminar de usar o ambiente, desligue os contêineres para liberar recursos:

```bash
docker-compose down
```

Para remover também os volumes (dados persistentes):

```bash
docker-compose down -v
```

> **Atenção:** O comando acima removerá todos os dados processados pelo pipeline. Use apenas se quiser começar do zero. 