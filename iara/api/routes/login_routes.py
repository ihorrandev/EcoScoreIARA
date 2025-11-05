import pandas as pd
from fastapi import APIRouter, HTTPException
from api.config_api.config import EXCEL_PATH

login_router = APIRouter(prefix="/login", tags=["login"])

@login_router.post("/")
async def login_empresa(empresa_cod: str, empresa_email: str, empresa_senha: int):
    df_database = pd.read_excel(EXCEL_PATH, sheet_name=None)

    df_empresa = df_database["empresa"]
    df_login_empresa = df_database.get("login_empresa", pd.DataFrame(columns=["cod_login", "login_auth", "cod_empresa_FK"]))

    empresa = df_empresa[df_empresa["empresa_cod"] == empresa_cod]
    if empresa.empty:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    cod_empresa = int(empresa["cod_empresa"].values[0])
    empresa_nome = empresa["empresa_nome"].values[0]

    email_correto = empresa["empresa_email"].values[0]
    senha_correta = str(empresa["empresa_senha"].values[0])
    if str(empresa_senha) != senha_correta and empresa_email != email_correto:
        raise HTTPException(status_code=401, detail="Dados incorretos!")

    login_existente = df_login_empresa[df_login_empresa["cod_empresa_FK"] == cod_empresa]

    if not login_existente.empty:
        df_login_empresa.loc[df_login_empresa["cod_empresa_FK"] == cod_empresa, "login_auth"] = 1
        cod_login = int(login_existente["cod_login"].values[0])
    else:
        novo_cod_login = 1 if df_login_empresa.empty else int(df_login_empresa["cod_login"].max()) + 1
        nova_linha = {
            "cod_login": novo_cod_login,
            "login_auth": 1,
            "cod_empresa_FK": cod_empresa
        }
        df_login_empresa = pd.concat([df_login_empresa, pd.DataFrame([nova_linha])], ignore_index=True)
        cod_login = novo_cod_login

    with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df_empresa.to_excel(writer, sheet_name="empresa", index=False)
        df_login_empresa.to_excel(writer, sheet_name="login_empresa", index=False)

        for sheet_name, df_sheet in df_database.items():
            if sheet_name not in ["empresa", "login_empresa"]:
                df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

    return {
        "mensagem": "Login realizado com sucesso!",
        "cod_empresa": int(cod_empresa),      
        "cod_login": int(cod_login),
        "empresa_cod": empresa_cod,          
        "empresa_email": empresa_email,
        "empresa_nome": empresa_nome
    }


@login_router.put("/logout")
async def logout_empresa(cod_login: int):
    df_database = pd.read_excel(EXCEL_PATH, sheet_name=None)
    df_login_empresa = df_database.get("login_empresa")

    if df_login_empresa is None or df_login_empresa.empty:
        raise HTTPException(status_code=404, detail="Nenhum login encontrado")

    if cod_login not in df_login_empresa["cod_login"].values:
        raise HTTPException(status_code=404, detail="Login não encontrado")

    df_login_empresa.loc[df_login_empresa["cod_login"] == cod_login, "login_auth"] = 0

    with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df_login_empresa.to_excel(writer, sheet_name="login_empresa", index=False)
        for sheet_name, df_sheet in df_database.items():
            if sheet_name != "login_empresa":
                df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

    return {
        "mensagem": "Logout realizado com sucesso!",
        "cod_login": int(cod_login)
    }
