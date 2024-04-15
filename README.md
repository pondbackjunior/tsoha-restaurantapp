# Ravintolasovellus

Sovelluksessa näkyy tietyn alueen ravintolat, joista voi etsiä tietoa ja lukea arvioita. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

## Tämän hetken tominnot
Tällä hetkellä sovelluksessa toimii:
* Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
* Käyttäjä voi antaa arvion (tähdet ja kommentti) ravintolasta ja lukea muiden antamia arvioita.
* Ylläpitäjä voi lisätä ja poistaa ravintoloita sekä määrittää ravintolasta näytettävät tiedot.
* Käyttäjä näkee myös listan, jossa ravintolat on järjestetty parhaimmasta huonoimpaan arvioiden mukaisesti.
* Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion.

Tällä hetkellä ravintolat näkyy listana, ei kartassa.

Sovellus luo muutaman esimerkkiravintola käynnistäessä. Toimintoja voi testata tekemällä uuden tilin tai testaamalla ylläpitäjätoimintoja käyttämällä käyttäjänimeä `admin` salasanalla `admin`, jotka on kovakoodattu.

## Lopulliset toiminnot
Sovelluksen valmistuessa tavoitteena on olla kaikki nämä toiminnot: 
* Käyttäjä näkee ravintolat kartalla ja voi painaa ravintolasta, jolloin siitä näytetään lisää tietoa (kuten kuvaus ja aukioloajat).
* Käyttäjä voi etsiä kaikki ravintolat, joiden kuvauksessa on annettu sana.
* Ylläpitäjä voi luoda ryhmiä, joihin ravintoloita voi luokitella. Ravintola voi kuulua yhteen tai useampaan ryhmään.

# Käynnistysohjeet

Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

```
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>
```
Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```
Olettaen, että [local-pg](https://github.com/hy-tsoha/local-pg) on asennettu, käynnistä se komennolla
```
$ start-pg.sh
```
Erillisessä ikkunassa määritä vielä tietokannan skeema tällä komennolla. Vaihda `schema.sql` vastaamaan tarkaa sijaintia, missä tiedosto on.
```
$ psql < schema.sql
```
Erillisessä ikkunassa nyt voit käynnistää sovelluksen komennolla
```
$ flask run
```
