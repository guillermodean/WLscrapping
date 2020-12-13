import bs4
from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import pandas as pd

df=pd.DataFrame(columns={"Nombre","URL","Km","Dificultad","Ubicación"})

#DONE iterar por todas las paginas
for n in range(0,2400,24):
    my_url="https://es.wikiloc.com/rutas/senderismo?act=1&from="+str(n)+"&to="+str(n+24)

    #Pongo mozilla para que no me lo reconozca como un buscador e inicializo uReq
    req=Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})
    uClient=uReq(req)
    page_html=uClient.read()
    uClient.close()

    #Defino la función para corregir el texto
    def replace_text(string):
        #string=string.replace("\t","")
        #string=string.replace("\n","")
        string=string.replace("\xa0"," ")
        return string #Can be done with .strip() all but \xa0

    #Parse Html
    page_soup=soup(page_html,"html.parser")
    containers=page_soup.findAll("div",{"class":"info col-md-7 col-sm-6 col-xs-10"})


    #Itero por los contenedores
    for container in containers:
        #DONE solo recoger datos en los que ficha_ubicación contenga Navarra
        ficha_ubicacion = container.findAll("p", {"class": "description"})
        ficha_ubicacion = ficha_ubicacion[0].text.strip()
        ficha_ubicacion = replace_text(ficha_ubicacion)


        ubicacion="Navarra"
        if ubicacion in ficha_ubicacion:
            ficha_url=container.h3.a["href"]
            ficha_nombre=container.h3.a["title"]
            ficha_km=container.p.strong.text.strip()
            ficha_km=replace_text(ficha_km)
            ficha_dificultad=container.p.span.text.strip()
            ficha_dificultad=replace_text(ficha_dificultad)
            registro={"Nombre":ficha_nombre,"URL":ficha_url,"Km":ficha_km,"Dificultad":ficha_dificultad,"Ubicación":ficha_ubicacion}
            df=df.append(registro,ignore_index=True)

    #TODO ver si se puede scrapear las cordenadas desde las urls
    df.to_csv('wikiloc',sep=";")
