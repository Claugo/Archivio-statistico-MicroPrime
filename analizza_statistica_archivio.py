"""
Analizzatore Primi da File Pickle - MicroPrime Studio
Legge numeri primi da file pickle (formato ruota mod 60) e li analizza
"""

import sys
import json
import math
import pickle
from datetime import datetime
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QApplication

# === CONFIGURAZIONE: lasciare None per leggere i dati esistenti ===
FILE_PICKLE = None


def formatta_numero(n):
    """Formatta numero con punti: 1234567 -> 1.234.567"""
    return f"{n:,}".replace(",", ".")


def carica_pickle_come_lista(file_pickle):
    """
    Carica un file pickle MicroPrime e restituisce:
    - inizio: primo numero dell'intervallo
    - fine: ultimo numero dell'intervallo  
    - primi_trovati: lista di tutti i numeri primi (interi)
    """
    with open(file_pickle, "rb") as f:
        lista = pickle.load(f)
    
    # Estrai riferimento
    rif_raw = lista[-1]
    rif = rif_raw[0] if isinstance(rif_raw, list) else rif_raw
    
    # Ricostruisci tutti i primi
    primi_trovati = []
    for i in range(len(lista) - 1):
        for offset in lista[i]:
            n = (rif * 60 + 10) + 60 * i + offset
            primi_trovati.append(n)
    
    # Calcola intervallo
    inizio = rif * 60 + 10
    fine = inizio + 60 * (len(lista) - 1)
    
    return inizio, fine, primi_trovati


class FinestraDati(QtWidgets.QMainWindow):
    def __init__(self):
        super(FinestraDati, self).__init__()
        # Carichiamo il file .ui
        uic.loadUi("finestra_dati.ui", self)

        # Dati delle statistiche
        self.dati_statistiche = None

        # Collegamento pulsanti
        self.pushButton_esporta.clicked.connect(self.salva_statistiche)
        self.pushButton_carica.clicked.connect(self.carica_statistiche)
        self.pushButton_chiudi.clicked.connect(self.close)

        # Aggiungi pulsante per caricare file primi
        self.pushButton_carica_file = QtWidgets.QPushButton(
            "📂 Carica File Pickle", self
        )
        self.pushButton_carica_file.clicked.connect(self.carica_file_primi)

        # Trova il layout dei pulsanti e aggiungi il nuovo pulsante
        # (assumendo che ci sia un layout orizzontale per i pulsanti)
        try:
            # Cerca il parent dei pulsanti esistenti
            parent_widget = self.pushButton_esporta.parent()
            layout = parent_widget.layout()
            if layout:
                layout.insertWidget(0, self.pushButton_carica_file)
        except:
            # Se non riesce, posiziona il pulsante manualmente
            self.pushButton_carica_file.setGeometry(10, 10, 200, 30)

    def carica_file_primi(self):
        """Carica file pickle con primi e calcola statistiche"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleziona File Pickle", "", "Pickle Files (*.pkl);;All Files (*)"
        )

        if not file_path:
            return

        self.elabora_file_pickle(file_path)

    def elabora_file_pickle(self, file_path):
        """Elabora un file pickle e calcola le statistiche"""
        try:
            # Carica il pickle e trasformalo nel formato atteso
            print(f"📂 Caricamento file pickle: {file_path}")
            inizio, fine, primi_trovati = carica_pickle_come_lista(file_path)

            print(f"📊 Intervallo: {formatta_numero(inizio)} - {formatta_numero(fine)}")
            print(f"🔢 Primi trovati: {formatta_numero(len(primi_trovati))}")

            if not primi_trovati:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Attenzione",
                    f"Nessun primo trovato nel file.\n\n"
                    f"Intervallo: {formatta_numero(inizio)} - {formatta_numero(fine)}",
                )
                return

            # Prepara parametri
            parametri = {
                "inizio": inizio,
                "fine": fine,
                "radice": int(math.sqrt(fine)) + 1,
                "file_usati": file_path,
                "divisori_caricati": len(primi_trovati),
                "debug_attivo": False,
            }

            # Calcola statistiche
            self.dati_statistiche = self.calcola_statistiche(
                primi_trovati, parametri
            )

            # Popola finestra
            self.popola_finestra()

            QtWidgets.QMessageBox.information(
                self,
                "Successo",
                f"File caricato e analizzato con successo!\n\n"
                f"Primi analizzati: {formatta_numero(len(primi_trovati))}",
            )

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Errore", f"Errore nel caricamento del file:\n{str(e)}"
            )
            import traceback
            traceback.print_exc()

    def calcola_statistiche(self, primi_trovati, parametri):
        """Calcola tutte le statistiche dai primi trovati"""

        if not primi_trovati:
            return None

        inizio = parametri["inizio"]
        fine = parametri["fine"]
        ampiezza = fine - inizio

        # ===== STATISTICHE BASE =====
        count_primi = len(primi_trovati)
        densita_reale = (count_primi / ampiezza) * 100 if ampiezza > 0 else 0

        # Densità teorica (Teorema dei numeri primi)
        medio = (inizio + fine) / 2
        densita_teorica = (1 / math.log(medio)) * 100 if medio > 1 else 0
        differenza = densita_reale - densita_teorica

        # ===== ANALISI GAP =====
        gap_lista = []
        for i in range(1, len(primi_trovati)):
            gap = primi_trovati[i] - primi_trovati[i - 1]
            gap_lista.append(gap)

        gap_min = min(gap_lista) if gap_lista else 0
        gap_max = max(gap_lista) if gap_lista else 0
        gap_medio = sum(gap_lista) / len(gap_lista) if gap_lista else 0

        # ===== DISTRIBUZIONE MODULO 60 =====
        distribuzione_mod60 = {}
        posizioni_valide = [
            1,
            7,
            11,
            13,
            17,
            19,
            23,
            29,
            31,
            37,
            41,
            43,
            47,
            49,
            53,
            59,
        ]

        for pos in posizioni_valide:
            distribuzione_mod60[pos] = 0

        for primo in primi_trovati:
            mod = primo % 60
            if mod in distribuzione_mod60:
                distribuzione_mod60[mod] += 1

        # ===== PRIMI SPECIALI =====
        gemelli = []  # gap = 2
        cugini = []  # gap = 4
        sexy = []  # gap = 6

        for i in range(len(gap_lista)):
            gap = gap_lista[i]
            if gap == 2:
                gemelli.append((primi_trovati[i], primi_trovati[i + 1]))
            elif gap == 4:
                cugini.append((primi_trovati[i], primi_trovati[i + 1]))
            elif gap == 6:
                sexy.append((primi_trovati[i], primi_trovati[i + 1]))

        # ===== COMPILA DATI =====
        return {
            "parametri": parametri,
            "statistiche": {
                "count_primi": count_primi,
                "ampiezza": ampiezza,
                "densita_reale": densita_reale,
                "densita_teorica": densita_teorica,
                "differenza": differenza,
            },
            "gap": {
                "gap_min": gap_min,
                "gap_max": gap_max,
                "gap_medio": gap_medio,
                "gap_lista": gap_lista[:100],  # Solo primi 100 per JSON
            },
            "mod60": distribuzione_mod60,
            "speciali": {
                "gemelli": gemelli[:50],  # Limita per JSON
                "cugini": cugini[:50],
                "sexy": sexy[:50],
            },
            "primi": primi_trovati[:1000],  # Solo primi 1000 per visualizzazione
        }

    def popola_finestra(self):
        """Popola tutti i widget della finestra con i dati"""
        if not self.dati_statistiche:
            return

        stats = self.dati_statistiche["statistiche"]
        gap = self.dati_statistiche["gap"]
        mod60 = self.dati_statistiche["mod60"]
        speciali = self.dati_statistiche["speciali"]
        primi = self.dati_statistiche["primi"]
        params = self.dati_statistiche["parametri"]

        def safe_set_text(widget_name, text):
            """Imposta il testo di un widget se esiste"""
            if hasattr(self, widget_name):
                getattr(self, widget_name).setText(str(text))

        # ===== INFO GENERALI =====
        inizio = params["inizio"]
        fine = params["fine"]
        safe_set_text(
            "label_intervallo", f"{formatta_numero(inizio)} → {formatta_numero(fine)}"
        )
        safe_set_text("label_ampiezza", f"{formatta_numero(stats['ampiezza'])} numeri")
        safe_set_text("label_count_primi", f"{formatta_numero(stats['count_primi'])}")
        safe_set_text("label_file_usati", str(params.get("file_usati", "N/A")))
        safe_set_text(
            "label_divisori", f"{formatta_numero(params.get('divisori_caricati', 0))}"
        )

        # ===== DENSITÀ =====
        safe_set_text("label_densita_reale", f"{stats['densita_reale']:.6f}%")
        safe_set_text("label_densita_teorica", f"{stats['densita_teorica']:.6f}%")

        diff = stats["differenza"]
        color = "green" if diff >= 0 else "red"
        safe_set_text("label_differenza", f"{diff:+.6f}%")
        if hasattr(self, "label_differenza"):
            self.label_differenza.setStyleSheet(f"color: {color}; font-weight: bold;")

        # Progress bar densità
        if hasattr(self, "progressBar_densita"):
            valore_progress = min(100, max(0, int(stats["densita_reale"] * 10)))
            self.progressBar_densita.setValue(valore_progress)

        # ===== ANALISI GAP =====
        safe_set_text("label_gap_min", str(gap["gap_min"]))
        safe_set_text("label_gap_max", str(gap["gap_max"]))
        safe_set_text("label_gap_medio", f"{gap['gap_medio']:.2f}")

        # ===== PRIMI SPECIALI =====
        safe_set_text("label_gemelli", f"{len(speciali['gemelli'])} coppie")
        safe_set_text("label_cugini", f"{len(speciali['cugini'])} coppie")
        safe_set_text("label_sexy", f"{len(speciali['sexy'])} coppie")

        # ===== DISTRIBUZIONE MOD 60 =====
        if hasattr(self, "textBrowser_mod60"):
            try:
                # Costruisci testo formattato per il textBrowser
                html = "<table border='1' cellpadding='5' style='border-collapse: collapse;'>"
                html += "<tr style='background-color: #e0e0e0; font-weight: bold;'>"
                html += "<th>Posizione</th><th>Count</th><th>%</th></tr>"

                for pos in sorted(mod60.keys()):
                    count = mod60[pos]
                    percentuale = (
                        (count / stats["count_primi"] * 100)
                        if stats["count_primi"] > 0
                        else 0
                    )

                    html += f"<tr>"
                    html += f"<td align='center'>{pos}</td>"
                    html += f"<td align='center'>{formatta_numero(count)}</td>"
                    html += f"<td align='center'>{percentuale:.2f}%</td>"
                    html += f"</tr>"

                html += "</table>"
                self.textBrowser_mod60.setHtml(html)
            except Exception as e:
                print(f"⚠️ Errore nel popolare textBrowser_mod60: {e}")
        else:
            print("⚠️ Widget textBrowser_mod60 non trovato nell'interfaccia")

        # ===== TABELLA PRIMI =====
        if hasattr(self, "tableWidget_primi"):
            try:
                self.tableWidget_primi.setRowCount(0)

                # Imposta larghezza colonne prima di popolare
                self.tableWidget_primi.setColumnWidth(
                    0, 250
                )  # Numero (largo per 22 cifre)
                self.tableWidget_primi.setColumnWidth(1, 80)  # Posizione
                self.tableWidget_primi.setColumnWidth(2, 80)  # Gap
                self.tableWidget_primi.setColumnWidth(3, 80)  # Mod 60
                self.tableWidget_primi.setColumnWidth(4, 150)  # Tipo Speciale

                for idx, primo in enumerate(primi):
                    mod = primo % 60

                    # Calcola gap
                    if idx > 0:
                        gap_val = primo - primi[idx - 1]
                    else:
                        gap_val = 0

                    # Tipo speciale
                    tipo_speciale = ""
                    if gap_val == 2:
                        tipo_speciale = "👯 Gemello"
                    elif gap_val == 4:
                        tipo_speciale = "👥 Cugino"
                    elif gap_val == 6:
                        tipo_speciale = "💋 Sexy"

                    row = self.tableWidget_primi.rowCount()
                    self.tableWidget_primi.insertRow(row)

                    try:
                        self.tableWidget_primi.setItem(
                            row, 0, QTableWidgetItem(formatta_numero(primo))
                        )
                        self.tableWidget_primi.setItem(
                            row, 1, QTableWidgetItem(str(idx + 1))
                        )
                        self.tableWidget_primi.setItem(
                            row, 2, QTableWidgetItem(str(gap_val))
                        )
                        self.tableWidget_primi.setItem(
                            row, 3, QTableWidgetItem(str(mod))
                        )
                        self.tableWidget_primi.setItem(
                            row, 4, QTableWidgetItem(tipo_speciale)
                        )

                        # Colora riga
                        if tipo_speciale:
                            for col in range(5):
                                item = self.tableWidget_primi.item(row, col)
                                if item:  # Verifica che l'item esista
                                    if "Gemello" in tipo_speciale:
                                        item.setBackground(Qt.yellow)
                                    elif "Cugino" in tipo_speciale:
                                        item.setBackground(Qt.cyan)
                                    elif "Sexy" in tipo_speciale:
                                        item.setBackground(Qt.magenta)
                    except Exception as e:
                        print(f"⚠️ Errore alla riga {idx}: {e}")
                        break  # Ferma se c'è un errore

                print(
                    f"✅ Popolate {self.tableWidget_primi.rowCount()} righe nella tabella"
                )
            except Exception as e:
                print(f"⚠️ Errore nel popolare tableWidget_primi: {e}")
        else:
            print("⚠️ Widget tableWidget_primi non trovato")
    # **********************************************************************

    def salva_statistiche(self):
        """Salva statistiche in JSON con nome predefinito dinamico"""
        if not self.dati_statistiche:
            QtWidgets.QMessageBox.warning(self, "Attenzione", "Nessun dato da salvare!")
            return

        # --- LOGICA PER IL NOME DEL FILE ---
        import os

        # Recuperiamo il percorso del file originale dai dati caricati
        file_sorgente = self.dati_statistiche.get("parametri", {}).get("file_usati", "")

        if file_sorgente:
            # Estraiamo solo il nome (es. da "C:/test/lista_0007.pkl" a "lista_0007")
            nome_base = os.path.basename(file_sorgente)
            nome_solo_lista = os.path.splitext(nome_base)[0]
            nome_proposto = f"statistiche_{nome_solo_lista}.json"
        else:
            # Se non c'è un file pkl (es. hai caricato un json), usa la data
            nome_proposto = f"statistiche_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        # -----------------------------------

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salva Statistiche",
            nome_proposto,  # <--- Qui usiamo il nome costruito sopra
            "JSON Files (*.json)",
        )

        if file_path:
            try:
                with open(file_path, "w") as f:
                    json.dump(self.dati_statistiche, f, indent=2)

                QtWidgets.QMessageBox.information(
                    self, "Successo", f"Statistiche salvate in:\n{file_path}"
                )
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self, "Errore", f"Errore nel salvataggio:\n{str(e)}"
                )  

    # ******************************************************************************
    def carica_statistiche(self):
        """Carica statistiche da JSON"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Carica Statistiche", "", "JSON Files (*.json)"
        )

        if file_path:
            try:
                with open(file_path, "r") as f:
                    self.dati_statistiche = json.load(f)

                self.popola_finestra()

                QtWidgets.QMessageBox.information(
                    self, "Successo", f"Statistiche caricate da:\n{file_path}"
                )
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self, "Errore", f"Errore nel caricamento:\n{str(e)}"
                )


if __name__ == "__main__":
    print("=" * 70)
    print("📊 ANALIZZATORE PRIMI DA FILE PICKLE - MicroPrime Studio")
    print("=" * 70)
    # Mostra None se non impostato, altrimenti il percorso
    print(f"File pickle predefinito: {FILE_PICKLE}")
    print("Formato: ruota mod 60 con riferimento nell'ultimo elemento")
    print("=" * 70)
    print()

    app = QApplication(sys.argv)
    finestra = FinestraDati()
    finestra.show()

    # Carica automaticamente il file predefinito SOLO se è stato indicato (non è None)
    import os

    # Verifichiamo prima che FILE_PICKLE non sia None, poi che esista sul disco
    if FILE_PICKLE and os.path.exists(FILE_PICKLE):
        print(f"🚀 Caricamento automatico di: {FILE_PICKLE}")
        QTimer.singleShot(100, lambda: finestra.elabora_file_pickle(FILE_PICKLE))
    elif FILE_PICKLE is None:
        # Se è None, partiamo con la pagina vuota senza errori
        print("💡 Modalità consultazione: Nessun file predefinito.")
        print("   Carica un file Pickle o un archivio JSON per iniziare.")
    else:
        # Se c'è un percorso ma il file non esiste fisicamente
        print(f"⚠️ File predefinito non trovato: {FILE_PICKLE}")
        print("   Usa il pulsante '📂 Carica File Pickle' per selezionare un file")
        # Opzionale: attiva il dialogo solo se il file era atteso ma non trovato
        QTimer.singleShot(100, finestra.carica_file_primi)

    sys.exit(app.exec_())
