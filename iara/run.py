import multiprocessing
import time
import requests
import uvicorn
from model.model_login.model_login import iniciar_gui
from model.model_loading.model_loading import show_loading_screen

API_URL = "http://127.0.0.1:8000"

def run_api():
    print("\033[93m[API] Iniciando servidor Fa6stAPI...\033[0m")
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=False, log_level="info")

def verificar_api(max_tentativas=10, intervalo=1):
    for tentativa in range(max_tentativas):
        try:
            response = requests.get(f"{API_URL}/docs", timeout=2)
            if response.status_code == 200:
                print("\033[92m[API] Servidor FastAPI está online!\033[0m")
                return True
        except:
            pass
        print(f"[API] Tentativa {tentativa + 1}/{max_tentativas}: aguardando servidor subir...")
        time.sleep(intervalo)
    print("\033[91m[ERRO] API não respondeu após várias tentativas.\033[0m")
    return False


if __name__ == "__main__":

    print("\033[96m============================================\033[0m")
    print("\033[96m🚀 Iniciando sistema EcoScore (API + Interface)\033[0m")
    print("\033[96m============================================\033[0m")

    api_process = multiprocessing.Process(target=run_api, daemon=True)
    api_process.start()

    if verificar_api():
        print("\033[94m[GUI] Abrindo interface do EcoScore...\033[0m")
        show_loading_screen(iniciar_gui)
    else:
        print("\033[91m[ERRO] Não foi possível iniciar a interface — API fora do ar.\033[0m")
