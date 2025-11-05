import pandas as pd
from fastapi import APIRouter, HTTPException
from datetime import datetime
from api.config_api.config import EXCEL_PATH
from api.modules.__modules import calcular_score_diario

resposta_router = APIRouter(prefix="/resposta", tags=["resposta"])

@resposta_router.post("/")
async def registrar_resposta(cod_empresa_FK: int, cod_pergunta_FK: int, respDiaria_texto: str):
    """
    Registra uma resposta de pergunta e atualiza o score diário da empresa.
    """
    try:
        df_database = pd.read_excel(EXCEL_PATH, sheet_name=None)

        if "pergunta" not in df_database or "resposta" not in df_database:
            raise HTTPException(status_code=404, detail="Tabelas 'pergunta' ou 'resposta' não encontradas.")

        df_pergunta = df_database["pergunta"]
        df_resposta = df_database["resposta"]

        pergunta = df_pergunta[df_pergunta["cod_pergunta"] == cod_pergunta_FK]
        if pergunta.empty:
            raise HTTPException(status_code=404, detail="Pergunta não encontrada.")

        hoje = datetime.now().date()
        if not df_resposta.empty:
            df_resposta["respDiaria_data"] = pd.to_datetime(df_resposta["respDiaria_data"], errors="coerce").dt.date
            ja_respondeu = df_resposta[
                (df_resposta["cod_empresa_FK"] == cod_empresa_FK) &
                (df_resposta["cod_pergunta_FK"] == cod_pergunta_FK) &
                (df_resposta["respDiaria_data"] == hoje)
            ]
            if not ja_respondeu.empty:
                raise HTTPException(
                    status_code=400,
                    detail="A empresa já respondeu essa pergunta hoje. Tente novamente amanhã."
                )

        pergunta_peso = int(pergunta["pergunta_peso"].values[0])

        resposta_normalizada = respDiaria_texto.strip().lower()
        if resposta_normalizada in ["sim", "1"]:
            respDiaria_pontuacao = pergunta_peso
        elif resposta_normalizada in ["não", "nao", "0"]:
            respDiaria_pontuacao = 0
        else:
            raise HTTPException(status_code=400, detail="Resposta inválida. Use 'Sim'/'Não' ou '1'/'0'.")

        novo_cod = 1 if df_resposta.empty else int(df_resposta["cod_respDiaria"].max()) + 1

        nova_resposta = {
            "cod_respDiaria": novo_cod,
            "cod_pergunta_FK": cod_pergunta_FK,
            "respDiaria_data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "respDiaria_texto": resposta_normalizada.capitalize(),
            "respDiaria_pontuacao": respDiaria_pontuacao,
            "cod_empresa_FK": cod_empresa_FK
        }

        df_resposta = pd.concat([df_resposta, pd.DataFrame([nova_resposta])], ignore_index=True)

        with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df_resposta.to_excel(writer, sheet_name="resposta", index=False)
            for sheet_name, df_sheet in df_database.items():
                if sheet_name != "resposta":
                    df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

        score_info = calcular_score_diario(cod_empresa_FK)

        return {
            "mensagem": "Resposta registrada com sucesso!",
            "cod_respDiaria": int(novo_cod),
            "cod_empresa_FK": cod_empresa_FK,
            "cod_pergunta_FK": cod_pergunta_FK,
            "respDiaria_pontuacao": respDiaria_pontuacao,
            "score_atual": score_info
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao registrar resposta: {str(e)}")