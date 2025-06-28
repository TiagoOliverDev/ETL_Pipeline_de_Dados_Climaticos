import pandas as pd
import sys
from sqlalchemy.exc import SQLAlchemyError
from src.db.db_connections import connect_db_sqlalchemy  
from src.utils.logger import logger

def load_data(df: pd.DataFrame):
    """
    Recebe um DataFrame e insere os dados na tabela natal_weather_records do banco PostgreSQL.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("O objeto recebido não é um DataFrame válido.")
    
    try:
        engine = connect_db_sqlalchemy()

        df.to_sql(
            name='natal_weather_records',
            con=engine,
            if_exists='append',
            index=False
        )
        logger.info("✅ Dados inseridos na tabela natal_weather_records com sucesso!")
    except SQLAlchemyError as e:
        logger.error(f"Erro ao inserir dados no banco: {e}")
        raise  
