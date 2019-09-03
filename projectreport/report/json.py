import datetime
import json


def to_json(dict_: dict) -> str:

    def json_converter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    return json.dumps(dict_, default=json_converter, indent=2)
