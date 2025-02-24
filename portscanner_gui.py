import tkinter as tk 
import socket
import csv

common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 143, 443, 993, 995, 3306, 3389, 5900, 8080]

def scan_port(ip, port, results):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:
                banner = sock.recv(1024).decode().strip()
                service = None
                if "HTTP" in banner:
                    service = "HTTP"
                elif "SSH" in banner:
                    service = "SSH"
                elif "FTP" in banner:
                    service = "FTP"
                results.append([port, "OPEN", banner, service])
                print(f"Porta {port} aberta: {banner}")
            except socket.error:
                results.append([port, "OPEN", "N/A", "N/A"])
                print(f"Porta {port} aberta, mas não foi possível ler o banner")
        else:
            results.append([port, "CLOSED", "N/A", "N/A"])
            print(f"Porta {port} fechada")
    except socket.gaierror:
        print(f"Network address error occurred while trying to connect to {ip}:{port}")
    except Exception as e:
        print(f"Error occurred while trying to connect to {ip}:{port}: {str(e)}")
    finally:
        sock.close()





def save_results_to_csv(ip, start_port, end_port, results):
    filename = f"scan_results_{ip}_{start_port}_{end_port}.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Port", "Status", "Banner", "Service"])
        writer.writerows(results)
    print(f"Resultados salvos no arquivo {filename}")

root = tk.Tk()
root.title("Port Scanner melhor que Nmap")
root.geometry("400x300")


ip_label = tk.Label(root, text="Digite o endereço IP:")
ip_label.pack(padx=10, pady=10)
ip_entry = tk.Entry(root)
ip_entry.pack(padx=10, pady=5)

# Criação dos campos de entrada para as portas
start_port_label = tk.Label(root, text="Digite a porta inicial:")
start_port_label.pack(padx=10, pady=5)
start_port_entry = tk.Entry(root)
start_port_entry.pack(padx=10, pady=5)


end_port_label = tk.Label(root, text="Digite a porta final:")
end_port_label.pack(padx=10, pady=5)
end_port_entry = tk.Entry(root)
end_port_entry.pack(padx=10, pady=5)

results_text = tk.Text(root, height=10, width=40)
results_text.pack(padx=10, pady=10)

def start_scan():
    print("Botão Iniciar Escaneamento clicado")  # Mensagem de depuração
    ip = ip_entry.get()
    start_port = int(start_port_entry.get())
    end_port = int(end_port_entry.get())
    results = []
    for port in range(start_port, end_port + 1):
        scan_port(ip, port, results)
    save_results_to_csv(ip, start_port, end_port, results)
    results_text.delete(1.0, tk.END)
    for result in results:
        results_text.insert(tk.END, f"Port {result[0]}: {result[1]} - {result[2]}\n")

# Adição do botão para iniciar o escaneamento
scan_button = tk.Button(root, text="Iniciar Escaneamento", command=start_scan)
scan_button.pack(padx=10, pady=10)



root.mainloop()