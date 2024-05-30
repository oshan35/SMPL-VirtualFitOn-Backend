import smplx
import torch
from models.smpl.smpl_webuser import serialization
import numpy as np

## Load SMPL model (here we load the female model)
## Make sure path is correct
from models.smpl.smpl_webuser.serialization import load_model



shape_params = [ 1.05071094 ,0.72027541 ,0.2989638  ,0.05701623 ,0.07447251 ,-0.09911867,
  0.07585485, -0.05481659, -0.00452416,  0.11355854]
def create_model(gender, body_shapes):
    if gender == "male":
        m = load_model('models/smpl/models/basicmodel_m_lbs_10_207_0_v1.0.0.pkl')
    else:
        m = load_model('models/smpl/models/basicmodel_f_lbs_10_207_0_v1.0.0.pkl')
    print(m.pose.size)
    m.pose[:] = np.zeros((1, m.pose.size))*0.2
    # m.pose[:] = np.random.rand(m.pose.size) * .2
    m.betas[:] = [x * 0.03 for x in body_shapes]
    outmesh_path = 'bodymeshes/model.obj'
    with open(outmesh_path, 'w') as fp:
        for v in m.r:
            fp.write('v %f %f %f\n' % (v[0], v[1], v[2]))

        for f in m.f + 1:  # Faces are 1-based, not 0-based in obj files
            fp.write('f %d %d %d\n' % (f[0], f[1], f[2]))
    return m




if __name__ == '__main__':
    create_model("female", shape_params)