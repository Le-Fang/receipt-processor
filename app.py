from flask import Flask, request, jsonify
from marshmallow import ValidationError
import uuid
from schemas import ReceiptSchema, ItemSchema
from datetime import datetime
import math

app = Flask(__name__)

# In-memory storage for receipts
receipts_db = {}

receipt_schema = ReceiptSchema()

@app.route("/receipts/process", methods=["POST"])
def process_receipt():
    try:
        data = receipt_schema.load(request.json)  # Validate request body
    except ValidationError as err:
        return jsonify({"error": "The receipt is invalid."}), 400  # BadRequest

    receipt_id = str(uuid.uuid4())  # Generate unique receipt ID
    data["points"] = -1 # Unprocessed receipt
    receipts_db[receipt_id] = data  # Store data

    return jsonify({"id": receipt_id}), 200

@app.route("/receipts/<string:id>/points", methods=["GET"])
def get_receipt_points(id):
    if id not in receipts_db:
        return jsonify({"error": "No receipt found for that ID."}), 404  # NotFound

    # Get receipt data
    data = receipts_db[id]

    # If points have already been calculated, return it
    if data["points"] != -1:
        return jsonify({"points": data["points"]}), 200

    # Calculate points
    points = calculate_points(data)

    return jsonify({"points": points}), 200

def calculate_points(data):
    points = 0

    # One point for every alphanumeric character in the retailer name.
    points += sum([character.isalnum() for character in data["retailer"]])

    # 50 points if the total is a round dollar amount with no cents.
    total = float(data["total"])
    if total.is_integer():
        points += 50

    # 25 points if the total is a multiple of 0.25.
    if total % 0.25 == 0:
        points += 25
    
    # 5 points for every two items on the receipt.
    num_items = len(data["items"])
    points += (num_items // 2) * 5

    # Add points for if trimmed description length is divisible by 3
    for item in data["items"]:
        trimmed_description_len = len(item["shortDescription"].strip())
        if trimmed_description_len % 3 == 0:
            points += math.ceil(float(item["price"]) * 0.2) # Round to nearest integer

    # Add points if the date is odd
    purchase_date = data["purchaseDate"]
    if purchase_date.day % 2 != 0:
        points += 6
    
    # Add points if the time is after 2:00 PM and before 4:00 PM
    purchase_time = datetime.strptime(data["purchaseTime"], "%H:%M")
    if purchase_time.time() > datetime.strptime("14:00", "%H:%M").time() and purchase_time.time() < datetime.strptime("16:00", "%H:%M").time():
        points += 10
    
    return points

@app.errorhandler(404)
def handle_not_found_error(error):
    response = jsonify({"error": "Resource not found."})
    response.status_code = 404
    return response

@app.errorhandler(500)
def handle_internal_server_error(error):
    response = jsonify({"error": "Internal server error."})
    response.status_code = 500
    return response