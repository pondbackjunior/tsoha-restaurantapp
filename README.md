# Ravintolasovellus

Sovelluksessa näkyy tietyn alueen ravintolat, joista voi etsiä tietoa ja lukea arvioita. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

Sovellus luo muutaman esimerkkiravintolan käynnistäessä. Toimintoja voi testata tekemällä uuden tilin tai testaamalla ylläpitäjätoimintoja käyttämällä käyttäjänimeä `admin` salasanalla `admin`, jotka on kovakoodattu.

Sovellus on testattavissa fly.io:ssa osoitteessa https://tsoha-restaurantapp.fly.dev/. (Jos sivusto näyttää ekalla avauksella erroria, päivitä sivu ja pitäisi toimia).

## Välipalautus 2 (7.4.2024)
Sovellukseen on lisätty seuraavat toiminnot:
* Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
* Käyttäjä voi antaa arvion (tähdet ja kommentti) ravintolasta ja lukea muiden antamia arvioita.
* Ylläpitäjä voi lisätä ja poistaa ravintoloita sekä määrittää ravintolasta näytettävät tiedot.
* Käyttäjä näkee myös listan, jossa ravintolat on järjestetty parhaimmasta huonoimpaan arvioiden mukaisesti.
* Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion.

Tällä hetkellä ravintolat näkyy listana, ei kartassa.

## Välipalautus 3 (21.4.2024)
Sovellukseen on lisätty seuraavat toiminnot:
* Käyttäjä voi etsiä kaikki ravintolat, joiden kuvauksessa tai nimessä on annettu sana.
* Ylläpitäjä voi luoda ryhmiä, joihin ravintoloita voi luokitella. Ravintola voi kuulua yhteen tai useampaan ryhmään.
* Ravintoloiden tietojen määrää on lisätty, ja kartta on aloitettu.

Tällä hetkellä kartta on vielä hieman kesken. Se ei siis näytä ravintoloita siinä vielä. Kaikki muut sovelluksen ominaisuudet ovat kuitenkin käytännössä valmiita, eli sovellus tarvii vielä hieman viimestelyä ja ulkoasun parantamista.
<!--
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
-->
