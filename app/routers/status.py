from fastapi import APIRouter

router = APIRouter()

@router.get("/api/status", summary="判断服务运行状态")
async def get_status():
    """
    判断服务是否正常运行
    """
    try:
        # 假设这里还可以加入更多判断逻辑，比如服务依赖检查
        return {"code": 200, "message": "OK"}
    except Exception as e:
        # 返回异常信息（简化处理）
        return {"code": 500, "message": f"Error: {str(e)}"}
