'''
Created on Nov 15, 2018

@author: xuwang
'''
import argparse
import PhotoScan
import os
import errno

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-wp", "--wpath", required=True, help="workingPath")
args = vars(ap.parse_args())
workingPath = args["wpath"]+"\\"
print("Working path is: %s" % workingPath)

try:
    os.makedirs(workingPath+"orthophotos")
    print("Creating Calibrated directory.")
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise

project = workingPath+"ortho_dem_process.psx"

app = PhotoScan.Application()
doc = PhotoScan.app.document
doc.open(project)

chunk = doc.chunk
chunk.crs = PhotoScan.CoordinateSystem("EPSG::4326")

proj = Metashape.OrthoProjection()
proj.crs = Metashape.CoordinateSystem("EPSG::4326")

compr = Metashape.ImageCompression()
compr.tiff_compression = Metashape.ImageCompression.TiffCompressionNone
compr.tiff_big = False
compr.tiff_overviews = False
compr.tiff_tiled = False

chunk.exportOrthophotos(path=workingPath+"orthophotos\\{filename}.tif", cameras=chunk.cameras, raster_transform=Metashape.RasterTransformNone,
                        projection=proj, save_kml=False,
                        save_world=False, save_alpha=False, image_compression=compr,
                        white_background=False)

doc.save(path=project, chunks=[doc.chunk])