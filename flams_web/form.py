from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    SubmitField,
    IntegerField,
    SelectMultipleField,
    RadioField,
    StringField,
)
from wtforms.validators import NumberRange, Optional, InputRequired, Regexp
import flams.databases.setup


class InputForm(FlaskForm):
    input_type = RadioField(
        label="Queried sequence",
        choices=["Fasta file", "Uniprot ID"],
        default="Fasta file",
    )
    fasta_file = FileField(
        validators=[
            FileAllowed(["fa", "fasta"], "Only fasta files allowed!"),
            Optional(),
        ],
    )
    uniprot_id = StringField(
        validators=[
            # https://www.uniprot.org/help/accession_numbers
            Regexp(
                r"[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}"
            ),
            Optional(),
        ]
    )
    modifications = SelectMultipleField(
        label="Modifications",
        choices=flams.databases.setup.MODIFICATIONS.keys(),
        validators=[InputRequired()],
    )
    position = IntegerField(
        "Position of modification",
        validators=[NumberRange(min=1), InputRequired()],
    )
    range = IntegerField("+/- positions", validators=[NumberRange(min=0), Optional()])
    submit = SubmitField("Submit")

    def validate(self, *args, **kwargs) -> bool:
        super(InputForm, self).validate(*args, **kwargs)
        return self.fasta_file.raw_data or self.uniprot_id.raw_data
