# Web 04 - HTTP: l'header Accept

Quello di risorsa, in HTTP, è un concetto molto astratto. Una risorsa non designa necessariamente un file su un disco, ma potrebbe tranquillamente essere un dispositivo hardware, il contenuto di un database, l'output di un programma, o più in generale qualsiasi cosa sia rappresentabile astrattamente come una collezione di dati.

Quando "richiediamo una risorsa" tramite HTTP, non stiamo veramente ricevendo la risorsa originale (che in certi casi non è neanche fisicamente trasferibile tramite la rete, si pensi all'esempio di un dispositivo hardware), bensì una sua rappresentazione.

Le risorse che vengono offerte da un server hanno solitamente una singola rappresentazione, ma in alcuni casi è possibile richiedere (e ricevere) più rappresentazioni equivalenti, in modo da poter scegliere il formato che è più semplice da elaborare per il client.

Lo header Accept inviato come parte della richiesta specifica una lista di formati che il client considera "accettabili" in ordine di preferenza, usando un sistema di classificazione detto tipo MIME (un elenco completo dei tipi MIME disponibili è consultabile sul sito ufficiale dell'organizzazione IANA che si occupa di assegnarli).

Talvolta, a causa ad esempio di una disattenzione legata alle differenti caratteristiche dei vari formati, le varie rappresentazioni di una risorsa non sono veramente equivalenti, e una rappresentazione alternativa può rivelare informazioni aggiuntive che si pensavano segrete.

L'obiettivo di questa challenge è richiedere la risorsa http://web-04.challs.olicyber.it/users utilizzando la rappresentazione alternativa application/xml anziché quella di default application/json.

Si consiglia di provare ad ottenere la risorsa normalmente, e successivamente specificando un tipo di rappresentazione diversa (application/xml) tramite lo header Accept.

# writeup

La challenge consiste nell'inviare una richiesta all'url http://web-04.challs.olicyber.it/users utilizzando l'header Accept.

Per questa challenge possiamo usare curl o requests di python.

Per ottenere la flag, l'header Accept deve contenere la rappresentazione 'application/xml'.

# exploit

## bash

script in bash:

```bash
curl -H "Accept: application/xml" http://web-04.challs.olicyber.it/users
```

### Attenzione!

Se la risposta di una richiesta è troppo lunga o confusa e non si riesce a trovare la flag, si può filtrare il testo con grep.
grep è un tool di linux che serve a filtrare un testo che gli viene dato tramite una parola chiave.

Es:
```bash
curl -H "Accept: application/xml" http://web-04.challs.olicyber.it/users | grep flag
```

## python

script in python (ch4.py):

```python
from bs4 import BeautifulSoup as bs
import requests as r

uri = "http://web-04.challs.olicyber.it/users"
headers = {'Accept': 'application/xml'}

def main():
    message = r.get(uri, headers=headers).text
    soup = bs(message, 'html.parser')
    text = soup.find("user")
    return text

if __name__ == "__main__":
    text = main()
    print(text)
```

Questa volta, oltre a requests, importiamo un modulo in più: [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) (guarda la documentazione di [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/))

Specifichiamo come sempre l'url e l'header all'inizio del file e creiamo la funzione main.

salviamo il la risposta della richiesta, che sarebbe un [XML](https://en.wikipedia.org/wiki/XML), in una variabile e la lavoriamo con BeautifulSopup.

utiliziamo la funzione find di BeautifulSopup per trovare la riga che contiene la flag, cioè la riga user.

Ritoriamo il valore ottenuto e, in fine, richiamiamo la funzione main salvanto il return un una variabile e stampiamo il valore della variabile

## ottenendo la flag:
> flag{54m3_7hing_diff3r3n7_7hing}