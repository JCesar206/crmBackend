from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

# Cambia 'root' y 'tu_password' por tus credenciales locales de MySQL
DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "crm_db"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print("🔄 [DB_CONFIG] Intentando conectar con el servidor MySQL...")

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    
    # Prueba rápida de conexión
    with engine.connect() as connection:
        print("✅ [DB_SUCCESS] ¡Conexión exitosa con la base de datos MySQL!")
except Exception as e:
    print(f"❌ [DB_ERROR] Falló la conexión a MySQL: {e}")

# Dependencia para obtener la sesión de BD en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()