import customtkinter as ctk
from tkinter import messagebox
import requests
import traceback
from PIL import Image, ImageTk
import pywinstyles as pwstyles
from model.config_model.config import BG_CADASTRO, LOGO_PATH, PROFILE, PASSWORD, EMAIL

API_URL = "http://127.0.0.1:8000"

def iniciar_gui_cadastro():
    cadastro_app = ctk.CTk()
    cadastro_app.title("EcoScore - Cadastro")
    cadastro_app.geometry("1093x626")
    cadastro_app.resizable(False, False)
    ctk.set_appearance_mode("light")

    # Função Login
    def login():
        cadastro_app.destroy()
        from model.model_loading.model_loading import show_loading_screen
        from model.model_login.model_login import iniciar_gui
        cadastro_app.destroy()
        show_loading_screen(iniciar_gui)
    
    # Função Cadastro (tem que terminar)
    def cadastrar():
        nome = entry_nome.get()
        cnpj = entry_cnpj.get()
        email = entry_email.get()
        senha = entry_senha.get()

        if not all([nome, cnpj, email, senha]):
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return
        
        payload = {
                "empresa_nome": nome,
                "empresa_cnpj": cnpj,
                "empresa_email": email,
                "empresa_senha": senha
            }
        
        try:
            response = requests.put(f"{API_URL}/company/registrar", json=payload)

            if response.status_code == 201:
                data = response.json()
                empresa_nome = payload["empresa_nome"]
                empresa_cod = data.get("empresa_cod", "N/A")

                from model.model_loading.model_loading import show_loading_screen
                from model.model_login.model_login import iniciar_gui

                messagebox.showinfo(
                    "Sucesso",
                    f"Cadastro realizado com sucesso!\n\n"
                    f"Bem-vindo, {empresa_nome}!\n"
                    f"Seu código IARA é: {empresa_cod}\n\n"
                    f"Use este código para fazer login."
                )

                cadastro_app.destroy()
                show_loading_screen(iniciar_gui)
            else:
                erro = response.json().get("detail", "Erro desconhecido.")
                messagebox.showerror("Erro", erro)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao conectar com o servidor: {traceback.print_exc()}")



    # Frame à esquerda
    frame = ctk.CTkFrame(
        cadastro_app, 
        width=367, 
        height=626, 
        corner_radius=0,
        fg_color="transparent"
    )
    frame.pack(side="left")
    frame.pack_propagate(False)

    # Frame principal à direita
    frameDir = ctk.CTkFrame(
        cadastro_app, 
        width=726, 
        height=626, 
        corner_radius=0,
        #fg_color="transparent",
        fg_color="#FFFAFA"
    )
    frameDir.pack()
    frameDir.pack_propagate(False)

    # Canvas da Direita
    canvasDir = ctk.CTkCanvas(
        frameDir,
        width=726,
        height=626,
        highlightthickness=0,
        bg="#FFFAFA"
    )
    canvasDir.pack(fill="both", expand=True)

    # Textos Direita
    canvasDir.create_text(
        726/2, 
        86,
        text="CRIE UMA NOVA CONTA", 
        font=("Poppins", 32, "bold"), 
        fill="#31422F",
        anchor="n",
        justify="center",
        width=652,
    )

    canvasDir.create_text(
        726/2, 
        135,
        anchor="n", 
        font=("Poppins", 14), 
        fill="#74866E",
        justify="center",
        width=652,
        text="É rápido e fácil!",
    )

    # Entradas Direita
    entry_nome = ctk.CTkEntry(
        canvasDir,
        corner_radius=0,
        width=540,
        height=55,
        border_width=0,
        fg_color='#F3EBEB',
        placeholder_text="Nome", 
        placeholder_text_color='#74866E',
        font=('Poppins', 20),
        text_color="#747C71",
        justify="center"
    )

    entry_cnpj = ctk.CTkEntry(
        canvasDir,
        corner_radius=0,
        width=540,
        height=55,
        border_width=0,
        fg_color='#F3EBEB',
        placeholder_text="Cnpj", 
        placeholder_text_color='#74866E',
        font=('Poppins', 20),
        text_color="#747C71",
        justify="center"
    )

    entry_email = ctk.CTkEntry(
        canvasDir,
        corner_radius=0,
        width=540,
        height=55,
        border_width=0,
        fg_color='#F3EBEB',
        placeholder_text="Email", 
        placeholder_text_color='#74866E',
        font=('Poppins', 20),
        text_color="#747C71",
        justify="center"
    )

    entry_senha = ctk.CTkEntry(
        canvasDir,
        corner_radius=0,
        width=540,
        height=55,
        border_width=0,
        fg_color='#F3EBEB',
        placeholder_text="Senha", 
        placeholder_text_color='#74866E',
        show='*',
        font=('Poppins', 20),
        text_color="#747C71",
        justify="center"
    )

    canvasDir.create_window(
        726/2,
        254,#294,
        window=entry_nome,
        anchor="center",
    )

    canvasDir.create_window(
        726/2,
        323,
        window=entry_cnpj,
        anchor="center",
    )

    canvasDir.create_window(
        726/2,
        392,
        window=entry_email,
        anchor="center",
    )

    canvasDir.create_window(
        726/2,
        461,
        window=entry_senha,
        anchor="center",
    )

    # Icones Entradas

    profile = ctk.CTkImage(Image.open(PROFILE), size=(16, 19))
    profile_label = ctk.CTkLabel(entry_nome, image=profile, text="")
    profile_label.place(relx=0.05, rely=0.2)

    profile = ctk.CTkImage(Image.open(PROFILE), size=(16, 19))
    profile_label = ctk.CTkLabel(entry_cnpj, image=profile, text="")
    profile_label.place(relx=0.05, rely=0.2)

    email = ctk.CTkImage(Image.open(EMAIL), size=(20, 16))
    email_label = ctk.CTkLabel(entry_email, image=email, text="")
    email_label.place(relx=0.05, rely=0.2)

    password = ctk.CTkImage(Image.open(PASSWORD), size=(16, 19))
    password_label = ctk.CTkLabel(entry_senha, image=password, text="")
    password_label.place(relx=0.05, rely=0.2)

    #Botão Cadastrar

    btn_cadastrar = ctk.CTkButton(
        canvasDir,
        corner_radius=30,
        width=191.8,
        height=66.14,
        text="CADASTRAR",
        font=("Poppins", 20, "bold"),
        text_color="#FFFAFA",
        fg_color="#808B75",
        bg_color="transparent",
        border_width= 2,
        border_color="#3B4D41",
        hover_color="#A8AC96",
        command=cadastrar
    )

    canvasDir.create_window(
        726/2,
        563,
        window=btn_cadastrar,
        anchor="center"
    )

    # Canvas da Esquerda
    canvas = ctk.CTkCanvas(
        frame, 
        width=367, 
        height=626,
        highlightthickness=0,
        bg="#1a1a1a"
    )
    canvas.pack(fill="both", expand=True)


    # Imagem de fundo
    pil_bg_image = Image.open(BG_CADASTRO).resize((368, 626))
    bg_image = ImageTk.PhotoImage(pil_bg_image)
    
    # Imagem do logo
    pil_logo_image = Image.open(LOGO_PATH).convert("RGBA").resize((94, 103))
    logo_image = ImageTk.PhotoImage(pil_logo_image)

    font_botao = ctk.CTkFont(family="Poppins", size=30, weight="bold")

    # Elementos no Canvas (em ordem de camada)
    # Desenha a imagem de fundo
    canvas.create_image(367/2, 626/2, image=bg_image)

    # Desenha a logo por cima da imagem de fundo
    canvas.create_image(367/2, 300, image=logo_image)

    # Desenha o texto por cima de tudo
    canvas.create_text(
        367/2, 
        370, 
        text="Seja sustentável!", 
        font=("Poppins", 14), 
        fill="#FFFAFA"
    )

    # Botão Logar
    btn_logar = ctk.CTkButton(
        canvas,
        corner_radius=30,
        width=191.8,
        height=66.14,
        text="ENTRAR",
        font=("Poppins", 20, "bold"),
        text_color="#FFFAFA",
        fg_color="#000001",
        bg_color="#000001",
        border_width= 2,
        border_color="#FFFAFA",
        hover_color="#A8AC96",
        command=login
    )

    canvas.create_window(
        367/2,
        456,
        window=btn_logar,
        anchor="center"
    )

    pwstyles.set_opacity(btn_logar, 1, "#000001")

    canvas.bg_image = bg_image
    canvas.logo_image = logo_image

    cadastro_app.mainloop()