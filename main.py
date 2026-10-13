from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db
from models import Cliente, Cotizacion
from pydantic import BaseModel

app = FastAPI(title="CRM API", version="1.0")

# Configurar CORS para que tu frontend React (ej. puerto 3000 o 5173) pueda conectarse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquemas Pydantic para validar los datos que entran por JSON
class ClienteCreate(BaseModel):
    nombre: str
    email: str
    empresa: str = None

class CotizacionCreate(BaseModel):
    cliente_id: int
    titulo: str
    total: float
    estado: str = "Pendiente"

@app.get("/")
def read_root():
    print("📥 [LOG] Petición recibida en la ruta raíz GET /")
    return {"message": "¡Servidor de Python corriendo al 100%! 🚀"}

# Endpoints clientes
@app.get("/clientes")
def get_clientes(db: Session = Depends(get_db)):
    print("📥 [LOG] Consultando lista de clientes...")
    clientes = db.query(Cliente).all()
    return clientes

@app.post("/clientes")
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    print(f"📥 [LOG] Creando nuevo cliente: {cliente.email}")
    nuevo = Cliente(nombre=cliente.nombre, email=cliente.email, empresa=cliente.empresa)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    print(f"✅ [LOG] Cliente creado con ID: {nuevo.id}")
    return nuevo

# Endpoints cotizaciones
@app.get("/cotizaciones")
def get_cotizaciones(db: Session = Depends(get_db)):
    print("📥 [LOG] Consultando lista de cotizaciones...")
    cotizaciones = db.query(Cotizacion).all()
    return cotizaciones

@app.post("/cotizaciones")
def create_cotizacion(cot: CotizacionCreate, db: Session = Depends(get_db)):
    print(f"📥 [LOG] Creando cotización para el cliente ID: {cot.cliente_id}")
    nueva = Cotizacion(cliente_id=cot.cliente_id, titulo=cot.titulo, total=cot.total, estado=cot.estado)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    print(f"✅ [LOG] Cotización creada con ID: {nueva.id}")
    return nueva