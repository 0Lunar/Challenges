# Web 06 - HTTP: ricevere un cookie

Quello dei cookie non è un meccanismo ridondante rispetto agli altri tipi di parametro osservati finora. A differenza di essi, infatti, il server è in grado di richiedere l'installazione di cookie da esso forniti nella memoria del client. Questi cookie vengono associati al sito che li ha generati, e possono contenere una data di scadenza.

Nei browser web questa memorizzazione viene gestita automaticamente, e i cookie salvati vengono automaticamente inviati nelle richieste successive inviate allo stesso sito, e cancellati al raggiungimento della data indicata. In questo modo essi possono essere utilizzati per identificare una sessione con un client specifico, ovvero una serie di richieste consecutive eseguite dallo stesso dispositivo, anche quando più dispositivi sono connessi a internet attraverso la stessa sottorete e quindi condividono indirizzo IP.

L'obiettivo di questa challenge è eseguire una richiesta GET alla risorsa http://web-06.challs.olicyber.it/token che cercherà di installare un cookie di sessione, una volta ottenuto il quale sarà possibile accedere a http://web-06.challs.olicyber.it/flag per ottenere la flag.

La funzione get della libreria requests usata finora adotta un modello senza stato, ovvero non utilizza nessuna delle informazioni precedentemente ricevute dal server nella composizione delle richieste successive. Per completare questa challenge, si consiglia di istanziare un oggetto di classe Session ed eseguire le richieste tramite il suo metodo get, che differisce dalla normale funzione get proprio per la caratteristica di salvare queste informazioni all'interno dell'oggetto emulando parzialmente il comportamento un browser.

# writeup

La challenge consiste nell'inviare una richiesta all'url http://web-06.challs.olicyber.it/token per ottenere il cookie che servirà ad accedere all'url successivo.

Una volta ottenuto il cookie 'segreto' potremo ottenere la flag inviando una richiesta all'url http://web-06.challs.olicyber.it/flag col cookie segreto.

Per questa challenge è consigliato utilizzare python, ma si può comunque utilizzare curl col parametro -I, che visualizza gli header di una richiesta (i cookie sono contenuti nell'header).

Nel caso si voglia utilizzare curl, ci sarà bisogno di filtrare il testo.

# exploit

script in bash:
```bash
TOKEN=$(curl -I http://web-06.challs.olicyber.it/token | grep Set-Cookie | cut -d ":" -f2 | cut " " -f2)
curl --cookie $TOKEN http://web-06.challs.olicyber.it/flag
```

script in python (ch6.py):
```bash
python3 ch6.py
```

ottenendo la flag:
> flag{7w0_574g3_4cc3s5}