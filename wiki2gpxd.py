#!/usr/bin/env python3
import re
def wiki2gpxd(gemeente):
#gemeente='Raesfeld'
  gemeentebestand=gemeente.lower()+'1.txt'
  gpxbestandnaam=gemeentebestand.replace('.txt','.gpx')
  bestand=open(gemeentebestand,'r')
  gpxbestand=open(gpxbestandnaam,'w')
  gpxbestand.write( '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
  gpxbestand.write( '<gpx version="1.1" creator="Locus Android"\n')
  gpxbestand.write( ' xmlns="http://www.topografix.com/GPX/1/1"\n')
  gpxbestand.write( ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
  gpxbestand.write( ' xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"\n')
  gpxbestand.write( ' xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3"\n')
  gpxbestand.write( ' xmlns:gpxtrkx="http://www.garmin.com/xmlschemas/TrackStatsExtension/v1"\n')
  gpxbestand.write( ' xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v2"\n')
  gpxbestand.write( ' xmlns:locus="http://www.locusmap.eu">\n')
  opvraging=''
  bestandstekst=bestand.read()
  bestandgesplitst=bestandstekst.split('|')
  bestandgesplitstinregels=bestandstekst.split('\n')
  for regel in bestandgesplitstinregels:
    if regel.replace(' ','').startswith('|Adresse'):
#      print(regel)
#      ruwadres=regel
      regel1=regel
      reguliersort=re.compile(r'(\{\{SortKey\|(?:.*\|).*?\}\})')
      regulierkern=re.compile(r'\{\{SortKey\|(?:.*\|)(.*?)\}\}')
      sortkeylijst=reguliersort.findall(regel)
      kernlijst=regulierkern.findall(regel)
      for ding in zip(sortkeylijst,kernlijst):
        regel1=regel.replace(ding[0],ding[1])
#        print(regel1)
#      positiesortkey=regel.find('{{SortKey|')
#      if positiesortkey>-1:
#        positiestreep=regel.find('|',positiesortkey+10)
#        weghalen=regel[positiesortkey:positiestreep+1]
#        regel1=regel.replace(weghalen,'')
#      regel1=regel.replace('{{SortKey|','')
#      regel1=regel1.replace('}}','')
#      if '|' in regel1:
#        regel1lijst=regel1.split('|')
#        regel1='='+regel1lijst[-1]
      straatlijst=regel1.split('=')
      straat=straatlijst[-1]
      straat=straat.replace('&nbsp;',' ').strip()
      straat=straat.replace('–','-')
    elif regel.replace(' ','').startswith('|EW'):
#      print(regel)
      ewlijst=regel.split('=')
      ewwaarde=ewlijst[-1].strip()
    elif regel.replace(' ','').startswith('|NS'):
#      print(regel)
      nslijst=regel.split('=')
      nswaarde=nslijst[-1].strip()
#    if regel.replace(' ','').startswith('|Ortsteil'):
#        print(regel)
    elif regel.replace(' ','').startswith('|Beschreibung'):
#      print(regel)
      beschreibungslijst=regel.split('=')
      beschrijving=beschreibungslijst[-1].strip()
      beschrijving=beschrijving.replace('<br />',' ')
      if len(nswaarde)>0 and len(ewwaarde)>0:
        gpxbestand.write('<wpt lat="'+nswaarde+'" lon="'+ewwaarde+'">\n')
        gpxnaam='  <name>'+straat+', '+beschrijving
#    gpxnaam+=' '+dictio['bouwjaar']
        gpxnaam=gpxnaam.replace(';','')
        gpxbestand.write(gpxnaam)
        gpxbestand.write('</name>\n')
        gpxbestand.write('</wpt>\n')
  gpxbestand.write('</gpx>\n')
