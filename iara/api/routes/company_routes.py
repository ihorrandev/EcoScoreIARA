import pandas as pd
from fastapi import APIRouter, HTTPException
from api.config_api.config import EXCEL_PATH
from api.modules.__modules import autenticar_empresa, autenticar_usuario, user_admin
from api.modules.__classes import Empresa, EmpresaUpdate

company_router = APIRouter(prefix="/company", tags=["company"])

@company_router.get("/all")
async def get_all(user_id: int):
    df_database = pd.read_excel(EXCEL_PATH, sheet_name=None)
    df_empresa = df_database["empresa"]
    auth = autenticar_usuario(user_id)

    if auth:
        admin = user_admin(auth, user_id)
        if admin:
            companies = df_empresa.to_dict(orient="records")
    return companies

@company_router.get("/{cod_empresa}")
async def get_company(cod_empresa: int):

    df_database = pd.read_excel(EXCEL_PATH, sheet_name=None)
    df_empresa = df_database["empresa"]
    auth = autenticar_empresa(cod_empresa)

    if auth:
        empresa = df_empresa[df_empresa['cod_empresa'] == cod_empresa]
        empresa_teste = empresa.to_dict(orient="records")
    return empresa_teste


@company_router.put("/registrar", status_code=201)
async def put_company(nova_empresa: Empresa):
    import pandas as pd
    from api.config_api.config import EXCEL_PATH

    df_database = pd.read_excel(EXCEL_PATH, sheet_name=None)
    df_empresa = df_database["empresa"]

    if df_empresa.empty:
        novo_cod_empresa = 1
    else:
        novo_cod_empresa = int(pd.to_numeric(df_empresa["cod_empresa"], errors="coerce").max() +1)

    empresa_cod = f"EMP{novo_cod_empresa:03d}"

    nova_linha = {
        "cod_empresa": novo_cod_empresa,
        "empresa_cod": empresa_cod,
        **nova_empresa.dict()
    }

    df_empresa = pd.concat([df_empresa, pd.DataFrame([nova_linha])], ignore_index=True)

    with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df_empresa.to_excel(writer, sheet_name="empresa", index=False)
        for sheet_name, df_sheet in df_database.items():
            if sheet_name != "empresa":
                df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

    return {
        "mensagem": "Empresa cadastrada com sucesso!",
        "cod_empresa": novo_cod_empresa,
        "empresa_cod": empresa_cod
    }


@company_router.patch("/{cod_empresa}")
async def atualizar_empresa(cod_empresa: int, dados: EmpresaUpdate):
    df_database = pd.read_excel(EXCEL_PATH, sheet_name=None)
    df_empresa = df_database["empresa"]
    auth = autenticar_empresa(cod_empresa)

    if auth: 
        if not df_empresa['cod_empresa'].eq(cod_empresa).any():
            raise HTTPException(status_code=404, detail="Empresa não encontrada")

        atualizacoes = dados.dict(exclude_unset=True)
        for coluna, valor in atualizacoes.items():
            df_empresa.loc[df_empresa['cod_empresa'] == cod_empresa, coluna] = valor

        with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df_empresa.to_excel(writer, sheet_name="empresa", index=False)
            for sheet_name, df_sheet in df_database.items():
                if sheet_name != "empresa":
                    df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

        return {"mensagem": "Empresa atualizada com sucesso!", "cod_empresa": cod_empresa}


@company_router.delete("/{cod_empresa}")
async def deletar_empresa(cod_empresa: int):
    df_database = pd.read_excel(EXCEL_PATH, sheet_name=None)
    df_empresa = df_database["empresa"]
    df_login_empresa = df_database["login_empresa"]
    auth = autenticar_empresa(cod_empresa)

    if auth: 
        if not df_empresa['cod_empresa'].eq(cod_empresa).any():
            raise HTTPException(status_code=404, detail="Empresa não encontrada")
        
        df_empresa = df_empresa[df_empresa['cod_empresa'] != cod_empresa]
        df_login_empresa = df_login_empresa[df_login_empresa['cod_empresa_FK'] != cod_empresa]

        with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df_empresa.to_excel(writer, sheet_name="empresa", index=False)
            df_login_empresa.to_excel(writer, sheet_name="login_empresa", index=False)
            for sheet_name, df_sheet in df_database.items():
                if sheet_name not in ["empresa", "login_empresa"]:
                    df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

        return {"mensagem": "Empresa deletada com sucesso!", "cod_empresa": cod_empresa}

@company_router.get("/score/{cod_empresa}")

async def ler_score(cod_empresa: int):
    try:
        df_database = pd.read_excel(EXCEL_PATH, sheet_name=None)
        if "score" not in df_database:
            raise HTTPException(status_code=404, detail="Tabela 'score' não encontrada.")


        df_score = df_database["score"]
        df_score["score_data"] = pd.to_datetime(df_score["score_data"], errors="coerce")


        empresa_score = df_score[df_score["cod_empresa_FK"] == cod_empresa]
        if empresa_score.empty:
            raise HTTPException(status_code=404, detail="Score da empresa não encontrado.")


        ultimo_registro = empresa_score.sort_values(by="score_data", ascending=False).iloc[0]
        ultimo_score_total = int(ultimo_registro["score_total"])
        ultimo_score_data = ultimo_registro["score_data"]


        mes = ultimo_score_data.month
        ano = ultimo_score_data.year


        score_mensal = empresa_score[
            (empresa_score["score_data"].dt.month == mes) &
            (empresa_score["score_data"].dt.year == ano)
        ]["score_total"].sum()


        dias_uteis = 22
        score_medio_dia = score_mensal / dias_uteis if dias_uteis > 0 else 0
        #score_medio_hoje = (ultimo_score_total * 100) / 170


        if ultimo_score_total <= 34:
            status = 0
            status_texto = "Ruim"
        elif ultimo_score_total <= 68:
            status = 1
            status_texto = "Baixa"
        elif ultimo_score_total <= 102:
            status = 2
            status_texto = "Ok"
        elif ultimo_score_total <= 136:
            status = 3
            status_texto = "Boa"
        else:
            status = 4
            status_texto = "Ótima"


        SCORE_MAXIMO = 170
        porcentagem_obtida = (ultimo_score_total / SCORE_MAXIMO) * 100


        return {
            "cod_empresa_FK": cod_empresa,
            "score_total": ultimo_score_total,
            "score_data": str(ultimo_score_data),
            "mes_referencia": f"{mes:02d}/{ano}",
            "score_mensal": int(score_mensal),
            "dias_uteis": dias_uteis,
            "score_medio_dia": round(score_medio_dia, 2),
            "status": status,
            "status_texto": status_texto,
            "porcentagem_obtida": round(porcentagem_obtida),
        }


    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler o score: {str(e)}")