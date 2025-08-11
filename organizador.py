#bem-vindo ao meu organizador automático de downloads!
#
#o que faz:
#1. ao iniciar, faz uma limpeza completa na pasta de Downloads com barra de progresso.
#2. continua rodando para monitorar a pasta e organizar novos arquivos assim que aparecem.
#3. exibe logs coloridos para cada ação.



from pathlib import Path
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tqdm import tqdm
from colorama import Fore, Style, init
import time

init(autoreset=True)

PASTA_DOWNLOADS = Path.home() / "Downloads"

MAPA_PASTAS = {
    ".pdf": "PDFs",
    ".docx": "Documentos",
    ".doc": "Documentos",
    ".xls": "Excels",
    ".xlsx": "Excels",
    ".zip": "Arquivos Compactados",
    ".rar": "Arquivos Compactados",
    ".jpg": "Imagem",
    ".png": "Imagem",
    ".jpeg": "Imagem",
    ".gif": "Imagem",
    ".msi": "Instaladores",
    ".exe": "Instaladores",
    ".wav": "Audio",
    ".mp3": "Audio",
    ".mp4": "Video",
    ".avi": "Video",
}

def mover_arquivo(arquivo: Path):
    if not arquivo.is_file():
        return

    extensao = arquivo.suffix.lower()
    if extensao in MAPA_PASTAS:
        try:
            pasta_destino = PASTA_DOWNLOADS / MAPA_PASTAS[extensao]
            pasta_destino.mkdir(exist_ok=True)
            shutil.move(str(arquivo), str(pasta_destino))
            nome_arquivo = Style.BRIGHT + arquivo.name + Style.NORMAL
            nome_pasta = Fore.MAGENTA + MAPA_PASTAS[extensao]
            print(f"{Fore.CYAN}[SUCESSO] {nome_arquivo} movido para a pasta {nome_pasta}")
        except Exception as e:
            print(f"{Fore.RED}[ERRO] Não foi possível mover {arquivo.name}: {e}")

def limpar_pasta_inicial():
    print(f"{Fore.YELLOW}--- Iniciando limpeza completa da pasta Downloads ---")
    arquivos_para_mover = [
        f for f in PASTA_DOWNLOADS.iterdir()
        if f.is_file() and f.suffix.lower() in MAPA_PASTAS
    ]

    if not arquivos_para_mover:
        print(f"{Fore.GREEN}Nenhum arquivo para organizar no momento. A pasta já está limpa!")
        return

    for arquivo in tqdm(arquivos_para_mover, desc="Organizando arquivos para mover", unit="arquivo"):
        mover_arquivo(arquivo)
        time.sleep(0.1)

    print(f"{Fore.YELLOW}--- Limpeza Concluída ---")

class MeuOrganizador(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            arquivo_novo = Path(event.src_path)
            time.sleep(1)
            mover_arquivo(arquivo_novo)

if __name__ == "__main__":
    limpar_pasta_inicial()

    event_handler = MeuOrganizador()
    observer = Observer()
    observer.schedule(event_handler, PASTA_DOWNLOADS, recursive=True)
    observer.start()

    print(f"\n{Fore.MAGENTA}==============")
    print(f"{Fore.MAGENTA}! {Style.BRIGHT}Organizador iniciado!{Style.NORMAL}")
    print(f"{Fore.MAGENTA}Estou monitorando sua pasta de Downloads em tempo real.")
    print(f"{Fore.MAGENTA}Pressione {Style.BRIGHT}Ctrl+C{Style.NORMAL} para parar o programa.")
    print(f"{Fore.MAGENTA}================\n")

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}--- O organizador está sendo encerrado... ---")
        observer.stop()
        observer.join()
        print(f"{Fore.YELLOW}--- Organizador encerrado. Até a próxima! ---")
