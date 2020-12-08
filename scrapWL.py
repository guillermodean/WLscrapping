import bs4
from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import pandas as pd

#Defining and opening conexion to navarra routes
my_url="https://es.wikiloc.com/rutas/senderismo"
#pongo mozilla para que no me pille.
req=Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})

uClient=uReq(req)
page_html=uClient.read()
uClient.close()

def replace_text(string):
    #string=string.replace("\t","")
    #string=string.replace("\n","")
    string=string.replace("\xa0"," ")
    return string #Can be done with .strip() all but \xa0

#Parse Html

page_soup=soup(page_html,"html.parser")
containers=page_soup.findAll("div",{"class":"info col-md-7 col-sm-6 col-xs-10"})
print(len(containers))
df=pd.DataFrame(columns={"Nombre","URL","Km","Dificultad","Ubicación"})
for container in containers:
    ficha_url=container.h3.a["href"]
    ficha_nombre=container.h3.a["title"]
    ficha_km=container.p.strong.text.strip()
    ficha_km=replace_text(ficha_km)
    ficha_dificultad=container.p.span.text.strip()
    ficha_dificultad=replace_text(ficha_dificultad)
    ficha_ubicacion=container.findAll("p",{"class":"description"})
    ficha_ubicacion=ficha_ubicacion[0].text.strip()
    ficha_ubicacion=replace_text(ficha_ubicacion)
    registro={"Nombre":ficha_nombre,"URL":ficha_url,"Km":ficha_km,"Dificultad":ficha_dificultad,"Ubicación":ficha_ubicacion}
    df=df.append(registro,ignore_index=True)

df.to_csv('wikiloc',sep=";")
