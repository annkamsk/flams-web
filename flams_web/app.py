from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap4
from flams_web.process import (
    ProcessedRequest,
    process_request,
    run_blast_and_save_result,
    _get_results_filename
)
from flask import send_file
from flams_web.form import InputForm
import csv


app = Flask(__name__)

# FIXME do not deploy to production before setting proper env vars here!!!
app.config.update(
    DEBUG=True,
    SECRET_KEY="192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf",
    MAX_CONTENT_LENGTH=20 * 1024 * 1024,  # allow files <= 20MB
)

Bootstrap4(app)


@app.route("/", methods=["POST", "GET"])
def index():
    form = InputForm(modifications=["acetylation"])
    if form.validate_on_submit():
        processed_request = process_request(form)
        if processed_request.is_success:
            results_file = run_blast_and_save_result(processed_request)

            # Read results from file into an array
            results=[]
            with open(results_file) as fd:
                reader = csv.reader(fd, delimiter="\t")
                for row in reader:
                    results.append(row)

            return render_template("index.html", form=form, processed_request=processed_request, results=results)

    return render_template("index.html", form=form, processed_request=None)

@app.route("/result")
def result():
    result_id = request.args.get('id')
    # Check that the result-id is given AND that it is alphanumeric only
    # Need to be careful here coz if input is not filtered, user could give path to any file in OS and download it...
    # Alphanumeric restriction should take care of this.
    if not result_id or not result_id.isalnum():
        return "Invalid result ID"

    results_file = _get_results_filename(result_id)

    # Return the results file to the user.
    return send_file(results_file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
