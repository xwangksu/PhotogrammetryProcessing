'''
Created on Apr 5, 2018
Updated on Dec 2, 2020

@author: Xu Wang
'''
import os
import argparse
import Metashape

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-wp", "--wpath", required=True, help="workingPath")
args = vars(ap.parse_args())
workingPath = args["wpath"]
print("Working path is: %s" % workingPath)
srcImagePath = workingPath
project = workingPath+"\\ortho_dem_process.psx"

files = os.listdir(srcImagePath+"\\calibrated\\")
file_list=[]
for file in files:
    if file.endswith(".tif"):
        filePath = srcImagePath +"\\calibrated\\"+ file
        file_list.append(filePath)
app = Metashape.Application()
doc = Metashape.app.document

Metashape.app.gpu_mask = 15
Metashape.app.cpu_enable = False

chunk = doc.addChunk()
chunk.crs = Metashape.CoordinateSystem("EPSG::4326")
# Import photos
chunk.addPhotos(file_list, Metashape.MultiplaneLayout)
chunk.matchPhotos(accuracy=Metashape.HighAccuracy, preselection=Metashape.ReferencePreselection, keypoint_limit = 15000, tiepoint_limit = 10000)
# Align photos                 
chunk.alignCameras(adaptive_fitting=True)
# Save project
doc.save(path=project, chunks=[doc.chunk])
