from src.rcon_emit_cmd import rcon_emit_cmd
from jsonrpc import dispatcher, JSONRPCResponseManager
import json


async def read_body(receive):
    """
    Read and return the entire body from an incoming ASGI message.
    """
    body = b""
    more_body = True

    while more_body:
        message = await receive()
        body += message.get("body", b"")
        more_body = message.get("more_body", False)

    return body


async def app(scope, receive, send):
    assert scope["type"] == "http"

    body = await read_body(receive)

    response = JSONRPCResponseManager.handle(body, dispatcher)
    response_str = json.dumps(response.data).encode()

    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                (b"content-type", b"text/plain"),
                (b"content-length", str(len(response_str)).encode()),
            ],
        }
    )

    await send(
        {
            "type": "http.response.body",
            "body": response_str,
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=5000, reload=True, log_level="info")
