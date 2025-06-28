from src.etl.extract_data import extract_data
from src.etl.transform_data import transform_data
from src.etl.json_loader import loading_data, find_most_recent_data
from src.etl.load_data import load_data
from datetime import datetime
from config.settings import FILES_FOLDER_RAW, PROCESSED_DATA_DIR, NATAL_TZ
from src.utils.logger import logger


def main(latitude: str, longitude: str):
    """
    Executa o pipeline ETL completo para coleta de dados meteorológicos de Natal/RN
    usando a API do Open-Meteo.
    """
    DATETIME = datetime.now(NATAL_TZ)
    TIMESTAMP = DATETIME.strftime('%Y-%m-%d_%H-%M-%S')
    output_path = FILES_FOLDER_RAW / f"natal_weather_{TIMESTAMP}.json"

    try:
        logger.info("="*50)
        logger.info("Iniciando pipeline ETL - Natal Weather 🌤️")
        logger.info("="*50)

        logger.info("\n🔎 [1/3] Extraindo dados da Open-Meteo...")
        extract_data(output_path=output_path, execution_dt=DATETIME, latitude=latitude, longitude=longitude)
        path = find_most_recent_data(FILES_FOLDER_RAW)
        logger.info(f"✅ Arquivo extraído: {path}\n")

        logger.info("🛠️ [2/3] Carregando e normalizando dados do JSON...")
        raw_df = loading_data(path)
        logger.info("✅ Dados carregados\n")

        logger.info("📦 [2/3] Transformando dados para o formato final...")
        processed_df = transform_data(
            df=raw_df,
            processed_data_dir=PROCESSED_DATA_DIR,
            timestamp=TIMESTAMP
        )
        logger.info("✅ Transformação concluída\n")

        logger.info("🚚 [3/3] Enviando dados para o banco de dados...")
        load_data(df=processed_df)
        logger.info("✅ Dados inseridos no banco com sucesso!\n")

        logger.info("="*50)
        logger.info("🏁 Pipeline finalizado com sucesso!")
        logger.info("="*50)

    except Exception as e:
        logger.warning("="*50)
        logger.error(f"❌ Ocorreu um erro no pipeline: {e}")
        logger.warning("="*50)

if __name__ == "__main__":
    main(latitude='-5.7945', longitude='-35.2110') # LAT e LONG estático de Natal/RN
