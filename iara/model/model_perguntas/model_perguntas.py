import customtkinter as ctk
import requests
from session import current_user
from tkinter import messagebox
from model.config_model.config import API_URL


def iniciar_gui_perguntas():
    perguntas_app = ctk.CTk()
    perguntas_app.title("Ecoscore - Perguntas")
    perguntas_app.geometry("1093x626")
    perguntas_app.resizable(False, False)
    perguntas_app.config(bg="#B2BEA9")
    ctk.set_appearance_mode("light")

    lista_perguntas = []
    respostas = {}  
    indice_pergunta_atual = 0

    def exibir_pergunta():

        nonlocal indice_pergunta_atual

        if not lista_perguntas:
            canvas.itemconfig(id_texto_pergunta, text="Nenhuma pergunta encontrada.")
            return

        if indice_pergunta_atual >= len(lista_perguntas):
            mostrar_resumo()
            return

        pergunta_atual = lista_perguntas[indice_pergunta_atual]
        num_pergunta = pergunta_atual.get('cod_pergunta')
        texto_pergunta = pergunta_atual.get('pergunta_texto', 'Texto não encontrado.')
        total_perguntas = len(lista_perguntas)

        canvas.itemconfig(id_texto_pergunta, text=f"{num_pergunta}/{total_perguntas}")
        canvas.itemconfig(id_texto_pergunta_completa, text=texto_pergunta)

        btn_sim.configure(state="normal")
        btn_nao.configure(state="normal")

        resposta_anterior = respostas.get(num_pergunta)
        if resposta_anterior == "1":
            btn_sim.configure(fg_color="#5FA55A")
            btn_nao.configure(fg_color="#E74C3C")
        elif resposta_anterior == "0":
            btn_nao.configure(fg_color="#C0392B")
            btn_sim.configure(fg_color="#7EB87E")
        else:
            btn_sim.configure(fg_color="#7EB87E")
            btn_nao.configure(fg_color="#E74C3C")

    def responder(resposta_texto):
        nonlocal indice_pergunta_atual
        if not lista_perguntas:
            return

        pergunta_atual = lista_perguntas[indice_pergunta_atual]
        cod_pergunta = pergunta_atual.get('cod_pergunta')
        respostas[cod_pergunta] = resposta_texto

        indice_pergunta_atual += 1
        exibir_pergunta()

    def voltar():
        nonlocal indice_pergunta_atual
        if indice_pergunta_atual > 0:
            indice_pergunta_atual -= 1
            exibir_pergunta()

    def mostrar_resumo():
        canvas.itemconfig(id_texto_pergunta, text="✅ Questionário finalizado!")
        canvas.itemconfig(id_texto_pergunta_completa,
                          text=f"Você respondeu {len(respostas)} perguntas.\nClique em 'Enviar Respostas' para finalizar.")

        btn_sim.configure(state="disabled")
        btn_nao.configure(state="disabled")
        btn_voltar.configure(state="disabled")
        btn_enviar.place(x=503, y=420, anchor="center")

    def enviar_respostas():
        try:
            for cod_pergunta, resposta in respostas.items():
                payload = {
                    "cod_empresa_FK": current_user.cod_empresa,
                    "cod_pergunta_FK": cod_pergunta,
                    "respDiaria_texto": resposta
                }
                response = requests.post(f"{API_URL}/resposta/", params=payload)
                if response.status_code != 200:
                    erro = response.json().get("detail", "Erro desconhecido.")
                    messagebox.showerror("Erro", f"Erro ao enviar resposta {cod_pergunta}: {erro}")
                    return

            messagebox.showinfo("Sucesso", "Todas as respostas foram enviadas com sucesso!")
            perguntas_app.destroy()
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao servidor.")
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

    def preencher_perguntas():
        nonlocal lista_perguntas
        try:
            response = requests.get(f"{API_URL}/perguntas/")
            if response.status_code == 200:
                dados_api = response.json()
                lista_perguntas = dados_api.get('perguntas', [])
                if not lista_perguntas:
                    canvas.itemconfig(id_texto_pergunta, text="Nenhuma pergunta encontrada.")
                    return
                exibir_pergunta()
            else:
                print(f"Erro ao buscar perguntas: {response.status_code}")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    frame = ctk.CTkFrame(perguntas_app, width=1093, height=626, corner_radius=0)
    frame.pack(expand=True, fill="both")
    frame.pack_propagate(False)

    canvas = ctk.CTkCanvas(frame, highlightthickness=0, bg='#FFFAFA')
    canvas.pack(fill='both', expand=True)

    id_texto_pergunta = canvas.create_text(503, 127, text='Carregando...', font=("Inter", 48, 'bold'), fill='#4E5D4D')
    id_texto_pergunta_completa = canvas.create_text(503, 200, text='Carregando...', font=("Inter", 18), fill='#4E5D4D', width=800)

    btn_sim = ctk.CTkButton(perguntas_app, text="SIM", width=150, height=50,
                            font=("Inter", 20, "bold"), fg_color="#7EB87E",
                            command=lambda: responder("1"))
    btn_nao = ctk.CTkButton(perguntas_app, text="NÃO", width=150, height=50,
                            font=("Inter", 20, "bold"), fg_color="#E74C3C",
                            command=lambda: responder("0"))
    btn_voltar = ctk.CTkButton(perguntas_app, text="← Voltar", width=120, height=40,
                               font=("Inter", 16, "bold"), fg_color="#95A5A6",
                               hover_color="#7F8C8D", command=voltar)
    btn_enviar = ctk.CTkButton(perguntas_app, text="Enviar Respostas", width=220, height=50,
                               font=("Inter", 20, "bold"), fg_color="#2E7D32",
                               hover_color="#1B5E20", command=enviar_respostas)


    canvas.create_window(503 - 80, 350, window=btn_sim, anchor="center")
    canvas.create_window(503 + 80, 350, window=btn_nao, anchor="center")
    canvas.create_window(90, 50, window=btn_voltar, anchor="center")

    perguntas_app.after(100, preencher_perguntas)
    perguntas_app.mainloop()
