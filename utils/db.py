from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import yaml

def load_config(config_path='config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

config = load_config()

DATABASE_URL = f"postgresql://{config['database']['user']}:{config['database']['password']}@" \
               f"{config['database']['host']}:{config['database']['port']}/{config['database']['dbname']}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    return SessionLocal()
