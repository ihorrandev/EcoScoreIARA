import customtkinter as ctk
import random

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

DICAS_SUSTENTABILIDADE = [
    """🌿 Gestão de Resíduos Corporativos
Implemente um programa de coleta seletiva no escritório, com lixeiras identificadas para papel, plástico e orgânicos. 
Crie relatórios mensais mostrando o impacto positivo e premie equipes que mais colaborarem.""",

    """💧 Redução de Consumo de Água
Substitua torneiras comuns por modelos com temporizador e instale redutores de vazão. 
Capte água da chuva para limpeza e manutenção. Promova campanhas internas de conscientização sobre o uso consciente.""",

    """⚡ Eficiência Energética
Troque lâmpadas por LEDs, use sensores de presença e desligue aparelhos fora do expediente. 
Monitore o consumo mensal e incentive metas de economia por setor.""",

    """🌱 Compras Sustentáveis
Priorize fornecedores com certificações ambientais e políticas de ESG. 
Inclua cláusulas de sustentabilidade em contratos e divulgue anualmente o impacto positivo dessas ações.""",

    """🚲 Mobilidade Sustentável
Incentive o uso de transporte coletivo, caronas e bicicletas. 
Crie bicicletários e promova campanhas de conscientização sobre mobilidade limpa.""",

    """♻️ Cultura Ambiental
Promova treinamentos internos sobre sustentabilidade, 
divulgue boas práticas no mural da empresa e envolva colaboradores em ações ambientais externas."""
]

def iniciar_notificacoes_gui():
    app = ctk.CTk()
    app.title("EcoScore - Dicas de Sustentabilidade")
    app.geometry("1000x600")
    app.resizable(False, False)
    app.configure(fg_color="#EAF1EA") 

    frame = ctk.CTkFrame(app, corner_radius=10, fg_color="#EAF1EA")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    def ir_inicio():
        from model.model_inicio.model_inicio import iniciar_gui_inicio
        app.destroy()
        iniciar_gui_inicio()

    btn_voltar = ctk.CTkButton(
        frame,
        text="⬅ Voltar ao Início",
        fg_color="#2E7D32",
        hover_color="#1B5E20",
        text_color="white",
        font=("Inter", 16, "bold"),
        width=180,
        height=40,
        command=ir_inicio
    )
    btn_voltar.pack(anchor="nw", pady=(10, 0), padx=(10, 0))

    # Título
    title = ctk.CTkLabel(
        frame,
        text="🌎 Dica de Sustentabilidade Corporativa",
        font=("Inter", 28, "bold"),
        text_color="#1B5E20"
    )
    title.pack(pady=(30, 15))

    # Dica principal
    dica_label = ctk.CTkLabel(
        frame,
        text=random.choice(DICAS_SUSTENTABILIDADE),
        font=("Inter", 20),
        text_color="#145A32",
        wraplength=850,
        justify="center"
    )
    dica_label.pack(expand=True, pady=(40, 30))

    def nova_dica():
        dica_label.configure(text=random.choice(DICAS_SUSTENTABILIDADE))

    btn_nova = ctk.CTkButton(
        frame,
        text="Nova Dica",
        fg_color="#2E7D32",
        hover_color="#1B5E20",
        text_color="white",
        font=("Inter", 18, "bold"),
        width=200,
        height=50,
        command=nova_dica
    )
    btn_nova.pack(pady=(10, 20))

    app.mainloop()

if __name__ == "__main__":
    iniciar_notificacoes_gui()
