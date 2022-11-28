
let inputTypeRadios = document.getElementsByName("input_type");


inputTypeRadios.forEach(element => element.addEventListener("change", e => {
    if (e.target.checked) {
        if (e.target.id == "input_type-0") {
            document.getElementById("fasta").hidden = false;
            document.getElementById("fasta_file").required = true;

            document.getElementById("uniprot").hidden = true;
            document.getElementById("uniprot_id").required = false;

        } else {
            document.getElementById("fasta").hidden = true;
            document.getElementById("fasta_file").required = false;

            document.getElementById("uniprot").hidden = false;
            document.getElementById("uniprot_id").required = true;
        }
    }
}));

document.getElementById("uniprotSearch").addEventListener("click", (e) => {
    var uniprotId = document.getElementById("uniprot_id").value;
    fetch(`https://rest.uniprot.org/uniprotkb/${uniprotId}?format=json`)
        .then(res => {
            if (!res.ok) {
                throw new Error("Invalid Uniprot ID");
            }
            return res.json()
        })
        .then(data => {
            const name = data.proteinDescription.recommendedName.fullName.value;
            document.getElementById("uniprotSearchResult").innerHTML = `<b>Uniprot OK</b>:${name}`;
            document.getElementById("uniprotSearchResult").hidden = false;
        })
        .catch(error => {
            document.getElementById("uniprotSearchResult").innerHTML = error;
            document.getElementById("uniprotSearchResult").hidden = false;
        })
})