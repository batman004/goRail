# settings.py
from dotenv import load_dotenv
load_dotenv()

# Verbose
load_dotenv(verbose=True)

# Explicit path to '.env'
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

import os
DEVELOPMENT_DATABASE_URI = os.getenv('Development_Database_URI')
PRODUCTION_DATABASE_URI  = os.getenv('Production_Database_URI')
