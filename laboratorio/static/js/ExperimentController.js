function showSponsors(response) {
    var sponsorsList  =$("#proyecto");
    var sponsor;
    for (var i=0; i <response.length; i++){
        sponsor = response[i];
        sponsorsList.append(new Option(sponsor.fields.nombre, sponsor.pk));
    }
}

function saveProject(){
    var project = {};
    project.nombre =$("#nombre").val();
    project.descripcion =$("#descripcion").val();
    project.fechaInicio =$("#fechaInicio").val();
    project.prioridad =$("#prioridad").val();
    project.estado =$("#estado").attr("id");
    project.resultado =$("#resultado").attr("id");
    project.proyecto =$("#proyecto").attr("id");
    project.patrocinador =$("#proyecto").attr("id");


    var url = $("#formAddExperiment").attr("data-add-experiment-url");
    $.ajax({
        url: host+url,
        method:"POST",
        data:experiment,
        sucess:successSaveExperiment,
        error:errorSaveExperiment,
        dataType: 'json'
    });
}

function successSaveExperiment() {

}

function errorSaveExperiment(e){
    console.log(e);
}
