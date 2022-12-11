from dataclasses import dataclass, field
import dataclasses
from enum import Enum, auto
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid
from flams.input import is_valid_fasta_file, is_position_lysine
from flams.databases.setup import update_db_for_modifications
from flams.run_blast import run_blast
from flams.display import display_result
import requests
from flams_web.form import InputForm

UPLOAD_PATH = Path(__file__).parent / "upload"
RESULTS_PATH = Path(__file__).parent / "data"


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


@dataclass
class RequestData:
    position: int
    range: int = 0
    modifications: List[str] = field(default_factory=lambda: [])


@dataclass
class ProcessedRequest:
    id: str
    data: RequestData
    errors: List[InputError] = field(default_factory=lambda: [])

    def __init__(
        self,
        id: str,
        data: Dict[str, Any] = {},
        errors: List[InputError] = [],
        form: Optional[InputForm] = None,
    ) -> None:
        self.id = id
        self.errors = errors
        if form:
            self.data = RequestData(
                form.position.data, form.range.data or 0, form.modifications.data
            )
        else:
            self.data = RequestData(**data)

    @property
    def is_success(self) -> bool:
        return len(self.errors) == 0

    def to_json(self) -> str:
        return json.dumps(dataclasses.asdict(self))

    @staticmethod
    def from_json(value: str) -> "ProcessedRequest":
        data = json.loads(value)
        return ProcessedRequest(**data)


def validate_input(fasta_file: Path, position: int) -> List[InputError]:
    errors: List[InputError] = []
    if not is_valid_fasta_file(fasta_file):
        return [InputError.INVALID_FASTA]
    if not is_position_lysine(position, fasta_file):
        errors.append(InputError.NOT_LYSINE)
    return errors


def save_uploaded_file(form: InputForm, request_id: str) -> Path:
    fasta_file = form.fasta_file.data
    filename = f"{request_id}.fa"
    fasta_file.save(UPLOAD_PATH / filename)
    return UPLOAD_PATH / filename


def save_protein_from_uniprot(form: InputForm, request_id: str) -> Path:
    uniprot_id = form.uniprot_id.data
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
    r = requests.get(url)

    r.raise_for_status()

    filename = UPLOAD_PATH / f"{request_id}.fa"
    with filename.open("w+") as f:
        f.write(r.text)

    return filename


def process_request(form: InputForm) -> ProcessedRequest:
    request_id = generate_request_id()

    if form.fasta_file.data:
        file = save_uploaded_file(form, request_id)
    else:
        file = save_protein_from_uniprot(form, request_id)
    errors = validate_input(file, form.position.data)
    return ProcessedRequest(request_id, form=form, errors=errors)


def generate_request_id():
    return uuid.uuid4().hex.upper()


def run_blast_and_save_result(request: ProcessedRequest):
    # TODO this should be run within some setup function on app install
    update_db_for_modifications(request.data.modifications)
    results = run_blast(
        input=UPLOAD_PATH / f"{request.id}.fa",
        modifications=request.data.modifications,
        lysine_pos=request.data.position,
        lysine_range=request.data.range,
    )
    filename = RESULTS_PATH / f"{request.id}.tsv"
    display_result(filename, results)
    return filename


def is_valid_request_id(request_id: Optional[str]) -> bool:
    """
    Check that the result-id is given AND that it is alphanumeric only
    Need to be careful here coz if input is not filtered, user could give path to any file in OS and download it...
    Alphanumeric restriction should take care of this.
    """
    return request_id is not None and request_id.isalnum() and len(request_id) == 16


def get_results_filename(request_id):
    return RESULTS_PATH / f"{request_id}.tsv"
