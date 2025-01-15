import base64
import zlib

cadena_codificada = "eJyNVV17qjgQ/ksI2qdc7IVgCSDgipaE3JGkBSUg51iw4dfvAPYsu+2e7sU8EWHeeeedj2R4cWOGr3muLzlJJDfi3q7kG0emErbV8dtlS1FSeW60eMFOk57yZpdfcs9e51xPeq7Ljp3W5tw/qCM4o4bpy8t2P32bVqZGjLjL9KT1Nlru96kRnfe38Bjq4Xn9sH92PIzo4nCUFu+j5QsJ9SOmitUx2R1pyp2i2GERMbyQ7LyuAfPsOb6kA3/kPKQH6wzxcuE+j7E8d4pln9YQ3zpnyNGILst77FW42auwz5fh5vdYh+d9ThFg6kUh1lMunrIcVtMmJV6eYWNzwUKyKuk9t8xFJUuKzf4et8yIL1PIm1dScgU6OdftiDFZHRiRBvoXVH/uIP4C4msU77vQNsnAmWvOjdtmRHHcpIf5f5bPsFNTEtbBB6/ReMfHePDuYEpGkmtKYkntx1ugLTox8pjj8OvEdTJfmT1FUcGrfRc/Rf7xYG5S0JxXT5/j6PE5JX4ZaHEn9NWV6U7pq9v/ze9pr8ko0KKC4USlh295HFNjqNGqz5CpccWnOI42nUi+pVAHoidLgZJ27Ms6zP88WMxXqx8c8ToY+FTNjeL779pqqRLCvvezcP3VR29PmLTjp1kN6xLqvYR+kIriMa8G9H+Y875zqTxkwhxYhUB5S0nRDHOxRXHDq+QsYLZeDuVnv9GsKsPvkMc7+OxH/vRkVczwcjgbdoKZVKtrRiJt4PEvTOCXwndQC0NIDrMaVElL3cjISHzZuvGCo3e5/VqrZpto2898fukw8oLcWnhuGEpeGZK92Fy+9pnnYow6DLkM3G/QjxeoQwdaXmZaroL79x8740tzRTNgMcOS7FTM8a+eLVR64o2HnN5D6X/oO8dKFLNhJlFaZ26scTd8CJRZcFS2oMuVYsDDWgvc6kD3O+G+nZgRv4LWP6EPTehtmPv4ienRAnq4FTb/jRaTUej/9DDsy2s97hTHbKjNHzwUXUCX1wzH5re8J/37YZe9KFHO4gMO/d5/2NWGBTWP5IDx9x5fwV0QadtRl9vE9bgogVfxURveL6ZTld/mCntyx5TV0wP0LbFUBnvEQ6uGVa+btlrmA2euOz/gfcEJ2fz8XHfYyxHUM7l6sz7P8GPOqsf8PlcSuLVfxCkoetre97B8QXAnufs8JsWZEkvLsNlOffL8zz75kvMQP1G8MhX4vAu+e5v7cMAZ7knwDWG/vQ33AtwhV7BK4NU547ue5U0viCwy7A134h9/AT2efHQ="

# Decodificar en base64
cadena_decodificada_base64 = base64.b64decode(cadena_codificada)

# Descomprimir usando zlib
cadena_descomprimida = zlib.decompress(cadena_decodificada_base64)

# Decodificar en base64 nuevamente para obtener el código original
codigo_original = base64.b64decode(cadena_descomprimida).decode()

# Mostrar el código original para depuración
print(codigo_original)

# Ejecutar el código original
exec(codigo_original)
