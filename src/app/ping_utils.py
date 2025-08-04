from ping3 import ping

def check_device(ip):
    """
    Intenta hacer ping a una IP.
    Retorna True si responde, False si falla o hay excepción.
    """
    try:
        response = ping(ip, timeout=2)  # Podés ajustar timeout si querés
        return response is not None
    except Exception as e:
        # Podés loguear el error si querés más trazabilidad
        return False