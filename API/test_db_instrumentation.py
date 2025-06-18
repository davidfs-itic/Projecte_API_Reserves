import logging
import mysql.connector
from mysql.connector import pooling
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.mysql import MySQLInstrumentor

# Habilitar el logging de OpenTelemetry
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("opentelemetry").setLevel(logging.DEBUG)
logging.getLogger("opentelemetry.sdk").setLevel(logging.DEBUG)
logging.getLogger("opentelemetry.sdk.trace").setLevel(logging.DEBUG)
logging.getLogger("opentelemetry.instrumentation").setLevel(logging.DEBUG)
logging.getLogger("opentelemetry.exporter").setLevel(logging.DEBUG)

# 1. Configuració bàsica d'OpenTelemetry
resource = Resource.create(attributes={
    "service.name": "test-db-app",
    "service.version": "1.0.0",
})

provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# 2. Configura l'exportador de consola
span_exporter_console = ConsoleSpanExporter()
span_processor_console = BatchSpanProcessor(span_exporter_console)
provider.add_span_processor(span_processor_console)

# 3. Instrumenta MySQL/MariaDB
MySQLInstrumentor().instrument(tracer_provider=provider)

# Configura la connexió a MariaDB (has d'adaptar-ho a la teva configuració real)
db_config = {
    'host': 'mariadb', # Assegura't que 'mariadb' es resol correctament o usa una IP
    'user': 'david',
    'password': '1357924680',
    'database': 'reserves',
    'collation': 'utf8mb4_general_ci'
}

db_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config)

def run_db_query():
    print("\n--- Realitzant consulta a la DB ---")
    conn = None
    cursor = None
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT 1 + 1 AS result;") # Consulta simple per provar
        result = cursor.fetchone()
        print(f"Resultat de la consulta: {result}")

        cursor.execute("SELECT id, nom, rol FROM usuaris LIMIT 1;") # Una consulta a la teva taula
        user = cursor.fetchone()
        print(f"Usuari de la DB: {user}")

    except Exception as e:
        print(f"Error en la consulta a la DB: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    print("--- Consulta DB finalitzada ---\n")

if __name__ == "__main__":
    run_db_query()
    # Per assegurar-nos que els spans s'exporten abans que el programa finalitzi
    provider.force_flush()