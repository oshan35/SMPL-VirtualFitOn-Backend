import numpy as np

MEAS_COEF_FILE = './coefs/{}_meas_coefs.npy'
SHAPE_COEF_FILE = './coefs/{}_shape_coefs.npy'
measurements_name = [
                "head_circumference",
                "neck_circumference",
                "shoulder_to_crotch",
                "chest_circumference",
                "waist_circumference",
                "hip_circumference",
                "wrist_circumference",
                "bicep_circumference",
                "forearm_circumference",
                "arm_length",
                "inside_leg_length",
                "thigh_circumference",
                "calf_circumference",
                "ankle_circumference",
                "shoulder_breadth"
                ]

def getBodyMeasurements(gender, weight, height):
    meas_coefs = np.load(MEAS_COEF_FILE.format(gender))
    shape_coefs = np.load(SHAPE_COEF_FILE.format(gender))

    h,w = float(height),float(weight)


    measurements = h * meas_coefs[:, 0] + w * meas_coefs[:, 1] + \
        w / h**2 * meas_coefs[:, 2] + w * h * meas_coefs[:, 3] + meas_coefs[:, 4]
    shape_params = h * shape_coefs[:, 0] + w * shape_coefs[:, 1] + shape_coefs[:, 2]

    measurements_map = {}


    for mes, unit in zip(measurements_name,measurements):

        measurements_map[mes] = round(unit * 100,2)

    return measurements_map

def getBodyShapeParams(gender, weight, height):

    shape_coefs = np.load(SHAPE_COEF_FILE.format(gender))

    h,w = float(height),float(weight)

    shape_params = h * shape_coefs[:, 0] + w * shape_coefs[:, 1] + shape_coefs[:, 2]

    return shape_params

if __name__ == '__main__':
    getBodyMeasurements("male", 65, 1.72)