from rcon.source import Client
from jsonrpc import dispatcher
from typing import List


@dispatcher.add_method
def rcon_emit_cmd(ip: str, port: int, passwd: str, cmd: str, args: List) -> str:
    with Client(ip, port, passwd=passwd) as client:
        response = client.run(cmd, *args)

    return response
