from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def healthcheck():
    """
    Healthcheck endpoint to verify the service is running
    """
    return {"status": "ok"}
