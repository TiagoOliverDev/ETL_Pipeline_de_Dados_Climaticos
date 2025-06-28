import pandas as pd
from datetime import datetime
from pathlib import Path
from config.settings import NATAL_TZ
from src.utils.logger import logger


def transform_data(df: pd.DataFrame, processed_data_dir: Path, timestamp: str):
    df = df.rename(columns={
        'temperature': 'temperature_celsius',
        'windspeed': 'wind_speed_kmh',
        'winddirection': 'wind_direction_degrees',
        'weathercode': 'weather_condition_code',
        'time': 'measurement_datetime',
        'interval': 'interval_seconds'
    })

    df['record_timestamp'] = pd.to_datetime(datetime.now(NATAL_TZ)).floor('s')

    # Converte measurement_datetime para datetime com timezone UTC
    df['measurement_datetime'] = pd.to_datetime(df['measurement_datetime'])
    df['measurement_datetime'] = df['measurement_datetime'].dt.tz_localize('UTC').dt.tz_convert(NATAL_TZ)

    df['measurement_datetime'] = df['measurement_datetime'].dt.tz_localize(None)

    output_filename = f'processed_natal_weather_{timestamp}.csv'
    output_path = processed_data_dir / output_filename

    processed_data_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    logger.info(f'Dados transformados salvos em {processed_data_dir} √')
    return df