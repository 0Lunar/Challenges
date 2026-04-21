# Web 10 - HTTP: il metodo OPTIONS

Abbiamo finora osservato vari modi di interagire con le risorse che un server HTTP mette a disposizione, sotto forma dei verbi GET, HEAD e POST, ma non tutte queste operazioni sono supportate da tutti i tipi di risorsa. Non ha senso ad esempio eseguire una richiesta POST nei confronti di una risorsa di sola lettura. Per conoscere le operazioni supportate da una data risorsa, HTTP mette a disposizione il verbo OPTIONS. Una richiesta OPTIONS restituisce l'elenco dei verbi supportati all'interno dello header Allow.

Talvolta può essere interessante cercare di utilizzare intenzionalmente un verbo non supportato. Normalmente un server dovrebbe gestire richieste non supportate in maniera pulita, ma in presenza di configurazioni errate o errori di programmazione, utilizzare un metodo imprevisto può indurre un crash. I crash e più in generale le operazioni non anticipate possono rivelare informazioni interessanti che nell'utilizzo normale di un servizio web sono nascoste.

L'obiettivo di questa challenge è determinare l'insieme dei verbi supportati per la risorsa http://web-10.challs.olicyber.it/, provare a utilizzarne uno poco comune e imprevisto ed osservare la risposta. La libreria requests mette a disposizione funzioni analoghe alla funzione get anche per i verbi meno comuni, come put e patch.

# writeup

La challenge consiste nell'inviare una richiesta di un tipo non frequentemente utilizzato all'url http://web-10.challs.olicyber.it/ e visualizzare gli header per trovare la flag.

solitamente i metodi più utilizzati sono GET e POST, quindi noi useremo il metodo PUT.

Per questa challenge possiamo utilizzare curl o requests di python.

In curl, per specificare il metodo con cui trasmettere la richiesta, si usa il parametro -X seguito dal nome del metodo.

Il messaggio che dovremo ricevere dal server è il 500 (Internal server error).

P.S. nello script in bash, filtrerò il testo con dei tools di linux, ma non è neccessario utilizzarli.

# exploit

script in bash:
```bash
curl -X PUT -I http://web-10.challs.olicyber.it/ | grep X-Flag | cut -d ":" -f2
```

script in python (ch10):
```bash
python3 ch10.py
```

ottenendo la flag:
> flag{br34king_7h3_ru135}
