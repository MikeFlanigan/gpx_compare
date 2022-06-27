import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import datetime as dt
import pyproj

geodesic = pyproj.Geod(ellps='WGS84')


tree = ET.parse('track_files/6-30-21-El_Cajon.gpx')
# tree = ET.parse('track_files/Darren-Thomas-El_Cajon.gpx')

root = tree.getroot()

meta_data = root[0]
trk = root[1]

time_start = meta_data[0]

Name = trk[0]
trk_seg = trk[2]

elevation = []
heart_rate = []
elapsed = []
distance = []

ups = []
downs = []

going_up = False 

i = 0
for pt in trk_seg:

    ele = float(pt[0].text)*3.281 # converting to feet
    ts = pt[1]

    hr = int(pt[2][0][0].text)

    lat = float(pt.attrib["lat"])
    lon = float(pt.attrib["lon"])

    elevation.append(ele)
    heart_rate.append(hr)

    time = pt[1].text
    dt_ts = dt.datetime.fromisoformat(time.replace("Z", ""))
    if i == 0:
        elapsed.append(0)
        distance.append(0)
    else:

        bearing, reverse_azimuth, dist = geodesic.inv(lon,
                                        lat,
                                        last_lon,
                                        last_lat)
        dist = dist*3.281/5280 # converting to miles
        distance.append(distance[i-1] + dist)

        elapsed.append(elapsed[i-1] + (dt_ts - last_ts).total_seconds())

        if elevation[i] >= elevation[i-1]:
            # uphill & flats
            if not going_up:
                # this was a change in elevation profile
                ups.append({"elevation":[],"distance":[],"time":[]})
            going_up = True

            if i == 1:
                ups[len(ups)-1]["elevation"].append(elevation[i-1])
                ups[len(ups)-1]["distance"].append(distance[i-1])
                ups[len(ups)-1]["time"].append(elapsed[i-1])
            ups[len(ups)-1]["elevation"].append(elevation[i])
            ups[len(ups)-1]["distance"].append(distance[i])
            ups[len(ups)-1]["time"].append(elapsed[i])
        else:
            # downhill
            if going_up:
                # this was a change in elevation profile
                downs.append({"elevation":[],"distance":[],"time":[]})
            going_up = False

            if i == 1:
                downs[len(downs)-1]["elevation"].append(elevation[i-1])
                downs[len(downs)-1]["distance"].append(distance[i-1])
                downs[len(downs)-1]["time"].append(elapsed[i-1])
            downs[len(downs)-1]["elevation"].append(elevation[i])
            downs[len(downs)-1]["distance"].append(distance[i])
            downs[len(downs)-1]["time"].append(elapsed[i])         

            

    last_ts = dt_ts
    last_lat = lat
    last_lon = lon

    i += 1

elapsed_ele = max(elevation) - min(elevation)
dist_travelled = distance[-1]
time_elapsed = elapsed[-1]

print("Net elevation gain: ",elapsed_ele)
print("distance: ",dist_travelled)
print("Time elapsed: ",time_elapsed)


plt.figure()
plt.plot(distance,elevation)

# dist_a = distance[0:1000]
# ele_a = elevation[0:1000]
# dist_b = distance[1000:]
# ele_b = elevation[1000:]

# plt.plot(dist_a,ele_a,'r')
# plt.plot(dist_b,ele_b,'g')
# plt.show()

plt.figure()
for segment in ups:
    plt.plot(segment["distance"],segment["elevation"],'r')
for segment in downs:
    plt.plot(segment["distance"],segment["elevation"],'g')


plt.xlabel("Miles")
plt.ylabel("Elevation [feet]")
plt.show()

pass 

"""
split ups and downs

"""

# next work session
# turn the above into a function
# then need to plot the two over each other... 
# add trim points to even them out?
# do some stats combining to see how long is spend on the ups, how long is spent on the downs
# get the miles to line up... then plot and show for an up or a down, who was faster **** this is a good goal. 
# would be nice to iterate through each one and potentially list by how much was one or the other faster


# maybe logical to-do list items
# create a plot of the elevation
# animate the movement of a trackpoint over the elevation...
# make add time or speed somehow...
# load a second file
# align the start finish somehow...
# plot both dots at the same time
