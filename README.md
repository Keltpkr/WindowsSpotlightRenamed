# WindowsSpotlightRenamed
Python script that get Spotlight pictures in a temp folder. Analyse them with IA and rename them with an accurate name 
#
#
# BLIP Model Setup Guide

## Required Files for BLIP

### `config.json`
- Contains the model configuration parameters.
- Required for `BlipProcessor` and `BlipForConditionalGeneration` to understand the model structure.

### `pytorch_model.bin`
- The main file containing the trained model weights.
- This is often the largest file (several hundred MB).

### `tokenizer_config.json`
- Contains the configuration used for the tokenizer (text preprocessing).

### `special_tokens_map.json`
- A map of special tokens (e.g., `[CLS]`, `[SEP]`) used by the tokenizer.

### `vocab.txt` (or a similar file specific to the model)
- The vocabulary used by the tokenizer to convert words into numerical IDs.

### `preprocessor_config.json`
- Specifies how the images are preprocessed before being sent to the model.

---

## Steps to Download the Files

### 1. Access the Model on Hugging Face
- [Salesforce/blip-image-captioning-base](https://huggingface.co/Salesforce/blip-image-captioning-base).

### 2. Download Each File Individually
- Click on the file names mentioned above to download them.

### 3. Create a Local Folder
- For example: `C:\Models\blip-image-captioning-base`.

### 4. Place All Files in This Folder
- Ensure all the downloaded files are grouped in this folder.

---

## Folder Structure After Download
Your folder `C:\Models\blip-image-captioning-base` should contain these files:

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

## Why Are These Files Necessary?

### `config.json`
- Enables the model to understand how it was configured during training.

### `pytorch_model.bin`
- Contains the parameters learned during training.

### `preprocessor_config.json` and `tokenizer_config.json`
- Help normalize the input images and text to be compatible with the model.

### `special_tokens_map.json` and `vocab.txt`
- Define how text is tokenized to generate or understand captions.

---

## Verification After Download

Run a small Python script to verify that the model is properly loaded:

```python
from transformers import BlipProcessor, BlipForConditionalGeneration

model_path = r"C:\Models\blip-image-captioning-base"

try:
    processor = BlipProcessor.from_pretrained(model_path)
    model = BlipForConditionalGeneration.from_pretrained(model_path)
    print("The BLIP model has been successfully loaded.")
except Exception as e:
    print(f"Error loading the model: {e}")
```

### If this script works, you are ready to run the complete script.
