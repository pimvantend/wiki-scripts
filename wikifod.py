#!/usr/bin/env python3
import glob
apparaatidentificatie=glob.glob(r'/storage/')
if len(apparaatidentificatie) == 0:
  txtdirectory=r'./'
  gpxdirectory=r'../gpx2/'
  plaatjesdirectory=r'/home/zeeman/Pictures/'
  coredirectory=r'../../core/'
else:
  txtdirectory=r'/storage/sdcard/'
  gpxdirectory=r'/storage/sdcard/'
  plaatjesdirectory=r'/storage/sdcard/'
  coredirectory=r'/storage/sdcard/'
#import piexif
#wikihaald
import re
import subprocess
import sys
appendofwrite='w'
telezen='m_stadtbezirk_bochum-wattenscheid.txt'
dirvoorvoegsel='/home/zeeman/Pictures/170623-woestehoeve/'
datumwens='2018-01-25 13:30'
catwens="Bochum_(Stadtbezirk_Wattenscheid)"
#'Burgemeesterswijk en Hoogkamp, Arnhem'
#'Geitenkamp, Arnhem'
jaar='24'
gewensteplaats="Bochum-Wattenscheid"
provincie='NW'
gpxvoorvoegsel='../gpx2/'
if len(sys.argv)>1:
    optehalen=sys.argv[-1]
    print(optehalen)
#    import wikihaald
#    wikihaald.wikihaald(optehalen)
    subprocess.call(['python3','./wikihaalde.py',optehalen])
    telezen=optehalen.lower()+'.txt'
#    print telezen
else:
    import piexif
sedbestandnaam=txtdirectory+telezen.replace('.txt','.bash')
sedbestand=open(sedbestandnaam,'w')
subprocess.call(['chmod','a+xwr',sedbestandnaam])
gpxbestandnaam=telezen.replace('.txt','.gpx')
gpxbestand=open(gpxdirectory+gpxbestandnaam,'w')
gpxbestand.write( '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
gpxbestand.write( '<gpx version="1.1" creator="Locus Android"\n')
gpxbestand.write( ' xmlns="http://www.topografix.com/GPX/1/1"\n')
gpxbestand.write( ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
gpxbestand.write( ' xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"\n')
gpxbestand.write( ' xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3"\n')
gpxbestand.write( ' xmlns:gpxtrkx="http://www.garmin.com/xmlschemas/TrackStatsExtension/v1"\n')
gpxbestand.write( ' xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v2"\n')
gpxbestand.write( ' xmlns:locus="http://www.locusmap.eu">\n')
wikibestand=open(txtdirectory+telezen,'r')
wikibestand=wikibestand.read()
wikibestand=wikibestand.replace('\n',' ')
if not(len(sys.argv)>1):
  opdrachtbestandsnaam=coredirectory+'oplaad-'+telezen.replace('.txt','.bash')
  opdrachtbestand=open(opdrachtbestandsnaam,appendofwrite)
  subprocess.call(['chmod','a+xwr',opdrachtbestandsnaam])
#print wikibestand
regulierltgt=re.compile('(<.*?>)')
lijstltgt=regulierltgt.findall(wikibestand)
for dingltgt in lijstltgt:
  wikibestand=wikibestand.replace(dingltgt,'')
#wikibestand=wikibestand.replace(' =','=')
wikibestand=wikibestand.replace('&nbsp;',' ')
wikibestand=wikibestand.replace('&','und')
wikibestand=wikibestand.replace('commonscat=','commonscat =')
wikibestand=wikibestand.replace('image=','image =')

reguliera=re.compile('({{[^D].*?}})')
lijst1=reguliera.findall(wikibestand)
#print lijst1
for ding in lijst1:
    wikibestand=wikibestand.replace(ding,'')

reguliera=re.compile('({{Dtsx.*?}})')
lijst1=reguliera.findall(wikibestand)
#print lijst1
for ding in lijst1:
    wikibestand=wikibestand.replace(ding,'')

reguliera1=re.compile(r'({{DL\ Bochum\|.*?}})')
lijst1=reguliera1.findall(wikibestand)
print(lijst1)
reguliera2=re.compile(r'{{DL\ Bochum\|(.*?)}}')
lijst2=reguliera2.findall(wikibestand)
print(lijst2)
for (ding1,ding2) in zip(lijst1,lijst2):
    wikibestand=wikibestand.replace(ding1,'A '+ding2)

reguliere=re.compile('{{Denkmalliste1 Tabellenzeile(.*?)}')
lijst=reguliere.findall(wikibestand)
#print lijst
dictmeervoudige={}
dictiolijst=[]
regulierd=re.compile(r'([_a-z]*?) =')
reguliere=re.compile(r'(Bild)=')
regulierf=re.compile(r'=(.*?)\|')
regulierg=re.compile(r'Bild=(.*?)\.')
regulierh=re.compile(r'([0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]\.JPG)')
for ding in lijst: #lijst bevat de tabelrijen
    ding+='|'
    dictio={}
    dictio['postcode']=''
    dictio['architect']=''
    dictio['oorspr_fun']=''
    dictio['kadaster']=''
    dictio['Bild']=''
    dictio['Abmessungen']=''
    dictio['Commonscat']=''
    dictio['Bezeichnung']=''
    dictio['Ortsteil']=''
    dictio['Adresse']=''
    dictio['NS']=''
    dictio['EW']=''
    dictio['Region']=''
    dictio['Beschriftung']=''
    dictio['Beschreibung']=''
    dictio['Bauzeit']=''
    dictio['Eintragung']=''
    dictio['Nummer']=''
#    print ding
    dinggesplitstlijst=ding.split('|')
#    print dinggesplitstlijst
    for iets in dinggesplitstlijst:
#        print iets
      ietslijst=iets.split('=')
#        print ietslijst
      if len(ietslijst)==2:
        sleutel=ietslijst[0].strip()
        waarde=ietslijst[1].strip()
        dictio[sleutel]=waarde
    plaatjesnaam=dictio['Bild']
#    print dictio
    if plaatjesnaam=='' and 'NS' in dictio.keys() and 'EW' in dictio.keys():
      if len(dictio['NS'])>0 and len(dictio['EW'])>0:
        gpxbestand.write('<wpt lat="'+dictio['NS']+'" lon="'+dictio['EW']+'">\n')
        gpxnaam='  <name>'+dictio['Adresse']+' '+dictio['Bezeichnung']
        gpxnaam+=' '+dictio['Bauzeit']
        gpxnaam=gpxnaam.replace(';','')
        gpxbestand.write(gpxnaam)
        gpxbestand.write('</name>\n')
        gpxbestand.write('</wpt>\n')
    lijst3=regulierh.findall(plaatjesnaam)
    if plaatjesnaam.startswith('IMG_') and plaatjesnaam.endswith('.JPG'):
      lijst3=[plaatjesnaam]
    elif len(plaatjesnaam)>12:
      lijst3=[]
    if len(lijst3)==1:
#	dictio['postcode']=dictio['postcode'][:4]+' '+dictio['postcode'][4:].strip()
      regurliera=re.compile('([0-9])')
      cijfermatch=regurliera.search(dictio['Adresse'])
      if cijfermatch:
        dictio['straatnaam']=dictio['Adresse'][:cijfermatch.start()].strip()
        dictio['huisnummer']=dictio['Adresse'][cijfermatch.start():].strip()
      else:
        dictio['straatnaam']=dictio['Adresse'].strip()
        dictio['huisnummer']=''
      if plaatjesnaam not in dictmeervoudige:
        dictmeervoudige[plaatjesnaam]=[]
        dictiolijst+=[dictio]
      else:
        dictmeervoudige[plaatjesnaam]+=[(dictio['Nummer'],dictio['straatnaam'],dictio['huisnummer'],dictio['postcode'])]
for dictio in dictiolijst:
  plaatjesnaam=dictio['Bild']
  dictio['plaats']=gewensteplaats
  if len(dictio['Ortsteil'].strip())>0 and dictio['Ortsteil'].strip() not in [gewensteplaats]:
    dictio['plaats']+='-'+dictio['Ortsteil']
  plaats=dictio['plaats']
  gewenstenaam=plaats.replace(' ','')+'-'+dictio['straatnaam'].lower().replace('.','').replace(' ','')+'-'+jaar+plaatjesnaam.lower()
  gewenstenaam=gewenstenaam.replace('img_','')
  gewenstenaam=gewenstenaam.replace(r'/','-')
  oorspronkelijkenaam=plaatjesnaam
  sedbestand.write(r'sed -i "s/'+oorspronkelijkenaam+r'/'+gewenstenaam+r'/" '+telezen+'\n')
  plaatjezoeken=glob.glob('/home/zeeman/Pictures/'+jaar+'*/'+oorspronkelijkenaam)
  if len(plaatjezoeken)==1:
    oorspronkelijkpad=plaatjezoeken[0]
  else:
    oorspronkelijkpad=dirvoorvoegsel+oorspronkelijkenaam
  beschrijving='== {{int:filedesc}} ==\n{{Information\n'
  if dictio['Bezeichnung']=='':
    beschrijving+='|description={{de|1='+'Baudenkmal'
  else:
    beschrijving+='|description={{de|1='+dictio['Bezeichnung'].replace('[[','').replace(']]','')
  if not dictio['architect']=='':
    beschrijving+=', architect '+dictio['architect']
  if not dictio['Beschreibung']=='':
    beschrijving+=', '+dictio['Beschreibung'].replace('[[','').replace(']]','')
  if not dictio['Bauzeit']=='':
    beschrijving+=', Bauzeit '+dictio['Bauzeit']
  if not dictio['Eintragung']=='':
    beschrijving+=', Baudenkmal seit '+dictio['Eintragung']
  if not dictio['oorspr_fun']=='':
    beschrijving+=', oorspronkelijk '+dictio['oorspr_fun']
  if not dictio['kadaster']=='':
    beschrijving+=', kadasteraanduiding '+dictio['kadaster']
#++', '+dictio['postcode']+' '+dictio['plaats']+'\n'
  beschrijving+='}}'
  beschrijving+='{{Kulturdenkmal|Typ=|Ort='+dictio['plaats']+'|Nummer='+dictio['Nummer']+'}}\n'
  for ding2 in dictmeervoudige[plaatjesnaam]:
    (nummer2,straatnaam2,huisnummer2,postcode2)=ding2
    beschrijving+='{{Kulturdenkmal|Typ=|Ort='+dictio['plaats']+'|Nummer='+nummer2+'}}\n'
  beschrijving+='{{Building address\n'
  beschrijving+='| Street name = '+dictio['straatnaam']+'\n'
  beschrijving+='| House number = '+dictio['huisnummer']+'\n'
#	beschrijving+='| Postal code = '+dictio['postcode']+'\n'
  beschrijving+='| City = '+dictio['plaats']+'\n'
  beschrijving+='| State = '+provincie+'\n'
  beschrijving+='| Country = DE'+'\n'
  beschrijving+='}}\n'
  for ding2 in dictmeervoudige[plaatjesnaam]:
    (objnr2,straatnaam2,huisnummer2,postcode2)=ding2
    beschrijving+='{{Building address\n'
    beschrijving+='| Street name = '+straatnaam2+'\n'
    beschrijving+='| House number = '+huisnummer2+'\n'
    beschrijving+='| Postal code = '+postcode2+'\n'
    beschrijving+='| City = '+dictio['plaats']+'\n'
    beschrijving+='| State = '+provincie+'\n'
    beschrijving+='| Country = NL'+'\n'
    beschrijving+='}}\n'
  exifdict=piexif.load(oorspronkelijkpad)
  for ifd in ('0th','Exif','GPS','1st'):
    for tag in exifdict[ifd]:
      if piexif.TAGS[ifd][tag]["name"]=='DateTime':
        datum=exifdict[ifd][tag].replace(b':',b'-',2)
  if datum<b'2005':
    datum=datumwens
  beschrijving+='|date='+str(datum).replace("b'",'').replace("'",'')+'\n'
  beschrijving+='|source={{own}}'+'\n'
  beschrijving+='|author=[[User:Pimvantend|Pim van Tend]]'+'\n'
  beschrijving+='|permission='+'\n'
  beschrijving+='|other versions='+'\n'
  beschrijving+='}}\n'
  beschrijving+='{{Object location dec|'+dictio['NS']+'|'+dictio['EW']+'}}\n'
  beschrijving+='\n'
  beschrijving+='== {{int:license-header}} ==\n'
  beschrijving+='{{self|cc-by-sa-4.0}}\n'
  beschrijving+='\n'
  if dictio['Commonscat']=='':
    beschrijving+='[[Category:Cultural heritage monuments in '+catwens+']]'
#+'\n[[Category:Uploaded via Campaign:wlm-nl]]'+'\n{{Wiki Loves Monuments 2017|nl}}'
  else:
    beschrijving+='[[Category:'+dictio['Commonscat']+']]'
#+'\n[[Category:Uploaded via Campaign:wlm-nl]]'+'\n{{Wiki Loves Monuments 2017|nl}}'
#	print beschrijving
  opdrachtbestand.write(r'echo -e "\n\n"')
  opdrachtbestand.write(r'|')
  alsopdracht='python3 pwb.py scripts/upload.py '
  alsopdracht+='-filename:'+gewenstenaam+' '+oorspronkelijkpad+' "'+beschrijving+'"'
  opdrachtbestand.write(alsopdracht)
  opdrachtbestand.write('\n')
gpxbestand.write('</gpx>\n')
gpxbestand.close()
