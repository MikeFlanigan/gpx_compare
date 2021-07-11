import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

tree = ET.parse('track_files/6-30-21-El_Cajon.gpx')
root = tree.getroot()

meta_data = root[0]
trk = root[1]

time_start = meta_data[0]

Name = trk[0]
trk_seg = trk[2]

elevation = []
heart_rate = []

i = 0
for pt in trk_seg:

    ele = float(pt[0].text)
    ts = pt[1]

    hr = int(pt[2][0][0].text)

    elevation.append(ele)
    heart_rate.append(hr)

plt.plot(elevation)
plt.show()


