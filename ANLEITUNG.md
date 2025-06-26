# Schritt-für-Schritt-Anleitung

Diese Kurzanleitung richtet sich an Einsteiger und beschreibt, wie Sie das "SongArchiv"-Programm in einer frischen Umgebung ausführen.

1. **Python installieren**
   Stellen Sie sicher, dass Python 3.11 oder neuer auf Ihrem System verfügbar ist. Unter Ubuntu können Sie z.B. Folgendes ausführen:
   ```bash
   sudo apt-get install python3 python3-venv python3-pip
   ```

2. **Projekt herunterladen**
   Klonen Sie das Repository oder laden Sie den Quellcode als ZIP-Datei herunter. Mit `git` funktioniert das so:
   ```bash
   git clone <REPOSITORY-URL>
   cd TOOL
   ```
   Ersetzen Sie `<REPOSITORY-URL>` durch die Adresse dieses Projekts.

3. **Virtuelle Umgebung anlegen (empfohlen)**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```

5. **Programm starten**
   ```bash
   python main.py
   ```
   Beim ersten Start werden automatisch die Datenbanken im Ordner `db` erstellt.

6. **Test-Suite ausführen** (optional)
   ```bash
   python selftest.py
   ```
   Falls ein Test scheitert, versucht das Skript automatisch eine Reparatur und startet die Tests erneut.

7. **Plugins nutzen** (optional)
   Legen Sie Plugins im Ordner `plugins` ab. Diese werden beim Start automatisch eingelesen.

Fertig! Die Anwendung sollte nun wie beschrieben funktionieren.
