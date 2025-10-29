HY tietojenkäsittelytiede, Ohjelmistotuotannon laskuharjoitukset 2-13

## Tehtävä 2 - GitHubiin

[X] Luo GitHubiin repositorio nimellä ohtuvarasto            


## Tehtävä 3 - Gitin alkeet [versionhallinta]

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

## Tehtävä 4 -  Tiedostojen lisääminen GitHubiin 

[X] Pushaa tehtävän 3 tiedostot Githubiin.             

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

[X] "Pullaa" kloonin kautta tehdyt muutokset alkuperäiseen ohtuvarasto-repoon. 
```` 
/ohtuvarasto$ git pull
remote: Enumerating objects: 8, done.
remote: Counting objects: 100% (8/8), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 6 (delta 3), reused 6 (delta 3), pack-reused 0 (from 0)
Unpacking objects: 100% (6/6), 835 bytes | 23.00 KiB/s, done.
From github.com:Tapir79/ohtuvarasto
   fcf32b1..b07ccad  main       -> origin/main
Updating fcf32b1..b07ccad
Fast-forward
 README.md              | 16 +++++++++++++++-
 ohtukloonin_kautta.txt |  1 +
 2 files changed, 16 insertions(+), 1 deletion(-)
 create mode 100644 ohtukloonin_kautta.txt
 ```` 

[X] Lisää alkuperäiseen klooniin joitain tiedostoja ja pushaa ne GitHubiin. Pullaa lisätyt uudet tiedostot tiedosto3.txt ja /hakemisto1/hakemisto1_tiedosto2_harj5.txt ohtuklooniin.      
 ```` 
/ohtuklooni$ git pull
remote: Enumerating objects: 12, done.
remote: Counting objects: 100% (12/12), done.
remote: Compressing objects: 100% (6/6), done.
remote: Total 9 (delta 4), reused 8 (delta 3), pack-reused 0 (from 0)
Unpacking objects: 100% (9/9), 1.31 KiB | 43.00 KiB/s, done.
From github.com:Tapir79/ohtuvarasto
   b07ccad..d92c5ba  main       -> origin/main
Updating b07ccad..d92c5ba
Fast-forward
 README.md                                 | 20 +++++++++++++++++++-
 hakemisto1/hakemisto1_tiedosto2_harj5.txt |  3 +++
 tiedosto3.txt                             |  3 +++
 3 files changed, 25 insertions(+), 1 deletion(-)
 create mode 100644 hakemisto1/hakemisto1_tiedosto2_harj5.txt
 create mode 100644 tiedosto3.txt
  ````    

## Tehtävä 6 - Repositorion siivous

[X] Poista tehtävän 5 harjoitusklooni `rm -rf ohtu-klooni`                   

[X] Poista repositorioistasi kaikki hakemistot sekä muut tiedostot paitsi .git, .gitignore ja README.md
```` 
/ohtuvarasto$ ls -a
.  ..  .git  .gitignore  README.md
````

[X] Hae ja pura varasto.zip sisältö projektin juureen.  
````
 ls -la
total 28
drwxr-xr-x 4 saara saara 4096 Oct 27 18:09 .
drwxr-xr-x 5 saara saara 4096 Oct 27 18:08 ..
drwxr-xr-x 8 saara saara 4096 Oct 27 18:05 .git
-rw-r--r-- 1 saara saara  171 Oct 27 16:25 .gitignore
-rw-r--r-- 1 saara saara 4087 Oct 27 18:05 README.md
-rw-r--r-- 1 saara saara  400 Oct 27 18:09 pyproject.toml
drwxr-xr-x 3 saara saara 4096 Oct 27 18:09 src
````

## Tehtävä 7 - Poetry  

[X] Päivitä Python versioon 3.13       
[X] Päivitä Poetry versioon 2.2.1          
[X] Aseta Poetry käyttämään versiota 3.13 `poetry env use 3.13.0`  

## Tehtävä 8 - Unittest

[X] Asenna coverage ja lisää .coveragerc             
[X] Luo htmlcov             
[X] Lisää htmlcov ja .coverage .gitignoreen           
[X] Luo testit, joilla haaraumakattavuus saavuttaa 100%

Bonus: 

[X] Alias .bashrc-tiedostoon `alias poetry-activate='eval $(poetry env activate)'`

## Tehtävä 9,10,11 - GitHub Actions, osa 1,2,3

[X] Luo .github/workflows/main.yml            
[X] Hajota testit, jotta GHA menee punaiselle               
[X] Korjaa rikkinäinen testi ja varmista, että CI toimii oikein.                
[X] Lisää CI badge             
[X] Muuta testitiedostoa > pull antaa virheen > pull.rebase > push           
[X] Tee badgestä linkki Actions-välilehdelle            
 
 ## Tehtävä 12 - Codecov

 [X] Lisää repositorio Codecoviin alaisuuteen             
 [X] Lisää Codecov token Githubiin               
 [X] Lisää Codecov Github Action -konfiguraatioon            
 [X] Lisää badge Codecoviin               

 ## Tehtävä 13 - Parempi testikattavuus
 [X] Lisää juurihakemiston .coveragerc-tiedostoon, omit-konfiguraatio ja määrittele huomioimatta jätettävät tiedostot                   