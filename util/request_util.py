import os
from requests import get, post

from util.conf_util import get_conf

conf = get_conf()
search_url = os.environ.get("FUZI_SEARCH_URL", conf["search"]["url"])
nlu_url = os.environ.get("FUZI_NLU_URL", conf["nlu"]["url"])


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
