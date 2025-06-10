# ProjecteReserves-API

En aquest README, trobareu instruccions per instalar i fer el setup d'un projecte amb Fastapi (Reserves de material) i alguns subprojectes.


* Setup GIT 
  Com iniciar un projecte en github amb les fonts preexistents en local.
* Setup projecte Python:
  - Creació de un virtual envirovment per instal·lar dependències
  - Exemple de prompt per generar una api amb FastAPI
* Creació 


## Setup GIT
Per penjar un projecte en el que ja tinguem les fonts en local.
Podem crear un projecte buit en Git, !Sense Readme.me ni cap altre arxiu!
Després anem a la carpeta del projecte i:

```
git init
git config --global --add safe.directory '/mnt/9CB098F7B098D8DA/David/Institut TIC/Projecte/Reserva_Material/API_Reserves'
git add .
git remote add origin https://github.com/davidfs-itic/Projecte_API_Reserves.git
git commit -m "first commit"
git push -u origin main
```

## Setup projecte python
Des de la carpeta de projecte:
```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### Generar codi font amb la IA
Demanar la generació de fastapi:
Necessito un projecte en python amb fastapi, pero sense router, ni sqlalchemy. Només el módul fastapi i amb mariadb. les taules són aquestes i les relacions entre elles són aquestes.

#### Estructura del projecte
```
project/
│
├── API/
│   ├── main.py            # Fitxer principal de FastAPI
│   ├── db.py              # Fitxer configuracio BBDD
│   ├── models.py          # Fitxer classes ORM
│   ├── requirements.txt   # Dependències de Python
│   ├── ssl/
│   │   ├── cert.pem           # Certificat SSL
│   │   ├── key.pem            # Clau privada SSL
│   │
├── docker-compose.yml     # Fitxer Docker Compose
├── dockerfile             # Fitxer creacio imatge api
```


### Instal·lar dependèincies
Crear arxiu requirements.txt amb:
    fastapi
    uvicorn
    mysql-connector-python

Instal·lar dependències:
```
pip install --no-cache-dir -r requirements.txt
```

### Creacio certificats
```
openssl req -x509 -newkey rsa:4096 -keyout ./API/ssl/key.pem -out ./API/ssl/cert.pem -days 3650 -nodes
```

### Provar la api en local 
Cal tenir alguna base de dades preparada, en local o en remot. Vegeu com instal·lar un servidor de mariadb amb docker.


```
//Si estem en la carpeta del projecte
uvicorn API.main:app --host 0.0.0.0 --reload --port 8443 --ssl-keyfile ./API/ssl/key.pem --ssl-certfile ./API/ssl/cert.pem
uvicorn main:app --host 0.0.0.0 --reload --port 8443 --ssl-keyfile ./ssl/key.pem --ssl-certfile ./ssl/cert.pem
```

# Instal·lació docker (si utilitzem un ubuntu sense configurar)
Seguir instruccions a :
https://docs.docker.com/engine/install/ubuntu/


## Creació Network per als contenidors
```
docker network create -d bridge xarxa_docker1
```

## Crear contenidor per base de dades:
Preparar carpeta per base de dades:
```
mkdir -p /opt/docker/mariadb/datadir
chown 1000:1000 /opt/docker/mariadb -R
```

>[!NOTE]
> El chown es fa perque dins el contenidor, el procés de mysql es llença amb l'usuari 1000, i ha de tenir accés d'escriptura a la carpeta per poder inicialitzar la base de dades.

## docker-compose.yaml 
Amb aquest arxiu yaml, es crearà un servidor mysql 

```
version: '3.8'

services:
  mariadb:
    image: mariadb:11.4
    container_name: mariadb
    restart: unless-stopped
    environment:
      MARIADB_ROOT_PASSWORD: P@ssw0rd
    volumes:
      - mariadb_data:/var/lib/mysql
    networks:
      - xarxa1
    ports:
      - 3306:3306

networks:
  xarxa1:
    name: xarxa_docker1
    external: true


volumes:
  mariadb_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/docker/mariadb/datadir
```

### Connexio a la base de dades 

Quan tinguem un servidor de mysql preparat, ens podem connectar d'aquesta manera:

Instal·lem el client de mysql.
```
apt install -y mariadb-client-core
```

Ensn connectem al servidor
```
mysql -u root -p -h 127.0.0.1 
```

> [!IMPORTANT]
> Si el servidor està instal·lat amb docker, hem de posar el modificador -h 127.0.0.1
> Si no ho posem, no es connectarà per tcp, i buscara connectar-se per Unix Sockets.
> Per Unix Sockets, només funciona si el servidor mysql o mariadb està instalat en el SO directament i no en un contenidor
> Si el servidor està en un contenidor, l'arxiu .sock estarà ubicat dins el contenidor i no podrà ser accesible des de fora.




### Script creació (demanar a la IA)
Si ja tenim a punt el servidor de bases de dades a punt, podrem executar els scripts de creació.

```
create database reserves;

grant all privileges on reserves.* to david@'%' identified by '1357924680' with grant option;
flush privileges;

use reserves;

-- Crear la taula "usuaris"
CREATE TABLE IF NOT EXISTS usuaris (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Crear la taula "materials"
CREATE TABLE IF NOT EXISTS materials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcio VARCHAR(255) NOT NULL,
    imatge VARCHAR(255)
);

-- Crear la taula "reserves"
CREATE TABLE IF NOT EXISTS reserves (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idusuari INT NOT NULL,
    idmaterial INT NOT NULL,
    datareserva DATETIME NOT NULL,
    datafinal DATETIME NOT NULL,
    FOREIGN KEY (idusuari) REFERENCES usuaris(id) ON DELETE CASCADE,
    FOREIGN KEY (idmaterial) REFERENCES materials(id) ON DELETE CASCADE
);

-- Inserir registres d'exemple a "usuaris"
INSERT INTO usuaris (nom, rol, password) VALUES
('admin', 'admin', '$2b$12$examplehashedpassword1'), -- Afegeix un hash real amb bcrypt
('usuari1', 'user', '$2b$12$examplehashedpassword2'),
('usuari2', 'user', '$2b$12$examplehashedpassword3');

-- Inserir registres d'exemple a "materials"
INSERT INTO materials (descripcio, imatge) VALUES
('Ordinador portàtil HP', 'imatge_hp.jpg'),
('Projector Epson', 'imatge_epson.jpg'),
('Tauleta gràfica Wacom', 'imatge_wacom.jpg'),
('Trípode Manfrotto Befree Advanced', 'https://example.com/tripod1'),
('Càmera mirrorless Sony Alpha 7 III', 'https://example.com/camera2'),
('Micròfon Lavalier Rode SmartLav+', 'https://example.com/microphone2'),
('Kit de focus Aputure Amaran 100d', 'https://example.com/light2'),
('Estabilitzador DJI Ronin-S', 'https://example.com/gimbal1'),
('Monitor portàtil FeelWorld T7 7”', 'https://example.com/monitor1'),
('Grabador de so Zoom H6', 'https://example.com/recorder1');

-- Inserir registres d'exemple a "reserves"
INSERT INTO reserves (idusuari, idmaterial, datareserva, datafinal) VALUES
(1, 1, '2025-01-01', '2025-01-10'),
(2, 2, '2025-01-02', '2025-01-11'),
(3, 3, '2025-01-03', '2025-01-12'),
(1, 4, '2025-01-04', '2025-01-13'),
(2, 5, '2025-01-05', '2025-01-14'),
(3, 6, '2025-01-06', '2025-01-15'),
(1, 7, '2025-01-07', '2025-01-16'),
(2, 8, '2025-01-08', '2025-01-17'),
(3, 9, '2025-01-09', '2025-01-18'),
(1, 10, '2025-01-10', '2025-01-19'),
(2, 1, '2025-01-11', '2025-01-20'),
(3, 2, '2025-01-12', '2025-01-21'),
(1, 3, '2025-01-13', '2025-01-22'),
(2, 4, '2025-01-14', '2025-01-23'),
(3, 5, '2025-01-15', '2025-01-24'),
(1, 6, '2025-01-16', '2025-01-25'),
(2, 7, '2025-01-17', '2025-01-26'),
(3, 8, '2025-01-18', '2025-01-27'),
(1, 9, '2025-01-19', '2025-01-28'),
(2, 10, '2025-01-20', '2025-01-29');
```

## Pujar fonts al servidor (si no les teniu al git)

Per pujar arxius de l'ordinador local a un remot, es pot fer per ssh amb la comanda scp.

Aqui hi ha alguns exemples de com funciona, concretament per pujar arxius de la nostra api 

```
scp -i ~/.ssh/vockey.pem  ./docker* ubuntu@11.22.33.44:/opt/docker/reserves
scp -i ~/.ssh/vockey.pem  ./API/*.py ./API/*.txt ubuntu@11.22.33.44:/opt/docker/reserves/API
scp -i ~/.ssh/vockey.pem  ./API/ssl/* ubuntu@11.22.33.44:/opt/docker/reserves/API/ssl
```

## Creació contenidor amb Fastapi
Tenint en compte que ja tenim un dockerfile i un docker-compose, podem crear la imatge, el contenidor i engeger-ho amb docker-compose.

L'arxiu **dockerfile** crea una imatge de docker amb les nostres fonts, a partir d'una imatge de python standard.

L'arxiu **docker-compose** aixeca diferents contenidors, i defineix quins ports utilitzarà cadascún d'ells, a quina carpeta es guardaran les dades del contenidor (si cal), i a quina xarxa interna de docker es connectarà, per poder comunicar-se amb altres contenidors, sense necessàriament obrir un port en el SO amfitrió.

```
cd /opt/docker/reserves
docker-compose up -d --build
```

## Eliminar i tornar a crear el contenidor amb noves fonts
```
docker-compose down
docker-compose up -d --build
```

## Provar que funciona 
https://ipserver/docs

## Si no funciona, comprovar els logs del contenidor
```
docker logs reservesapi
```

# Altres contenidors:

## Servidor web simple

Crear una carpeta en /opt/docker/
per a que contingui els arxius del nostre webserver
```
mkdir -p /opt/docker/servidor_web/html
```


anar a la carpeta /opt/docker/servidorweb i crear l'arxiu docker-compose.yaml 
```
version: '3.8'

services:
  web:
    image: httpd:2.4
    container_name: servidor_web
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/local/apache2/htdocs
    restart: unless-stopped
    networks:
      - internal
networks:
  internal:
    name: internal
    external: true    
```

i des de la carpeta /opt/docker/servidorweb executar el docker-compose up -d 



## Servidor web amb configuracio i logs muntats en el sistema operatiu
Crear carpetes per al servidor:
```
mkdir -p /opt/docker/servidor_web/{html,config,logs}
```
Arxiu docker-compose-yaml
```
echo "\
version: '3.8'

services:
  web:
    image: httpd:2.4
    container_name: servidor_web
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/local/apache2/htdocs
      - ./logs:/usr/local/apache2/logs
      - ./config/httpd.conf:/usr/local/apache2/conf/httpd.conf
    restart: unless-stopped
    networks:
      - internal
networks:
  internal:
    name: internal
    external: true
"|sudo tee /opt/docker/servidor_web/docker-compose.yaml
```

Obtenir un ariux de configuració de mostra:
```
docker run --rm httpd:2.4 cat /usr/local/apache2/conf/httpd.conf > /opt/docker/servidor_web/config/httpd.conf
```

Executar el sevidor web en la carpeta
```
cd /opt/docker/servidor_web
docker-compose up -d
```


## Node Red
Aquest exemple no utilitza el docker-compose, sino que crea el contenidor node-red directament

```
mkdir -p /opt/docker/nodered/node1
chown -R 1000:1000 /opt/docker/nodered/

docker container create -p 1880:1880 -v /opt/docker/nodered/node1/:/data --restart=unless-stopped --network=internal --name node1 nodered/node-red:4.0.2-22
docker start node1
docker container list -a
```


## Grafana

```
version: '3.8'

services:
  grafana:
    image: grafana/grafana-oss:12.0.1 # Utilitzem la imatge oficial de Grafana
    container_name: grafana
    restart: unless-stopped # Assegura que Grafana es reinicia automàticament
    ports:
      - "3000:3000" # Mapeja el port 3000 del host al port 3000 del contenidor (port per defecte de Grafana)
    volumes:
      - /opt/docker/grafana:/var/lib/grafana # Mapeja el volum local a la ruta de dades de Grafana
    environment:
      # Configuració opcional: pots canviar el password de l'admin inicial
      # - GF_SECURITY_ADMIN_USER=admin
      # - GF_SECURITY_ADMIN_PASSWORD=your_secure_password
      # Si no els configures, l'usuari/password per defecte serà admin/admin
      - GF_PLUGINS_PREINSTALL=grafana-clock-panel
    networks:
      - internal # Connecta Grafana a la xarxa 'internal' que hem definit com a externa

networks:
  internal:
    name: xarxa_docker1 # Aquest és el nom de la xarxa que ja tens creada
    external: true # Indica que aquesta xarxa ja existeix i no ha de ser creada/eliminada per Compose
```

## Influxdb2  i Telegraf

```
sudo mkdir -p /opt/docker/influxdb/data
# No cal una carpeta específica per a Telegraf si només guarda la configuració en un volum.
# Però necessitaràs una carpeta per al fitxer de configuració de Telegraf al host.
sudo mkdir -p /opt/docker/telegraf/config
sudo chmod -R 777 /opt/docker/influxdb /opt/docker/telegraf # Ajusta permisos
```

### influxdb
```
version: '3.8'

services:
  influxdb:
    image: influxdb:2.7 # Utilitzem una versió estable d'InfluxDB 2.x
    container_name: influxdb # Nom del contenidor
    restart: unless-stopped # Assegura que InfluxDB es reinicia automàticament
    ports:
      - "8086:8086" # Mapeja el port 8086 del host al port 8086 del contenidor (port per defecte d'InfluxDB UI/API)
    volumes:
      - /opt/docker/influxdb/data:/var/lib/influxdb2 # Volum per a les dades persistents d'InfluxDB
      # - /opt/docker/influxdb/config:/etc/influxdb2 # Volum opcional per a fitxers de configuració personalitzats
    environment:
      # Configuració inicial obligatòria per a InfluxDB 2.x quan s'inicia per primera vegada
      - DOCKER_INFLUXDB_INIT_MODE=setup
      - DOCKER_INFLUXDB_INIT_USERNAME=admin # Nom d'usuari per defecte
      - DOCKER_INFLUXDB_INIT_PASSWORD=1357924680 # La contrasenya que heu especificat
      - DOCKER_INFLUXDB_INIT_ORG=Itic # Nom de l'organització per defecte
      - DOCKER_INFLUXDB_INIT_BUCKET=bucket1 # Nom del bucket de dades per defecte
      - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=dshdifuhb9733011237ewfdifnfldksaodhwieugfas # ATENCIÓ: Guardeu aquest token! El necessitareu per accedir a l'API o connectar Grafana.
    networks:
      - internal # Connecta InfluxDB a la xarxa definida com a 'internal'

networks:
  internal:
    name: xarxa_docker1 # Aquest és el nom real de la xarxa que ja heu creat (amb `docker network create -d bridge xarxa_docker1`)
    external: true # Indica a Docker Compose que aquesta xarxa ja existeix i no ha de ser gestionada per ell

```
### telegraf

Fitxer configuració:

```
# /opt/docker/telegraf/config/telegraf.conf

[global_tags]
  # Pots afegir tags globals a totes les mètriques, per exemple, el nom del host
  host = "$HOSTNAME" # Telegraf agafarà el hostname del contenidor, que pot ser útil
  # Alternativament, si vols el nom del host real, pots fer-ho així (requereix env var)
  # host = "${HOST_REAL_HOSTNAME}" 

[agent]
  interval = "10s"
  round_interval = true
  metric_batch_size = 1000
  metric_buffer_limit = 10000
  collection_jitter = "0s"
  flush_interval = "10s"
  flush_jitter = "0s"
  precision = ""
  hostname = "" ## Si deixes buit, utilitza el hostname del contenidor.
                  ## Pots posar-hi "${HOST_REAL_HOSTNAME}" si passes la variable d'entorn.
  omit_hostname = false

###############################################################################
#                            OUTPUT PLUGINS                                   #
###############################################################################

[[outputs.influxdb_v2]]
  urls = ["http://influxdb:8086"] # Adreça d'InfluxDB a la mateixa xarxa de Docker Compose
  token = "dshdifuhb9733011237ewfdifnfldksaodhwieugfas" # IMPORTANT: Usa el mateix token que vas definir per a InfluxDB
  organization = "Itic"
  #bucket = "bucket1"
  ## Descomenta la línia següent per enviar totes les mètriques a un bucket específic de Telegraf
  bucket = "telegraf" 
  timeout = "5s"

###############################################################################
#                            INPUT PLUGINS                                    #
###############################################################################

# Mètriques de CPU del host
[[inputs.cpu]]
  percpu = true
  totalcpu = true
  collect_cpu_time = false
  report_active = false
  ## IMPORTANT: Per a monitoritzar el host des d'un contenidor,
  ## calen aquestes variables d'entorn al contenidor de Telegraf
  ## HOST_PROC=/hostfs/proc i HOST_SYS=/hostfs/sys
  
# Mètriques de memòria del host
[[inputs.mem]]
  ## HOST_PROC=/hostfs/proc

# Mètriques de la càrrega del sistema
[[inputs.system]]
  ## HOST_PROC=/hostfs/proc
  ## HOST_SYS=/hostfs/sys

# Mètriques d'ús del disc del host
[[inputs.disk]]
  ignore_fs = ["tmpfs", "devtmpfs", "devfs", "overlay", "aufs", "squashfs"]
  mount_points = ["/hostfs"] # Telegraf buscarà els punts de muntatge a /hostfs dins del contenidor
  ## HOST_PROC=/hostfs/proc
  ## HOST_SYS=/hostfs/sys

# Mètriques d'I/O del disc del host
[[inputs.diskio]]
  ## HOST_PROC=/hostfs/proc
  ## HOST_SYS=/hostfs/sys

# Mètriques de xarxa del host
[[inputs.net]]
  interfaces = ["eth0", "lo"] # O les interfícies que vulguis monitoritzar
  ## HOST_PROC=/hostfs/proc
  ## HOST_SYS=/hostfs/sys

# Mètriques del procés de Docker (si vols monitoritzar el propi daemon de Docker)
# Necessita accés al socket de Docker
# Read metrics about docker containers
[[inputs.docker]]
  ## Docker Endpoint
  ##   To use TCP, set endpoint = "tcp://[ip]:[port]"
  ##   To use environment variables (ie, docker-machine), set endpoint = "ENV"
  endpoint = "unix:///var/run/docker.sock"

  ## Set to true to collect Swarm metrics(desired_replicas, running_replicas)
  ## Note: configure this in one of the manager nodes in a Swarm cluster.
  ## configuring in multiple Swarm managers results in duplication of metrics.
  gather_services = false

  ## Only collect metrics for these containers. Values will be appended to
  ## container_name_include.
  ## Deprecated (1.4.0), use container_name_include
  container_names = []

  ## Set the source tag for the metrics to the container ID hostname, eg first 12 chars
  source_tag = false

  ## Containers to include and exclude. Collect all if empty. Globs accepted.
  container_name_include = []
  container_name_exclude = []

  ## Container states to include and exclude. Globs accepted.
  ## When empty only containers in the "running" state will be captured.
  ## example: container_state_include = ["created", "restarting", "running", "removing", "paused", "exited", "dead"]
  ## example: container_state_exclude = ["created", "restarting", "running", "removing", "paused", "exited", "dead"]
  # container_state_include = []
  # container_state_exclude = []

  ## Objects to include for disk usage query
  ## Allowed values are "container", "image", "volume" 
  ## When empty disk usage is excluded
  storage_objects = []

  ## Timeout for docker list, info, and stats commands
  timeout = "5s"

  ## Specifies for which classes a per-device metric should be issued
  ## Possible values are 'cpu' (cpu0, cpu1, ...), 'blkio' (8:0, 8:1, ...) and 'network' (eth0, eth1, ...)
  ## Please note that this setting has no effect if 'perdevice' is set to 'true'
  # perdevice_include = ["cpu"]

  ## Specifies for which classes a total metric should be issued. Total is an aggregated of the 'perdevice' values.
  ## Possible values are 'cpu', 'blkio' and 'network'
  ## Total 'cpu' is reported directly by Docker daemon, and 'network' and 'blkio' totals are aggregated by this plugin.
  ## Please note that this setting has no effect if 'total' is set to 'false'
  # total_include = ["cpu", "blkio", "network"]

  ## docker labels to include and exclude as tags.  Globs accepted.
  ## Note that an empty array for both will include all labels as tags
  docker_label_include = []
  docker_label_exclude = []

  ## Which environment variables should we use as a tag
  tag_env = ["JAVA_HOME", "HEAP_SIZE"]

  ## Optional TLS Config
  # tls_ca = "/etc/telegraf/ca.pem"
  # tls_cert = "/etc/telegraf/cert.pem"
  # tls_key = "/etc/telegraf/key.pem"
  ## Use TLS but skip chain & host verification
  # insecure_skip_verify = false
```

Fitxer docker-compose
```
# telegraf_stack/docker-compose.yml
version: '3.8'

services:
  telegraf:
    image: telegraf:1.34.4-alpine
    container_name: telegraf
    restart: unless-stopped
    volumes:
      # Muntar el fitxer de configuració de Telegraf
      - ./config/telegraf.conf:/etc/telegraf/telegraf.conf:ro
      # Muntar les rutes del host que Telegraf necessita
      - /etc:/hostfs/etc:ro
      - /proc:/hostfs/proc:ro
      - /sys:/hostfs/sys:ro
      - /var/run/utmp:/var/run/utmp:ro
      # - /var:/hostfs/var:ro # Si necessites més mètriques
    environment:
      # Variables d'entorn per indicar a Telegraf on trobar els fitxers del host
      - HOST_ETC=/hostfs/etc
      - HOST_PROC=/hostfs/proc
      - HOST_SYS=/hostfs/sys
      - HOST_RUN=/hostfs/run
      - HOST_MOUNT_PREFIX=/hostfs
      - HOST_REAL_HOSTNAME=${HOSTNAME} # O el nom que vulguis per al host
    networks:
      - internal # Connecta Telegraf a la xarxa externa

networks:
  internal:
    name: xarxa_docker1 # El nom de la xarxa que ja has creat i on InfluxDB està connectat
    external: true # Indica a Docker Compose que aquesta xarxa ja existeix
```

## Instalacio OpenTelemetry collection_jitter

Arxiu configuració:

```
# collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc: # Puerto por defecto 4317 para gRPC
      http: # Puerto por defecto 4318 para HTTP

processors:
  batch:
    send_batch_size: 1000
    timeout: 1s
 
exporters:
  influxdb:
    endpoint: "http://influxdb:8086" # <-- ¡Importante! Si InfluxDB también está en Docker, usa el nombre del servicio
    org: "Itic"
    bucket: "telemetry"
    token: "dshdifuhb9733011237ewfdifnfldksaodhwieugfas"
    metrics_schema: "telegraf-prometheus-v2"

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [influxdb]
    # Si vas a usar trazas, necesitarás configurar un exportador como Jaeger o Tempo aquí:
    # traces:
    #   receivers: [otlp]
    #   processors: [batch]
    #   exporters: [jaeger] # o [tempo]
    # logs:
    #   receivers: [otlp]
    #   processors: [batch]
    #   exporters: [loki] # o similar
```    

Docker compose 

```
version: '3.8'

services:
  otel:
    image: otel/opentelemetry-collector-contrib:0.128.0
    container_name: otel
    command: ["--config=/etc/otelcol/config.yaml"]
    volumes:
      - ./config/collector-config.yaml:/etc/otelcol/config.yaml # Monta tu archivo de configuración
    ports:
      - "4317:4317" # Puerto gRPC para OTLP
      - "4318:4318" # Puerto HTTP para OTLP
      - "8888:8888" # Puerto para el endpoint de estado/healthcheck del Collector (opcional)
  
```