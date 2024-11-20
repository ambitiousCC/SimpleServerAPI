from fastapi import APIRouter, HTTPException, Depends, Header
import json
from pathlib import Path
from app.middlewares.auth import verify_token

router = APIRouter()

# 本地存储的机器信息文件
MACHINE_DATA_FILE = Path("data/machines.json")

# 确保机器信息文件存在
MACHINE_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
if not MACHINE_DATA_FILE.exists():
    MACHINE_DATA_FILE.write_text(json.dumps([]))  # 初始化为空列表


def read_machines():
    """读取本地存储的机器信息"""
    with open(MACHINE_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/api/info", summary="获取所有可用机器信息", dependencies=[Depends(verify_token)])
async def get_all_machines():
    """
    获取所有可用机器信息
    """
    try:
        machines = read_machines()
        return {"data": machines}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve machines: {str(e)}")
