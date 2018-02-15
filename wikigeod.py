#!/usr/bin/env python3
import geocoder,re,time,readline,sys
ophalen=True
ernst=True
handmatig=True
ortsteile=True
aanvullen=False
if len(sys.argv)>1:
  gemeente=sys.argv[1]
else:
  gemeente='Rheurdt'
  ophalen=False
#sys.exit()
#
#'Ibbenbüren'
#'Hörstel'
regio='DE-NW'
import wikihaald
if ophalen:
  wikihaald.wikihaald(gemeente,'de')
gemeentebestand=gemeente.lower()+'.txt'
bestand=open(gemeentebestand,'r')
schrijfbestand=open(gemeentebestand.replace('.txt','1.txt'),'w')
bestandstekst=bestand.read()
bestandgesplitst=bestandstekst.split('|')
bestandgesplitstinregels=bestandstekst.split('\n')
for regel in bestandgesplitstinregels:
    regel1=regel
    reguliersort=re.compile(r'(\{\{SortKey\|(?:.*\|).*?\}\})')
    regulierkern=re.compile(r'\{\{SortKey\|(?:.*\|)(.*?)\}\}')
    sortkeylijst=reguliersort.findall(regel1)
    kernlijst=regulierkern.findall(regel1)
    for ding in zip(sortkeylijst,kernlijst):
      regel1=regel1.replace(ding[0],ding[1])
    if regel.replace(' ','').startswith('{{Denkmalliste1Tabellenzeile'):
#      print(regel)
      ortsteilwaarde=''
      straat=''
      schrijfbestand.write(regel+'\n')
    elif regel.replace(' ','').startswith('|Ortsteil'):
      ortsteillijst=regel1.split('=')
      ortsteilwaarde=ortsteillijst[-1].strip()
      schrijfbestand.write(regel+'\n')
    elif regel.replace(' ','').startswith('|Adresse'):
      schrijfbestand.write(regel+'\n')
      straatlijst=regel1.split('=')
      straat=straatlijst[-1]
      straat=straat.replace('&nbsp;',' ').strip()
      straat=straat.replace('–','-')
#      if r'-' in straat:
#        locatiestreepje=straat.find(r'-')
#        straat=straat[:locatiestreepje]
#      schrijfbestand.write(straat)
#      if r'/' in straat:
#        locatieslash=straat.find(r'/')
#        straat=straat[:locatieslash]
      g=False
      opvraging=''
      nieuwens=''
      nieuweew=''
      if len(straat)>0:
        opvraging=straat+', '+gemeente+', Deutschland'
        if ortsteile and len(ortsteilwaarde)>0 and not ortsteilwaarde==gemeente:
          opvraging=straat+', '+ortsteilwaarde+', '+gemeente+', Deutschland'
        opvraging=opvraging.replace('_',' ')
        opvraging=opvraging.replace('Fröndenberg','Fröndenberg/Ruhr')
        opvraging=opvraging.replace('Mnorgensternsiedlung,','')
        opvraging=opvraging.replace('Stadtmitte, ','')
        opvraging=opvraging.replace(' und Neuheim','')
        opvraging=opvraging.replace('gegenüber ','')
        opvraging=opvraging.replace(' (Gemeinde)','')
        opvraging=opvraging.replace(' (Münsterland)','')
        opvraging=opvraging.replace(' (Kernstadt)','')
        opvraging=opvraging.replace('[','')
        opvraging=opvraging.replace(']','')
        regulara=re.compile(r'\((.*?)\)')
        haakjeslijst=regulara.findall(opvraging)
        for haakjestekst in haakjeslijst:
          opvraging=opvraging.replace(' ('+haakjestekst+')','')
        regularb=re.compile(r'\<(.*?)\>')
        punthakenlijst=regularb.findall(opvraging)
        for punthakentekst in punthakenlijst:
          opvraging=opvraging.replace('<'+punthakentekst+'>',' ')
    elif regel.replace(' ','').startswith('|NS'):
#      schrijfbestand.write(regel)
      nslijst=regel.split('=')
      nswaarde=nslijst[-1].strip()
      if len(nswaarde)==0 and len(straat)>0:
        if ernst:
          time.sleep(2)
          g=geocoder.osm(opvraging)
          if handmatig and not g:
            plaatskomma=straat.find(',')
            if plaatskomma>0:
              opvraging1=straat[:plaatskomma]+', '+gemeente+', Deutschland'
              opvraging1=opvraging1.replace('_',' ')
              regulara=re.compile(r'\((.*?)\)')
              haakjeslijst=regulara.findall(opvraging1)
              for haakjestekst in haakjeslijst:
                opvraging1=opvraging1.replace(' ('+haakjestekst+')','')
              print(opvraging1)
              g=geocoder.osm(opvraging1)
          if handmatig and not g:
            def pre_input_hook():
              readline.insert_text(opvraging)
              readline.redisplay()
            readline.set_pre_input_hook(pre_input_hook)
            print(straat)
            nieuweopvraging=input()
#            print(len(nieuweopvraging))
            if len(nieuweopvraging)>0:
              g=geocoder.osm(nieuweopvraging)
        else:
          g=False
          print(opvraging)
        if g and 'y' in g.osm:
          nieuwens=str(g.osm['y'])
          regel1=regel.replace('=','= '+nieuwens)
#          print(g.json)
          if 'town' in g.geojson['features'][0]['properties'].keys():
            plaats1=g.geojson['features'][0]['properties']['town']
            print(plaats1,straat)
          elif 'city' in g.geojson['features'][0]['properties'].keys():
            plaats1=g.geojson['features'][0]['properties']['city']
            print(plaats1,straat)
          elif 'village' in g.geojson['features'][0]['properties'].keys():
            plaats1=g.geojson['features'][0]['properties']['village']
            print(plaats1,straat)
          elif 'suburb' in g.geojson['features'][0]['properties'].keys():
            plaats1=g.geojson['features'][0]['properties']['suburb']
            print(plaats1,straat)
          else:
            print(g.geojson['features'][0]['properties'].keys())
        if g and 'x' in g.osm:
          nieuweew=str(g.osm['x'])
        schrijfbestand.write(regel1.rstrip()+'\n')
      else:
        schrijfbestand.write(regel+'\n')
    elif regel.replace(' ','').startswith('|EW'):
#      schrijfbestand.write(regel)
      ewlijst=regel.split('=')
      ewwaarde=ewlijst[-1].strip()
      if len(ewwaarde)==0:
        regel1=regel.replace('=','= '+nieuweew)
        schrijfbestand.write(regel1.rstrip()+'\n')
      else:
        schrijfbestand.write(regel+'\n')
    elif regel.replace(' ','').startswith('|Region'):
      regiolijst=regel1.split('=')
      regiowaarde=regiolijst[-1].strip()
      if len(regiowaarde)==0:
        regel1=regel.replace('=','= '+regio)
        schrijfbestand.write(regel1+'\n')
      else:
        schrijfbestand.write(regel+'\n')
    elif regel.startswith('|Nummer') and aanvullen:
      schrijfbestand.write(regel+'\n')
      schrijfbestand.write('|NS           ='+'\n')
      schrijfbestand.write('|EW           ='+'\n')
      schrijfbestand.write('|Region       ='+'\n')
    else:
      schrijfbestand.write(regel+'\n')
schrijfbestand.close()
import wiki2gpxd
wiki2gpxd.wiki2gpxd(gemeente)
#schöppingen.txt
