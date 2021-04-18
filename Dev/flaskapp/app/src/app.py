# https://www.digitalocean.com/community/tutorials/how-to-set-up-flask-with-mongodb-and-docker
#a = APPID = 0bb27904-1297-48d9-b649-1f1e098fd95f
#n = MAXOFFERS = 400
#i = 0
#sb = sortBY - EX
#so = sortOrder - asc
#https://bjs.apir.receiptiq.com/service/user/token?p=6cac42f3-36ac-4c4c-aac5-f63e6f2ae15c&s=120fb46d-ef6b-4ef1-8913-64c8e487c5da&u=08642403500&ut=LoyaltyNumber
#https://bjs.apir.receiptiq.com/service/offers/activated?t=e477faaf-87d3-4dea-bccc-76927f9c0f4d&a=0bb27904-1297-48d9-b649-1f1e098fd95f&n=400&i=0&sb=EX&so=asc
#filter="redeemable:yes"
#channel = Toshiba Vector
#transactionID 
#zipcode
#offers - json

#https://bjs.apir.receiptiq.com/service/offers/redeem?t=17e25ecb-7e4f-4961-8b99-27efa410081f&a=0bb27904-1297-48d9-b649-1f1e098fd95f


##TODO Set timeouts on connections
import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import boto3
import simplejson
from boto3.dynamodb.conditions import Key

application = Flask(__name__)
tableName = "members"
dynamodb = boto3.resource(
    "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
)
dynamo_client = boto3.client(
    "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
)


@application.route("/")
def index():
    return jsonify(status=True, message="Welcome to the Dockerized Flask DynamoDB app!")


@application.route("/listtables")
def list_table():
    response = boto3.client(
        "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
    ).list_tables()
    return jsonify(status=True, message=response)


@application.route("/inittable")
def init_table():
    try:
        dynamo_client = boto3.client(
            "dynamodb",
            region_name="us-west-1",
            endpoint_url="http://dynamodb-local:8000",
        )
        response = dynamo_client.delete_table(TableName="members")
    except:
        print("Error - Resource Does not exist!")
    # Create the DynamoDB table.
    table = dynamo_client.create_table(
        TableName="members",
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
            # {"AttributeName": "Redeemed", "AttributeType": "B"},
            {"AttributeName": "ActiveDate", "AttributeType": "N"},
            {"AttributeName": "EndDate", "AttributeType": "N"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        LocalSecondaryIndexes=[
            {
                "IndexName": "ActiveOffers",
                "KeySchema": [
                    {"AttributeName": "PK", "KeyType": "HASH"},  # Partition key
                    {"AttributeName": "EndDate", "KeyType": "RANGE"},  # Sort key
                
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
            {
                "IndexName": "OffersByStartDate",
                "KeySchema": [
                    {"AttributeName": "PK", "KeyType": "HASH"},  # Partition key
                    {"AttributeName": "ActiveDate", "KeyType": "RANGE"},  # Sort key
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
    )

    # Wait until the table exists.
    # table.meta.client.get_waiter("table_exists").wait(TableName=tableName)
    # Print out some data about the table.
    return "Table created"


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
            "ActiveDate": 20210401,
            "EndDate": 20210405,
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
            "ActiveDate": 20210401,
            "EndDate": 20210405,
        }
    )
    response = table.put_item(
        Item={
            "PK": "USER#ddayley",
            "SK": "OFFER#tide",
            "OfferCode": "21474008",
            "OfferType": "Recommended",
            "OfferID": "e517d523-a6d4-4f47-8e5d-c7e7f052bf11",
            "Redeemed": "False",
            "LastUpdatedDate": "04-01-21",
            "ActiveDate": 20210401,
            "EndDate": 20210405,
        }
    )
    # esponse = table.put_item(
    #     Item={
    #         "PK": "USER#ndayley",
    #         "SK": "OFFER#tide",
    #         "OfferCode": "21474008",
    #         "OfferType": "Recommended",
    #         "OfferID": "e517d523-a6d4-4f47-8e5d-c7e7f052bf11",
    #         "LastUpdatedDate": "04-01-21",
    #         "ActiveDate": 20210401,
    #         "EndDate": 20210405,
    #     }
    # )
    return jsonify(status=True, data=response)


@application.route("/getActiveOffers")
def getActiveOffers():
    dynamodb = boto3.resource(
        "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
    )
    table = dynamodb.Table(tableName)
    cDate = "2021-04-01"
    memberID = "USER#ddayley"
    response = table.query(
        TableName="members",
        IndexName="ActiveOffers",
        KeyConditionExpression=Key("PK").eq("USER#ddayley")
        & Key("EndDate").gt(20210407),
    )
    ##TODO Filter out the upcoming offers
    return simplejson.dumps(response["Items"]), 201
    # jsonify(status=True, message=response), 201


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host="0.0.0.0", port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)