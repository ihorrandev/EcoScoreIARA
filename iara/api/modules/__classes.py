from pydantic import BaseModel

class Empresa(BaseModel):
    empresa_nome: str
    empresa_cnpj: int
    empresa_email: str
    empresa_senha: str

class EmpresaUpdate(BaseModel):
    empresa_nome: str | None = None
    empresa_cnpj: int | None = None
    empresa_email: str | None = None
    empresa_senha: str | None = None