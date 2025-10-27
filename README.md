# ohtuvarasto
HY tietojenkäsittelytiede, Ohjelmistotuotannon laskuharjoitukset

## Viikko1 tehtävät

[X] Lisää ja committaa repositorioon kaksi tiedostoa ja kaksi hakemistoa, joiden sisällä on tiedostoja              

[X] Muuta ainakin kahden tiedoston sisältöä ja committaa muutokset repositorioon      

[X] Tee .gitignore-tiedosto, jossa määrittelet, että repositorion juurihakemistossa olevat tiedostot, joiden pääte on tmp, sekä hakemistot, joiden nimi on __pycache__ ja .pytest_cache ignoroidaan             

[X] Lisää tmp-päätteisiä tiedostoja hakemistoon ja varmista että Git jättää ne huomioimatta      

[X] Lisää myös hakemisto nimeltä __pycache__ ja hakemiston sisälle joku tiedosto. Varmista, että hakemisto sisältöineen ei mene versionhallinnan alaisuuteen           

[X] Lisää ja commitoi .gitignore-tiedosto repositorioosi          

[X] Tee muutos johonkin tiedostoon. Älä lisää tiedostoa “staging”-alueelle. 
Esimerkki README.md
Peru muutos `restore README.md`-komennolla. Komento palauttaa tiedoston työtilasta (working directory) viimeisimpään committiin (tai repository HEAD) ja unohtaa siihen tehdyt muutokset. 

[X] Tee muutos ja lisää tiedosto “staging”-alueelle, varmista että muutosta ei enää näy tiedostossa. Esimerkki README.md
Peru muutos `restore --staged README.md` ja `restore README.md` -komennoilla. 1. komento palauttaa tiedoston staging-alueelta työtilaan. 2. Komento palauttaa tiedoston työtilasta (working directory) viimeisimpään committiin (tai repository HEAD) ja unohtaa siihen tehdyt muutokset. 

[X] git add -p -harjoituksella lisätty yksittäisiä rivejä kahteen tiedostoon tiedosto1.txt ja tiedosto2.txt ja jätetty muutama rivi työtilaan (working directory). 

## Tehtävä 5 - Monta kloonia samasta repositoriosta

[X] Kloonaa ohtuvarasto toiseen hakemistoon, joka ei ole Git-repositorio.
```` 
mkdir ohtu-klooni
cd ohtu-klooni
git clone git@github.com:ktunnus/ohtuvarasto.git ohtuklooni    
cd ohtuklooni
echo "Tämä tiedosto luotiin ohtukloonin kautta." > ohtukloonin_kautta.txt 
git add ohtukloonin_kautta.txt
git commit -m "Add new file with cloned repo"
git push
```` 