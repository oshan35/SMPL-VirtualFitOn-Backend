from flask import Flask, request, jsonify
from BodyMeasurementsPrediction import *
# from BodyMeshGenerater import *
# from Blender import *
from Match import *

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Body Measurements API!"

@app.route('/test', methods=['GET'])
def test_api():
    return jsonify({
        "status": "success",
        "message": "Test API is working!"
    })

@app.route('/measurements', methods=['GET'])
def bodymeasurements():
    gender = request.args.get('param1', default=None, type=str)
    height = request.args.get('param2', default=None, type=str)
    weight = request.args.get('param3', default=None, type=str)

    # Check if all parameters are provided
    if None in (gender, height, weight):
        return jsonify({"error": "Missing parameters"}), 400

    body_measurements = getBodyMeasurements(gender, weight, height)

    return jsonify(body_measurements)

# @app.route('/bodymesh', methods=['GET'])  # Corrected here
# def bodymesh():
#     gender = request.args.get('gender', default=None, type=str)
#     height = request.args.get('height', default=None, type=str)
#     weight = request.args.get('weight', default=None, type=str)
#
#     shape_params = getBodyShapeParams(gender, weight, height)
#
#     bodymesh = create_model(gender, shape_params)
#
#     return jsonify(bodymesh)


@app.route('/sizematch', methods=['POST'])
def match_size():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    product_measurements = data.get('product_measurements')
    customer_measurements = data.get('customer_measurements')
    if not product_measurements or not customer_measurements:
        return jsonify({"error": "Missing product or customer measurements"}), 400

    match_size = ""
    best_match = 0

    for size, product_item_measurements in product_measurements.items():
        print(size)
        match_pres = calculate_match_percentage(customer_measurements, product_item_measurements)
        if match_pres > best_match:
            best_match = match_pres
            match_size = size

    return jsonify({
        "matching_size": match_size,
        "matching_percentage": best_match
    })



@app.route('/fitcloths', methods=['GET'])  # Corrected here and added @
def fashionFits():
    bodymesh = request.args.get('bodymesh', default=None, type=str)
    cloth_model = request.args.get('clothmodel', default=None, type=str)

    # combined = load_and_combine_meshes(bodymesh, cloth_model)
    # return jsonify(combined)
    return jsonify({"message": "Not implemented"}), 501  # Example placeholder response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
