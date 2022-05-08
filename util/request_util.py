from requests import get, post

from util.conf_util import get_conf

conf = get_conf()
nlu_url = conf["nlu"]["url"]


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


async def get_questions():
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
