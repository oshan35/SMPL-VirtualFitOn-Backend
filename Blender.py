import numpy as np
from scipy.optimize import minimize
from models.smpl.smpl_webuser.serialization import load_model

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

    h, w = float(height), float(weight)

    measurements = h * meas_coefs[:, 0] + w * meas_coefs[:, 1] + \
        w / h**2 * meas_coefs[:, 2] + w * h * meas_coefs[:, 3] + meas_coefs[:, 4]
    shape_params = h * shape_coefs[:, 0] + w * shape_coefs[:, 1] + shape_coefs[:, 2]

    measurements_map = {}

    for mes, unit in zip(measurements_name, measurements):
        measurements_map[mes] = round(unit * 100, 2)

    return measurements_map

def create_model(gender, betas):
    if gender == "male":
        m = load_model('models/smpl/models/basicmodel_m_lbs_10_207_0_v1.0.0.pkl')
    else:
        m = load_model('models/smpl/models/basicmodel_f_lbs_10_207_0_v1.0.0.pkl')

    m.betas[:] = betas[:10]  # SMPL allows 10 shape parameters
    print(m.r)

    outmesh_path = 'bodymeshes/test2.obj'
    with open(outmesh_path, 'w') as fp:
        for v in m.r:
            fp.write('v %f %f %f\n' % (v[0], v[1], v[2]))

        for f in m.f + 1:  # Faces are 1-based, not 0-based in obj files
            fp.write('f %d %d %d\n' % (f[0], f[1], f[2]))

    return m

def objective_function(betas, target_measurements, gender):
    model = create_model(gender, betas)
    estimated_measurements = get_estimated_measurements(model)
    loss = np.sum((estimated_measurements - target_measurements) ** 2)
    return loss

def get_estimated_measurements(model):
    # Dummy function to calculate measurements from the model vertices
    # This should be replaced with actual calculations based on model vertices
    measurements = np.zeros(len(measurements_name))
    # Perform calculations to estimate body measurements based on model vertices
    return measurements

def fit_body_model(gender, target_measurements):
    initial_betas = np.zeros(10)  # Initial guess for shape parameters
    result = minimize(objective_function, initial_betas, args=(target_measurements, gender), method='BFGS')
    return result.x

if __name__ == '__main__':
    gender = "male"
    weight = 70
    height = 1.75

    target_measurements = np.array([
        57.0, 38.0, 60.0, 200.0, 80.0, 90.0, 16.0, 30.0, 25.0, 60.0,
        80.0, 55.0, 40.0, 25.0, 45.0
    ])

    optimized_betas = fit_body_model(gender, target_measurements)
    print("Optimized Betas:", optimized_betas)

    create_model(gender, optimized_betas)
