import customtkinter as ctk
import pywinstyles as pwstyles
from PIL import Image
from model.config_model.config import LOGO_PATH


def show_loading_screen(next_function):
    loading_app = ctk.CTk()
    loading_app.title("EcoScore - Iniciando")
    loading_app.geometry("400x300")
    loading_app.resizable(False, False)
    loading_app.config(bg="#9ea696")
    loading_app.eval('tk::PlaceWindow . center')

    try:
        logo = ctk.CTkImage(
            light_image=Image.open(LOGO_PATH),
            dark_image=Image.open(LOGO_PATH),
            size=(110, 120)
        )
        logo_label = ctk.CTkLabel(loading_app, image=logo, text="", bg_color="#000001")
        logo_label.pack(pady=20)
        pwstyles.set_opacity(logo_label, 1, '#000001')
    except Exception as e:
        print(f"[AVISO] Não foi possível carregar o logo: {e}")

    label = ctk.CTkLabel(loading_app, text="Carregando... 0%", font=("Segoe UI", 18, "bold"), text_color="white", bg_color="#000001")
    label.pack(pady=10)

    progress = ctk.CTkProgressBar(loading_app, width=250, height=20, progress_color="#00b050", fg_color="#333", bg_color="#000001")
    progress.pack(pady=15)
    progress.set(0)

    def atualizar_barra(i=0):
        if i <= 100:
            progress.set(i / 100)
            label.configure(text=f"Carregando... {i}%")
            i += 1
            loading_app.after(20, atualizar_barra, i)
        else:
            loading_app.destroy()
            next_function()  

    pwstyles.set_opacity(label, 1, '#000001')
    pwstyles.set_opacity(progress, 1, '#000001')

    atualizar_barra()
    loading_app.mainloop()
