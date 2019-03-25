"""
Remote Sensing Data - Masks and Plotting with EarthPy
=====================================================


"""

###############################################################################
# Plotting with EarthPy
# ---------------------
#
# .. note:: The examples below demonstrate a typical workflow using Landsat data with earthpy


###############################################################################
# Plot Continuous Data
# ------------------------------
#
# Let's explore a simple plot using earthpy. To begin, import the needed packages
# and create an array to be plotted. Below we plot the data as continuous with a colorbar
# using the ``plot_bands()`` function

import numpy as np
from glob import glob
import os
import matplotlib.pyplot as plt
import rasterio as rio
from rasterio.plot import plotting_extent
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import earthpy.mask as em

# Get data and set your home working directory
data = et.data.get_data("cold-springs-fire")

###############################################################################
# Import Example Data
# ------------------------------

os.chdir(os.path.join(et.io.HOME, "earth-analytics"))

# Create a numpy array. Let's pretend this is what you want to plot.
# Stack the landsat pre fire data
landsat_paths_pre = glob(
    "data/cold-springs-fire/landsat_collect/LC080340322016070701T1-SC20180214145604/crop/*band*.tif"
)
landsat_paths_pre.sort()
arr_st, meta = es.stack(landsat_paths_pre)

# We will
with rio.open(
    "data/cold-springs-fire/landsat_collect/LC080340322016070701T1-SC20180214145604/crop/LC08_L1TP_034032_20160707_20170221_01_T1_pixel_qa_crop.tif"
) as landsat_pre_cl:
    landsat_qa = landsat_pre_cl.read(1)
    landsat_ext = plotting_extent(landsat_pre_cl)

###############################################################################
# Plot Histogram of Each Band in Your Data
# ----------------------------------------

# You can view a histogram for each band in your dataset by using the
# hist() function from the `earthpy.plot` module.

ep.hist(arr_st)
plt.show()

###############################################################################
# Customize Histogram Plot with Titles and Colors
# -----------------------------------------------

# Read landsat pre fire data
ep.hist(
    arr_st,
    colors=["blue"],
    title=[
        "Band 1",
        "Band 2",
        "Band 3",
        "Band 4",
        "Band 5",
        "Band 6",
        "Band 7",
    ],
)
plt.show()

###############################################################################
# View Single Band Plots
# -----------------------------------------------
# Next, have a look at the data, it looks like there is a large cloud that you
# may want to mask out.

# When plot_bands is updated a cbar will be here as well
ep.plot_bands(arr_st)
plt.show()


###############################################################################
# Mask the Data
# -----------------------------------------------

# You can use the earthpy mask() function to handle this cloud.
# TO begin you need to have a layer that defines the pixels that
# you wish to mask. In this case, the ``landsat_qa`` layer will be used.

# Still haven't found a good way to normalize this data
ep.plot_bands(
    landsat_qa,
    title="The Landsat QA Layer Comes with Landsat Data\n It can be used to remove clouds and shadows",
)
plt.show()


# Generate array of all possible cloud / shadow values
cloud_shadow = [328, 392, 840, 904, 1350]
cloud = [352, 368, 416, 432, 480, 864, 880, 928, 944, 992]
high_confidence_cloud = [480, 992]

all_masked_values = cloud_shadow + cloud + high_confidence_cloud
arr_ma = em.mask_pixels(arr_st, landsat_qa, vals=all_masked_values)

###############################################################################
# Plot The Masked Data
# ~~~~~~~~~~~~~~~~~~~~~
# Now plot the masked data

# sphinx_gallery_thumbnail_number = 5
ep.plot_rgb(
    arr_ma, rgb=[4, 3, 2], title="Array with Clouds and Shadows Masked"
)
plt.show()