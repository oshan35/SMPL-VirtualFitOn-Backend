from flask import Flask, request, jsonify
from BodyMeasurementsPrediction import *
from BodyMeshGenerater import *
from Blender import *
app = Flask(__name__)



@app.route('/measurements', methods=['GET'])
def bodymeasurements():
    gender = request.args.get('param1', default=None, type=str)
    height= request.args.get('param2', default=None, type=str)
    weight = request.args.get('param3', default=None, type=str)

    # Check if all parameters are provided
    if None in (gender, height, weight):
        return jsonify({"error": "Missing parameters"}), 400

    body_measurements, shapeparams = getBodyMeasurements(gender,weight,height)

    return jsonify(body_measurements)

@app.route('/bodymesh', method=['GET'])
def bodymesh():
    gender = request.args.get('gender', default=None, type=str)
    height = request.args.get('height', default=None, type= str)
    weight = request.args.get('weight', default=None, type= str)

    shape_params = getBodyShapeParams(gender,weight,height)

    bodymesh = create_model(gender,shape_params)

    return jsonify(bodymesh)


app.route('/fitcloths', method=['GET'])
def fashionFits():
    bodymesh = request.args.get('bodymesh', default=None, type=str)
    cloth_model = request.args.get('clothmodel', default=None, type=str)
    combined = load_and_combine_meshes(bodymesh, cloth_model)
    return jsonify(combined)


if __name__ == '__main__':
    app.run()
