# 🌦️ Natal METEO API Pipeline

Pipeline ETL para coleta, processamento e armazenamento de dados meteorológicos de Natal, utilizando **Python**, **Apache Airflow** e **PostgreSQL**.

---

## 📚 Visão Geral

- **Extração:** Coleta dados da API METEO e salva em JSON.
- **Transformação:** Normaliza, limpa e transforma os dados em CSV.
- **Carga:** Insere os dados processados em um banco PostgreSQL.
- **Orquestração:** Todo o fluxo é automatizado via Apache Airflow.

---

## 🗂️ Estrutura do Projeto

```bash
api_meteo_pipeline/
├── config/                  # Configurações globais do pipeline
│   └── settings.py
├── dags/                    # DAGs do Airflow
│   └── city_weather_dag.py
├── data/                    # Dados brutos e processados (ignorado pelo git)
│   ├── raw/
│   └── processed/
├── logs/                    # Logs do Airflow (ignorado pelo git)
├── notebooks/               # Notebooks de análise e exploração
├── plugins/                 # Plugins customizados do Airflow (opcional)
├── src/     
│   ├── db/                  # Arquivo de conexão no banco dinâmico (Pode conectar localmente via variáveis .env ou pode conectar no banco do Airflow via connections id)
│   │   └── db_connections.py      
│   ├── etl/                 # Aonde a mágica acontece, aqui fica o ETL do projeto
│   │   └── extract_data.py
│   │   └── json_loader.py
│   │   └── load_data.py
│   │   └── transform_data.py
│   ├── utils/               # Aqui fica algumas funções úteis
│   │   └── logger.py
├── tests/                   # Testes automatizados
├── .env.example             # Exemplo de Variáveis de ambiente 
├── .gitignore
├── .dockerignore
├── docker-compose.yml       # Orquestração dos containers
├── Dockerfile               # Build customizado (opcional)
├── requirements.txt         # Dependências Python
└── main.py                  # Execução manual do pipeline (fora do Airflow)

```

---

## ⚙️ Configuração do Ambiente

### 1. **Pré-requisitos**

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.11+ (apenas para execução manual)

```
Crie um banco de dados local para acompanhar os dados caindo, insira as credênciais dele no .env e crie a tabela:

CREATE TABLE IF NOT EXISTS natal_weather_records (
    id SERIAL PRIMARY KEY,
    measurement_datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    interval_seconds INTEGER,
    temperature_celsius NUMERIC(5,2) NOT NULL,
    wind_speed_kmh NUMERIC(5,2) NOT NULL,
    wind_direction_degrees INTEGER NOT NULL,
    is_day INTEGER,
    weather_condition_code INTEGER NOT NULL,
    latitude NUMERIC(8,5) NOT NULL,
    longitude NUMERIC(8,5) NOT NULL,
    timezone VARCHAR(50) NOT NULL,
    elevation INTEGER NOT NULL,
    record_timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL
);


```

### 2. **Clone o Repositório**

```bash
git clone https://github.com/TiagoOliverDev/ETL_Pipeline_de_Dados_Climaticos
cd ETL_Pipeline_de_Dados_Climaticos
```

### 3. **Crie o Arquivo `.env`**

Baseie-se no modelo .env.example

### 4. **Suba o Ambiente com Docker Compose**

```bash
docker-compose up --build
```

- O Airflow estará disponível em: [http://localhost:8080](http://localhost:8080/)
- Usuário e senha definidos no `.env`

### 5. **Ative a DAG no Airflow**

1. Acesse a interface web do Airflow
2. Ative a DAG `natal_weather_pipeline`
3. Você pode disparar manualmente ou aguardar a execução automática

---

## 🛠️ Execução Manual (fora do Airflow)

Se desejar rodar o pipeline manualmente:

```bash
python main.py
```

---

## 🧩 Principais Arquivos

- `dags/city_weather_dag.py`: DAG principal do Airflow
- `src/etl/extract_data.py`: Função de extração da API
- `src/etl/transform_data.py`: Funções de transformação
- `src/etl/load_data.py`: Função de carga no PostgreSQL
- `config/settings.py`: Parâmetros globais do pipeline
- `main.py`: Execução manual do pipeline

---

## 📝 Observações

- Os diretórios `data/raw`, `data/processed` e `logs` estão no `.gitignore`
- A tabela é criada automaticamente no banco se não existir
- O Airflow usa a conexão nomeada `postgres_etl_conn`

---

## 📚 Licença

Este projeto é open-source e está sob a licença MIT.

---

## 👩‍💻 Desenvolvido por

Tiago Oliveira – Analista desenvolvedor e Engenheiro de dados em formação

- 💼 [LinkedIn](https://www.linkedin.com/in/tiago-oliveira-49a2a6205/)
- 💻 [GitHub](https://github.com/TiagoOliverDev)

