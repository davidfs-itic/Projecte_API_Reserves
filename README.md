# ProjecteReserves-API

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
│   ├── Dockerfile         # Dockerfile per al servei FastAPI amb HTTPS
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
Cal tenir alguna base de dades preparada, en local o en remot.
```
//Si estem en la carpeta del projecte
uvicorn API.main:app --host 0.0.0.0 --reload --port 8443 --ssl-keyfile ./API/ssl/key.pem --ssl-certfile ./API/ssl/cert.pem
uvicorn main:app --host 0.0.0.0 --reload --port 8443 --ssl-keyfile ./ssl/key.pem --ssl-certfile ./ssl/cert.pem
```

## Creació bbdd
### Connexio a la base de dades 
```
mysql -u root -p -h 127.0.0.1 
```

### Script creació (demanar a la IA)
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


# Instal·lació docker (si utilitzem un ubuntu sense configurar)
Seguir instruccions a :
https://docs.docker.com/engine/install/ubuntu/


## Desinstalar altres versions:
```
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

## Instal·lar apk

1-Set up Docker's apt repository.
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

2-Install the Docker packages.
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## Crear contenidor per base de dades:

Client de mysql.

apt install -y mariadb-client-core

Preparar carpeta per base de dades:
mkdir -p /opt/docker/mariadb/datadir 




# Creació de contenidors.
El contenidor amb un servidor de bbdd ja està inclos en la imatge, però si voleu personalitzar, o afegir-ne més:

## Creació Network per als contenidors
```
docker network create -d bridge internal
```

## Creació contenidor amb mariadb
```
mkdir -p /opt/docker/mariadb/datadir
docker create -p 3306:3306 --restart=unless-stopped --network=internal -v /opt/docker/mariadb/datadir:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=P@ssw0rd --name mariadb  mariadb:11.4 
```

## Pujar fonts al servidor:
scp -i ~/.ssh/vockey.pem  ./docker* ubuntu@daviditic.mooo.com:/opt/docker/reserves
scp -i ~/.ssh/vockey.pem  ./API/*.py ./API/*.txt ubuntu@daviditic.mooo.com:/opt/docker/reserves/API
scp -i ~/.ssh/vockey.pem  ./API/ssl/* ubuntu@daviditic.mooo.com:/opt/docker/reserves/API/ssl

scp ./docker* root@10.2.192.183:/opt/docker/reserves
scp ./API/*.py ./API/*.txt root@10.2.192.183:/opt/docker/reserves/API
scp ./API/ssl/* root@10.2.192.183:/opt/docker/reserves/API/ssl



## Creació contenidor amb Fastapi
cd /opt/docker/reserves
docker-compose up -d --build

## Eliminar i tornar a crear el contenidor amb noves fonts
docker-compose down
docker-compose up -d --build

## Provar que funciona 
https://ipserver:8443/docs

# Altres contenidors:

## Node Red
mkdir -p /opt/docker/nodered/node1
chown -R 1000:1000 /opt/docker/nodered/

docker container create -p 1880:1880 -v /opt/docker/nodered/node1/:/data --restart=unless-stopped --network=internal --name node1 nodered/node-red:4.0.2-22
docker start node1
docker container list -a

