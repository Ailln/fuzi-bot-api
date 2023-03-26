import os
from requests import get, post

from util.conf_util import get_conf

conf = get_conf()

search_host = os.environ.get("FUZI_SEARCH_SERVICE_HOST")
search_port = os.environ.get("FUZI_SEARCH_SERVICE_PORT")
if search_host and search_port:
    search_url = f"http://{search_host}:{search_port}"
else:
    search_url = conf["search"]["url"]

nlu_host = os.environ.get("FUZI_NLU_SERVICE_HOST")
nlu_port = os.environ.get("FUZI_NLU_SERVICE_PORT")
if nlu_host and nlu_port:
    nlu_url = f"http://{nlu_host}:{nlu_port}"
else:
    nlu_url = conf["nlu"]["url"]


async def post_search(question, threshold=0.9, limit=1):
    res = post(f"{search_url}/search", json={"question": question, "threshold": threshold, "limit": limit})
    if res.status_code == 200:
        res_data = res.json()
        if res_data["status"] == 1:
            result = res_data["data"]["result"]
        else:
            raise Exception(res_data["message"])
    else:
        raise Exception(f"post search request failed! code {res.status_code}")

    return result


async def post_nlu(question):
    res = post(f"{nlu_url}/nlu", json={"question": question})
    if res.status_code == 200:
        res_data = res.json()
        if res_data["status"] == 1:
            intent = res_data["data"]["intent"]
        else:
            raise Exception(res_data["message"])
    else:
        raise Exception(f"post nlu request failed! code {res.status_code}")

    return intent


def get_questions():
    res = get(f"{nlu_url}/questions")
    if res.status_code == 200:
        res_data = res.json()
        if res_data["status"] == 1:
            questions = res_data["data"]
        else:
            raise Exception(res_data["message"])
    else:
        raise Exception(f"get questions request failed! code {res.status_code}")

    return questions
