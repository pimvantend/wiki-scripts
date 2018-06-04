# wiki-scripts
scripts voor wikipediadingen

wiki4gpx.py maakt een .gpx-bestand met de coordinaten van de gemeentelijke monumenten die nog geen foto hebben.
de belangrijkste aanpassing per plaats/gemeente is het invullen van de plaatsnaam voorin het script.
het script vereist python-mechanize. Dit script is buiten gebruik. Deze taak loopt nu via wikifon.py met de gemeente- of plaatsnaam als parameter.

wikigeovenlo.py maakt de geocodering voor de lijst van gemeentelijke monumenten in venlo. dit script vereist geocoder.

wikicommo.py maakt een .gpx-bestand van al mijn gegeocodeerde commonsfoto's. dit script vereist python-mechanize.

upload.pl is een gewijzigd neergeladen nichalp oplaadscript, dat nog steeds niet werkt.

wikifon.py is voor het opladen van foto's van gemeentelijke monumenten. Heeft allerlei hulpprogramma's nodig.
wikifor.py is hetzelfde voor rijksmonumenten.

wikigeod.py geocodeert monumentenlijsten in de duitstalige wikipedia, is python3 en vereist geocoder

wiki2gpxd.py maakt van het resultaat een gpx-bestand om te kunnen controleren of er geen rare posities zijn

wikihaald.py wordt aangeroepen door wikigeod.py om de lijst ter bewerking neer te laden. kan ook Nederlandse gemeentelijke monumenten ophalen.
wikihaalr.py haalt een Nederlandse rijksmonumentenlijst.

wikicropd.py dient om coordinaten die ver buiten de gemeente vallen, gemakkelijk te kunnen verwijderen.
