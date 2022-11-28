import csv
from flask import Flask, redirect, render_template, request, send_file, url_for
from flask_bootstrap import Bootstrap4
from flams_web.process import (
    ProcessedRequest,
    get_results_filename,
    is_valid_request_id,
    process_request,
    run_blast_and_save_result,
)

from flams_web.form import InputForm
import os
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()

app.config.update(
    DEBUG=os.environ.get("ENV") == "TEST",
    SECRET_KEY=os.environ.get("SECRET_KEY"),
    MAX_CONTENT_LENGTH=20 * 1024 * 1024,  # allow files <= 20MB
)

Bootstrap4(app)


@app.route("/", methods=["POST", "GET"])
def index():
    form = InputForm(modifications=["acetylation"])
    processed_request = None
    if form.validate_on_submit():
        processed_request = process_request(form)
        if processed_request.is_success:
            return redirect(
                url_for("result", processed_request=processed_request.to_json())
            )
    return render_template("index.html", form=form, processed_request=processed_request)


@app.route("/result")
def result():
    data = request.args.get("processed_request")
    processed_request = ProcessedRequest.from_json(data)
    results_file = run_blast_and_save_result(processed_request)
    results = []
    with open(results_file) as fd:
        reader = csv.reader(fd, delimiter="\t")
        for row in reader:
            results.append(row)
    return render_template(
        "results.html", processed_request=processed_request, results=results
    )


@app.route("/download", methods=["GET"])
def download_result():
    result_id = request.args.get("id")
    if is_valid_request_id(result_id):
        return "Invalid result ID"

    results_file = get_results_filename(result_id)
    return send_file(results_file, as_attachment=True)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
