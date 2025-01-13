import os
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time

ascii_art = r"""

              .-.
        .-'``(|||)
     ,`\ \    `-`.               88                         88
    /   \ '``-.   `              88                         88
  .-.  ,       `___:    88   88  88,888,  88   88  ,88888, 88888  88   88
 (:::) :        ___     88   88  88   88  88   88  88   88  88    88   88
  `-`  `       ,   :    88   88  88   88  88   88  88   88  88    88   88
    \   / ,..-`   ,     88   88  88   88  88   88  88   88  88    88   88
     `./ /    .-.`      '88888'  '88888'  '88888'  88   88  '8888 '88888'
 LGB    `-..-(   )
              `-`

------------------------------------------------
This ASCII pic can be found at
https://asciiart.website/index.php?art=logos%20and%20insignias/linux
"""

base_url = 'https://releases.ubuntu.com/'

def fetch_versions(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        versions = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.endswith('/') and href[:-1].replace('.', '').isdigit():  
                versions.append(href.strip('/'))
        return versions
    else:
        print("Erro ao acessar a página.")
        return []

def download_iso(version, progress_bar, download_button, download_window, cancel_button, complete_button, speed_label):
    url = f"{base_url}{version}/ubuntu-{version}-desktop-amd64.iso"
    file_name = url.split('/')[-1]
    
    cancel_download = False

    def cancel_download_function():
        nonlocal cancel_download
        cancel_download = True
        download_window.destroy()
        messagebox.showinfo("Cancelado", "Download cancelado e arquivo removido.")
        if os.path.exists(file_name):
            os.remove(file_name)
        download_button.config(state=tk.NORMAL)

    cancel_button.config(command=cancel_download_function)

    response = requests.head(url)
    total_size = int(response.headers.get('content-length', 0))

    start_time = time.time()
    bytes_downloaded = 0

    try:
        with requests.get(url, stream=True) as response, open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if cancel_download:
                    return
                file.write(chunk)
                bytes_downloaded += len(chunk)
                progress_bar['value'] += (len(chunk) / total_size) * 100
                progress_bar.update()

                elapsed_time = time.time() - start_time
                speed = bytes_downloaded / elapsed_time  
                speed_in_kb = speed / 1024  

                if int(elapsed_time) % 1 == 0:
                    if download_window.winfo_exists():
                        speed_label.config(text=f"Velocidade: {speed_in_kb:.2f} KB/s")
                    else:
                        return  

        messagebox.showinfo("Sucesso", f"{file_name} baixado com sucesso!")
        complete_button.config(state=tk.NORMAL)
        cancel_button.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar o arquivo: {e}")
        cancel_button.config(state=tk.DISABLED)

def start_download(selected_version, progress_bar, download_button):
    download_button.config(state=tk.DISABLED)

    download_window = tk.Toplevel()
    download_window.title("Download")
    download_window.geometry("400x200")
    download_window.resizable(False, False)

    label_progress_title = tk.Label(download_window, text="Baixando ISO, aguarde!", font=("Helvetica", 12))
    label_progress_title.pack(pady=10)

    progress_bar = ttk.Progressbar(download_window, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=20)

    speed_label = tk.Label(download_window, text="Velocidade: 0.00 KB/s", font=("Helvetica", 10))
    speed_label.pack(pady=5)

    button_frame = tk.Frame(download_window)
    button_frame.pack(pady=10)

    cancel_button = tk.Button(button_frame, text="Cancelar", state=tk.NORMAL)
    cancel_button.pack(side=tk.LEFT, padx=5)

    complete_button = tk.Button(button_frame, text="Concluir", state=tk.DISABLED, command=download_window.destroy)
    complete_button.pack(side=tk.RIGHT, padx=5)

    download_iso(selected_version, progress_bar, download_button, download_window, cancel_button, complete_button, speed_label)

def create_gui():
    root = tk.Tk()
    root.title("Ubuntu Release Downloader GUI")
    
    root.geometry("500x600") 
    root.resizable(False, False) 
    
    label_ascii_art = tk.Label(root, text=ascii_art, font=("Courier", 8), justify="left")
    label_ascii_art.pack(pady=10)

    label_title = tk.Label(root, text="Ubuntu Releases GUI", font=("Helvetica", 16, "bold"))
    label_title.pack(pady=5)

    versions = fetch_versions(base_url)
    if versions:
        version_listbox = tk.Listbox(root, height=10, selectmode=tk.SINGLE, width=50)
        for version in versions:
            version_listbox.insert(tk.END, version)
        version_listbox.pack(pady=10)

        download_button = tk.Button(root, text="Iniciar Download", 
                                    command=lambda: start_download(version_listbox.get(tk.ACTIVE), None, download_button))
        download_button.pack(pady=5)
    
    else:
        label_no_versions = tk.Label(root, text="Nenhuma versão encontrada.")
        label_no_versions.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    create_gui()
