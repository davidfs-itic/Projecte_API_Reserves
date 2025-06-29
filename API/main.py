#https://fastapi.tiangolo.com/#installation
from fastapi import FastAPI, HTTPException
from db import get_db_connection
from models import Usuari, Material, Reserva
# from fastapi.middleware.cors import CORSMiddleware

import time
import logging
# Import OpenTelemetry libraries
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter # Importa ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.mysql import MySQLInstrumentor


# Habilitar el logging de OpenTelemetry
logging.basicConfig(level=logging.DEBUG) # O logging.INFO, pero DEBUG será más detallado
# Configurar loggers específicos de OpenTelemetry a DEBUG
logging.getLogger("opentelemetry").setLevel(logging.DEBUG)
logging.getLogger("opentelemetry.sdk").setLevel(logging.DEBUG)
logging.getLogger("opentelemetry.sdk.trace").setLevel(logging.DEBUG)
logging.getLogger("opentelemetry.instrumentation").setLevel(logging.DEBUG)
logging.getLogger("opentelemetry.exporter").setLevel(logging.DEBUG)

DELAY_TIME=3


# 1. Configure OpenTelemetry PRIMER (abans de qualsevol altra cosa)
resource = Resource.create(attributes={
    "service.name": "reserves-api",
    "service.version": "1.0.0",
})

provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# 2. Configura els exportadors
span_exporter_otlp = OTLPSpanExporter(endpoint="http://alloy:4317", insecure=True)
span_processor_otlp = BatchSpanProcessor(span_exporter_otlp)
provider.add_span_processor(span_processor_otlp)

span_exporter_console = ConsoleSpanExporter()
span_processor_console = BatchSpanProcessor(span_exporter_console)
provider.add_span_processor(span_processor_console)

# 3. Instrumenta MySQL ABANS de crear l'app i ABANS d'importar/usar mysql.connector
MySQLInstrumentor().instrument(
    tracer_provider=provider,
    # Dona error amb el comenter. per tant es deshabilita
    enable_commenter=False,
    commenter_options={}
)

# 4. Crea l'app FastAPI
app = FastAPI()

# 5. Instrumenta FastAPI després de crear l'app
FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)



#PyMySQLInstrumentor().instrument(tracer_provider=provider)

# Configura els origens permesos
# origins = [
#     "http://127.0.0.1:8443",  # Per React o altres frameworks en desenvolupament
#     "http://reservesapi:8443",  # Si accedeixes des del mateix servidor
#     "*",  # des de tot arreu.
# ]

# Afegeix el middleware de CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,  # Origines permesos
#     allow_credentials=True, # Permetre cookies i autenticació
#     allow_methods=["*"],    # Permetre tots els mètodes HTTP (GET, POST, PUT, DELETE, etc.)
#     allow_headers=["*"],    # Permetre tots els encapçalaments
# )

@app.get("/")
def home():
    return {"message": "API RESERVES, amb FastAPI i MariaDB sense routers"}

# CRUD per a Usuaris
@app.post("/usuaris/")
def crear_usuari(usuari: Usuari):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuaris (id, nom, rol, password) VALUES (%s, %s, %s, %s)",
            (usuari.id, usuari.nom, usuari.rol, usuari.password),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Usuari creat correctament"}

@app.get("/usuaris/{id}")
def obtenir_usuari(id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuaris WHERE id = %s", (id,))
    usuari = cursor.fetchone()
    cursor.close()
    conn.close()
    if not usuari:
        raise HTTPException(status_code=404, detail="Usuari no trobat")
    return usuari

@app.get("/login/{usuari}")
def obtenir_usuari(usuari: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id,nom,rol FROM usuaris WHERE nom = %s", (usuari,))    
    usuari = cursor.fetchone()
    cursor.close()
    conn.close()
    if not usuari:
        raise HTTPException(status_code=404, detail="Usuari no trobat")
    return usuari

#1. Afegir Material (POST)
@app.post("/materials/")
def crear_material(material: Material):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO materials (id, descripcio, imatge) VALUES (%s, %s, %s)",
            (material.id, material.descripcio, material.imatge),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Material creat correctament"}


#2. Obtenir Material per ID (GET)
@app.get("/materials/{id}")
def obtenir_material(id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM materials WHERE id = %s", (id,))
    material = cursor.fetchone()
    cursor.close()
    conn.close()
    if not material:
        raise HTTPException(status_code=404, detail="Material no trobat")
    return material

#3. Obtenir tots els Materials (GET)
@app.get("/materials/")
def obtenir_tots_materials():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM materials")
    materials = cursor.fetchall()
    cursor.close()
    conn.close()
    return materials

#4. Modificar Material (PUT)
@app.put("/materials/{id}")
def modificar_material(id: int, material: Material):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE materials SET descripcio = %s, imatge = %s WHERE id = %s",
            (material.descripcio, material.imatge, id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Material no trobat")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Material actualitzat correctament"}

#5. Eliminar Material (DELETE)
@app.delete("/materials/{id}")
def eliminar_material(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM materials WHERE id = %s", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Material no trobat")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Material eliminat correctament"}

#-----------------------------------------------------------------------
#   RESERVES
#-----------------------------------------------------------------------

#1. Afegir Reserva (POST)
@app.post("/reserves/")
def crear_reserva(reserva: Reserva):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO reserves (idusuari, idmaterial, datareserva, datafinal) VALUES (%s, %s, %s, %s)",
            (reserva.idusuari, reserva.idmaterial, reserva.datareserva, reserva.datafinal),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Reserva creada correctament"}

#2. Obtenir Reserva per ID (GET)
@app.get("/reserves/{idusuari}/{idmaterial}/{datareserva}")
def obtenir_reserva(idusuari: int, idmaterial: int, datareserva: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM reserves WHERE idusuari = %s AND idmaterial = %s AND datareserva = %s",
        (idusuari, idmaterial, datareserva),
    )
    reserva = cursor.fetchone()
    cursor.close()
    conn.close()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no trobada")
    return reserva

#3. Obtenir totes les Reserves d'un Usuari (GET)
@app.get("/reserves/usuari/{idusuari}")
def obtenir_reserves_usuari(idusuari: int):
    time.sleep(DELAY_TIME)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT reserves.*,materials.descripcio as descripcio,materials.imatge FROM reserves inner join materials on reserves.idmaterial=materials.id WHERE idusuari = %s", (idusuari,))
    reserves = cursor.fetchall()
    cursor.close()
    conn.close()
    return reserves

#4. Modificar Reserva (PUT)
@app.put("/reserves/{idusuari}/{idmaterial}/{datareserva}")
def modificar_reserva(idusuari: int, idmaterial: int, datareserva: str, reserva: Reserva):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE reserves SET datafinal = %s WHERE idusuari = %s AND idmaterial = %s AND datareserva = %s",
            (reserva.datafinal, idusuari, idmaterial, datareserva),
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Reserva no trobada")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Reserva actualitzada correctament"}

#5. Eliminar Reserva (DELETE)

@app.delete("/reserves/{idusuari}/{idmaterial}/{datareserva}")
def eliminar_reserva(idusuari: int, idmaterial: int, datareserva: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM reserves WHERE idusuari = %s AND idmaterial = %s AND datareserva = %s",
            (idusuari, idmaterial, datareserva),
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Reserva no trobada")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Reserva eliminada correctament"}
