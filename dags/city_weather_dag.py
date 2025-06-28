import sys
from pathlib import Path
from datetime import datetime
import pendulum

DAG_FOLDER = Path(__file__).parent
PROJECT_ROOT = DAG_FOLDER.parent
sys.path.append(str(PROJECT_ROOT))

from airflow.decorators import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from src.etl.extract_data import extract_data
from src.etl.transform_data import transform_data
from src.etl.json_loader import loading_data, find_most_recent_data
from src.etl.load_data import load_data
from config.settings import FILES_FOLDER_RAW, PROCESSED_DATA_DIR, NATAL_TZ


@dag(
    dag_id='natal_weather_pipeline',
    start_date=pendulum.datetime(2024, 1, 1, tz="America/Recife"),
    schedule_interval='0 */6 * * *',
    catchup=False,
    tags=["etl", "weather", "natal"],
    doc_md="""
    ### ☁️ Pipeline ETL de Clima - Natal/RN
    Coleta dados da Open-Meteo, transforma e insere no PostgreSQL.
    """,
)
def dag_city_weather_pipeline():
    
    DATETIME = datetime.now(NATAL_TZ)
    TIMESTAMP = DATETIME.strftime('%Y-%m-%d_%H-%M-%S')

    @task()
    def extract():
        from datetime import datetime
        execution_dt = datetime.now(NATAL_TZ)
        timestamp = execution_dt.strftime('%Y-%m-%d_%H-%M-%S')
        output_path = FILES_FOLDER_RAW / f"natal_weather_{timestamp}.json"
        extract_data(output_path=output_path, execution_dt=execution_dt, latitude='-5.7945', longitude='-35.2110')
        return str(output_path)

    @task()
    def transform(output_path: str):
        path = find_most_recent_data(FILES_FOLDER_RAW)
        raw_df = loading_data(path)
        processed_df = transform_data(
            df=raw_df,
            processed_data_dir=PROCESSED_DATA_DIR,
            timestamp=TIMESTAMP
        )
        return processed_df.to_json(orient="records", date_format='iso')

    @task()
    def load(processed_json: str):
        import pandas as pd
        df = pd.read_json(processed_json, convert_dates=['measurement_datetime', 'record_timestamp'])
        load_data(df)

    ensure_table_exists = SQLExecuteQueryOperator(
        task_id="ensure_table_exists",
        conn_id="local_postgres_conn",  
        sql="""
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
        """
    )

    # Orquestração das tasks: extract -> transform -> ensure_table_exists -> load
    extracted = extract()
    transformed = transform(extracted)
    transformed >> ensure_table_exists  # Garante tabela antes de carregar
    ensure_table_exists >> load(transformed)

dag_city_weather_pipeline()
