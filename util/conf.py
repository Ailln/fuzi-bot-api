from ruamel.yaml import YAML

from util.arg import get_args

yaml = YAML()
args = get_args()


def read_yaml(yaml_path):
    with open(yaml_path, "r") as f_yaml:
        datas = yaml.load(f_yaml)
    return datas


def save_yaml(yaml_path, data):
    with open(yaml_path, "w") as f_yaml:
        yaml.dump(data, f_yaml)


def get_conf() -> dict:
    conf_data = read_yaml(args["conf"])
    conf_data["env"] = args["env"]
    return conf_data
