from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)


try: 
  mongo = pymongo.MongoClient(
    host='localhost', 
    port=27017, 
    serverSelectionTimeoutMS = 1000
  )
  db = mongo.company
  mongo.server_info() # trigger exception if cannot connect to database
except:
  print("ERROR - Cannot connect to db")

#====================================
@app.route("/users", methods=["GET"])
def get_user():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        # print(data)
        return Response(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
      )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "cannot get user"}),
            status=400,
            mimetype='application/json'
      )
      
#====================================
@app.route("/users", methods=["POST"])
def create_user():
    try:
        user = {
            "name":request.form["name"], 
            "lastName":request.form["lastName"]
        }
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
        # for attr in dir(dbResponse):
        #   print(attr)
        return Response(
          response=json.dumps({
              "message": "user created", 
              "id": f"{dbResponse.inserted_id}"
          }),
          status=200,
          mimetype='application/json'
        )
    except Exception as ex:
        print("******")
        print(ex)
        print("******")


#====================================
@app.route("/users/<id>", methods=["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set":{"name": request.form["name"]}}
        )
        # for attr in dir(dbResponse):
        #     print(f"*****{attr}*****")
        if dbResponse.modified_count == 1:
            return Response(
                response=json.dumps({
                  "message": "user updated", 
                  # "id": f"{dbResponse.inserted_id}"
                }),
                status=200,
                mimetype='application/json'
            )
        else: 
            return Response(
                response=json.dumps({
                  "message": "nothing to update", 
                  # "id": f"{dbResponse.inserted_id}"
                }),
                status=200,
                mimetype='application/json'
            )
    except Exception as ex:
        print("******")
        print(ex)
        print("******")
        return Response(
            response=json.dumps({"message": "Error: Cannot update user"}),
            status=400,
            mimetype='application/json'
        )


#====================================
@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id": ObjectId(id)})
        # for attr in dir(dbResponse):
        #     print(f"*****{attr}*****")
        if dbResponse.deleted_count == 1:
            return Response(
                response=json.dumps({
                    "message": "user deleted", 
                    "id": f"{id}"
                }),
                status=200,
                mimetype='application/json'
            )
        return Response(
            response=json.dumps({
                "message": "user not found", 
                "id": f"{id}"
            }),
            status=200,
            mimetype='application/json'
        )
    except Exception as ex:
        print("******")
        print(ex)
        print("******")
        return Response(
            response=json.dumps({"message": "Error: Cannot delete user"}),
            status=400,
            mimetype='application/json'
        )


#====================================
if __name__ == "__main__":
    app.run(port=5555, debug=True)
print('x')