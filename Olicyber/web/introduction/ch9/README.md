# Web 09 - HTTP: una richiesta POST con body JSON

application/x-www-form-urlencoded, nonostante la sua diffusione storica, è un formato obsolescente e poco adatto a rappresentare dati strutturati, per cui è stato gradualmente soppiantato, in quelle applicazioni che non richiedano compatibilità con il meccanismo di invio tradizionale dei form web, da formati più moderni come XML e JSON.

Quest'ultimo, in particolare, in virtù della sua semplicità d'uso in JavaScript, il più diffuso linguaggio di programmazione web, si è rapidamente affermato come nuovo standard de-facto, per cui librerie come requests offrono scorciatoie per inviare richieste POST con body codificato in JSON con la stessa facilità offerta per il vecchio sistema, oltre che per decodificare automaticamente eventuali risorse restituite in tale formato dal server nelle risposte.

Analogamente alla precedente, l'obiettivo di questa challenge è inviare una richiesta POST verso la risorsa http://web-09.challs.olicyber.it/login fornendo in formato JSON la coppia di valori "username": "admin" e "password": "admin", analogamente a un'ipotetica operazione di login nei confronti di un servizio web. La flag sarà restituita nel testo della risposta all'operazione.

# writeup

La challenge consiste nell'inviare una richiesta POST all'url http://web-09.challs.olicyber.it/login nel formato application/json;
con un payload contenete la coppia di valori: username=admin e password=admin.

In questo caso per specificare nell'header che il formato della richiesta è json, useremo il parametro Content-Type 

Json, a differenza del x-www-form-urlencoded, non usa l'uguale per assegnare un valore, ma usa i ':'.
In json i valori andranno messi in mezzo agli doppi apici, tutto all'interno delle parentesi graffe, per dividere più valori si usa la virgola.

Per questa challenge possiamo utilizzare curl o requests di python.

### payload

json:
```json
{"username": "admin", "password": "admin"}
```

header:
```
Content-Type: application/json
```

# exploit

script in bash:
```bash
curl -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin"}' http://web-09.challs.olicyber.it/login
```

script in python
```bash
python3 ch9.py
```

ottenendo la flag:
> flag{w31c0m3_70_7h3_y34r_2000}