#!/usr/bin/env python
import re
import piexif
import subprocess
import glob
appendofwrite='w'
telezen='bocholt.txt'
dirvoorvoegsel='/home/zeeman/Pictures/170623-woestehoeve/'
datumwens='2018-01-25 13:30'
catwens="Bocholt"
#'Burgemeesterswijk en Hoogkamp, Arnhem'
#'Geitenkamp, Arnhem'
jaar='18'
gewensteplaats="Bocholt"
provincie='NW'
sedbestandnaam=telezen.replace('.txt','.bash')
sedbestand=open(sedbestandnaam,'w')
subprocess.call(['chmod','a+xwr',sedbestandnaam])
gpxbestandnaam=telezen.replace('.txt','.gpx')
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
wikibestand=open(telezen,'r')
opdrachtbestandsnaam='/home/zeeman/Downloads/core_stable/oplaad-'+telezen.replace('.txt','.bash')
opdrachtbestand=open(opdrachtbestandsnaam,appendofwrite)
subprocess.call(['chmod','a+xwr',opdrachtbestandsnaam])
wikibestand=wikibestand.read()
#print wikibestand
wikibestand=wikibestand.replace('\n',' ')
regulierltgt=re.compile('(<.*?>)')
lijstltgt=regulierltgt.findall(wikibestand)
for dingltgt in lijstltgt:
  wikibestand=wikibestand.replace(dingltgt,'')
#wikibestand=wikibestand.replace(' =','=')
wikibestand=wikibestand.replace('&nbsp;',' ')
wikibestand=wikibestand.replace('commonscat=','commonscat =')
wikibestand=wikibestand.replace('image=','image =')
reguliera=re.compile('({{[^D].*?}})')
lijst1=reguliera.findall(wikibestand)
#print lijst1
for ding in lijst1:
    wikibestand=wikibestand.replace(ding,'')
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
	ietslijst=iets.split('=')
	if len(ietslijst)==2:
	    sleutel=ietslijst[0].strip()
	    waarde=ietslijst[1].strip()
	    dictio[sleutel]=waarde
    plaatjesnaam=dictio['Bild']
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
	plaats=dictio['plaats']
	gewenstenaam=plaats.replace(' ','')+'-'+dictio['straatnaam'].lower().replace('.','').replace(' ','')+'-'+jaar+plaatjesnaam.lower()
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
	    beschrijving+='|description={{nl|1='+dictio['Bezeichnung']
	if not dictio['architect']=='':
	    beschrijving+=', architect '+dictio['architect']
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
#	beschrijving+='{{Gemeentelijk monument|'+dictio['gemcode']+'/'+dictio['objnr']+'}}\n'
	for ding2 in dictmeervoudige[plaatjesnaam]:
	    (objnr2,straatnaam2,huisnummer2,postcode2)=ding2
	    beschrijving+='{{Gemeentelijk monument|'+dictio['gemcode']+'/'+objnr2+'}}\n'
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
		    datum=exifdict[ifd][tag].replace(':','-',2)
	if datum<'2005':
	    datum=datumwens
	beschrijving+='|date='+datum+'\n'
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
	    beschrijving+='[[Category:Baudenkmaeler in '+catwens+']]'
#+'\n[[Category:Uploaded via Campaign:wlm-nl]]'+'\n{{Wiki Loves Monuments 2017|nl}}'
	else:
	    beschrijving+='[[Category:'+dictio['Commonscat']+']]'
#+'\n[[Category:Uploaded via Campaign:wlm-nl]]'+'\n{{Wiki Loves Monuments 2017|nl}}'
#	print beschrijving
	alsopdracht='python3 pwb.py scripts/upload.py '
	alsopdracht+='-filename:'+gewenstenaam+' '+oorspronkelijkpad+' "'+beschrijving+'"'
	opdrachtbestand.write(alsopdracht)
	opdrachtbestand.write('\n')
gpxbestand.write('</gpx>\n')
