import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.core.config import settings
from urllib.parse import urlparse

def create_database():
    # URL de conexión
    db_url = settings.DATABASE_URL
    parsed_url = urlparse(db_url)
    
    # Datos de conexión al servidor
    dbname = parsed_url.path[1:]
    user = parsed_url.username
    password = parsed_url.password
    host = parsed_url.hostname
    port = parsed_url.port or 5432

    # Conectar al servidor Postgres base para crear la nueva DB
    try:
        con = psycopg2.connect(
            dbname='postgres', 
            user=user, 
            password=password, 
            host=host, 
            port=port
        )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        
        # Verificar si la DB ya existe
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbname}'")
        exists = cur.fetchone()
        
        if not exists:
            print(f"Creando base de datos '{dbname}'...")
            cur.execute(f'CREATE DATABASE "{dbname}"')
            print(f"Base de datos '{dbname}' creada satisfactoriamente.")
        else:
            print(f"La base de datos '{dbname}' ya existe.")
            
        cur.close()
        con.close()
        
    except Exception as e:
        print(f"Error al intentar crear la base de datos: {e}")

if __name__ == "__main__":
    create_database()
