
def base(function,payload):
    if function.lower() == "vendors":
        from store.db import saveData
        return saveData(payload)
    if function.lower() == "add-product":
        from store.db import addProduct
        return addProduct(payload)
    else:
        return {
            "code":404,
            "msg":"Method not found",
            "error":True,
            "data":{}
        }
    