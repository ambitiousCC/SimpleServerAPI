from fastapi import FastAPI
from app.routers import status, ticket, machine

app = FastAPI()

# 包含 /api/status 路由
app.include_router(status.router)
app.include_router(ticket.router)
app.include_router(machine.router)