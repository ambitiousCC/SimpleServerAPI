from fastapi import Depends, HTTPException, Header

from uuid import uuid4

from datetime import datetime, timedelta

# 存储用户凭证及有效期的全局字典
tokens = {}

def register_token(username: str) -> str:
    """
    注册用户凭证并设置有效时间为 2 小时
    """
    token = str(uuid4())  # 生成唯一 token
    expiry = datetime.now() + timedelta(hours=2)  # 设置有效时间为 2 小时
    tokens[token] = {"username": username, "expiry": expiry}
    return token

def validate_token(token: str) -> bool:
    """
    验证凭证是否有效
    """
    token_data = tokens.get(token)
    if not token_data:
        return False  # 凭证不存在
    if token_data["expiry"] < datetime.now():
        tokens.pop(token)  # 凭证过期，移除
        return False
    return True

async def verify_token(x_auth_token: str = Header(...)):
    """
    FastAPI 依赖：验证请求头中的 X-Auth-Token 凭证
    """
    if not validate_token(x_auth_token):
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return True
