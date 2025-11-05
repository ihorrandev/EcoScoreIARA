from fastapi import FastAPI
app = FastAPI()

from api.routes.company_routes import company_router
from api.routes.login_routes import login_router
from api.routes.questions_routes import pergunta_router
from api.routes.answer_routes import resposta_router
app.include_router(company_router)
app.include_router(login_router)
app.include_router(pergunta_router)
app.include_router(resposta_router)