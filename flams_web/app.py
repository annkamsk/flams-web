from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap4
from flams_web.process import (
    ProcessedRequest,
    process_request,
    run_blast_and_save_result,
)

from flams_web.form import InputForm


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
    run_blast_and_save_result(processed_request)
    return "Success"


if __name__ == "__main__":
    app.run(debug=True)
