function validateData(createProject){
    if(dataIsCorrect()) {
        if(createProject)
            saveProject();
        else
            updateProject();
    }
}

function dataIsCorrect() {

    if($("#nombre").val().trim() == '') {
        alertify.error("El nombre es requerido",2);
        return false;
    }

    if($("#descripcion").val().trim() == '') {
        alertify.error("La descripción es requerida",2);
        return false;
    }

    if($("#prioridad").val().trim() == '') {
        alertify.error("La prioridad es requerida",2);
        return false;
    }

    if($("#avance").val().trim() == '') {
        alertify.error("El avance es requerido",2);
        return false;
    }

    if($("#avance").val()>100 || $("#avance").val()<0) {
        alertify.error("El avance debe ser entre 0% y 100%",2);
        return false;
    }

    if($("#prioridad").val()>10 || $("#prioridad").val()<1) {
        alertify.error("La prioridad debe ser entre 1 y 10",2);
        return false;
    }

    var startDate = moment($("#fechaInicio").val())
    var endDate  =moment($("#fechaFinal").val());
    if(!startDate.isValid() || !endDate.isValid()){
        alertify.error("Las fechas son requeridas",2);
        return false;
    }

    if(startDate.diff(endDate)>=0) {
        alertify.error("La fecha incial debe ser menor a la fecha final",2);
        return false;
    }

    if($('#estado option:selected').val() == -1) {
        alertify.error("Seleccione un estado",2);
        return false;
    }

    if($('#patrocinador option:selected').val() == -1) {
        alertify.error("Seleccione un patrocinador",2);
        return false;
    }
    return true;
}

function saveProject() {
    var url = $("#formProject").attr("data-project-url");
    $.ajax({
        url: host+url,
        method:"POST",
        data:getData(),
        success:successSaveProject,
        error:errorSaveProject,
        dataType: "json"
    });
}

function updateProject() {
    var url = $("#formProject").attr("data-project-url");
    $.ajax({
        url: host + url,
        async:true,
        method: "PUT",
        data: JSON.stringify(getData()),
        success: successSaveProject,
        error: errorSaveProject,

    });
}

function getData() {
     var project = {};
    project.nombre =$("#nombre").val();
    project.descripcion =$("#descripcion").val();
    project.fechaInicio =$("#fechaInicio").val();
    project.fechaFinal =$("#fechaFinal").val();
    project.prioridad =$("#prioridad").val();
    project.avance =$("#avance").val();
    project.estado =$('#estado option:selected').val();
    project.idPatrocinador =$('#patrocinador option:selected').val();

    return project;
}

function successSaveProject(response) {
    alertify.success("El proyecto se ha guardado correctamente");
}

function errorSaveProject(e){
    alertify.error("Error al guardar el proyecto");
}

function showProjectStates(response){
    var statesList =$("#estado");
    var state;
    statesList.append(new Option("Seleccione un estado", -1));

    for (var i=0; i <response.length; i++){
        state = response[i];
        statesList.append(new Option(state.estado, state.id));
    }
}

function showSponsors(response) {
    var sponsorsList  =$("#patrocinador");
    var sponsor;
    sponsorsList.append(new Option("Seleccione un patrocinador", -1));
    for (var i=0; i <response.length; i++){
        sponsor = response[i];
        sponsorsList.append(new Option(sponsor.fields.nombre, sponsor.pk));
    }
}

function setDate(date, id){
    var dateValue =moment(date).format('YYYY-MM-DD')
    $("#"+id).val(dateValue);
}

function showAllProjects(urlAll, urlEdit){
    var nameToFind = $("#name").val();
    $.ajax({
        url: urlAll+"?name="+nameToFind,
        method:"GET",
        success:function(response){paintProjects(response,urlEdit);},
        error:errorPaintProjects,
        async:true,
        crossDomain:true
    });
}

function errorPaintProjects() {
        alertify.error("No es posible recuperar los proyectos");
}

function paintProjects(data, urlEdit) {
    console.log(data)
    urlEdit = urlEdit.replace("0","{idProject}");
    var html = "";
    if(data.length==0) {
        html="<h1>No se han encontrado proyectos</h1>";
    }else {
        var project;
        for (var i=0; i<data.length;i++)
        {
            project = data[i];
            html += "<tr class='alt'>";
            html += "<td>" + project.nombre + "</td>";
            html += "<td>" + project.avance + "</td>";
            html += "<td>" + project.estado + "</td>";
            html += "<td>" + project.prioridad + "</td>";
            html += "<td>" + project.fechaInicio + "</td>";
            html += "<td style=\"width: 10%\"><a href=\""+urlEdit.replace("{idProject}",project.pk)+ "\" class=\"btn btn-info btn-round\"><span class=\"glyphicon glyphicon-pencil\"></span></a></td>";
            html += "</tr>";
        }
    }
    $("#projects tbody").html(html);
}