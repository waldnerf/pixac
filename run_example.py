import rasterio
import numpy as np
from rasterio.plot import reshape_as_raster, reshape_as_image
import pickle
import matplotlib.pyplot as plt

from pixac.pixelaccuracy import *

# Read the training data

with open('./example/example_data.pickle', 'rb') as handle:
    example_data = pickle.load(handle)

# my_X: features; lbls: reference labels; prds: predicted labels
my_X = example_data['X']
lbls = example_data['labels']
prds = example_data['preds']

pixel_accuracy = PixelAccuracy()
pixel_accuracy.fit(my_X, lbls, prds)

# read the image stack to use for inference
with rasterio.open(r'./example/example_image.tif') as src:
    ras = src.read()
    img = reshape_as_image(ras).astype(np.int)
    profile = src.profile

img = np.nan_to_num(img)

# apply inference
my_pamaps = pixel_accuracy.inference(img)

# save output to raster
profile.update(
    dtype=rasterio.float64,
    count=my_pamaps.shape[0],
    compress='lzw')

with rasterio.open('./example/pixel_based_accuracy.tif', 'w', **profile) as dst:
    dst.write(my_pamaps)


# With map to mask out
with open('./example/example_data.pickle', 'rb') as handle:
    example_data = pickle.load(handle)

# my_X: features; lbls: reference labels; prds: predicted labels
my_X = example_data['X']
lbls = example_data['labels']
prds = example_data['preds']

pixel_accuracy = PixelAccuracy()
pixel_accuracy.fit(my_X, lbls, prds)

# read the image stack to use for inference
with rasterio.open(r'./example/example2_image.tif') as src:
    ras = src.read()
    img = reshape_as_image(ras).astype(np.int)
    profile = src.profile

img = np.nan_to_num(img)

with rasterio.open(r'./example/example2_map.tif') as src:
    _ras = src.read(1)
    map = _ras.astype(np.int)



# apply inference
my_pamaps = pixel_accuracy.inference(img, map)
my_pamaps_bu = my_pamaps

my_pamaps = my_pamaps_bu
for i, _class in enumerate(pixel_accuracy.model_dic.keys()):
    print(i)
    _acc_class_i = my_pamaps[i]
    _acc_class_i[map != _class] = -10000
    plt.figure()
    plt.imshow(_acc_class_i)
    my_pamaps[i] = _acc_class_i
_acc_masked = my_pamaps.max(axis=0)
plt.imshow(_acc_masked)


# save output to raster
profile.update(
    dtype=rasterio.float64,
    count=1,
    compress='lzw')

with rasterio.open('./example/pixel_based_accuracy2.tif', 'w', **profile) as dst:
    my_pamaps[my_pamaps==-10000]=np.nan
    dst.write(np.expand_dims(my_pamaps, 0))


# EOF
