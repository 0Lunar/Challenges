import xml.etree.ElementTree as ET
import os

filepath = 'solve.xml'
ns = {'gpx': 'http://www.topografix.com/GPX/1/1'}

tree = ET.parse(filepath)
root = tree.getroot()
trkpt = root.find('.//gpx:trk/gpx:trkseg/gpx:trkpt', ns)
if trkpt is None:
    print("Error: GPX must contain a track with at least one track point.", 400)

for pt in root.findall('.//gpx:trkpt', ns):
    if pt.find('gpx:ele', ns) is None:
        print("Error: Every track point must include an elevation (<ele>) element.", 400)
        
metadata = root.find('gpx:metadata', ns)
if metadata is None or metadata.find('gpx:name', ns) is None:
    print("Error: GPX metadata must include a <name> tag.", 400)
if metadata.find('gpx:time', ns) is None:
    print("Error: GPX metadata must include a <time> tag.", 400)
    
out_name = metadata.find('gpx:name', ns).text or "output"
out_name = out_name.replace(" ", "")

out_path = os.path.join("/", out_name)
command = f"gpsbabel -i gpx -f {filepath} -o geojson -F {out_path}.json"

print(command)