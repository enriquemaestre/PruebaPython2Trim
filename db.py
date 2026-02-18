from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

password = quote_plus("Veroguevi402286*")
DATABASE_URL = f"mysql+pymysql://root:{password}@localhost:3306/fastapi_incidentes"
print("Conectando a: ", DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print("Conexión a la DB OK")
    except Exception as e:
        print("Error al conectar:", e)