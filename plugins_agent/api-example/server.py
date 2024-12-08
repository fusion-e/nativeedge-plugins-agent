from fastapi import FastAPI
from routes.conversation import router as conversation_router
from routes.new_conversation import router as new_conversation_router

app = FastAPI()

# Register routers
app.include_router(conversation_router)
app.include_router(new_conversation_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
