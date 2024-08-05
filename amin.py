# def gc_to_pixel(L):  #L -> [lat,lon]  (image centre)

#image resolution : 1920 left to right, 1080 top to bottom
from geocoding import gc
from map import make_map
from selen import save_ss
from cluster import make_cluster

c=gc("raipur",0)                  #if geocode dont exist it returns an empty list?




if len(c):
    path=make_map(c[0][1],"raipur")
    img_path=save_ss("raipur",path)
    r=make_cluster(img_path)





# 1 px -> top gcoord - 0.312/1080   conversion from pixel value to coordinate

# 1 px-> left gcoord +0.644/1920




#difference from centre : (geocodes)
#lat -> top = centre + 0.156,  boottom = centre - 0.156
#long -> left = centre - 0.322, right = centre + 0.322

#using these, we can convert the pixels (cluster centroids) to lat long values 

#NOW SHOW THE USER DETAILED ANALYSIS WHICH CENTROID IS NEAR TO MARKET, WHICH IS FAR, REMOVE THE CENTROIDS NEAR TO AIRPORT
#CREATE A MONGO DATABASE AND SAVE THE APPROVEDD CENTROIDS FOR THE CITY. NEXT TIME BEFORE CLUSTERING, SEARCH  IN THE DATABASE FOR THE CITY
#ALSO CREATE A MAIN MAP, WHICH WILL CONTAIN ALL MARKED CENTRES WHICH ARE APPROVED. WHILE PERFORMING LLIVE DELIVERY, SHOW THE USER MAP COPIED FROM THE MAIN MAP ONLY
#FIND HOW TO CALCULATE DISTANCE BETWEEN TWO POINTS IF YOU KKNOW LATITUDE AND LONGITUDE
