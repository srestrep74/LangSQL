import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.modules.alerts.routes import router as alerts_router
from src.modules.auth.routes import router as auth_router
from src.modules.control_panel.routes import router as control_panel_router
from src.modules.queries.routes import router as queries_router
from src.modules.reports.routes import router as reports_router
from src.modules.text_to_sql.routes import router as text_to_sql_router

app = FastAPI(
    title="LangSQL",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(text_to_sql_router,
                   prefix="/api/text-to-sql", tags=["Text to SQL"])
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(alerts_router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(control_panel_router,
                   prefix="/api/control-panel", tags=["Control Panel"])
app.include_router(queries_router, prefix="/api/queries", tags=["Queries"])
app.include_router(reports_router, prefix="/api/reports", tags=["Reports"])


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
