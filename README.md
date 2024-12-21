# WindowsSpotlightRenamed
Python script that get Spotlight pictures in a temp folder. Analyse them with IA and rename them with an accurate name 

# Guide de Configuration pour le Modèle BLIP

## Fichiers Obligatoires pour BLIP

### `config.json`
- Contient les paramètres de configuration du modèle.
- Nécessaire pour que `BlipProcessor` et `BlipForConditionalGeneration` comprennent la structure du modèle.

### `pytorch_model.bin`
- Le fichier principal contenant les poids entraînés du modèle.
- C'est souvent le fichier le plus volumineux (plusieurs centaines de Mo).

### `tokenizer_config.json`
- Contient la configuration utilisée pour le tokenizer (prétraitement des données textuelles).

### `special_tokens_map.json`
- Une carte des tokens spéciaux (par exemple, `[CLS]`, `[SEP]`) utilisés par le tokenizer.

### `vocab.txt` (ou fichier similaire, spécifique au modèle)
- Le vocabulaire utilisé par le tokenizer pour convertir les mots en identifiants numériques.

### `preprocessor_config.json`
- Spécifie comment le prétraitement des images est réalisé avant d'être envoyées au modèle.

---

## Étapes pour Télécharger les Fichiers

### 1. Accédez au Modèle sur Hugging Face
- [Salesforce/blip-image-captioning-base](https://huggingface.co/Salesforce/blip-image-captioning-base).

### 2. Téléchargez Chaque Fichier Individuellement
- Cliquez sur les noms des fichiers mentionnés ci-dessus pour les télécharger.

### 3. Créez un Dossier Local
- Par exemple : `C:\Models\blip-image-captioning-base`.

### 4. Placez Tous les Fichiers dans ce Dossier
- Assurez-vous que tous les fichiers téléchargés sont regroupés dans ce dossier.

---

## Structure du Dossier Après Téléchargement
Votre dossier `C:\Models\blip-image-captioning-base` devrait contenir ces fichiers :

```
C:\Models\blip-image-captioning-base\
│
├── config.json
├── pytorch_model.bin
├── preprocessor_config.json
├── special_tokens_map.json
├── tokenizer_config.json
└── vocab.txt
```

---

## Pourquoi Ces Fichiers Sont Nécessaires ?

### `config.json`
- Permet au modèle de savoir comment il a été configuré lors de son entraînement.

### `pytorch_model.bin`
- Contient les paramètres appris pendant l'entraînement.

### `preprocessor_config.json` et `tokenizer_config.json`
- Aident à normaliser les images et les textes d'entrée pour qu'ils soient compatibles avec le modèle.

### `special_tokens_map.json` et `vocab.txt`
- Définit comment le texte est tokenisé pour générer ou comprendre des légendes.

---

## Vérification Après Téléchargement

Lancez un petit script Python pour vérifier que le modèle est bien chargé :

```python
from transformers import BlipProcessor, BlipForConditionalGeneration

model_path = r"C:\Models\blip-image-captioning-base"

try:
    processor = BlipProcessor.from_pretrained(model_path)
    model = BlipForConditionalGeneration.from_pretrained(model_path)
    print("Le modèle BLIP a été chargé avec succès.")
except Exception as e:
    print(f"Erreur lors du chargement du modèle : {e}")
```

### Si ce script fonctionne, vous êtes prêt à exécuter le script complet.

