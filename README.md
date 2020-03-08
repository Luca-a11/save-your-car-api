# SaveYourCar API

Questo è un servizio API, sviluppato in Flask.

# File di avvio: app.py
    Nel file di avvio app.py viene importata l'istanza app di flask e mandata in run qualora si chiami il file.

# Package app:
    Il pacchetto app è dotato di un file init dove son presenti tutte le configurazioni, le istanze dell'app Flask e dei suoi wrapper, nonchè la registrazione dei namespace.
    Contine inoltre tre moduli:
    Users, Cars e Reminders:
    In ogni modulo son presenti models e i controllers.
  - Models:
        - Vengono definite le classi corrispondeti alle tabelle relative al modulo di appartenenza.
        - Contengono degli schemi necessari a trasformare le classi in dizionari. Questi son necessari al fine di restituire le query in un formato valido.
        - Ad alcune classi sono annesse delle funzioni.
  -  Controllers:
        Viene definito il namespace relativo al modulo e tutti gli endpoint ad esso annessi.

# Avvio:

    Per avviare il programma:
     - avviare, in un terminale, un virtualenvironmant python
     - installare i requirements
     - posizionarsi nella cartella sycAPI
     - avviare l'app con python app.py