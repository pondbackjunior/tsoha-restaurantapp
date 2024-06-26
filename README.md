# Ravintolasovellus

Sovelluksessa näkyy tietyn alueen ravintolat, joista voi etsiä tietoa ja lukea arvioita. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

Sovelluksessa on muutama esimerkkiravintola luotuna valmiiksi. 

Toimintoja voi testata tekemällä uuden tilin tai testaamalla ylläpitäjätoimintoja käyttämällä käyttäjänimeä `admin` salasanalla `admin`, jotka on kovakoodattu.

Sovellus on testattavissa fly.io:ssa osoitteessa https://tsoha-restaurantapp.fly.dev/.
* Sivusto saattaa näyttää ensimmäisellä avauksella erroria. Päivittämällä sivun se toimii normaalisti.
  * Tämä virhe johtuu lokien mukaan sqlalchemyn ja fly.io:n serverin yhteyden välisestä häikästä, eli tämä ei ole korjattavissa sovelluksen koodissa.

# Toiminnot
* Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
* Etusivulla on kartta. Painamalla ravintoloita näkee niiden nimen ja osoitteen. Painamalla nimeä pääsee ravintolan sivulle.
  * Kartta käyttää Google Maps API:ta, ja merkit sijoittuvat kartalle JSON:in avulla.
* Etusivulla on myös listana (max 10kpl) ravintoloita. Käyttäjä voi vaihtaa listän järjestystä uusimman tai parhaiden arvostellun mukaan.
* Käyttäjä voi antaa arvion (tähdet ja kommentti) ravintolasta ja lukea muiden antamia arvioita.
* Ylläpitäjä voi lisätä ja poistaa ravintoloita sekä määrittää ravintolasta näytettävät tiedot.
* Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion.
* Käyttäjä voi etsiä kaikki ravintolat, joiden kuvauksessa tai nimessä on annettu sana.
* Ylläpitäjä voi luoda ryhmiä, joihin ravintoloita voi luokitella. Ravintola voi kuulua yhteen tai useampaan ryhmään.

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
