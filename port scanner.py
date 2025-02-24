import socket

# Lista de portas comuns
common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5900, 8080]

ip  = input("what is the target ip addr: ")
start_port = int(input("enter the start port: "))
end_port = int(input("enter end port:  "))


def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:

                banner = sock.recv(1024).decode().strip()
                print(f"Porta {port} aberta: {banner}")
                # Verificação de serviço simples com base no banner
                if "HTTP" in banner:
                    print(f"Serviço HTTP identificado na porta {port}")
                elif "SSH" in banner:
                    print(f"Serviço SSH identificado na porta {port}")
                elif "FTP" in banner:
                    print(f"Serviço FTP identificado na porta {port}")
            except socket.error:
                print(f"Porta {port} aberta, mas não foi possível ler o banner")    
            print(f"Port {port} is OPEN")
        else:
            print(f"Port {port} is CLOSED")
    except socket.gaierror:
        print(f"Network address error occurred while trying to connect to {ip}:{port}")
    except Exception as e:
        print(f"Error occurred while trying to connect to {ip}:{port}: {str(e)}")
    finally:
        sock.close()

for port in range(start_port, end_port + 1):
    scan_port(ip, port)

