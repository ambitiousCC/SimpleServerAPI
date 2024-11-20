from fastapi import Depends, HTTPException, Header

from uuid import uuid4

from datetime import datetime, timedelta

import redis
from datetime import datetime, timedelta
import json

# Redis 配置
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

TOKEN_EXPIRY_SECONDS = 2 * 60 * 60  # 凭证有效期：2 小时

def register_token(username: str) -> str:
    """
    注册用户凭证并设置有效时间为 2 小时
    """
    token = str(uuid4())  # 生成唯一 token
    expiry_time = datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRY_SECONDS)  # 设置有效时间为 2 小时

    # 将凭证信息存储到 Redis
    redis_client.setex(f"token:{token}", TOKEN_EXPIRY_SECONDS, json.dumps({
        "username": username,
        "expiry": expiry_time.isoformat()  # 以 ISO 格式存储
    }))
    return token

def validate_token(token: str) -> bool:
    """
    验证 Redis 中存储的凭证是否有效
    """
    token_data = redis_client.get(f"token:{token}")
    if not token_data:
        return False  # 凭证不存在或已过期

    # 解析存储的凭证数据
    token_data = json.loads(token_data)
    expiry_time = datetime.fromisoformat(token_data["expiry"])
    if expiry_time < datetime.utcnow():
        return False  # 凭证已过期
    return True

async def verify_token(x_auth_token: str = Header(...)):
    """
    FastAPI 依赖：验证请求头中的 X-Auth-Token 凭证
    """
    if not validate_token(x_auth_token):
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return True
