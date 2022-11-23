from flask import Flask, render_template
from flask_bootstrap import Bootstrap4
from flams_web.process import process_request

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
    if form.validate_on_submit():
        processed_request = process_request(form)
        return render_template(
            "index.html", form=form, processed_request=processed_request
        )

    return render_template("index.html", form=form, processed_request=None)


if __name__ == "__main__":
    app.run(debug=True)
