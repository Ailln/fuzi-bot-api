from aiohttp import web
from socketio import AsyncServer

from util.log import get_logger
from util.conf import get_conf
from util.request import post_search, post_nlu

logger = get_logger("server.main", is_save_file=True)

app = web.Application()
sio = AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
sio.attach(app)

conf = get_conf()
answer_dict = conf["nlg"]["answer"]


@sio.on("chat-request")
async def chat_index(sid, data):
    logger.info(f"chat-request # data # {sid}: {data}")
    try:
        messages = data["messages"]
        content = None
        for message in reversed(messages):
            if message["role"] == "user":
                content = message["content"]
                break

        if content is not None:
            result = await post_search(content)
            if len(result) == 1:
                intent = result[0]["intent"]
            else:
                intent = await post_nlu(content)
            answer = {
                "role": "assistant",
                "content": answer_dict[intent]
            }
            logger.info(f"chat-request # answer # {sid}: {answer}")
            await sio.emit(event="chat-reply", data=answer, to=sid)
        else:
            raise ValueError("no user message")

    except Exception as e:
        logger.error(str(e))
        await sio.emit(event="error", data=str(e), to=sid)


if __name__ == "__main__":
    web.run_app(app, **conf["app"]["run"])
