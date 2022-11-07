
let inputTypeRadios = document.getElementsByName("input_type");


inputTypeRadios.forEach(element => element.addEventListener("change", e => {
    if (e.target.checked) {
        if (e.target.id == "input_type-0") {
            document.getElementById("fasta_file").hidden = false;
            document.getElementById("uniprot").hidden = true;
        } else {
            document.getElementById("fasta_file").hidden = true;
            document.getElementById("uniprot").hidden = false;
        }
    }
}));
