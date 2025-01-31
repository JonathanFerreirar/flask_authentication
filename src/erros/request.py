ERRO_MISS_BODY = {"error": "badRequest",
                  "msg": "Check if you pass the correctly propertys on the request body.."}, 400

ERRO_BAD_REQUEST = {"error": "badRequest",
                    "msg": "property not found or cannot be changed."}, 400


def ERRO_NOT_FOUND(assumption: str):
    return {"error": "notFound",
            "msg": f"{assumption} not found."}, 404


def ERRO_ALREDY_EXIST(assumption: str):
    return {"error": "conflict",
            "msg": f"Alredy existe this {assumption}"}, 409
