from geocoding import gc
from map import make_map
from selen import save_ss
from cluster import make_cluster

c=gc("bhopal")
if len(c):
    path=make_map(c[0][1],"bhopal")
    img_path=save_ss("bhopal",path)
    make_cluster(img_path)

else:
    #show in frontend -> location not exist
    pass



# difference from centre : (geocodes)

#lat -> top = centre + 0.156,  boottom = centre - 0.156
#long -> left = centre - 0.322, right = centre + 0.322

#using these, we can convert the pixels (cluster centroids) to lat long values 

#NOW SHOW THE USER DETAILED ANALYSIS WHICH CENTROID IS NEAR TO MARKET, WHICH IS FAR, REMOVE THE CENTROIDS NEAR TO AIRPORT
#CREATE A MONGO DATABASE AND SAVE THE APPROVEDD CENTROIDS FOR THE CITY. NEXT TIME BEFORE CLUSTERING, SEARCH  IN THE DATABASE FOR THE CITY
#ALSO CREATE A MAIN MAP, WHICH WILL CONTAIN ALL MARKED CENTRES WHICH ARE APPROVED. WHILE PERFORMING LLIVE DELIVERY, SHOW THE USER MAP COPIED FROM THE MAIN MAP ONLY
#FIND HOW TO CALCULATE DISTANCE BETWEEN TWO POINTS IF YOU KKNOW LATITUDE AND LONGITUDE
