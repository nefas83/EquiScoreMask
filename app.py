from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, emit
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import xml.etree.ElementTree as ET
import json

# ======== CLASSES ========
class XMLData:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.data = self.parse_xml()

    def parse_xml(self):
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        data = []

        for item in root.findall('TResultsProvider'):
            competition = {
                'mId': item.find('mId').text,
                'identifier': item.find('identifier').text,
                'orgId': item.find('orgId').text,
                'name': item.find('name').text,
                'startTime': item.find('startTime').text,
                'classNumber': item.find('classNumber').text,
                'Officials': [],
                'Competitors': []
            }
            
            for official in item.findall('Officials/o'):
                competition['Officials'].append({
                    'judgeBy': official.find('judgeBy').text,
                    'fullName': official.find('fullName').text,
                })

                competitors = []
                for competitor in item.findall('Competitors/o'):
                    dressage_results = []
                    total_results = []

                    country_code_node = competitor.find('country')
                    if country_code_node is not None:
                        country_code = country_code_node.text
                        flag_image = get_flag_image(country_code, flags)
                    
                    results_node = competitor.find('Results')
                    if results_node is not None:
                        for result in results_node.iter('o'):
                            result_item_type_node = result.find('resultItemType')
                            if result_item_type_node is not None:
                                if result_item_type_node.text == 'ritDressage':
                                    dressage_results.append({
                                        'resultItemType': result_item_type_node.text,
                                        'judgeBy': result.find('judgeBy').text,
                                        'score': result.find('score').text,
                                        'procent': result.find('procent').text,
                                        'rank': result.find('rank').text if result.find('rank') is not None else 'N/A',
                                    })
                                
                                elif result_item_type_node.text == 'ritDressageTotal':
                                    total_results.append({
                                        'resultItemType': result_item_type_node.text,
                                        'score': result.find('score').text,
                                        'procent': result.find('procent').text,
                                        'penaltyPoints': result.find('penaltyPoints').text,
                                    })

                    competitors.append({
                        'id': competitor.find('id').text,
                        'startingNumber': competitor.find('startingNumber').text,
                        'rank': competitor.find('rank').text if competitor.find('rank') is not None else 'N/A',
                        'fullName': competitor.find('fullName').text,
                        'orgName': competitor.find('orgName').text,
                        'flag_image': flag_image,
                        'DressageResults': dressage_results,
                        'TotalResults': total_results,
                        'Gespanne': [{
                            'HorseName': horse.find('HorseName').text,
                            'bornYear': horse.find('bornYear').text,
                            'sex': horse.find('sex').text
                        } for horse in competitor.find('Gespanne').iter('o')],
                    })

            competition['Competitors'] = sorted(competitors, key=lambda x: int(x['rank']) if x['rank'].isdigit() else float('inf'))
            data.append(competition)

        return data

    def reload_data(self):
        self.data = self.parse_xml()

    def get_data(self):
        return self.data
    
# -------------------------------------------------------    
    
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')
        if event.src_path == xml_data.xml_file:
            xml_data.reload_data()
            socketio.emit('data_updated')
        else:
            print("=====================================> Modified file is not the XML file, ignoring...")

    def on_any_event(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')
# ===========================
# ===========================  

# ======== VARIABLES ========
xml_data = XMLData('data/equiscore.xml')
data = []

app = Flask(__name__)
app.debug = True
bootstrap = Bootstrap(app)
socketio = SocketIO(app,cors_allowed_origins='*', logger=True, engineio_logger=True)
# =========================== 
# =========================== 

# ======== FUNCTIONS ========
# Load the flags.json file
def get_flag_image(code, flags):
    for flag in flags:
        if flag['code'] == code:
            return flag['image']
    return ''

# Lade die flags.json-Datei
with open('static/flags.json', 'r', encoding='utf-8') as f:
    flags = json.load(f)
# =========================== 
# =========================== 

# ======== ROUTES ===========
@app.route('/')
def home():
    return render_template('table.html', data=xml_data.get_data(), flags=flags)

@app.route('/data')
def get_data():
    return jsonify(xml_data.get_data())
# =========================== 
# =========================== 

# ======== MAIN =============
if __name__ == "__main__":
    observer = Observer()
    event_handler = FileChangeHandler()
    observer.schedule(event_handler, path='data/', recursive=False)
    observer.start()

    try:
        socketio.run(app,  host='0.0.0.0', port=5000, debug=True)
    finally:
        observer.stop()
        observer.join()
