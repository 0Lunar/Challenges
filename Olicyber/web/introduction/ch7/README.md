# Web 07 - HTTP: il metodo HEAD

A volte può essere interessante, per un client, conoscere i metadati di una risorsa senza doverne necessariamente ricevere l'intera rappresentazione (si pensi ad esempio al caso di un file di grandi dimensioni). Proprio per queste casistiche il protocollo HTTP fornisce il verbo HEAD, pensato per ottenere in risposta gli header di una richiesta GET equivalente, ma senza eseguire il trasferimento della risorsa.

Gli header riportati dovrebbero essere identici a quelli di un'analoga richiesta GET ma, come nel caso dello header Accept, un server difettoso o mal configurato può trapelare accidentalmente informazioni aggiuntive che non sarebbero incluse nella risposta a una normale richiesta GET.

L'obiettivo di questa challenge è eseguire una richiesta HEAD alla risorsa http://web-07.challs.olicyber.it/ ed osservare gli header restituiti. Si consiglia di utilizzare la funzione head della libreria requests, di utilizzo analogo a quello della funzione get.

# writeup

La challenge consiste nel fare una richiesta all'url http://web-07.challs.olicyber.it/ ed osservare gli header restituiti dal sito web.

Per questa challenge possiamo utilizzare curl o requests di python.

Possiamo visualizzare gli header con curl utilizzando il parametro -I.

P.S. nello script in bash filto il testo per visualizzare meglio la flag, ma non è per forza necessario filtrarlo.

# exploit

script in bash:
```bash
curl -I http://web-07.challs.olicyber.it/ | grep X-Flag | cut -d ":" -f2 | cut -d " " -f2
```

script in python (ch7.py):
```bash
python3 ch7.py
```

ottenendo la flag:
> flag{r0gu3_m374d474}
