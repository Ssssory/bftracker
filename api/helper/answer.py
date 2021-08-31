
class Answer():
    def success(rez,id):
        return {"jsonrpc": "2.0", "result": {"status": "success", "data": rez}, "id": id}

    def error(text,id):
        return {"jsonrpc": "2.0", "result": {"status": "error", "text": text}, "id": id}
