from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, Response
import requests

app = FastAPI()

@app.post("/v1/chat/completions")
async def proxy_chat(request: Request):
    body = await request.body()
    headers = {
        "User-Agent": "opencode/1.0.0",
        "Authorization": "Bearer public",
        "Content-Type": "application/json",
        "x-opencode-client": "desktop"
    }
    url = "https://opencode.ai/zen/v1/chat/completions"
    
    try:
        response = requests.post(url, headers=headers, data=body, timeout=60, stream=True)
        return StreamingResponse(
            response.iter_content(chunk_size=1024), 
            status_code=response.status_code, 
            media_type=response.headers.get("Content-Type", "text/event-stream")
        )
    except Exception as e:
        return Response(content=str(e), status_code=500)
