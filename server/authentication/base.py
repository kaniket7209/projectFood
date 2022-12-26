from mongodb.base import executeMongoConfig,performAndClose

class vendorsData:
    def __init__(self):
        mongoConfig = executeMongoConfig()
        self.db = mongoConfig['db']
        self.client = mongoConfig['client']
        self.collection = self.db.vendors_data
        
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

    def save(self,email,phoneNo,password):
        def save_in_mongo(query,db):
            try:
                print("save is processing",phoneNo)
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
        print(email,password,phoneNo)
        is_present_response = self.is_already_present({"email":email})
        if is_present_response['error'] == True:
            return is_present_response 
        if is_present_response['length'] != 0:
            print(is_present_response,"--80")
            res = self.deleteFromDb({"email":email})
            # return  res

        query = {'email':email,'mobile_number':str(phoneNo),"password":password}
        saved_response  = save_in_mongo(query,self)
        # saved_response = performAndClose(save_in_mongo,self.client,self.db,query)
        return saved_response



def saveData(data):
    from passlib.hash import pbkdf2_sha256
    base = vendorsData()
    # encrypt password
    hash = pbkdf2_sha256.hash(data['password'])
    res = base.save(data['email'],data['mobile_number'],hash)
    return res

def validate(data,method):
    from passlib.hash import pbkdf2_sha256
    base = vendorsData()
    # get password 
    findEntries = base.is_already_present({'mobile_number':str(data['mobile_number'])}) if method == "number" else base.is_already_present({'email':str(data['email'])})
    hashPass = findEntries['data'][0]['password']
    # decrypt password
    password = pbkdf2_sha256.verify(data['password'],hashPass)
    if password != True:
        return {
            "msg":"Invalid credentials",
            "code":500,
            "error":True,
            "data":{}
        }
    findEntries['code']=200
    findEntries['error']=False
    findEntries['message']="Successfully logged in"
    return findEntries