import socket

# Cria um socket temporário para capturar o IP local
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Conecta a um servidor DNS externo
        ip_address = s.getsockname()[0]  # Obtém o IP local
        s.close()
        return ip_address
    except Exception as e:
        return f"Erro ao obter IP: {e}"
