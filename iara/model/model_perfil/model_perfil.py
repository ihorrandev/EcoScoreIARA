from session import current_user
import datetime
import locale
import customtkinter as ctk
import requests
from PIL import Image, ImageTk
from model.config_model.config import HOME_ICON, NOTIFY_ICON, GRAPH_ICON
from model.model_loading.model_loading import show_loading_screen
from model.model_inicio.model_inicio import iniciar_gui_inicio

API_URL = "http://127.0.0.1:8000"

def iniciar_gui_perfil():
    perfil_app = ctk.CTk()
    perfil_app.title("EcoScore - Perfil")
    perfil_app.geometry("1093x626")
    perfil_app.resizable(False, False)
    perfil_app.config(bg="#FFFAFA")

    def preencher_dados():
        response = requests.get(
            f"{API_URL}/company/{current_user.cod_empresa}",
        )
        if response.status_code == 200:
            data = response.json()
            empresa = data[0]
            print(empresa)
            nome_empresa.configure(text=empresa["empresa_nome"])
            cod_empresa.configure(text=f"CÓDIGO DE LOGIN DA EMPRESA: {empresa['cod_empresa']}")
            cnpj_empresa.configure(text=f"CNPJ: {empresa['empresa_cnpj']}")
            email_empresa.configure(text=f"E-MAIL: {empresa['empresa_email']}")
            senha_empresa.configure(text=f"SENHA: {empresa['empresa_senha']}")
            
        response_score = requests.get(
            f"{API_URL}/company/score/{current_user.cod_empresa}",
        )

        if response_score.status_code == 200:
            data_score = response_score.json()

            pontuacao_diaria.configure(text=f"Pontuação Diária: {data_score['score_total']}")

            mensal_pontuacao.configure(text=f"Pontuação Total do Mês: {data_score['score_mensal']}")
            avaliacao.configure(text=f"Avaliação EcoScore da Empresa: {data_score['status_texto']}")
            #perguntas_respondidas.configure(text=str(empresa_score['score_total']))
        
        try:
            locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        except locale.Error:
            try:
                locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
            except locale.Error:
                print("Aviso: Locale para português não encontrado. O mês será exibido em inglês.")

        data_agora = datetime.datetime.now()

        data_formatada = data_agora.strftime('%B, %Y')

        #data_formatada = data_objeto.strftime('%B, %d')

        print(data_formatada)

    def ir_inicio():
        perfil_app.destroy()
        show_loading_screen(iniciar_gui_inicio)
    

    frame = ctk.CTkFrame(
        perfil_app,
        width=124,
        height=626,
        corner_radius=0,
        fg_color="transparent"
        )
    frame.pack(side="left")
    frame.pack_propagate(False)

    canvas = ctk.CTkCanvas(
        frame,
        width=124,
        height=626,
        highlightthickness=0,
        bg="#FFFAFA"
    )
    canvas.pack(fill='both', expand=True)

    def on_home_click(event=None):
        #print("Direciona para tela Inicial")
        ir_inicio()


    try:

        pil_home_icon = Image.open(HOME_ICON).resize((51, 50))
        home_icon = ImageTk.PhotoImage(pil_home_icon)
        canvas.home_icon = home_icon

        home_btn = canvas.create_image(124/2, 82, image=home_icon)
        canvas.tag_bind(home_btn, "<Button-1>", on_home_click)
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: Arquivo de imagem não encontrado em: {HOME_ICON}")
    except Exception as e:
        print(f"ERRO CRÍTICO ao carregar a imagem home: {e}")


    frame_principal = ctk.CTkFrame(
        perfil_app,
        width=845, 
        height=626, 
        corner_radius=0,
        fg_color="transparent"
    )
    frame_principal.pack(side="left")
    frame_principal.pack_propagate(False)

    canvas_principal = ctk.CTkCanvas(
        frame_principal,
        width=845,
        height=626,
        highlightthickness=0,
        bg="#FFFAFA"
    )
    canvas_principal.pack(fill='both', expand=True)

#   --BLOCO INFO

    bloco_info = ctk.CTkFrame(
        canvas_principal,
        width= 578,
        height= 224,
        fg_color="#E0E0D4",
        corner_radius=10,
    )
    bloco_info.pack_propagate(False)

    nome_empresa = ctk.CTkLabel(
        bloco_info,
        #text=current_user.nome_empresa.upper(),
        text="NOME DA EMPRESA",
        font=("Inter", 24, "bold"),
        text_color="#4E5D4D",
        wraplength=500
    )
    nome_empresa.pack(pady=11, anchor="n")

    cod_empresa = ctk.CTkLabel(
        bloco_info,
        #text=f"CÓDIGO DA EMPRESA: {current_user.cod_empresa}",
        text="CÓDIGO DA EMPRESA:",
        font=("Inter", 16, "bold"),
        text_color="#52765A",
        wraplength=500
    )
    cod_empresa.place(relx = 0.04, rely= 0.25)

    cnpj_empresa = ctk.CTkLabel(
        bloco_info,
        #text=f"CNPJ: {current_user.cnpj_empresa}",
        text="CNPJ DA EMPRESA:",
        font=("Inter", 16, "bold"),
        text_color="#52765A",
        wraplength=500
    )
    cnpj_empresa.place(relx = 0.04, rely= 0.45)

    email_empresa = ctk.CTkLabel(
        bloco_info,
        #text=f"EMAIL: {current_user.email_empresa}",
        text="EMAIL DA EMPRESA:",
        font=("Inter", 16, "bold"),
        text_color="#52765A",
        wraplength=500
    )
    email_empresa.place(relx = 0.04, rely= 0.65)

    senha_empresa = ctk.CTkLabel(
        bloco_info,
        #text=f"SENHA: {current_user.senha_empresa}",
        text="SENHA DA EMPRESA:",
        font=("Inter", 16, "bold"),
        text_color="#52765A",
        wraplength=500
    )
    senha_empresa.place(relx = 0.04, rely= 0.85)
    
    canvas_principal.create_window(
        845/2,
        167,
        window=bloco_info
    )

    bloco_score = ctk.CTkFrame(
        canvas_principal,
        width= 578,
        height= 140,
        fg_color="#E0E0D4",
        corner_radius=10,
    )

    bloco_score.pack_propagate(False)
    
#   --BLOCO SCORE

    pont_empresa = ctk.CTkLabel(
        bloco_score,
        text="Sua Pontuação",
        font=("Inter", 24, "bold"),
        text_color="#4E5D4D",
        wraplength=500
    )
    pont_empresa.place(relx = 0.04, rely= 0.10)

    pontuacao_diaria = ctk.CTkLabel(
        bloco_score,
        text="Pontuação Diária: ",
        font=("Inter", 16, "bold"),
        text_color="#52765A",
        wraplength=500
    )
    pontuacao_diaria.place(relx = 0.04, rely= 0.35)

    mensal_pontuacao = ctk.CTkLabel(
        bloco_score,
        text="Pontuação Total do Mês:",
        font=("Inter", 16, "bold"),
        text_color="#52765A",
        wraplength=500
    )
    mensal_pontuacao.place(relx = 0.04, rely= 0.55)

    avaliacao = ctk.CTkLabel(
        bloco_score,
        text="Avaliação:",
        font=("Inter", 16, "bold"),
        text_color="#52765A",
        wraplength=500
    )
    avaliacao.place(relx = 0.04, rely= 0.75)

    canvas_principal.create_window(
        845/2,
        356,
        window=bloco_score
    )

    print(f"DEBUG: Estado do current_user ao abrir o perfil: {current_user.__dict__}")


    perfil_app.after(100, preencher_dados)
    perfil_app.mainloop()