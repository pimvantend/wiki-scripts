#!/usr/bin/env python3
import geocoder,re,time
gemeente='Legden'
regio='DE-NW'
gemeentebestand=gemeente.lower()+'.txt'
bestand=open(gemeentebestand,'r')
schrijfbestand=open(gemeentebestand.replace('.txt','1.txt'),'w')
ortsteilwaarde=''
bestandstekst=bestand.read()
bestandgesplitst=bestandstekst.split('|')
bestandgesplitstinregels=bestandstekst.split('\n')
for regel in bestandgesplitstinregels:
    if regel.replace(' ','').startswith('|Ortsteil'):
      ortsteillijst=regel.split('=')
      ortsteilwaarde=ortsteillijst[-1].strip()
      schrijfbestand.write(regel+'\n')
    elif regel.replace(' ','').startswith('|Adresse'):
      schrijfbestand.write(regel+'\n')
      regulara=re.compile(r'\((.*?)\)')
      haakjeslijst=regulara.findall(regel)
#      if '(' in regel:
      regel1=regel
      for haakjestekst in haakjeslijst:
        regel1=regel.replace(' ('+haakjestekst+')','')
#        schrijfbestand.write(regel1)
#        exit()
#      ruwadres=regel
      positiesortkey=regel1.find('{{SortKey|')
      if positiesortkey>-1:
        positiestreep=regel1.find('|',positiesortkey+10)
        weghalen=regel1[positiesortkey:positiestreep+1]
        regel1=regel1.replace(weghalen,'')
#      regel1=regel.replace('{{SortKey|','')
      regel1=regel1.replace('}}','')
#      if '|' in regel1:
#        regel1lijst=regel1.split('|')
#        regel1='='+regel1lijst[-1]
      straatlijst=regel1.split('=')
      straat=straatlijst[-1]
      straat=straat.replace('&nbsp;',' ').strip()
      straat=straat.replace('–','-')
      if r'-' in straat:
        locatiestreepje=straat.find(r'-')
        straat=straat[:locatiestreepje]
      if r'/' in straat:
        locatieslash=straat.find(r'/')
        straat=straat[:locatieslash]
#      schrijfbestand.write(straat)
      opvraging=''
      nieuwens=''
      nieuweew=''
      if len(straat)>0:
        if len(ortsteilwaarde)>0:
          opvraging=straat+' '+ortsteilwaarde+' Germany'
        else:
          opvraging=straat+' '+gemeente+' Germany'
        opvraging=opvraging.replace('Morgensternsiedlung,','')
        opvraging=opvraging.replace('Nienborg','Nienborg/Heek')
#        schrijfbestand.write(opvraging)
    elif regel.replace(' ','').startswith('|NS'):
#      schrijfbestand.write(regel)
      nslijst=regel.split('=')
      nswaarde=nslijst[-1].strip()
      if len(nswaarde)==0:
        time.sleep(2)
        g=geocoder.osm(opvraging)
        if g and 'y' in g.osm:
          nieuwens=str(g.osm['y'])
        if g and 'x' in g.osm:
          nieuweew=str(g.osm['x'])
        regel1=regel.replace('=','= '+nieuwens)
        schrijfbestand.write(regel1+'\n')
      else:
        schrijfbestand.write(regel+'\n')
    elif regel.replace(' ','').startswith('|EW'):
#      schrijfbestand.write(regel)
      ewlijst=regel.split('=')
      ewwaarde=ewlijst[-1].strip()
      if len(ewwaarde)==0:
        regel1=regel.replace('=','= '+nieuweew)
        schrijfbestand.write(regel1+'\n')
      else:
        schrijfbestand.write(regel+'\n')
    elif regel.replace(' ','').startswith('|Region'):
      regiolijst=regel.split('=')
      regiowaarde=regiolijst[-1].strip()
      if len(regiowaarde)==0:
        regel1=regel.replace('=','= '+regio)
        schrijfbestand.write(regel1+'\n')
      else:
        schrijfbestand.write(regel+'\n')
    else:
      schrijfbestand.write(regel+'\n')
