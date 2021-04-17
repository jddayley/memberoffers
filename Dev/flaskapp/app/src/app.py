# https://www.digitalocean.com/community/tutorials/how-to-set-up-flask-with-mongodb-and-docker
import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import boto3
import simplejson
from boto3.dynamodb.conditions import Key

application = Flask(__name__)
tableName = "members"

dynamo_client = boto3.client(
    "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
)


@application.route("/")
def index():
    return jsonify(status=True, message="Welcome to the Dockerized Flask MongoDB app!")


@application.route("/inittable")
def init_table():
    # Get the service resource.
    dynamo_client = boto3.resource(
        "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
    )
    # Delete the table before creating it.
    table = dynamo_client.Table(tableName)
    try:
        table.delete()
    except:
        print("error happened")
     # Create the DynamoDB table.
    table = dynamo_client.create_table(
        TableName=tableName,
        KeySchema=[
            {"AttributeName": "PK", "KeyType": "HASH"},
            {"AttributeName": "SK", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "PK", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"},
            # {"AttributeName": "memberID", "AttributeType": "N"},
            # {"AttributeName": "email", "AttributeType": "S"},
            # {"AttributeName": "createdDate", "AttributeType": "N"},
            # {"AttributeName": "lastUpdateDate", "AttributeType": "N"},
            # {"AttributeName": "offerCode", "AttributeType": "S"},
            # {"AttributeName": "offerID", "AttributeType": "S"},
            # {"AttributeName": "startDate", "AttributeType": "N"},
            {"AttributeName": "EndDate", "AttributeType": "N"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        LocalSecondaryIndexes=[
            {
                "IndexName": "OffersByEndDate",
                "KeySchema": [
                    {"AttributeName": "PK", "KeyType": "HASH"},  # Partition key
                    {"AttributeName": "EndDate", "KeyType": "RANGE"},  # Sort key
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
    )

    # Wait until the table exists.
    table.meta.client.get_waiter("table_exists").wait(TableName=tableName)
    # Print out some data about the table.
    return jsonify(status=True, message="table.item_count")


@application.route("/createmember")
def create_member():
    # if not dynamodb:
    dynamodb = boto3.resource(
        "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
    )
    table = dynamodb.Table(tableName)
    response = table.put_item(
        Item={
            "PK": "USER#ddayley",
            "SK": "#PROFILE#ddayley",
            "Email": "ddayley@bjs.com",
            "EndDate": 20210401,
        }
    )
    return jsonify(status=True, data=response)


@application.route("/createoffer")
def create_offer():
    # if not dynamodb:
    dynamodb = boto3.resource(
        "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
    )
    table = dynamodb.Table(tableName)
    response = table.put_item(
        Item={
            "PK": "USER#ddayley",
            "SK": "OFFER#bounty",
            "OfferCode": "21474008",
            "OfferType": "Recommended",
            "OfferID": "d517d523-a6d4-4f47-8e5d-c7e7f052bf11",
            "LastUpdatedDate": "04-01-21",
            "StartDate": "2021-04-01",
            "EndDate": 20210401,
        }
    )
    return jsonify(status=True, data=response)

@application.route("/items")
def get_items():
    dynamodb = boto3.resource(
        "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
    )
    table = dynamodb.Table(tableName)
    cDate = "2021-04-01"
    memberID = "USER#ddayley"
    response = table.query(
        TableName="users",
        IndexName="OffersByEndDate",
        KeyConditionExpression=Key("PK").eq("USER#ddayley")
        & Key("EndDate").eq(20210401),
    )
    #print(response)
    return simplejson.dumps(response['Items']), 201
    # jsonify(status=True, message=response), 201


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host="0.0.0.0", port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)