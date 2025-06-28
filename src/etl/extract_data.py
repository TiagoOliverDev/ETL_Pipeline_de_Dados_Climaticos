import requests
import os
import json
from config.settings import FILES_FOLDER_RAW
from src.utils.logger import logger
from pathlib import Path

def extract_data(output_path: Path, execution_dt: str, latitude: str, longitude: str):
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&timezone=auto'
    
    response = requests.get(url)
    data = response.json()

    os.makedirs(FILES_FOLDER_RAW, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    logger.info(f'Arquivo salvo em {output_path}')