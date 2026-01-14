# Archivio statistico MicroPrime

Questo repository contiene un insieme di **analisi statistiche** relative agli archivi numerici generati nell’ambito della sperimentazione del metodo *MicroPrime*.

I dati sono resi pubblici esclusivamente per consentire **analisi indipendenti**, verifiche e osservazioni critiche.


## Contenuto del repository

Il repository include:

- **636 file in formato JSON**, ciascuno relativo all’analisi di un singolo archivio numerico
- una cartella `dati/` contenente i file JSON
- uno script Python di esempio per la lettura dei dati
- questo file README con la descrizione della struttura e del significato dei dati


## Descrizione dei dati

Ogni file JSON rappresenta **l’analisi statistica di un archivio numerico indipendente**, riferito a un intervallo di ampiezza pari a **500.000.000**.

L’insieme dei 636 archivi costituisce l’**archivio globale** utilizzato per la sperimentazione, che copre un quadrato numerico fino a \(10^{23}\).

L’archivio globale completo, così come è stato generato e memorizzato in formato binario (*pickle*), ha una dimensione di circa **41 GB** e non è incluso in questo repository per motivi puramente pratici legati alla dimensione dei dati.


## Tipo di analisi contenuta

I file JSON contengono esclusivamente **informazioni statistiche**, tra cui, a titolo esemplificativo:

- frequenza dei numeri primi all’interno dell’archivio
- distribuzione dei gap
- misure descrittive interne all’intervallo analizzato

Non sono presenti numeri primi grezzi né dati esterni all’archivio di riferimento.


## Distinzione tra archivio e generazione dinamica

L’esplorazione dei dati oltre l’archivio globale, fino al suo quadrato, **non è memorizzata** nei file presenti in questo repository.

Tali dati vengono generati dinamicamente dal programma di studio (*studia*) e riguardano intervalli numerici non archiviabili o non memorizzati in forma persistente.  
Essi **non fanno parte del dataset pubblicato**.


## Utilizzo dei dati

I file sono in **formato JSON standard** e possono essere analizzati con qualunque linguaggio o strumento adatto alla lettura di questo formato (Python, R, Julia, shell, ecc.).

Lo script Python fornito ha il solo scopo di mostrare un esempio di lettura dei dati e **non è necessario** per l’analisi.


## Coerenza dei dati e segnalazioni

Le statistiche contenute in questo archivio risultano **in linea con i dati ufficiali noti** sulla distribuzione dei numeri primi.

Chiunque, analizzando i file, riscontrasse **eventuali anomalie, discrepanze o comportamenti inattesi** è invitato a segnalarli, indicando l’archivio di riferimento e il tipo di osservazione effettuata.

Tali segnalazioni saranno utili per eventuali analisi di approfondimento.
