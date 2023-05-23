"""
EquiScoreMask: A Python Flask application for displaying equestrian competition results.

This application reads competition results from an XML file 
and presents them in a tabular format on a web page.
The application also watches for changes in the XML file 
and updates the displayed results in real-time.
"""

import json
import xml.etree.ElementTree as ET

from flask import Flask, jsonify, render_template
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


# ======== FUNCTIONS ========
# Load the flags.json file


def get_flag_image(code, _flags):
    """
    Returns the flag image URL for a given country code.

    Parameters
    ----------
    code : str
        The ISO 3166-1 alpha-2 country code.
    flags : list
        A list of dictionaries representing the flag data.

    Returns
    -------
    str
        The URL of the flag image corresponding to the country code.
        If no match is found, an empty string is returned.
    """
    for flag in _flags:
        if flag['code'] == code:
            return flag['image']
    return ''


# Lade die flags.json-Datei
with open('static/flags.json', 'r', encoding='utf-8') as f:
    flags = json.load(f)
# ===========================
# ===========================

# ======== CLASSES ========
class XMLData:
    """
    A class used to represent the XML data of the competition results.

    ...

    Attributes
    ----------
    xml_file : str
        a string representing the path to the XML file
    data : list
        a list of dictionaries representing the parsed XML data

    Methods
    -------
    parse_xml()
        Parses the XML file and returns a list of dictionaries representing the competition results.
    reload_data()
        Reloads the data from the XML file.
    get_data()
        Returns the data.
    """

    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.data = self.parse_xml()

    def parse_xml(self):
        """
        Parses the XML file and returns a list of dictionaries representing the competition results.

        The XML file is expected to have a specific structure with 
        'TResultsProvider' elements containing the competition 
        details and nested 'Officials' and 'Competitors' elements containing the details 
        of the officials and competitors 
        respectively.

        Returns
        -------
        list
            A list of dictionaries where each dictionary represents a competition and contains
            the details of the competition,
            the officials, and the competitors.
        """
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
                            result_item_type_node = result.find(
                                'resultItemType')
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

            competition['Competitors'] = sorted(competitors, key=lambda x: int(
                x['rank']) if x['rank'].isdigit() else float('inf'))
            data.append(competition)

        return data

    def reload_data(self):
        """
        Reloads the data from the XML file.

        This method is useful when the XML file has been updated and the changes need to be 
        reflected in the application.
        """
        self.data = self.parse_xml()

    def get_data(self):
        """
        Returns the data.

        Returns
        -------
        list
            The data that has been loaded from the XML file.
        """
        return self.data

# -------------------------------------------------------


class FileChangeHandler(FileSystemEventHandler):
    """
    A class used to handle file change events.

    This class inherits from the FileSystemEventHandler class in the watchdog.events module.
    It overrides the on_modified and on_any_event methods to handle file modification events.
    """

    def on_modified(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')
        if event.src_path == xml_data.xml_file:
            xml_data.reload_data()
            socketio.emit('data_updated')
        else:
            print("Modified file is not the XML file, ignoring...")

    def on_any_event(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')
# ===========================
# ===========================


# ======== VARIABLES ========
xml_data = XMLData('data/equiscore.xml')
#data = []

app = Flask(__name__)
app.debug = True
bootstrap = Bootstrap(app)
socketio = SocketIO(app, cors_allowed_origins='*',
                    logger=True, engineio_logger=True)
# ===========================
# ===========================

# ======== ROUTES ===========


@app.route('/')
def home():
    """
    The home route.

    Returns
    -------
    str
        The rendered HTML for the home page.
    """
    return render_template('table.html', data=xml_data.get_data(), flags=flags)


@app.route('/data')
def get_data():
    """
    The data route.

    Returns
    -------
    str
        The competition results data in JSON format.
    """
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
