from datetime import datetime
from fastapi import HTTPException
import pandas as pd
import re
from api.config_api.config import EXCEL_PATH


def autenticar_empresa(empresa_id: int):
    df_login = pd.read_excel(EXCEL_PATH, sheet_name='login_empresa')
    login = df_login[
        (df_login['cod_empresa_FK'] == empresa_id) &
        (df_login['login_auth'] == 1)
    ]
    if login.empty:
        raise HTTPException(status_code=404, detail="Empresa não autenticada!")
    return True

def autenticar_usuario(user_id: int):
    df_login = pd.read_excel(EXCEL_PATH, sheet_name='login_user')
    login = df_login[
        (df_login['cod_user_FK'] == user_id) &
        (df_login['login_auth'] == 1)
    ]
    if login.empty:
        raise HTTPException(status_code=404, detail="Usuario não autenticado!")
    return True

def user_admin(auth: bool, user_id: int):
    df_login = pd.read_excel(EXCEL_PATH, sheet_name='user')
    login = df_login[
        (df_login['cod_user'] == user_id) &
        (df_login['user_type'] == 1)
    ]
    if login.empty:
        raise HTTPException(status_code=404, detail="Não é administrador!")
    return True

def conferencia_senha(senha: str) -> bool:
    if len(senha) < 6:
        return False

    if not re.search(r"\d", senha):
        return False

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
        return False

    return True


def calcular_score_diario(cod_empresa_FK: int):
    df_database = pd.read_excel(EXCEL_PATH, sheet_name=None)

    if "resposta" not in df_database or "score" not in df_database:
        raise HTTPException(status_code=404, detail="Tabelas 'resposta' ou 'score' não encontradas.")

    df_resposta = df_database["resposta"]
    df_score = df_database["score"]

    df_resposta["respDiaria_data"] = pd.to_datetime(df_resposta["respDiaria_data"], errors="coerce").dt.date
    hoje = datetime.now().date()

    respostas_hoje = df_resposta[
        (df_resposta["cod_empresa_FK"] == cod_empresa_FK) &
        (df_resposta["respDiaria_data"] == hoje)
    ]

    if respostas_hoje.empty:
        return {"mensagem": "Nenhuma resposta encontrada para hoje."}

    total_score = int(respostas_hoje["respDiaria_pontuacao"].sum())

    df_score["score_data"] = pd.to_datetime(df_score["score_data"], errors="coerce").dt.date
    score_existente = df_score[
        (df_score["cod_empresa_FK"] == cod_empresa_FK) &
        (df_score["score_data"] == hoje)
    ]

    if not score_existente.empty:
        df_score.loc[
            (df_score["cod_empresa_FK"] == cod_empresa_FK) &
            (df_score["score_data"] == hoje),
            "score_total"
        ] = total_score
        mensagem = "Score diário atualizado."
        cod_score = int(score_existente["cod_score"].values[0])
    else:
        novo_cod = 1 if df_score.empty else int(df_score["cod_score"].max()) + 1
        nova_linha = {
            "cod_score": novo_cod,
            "cod_empresa_FK": cod_empresa_FK,
            "score_total": total_score,
            "score_data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        df_score = pd.concat([df_score, pd.DataFrame([nova_linha])], ignore_index=True)
        mensagem = "Novo score diário criado."
        cod_score = novo_cod

    with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df_score.to_excel(writer, sheet_name="score", index=False)
        for sheet_name, df_sheet in df_database.items():
            if sheet_name != "score":
                df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

    return {
        "mensagem": mensagem,
        "cod_score": int(cod_score),
        "score_total": total_score
    }

