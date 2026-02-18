from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from db import get_db
from models import Incidencia
from deps import get_current_user
from auth import router as auth_router

app = FastAPI(
    title= "Prueba trimestral 2",
    description = "Examen de Python",
    version= "1.0.0"
)

class IncidenciaCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    descripcion: str = Field(min_length=1, max_length=200)
    prioridad: str = Field(min_length=1, max_length=100)
    estado: str = Field(min_length=1, max_length=100)

class IncidenciaResponse(IncidenciaCreate):
    id: int
    class Config:
        from_atributes = True

app.include_router(auth_router)

@app.get("/privado")
def privado(usuario: str = Depends(get_current_user)):
    return {"mensaje": f"Hol {usuario}, estás autenticado"}

@app.get("/")
def root():
    return {"ok":True, "mensaje":"FastAPI funcionando, ve a /docs"}

@app.get("/incidencias", response_model=list[IncidenciaResponse])
def listar_incidencias(db: Session = Depends(get_db)):
    return db.query(Incidencia).all()

@app.get("/incidencias/{incidencia_id}", response_model=IncidenciaResponse)
def obtener_incidencia(incidencia_id: int, db: Session = Depends(get_db)):
    inc = db.query(Incidencia).filter(Incidencia.id == incidencia_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada")
    return inc

@app.post("/incidencias", response_model=IncidenciaResponse, status_code=201)
def crear_incidencia(incidencia: IncidenciaCreate, db: Session = Depends(get_db)):
    nueva = Incidencia(titulo=incidencia.titulo,descripcion= incidencia.descripcion, prioridad= incidencia.prioridad, estado = incidencia.estado)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva