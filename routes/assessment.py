import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename
from models import db, Assessment
from ai.image_validator import validate_images, is_valid_image
from ai.vision import analyze_image

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

        new_assessment = Assessment(
            user_id=session["user_id"],
            image_paths="",
            status="uploaded"
        )
        db.session.add(new_assessment)
        db.session.commit()

        assessment_folder = os.path.join(
            current_app.config["UPLOAD_FOLDER"], str(new_assessment.id)
        )
        os.makedirs(assessment_folder, exist_ok=True)

        saved_paths = []
        for f in files:
            if f.filename == "":
                continue
            filename = secure_filename(f.filename)
            filepath = os.path.join(assessment_folder, filename)
            f.save(filepath)

            if not is_valid_image(filepath):
                os.remove(filepath)
                flash(filename + " is not a valid or is a corrupted image.")
                db.session.delete(new_assessment)
                db.session.commit()
                return redirect(url_for("assessment.upload"))

            saved_paths.append(filepath)

        all_findings = []
        for path in saved_paths:
            image_findings = analyze_image(path)
            all_findings.extend(image_findings)

        new_assessment.image_paths = ",".join(saved_paths)
        new_assessment.findings = json.dumps(all_findings)
        new_assessment.status = "analyzed"
        db.session.commit()

        flash("Images uploaded and analyzed. Assessment ID: " + str(new_assessment.id))
        return redirect(url_for("assessment.view_assessment", assessment_id=new_assessment.id))

    return render_template("upload.html")

@assessment_bp.route("/assessment/<int:assessment_id>")
def view_assessment(assessment_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    assessment = Assessment.query.get_or_404(assessment_id)
    if assessment.user_id != session["user_id"]:
        flash("You do not have access to that assessment.")
        return redirect(url_for("auth.dashboard"))

    image_list = assessment.image_paths.split(",") if assessment.image_paths else []
    image_names = []
    for p in image_list:
        rel = os.path.relpath(p, current_app.config["UPLOAD_FOLDER"])
        rel = rel.replace("\\", "/")
        image_names.append(rel)

    findings = json.loads(assessment.findings) if assessment.findings else []

    return render_template(
        "assessment_detail.html",
        assessment=assessment,
        image_names=image_names,
        findings=findings
    )
