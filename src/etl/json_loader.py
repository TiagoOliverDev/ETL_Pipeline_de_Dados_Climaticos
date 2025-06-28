import json
import pandas as pd
from pathlib import Path
from src.utils.logger import logger


def loading_data(path: Path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data_json = json.load(f)
        
        current = data_json['current_weather']
        
        # Adiciona lat/lon, timezone, elevation
        current['latitude'] = data_json.get('latitude')
        current['longitude'] = data_json.get('longitude')
        current['timezone'] = data_json.get('timezone')
        current['elevation'] = data_json.get('elevation')
        
        df = pd.DataFrame([current])
        
        logger.info('Dados carregados e normalizados com sucesso. √')
        return df

    except Exception as e:
        logger.error(f'Erro ao carregar dados: {e}')
        raise
    
def find_most_recent_data(files_folder: Path) -> str:
    """
    Retorna o caminho do arquivo JSON mais recente na pasta especificada.
    Os arquivos devem seguir o padrão 'natal_weather_*.json'.
    """
    files = sorted(files_folder.glob('natal_weather_*.json'), reverse=True)

    if not files:
        raise FileNotFoundError(f'Nenhum arquivo JSON encontrado na pasta {files_folder}.')

    return str(files[0])
