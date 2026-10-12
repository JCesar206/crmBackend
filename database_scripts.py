import sys
from database import engine, Base, SessionLocal
from models import Cliente, Cotizacion

def init_db():
    print("🚀 [INIT] Creando tablas en MySQL...")
    Base.metadata.create_all(bind=engine)
    print("✅ [INIT] ¡Tablas creadas correctamente!")

def seed_db():
    print("🌱 [SEED] Insertando datos de prueba...")
    db = SessionLocal()
    try:
        # Verificar si ya existen datos
        if db.query(Cliente).first():
            print("⚠️ [SEED] La base de datos ya contiene registros. Se omite el seed.")
            return

        cliente1 = Cliente(nombre="Ana Gómez", email="ana@empresa.com", empresa="Tech Solutions")
        cliente2 = Cliente(nombre="Carlos Ruiz", email="carlos@logistica.com", empresa="Logística Global")
        
        db.add_all([cliente1, cliente2])
        db.commit()

        # Agregar cotizaciones de prueba
        cot1 = Cotizacion(cliente_id=1, titulo="Desarrollo de Landing Page", total=1200.00, estado="Aceptada")
        cot2 = Cotizacion(cliente_id=2, titulo="Consultoría de Seguridad", total=850.50, estado="Pendiente")

        db.add_all([cot1, cot2])
        db.commit()
        print("✅ [SEED] ¡Datos de prueba insertados con éxito!")
    except Exception as e:
        print(f"❌ [SEED_ERROR] Error al poblar datos: {e}")
        db.rollback()
    finally:
        db.close()

def reset_db():
    print("⚠️ [RESET] Eliminando todas las tablas de la base de datos...")
    Base.metadata.drop_all(bind=engine)
    print("🗑️ [RESET] Tablas eliminadas. Recreando estructura...")
    init_db()
    print("✨ [RESET] ¡Base de datos reiniciada por completo!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python database_scripts.py [init | seed | reset]")
    else:
        command = sys.argv[1]
        if command == "init":
            init_db()
        elif command == "seed":
            seed_db()
        elif command == "reset":
            reset_db()
        else:
            print(f"Comando desconocido: {command}")