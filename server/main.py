import re

from aiohttp import web
from socketio import AsyncServer

from util.log_util import get_logger
from util.conf_util import get_conf
from util.request_util import post_search, post_nlu, get_questions

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
        if "@@" in data:
            model_type, _msg = data.split("@@")
            if model_type in ["JointNLU", "ChatGLM-6B", "ChatGPT"]:
                data = _msg
            else:
                raise Exception(f"model type {model_type} not found!")

        result = await post_search(data)
        if len(result) == 1:
            intent = result[0]["intent"]
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
        index = 0
        if len(data) <= 2:
            questions = get_questions()
            for item in re.finditer(fr"^{data}.*", "\n".join(questions), re.MULTILINE):
                index += 1
                if index <= max_suggestion_number:
                    suggestion_list.append(item.group())
                else:
                    break
        else:
            for item in await post_search(data, 0.8, max_suggestion_number):
                suggestion_list.append(item["question"])

        logger.info(f"suggest-request # suggest_list: {suggestion_list}")
        await sio.emit(event="suggest-reply", data=suggestion_list, to=sid)
    except Exception as e:
        logger.error(str(e))
        await sio.emit(event="error", data=str(e), to=sid)


if __name__ == "__main__":
    web.run_app(app, host=conf["app"]["host"], port=conf["app"]["port"])
