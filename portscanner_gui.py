import threading
from tkinter import ttk 
import tkinter as tk 
import socket
import csv

common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 143, 443, 993, 995, 3306, 3389, 5900, 8080]




def scan_port(ip, port, results, timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)  # Use the user-defined timeout
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
root.title("ABCX Scanner")
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

timeout_label = tk.Label(root, text="Defina o timeout (segundos):")
timeout_label.pack(padx=10, pady=5)

timeout_slider = tk.Scale(root, from_=0.5, to=5, resolution=0.5, orient=tk.HORIZONTAL)
timeout_slider.set(1)  # Default timeout of 1 second
timeout_slider.pack(padx=10, pady=5)

common_ports_var = tk.BooleanVar()
common_ports_check = tk.Checkbutton(root, text="Scan Common Ports", variable=common_ports_var)
common_ports_check.pack(padx=10, pady=5)

progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(padx=10, pady=5)

results_text = tk.Text(root, height=10, width=40)
results_text.pack(padx=10, pady=10)


def threaded_scan():
    ip = ip_entry.get()
    start_port = int(start_port_entry.get())
    end_port = int(end_port_entry.get())
    timeout = float(timeout_entry.get())
    results = []
    total_ports = end_port - start_port + 1

    progress["value"] = 0
    progress["maximum"] = total_ports
    results_text.delete(1.0, tk.END)

    for count, port in enumerate(range(start_port, end_port + 1), start=1):
        scan_port(ip, port, results, timeout)  # Perform the scan
        progress["value"] = count     # Update progress bar value
        progress.update()            # Refresh the progress bar
        root.update_idletasks()      # Keep GUI responsive

    save_results_to_csv(ip, start_port, end_port, results)
    for result in results:
        results_text.insert(tk.END, f"Port {result[0]}: {result[1]} - {result[2]}\n")

   
   
   

def start_scan():
        threading.Thread(target=threaded_scan).start()

   

def toggle_dark_mode():
    bg_color = "#2e2e2e" if dark_mode_var.get() else "#f0f0f0"
    fg_color = "white" if dark_mode_var.get() else "black"
    root.config(bg=bg_color)
    for widget in root.winfo_children():
        widget.config(bg=bg_color, fg=fg_color)

dark_mode_var = tk.BooleanVar()
dark_mode_check = tk.Checkbutton(root, text="Dark Mode", variable=dark_mode_var, command=toggle_dark_mode)
dark_mode_check.pack(padx=10, pady=5)


# Adição do botão para iniciar o escaneamento
scan_button = tk.Button(root, text="Iniciar Escaneamento", command=start_scan)
scan_button.pack(padx=10, pady=10)

timeout_label = tk.Label(root, text="Defina o timeout (segundos):")
timeout_label.pack(padx=10, pady=5)

timeout_entry = tk.Entry(root)
timeout_entry.insert(0, "1.0")  # Default timeout value
timeout_entry.pack(padx=10, pady=5)

root.mainloop()
