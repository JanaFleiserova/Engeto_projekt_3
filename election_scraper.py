"""
election_scraper.py: třetí projekt do Engeto Online Python Akademie

author: Jana Fleišerová
email: fleiserova.jana@gmail.com
discord: Jana F.
"""

from requests import get
from bs4 import BeautifulSoup as bs
import csv
import re
import sys

def zjisti_volebni_vysledky(url: str, nazev_csv: str):
    print("ověřuji argumenty...")
    if url == "https://volby.cz/pls/ps2017nss/ps36?xjazyk=CZ" and nazev_csv.endswith(".csv"):
        print("stahuji data...")
        slovnik_okrsku = sestav_slovnik_okrsku(url)
        url_adresy_okrsku = sestav_slovnik_url_adres_okrsku(slovnik_okrsku)
        strany = sestav_seznam_stran_zahranici()
        zapis_hlavicku_zahranici(strany, nazev_csv)
        zjisti_a_zapis_udaje_okrsku(url_adresy_okrsku, nazev_csv, strany)
        print("ukončuji election_scraper")
    else:
        slovnik_kraju_a_uzemnich_celku = sestav_slovnik_kraju_a_uzemnich_celku()
        over_argumenty(url, nazev_csv, slovnik_kraju_a_uzemnich_celku)
        print("stahuji data...")
        cislo_kraje = zjisti_cislo_kraje(url)
        cislo_uzemniho_celku = zjisti_cislo_uzemniho_celku(url)
        cisla_obci = sestav_seznam_cisel_obci(url)
        url_adresy_obci = sestav_slovnik_url_adres_obci(cisla_obci, cislo_uzemniho_celku, cislo_kraje)
        strany = sestav_seznam_stran_obci(cislo_uzemniho_celku, cislo_kraje)
        zapis_hlavicku_obci(strany, nazev_csv)
        zjisti_a_zapis_udaje_obci(url_adresy_obci, nazev_csv, strany)
        print("ukončuji election_scraper")

def sestav_slovnik_kraju_a_uzemnich_celku() -> dict:
    rozdelene_html = vytvor_rozdelene_html("https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ")
    slovnik_kraju_a_uzemnich_celku = {}
    a_tagy = rozdelene_html.select("a[href *= 'numnuts']")
    for a_tag in a_tagy:
        href = a_tag.get("href")
        kraj = re.search(r"kraj=(\d+)", href).group(1)
        uzemni_celek = href.split("=")[-1]
        slovnik_kraju_a_uzemnich_celku[uzemni_celek] = kraj
    return slovnik_kraju_a_uzemnich_celku

def over_argumenty(url: str, nazev_csv: str, slovnik_kraju_a_uzemnich_celku: dict):
    try:
        cislo_kraje = zjisti_cislo_kraje(url)
        cislo_uzemniho_celku = zjisti_cislo_uzemniho_celku(url)
    except:
        print("Nesprávně zadané argumenty, ukončuji program.")
        quit()
    if (
            url != "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=" + cislo_kraje + "&xnumnuts=" + cislo_uzemniho_celku or
            cislo_uzemniho_celku not in slovnik_kraju_a_uzemnich_celku or
            slovnik_kraju_a_uzemnich_celku[cislo_uzemniho_celku] != cislo_kraje or
            not nazev_csv.endswith(".csv")
        ):
        print("Nesprávně zadané argumenty, ukončuji program.")
        quit()


def zjisti_cislo_kraje(url: str) -> str:
    cislo_kraje = re.search(r"kraj=(\d+)", url).group(1)
    return cislo_kraje

def zjisti_cislo_uzemniho_celku(url: str) -> str:
    cislo_uzemniho_celku = url.split("=")[-1]
    return cislo_uzemniho_celku

def vytvor_rozdelene_html(url: str) -> bs:
    odpoved = get(url)
    rozdelene_html = bs(odpoved.text, features="html.parser")
    return rozdelene_html

def sestav_seznam_cisel_obci(url: str) -> list:
    rozdelene_html = vytvor_rozdelene_html(url)
    vsechny_a_tagy_s_td_class_cislo = rozdelene_html.select("td.cislo > a")
    cisla_obci = []
    for a_tag in vsechny_a_tagy_s_td_class_cislo:
        cisla_obci.append(a_tag.text)
    return cisla_obci

def sestav_slovnik_url_adres_obci(cisla_obci: list, cislo_uzemniho_celku: str, cislo_kraje: str) -> dict:
    url_adresy_obci = {}
    for cislo in cisla_obci:
        url_adresy_obci[cislo] = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=" + cislo_kraje + "&xobec=" + cislo + "&xvyber=" + cislo_uzemniho_celku
    return url_adresy_obci

def sestav_slovnik_okrsku(url: str) -> dict:
    rozdelene_html = vytvor_rozdelene_html(url)
    vsechny_a_tagy_s_td_class_cislo = rozdelene_html.select("td.cislo > a")
    slovnik_okrsku = {}
    for a_tag in vsechny_a_tagy_s_td_class_cislo:
        hodnota_href = a_tag.get("href")
        svetadil = re.search(r"svetadil=([^&]+)", hodnota_href).group(1)
        zeme = re.search(r"zeme=(\d+)", hodnota_href).group(1)
        slovnik_okrsku[a_tag.text] = [svetadil, zeme]
    return slovnik_okrsku

def sestav_slovnik_url_adres_okrsku(slovnik_okrsku: dict) -> dict:
    url_adresy_okrsku = {}
    for okrsek, hodnoty in slovnik_okrsku.items():
        svetadil, zeme = hodnoty
        url_adresy_okrsku[okrsek] = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=999997&xsvetadil=" + svetadil + "&xzeme=" + zeme + "&xokrsek=" + okrsek
    return url_adresy_okrsku

def sestav_seznam_stran_obci(cislo_uzemniho_celku: str, cislo_kraje: str) -> list:
    if cislo_kraje == "1":
        rozdelene_html = vytvor_rozdelene_html("https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=1")
    else:
        rozdelene_html = vytvor_rozdelene_html("https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=" + cislo_kraje + "&xnumnuts=" + cislo_uzemniho_celku)
    td_tagy_s_class_overflow = rozdelene_html.find_all("td", {"class": "overflow_name"})
    strany = []
    for td_tag in td_tagy_s_class_overflow:
        strany.append(td_tag.text)
    return strany

def sestav_seznam_stran_zahranici() -> list:
    rozdelene_html = vytvor_rozdelene_html("https://volby.cz/pls/ps2017nss/ps361?xjazyk=CZ")
    td_tagy_s_class_overflow = rozdelene_html.find_all("td", {"class": "overflow_name"})
    strany = []
    for td_tag in td_tagy_s_class_overflow:
        strany.append(td_tag.text)
    return strany

def zapis_do_csv(radek: list, soubor):
    zapisovac = csv.writer(soubor)
    zapisovac.writerow(radek)

def zapis_hlavicku_obci(strany: list, nazev_csv: str):
    hlavicka = ["kód", "obec", "voliči", "obálky", "platné"] + strany
    with open(nazev_csv, mode="w") as soubor:
        zapis_do_csv(hlavicka, soubor)

def zapis_hlavicku_zahranici(strany: list, nazev_csv: str):
    hlavicka = ["číslo a název okrsku", "země", "voliči", "obálky", "platné"] + strany
    with open(nazev_csv, mode="w") as soubor:
        zapis_do_csv(hlavicka, soubor)

def zjisti_a_zapis_udaje_okrsku(url_adresy_okrsku: dict, nazev_csv: str, strany: list):
    data = []
    for cislo, url_adresa_okrsku in url_adresy_okrsku.items():
        rozdelene_html = vytvor_rozdelene_html(url_adresa_okrsku)
        okrsek, zeme = zjisti_nazev_okrsku_a_zeme(rozdelene_html)
        volici = zjisti_pocet_volicu(rozdelene_html)
        obalky = zjisti_pocet_obalek(rozdelene_html)
        platne = zjisti_pocet_platnych(rozdelene_html)
        hlasy = sestav_seznam_hlasu(rozdelene_html, strany)
        radek = [okrsek, zeme, volici, obalky, platne] + hlasy
        data.append(radek)
    print("zapisuji data...")
    with open(nazev_csv, mode="a") as soubor:
        for radek in data:
            zapis_do_csv(radek, soubor)

def zjisti_a_zapis_udaje_obci(url_adresy_obci: dict, nazev_csv: str, strany: list):
    data = []
    for cislo, url_adresa_obce in url_adresy_obci.items():
        rozdelene_html = vytvor_rozdelene_html(url_adresa_obce)
        obec = zjisti_nazev_obce(rozdelene_html)
        volici = zjisti_pocet_volicu(rozdelene_html)
        obalky = zjisti_pocet_obalek(rozdelene_html)
        platne = zjisti_pocet_platnych(rozdelene_html)
        hlasy = sestav_seznam_hlasu(rozdelene_html, strany)
        radek = [cislo, obec, volici, obalky, platne] + hlasy
        data.append(radek)
    print("zapisuji data...")
    with open(nazev_csv, mode="a") as soubor:
        for radek in data:
            zapis_do_csv(radek, soubor)

def zjisti_nazev_obce(rozdelene_html: bs) -> str:
    div_tag_s_class_topline = rozdelene_html.find("div", {"class": "topline"})
    h3_tagy = div_tag_s_class_topline.find_all("h3")
    for h3_tag in h3_tagy:
        text_h3 = h3_tag.text
        if "Obec" in text_h3:
            obec = text_h3[7:].strip()
            break
    return obec

def zjisti_nazev_okrsku_a_zeme(rozdelene_html: bs) -> tuple:
    div_tag_s_class_topline = rozdelene_html.find("div", {"class": "topline"})
    h3_tagy = div_tag_s_class_topline.find_all("h3")
    for h3_tag in h3_tagy:
        text_h3 = h3_tag.text
        if "Okrsek" in text_h3:
            okrsek = text_h3[9:].strip()
            break
    for h3_tag in h3_tagy:
        text_h3 = h3_tag.text
        if "Země a území" in text_h3:
            zeme = text_h3[15:].strip()
            break
    return okrsek, zeme

def zjisti_pocet_volicu(rozdelene_html: bs) -> str:
    td_tag_s_sa2 = rozdelene_html.find("td", {"headers": "sa2"})
    volici = td_tag_s_sa2.text.replace("\xa0", "")
    return volici

def zjisti_pocet_obalek(rozdelene_html: bs) -> str:
    td_tag_s_sa5 = rozdelene_html.find("td", {"headers": "sa5"})
    obalky = td_tag_s_sa5.text.replace("\xa0", "")
    return obalky

def zjisti_pocet_platnych(rozdelene_html: bs) -> str:
    td_tag_s_sa6 = rozdelene_html.find("td", {"headers": "sa6"})
    platne = td_tag_s_sa6.text.replace("\xa0", "")
    return platne

def sestav_seznam_hlasu(rozdelene_html: bs, strany: list) -> list:
    tr_tagy = rozdelene_html.find_all("tr")
    hlasy = []
    for tr_tag in tr_tagy:
        td_tag_s_class_overflow = tr_tag.find("td", {"class": "overflow_name"})
        td_tag_s_t1sa2_t1sb3 = tr_tag.find("td", {"headers": "t1sa2 t1sb3"})
        td_tag_s_t2sa2_t2sb3 = tr_tag.find("td", {"headers": "t2sa2 t2sb3"})
        pocet_hlasu = None
        if td_tag_s_t1sa2_t1sb3:
            pocet_hlasu = td_tag_s_t1sa2_t1sb3.text.replace("\xa0", "")
        elif td_tag_s_t2sa2_t2sb3:
            pocet_hlasu = td_tag_s_t2sa2_t2sb3.text.replace("\xa0", "")
        if pocet_hlasu is not None and td_tag_s_class_overflow and td_tag_s_class_overflow.text in strany:
            hlasy.append(pocet_hlasu)
    return hlasy


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Chybný počet argumentů. Pro spuštění je potřeba uvést: python election_scraper.py <'url'> <název_souboru.csv>")
        sys.exit(1)

    url = sys.argv[1]
    nazev_csv = sys.argv[2]
    zjisti_volebni_vysledky(url, nazev_csv)
