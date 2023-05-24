# EquiScoreMask

EquiScoremask is a Python application developed to display competition results for equestrian events. The application uses the Flask framework to provide a web application that reads results from an XML file and presents them in a tabular format.

## Requirements

- Python 3.x
- Flask 2.3.2
- Flask-Bootstrap 3.3.7.1
- python-socketio 5.8.0
- watchdog 3.0.0

## Installation

1. Make sure Python is installed on your system (version 3.7 or higher).
2. Clone the repository from GitHub: [https://github.com/nefas83/EquiScoreMask.git](https://github.com/nefas83/EquiScoreMask.git)
3. Navigate to the project directory: `cd EquiScoreMask`
4. Create a virtual environment: `python -m venv venv`
5. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
6. Install the required dependencies: `pip install -r requirements.txt`

## Usage

1. Place your XML file containing the competition results in the `data` folder and name it accordingly (e.g., `equiscore.xml`). Or change the path to the `equiscore.xml`on your filesystem at the `app.py` file.
 ``` python
 xml_data = XMLData('<pathTo *.xml>')
 ```
2. Update the `flags.json` file in the `static` folder with the flag information for the countries you want to display in the results.

   - The ISO2 Country code has to changed to match the XML content.
3. Start the application: `python app.py`
4. Open a web browser and navigate to `http://localhost:5000` or the IP-Adress of your computer `http://192.168.x.x:5000`
5. The competition results will be displayed in a table, sorted by the participants' rank. The countries will be represented as flags based on the information from the `flags.json` file.

## Customization

- To customize the appearance of the application, you can edit the `styles.css` file in the `static` folder.
- To modify the XML structure of the competition results file, edit the `parse_xml` function in the `app.py` file.
- To add additional functionality or extend the logic, you can modify the code accordingly.
- If you want to change the logo at the top of the page, you have to replace the `logo.png` at the `static` folder.

## License

This project is licensed under the GNU v3 License. See the `LICENSE` file for more information.

## Notes

- Make sure the XML file contains valid competition result data and the required information is structured correctly.
- Double-check that the `flags.json` file has been correctly updated and contains the flag information for the respective countries.
- For any questions or issues, feel free to contact the developer: [gilbert.rauch@gmail.com](mailto:gilbert.rauch@gmail.com)

Enjoy using EquiScoreMask!

## Support
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/gilbertrau)
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/W7W8LKVL0)

--- 

# EquiScoreMask

EquiScoremask ist eine Python-Anwendung, die Ergebnisse von Reitwettbewerben anzeigt. Die Anwendung liest XML-Daten mit den Wettbewerbsergebnissen und präsentiert diese in tabellarischer Form auf einer Webseite.

## Anforderungen

- Python 3.x
- Flask 2.3.2
- Flask-Bootstrap 3.3.7.1
- python-socketio 5.8.0
- watchdog 3.0.0

## Installation

1. Stelle sicher, dass Python 3 auf deinem System installiert ist.
2. Klonen das EquiScoreMask-Projekt von GitHub: [https://github.com/nefas83/EquiScoreMask.git](https://github.com/nefas83/EquiScoreMask.git)
3. Navigiere in das Projektverzeichnis: `cd EquiScoreMask`
4. Erstelle und aktiviere eine virtuelle Umgebung (optional, aber empfohlen):  `python -m venv venv`
5. Aktivieren Sie die virtuelle Umgebung:
   - Auf Windows: `venv\Scripts\activate`
   - Auf macOS und Linux: `source venv/bin/activate`

6. Installiere die erforderlichen Pakete aus der `requirements.txt`-Datei: `pip install -r requirements.txt`

## Verwendung

1. Platzieren Sie Ihre XML-Datei mit den Wettbewerbsergebnissen im data-Ordner und benennen Sie sie entsprechend (z.B. `equiscore.xml`). Oder ändern Sie den Pfad zur `equiscore.xml` auf Ihrem Dateisystem in der `app.py`.
 ``` python
 xml_data = XMLData('<pathTo *.xml>')
 ```
2. Aktualisieren Sie die flags.json-Datei im static-Ordner mit den Flaggeninformationen für die Länder, die Sie in den Ergebnissen anzeigen möchten.

   - Der ISO2-Ländercode muss geändert werden, um dem XML-Inhalt zu entsprechen.
3. Starten Sie die Anwendung: `python app.py`
4. Öffnen Sie einen Webbrowser und navigieren Sie zu `http://localhost:5000` oder der IP-Adresse Ihres Computers `http://192.168.x.x:5000`
5. Die Wettbewerbsergebnisse werden in einer Tabelle angezeigt, sortiert nach dem Rang der Teilnehmer. Die Länder werden als Flaggen dargestellt, basierend auf den Informationen aus der `flags.json`-Datei.

## Anpassung

- Um das Aussehen der Anwendung anzupassen, können Sie die styles.css-Datei im static-Ordner bearbeiten.
- Um die XML-Struktur der Wettbewerbsergebnisdatei zu ändern, bearbeiten Sie die parse_xml-Funktion in der `app.py`-Datei.
- Um zusätzliche Funktionen hinzuzufügen oder die Logik zu erweitern, können Sie den Code entsprechend ändern.
- Flaggen: Die Flaggen werden aus der Datei `flags.json` geladen. Du kannst diese Datei anpassen oder durch eine andere Datei mit den Flaggen ersetzen.
- Zum ändern des Logo im Banner, ersetzen sie die Datei `logo.png` im Verzeichniss `static`.

## Hinweis

Dieses Projekt wurde mit Flask entwickelt, einem Webframework für Python. Flask ermöglicht eine schnelle und einfache Entwicklung von Webanwendungen. Weitere Informationen zu Flask findest du in der offiziellen [Dokumentation](https://flask.palletsprojects.com/).

- Stellen Sie sicher, dass die XML-Datei gültige Wettbewerbsergebnisdaten enthält und die erforderlichen Informationen korrekt strukturiert sind.
- Überprüfen Sie sorgfältig, ob die flags.json-Datei korrekt aktualisiert wurde und die Flaggeninformationen für die jeweiligen Länder enthält.
- Bei Fragen oder Problemen können Sie sich gerne an den Entwickler wenden: [gilbert.rauch@gmail.com](mailto:gilbert.rauch@gmail.com)

Viel Spaß mit EquiScoreMask!

## Lizenz

Dieses Projekt ist unter der GNU v3-Lizenz lizenziert. Weitere Informationen findest du in der Datei `LICENSE`.

## Support
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/gilbertrau)
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/W7W8LKVL0)
