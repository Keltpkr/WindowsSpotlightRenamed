import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import time

# Dossiers source et destination
source_dir = r"C:\Users\kelt_\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets"
destination_dir = r"C:\Users\kelt_\Pictures\WindowsSpotlightRenamed"

# Modèle local BLIP
model_path = r"C:\Models\blip-image-captioning-base"

# Vérifie si le dossier de destination existe, sinon le crée
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

def generate_description(image_path):
    """Génère une description pour une image donnée."""
    try:
        with Image.open(image_path) as image:
            image = image.convert("RGB")
            inputs = processor(image, return_tensors="pt")
            caption = model.generate(**inputs)
            description = processor.decode(caption[0], skip_special_tokens=True)
            return description.replace(" ", "_").replace(",", "").replace(".", "").replace("'", "").lower()
    except Exception as e:
        print(f"Erreur lors de la description de l'image {image_path}: {e}")
        return None

def wait_for_file(file_path, retries=5, delay=1):
    """Attendre que le fichier soit disponible pour lecture/écriture."""
    for _ in range(retries):
        try:
            with open(file_path, "rb"):
                return True
        except IOError:
            time.sleep(delay)
    return False

def process_images():
    """Parcourir les fichiers source et renommer les images en mode paysage."""
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)

        if os.path.isfile(file_path) and os.path.getsize(file_path) > 100 * 1024:  # Ignorer les petits fichiers
            temp_image_path = os.path.join(destination_dir, filename + ".tmp.jpg")

            # Copier le fichier temporairement
            try:
                # Attendre que le fichier soit libéré
                if not wait_for_file(file_path):
                    print(f"Le fichier {file_path} est verrouillé. Ignoré.")
                    continue

                with open(file_path, "rb") as src, open(temp_image_path, "wb") as dst:
                    dst.write(src.read())

                # Vérifier les dimensions de l'image
                try:
                    img = Image.open(temp_image_path)
                    if img.width > img.height:  # Vérifie que l'image est en mode paysage
                        new_name = generate_description(temp_image_path)
                        img.close()  # Fermer explicitement l'image
                        if new_name:
                            new_file_path = os.path.join(destination_dir, new_name + ".jpg")
                            os.replace(temp_image_path, new_file_path)  # Renommer avec remplacement sécurisé
                            print(f"Image renommée : {new_file_path}")
                        else:
                            print(f"Aucune description générée pour l'image {filename}.")
                            os.remove(temp_image_path)
                    else:
                        print(f"L'image {filename} n'est pas en mode paysage. Ignorée.")
                        img.close()  # Fermer explicitement l'image
                        os.remove(temp_image_path)
                except Exception as e:
                    print(f"Erreur lors du traitement de l'image {file_path}: {e}")
                    if os.path.exists(temp_image_path):
                        os.remove(temp_image_path)  # Nettoyer les fichiers temporaires
            except Exception as e:
                print(f"Erreur lors de la copie du fichier {file_path}: {e}")

if __name__ == "__main__":
    # Charger le modèle BLIP
    try:
        print("Chargement du modèle BLIP...")
        processor = BlipProcessor.from_pretrained(model_path)
        model = BlipForConditionalGeneration.from_pretrained(model_path)
        print("Modèle BLIP chargé avec succès.")
    except Exception as e:
        print(f"Erreur lors du chargement du modèle BLIP : {e}")
        exit(1)

    # Traiter les images
    process_images()
