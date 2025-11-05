import pandas as pd
from fastapi import APIRouter, HTTPException
from api.config_api.config import EXCEL_PATH

pergunta_router = APIRouter(prefix="/perguntas", tags=["perguntas"])

@pergunta_router.get("/")
async def get_perguntas(cod_categoria: int = None):
    try:
        df_database = pd.read_excel(EXCEL_PATH, sheet_name=None)
        if "pergunta" not in df_database:
            raise HTTPException(status_code=404, detail="Tabela 'pergunta' não encontrada no banco de dados.")

        df_pergunta = df_database["pergunta"]

        if cod_categoria:
            df_pergunta = df_pergunta[df_pergunta["cod_categoria"] == cod_categoria]

        if df_pergunta.empty:
            raise HTTPException(status_code=404, detail="Nenhuma pergunta encontrada.")

        perguntas = df_pergunta.to_dict(orient="records")
        return {"total": len(perguntas), "perguntas": perguntas}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar perguntas: {str(e)}")
