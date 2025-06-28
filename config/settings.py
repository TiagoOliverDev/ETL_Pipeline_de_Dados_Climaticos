from pathlib import Path
import pytz

# Diretórios
FILES_FOLDER_RAW = Path('data/raw')
PROCESSED_DATA_DIR = Path('data/processed')

# Timezone
NATAL_TZ = pytz.timezone("America/Recife")