from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (
    SubmitField,
    IntegerField,
    SelectMultipleField,
    RadioField,
    StringField,
)
from wtforms.validators import NumberRange, Optional, InputRequired, Regexp


class InputForm(FlaskForm):
    input_type = RadioField(
        label="Queried sequence",
        choices=["Fasta file", "Uniprot ID"],
        default="Fasta file",
    )
    fasta_file = FileField(
        validators=[
            FileRequired(),
            FileAllowed([".fa", ".fasta"], "Only fasta files allowed!"),
        ],
    )
    uniprot_id = StringField(
        validators=[
            # https://www.uniprot.org/help/accession_numbers
            Regexp(
                r"[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}"
            )
        ]
    )
    modifications = SelectMultipleField(
        label="Modifications",
        choices=["acetylation"],
        validators=[InputRequired()],
    )
    position = IntegerField(
        "Position of modification",
        validators=[NumberRange(min=1), InputRequired()],
    )
    range = IntegerField("+/- positions", validators=[NumberRange(min=0), Optional()])
    submit = SubmitField("Submit")
