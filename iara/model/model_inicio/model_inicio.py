import customtkinter as ctk
from tkinter import messagebox
import requests
from session import current_user
from PIL import Image, ImageTk
from model.config_model.config import API_URL, NOTIFY_ICON, PROFILE_ICON, AVALIACAO_BAIXA, AVALIACAO_BOA, AVALIACAO_OK, AVALIACAO_OTIMA, AVALIACAO_RUIM, SCORE_BAIXA, SCORE_BOM, SCORE_OK, SCORE_OTIMA, SCORE_RUIM, LINHA, LOGOUT_ICON, AVALIACAO_NULA, SCORE_NULO
from model.model_perguntas.model_perguntas import iniciar_gui_perguntas
from model.model_loading.model_loading import show_loading_screen
from model.model_notificacoes.model_notificacoes import iniciar_notificacoes_gui

def iniciar_gui_inicio():
    inicio_app = ctk.CTk()
    inicio_app.title("Ecoscore - Inicio")
    inicio_app.geometry("1093x626")
    inicio_app.resizable(False, False)
    inicio_app.config(bg="#FFFAFA")
    ctk.set_appearance_mode("light")

    def preencher_dados_inicio():
        try:
            response = requests.get(f"{API_URL}/company/score/{current_user.cod_empresa}")

            if response.status_code == 200:
                data = response.json()

                print(f"DEBUG: Dados completos da API: {data}")

                maior_score_btn.configure(text=f"Score Total\n do Mês: {data.get('score_mensal', 'N/A')}")

                canvas.itemconfig(porc_score, text=f"{str(data.get('porcentagem_obtida', 'N/A'))}%")

                score1_img = ImageTk.PhotoImage(pil_score1_img)
                canvas.score1_img = score1_img

                score_diario_ruim_img = ImageTk.PhotoImage(pil_scorediar_ruim)
                canvas.score_diario_ruim_img = score_diario_ruim_img

                score2_img = ImageTk.PhotoImage(pil_score2_img)
                canvas.score2_img = score2_img

                score_diario_baixa_img = ImageTk.PhotoImage(pil_scorediar_baixa)
                canvas.score_diario_baixa_img = score_diario_baixa_img

                score3_img = ImageTk.PhotoImage(pil_score3_img)
                canvas.score3_img = score3_img

                score_diario_ok_img = ImageTk.PhotoImage(pil_scorediar_ok)
                canvas.score_diario_ok_img = score_diario_ok_img

                score4_img = ImageTk.PhotoImage(pil_score4_img)
                canvas.score4_img = score4_img

                score_diario_bom_img = ImageTk.PhotoImage(pil_scorediar_bom)
                canvas.score_diario_bom_img = score_diario_bom_img

                score5_img = ImageTk.PhotoImage(pil_score5_img)
                canvas.score5_img = score5_img

                score_diario_otima_img = ImageTk.PhotoImage(pil_scorediar_otima)
                canvas.score_diario_otima_img = score_diario_otima_img

                if data.get('status') == 0:
                    canvas.itemconfig(scores_img, image=canvas.score1_img)
                    canvas.itemconfig(scores_diario_img, image=canvas.score_diario_ruim_img)
                    canvas.itemconfig(porc_score, fill="#DE494B")
                    print("Trocando a imagem para status 0...")
                elif data.get('status') == 1:
                    canvas.itemconfig(scores_img, image=canvas.score2_img)
                    canvas.itemconfig(scores_diario_img, image=canvas.score_diario_baixa_img)
                    canvas.itemconfig(porc_score, fill="#EE8667")
                    print("Trocando a imagem para status 1...")
                elif data.get('status') == 2:
                    canvas.itemconfig(scores_img, image=canvas.score3_img)
                    canvas.itemconfig(scores_diario_img, image=canvas.score_diario_ok_img)
                    canvas.itemconfig(porc_score, fill="#DEE85B")
                    print("Trocando a imagem para status 2...")
                elif data.get('status') == 3:
                    canvas.itemconfig(scores_img, image=canvas.score4_img)
                    canvas.itemconfig(scores_diario_img, image=canvas.score_diario_bom_img)
                    porc_score.configure(text_color="#ADF06A")
                    print("Trocando a imagem para status 3...")
                elif data.get('status') == 4:
                    canvas.itemconfig(scores_img, image=canvas.score5_img)
                    canvas.itemconfig(scores_diario_img, image=canvas.score_diario_otima_img)
                    canvas.itemconfig(porc_score, fill="#FFCD87")
                    print("Trocando a imagem para status 4...")
                else:
                    canvas.itemconfig(scores_img, image=canvas.score3_img)
                    canvas.itemconfig(scores_diario_img, image=canvas.score_diario_ok_img)
                    canvas.itemconfig(porc_score, fill="#DEE85B")
                    print("Status desconhecido, nenhuma imagem para exibir.")

        except requests.exceptions.ConnectionError:
            print("Erro de conexão: Não foi possível conectar à API.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    def ir_perguntas():
        show_loading_screen(iniciar_gui_perguntas)

    frameEsq = ctk.CTkFrame(
        inicio_app,
        width=113,
        height=626,
        corner_radius=0,
    )
    frameEsq.pack(side="left")
    frameEsq.pack_propagate(False)

    canvasEsq = ctk.CTkCanvas(
        frameEsq,
        highlightthickness=0,
        bg='#FFFAFA'
    )
    canvasEsq.pack(fill='both', expand=True)

    def on_notify_click(event=None):
        print("Direciona para as notificações")
        show_loading_screen(iniciar_notificacoes_gui)

    try:
        pil_notify_icon = Image.open(NOTIFY_ICON).resize((34, 50))
        notify_icon = ImageTk.PhotoImage(pil_notify_icon)
        canvasEsq.notify_icon = notify_icon

        notify_btn = canvasEsq.create_image(124/2, 83, image=notify_icon)
        canvasEsq.tag_bind(notify_btn, "<Button-1>", on_notify_click)
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: Arquivo de imagem não encontrado em: {NOTIFY_ICON}")
    except Exception as e:
        print(f"ERRO CRÍTICO ao carregar a imagem de notificação: {e}")

    frameDir = ctk.CTkFrame(
        inicio_app,
        width=113,
        height=626,
        corner_radius=0,
    )
    frameDir.pack(side="right")
    frameDir.pack_propagate(False)

    canvasDir = ctk.CTkCanvas(
        frameDir,
        highlightthickness=0,
        bg='#FFFAFA'
    )
    canvasDir.pack(fill='both', expand=True)

    def on_profile_click(event=None):
        from model.model_loading.model_loading import show_loading_screen
        from model.model_perfil.model_perfil import iniciar_gui_perfil
        #print("Direciona para o profile da empresa")
        inicio_app.destroy()
        show_loading_screen(iniciar_gui_perfil)
    
    try:
        pil_profile_icon = Image.open(PROFILE_ICON).resize((50, 50))
        profile_icon = ImageTk.PhotoImage(pil_profile_icon)
        canvasDir.profile_icon = profile_icon

        profile_btn = canvasDir.create_image(124/2, 83, image=profile_icon)
        canvasDir.tag_bind(profile_btn, "<Button-1>", on_profile_click)
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: Arquivo de imagem não encontrado em: {PROFILE_ICON}")
    except Exception as e:
        print(f"ERRO CRÍTICO ao carregar a imagem de profile: {e}")

    def on_logout_click(event=None):
        from model.model_loading.model_loading import show_loading_screen
        from model.model_login.model_login import iniciar_gui
        #print("Direciona para o profile da empresa")
        try:
            response = requests.put(
                f"{API_URL}/login/logout",
                params={
                    "cod_login": current_user.cod_login
                }
            )

            if response.status_code == 200:
                inicio_app.destroy()
                show_loading_screen(iniciar_gui)
            else:
                erro = response.json().get("detail", "Erro desconhecido.")
                messagebox.showerror("Erro", erro)
        except Exception as e:
            print(f"ERRO CRÍTICO: Falha ao fazer o logout")
    
    try:
        pil_logout_icon = Image.open(LOGOUT_ICON).resize((45, 50))
        logout_icon = ImageTk.PhotoImage(pil_logout_icon)
        canvasDir.logout_icon = logout_icon

        logout_btn = canvasDir.create_image(124/2, 197, image=logout_icon)
        canvasDir.tag_bind(logout_btn, "<Button-1>", on_logout_click)
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: Arquivo de imagem não encontrado em: {PROFILE_ICON}")
    except Exception as e:
        print(f"ERRO CRÍTICO ao carregar a imagem de logout: {e}")
    
    frame = ctk.CTkFrame(
        inicio_app,
        width=850,
        height=625,
        corner_radius=0,
        fg_color='transparent'
    )
    frame.pack()
    frame.pack_propagate(False)

    canvas = ctk.CTkCanvas(
        frame,
        highlightthickness=0,
        bg="#FFFAFA"
    )
    canvas.pack(fill='both', expand=True)

    perguntas_btn = ctk.CTkButton(
        canvas,
        width=280,
        height=253,
        corner_radius=30,
        border_spacing=5,
        fg_color="#7EB87E",
        text="PERGUNTAS",
        font=("Inter", 24, "bold"),
        text_color="#FFFAFA",
        command=ir_perguntas
    )

    maior_score_btn = ctk.CTkButton(
        canvas,
        width=280,
        height=253,
        corner_radius=30,
        border_spacing=5,
        fg_color="#4E5D4D",
        text="SEU MAIOR SCORE",
        font=("Inter", 24, "bold"),
        text_color="#FFFAFA"
    )

    espacamento = 40  
    largura_total = 280 * 2 + espacamento  
    inicio_x = (850 - largura_total) / 2 

    canvas.create_window(
        inicio_x + 280 / 2,
        181.5, 
        anchor='center',
        window=perguntas_btn
    )

    canvas.create_window(
        inicio_x + 280 + espacamento + 280 / 2,
        181.5,  # mesma altura
        anchor='center',
        window=maior_score_btn
    )


    try:

        pil_linha = Image.open(LINHA)
        linha_img = ImageTk.PhotoImage(pil_linha)
        canvas.linha = linha_img

        canvas.create_image(850/2, 468, image=linha_img)
        
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: Arquivo de imagem não encontrado em: {LINHA}")
    except Exception as e:
        print(f"ERRO CRÍTICO ao carregar a imagem home: {e}")

    pil_score1_img = Image.open(AVALIACAO_RUIM).resize((850, 124))
    pil_score2_img = Image.open(AVALIACAO_BAIXA).resize((850, 124))
    pil_score3_img = Image.open(AVALIACAO_OK).resize((850, 124))
    pil_score4_img = Image.open(AVALIACAO_BOA).resize((850, 124))
    pil_score5_img = Image.open(AVALIACAO_OTIMA).resize((850, 124))
    
    pil_score_null_img = Image.open(AVALIACAO_NULA).resize((850, 124))
    score_null_img = ImageTk.PhotoImage(pil_score_null_img)
    canvas.score_null_img = score_null_img

    scores_img = canvas.create_image(850/2, 387.5, image=canvas.score_null_img)

    #scores_img = canvas.create_image(850/2, 387.5, image=AVALIACAO_NULA)

    pil_scorediar_ruim = Image.open(SCORE_RUIM).resize((849, 81))
    pil_scorediar_baixa = Image.open(SCORE_BAIXA).resize((849, 81))
    pil_scorediar_ok = Image.open(SCORE_OK).resize((849, 81))
    pil_scorediar_bom = Image.open(SCORE_BOM).resize((849, 81))
    pil_scorediar_otima = Image.open(SCORE_OTIMA).resize((849, 81))

    pil_scorediar_null = Image.open(SCORE_NULO).resize((849, 81))
    score_diario_null_img = ImageTk.PhotoImage(pil_scorediar_null)
    canvas.score_diario_null_img = score_diario_null_img

    scores_diario_img = canvas.create_image(850/2, 528, image=canvas.score_diario_null_img)


    porc_score = canvas.create_text(
        700,
        528,
        text='',
        font=('Poppins', 48),
        fill="#DEE85B"
    )
    

    inicio_app.after(50, preencher_dados_inicio)
    inicio_app.mainloop()