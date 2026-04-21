# Web 08 - HTTP: una richiesta post tradizionale

Finora ci siamo occupati esclusivamente di ottenere risorse dal server, ma HTTP fornisce anche strumenti per l'operazione inversa. Si tratta dei verbi POST e PUT, che permettono di inviare una risorsa al server, specificando un indirizzo di destinazione. La differenza tra i due metodi è sottile, ma noi ci occuperemo solo di POST, di gran lunga il più usato tra i due, essendo il sistema associato, ad esempio, all'invio del contenuto dei form che sono inclusi in molti siti web.

In linea di principio la rappresentazione della risorsa inviata nel corpo di una richiesta POST può utilizzare qualunque formato ma, per ragioni storiche, quando si utilizza il meccanismo di invio built-in del browser per inviare il contenuto di un form, questo viene normalmente codificato utilizzando un formato legacy specifico e utilizzato esclusivamente per i form web, noto nella classificazione MIME come application/x-www-form-urlencoded. Per questo motivo, molti server che ricevono dati dagli utenti tramite richieste POST accettano preferenzialmente questo formato, anche quando l'origine dei dati non è un form web.

L'obiettivo di questa challenge è inviare una richiesta POST verso la risorsa http://web-08.challs.olicyber.it/login fornendo nel formato application/x-www-form-urlencoded la coppia di valori "username": "admin" e "password": "admin", analogamente a un'ipotetica operazione di invio di un form di login su un sito web. La flag sarà restituita nel testo della risposta all'operazione.

Il formato application/x-www-form-urlencoded è relativamente complicato da riprodurre ma, esattamente come altre parti del protocollo HTTP osservate finora, rappresenta essenzialmente una sequenza di coppie chiave-valore, e la libreria requests fornisce un meccanismo per generarlo in automatico a partire da un dizionario Python. Si consiglia di utilizzare il parametro data della funzione post della libreria requests.

# writeup

La challenge consiste nell'inviare una richiesta POST all'url http://web-08.challs.olicyber.it/login nel formato: application/x-www-form-urlencoded;
con un payload contenente la coppia di valori: username=admin e password=admin.

Per questa challenge possiamo utilizzare curl o requests di python.

Per impostare un formato in una richiesta si può usare l'header accept.

Per inviare delle informazioni con curl possiamo usare il parametro -d seguito dal suo contenuto tra i doppi apici.

Per inviare la coppia di valori insieme dovremo utilizzare la '&'.

### payload

```
username=admin&password=admin
```

# exploit

script in bash:
```bash
curl -H "Accept: application/x-www-form-urlencoded" -d "username=admin&password=admin" http://web-08.challs.olicyber.it/login
```

script in python (ch8.py):
```bash
python3 ch8.py
```

ottenendo la flag:
> flag{53nding_d474_7h3_01d_w4y}