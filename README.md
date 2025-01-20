# ProjecteReserves-API
python -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

## Instal·lar dependèincies
fastapi
uvicorn
mysql-connector-python


## Creació bbdd
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


## Estructura del projecte
```
project/
│
├── API/
│   ├── main.py            # Fitxer principal de FastAPI
│   ├── requirements.txt   # Dependències de Python
│   ├── Dockerfile         # Dockerfile per al servei FastAPI amb HTTPS
│   ├── ssl/
│   │   ├── cert.pem           # Certificat SSL
│   │   ├── key.pem            # Clau privada SSL
│   │
├── docker-compose.yml     # Fitxer Docker Compose
```


## Creacio certificats
```
openssl req -x509 -newkey rsa:4096 -keyout ./API/ssl/key.pem -out ./API/ssl/cert.pem -days 3650 -nodes
```


## Dockerfile:
```
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Assegurar que el certificat SSL estarà accessible
RUN mkdir -p /ssl
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "/ssl/key.pem", "--ssl-certfile", "/ssl/cert.pem"]

```
## Creació contenidor:

```
docker build -t fastapi-mariadb-app .
```


## Pujar fonts al servidor:
scp -i ~/.ssh/vockey.pem  ./docker* ubuntu@daviditic.mooo.com:/opt/docker/reserves
scp -i ~/.ssh/vockey.pem  ./API/*.py ./API/*.txt ubuntu@daviditic.mooo.com:/opt/docker/reserves/API
scp -i ~/.ssh/vockey.pem  ./API/ssl/* ubuntu@daviditic.mooo.com:/opt/docker/reserves/API/ssl

scp ./docker* root@10.2.192.183:/opt/docker/reserves
scp ./API/*.py ./API/*.txt root@10.2.192.183:/opt/docker/reserves/API
scp ./API/ssl/* root@10.2.192.183:/opt/docker/reserves/API/ssl

## Creació Network per als contenidors

docker network create -d bridge internal



uvicorn main:app" --host 0.0.0.0 -reload --port 8443 --ssl-keyfile ./ssl/key.pem --ssl-certfile ./ssl/cert.pem