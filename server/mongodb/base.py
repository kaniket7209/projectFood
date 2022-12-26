from pymongo import MongoClient

def executeMongoConfig():
    client = MongoClient("mongodb+srv://niklite:niklite@cluster0.8sfpess.mongodb.net/test")
    db = client.cloudbelly
    return { 
        'db':db,
        'client':client
    }
    
def performAndClose(perform_operation,client,mongoConfigDB,data = None):
    
    all_data = perform_operation(data,mongoConfigDB)
    client.close()
    return all_data



# executeMongoConfig()

# print("Connection Successful")




# db=client.admin
# col = db.sample_collection
# col.insert_one({'hello':'Amazon DocumentD'})
# x = col.find_one({'hello':'Amazon DocumentD'})
# print(x)


# serverStatusResult=db.command("serverStatus")

# print(serverStatusResult)


    