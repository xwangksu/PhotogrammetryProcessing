'''
Created on Apr 5, 2018
Updated on Dec 2, 2020

@author: Xu Wang
'''
import argparse
import Metashape

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-wp", "--wpath", required=True, help="workingPath")
args = vars(ap.parse_args())
workingPath = args["wpath"]+"\\"
print("Working path is: %s" % workingPath)

dem = workingPath+"dem.tif"
orthomosaic = workingPath+"ortho.tif"
project = workingPath+"ortho_dem_process.psx"

app = Metashape.Application()
doc = Metashape.app.document
doc.open(project)

Metashape.app.gpu_mask = 15
Metashape.app.cpu_enable = False

chunk = doc.chunk
chunk.crs = Metashape.CoordinateSystem("EPSG::4326")

chunk.buildDepthMaps(quality=Metashape.HighQuality, filter=Metashape.AggressiveFiltering)

chunk.buildDenseCloud()

chunk.buildModel(surface=Metashape.HeightField, interpolation=Metashape.DisabledInterpolation, face_count=Metashape.HighFaceCount)

doc.save(path=project, chunks=[doc.chunk])

doc = Metashape.app.document
doc.open(project)
app = Metashape.Application()

# PhotoScan.app.cpu_enable = 8

chunk = doc.chunk
chunk.crs = Metashape.CoordinateSystem("EPSG::4326")

chunk.buildDem(source=Metashape.DataSource.DenseCloudData, interpolation=Metashape.Interpolation.DisabledInterpolation, projection=Metashape.CoordinateSystem("EPSG::4326"))

chunk.buildOrthomosaic(surface=Metashape.DataSource.ElevationData, blending=Metashape.BlendingMode.MosaicBlending, projection=Metashape.CoordinateSystem("EPSG::4326"))

chunk.exportDem(dem, image_format=Metashape.ImageFormatTIFF, projection=Metashape.CoordinateSystem("EPSG::4326"), nodata=-9999, write_kml=False, write_world=False, tiff_big=False)

chunk.exportOrthomosaic(orthomosaic, image_format=Metashape.ImageFormatTIFF, raster_transform=Metashape.RasterTransformType.RasterTransformNone, projection=Metashape.CoordinateSystem("EPSG::4326"), write_kml=False, write_world=False, tiff_compression=Metashape.TiffCompressionNone, tiff_big=False)

doc.save(path=project, chunks=[doc.chunk])