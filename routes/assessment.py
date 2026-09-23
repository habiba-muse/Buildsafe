import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename
from models import db, Assessment
from ai.image_validator import validate_images, is_valid_image

assessment_bp = Blueprint("assessment", __name__)

@assessment_bp.route("/upload", methods=["GET", "POST"])
def upload():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        files = request.files.getlist("images")

        errors = validate_images(files)
        if errors:
            for e in errors:
                flash(e)
            return redirect(url_for("assessment.upload"))

        saved_paths = []
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)

        for f in files:
            if f.filename == "":
                continue
            filename = secure_filename(f.filename)
            filepath = os.path.join(upload_folder, filename)
            f.save(filepath)

            if not is_valid_image(filepath):
                os.remove(filepath)
                flash(filename + " is not a valid or is a corrupted image.")
                return redirect(url_for("assessment.upload"))

            saved_paths.append(filepath)

        new_assessment = Assessment(
            user_id=session["user_id"],
            image_paths=",".join(saved_paths),
            status="uploaded"
        )
        db.session.add(new_assessment)
        db.session.commit()

        flash("Images uploaded successfully. Assessment ID: " + str(new_assessment.id))
        return redirect(url_for("auth.dashboard"))

    return render_template("upload.html")
