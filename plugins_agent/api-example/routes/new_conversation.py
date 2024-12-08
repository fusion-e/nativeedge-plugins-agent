from fastapi import APIRouter

router = APIRouter(prefix="/rest/v1", tags=["New Conversation"])


# 5. Start a New Chat Session
@router.post("/new-conversation")
async def start_new_conversation():
    """
    Start a new chat session
    """
    return {}
