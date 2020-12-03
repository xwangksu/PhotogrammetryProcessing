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
ap.add_argument("-mf", "--mfile", required=True, help="markerFile")
args = vars(ap.parse_args())
workingPath = args["wpath"]+"\\"
markerFile = args["mfile"]
print("Working path is: %s" % workingPath)

project = workingPath+"ortho_dem_process.psx"

app = Metashape.Application()
doc = Metashape.app.document
doc.open(project)

Metashape.app.gpu_mask = 15
Metashape.app.cpu_enable = False

chunk = doc.chunk
chunk.crs = Metashape.CoordinateSystem("EPSG::4326")

# Assign GCPs
markerList = open(markerFile, "rt")
# print(markerList)
eof = False
line = markerList.readline() #reading the line in input file
# print(line)
while not eof:
    photos_total = len(chunk.cameras)         #number of photos in chunk
    # print(photos_total)
    markers_total = len(chunk.markers)         #number of markers in chunk
    sp_line = line.rsplit(",", 6)   #splitting read line by four parts
    camera_name = sp_line[0]        #camera label
    marker_name = sp_line[1]        #marker label
    x = int(sp_line[2])                #x- coordinate of the current projection in pixels
    y = int(sp_line[3])                #y- coordinate of the current projection in pixels
    cx = float(sp_line[4])            #world x- coordinate of the current marker
    cy = float(sp_line[5])            #world y- coordinate of the current marker
    cz = float(sp_line[6])            #world z- coordinate of the current marker
    flag = 0
    for i in range (0, photos_total):   
        if chunk.cameras[i].label == camera_name:
            for marker in chunk.markers:    #searching for the marker (comparing with all the marker labels in chunk)
                if marker.label == marker_name:
                    marker.projections[chunk.cameras[i]] = Metashape.Marker.Projection(Metashape.Vector([x,y]), True)       #setting up marker projection of the correct photo)
                    flag = 1
                    break
            if not flag:
                marker = chunk.addMarker()
                marker.label = marker_name
                marker.projections[chunk.cameras[i]] = Metashape.Marker.Projection(Metashape.Vector([x,y]), True)
                # print(marker)
            marker.reference.location = Metashape.Vector([cx, cy, cz])
            break
    line = markerList.readline()        #reading the line in input file
#     print (line)
    if len(line) == 0:
        eof = True
        break # EOF
markerList.close()
# Save project
doc.save(path=project, chunks=[doc.chunk])
