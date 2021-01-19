import rasterio
import numpy as np
from rasterio.plot import reshape_as_raster, reshape_as_image
import pickle

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
with rasterio.open(r'./example/test_image.tif') as src:
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

# EOF
