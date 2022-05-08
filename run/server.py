import re

from aiohttp import web
from socketio import AsyncServer
from cn2an import transform

from util.log_util import get_logger
from util.conf_util import get_conf
from util.request_util import post_nlu, get_questions

conf = get_conf()
logger = get_logger(__name__)
app = web.Application()
sio = AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
sio.attach(app)

max_suggestion_number = conf["nlu"]["max_suggestion_number"]
answer_dict = conf["nlg"]["answer"]


@sio.on("chat-request")
async def chat_index(sid, data):
    logger.info(f"chat-request # question: {data}")
    try:
        if ":" in data:
            mode, _msg = data.split(":")
            if mode in ["cn2an", "an2cn"]:
                answer = f"{transform(_msg, mode)}【by {mode}】"
            else:
                intent = await post_nlu(data)
                answer = answer_dict[intent]
        else:
            intent = await post_nlu(data)
            answer = answer_dict[intent]

        logger.info(f"chat-request # answer: {answer}")
        await sio.emit(event="chat-reply", data=answer, to=sid)
    except Exception as e:
        logger.error(str(e))
        await sio.emit(event="error", data=str(e), to=sid)


@sio.on("suggest-request")
async def suggest_index(sid, data):
    logger.info(f"suggest-request # question: {data}")
    try:
        suggestion_list = []
        questions = await get_questions()
        index = 0
        for item in re.finditer(fr"^{data}.*", "\n".join(questions), re.MULTILINE):
            index += 1
            if index <= max_suggestion_number:
                suggestion_list.append(item.group())
            else:
                break

        logger.info(f"suggest-request # suggest_list: {suggestion_list}")
        await sio.emit(event="suggest-reply", data=suggestion_list, to=sid)
    except Exception as e:
        logger.error(str(e))
        await sio.emit(event="error", data=str(e), to=sid)


if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)
