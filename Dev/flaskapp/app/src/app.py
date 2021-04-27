# https://www.digitalocean.com/community/tutorials/how-to-set-up-flask-with-mongodb-and-docker
# a = APPID = 0bb27904-1297-48d9-b649-1f1e098fd95f
# n = MAXOFFERS = 400
# i = 0
# sb = sortBY - EX
# so = sortOrder - asc
# https://bjs.apir.receiptiq.com/service/user/token?p=6cac42f3-36ac-4c4c-aac5-f63e6f2ae15c&s=120fb46d-ef6b-4ef1-8913-64c8e487c5da&u=08642403500&ut=LoyaltyNumber
# https://bjs.apir.receiptiq.com/service/offers/activated?t=e477faaf-87d3-4dea-bccc-76927f9c0f4d&a=0bb27904-1297-48d9-b649-1f1e098fd95f&n=400&i=0&sb=EX&so=asc
# filter="redeemable:yes"
# channel = Toshiba Vector
# transactionID
# zipcode
# offers - json

# https://bjs.apir.receiptiq.com/service/offers/redeem?t=17e25ecb-7e4f-4961-8b99-27efa410081f&a=0bb27904-1297-48d9-b649-1f1e098fd95f
# /service/user/register
# /service/user/profile
# /service/offers/recommended
# /service/offers/targeted
# /service/offers/activate
# /service/offers/activated
# /service/offers/redeem
# /service/offers/all


##TODO Set timeouts on connections
import os
from decimal import Decimal
from flask import Flask, request, jsonify
import boto3
import simplejson
import json
from boto3.dynamodb.conditions import Key, Attr
from flask import render_template
from flask import Flask, redirect, url_for, request
from datetime import datetime
from logging.config import dictConfig

application = Flask(__name__)
tableName = "members"
dynamodb = boto3.resource(
    "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
)
dynamo_client = boto3.client(
    "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
)


@application.route("/Redeem", defaults={"memberID": None, "offerID": None})
@application.route("/Redeem/<memberID>/<offerID>/<quantity>")
def offer_redeem(memberID, offerID, quantity=1):
    if not memberID:
        memberID = "USER#ddayley"
        dynamodb = boto3.resource(
            "dynamodb",
            region_name="us-west-1",
            endpoint_url="http://dynamodb-local:8000",
        )
        table = dynamodb.Table(tableName)
        # cDate = "2021-04-01"
        application.logger.info("Query is using %s ", memberID)
        response = table.query(
            TableName="members",
            IndexName="ActiveOffers",
            KeyConditionExpression=Key("PK").eq(memberID)
            & Key("EndDate").gte(20210404),
            FilterExpression=Attr("ActiveDate").gte(20210401)
            & Attr("Redeemed").ne("True"),
        )
        return render_template("redeem.html", offers=response["Items"])

    else:
        dynamodb = boto3.resource(
            "dynamodb",
            region_name="us-west-1",
            endpoint_url="http://dynamodb-local:8000",
        )
        table = dynamodb.Table(tableName)

        response = table.update_item(
            Key={"PK": memberID, "SK": offerID},
            UpdateExpression="set Redeemed = :val",
            ExpressionAttributeValues={":val": quantity},
            ReturnValues="UPDATED_NEW",
        )
        return jsonify(status=True, data=response)
    return "Error"


@application.route("/service/user/register", methods=["POST", "GET"])
def register_user(   zip="01748",):
    content = json.dumps(request.json)
    print("p0")
    request_json = request.get_json()
    memID = request_json.get("loyaltyNumber")
    address = request_json.get("address")
    zipCode = request_json.get("zip")
    # response_content = None

    if memID is not None:
        dynamodb = boto3.resource(
            "dynamodb",
            region_name="us-west-1",
            endpoint_url="http://dynamodb-local:8000",
        )
        application.logger.info("Posting Data %s ", memID)
        table = dynamodb.Table(tableName)
        now = datetime.now()
        current_time = now.strftime("%Y/%m/%d, %H:%M:%S")
        if request.method == "POST":
            response = table.put_item(
            Item={
                "PK": "USER#",
                "SK": "#PROFILE#" + memID,
                "Address": "None",
                "Zip": "None",
                "LastUpdatedDate": current_time,

            }
        )
        return str("mem: " + memID) + str(request.query_string)
    return str(request.query_string) + str(contet)
    #     print("p3")
    #     cursor.execute("INSERT INTO person (first_name,last_name) VALUES (%s,%s)", (value1, value2))
    #     response_content = conn.commit()


#     {
#    "errorCode": "4224",
#    "errorDescription": "Loyalty Number is already registered for another user"
#    }
# "POST /service/user/register?p=6cac42f3-36ac-4c4c-aac5-f63e6f2ae15c&s=120fb46d-ef6b-4ef1-8913-64c8e487c5da&a=08ec9c95-d398-40bb-a139-19f1c0c42267


@application.route("/")
@application.route("/hello/<name>")
def hello(name=None):
    return render_template("index.html", name=name)


@application.route("/ActiveOffers")
@application.route("/ActiveOffers/<offerID>")
def ActiveOffers(offerID=None):
    offerID = "BJ#OFFER"
    application.logger.info("Query is using %s ", offerID)
    table = dynamodb.Table(tableName)
    dynamo_client = boto3.client(
        "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
    )
    response = table.query(
        TableName="members",
        IndexName="ActiveOffers",
        KeyConditionExpression=Key("PK").eq(offerID) & Key("EndDate").gte(20210404),
        FilterExpression=Attr("ActiveDate").gte(20210401) & Attr("Redeemed").ne("True"),
    )
    return render_template("offers.html", offers=response["Items"])
@application.route("/Members")
@application.route("/Members/<memID>")
def Members(memID=None):
    PK = "USER#"
    application.logger.info("Query is using %s ", memID)
    table = dynamodb.Table(tableName)
    dynamo_client = boto3.client(
        "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
    )
    response = table.query(
        TableName="members",
        #IndexName="ActiveOffers",
        KeyConditionExpression=Key("PK").eq("USER#") & Key("SK").begins_with("#PROFILE#"),
        #FilterExpression=Attr("ActiveDate").gte(20210401) & Attr("Redeemed").ne("True"),
    )
    return render_template("members.html", offers=response["Items"])


@application.route("/dbdetails")
def list_table():
    dynamo_client = boto3.client(
        "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
    )

    tables = dynamo_client.list_tables()
    # partitions = dynamo_client.get_partitions()
    # pindexes = get_partition_indexes(    DatabaseName='string',  TableName='members',)
    return render_template("dbdetails.html", tableNames=tables)


@application.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("success", name=user))
    else:
        user = request.args.get("nm")
        return redirect(url_for("success", name=user))


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
        application.logger.error("Error - Resource does not exist!")
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
                "IndexName": "MemberOffers",
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


@application.route("/register", methods=["POST", "GET"])
def create_member():
    dynamodb = boto3.resource(
        "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
    )
    application.logger.info("Posting Data %s ", request.form["SK"])
    table = dynamodb.Table(tableName)
    now = datetime.now()
    current_time = now.strftime("%Y/%m/%d, %H:%M:%S")
    if request.method == "POST":
        response = table.put_item(
            Item={
                "PK": request.form["PK"],
                "SK": request.form["SK"],
                "Email": request.form["Email"],
                "LastUpdatedDate": current_time,
                "ActiveDate": int(request.form["ActiveDate"]),
                "EndDate": int(request.form["EndDate"]),
            }
        )
    return jsonify(status=True, data=response)


@application.route("/createoffer", methods=["POST", "GET"])
def create_offer():
    # if not dynamodb:
    dynamodb = boto3.resource(
        "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
    )
    table = dynamodb.Table(tableName)
    if request.method == "POST":
        application.logger.info("Posting Data %s ", request.form["SK"])
        now = datetime.now()
        current_time = now.strftime("%Y/%m/%d %H:%M:%S")
        response = table.put_item(
            Item={
                "PK": request.form["PK"],
                "SK": request.form["SK"],
                "OfferCode": request.form["OfferCode"],
                "OfferType": request.form["OfferType"],
                "OfferID": request.form["OfferID"],
                "LastUpdatedDate": current_time,
                "ActiveDate": int(request.form["ActiveDate"]),
                "EndDate": int(request.form["EndDate"]),
            }
        )
        application.logger.info("Posting Data Complete")
    return jsonify(status=True, data=response)


@application.route("/MemberOffers/<name>")
@application.route("/MemberOffers")
def getMemberOffers(name=None):
    dynamodb = boto3.resource(
        "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
    )
    table = dynamodb.Table(tableName)
    cDate = "2021-04-01"
    if not name:
        memberID = "USER#ddayley"
    else:
        memberID = "USER#" + name
    application.logger.info("Query is using %s ", memberID)
    response = table.query(
        TableName="members",
        IndexName="ActiveOffers",
        KeyConditionExpression=Key("PK").eq(memberID) & Key("EndDate").gte(20210404),
        FilterExpression=Attr("ActiveDate").gte(20210401) & Attr("Redeemed").ne("True"),
    )
    ##TODO Add Category hierachy to PK
    ##TODO Filter out the upcoming offers
    ##TODO Filter out Redeemed offers
    ##TODO Update Redeemed Flag - Read about locking and GSI
    return render_template("query.html", offers=response["Items"])
    # return simplejson.dumps(response["Items"]), 201
    # jsonify(status=True, message=response), 201


@application.route("/createsampledata")
def sampledata(name=None):
    now = datetime.now()
    current_time = now.strftime("%Y/%m/%d %H:%M:%S")
    dynamo_client = boto3.client(
        "dynamodb", region_name="us-west-1", endpoint_url="http://dynamodb-local:8000"
    )

    table = dynamodb.Table(tableName)
    response = table.put_item(
        # MEMBER ENTITY
        Item={
            "PK": "USER#sample",
            "SK": "#PROFILE#sample",
            "Email": "ddayley@bjs.com",
            "LastUpdatedDate": current_time,
            "ActiveDate": 20210401,
            "EndDate": 20210405,
        }
    )
    response = table.put_item(
        # MEMBER/OFFER
        Item={
            "PK": "USER#ddayley",
            # "SK": "2021-04-05",
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
        # OFFER ENTITY
        Item={
            "PK": "BJ#OFFER",
            "SK": "OFFER#bounty",
            "OfferCode": "21474008",
            "OfferType": "Recommended",
            "OfferID": "d517d523-a6d4-4f47-8e5d-c7e7f052bf11",
            "LastUpdatedDate": "04-01-21",
            "ActiveDate": 20210401,
            "EndDate": 20210405,
        }
    )

    return jsonify(status=True, data=response)


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host="0.0.0.0", port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)