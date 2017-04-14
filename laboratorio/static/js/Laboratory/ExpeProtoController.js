/**
 * Created by Lenovo on 28/03/2017.
 */
url="/laboratorio/Experimento/experimentos/";
function listarProtocolosExperimento(buscar){
    var settings = {
    "async": true,
    "crossDomain": true,
    "url": host+url+buscar+"/protocolos/",
    "method": "GET",
    "headers": {}
    }
    var html="";

     $.ajax(settings).done(function (response) {
         for(var i in response) {
                var objeto = response[i] ;
                html+="<tr class='alt'>";
                html+="<td>"+objeto.fields.titulo+"</td>";
                html+="<td>"+objeto.fields.descripcion+"</td>";
                html+="<td>"+objeto.fields.version+"</td>";
                html+="<td>"+objeto.fields.categoria+"</td>";
                html+="</tr>";
         }
       $("#myTable tbody").html(html);
        //console.log(response);
   });
}

function showProtocolos(response) {
    var protocoloList  =$("#protocolo");
    var protocolo;
    protocoloList.append(new Option("Seleccione un Protocolo", -1));
    for (var i=0; i <response.length; i++){
        protocolo = response[i];
        protocoloList.append(new Option(protocolo.fields.titulo+" V "+protocolo.fields.version, protocolo.pk));
    }
}

function agregarExperimentoProtocolo(id)
{
    var data = {};
    data.idExperimento =id;
    data.idProtocolo = $('#protocolo option:selected').val();

    if(protocolo==-1)
    {
        alert("Debe seleccionar  un protocolo ")
        return false;
    }
    var settings = {
    "async": true,
    "crossDomain": true,
    "url": host+"/laboratorio/protocolosExperimento/",
    "method": "POST",
    "headers": {
    "content-type": "application/json"
    },
    "processData": false,
    "data": JSON.stringify(data)
    }
    if(confirm("Esta seguro de agregar un nuevo protocolo ?")) {
        // alert("Responde ");
        $.ajax(settings).done(function (response) {
        alert("Se registro con exito")
        location.reload();
        });
    }else{
        return false;
    }
}