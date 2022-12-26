from mongodb.base import executeMongoConfig,performAndClose

class vendorsStore:
    def __init__(self,db,client,collection):
        # mongoConfig = executeMongoConfig()
        # self.db = mongoConfig['db']
        # self.client = mongoConfig['client']
        # self.collection = self.db.vendors_store_data
        # mongoConfig = executeMongoConfig()
        self.db = db
        self.client =client
        self.collection = collection
        
    def is_already_present(self,query):
        def is_present(query):
            try:
                data = list(self.collection.find(query,{"_id":0}))
                length = len(data)
                return {
                    'error':False,
                    'message':"",
                    'data':data,
                    'length':length,
                    'code':200
                }
            except Exception as e:
                return {
                    'error':False,
                    'message':"",
                    'data':data,
                    'code':500
                }
        response  = is_present(query)
        # response = performAndClose(is_present,self.client,self.db,query)
        return response
    
    
    def deleteFromDb(self,query):
        def delete(query):
            try:
                print("deletig")
                self.collection.delete_one(query)
                # print(self.collection,"--",query)
                return {
                    'error':False,
                    'message':self.collection,
                    'data':{},
                    'code':200
                }
            except Exception as e:
                return {
                    'error':True,
                    'message':"deleting",
                    'data':str(e),
                    'code':500
                }
        response  = delete(query)
        # response = performAndClose(delete,self.client,self.db,query)
        return response

    def save(self,query,mobile_number):
        def save_in_mongo(query,db):
            try:
                print("save is processing",mobile_number)
                self.collection.insert_one(query)
                return {
                    'error':False,
                    'message':"Succesfully saved data",
                    'data':{},
                    'code':200
                }
            except Exception as e:
                return {
                    'error':True,
                    'message':"",
                    'data':str(e),
                    'code':500
                }
       
        is_present_response = self.is_already_present({"mobile_number":mobile_number})
        if is_present_response['error'] == True:
            return is_present_response 
        if is_present_response['length'] != 0:
            print(is_present_response,"--80")
            res = self.deleteFromDb({"mobile_number":mobile_number})
            # return  res

        saved_response  = save_in_mongo(query,self)
        # saved_response = performAndClose(save_in_mongo,self.client,self.db,query)
        return saved_response



def saveData(data):
    mongoConfig = executeMongoConfig()
    db = mongoConfig['db']
    client = mongoConfig['client']
    collection = db.vendors_store_data
    base = vendorsStore(db,client,collection)
  
    res = base.save(data,data['mobile_number'])
    return res
def getVendorsData(mobile_no):
    mongoConfig = executeMongoConfig()
    db = mongoConfig['db']
    client = mongoConfig['client']
    collection = db.vendors_store_data
    base = vendorsStore(db,client,collection)
  
    res = base.is_already_present({'mobile_number':mobile_no})
    return res
    

def addProduct(data):
    
    store_data= getVendorsData(data['mobile_number'])['data']
    data['store_name'] = store_data[0]['store_name']
 
    mongoConfig = executeMongoConfig()
    db = mongoConfig['db']
    client = mongoConfig['client']
    collection = db.vendors_products
    base = vendorsStore(db,client,collection)
    res = base.save(data,data['mobile_number'])
    return res
