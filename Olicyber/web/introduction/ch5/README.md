# Web 05 - HTTP: cookie manuale

Tra le informazioni scambiate tra client e server tramite gli header HTTP ci sono dei piccoli pezzetti di informazione detti cookie. A differenza di header non-standard, i cookie sono concepiti appositamente dallo standard HTTP per contenere dati arbitrari utili al funzionamento di siti e servizi web e sono comunemente utilizzati come parte di meccanismi di autenticazione aggiuntivi rispetto a quelli offerti dallo standard.

In maniera simile alla challenge numero 3, l'obiettivo è ottenere la risorsa http://web-05.challs.olicyber.it/flag fornendo la stringa admin in un cookie di nome password. Si consiglia di utilizzare il parametro cookies della funzione get utilizzata fino a questo momento.

# writeup

La challenge consiste nell'inviare una richista all'url http://web-05.challs.olicyber.it/flag con un [cookie](https://it.wikipedia.org/wiki/Cookie) di nome password contenente la strings 'admin'

Per questa challenge possiamo usare curl o requests di python.

### struttura cookie

```
nomeCookie=contenuto
```

# exploit

## bash

Per impostare un cookie con curl dobbiamo usare il parametro --cookie con le virgolette che al suo interno andranno a specificare il cookie.

script in bash:
```bash
curl --cookie "password=admin" http://web-05.challs.olicyber.it/flag
```

## python

script in python (ch5.py):

```python
import requests as r

uri = "http://web-05.challs.olicyber.it/flag"
cookies = dict(password='admin')

def main():
    message = r.get(uri, cookies=cookies).text
    return message

if __name__ == "__main__":
    message = main()
    print(message)
```

Importiamo il modulo requests, e specifichiamo l'url a cui fare la richiesta.

Questa volta specifichiamo anche il cookie password che dovrà contenere il valore admin (il parametro cookies richiede un dizionario come valore, per questo nella variabile cookies uso la funzione [dict](https://www.tuttofaredigitale.it/python-funzioni-integrate/python-dict)).

Ritoriamo il valore ottenuto tramite la richiesta e, in fine, richiamiamo la funzione main salvanto il return un una variabile e stampiamo il valore della variabile

## ottenendo la flag:
> flag{v3ry_7457y_c00ki35}