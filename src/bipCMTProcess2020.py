'''
Created on Apr 10, 2020

@author: Xu Wang
'''

import argparse
import PhotoScan

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-wp", "--wpath", required=True, help="workingPath")
args = vars(ap.parse_args())
project = args["wpath"]
print("Working project is: %s" % project)

app = PhotoScan.Application()
doc = PhotoScan.app.document
doc.open(project)
PhotoScan.app.gpu_mask = 1
chunk = doc.chunk
chunk.crs = PhotoScan.CoordinateSystem("EPSG::4326")
chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy, preselection=PhotoScan.ReferencePreselection, keypoint_limit = 15000, tiepoint_limit = 10000)
# Align photos                 
chunk.alignCameras(adaptive_fitting=True)
# Save project
doc.save(path=project, chunks=[doc.chunk])


dem = project.replace(".psx","_dem.tif")
orthomosaic = project.replace(".psx","_ortho.tif")

app = PhotoScan.Application()
doc = PhotoScan.app.document
doc.open(project)

chunk = doc.chunk
chunk.crs = PhotoScan.CoordinateSystem("EPSG::4326")
chunk.updateTransform()
chunk.optimizeCameras(fit_f=True, fit_cxcy=True, fit_b1=True, fit_b2=True, fit_k1k2k3=True, fit_p1p2=True)
doc.save(path=project, chunks=[doc.chunk])


app = PhotoScan.Application()
doc = PhotoScan.app.document
doc.open(project)

PhotoScan.app.gpu_mask = 1

chunk = doc.chunk
chunk.crs = PhotoScan.CoordinateSystem("EPSG::4326")
chunk.buildDepthMaps(quality=PhotoScan.HighQuality, filter=PhotoScan.AggressiveFiltering)
chunk.buildDenseCloud()
chunk.buildModel(surface=PhotoScan.HeightField, interpolation=PhotoScan.DisabledInterpolation, face_count=PhotoScan.FaceCount.HighFaceCount)
doc.save(path=project, chunks=[doc.chunk])


doc = PhotoScan.app.document
doc.open(project)
app = PhotoScan.Application()
chunk = doc.chunk
chunk.crs = PhotoScan.CoordinateSystem("EPSG::4326")

chunk.buildDem(source=PhotoScan.DataSource.DenseCloudData, interpolation=PhotoScan.Interpolation.DisabledInterpolation, projection=PhotoScan.CoordinateSystem("EPSG::4326"))
chunk.buildOrthomosaic(surface=PhotoScan.DataSource.ElevationData, blending=PhotoScan.BlendingMode.MosaicBlending, projection=PhotoScan.CoordinateSystem("EPSG::4326"))
chunk.exportDem(dem, image_format=PhotoScan.ImageFormatTIFF, projection=PhotoScan.CoordinateSystem("EPSG::4326"), nodata=-9999, write_kml=False, write_world=False, tiff_big=False)
chunk.exportOrthomosaic(orthomosaic, image_format=PhotoScan.ImageFormatTIFF, raster_transform=PhotoScan.RasterTransformType.RasterTransformNone, projection=PhotoScan.CoordinateSystem("EPSG::4326"), write_kml=False, write_world=False, tiff_compression=PhotoScan.TiffCompressionNone, tiff_big=False)
doc.save(path=project, chunks=[doc.chunk])

