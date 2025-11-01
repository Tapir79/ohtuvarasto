# HY tietojenkäsittelytiede, Ohjelmistotuotannon laskuharjoitukset Viikko 2 - laskuharjoitukset 6-12

## Tehtävä 6 - Pylint ja koodin staattinen analyysi

- [X] Ota varasto-projektissa käyttöön Pylint `poetry add pylint --group dev`              
- [X] Lisää .pylitrc               
- [X] Ota autopep8 käyttöön `poetry add autopep8 --group dev`                
- [X] Aja pylint ja autopep8          
- [X] Muuta koodia niin, että testit menevät läpi, mutta pylint-säännöt rikkoutuvat. Kaikki määritellyt säännöt + trailing-whitespace. 
````
************* Module varasto
src/varasto.py:2:0: C0301: Line too long (103/80) (line-too-long)
src/varasto.py:11:34: C0303: Trailing whitespace (trailing-whitespace)
src/varasto.py:14:21: C0303: Trailing whitespace (trailing-whitespace)
src/varasto.py:28:0: C0301: Line too long (89/80) (line-too-long)
src/varasto.py:30:0: W0311: Bad indentation. Found 5 spaces, expected 8 (bad-indentation)
src/varasto.py:2:4: R0913: Too many arguments (7/5) (too-many-arguments)
src/varasto.py:2:4: R0917: Too many positional arguments (7/5) (too-many-positional-arguments)
src/varasto.py:9:11: W0125: Using a conditional statement with a constant value (using-constant-test)
src/varasto.py:9:8: R1702: Too many nested blocks (3/2) (too-many-nested-blocks)
src/varasto.py:2:4: R0915: Too many statements (19/10) (too-many-statements)
************* Module index
src/index.py:4:0: R0915: Too many statements (42/10) (too-many-statements)
````          
- [X] Korjaa koodi niin, että se noudattaa kaikkia sääntöjä             

## Tehtävä 7

- [X] Lisää Pylint-tarkastukset Github Actionsiin 