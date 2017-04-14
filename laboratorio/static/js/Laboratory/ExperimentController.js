var experiments;

function validateData(createExperiment){
    if(dataIsCorrect()) {
        if(createExperiment){
            saveExperiment();}
        else
            updateExperiment();
    }
}

function dataIsCorrect() {

    if($("#nombre").val().trim() == '') {
        alertify.error("El nombre es requerido",2);
        return false;
    }

    var startDate = moment($("#fechaInicio").val())
    if(startDate.isValid() ){
        var today = moment({hour:0, minutes:0})
        if(today.diff(startDate)>=0) {
            alertify.error("La fecha inicial es del pasado", 2);
            return false;
        }
    }

    if($('#proyecto option:selected').val() == -1) {
        alertify.error("Seleccione un proyecto",2);
        return false;
    }

    if($('#responsable option:selected').val() == -1) {
        alertify.error("Seleccione un responsable",2);
        return false;
    }

    if($('#estado option:selected').val() == -1) {
        alertify.error("Seleccione un estado",2);
        return false;
    }

    if($("#prioridad").val().trim() == '') {
        alertify.error("La prioridad es requerida",2);
        return false;
    }

    if($("#prioridad").val()>10 || $("#prioridad").val()<1) {
        alertify.error("La prioridad debe ser entre 1 y 10",2);
        return false;
    }

    if($("#descripcion").val().trim() == '') {
        alertify.error("La descripción es requerida",2);
        return false;
    }
    return true;
}

function saveExperiment(){
    var url = $("#formAddExperiment").attr("data-add-experiment-url");
    $.ajax({
        url: host+url,
        method:"POST",
        data:getData(),
        success:successSaveExperiment,
        error:errorSaveExperiment,
        dataType: 'json'
    });
}

function updateExperiment() {
    var url = $("#formEditExperiment").attr("data-edit-experiment-url");
    $.ajax({
        url: host + url,
        async:true,
        method: "PUT",
        data: JSON.stringify(getData()),
        success: successSaveExperiment,
        error: errorSaveExperiment
    });
}

function successSaveExperiment(response) {
    alertify.success("El experimento se ha guardado correctamente");
}

function errorSaveExperiment(response){
    alertify.error("Error al guardar el experimento");
}

function getData() {
    var experiment = {};
    experiment.nombre =$("#nombre").val();
    experiment.fechaInicio =$("#fechaInicio").val();
    experiment.idProyecto =$('#proyecto option:selected').val();
    experiment.idResponsable =$('#responsable option:selected').val();
    experiment.estado =$('#estado option:selected').val();
    experiment.prioridad =$("#prioridad").val();
    experiment.resultado =$('#resultado option:selected').val();
    experiment.descripcion =$("#descripcion").val();
    return experiment;
}

function showProyectsNames(response){
    var nameProyectList =$("#proyecto");
    var proyecto;
    nameProyectList.append(new Option("Seleccione un proyecto", -1));
    for (var i=0; i <response.length; i++){
        proyecto = response[i];
        nameProyectList.append(new Option(proyecto.fields.nombre, proyecto.pk));
    }
 }

function showResponsables(response){
    var responsablesList =$("#responsable");
    var responsable;
    responsablesList.append(new Option("Seleccione un responsable", -1));
    for (var i=0; i <response.length; i++){
        responsable = response[i];
        responsablesList.append(new Option(responsable.fields.nombre, responsable.pk));
    }
}

function showResultados(response){
    var resultadosList =$("#resultado");
    var resultado;
    resultadosList.append(new Option("Seleccione un resultado", -1));
    for (var i=0; i <response.length; i++){
        resultado = response[i];
        resultadosList.append(new Option(resultado.resultado, resultado.id));
    }
}

function showExperimentStates(response){
    var statesList =$("#estado");
    var state;
    statesList.append(new Option("Seleccione un estado", -1));
    for (var i=0; i <response.length; i++){
        state = response[i];
        statesList.append(new Option(state.estado, state.id));
    }
}

function setDate(date, id){
    var dateValue =moment(date).format('YYYY-MM-DD')
    $("#"+id).val(dateValue);
}

function showAllExperiments(urlAll, urlEdit, urlDetails,urlStartExp){
    var nameToFind = $("#name").val();
    $.ajax({
        url: urlAll+"?name="+nameToFind,
        method:"GET",
        success:function(response){paintExperiments(response,urlEdit,urlDetails,urlStartExp);},
        error:errorPaintExperiments,
        async:true,
        crossDomain:true
    });
}

function errorPaintExperiments() {
        alertify.error("No es posible recuperar los experimentos");
}

function startExperiment(id,urlAll, urlEdit, urlDetails,urlStartExp){
    $.ajax({
        url: urlStartExp.replace("{idExp}", id),
        method:"POST",
        data:JSON.stringify({id:id}),
        success:function () {
            showAllExperiments(urlAll, urlEdit, urlDetails,urlStartExp)
        },
        error:errorSaveExperiment,
        dataType: 'json'
    });
}
function paintExperiments(data, urlEdit, urlDetails, urlStartExp) {
    console.log(data)
    urlEdit = urlEdit.replace("0","{idExp}");
    urlDetails = urlDetails.replace("0","{idExp}");
    urlStartExp = urlStartExp.replace("0","{idExp}");
    var html = "";
    if(data.length==0) {
        html="<h1>No se han encontrado experimentos</h1>";
    }else {
        var experiment,state;
        experiments = data;
        var startExp;
        for (var i=0; i<experiments.length;i++)
        {
            experiment = experiments[i];
            if(experiment.fechaInicio!= undefined)
                startExp = experiment.fechaInicio;
            else
                startExp = "<a class=\"btn btn-info\" onclick='startExperiment("+experiment.id+",\""+urlAll+"\",\""+urlEdit+"\", \""+urlDetails+"\",\""+urlStartExp+"\");'>iniciar</a>"

            html += "<tr class='alt'>";
            html += "<td>" + experiment.nombre + "</td>";
            html += "<td>" + experiment.estado + "</td>";
            html += "<td>" + experiment.prioridad + "</td>";
            html += "<td>" + startExp + "</td>";
            html += "<td>" + experiment.proyecto + "</td>";
            html += "<td>" + experiment.responsable + "</td>";
            state = experiment.resultado != -1 ? experiment.resultado: "";
            html += "<td>" + state  + "</td>";
            html += "<td style=\"width: 10%\"><a href=\""+urlEdit.replace("{idExp}",experiment.id)+ "\" class=\"btn btn-info btn-round\"><span class=\"glyphicon glyphicon-pencil\"></span></a>";
            html += "<a href=\""+urlDetails.replace("{idExp}",experiment.id)+ "\" class=\"btn btn-info btn-round\"><span class=\"glyphicon glyphicon-cog\"></span></a></td>";
            html += "</tr>";
        }
    }
    $("#projects tbody").html(html);
}