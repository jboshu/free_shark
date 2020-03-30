import json

def make_json(code,msg,entity=None):
    if entity != None:
        t = {
            'code':code,
            'msg':msg,
            'entity': entity
        }
    else:
        t = {
            'code':code,
            'msg':msg
        }
    return json.dumps(t)
