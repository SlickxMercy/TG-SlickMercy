# TG-SlickMercy
Cualquier sugerencia sugerencias o pregunta contactarme a mi telegram @SlickMercy
### Termux 
1. Descarga Termux desde F-Droid (es importante obtenerlo de esta app).

### Instalación 
Ejecuta los siguientes comandos en Termux en el orden indicado para evitar errores. Copia y pega uno por uno.

```bash
termux-setup-storage

pkg install python

pkg install python-pip

pkg install git

pkg update && pkg upgrade

pip install colorama

pip install aiohttp

pip install art

pip install pycryptodome

pip install requests

pip install httpx

cd storage/downloads

git clone https://github.com/SlickxMercy/TG-SlickMercy

cd TG-SlickMercy

python SlickMercy.py
```
### Ejecutar script
```bash
python SlickMercy
```

### Opciónes 
opción 1: Escáner 

Funciona para escanear un rango de ips y puertos, verifica si esta asociada a una camara Hikvision y guarda las ips en el archivo llamado host.txt
(El rango debe ser de inicio a fin por ejemplo: inicio: 190.101.0.0 fin: 190.101.255.255)

Opción 2: Desencriptar Cámaras 

Funciona para desencriptar las contraseñas de las cámaras y obtener snapshots 
(usa el archivo host.txt para escanear las ips en búsqueda de las cámaras vulnerables, guarda las snapshots en la carpeta VDB con nombre ip,user,pass)

Opcion 3: BruteForce Cam 

Funciona para escanear las IPS del archivo host.txt y realiza comprobaciónes de credenciales,al obtener acceso a una camara toma snapshots y las guarda en la carpeta pics con el nombre ip,user,pass
utiliza los archivos user.txt y pass.txt 

