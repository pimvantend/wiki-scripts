#!/usr/bin/env python3
import urllib.request,urllib.parse
#,re
def wikihaald(gemeente):
  aan=False
#  gemeente='Hopsten'
  schrijfbestand=open(gemeente.lower()+'.txt','wb')
  opvraging='https://de.wikipedia.org/w/index.php?title=Liste_der_Baudenkm%C3%A4ler_in_'+urllib.parse.quote(gemeente)+'&action=edit'
  with urllib.request.urlopen(opvraging) as response:
#  html=response.read()
    for regel in response:
#    if b' name="wpTextbox1">' in bytes(regel):
      plaats=regel.find(b' name="wpTextbox1">')
#    regulierampersand=re.compile(r'(/&.*/;)')
#    ampersandlijst=regulierampersand.findall(regel)
#    for ding in ampersandlijst:
      regel1=regel.replace(b'&amp;',b'&')
#    if aan and not regel1==regel:
#      print(regel)
#      print(regel1)
      regel1=regel1.replace(b'&lt;',b'<')
      if plaats>0:
        aan=True
        regel1=regel1[plaats+19:]
      if aan and regel.startswith(b'</textarea>'):
        aan=False
      if aan:
        schrijfbestand.write(regel1)
#+'\n')
  schrijfbestand.close()
