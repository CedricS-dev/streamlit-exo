import streamlit as st
from exif import Image


def modifier_exif(image:str) :
  # Affiche l'image dans la page
  st.image(image, caption=f"{image}")
  # Ouvre l'image en mode binaire
  with open(image, "rb") as img_file :
    img = Image(img_file)

    # Récupère la liste des données EXIF
    data_list = img.list_all()

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
  
  # Ouvre l'image en mode écriture et sauvegarde les changements
  with open(image, 'wb') as new_image_file:
    new_image_file.write(img.get_file())

modifier_exif("Canon_40D.jpg")