# ProjecteReserves-API

En aquest README, trobareu instruccions per instalar i fer el setup d'un projecte amb Fastapi (Reserves de material) i alguns subprojectes.


* Setup GIT 
  Com iniciar un projecte en github amb les fonts preexistents en local.
* Setup projecte Python:
  Creació de un virtual envirovment per instal·lar dependències
* Generació de codi amb IA
  Exemple de prompt per generar una api amb FastAPI
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