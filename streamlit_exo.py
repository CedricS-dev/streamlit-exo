#********************************************************
# Nom ......... : streamlit_exo.py
# Rôle ........ : Code Python pour l'application Streamlit du cour OC
# Auteur ...... : Cedric SAGHI
# Version ..... : V0.1 du 28/03/2025
# Licence ..... : Réalisé dans le cadre du cours outils collaboratifs, chapitre 4, L1 informatique
# (../..)
# Compilation : aucune
# Usage : Pour exécuter : streamlit run streamlit_exo.py
#******************************************************** 


import streamlit as st
from exif import Image
from streamlit_folium import st_folium
import folium


# Image avec données EXIF à récupérer/modifier
photo = "Canon_40D.jpg"
# Coordonnées GPS de mon adresse
mon_adresse_gps = {
  "ville": "Morsang sur Orge",
  "latitude": 48.6595060199332,
  "longitude": 2.3426597977904797,
}
# Liste de coordonnées GPS de villes à vister
lieux_a_visiter = [
  {"ville": "Tokyo",
   "latitude": 35.75301067318405, 
   "longitude": 139.20383719685626 },
  {"ville": "Osaka",
   "latitude": 34.67079400535055, 
   "longitude": 135.4982224716991},
  {"ville": "Miami",
   "latitude": 25.760302216311736, 
   "longitude": -80.19398019978458},
  {"ville": "New York",
   "latitude": 40.7121198027981, 
   "longitude": -74.0200284586749},
  {"ville": "Florence",
   "latitude": 43.7691670050572,
   "longitude": 11.255043509117757},
  {"ville": "Rome",
   "latitude": 41.893259290361435, 
   "longitude": 12.468178215218568},
  {"ville": "St Pétersbourg",
   "latitude": 59.93793922179285,
   "longitude":  30.32398586577688},
  {"ville": "Prague",
   "latitude": 50.074097847515006,
   "longitude": 14.434029540724943},
  {"ville": "Oslo",
   "latitude": 59.912345838918824,
   "longitude": 10.751464244354647},
]

# Les différents exercices sont répartis dans des onglets sur l'application
tab1, tab2, tab3 = st.tabs(["Données EXIF", "Données GPS", "Lieux"])


def modifier_exif(image:str) -> None :
  """Récupère les données EXIF d'une image et les affiche dans un formulaire de
  modification dans une app Strealit.

  Args:
      image (str): Nom de l'image à traiter
  """
  # Affiche un titre et l'image dans la page
  st.title("Formulaire de modification des données EXIF")
  st.image(image, caption=f"{image}")
  # Ouvre l'image en mode binaire
  with open(image, "rb") as img_file :
    img = Image(img_file)
    # Récupère la liste des données EXIF
    data_list = img.list_all()
    # Dans un formulaire streamlit
    with st.form("Éditer les données EXIF") :
      # Pour chaque donnée dans la liste
      for data in data_list :
        # Imprime la donnée et sa valeur
        st.write(data," : " ,img.get(data))
        # Puis créé un champ de formulaire correspondant
        new_data = st.text_input(f"Entrez la valeur {data} :")
        # Si le formulaire a été remplis
        if new_data :
          # Enregistre la nouvelle valeur
          img[data] = (new_data)
          st.write("Nouvelle valeur = ", data," : " , img.get(data))
      
      # Et ajoute un bouton de validation
      submitted = st.form_submit_button("Enregistrer les modifications")
      if submitted :
        # Ouvre l'image en mode écriture et sauvegarde les changements
        with open(image, 'wb') as new_image_file:
          new_image_file.write(img.get_file())
  

def ajouter_gps(image:str, adresse:dict) -> None :
  """Ajoute les coordonnées GPS aux tag EXIF sur une image dans une app Streamlit.

  Args:
      image (str): Nom de l'image à traiter
      adresse (dict): Dictionnaire contenant les coordonnées GPS à ajouter  
  """
  # Affiche un titre et l'image dans la page
  st.title("Coordonées GPS de mon adresse")
  st.image(image, caption=f"{image}")
  # Ouvre l'image en mode binaire
  with open(image, "rb") as img_file :
    img = Image(img_file)
    # Ajoute les donnée GPS à l'image
    img.set("gps_latitude", f"{adresse["latitude"]}")
    img.set("gps_latitude_ref", "N")
    img.set("gps_longitude", f"{adresse["longitude"]}")
    img.set("gps_longitude_ref", "W")
    
    # Récupère la latitude et la longitude dans l'image
    ma_latitude = img.get("gps_latitude")
    ma_longitude =  img.get("gps_longitude")
    # Affiche ces données dans la page
    st.write("Latitude N : " , ma_latitude)
    st.write("Longitude W : " , ma_longitude)
  # Et enregistre les modifications
  with open(image, 'wb') as new_image_file:
    new_image_file.write(img.get_file())


def afficher_carte(image: str) -> None :
  """Affiche sur une carte dans une application Streamlit l'emplacement GPS
  enregistré dans les données EXIF.

  Args:
      image (str): Nom de l'image à traiter
  """
  # Ouvre l'image en mode lecture binaire
  with open(image, "rb") as img_file :
    img = Image(img_file)
    # Récupère la latitude et la longitude dans l'image
    ma_latitude = img.get("gps_latitude")
    ma_longitude =  img.get("gps_longitude")
    
    # Créé une carte folium centrée sur mon adresse et ajoute un marqueur
    m = folium.Map(location = [ma_latitude, ma_longitude], zoom_start=16)
    folium.Marker(
      [ma_latitude, ma_longitude],
      popup="Mon adresse",
      tooltip="Mon adresse",
      icon=folium.Icon(color="green", icon="home")
    ).add_to(m)
    # Affiche la carte
    st_folium(m, width=750)
    

def a_visiter(lieux:list, depart:dict) -> None :
  """Affiche sur une carte dans une app Streamlit les lieux dont les coordonnées
  GPS sont contenues dans une liste et les lie à une adresse de départ.

  Args:
      lieux (list): Liste de dictionnaire de lieux à visiter
      depart (dict): Dictionnaire contenant les coordonnées du point de départ 
  """
  st.title("Lieux à visiter")
  # Ajoute les lieux à visiter sur la carte
  m = folium.Map()
  for lieu in lieux :
    folium.Marker(
      [lieu["latitude"], lieu["longitude"]],
      popup=f"{lieu["ville"]}",
      tooltip=f"{lieu["ville"]}",
      icon=folium.Icon(color="blue")
    ).add_to(m)
  # Ajoute l'adresse de départ
  folium.Marker(
    [depart["latitude"], depart["longitude"]],
    popup=depart["ville"],
    tooltip=depart["ville"],
    icon=folium.Icon(color="green", icon="home")
  ).add_to(m)
  # Pour chaque lieu à visiter, ajoute une ligne (AntPath) connectant
  # l'adresse de départ à ce lieu
  for lieu in lieux :
    folium.plugins.AntPath(
      locations=[[depart["latitude"], depart["longitude"]],
        [lieu["latitude"], lieu["longitude"]]],
    ).add_to(m)
  # affiche la carte
  st_folium(m, width=750)


# Lance les exercices dans les onglets
with tab1 :
  modifier_exif(photo)
with tab2 :
  ajouter_gps(photo, mon_adresse_gps)
  afficher_carte(photo)
with tab3 :
  a_visiter(lieux_a_visiter, mon_adresse_gps)