import hashlib
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.middlewares.auth import register_token, verify_token

from uuid import uuid4

router = APIRouter()

# 本地存储的用户数据文件
USER_DATA_FILE = Path("data/users.json")

# 确保用户数据文件存在
USER_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
if not USER_DATA_FILE.exists():
    USER_DATA_FILE.write_text(json.dumps({}))  # 初始化为空字典

def read_users():
    """读取本地存储的用户数据"""
    with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def write_users(users):
    """写入本地用户数据"""
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)


def find_user(username: str):
    """根据用户名查找用户"""
    users = read_users()
    for user in users:
        if user["username"] == username:
            return user
    return None


def hash_password(password: str) -> str:
    """计算密码的 MD5 哈希"""
    return hashlib.md5(password.encode()).hexdigest()

@router.post("/api/ticket", summary="验证账户合法性并注册会话")
async def validate_user(data: dict):
    """
    请求体格式:
    {
        "username": "user1",
        "password": "A1B2C3D4E5F6G7H8I9HD"  # MD5 哈希值
    }
    """
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        raise HTTPException(status_code=400, detail="Invalid request: missing username or password")

    user = find_user(username)

    if user and user["password"] == password:
        # 注册并返回会话 token
        token = register_token(username)
        return JSONResponse({
            "data": {
                "CSRFPreventionToken": str(uuid4()),  # 另一个唯一 token
                "ticket": token
            }
        })
    else:
        # 登录失败
        return JSONResponse({"data": ""}, status_code=401)
