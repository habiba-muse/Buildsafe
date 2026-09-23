import os
from PIL import Image

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS

def is_valid_image(filepath):
    try:
        img = Image.open(filepath)
        img.verify()
        return True
    except Exception:
        return False

def validate_images(files):
    errors = []
    if len(files) == 0:
        errors.append("Please upload at least 1 image.")
    if len(files) > 5:
        errors.append("You can upload a maximum of 5 images.")
    for f in files:
        if f.filename == "":
            continue
        if not allowed_file(f.filename):
            errors.append(f.filename + ": only PNG, JPG, JPEG allowed.")
    return errors
