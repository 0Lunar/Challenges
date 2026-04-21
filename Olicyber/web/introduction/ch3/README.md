# Web 03 - HTTP: richiesta GET con header manuale

Quando viene inviata una richiesta HTTP, oltre al verbo, al percorso della risorsa desiderata e ad eventuali parametri associati, vengono comunicate al server alcune informazioni aggiuntive in campi detti header (dal fatto che vengono inviati nella prima parte del messaggio HTTP). Allo stesso modo, anche il server allegherà alla risposta degli header in aggiunta al contenuto richiesto. Questi header differiscono dai parametri della richiesta GET perché non vengono utilizzati per specificare la risorsa richiesta, ma contengono informazioni riguardanti il client (detto user-agent), il server e il canale di comunicazione, metadati associati alle risorse ed eventuali informazioni di debug.

Questi header vengono generalmente inseriti automaticamente dalle librerie client e dal server e appartengono ad un insieme standard definito come parte del protocollo stesso; ciononostante è possibile specificarne di aggiuntivi per soddisfare le esigenze di particolari applicazioni. Questi header non-standard hanno normalmente nomi che iniziano per X- e quando vengono inviati a un sistema non in grado di riconoscerli vengono solitamente ignorati.

In questa challenge, uno header non-standard è stato usato per fornire un meccanismo di autenticazione artigianale. L'obiettivo è ottenere il testo della risorsa all'indirizzo http://web-03.challs.olicyber.it/flag, ma il server risponderà solo a richieste che conterranno lo header X-Password contenente la password corretta, admin.

Si consiglia di utilizzare la parola chiave headers della funzione get utilizzata nelle challenge precedenti.

N.B.: il protocollo HTTP fornisce già diversi meccanismi di autenticazione tramite lo header standard Authorization, che sono generalmente più complessi dell'esempio di autenticazione "artigianale" presentato in questa challenge. Anziché manipolare direttamente lo header Authorization, quando necessario librerie come requests forniscono metodi specifici per interfacciarsi con esso.

# writeup

La challenge consiste nell'inviare una richiesta all'url http://web-03.challs.olicyber.it/flag utilizzando un header specifico: X-Password, che dovrà contenere la password 'admin'.

Gli headers sono come dei metadati che vengono inseriti in una richieta HTTP e vengono normalmente posizionati all'inizio del pacchetto.

Per questa challenge possiamo usare curl o requests di python.

### struttura header

```
X-Parametro: contenuto
```

# exploit

## bash

Per impostare un header con curl dobbiamo usare il parametro -H (Header), con le virgolette dove al suo interno andremo a specificare l'header.

script in bash:
```bash
curl -H "X-Password: admin" http://web-03.challs.olicyber.it/flag
```

## python

script in python (ch3.py):

```python
import requests as r
from colorama import Fore

url = "http://web-03.challs.olicyber.it/flag"
headers = {'X-Password': 'admin'}

def main():
    message = r.get(url, headers=headers).text
    return message

if __name__ == "__main__":
    message = main()
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + message + Fore.RESET)
```

Come prima cosa importiamo il modulo requests, e specifichiamo l'url a cui fare la richiesta.

Specifichiamo anche l'header in json.

Creiamo una funzione main che andrà a fare una richiesta GET all'url con l'header specificato.

Nel modulo requests, possiamo specificare un header o più col parametro headers.

Ritoriamo il valore ottenuto tramite la richiesta e, in fine, richiamiamo la funzione main salvanto il return un una variabile e stampiamo il valore della variabile

## ottenendo la flag:
> flag{7ru57_m3_i_m_7h3_4dmin}