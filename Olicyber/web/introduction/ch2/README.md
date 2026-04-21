# Web 02 - HTTP: richiesta GET con query string

La richiesta di alcune risorse può essere parametrizzata, per ottenere particolari versioni della risorsa in questione. Ad esempio, un blog potrebbe utilizzare un'unica risorsa per rappresentare tutti i post pubblicati (che sono strutturalmente tutti uguali, differendo solo per il contenuto) identificando il contenuto specifico desiderato tramite un parametro numerico id.

L'obiettivo di questa challenge è ottenere la risorsa http://web-02.challs.olicyber.it/server-records specificando il parametro id con il valore flag. Si consiglia di utilizzare la parola chiave params della funzione get illustrata nella challange precedente.

# writeup

La challenge consiste nel fare una richiesta get all'url http://web-02.challs.olicyber.it/server-records specificando il parametro id con il valore flag.

Per questa challenge possiamo usare curl o requests di python.

## exploit

## bash

Per usare un parametro in una richiesta curl, basterà mettere il '?' seguito dal nome del parametro, in questo caso id, e poi assegnarli un valore tramite l'uguale.

Es:
> http://web-02.challs.olicyber.it/server-records?id=3

ma in questo caso come parametro dobbiamo usare 'flag'.


Script in bash per fare richiesta http con curl:

```bash
curl http://web-02.challs.olicyber.it/server-records?id=flag
```

## python

Script in python (ch2.py):

```python
import requests as r

url = "http://web-02.challs.olicyber.it/server-records"

def main():
    message = r.get(url, params={"id": "flag"}).text
    return message

if __name__ == "__main__":
    message = main()
    print(message)
```

Come prima cosa importiamo il modulo requests, e specifichiamo l'url a cui fare la richiesta.

Successivamente dentro la funzione main utilizziamo la funzione GET di requests con i parametri id=flag

solo che a differenza di curl, python specifica i parametri in [json](https://www.json.org/json-it.html).

Ritoriamo il valore ottenuto tramite la richiesta e, in fine, richiamiamo la funzione main salvanto il return un una variabile e stampiamo il valore della variabile

## ottenendo la flag:
> flag{wh47_i5_y0ur_qu3ry}