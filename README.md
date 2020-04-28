# Fotobox für Touchscreen

Eine einfache Python3 Anwendung für Raspberry Pi, um
 * Kamerabilder auf den Bildschirm zu streamen (Liveview)
 * Aufnahmen anzustoßen
 * Auszuwählen, ob die lezte Aufnahme gespeichert oder gelöscht werden soll

1. Nach dem Start wird die ganze Zeit eine Vorschau dargestellt/gestreamt (preview).
2. Drückt man den Kameraknopf, wird ein Countdown gestartet.
3. Ist dieser abgelaufen, wird ein Foto erzeugt (capture) und dargestellt.
4. Der Anwender kann das Foto verwerfen oder akzeptieren.
5. Das Bild wird auf der SD-Karte der Kamera und (wenn vorhanden) auf einem USB-Stick abgelegt.
6. Danach kehrt das Programm zum Vorschau-Modus zurück 
7. Es wird kontinuierlich geprüft, ob ein USB-Stick vorhanden ist.
8. Es wird kontinuierlich der Platz von SD-Karte und USB-Stick geprüft.

Fehlen SD-Karte oder USB-Stick oder unterschreitet der verfügbare Platz einen bestimmten Wert, werden entsprechende Symbole angezeigt.
Diese können einfach weggedrückt werden, ohne, dass sich etwas am Verhalten ändert.

Die Fotobox verwendet folgende Python-Bibliotheken:
* [gphoto2](https://pypi.org/project/gphoto2/)
* [PyQt5](https://pypi.org/project/PyQt5/) 
 
Die Anwendung läuft im Vollbild ohne Mauszeiger.

Zusätzlich gibt es ein Skript, was für das automatische Starten beim Boot verwendet werden kann und was den Pi neu startet, sobald es einen Abbruch durch Fehler gab.

## Installation
Was am Pi benötigt wird:
* USB-Tastatur
* USB-Maus
* Internetzugang (Kabel oder WLAN)

### Raspberry Image
Am besten verwendet man das offizielle [Raspbian-Image mit empfohlener Software](https://www.raspberrypi.org/downloads/raspbian/). Dort sind bereits die meisten notwendigen Bibliotheken installiert.
Mit [balena Etcher](https://www.balena.io/etcher/) oder dem offiziellen [Imager für Windows](https://downloads.raspberrypi.org/imager/imager.exe) kann das Image auf eine SD-Karte gelschrieben werden.

### Erster Start
Unter Verwendung von diesem Image wird beim ersten Start die initiale Konfiguration durchlaufen. Hier ist der Internetzugang wichtig. Es wird dabei nach einem WLAN gesucht, da sollte man das Passwort bereithalten.

Bei besonders komplizierten Passwörtern empfiehlt es sich, die Textdatei auf einen USB-Stick zu kopieren und am Pi einzustecken. Dort ist der Stick auf dem Desktop sichtbar, die Textdatei kann mit einem Editor geöffnet und der Schlüssel mit Rechtsklick+kopieren in die Zwischenablage geladen werden. 

Speziell die automatische Installation der Updates erfordert Geduld. Abschließend wird neu gebootet und alls sollte in Ordnung sein.

### Deaktivieren Bildschirmschoner (blank screen)
Nach der Installation ist der Bildschirmschoner aktiviert. Nach ca. 10-15 Minuten wird der Bildschirm schwarz.

Um dieses Verhalten zu deaktivieren, geht man im Startmenü des Pi in Einstellungen -> Raspberry-Pi-Konfiguration. Da kann man im Reiter 'Display' das 'Screen Blanking' deaktivieren. OK klicken und fertig.  

### Installation zusätzlicher Software
#### Gphoto2
Da bei dem Image mit empfohlener Software fast alls vorhanden ist, muss nur die Software für Gphoto2 installiert werden.

```
sudo apt install gphoto2 libgphoto2-dev
sudo python3 -m pip install gphoto2
```

#### Fotobox
Die Fotobox wird mit

```git clone https://github.com/cybrix-dev/fotobox```

heruntergeladen. Anschließend kann sie manuell über

``python3 fotobox``

gestartet werden.

### Autostart
In dem Verzeichnis der Fotobox liegt ein Skript, mit dem die Fotobox gestartet und im 
Fehlerfall der Pi neu gestartet wird.

Damit sollen Fehler umgangen werden, die im laufenden Betrieb auftreten. 
Aktuell kann es dabei aber dazu führen, dass der Pi in eine endlose Bootschleife kommt 
und neu installiert werden muss. Deshalb wurde der reboot vorerst deaktiviert.

Um die Fotobox zumindest beim Boot direkt starten zu lassen, muss folgendes gemacht werden:

```
mkdir .config/autostart
cp fotobox/fotobox.desktop .config/autostart/
```

Damit wird das Skript ``.autostart`` bei jedem Start des Pi ausgeführt. 
Und zwar zu einem Zeitpunkt, zu dem der Desktop bereits aktiv ist und USB-Sticks automatisch 
erkannt und aktiviert wurden.

## Architektur

### Threading
Die Applikation läuft in 2 Threads:
* Der Haupt-Thread verarbeitet das GUI und die Benutzerinteraktion.
* Der zweite Thread kapselt die Kamera-Kommunikation, um das Livebild etwas flüssiger darzustellen.

#### Datenaustausch
Daten vom Hauptthread in den Kamera-Thread werden entweder über eine Python-Queue übertragen
(aktuell nur ein Kommandowert) oder ungesichert über Klassenvariablen ausgetauscht.

Daten vom Kamera-Thread zum Hauptthread werden über die Signal/Slot-Verbindungen von Qt übertragen.

### Quellcode
Die Applikation ist aufgeteilt auf folgende Dateien:

* ``gui.ui       `` - Wird über den Qt-Creator bearbeitet, GUI mit Anordnung der einzelnen Elemente
* ``ui.py        `` - Generierte Datei, erzeugt mit `pyuic5 -x gui.ui -o ui.py`
* ``box.py       `` - Hauptklasse, verschaltet alle nderen Module
* ``const.py     `` - beinhaltet fixe Werte, die auch nicht konfiguriert werden sollten
* ``config.py    `` - beinhaltet Werte, die man ggf. ändern kann -> siehe Offener Punkt [Konfiguration](#konfiguration)
* ``cam.py       `` - kapselt alle Verweise auf ``gphoto2``
* ``cam_thread.py`` - kapselt alle Verweise auf ``cam.py``; notwendig um gleichzeitige Zugriffe aus unterschiedlichen Threads zu vermeiden
* ``__main__.py  `` - Startpunkt der Applikation, ermöglicht den Aufruf ``python3 fotobox``
* ``__init__.py  `` - leer

### Modifikationen am GUI
Wenn das GUI geändert werden soll, sollte das mit der `gui.ui` und dem Creator von Qt gemacht werden.
Sind die Änderungen abgeschlossen, wird mit `pyuic5 -x gui.ui -o ui.py` die Datei `ui.py` aktualisiert.

**WICHTIG** Die Qt-Bibliothek des Pi kennt `PlaceholderText` nicht. Unter Umständen wird dieser aber in 
der `gui.ui` hinterlegt und dadurch in `ui.py` verwendet.

Das führt zum Absturz, wenn das GUI initialisiert wird. Nach Aktualisieren der `ui.py` deshalb 
auf dem Zielgerät testen mit `python3 ui.py`. Kommt es dabei zum Absturz mit , muss folgendes aus 
`gui.ui` entfernt werden:
```
```

### Debugging
Sollte ``gphoto2`` in Python nicht importiert werden können, dann wird im Modul ``cam.py`` der Dbug-Modus aktiviert.
Damit werden im Livemodus immer wieder drei Bilder übertragen (`./icons/test1.jpg`, `./icons/test2.jpg`, 
`./icons/test3.jpg`) und bei Aufnahme `./icons/test4.jpg`. Der verbleibende Platz auf der SD-Karte wird mit einem festen 
Wert (50MB) angegeben.

Andere Funktionen aus `cam.py` sind nicht verfügbar (Speichern auf USB-Stick, Löschen).

Die Abfrage, ob ein USB-Stick vorhanden ist und wieviel Platz übrig ist, erfolgt mit dem Kommandozeilen-
Aufruf `df -l`. Dieses Kommando ist auf Windows-Systemen nicht verfügbar. Schlägt der Aufruf fehl, wird eine Antwort
mit verbleibenden 50MB zurück gegeben.

Damit ist es möglich, verschiedene Teile auch unter Windows laufen zu lassen (ohne tatsächliche Kamera-Steuerung und ohne Zugriff auf USB). 

## Offene Punkte

### Fehler-Handling
Falls es Probleme mit der Kommunikation zwischen Kamera und Pi gibt, stürzt die Applikation ab.
Gleiches gilt für das Speichern der Bilder auf dem USB-Stick.

Speziell wenn die Applikation bei Fehlern einen automatischen Reboot veranlasst, muss das überarbeitet werden,
damit keine Deadloop erzeugt wird.

### Konfiguration
Sämtliche Parameter sind aktuell fest hinterlegt. Verschiedene Optionen bieten sich jedoch an, sie im GUI zu konfigurieren.
Dabei muss zwischen Parametern unterschieden werden, die pro System (bei Installation) und pro Benutzer festgelegt sind.

Bei Installation/Systemeinstellung:
* Verzeichnis, um USB-Stick zu detektieren
* Schwellwert 'Wenig Speicher' (Warnung, wenn weniger vorhanden)
* Typ Kamera-Speicher (aktuell nur SD-Karte)
* Darstellung gespiegelt (abhängig von Kamera)

Für Anwender:
* Dauer Countdown
* USB-Stick ja/nein
* Verzeichnis auf USB-Stick
* Benennung Dateien auf USB-Stick