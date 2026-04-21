#!/usr/bin/env python3
import os
import subprocess
from flask import Flask, request, render_template, send_file
import xml.etree.ElementTree as ET

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'
OUTPUT_FOLDER = '/tmp/outputs'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert_gpx():
    file = request.files.get('file')
    if not file:
        return "No file uploaded", 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    filepath = os.path.join(UPLOAD_FOLDER, "input.gpx")
    file.save(filepath)

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        ns = {'gpx': 'http://www.topografix.com/GPX/1/1'}

        trkpt = root.find('.//gpx:trk/gpx:trkseg/gpx:trkpt', ns)
        if trkpt is None:
            return "Error: GPX must contain a track with at least one track point.", 400

        for pt in root.findall('.//gpx:trkpt', ns):
            if pt.find('gpx:ele', ns) is None:
                return "Error: Every track point must include an elevation (<ele>) element.", 400

        metadata = root.find('gpx:metadata', ns)
        if metadata is None or metadata.find('gpx:name', ns) is None:
            return "Error: GPX metadata must include a <name> tag.", 400
        if metadata.find('gpx:time', ns) is None:
            return "Error: GPX metadata must include a <time> tag.", 400

        out_name = metadata.find('gpx:name', ns).text or "output"
        out_name = out_name.replace(" ", "")

        out_path = os.path.join(OUTPUT_FOLDER, out_name)
        command = f"gpsbabel -i gpx -f {filepath} -o geojson -F {out_path}.json"
        subprocess.run(command, shell=True, check=False, timeout=10)

        return send_file(
            f"{out_path}.json",
            mimetype="application/geo+json",
            as_attachment=True,
            download_name=f"{out_name}.json",
        )

    except ET.ParseError as e:
        return f"Error: Invalid XML — {str(e)}", 400
    except Exception as e:
        return f"Error processing file: {str(e)}", 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
