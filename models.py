from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    empresa = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación: Un cliente tiene muchas cotizaciones
    cotizaciones = relationship("Cotizacion", back_populates="cliente", cascade="all, delete")

class Cotizacion(Base):
    __tablename__ = "cotizaciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    titulo = Column(String(150), nullable=False)
    total = Column(Float, nullable=False)
    estado = Column(String(50), default="Pendiente") # Pendiente, Aceptada, Rechazada
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación inversa
    cliente = relationship("Cliente", back_populates="cotizaciones")