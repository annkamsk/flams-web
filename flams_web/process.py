from enum import Enum, auto
from pathlib import Path
from typing import List
import uuid
from flams.input import is_valid_fasta_file, is_position_lysine

from flams_web.form import InputForm

DATA_PATH = Path(__file__).parent / "data"


class InputError(str, Enum):
    message: str

    def __new__(cls, value, message):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.message = message
        return obj

    INVALID_FASTA = (
        auto(),
        "Invalid input file. File must be a valid fasta file and contain only single sequence.",
    )
    NOT_LYSINE = auto(), "Provided position is not a lysine."


def validate_input(fasta_file: Path, position: int) -> List[InputError]:
    errors: List[InputError] = []
    if not is_valid_fasta_file(fasta_file):
        return [InputError.INVALID_FASTA]
    if not is_position_lysine(position, fasta_file):
        errors.append(InputError.NOT_LYSINE)
    return errors


def save_uploaded_file(form: InputForm) -> Path:
    fasta_file = form.fasta_file.data
    filename = uuid.uuid4().hex.upper()
    fasta_file.save(DATA_PATH / filename)
    return DATA_PATH / filename


def process_request(form: InputForm):
    file = save_uploaded_file(form)
    errors = validate_input(file, form.position.data)

    if errors:
        return errors

    # TODO run blast and serve result as a file
    # run_blast(
    #     input=file,
    #     modifications=form.modifications.data,
    #     lysine_pos=form.position.data,
    #     lysine_range=form.range.data or 0,
    # )
