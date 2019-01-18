# Handleiding Pannenkoekenprinter 2.0
**2018-09-27**

## Benodigdheden
  - Printer
  - Kookplaatstand
  - Kookplaat
  - Router
  - Laptop
  - 2 LAN-kabels
  - Stekkerdoos/-dozen voor minimaal 6 stekkers
  - Stroomkabels voor de printer

  - Koopmans Pannenkoekenbeslag Compleet (hoeft alleen water bij), 1 pak per 2-3
    uur aaneensluitend demo
  - 3 beslagkommen
  - Zeer fijne zeef
  - Garde
  - Spateltje
  - Servetten om pannenkoeken op te dienen
  - Poedersuiker/stroop
  - Keukenpapier 
  - Prullenbak
  - Olie/boter
  - Weegschaal
  - Maatbeker

  - Schoonmaakspullen

## Printer klaarzetten
  - Zet de printer ergens met voldoende ruimte
  - Zet de kookplaatstand voor de printer met de kookplaat erin. Het goed
    positioneren van de kookplaat kan een beetje lastig zijn, maar het past
    precies en het is belangrijk dat hij goed staat
  - Zet een lokaal netwerk op met de router
  - Zorg dat alle componenenten stroom hebben
    - De pi
    - De pi motor hat (zit op de pi)
    - Het relais (via de powerbrick die eraan hangt)
    - De kookplaat
    - De router
    - De besturingslaptop
  - Maak een SSH-verbinding naar de raspberry pi
    - user: pi
    - password: raspberry
  - Zorg dat je de hygienehandleiding (zie hieronder) doorleest voordat je gaat
    printen, zeker op open dagen
  - Maak beslag, zoals hieronder aangegeven, en hang/tape de slang in de
    beslagkom. 

## Het beslag
  - Gebruik Koopmans Pannenkoekenmix Compleet. Andere mixen zal misschien melk
    bij moeten, maar dat kan i.v.m. andere viscositeit problemen opleveren. 
  - Mix 400 gram beslag met 750 mililiter water. Zorg dat je de weegschaal en de
    maatbeker gebruikt om dit enigszins precies te doen.  Roer het beslag goed
    met een garde totdat bijna alle klontjes verdwenen zijn. Doe dit niet in de
    beslagkom waaruit je gaat printen, maar in de andere. 
  - Giet het beslag nu door de zeef in de beslagkom waar je uit gaat printen. 

## Printen
  - Het programma `Pannenkoeken/runme.py` runt de printer met een enkele
    afbeelding. De afbeelding die op open dagen meestal gebruikt wordt is
    `images/rtilted.jpg`. Dit print een schuine versie van het Radboudlogo. 

## Hygienehandleiding
  - Zorg dat je de slang voordat je gaat printen van binnen en van buiten
    schoonmaakt. De slang van binnen schoonmaken doe je door er warm water door
    te pompen. Het programma `pannenkoeken/pannenkoeken/pannenkoeken/main.py`
    spoelt vijf minuten water door de slang. Het zou kunnen dat je nog het goede
    programma moet selecteren. Deze heet 'flow' en kan net onder alle
    programmainstructies gezet worden, in de variable `used_set`. 
  - Spoel na afloop de slang eerst 10 minuten met warm water MET dreft,
    vervolgen 10 minuten ZONDER dreft. Zorg ook dat de buitenkant van de slang
    weer schoon is. 
