import rasterio
import os, glob
import numpy as np
from rasterio.plot import reshape_as_raster, reshape_as_image
import pickle
import matplotlib.pyplot as plt

from pixac.pixelaccuracy import *

# Read the training data
root_dir = r'/eos/jeodpp/home/users/waldnfr/pixac'
rdata_fn = os.path.join(root_dir, r'LUCAS_validation_map_ref_S1_1x1.csv')
mp_fns   = glob.glob(os.path.join(root_dir, 's1_stack_EU*level2.tif'))
im_fns   = [x for x in glob.glob(os.path.join(root_dir, 's1_stack_EU*.tif')) if 'level2' not in x]
my_nan = -10000
nnodes = 10

# Read validation data and subset to stratum 1
df = pd.read_csv(rdata_fn)
df = df[df['stratum'].isin([1])]
df = df.dropna()

# Generate feature set, labels, and predictions
lbls = df['level_2'].values
prds = df['prediction_v5'].values
my_X = df[[x for x in list(df.columns) if x.startswith('V')]].values

# Build prediction models
pixel_accuracy = PixelAccuracy(njobs=2)
pixel_accuracy.fit(my_X, lbls, prds)

# Model inference on Sentinel-2 tiles
for mp_fn, im_fn in zip(mp_fns, im_fns):
    pa_fn = mp_fn.split('.tif')[0]+'_pa.tif'

    # read the image stack to use for inference
    with rasterio.open(im_fn) as src:
        ras = src.read()
        img = reshape_as_image(ras).astype(np.int)
        profile = src.profile

    img = np.nan_to_num(img)

    with rasterio.open(mp_fn) as src:
        _ras = src.read(1)
        map = _ras.astype(np.int)

    # apply inference
    my_pamaps = pixel_accuracy.inference(img, map, my_nan)

    # save output to raster
    profile.update(
        dtype=rasterio.float64,
        count=1,
        compress='lzw')

    with rasterio.open(pa_fn, 'w', **profile) as dst:
        my_pamaps[my_pamaps == my_nan] = np.nan
        dst.write(np.expand_dims(my_pamaps, 0))

# EOF