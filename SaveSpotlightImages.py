import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import time

# Source and destination directories
source_dir = r"C:\Users\kelt_\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets"
destination_dir = r"C:\Users\kelt_\Pictures\WindowsSpotlightRenamed"

# Local BLIP model
model_path = r"C:\Models\blip-image-captioning-base"

# Check if the destination folder exists, otherwise create it
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

def generate_description(image_path):
    """Generate a description for a given image."""
    try:
        with Image.open(image_path) as image:
            image = image.convert("RGB")
            inputs = processor(image, return_tensors="pt")
            caption = model.generate(**inputs)
            description = processor.decode(caption[0], skip_special_tokens=True)
            return description.replace(" ", "_").replace(",", "").replace(".", "").replace("'", "").lower()
    except Exception as e:
        print(f"Error generating description for the image {image_path}: {e}")
        return None

def wait_for_file(file_path, retries=5, delay=1):
    """Wait until the file is available for read/write."""
    for _ in range(retries):
        try:
            with open(file_path, "rb"):
                return True
        except IOError:
            time.sleep(delay)
    return False

def process_images():
    """Iterate through the source files and rename landscape images."""
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)

        if os.path.isfile(file_path) and os.path.getsize(file_path) > 100 * 1024:  # Ignore small files
            temp_image_path = os.path.join(destination_dir, filename + ".tmp.jpg")

            # Temporarily copy the file
            try:
                # Wait for the file to be released
                if not wait_for_file(file_path):
                    print(f"The file {file_path} is locked. Skipped.")
                    continue

                with open(file_path, "rb") as src, open(temp_image_path, "wb") as dst:
                    dst.write(src.read())

                # Check the image dimensions
                try:
                    img = Image.open(temp_image_path)
                    if img.width > img.height:  # Check if the image is in landscape mode
                        new_name = generate_description(temp_image_path)
                        img.close()  # Explicitly close the image
                        if new_name:
                            new_file_path = os.path.join(destination_dir, new_name + ".jpg")
                            os.replace(temp_image_path, new_file_path)  # Rename with secure replacement
                            print(f"Image renamed: {new_file_path}")
                        else:
                            print(f"No description generated for the image {filename}.")
                            os.remove(temp_image_path)
                    else:
                        print(f"The image {filename} is not in landscape mode. Skipped.")
                        img.close()  # Explicitly close the image
                        os.remove(temp_image_path)
                except Exception as e:
                    print(f"Error processing the image {file_path}: {e}")
                    if os.path.exists(temp_image_path):
                        os.remove(temp_image_path)  # Clean up temporary files
            except Exception as e:
                print(f"Error copying the file {file_path}: {e}")

if __name__ == "__main__":
    # Load the BLIP model
    try:
        print("Loading the BLIP model...")
        processor = BlipProcessor.from_pretrained(model_path)
        model = BlipForConditionalGeneration.from_pretrained(model_path)
        print("BLIP model successfully loaded.")
    except Exception as e:
        print(f"Error loading the BLIP model: {e}")
        exit(1)

    # Process the images
    process_images()
