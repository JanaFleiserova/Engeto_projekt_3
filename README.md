# Engeto_projekt_3

Election_scraper jako třetí projekt pro Engeto Python Adademii.


## Popis projektu

Election_scraper stáhne výsledky parlamentních voleb z r.2017 libovolného územního celku z tohoto [odkazu](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ). Stažené výsledky zapíše do souboru csv.


## Instalace knihoven

Program používá některé knihovny třetích stran, které je potřeba ke spuštění programu nainstalovat. Jejich seznam je uložen v souboru requirements.txt. Pro jejich instalaci je doporučené použít vlastní virtuální prostředí.

Pomocí manažeru pip nejdříve v příkazovém řádku ověřte verzi manažeru pip:

pip3 --version

Poté nainstalujte vyžadované knihovny:

pip3 install -r requirements.txt


## Spuštění projektu

Pro spuštění program vyžaduje dva argumenty: url adresu územního celku a název csv souboru, do kterého má stažené výsledky uložit. Url adresa musí být uzavřená v uvozovkách a název souboru musí být zakončen příponou .csv.
Příkaz v příkazovém řádku by měl vypadat takto:

python election_scraper.py "url" nazev_souboru.csv

## Ukázka projektu

### Výsledky hlasování pro územní celek Praha-západ:

1.argument: "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2110"

2.argument: vysledky_praha_zapad.csv

### Spuštění programu:

python election_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2110" vysledky_praha_zapad.csv

### Průběh stahování: 

ověřuji argumenty...

stahuji data...

zapisuji data...

ukončuji election_scraper

### Částečný výstup:

kód,obec,voliči,obálky,platné,Občanská demokratická strana,Řád národa - Vlastenecká unie...
539104,Bojanovice,372,268,267,36,0,0,24,0,19,15,1,3,6,0,0,36,0,0,13,78,1,0,7,0,1,0,1,24,2
571199,Bratřínov,149,121,121,29,0,0,8,0,5,11,1,1,0,0,0,19,0,0,6,32,0,0,2,0,1,0,1,5,0
...