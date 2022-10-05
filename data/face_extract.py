import face_alignment
from skimage import io
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._3D, flip_input=False, device='cpu')

input = io.imread('test.jpg')
preds = fa.get_landmarks(input)
print(len(preds))


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(preds[0][:,0], preds[0][:,1], preds[0][:,2], "red")
plt.show()