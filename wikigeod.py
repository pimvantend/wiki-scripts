#!/usr/bin/env python3
import geocoder,re,time,readline,sys
if len(sys.argv)>1:
  gemeente=sys.argv[1]
else:
  gemeente='Kranenburg_(Niederrhein)'
#sys.exit()
ernst=True
handmatig=True
#
#'Ibbenbüren'
#'Hörstel'
regio='DE-NW'
import wikihaald
if ernst:
  wikihaald.wikihaald(gemeente)
gemeentebestand=gemeente.lower()+'.txt'
bestand=open(gemeentebestand,'r')
schrijfbestand=open(gemeentebestand.replace('.txt','1.txt'),'w')
ortsteilwaarde=''
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
    if regel.replace(' ','').startswith('|Ortsteil'):
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
      if r'/' in straat:
        locatieslash=straat.find(r'/')
        straat=straat[:locatieslash]
#      schrijfbestand.write(straat)
      g=False
      opvraging=''
      nieuwens=''
      nieuweew=''
      if len(straat)>0:
        opvraging=straat+', '+gemeente+', Germany'
        if len(ortsteilwaarde)>0 and not ortsteilwaarde==gemeente:
          opvraging=straat+', '+ortsteilwaarde+'/'+gemeente+', Germany'
        opvraging=opvraging.replace('Morgensternsiedlung,','')
        opvraging=opvraging.replace('[','')
        opvraging=opvraging.replace(']','')
#        opvraging=opvraging.replace('_(Münsterland)','')
        opvraging=opvraging.replace('_',' ')
        regulara=re.compile(r'\((.*?)\)')
        haakjeslijst=regulara.findall(opvraging)
        for haakjestekst in haakjeslijst:
          opvraging=opvraging.replace(' ('+haakjestekst+')','')
    elif regel.replace(' ','').startswith('|NS'):
#      schrijfbestand.write(regel)
      nslijst=regel.split('=')
      nswaarde=nslijst[-1].strip()
      if len(nswaarde)==0 and len(straat)>0:
        if ernst:
          time.sleep(2)
          g=geocoder.osm(opvraging)
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
      regiolijst=regel1.split('=')
      regiowaarde=regiolijst[-1].strip()
      if len(regiowaarde)==0:
        regel1=regel.replace('=','= '+regio)
        schrijfbestand.write(regel1+'\n')
      else:
        schrijfbestand.write(regel+'\n')
    else:
      schrijfbestand.write(regel+'\n')
schrijfbestand.close()
import wiki2gpxd
wiki2gpxd.wiki2gpxd(gemeente)
#schöppingen.txt
