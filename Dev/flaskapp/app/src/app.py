# https://www.digitalocean.com/community/tutorials/how-to-set-up-flask-with-mongodb-and-docker
import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import boto3
from boto3.dynamodb.conditions import Key

application = Flask(__name__)
tableName = "users"

# #application.config["MONGO_URI"] = (
#     "mongodb://"
#     + os.environ["MONGODB_USERNAME"]
#     + ":"
#     + os.environ["MONGODB_PASSWORD"]
#     + "@"
#     + os.environ["MONGODB_HOSTNAME"]
#     + ":27017/"
#     + os.environ["MONGODB_DATABASE"]
#)

# mongo = PyMongo(application)
# db = mongo.db
dynamo_client = boto3.client(
    "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
)


@application.route("/")
def index():
    return jsonify(
        status=True, message="DD- Welcome to the Dockerized Flask MongoDB app!"
    )


@application.route("/inittable")
def init_table():
    # Get the service resource.
    # Create the DynamoDB table.
    dynamo_client = boto3.resource(
        "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
    )

    table = dynamo_client.Table(tableName)
    table.delete()
    table = dynamo_client.create_table(
        TableName=tableName,
        KeySchema=[
            {"AttributeName": "username", "KeyType": "HASH"},
            {"AttributeName": "last_name", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "username", "AttributeType": "S"},
            {"AttributeName": "last_name", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    # Wait until the table exists.
    table.meta.client.get_waiter("table_exists").wait(TableName=tableName)
    # Print out some data about the table.
    return jsonify(status=True, message="table.item_count")


@application.route("/createitem")
def create_item():
    # if not dynamodb:
    dynamodb = boto3.resource(
        "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
    )

    table = dynamodb.Table(tableName)
    response = table.put_item(Item={"username": "Don", "last_name": "Dayley"})
    return jsonify(status=True, data=response)


# @application.route("/todo")
# def todo():
#     _todos = db.todo.find()

#     item = {}
#     data = []
#     for todo in _todos:
#         item = {"id": str(todo["_id"]), "todo": todo["todo"]}
#         data.append(item)

#     return jsonify(status=True, data=data)


# @application.route("/todo", methods=["POST"])
# def createTodo():
#     data = request.get_json(force=True)
#     item = {"todo": data["todo"]}
#     db.todo.insert_one(item)

#     return jsonify(status=True, message="To-do saved successfully!"), 201


@application.route("/items")
def get_items():
    dynamodb = boto3.resource(
        "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
    )
    table = dynamodb.Table(tableName)
    response = table.scan()
    # data = response['Items']

    # while 'LastEvaluatedKey' in response:
    #    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    #    data.extend(response['Items'])
    # response = table.query(
    #     KeyConditionExpression=Key('username').eq('HASH')
    # )
    # list = [(k, v) for k, v in response.items()]
    return jsonify(status=True, message=response), 201


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host="0.0.0.0", port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
