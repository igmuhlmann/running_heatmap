import folium
import gpxpy
import os


# Parameter
# Change Center Map to desigred Values
center_map = [52.5211, 13.4133];

trackdata = {};
trackdata["color"] = "cornsilk"
trackdata["opacity"] = 0.8
trackdata["width"] = 0.5

# Archiv als geojson
laufkarte = './archive/archive.geojson'

# Ordner für neue Tracks (als GPX)
dir_path = './tracks/'

## Routine zum Abklappern des Verzeichnisses
res = []
for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        res.append(path)
print("Neue Tracks: ")
print(res)

## Routinen zum Zeichnen
# Style Function definieren
style_function = lambda x: {
    'color' : trackdata["color"],
    'weight' : trackdata["width"],
    'opacity' : trackdata["opacity"],
}

# Hintergrundkarte - cartodbdark_matter ist der dunkle Hintergrundkarte
m = folium.Map(location=center_map,zoom_start=13, tiles='cartodbdark_matter')
# Archiv einzeichnen
if os.path.isfile(laufkarte):
    folium.GeoJson(laufkarte,style_function=style_function).add_to(m)
else:
    print("Kein Archiv gefunden")

for testgpx in res:
    gpx_file = open(dir_path+testgpx, 'r')
    gpx = gpxpy.parse(gpx_file)
    points = []
    for track in gpx.tracks:
        for segment in track.segments:        
            for point in segment.points:
                points.append(tuple([point.latitude, point.longitude]))
    #print(points)
    folium.PolyLine(points, color=trackdata["color"], weight=trackdata["width"], opacity=trackdata["opacity"]).add_to(m)

folium.TileLayer('openstreetmap').add_to(m)
folium.LayerControl().add_to(m)
m.save('leaflet_map.html')

