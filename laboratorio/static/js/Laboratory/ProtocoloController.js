/**
 * Created by Lenovo on 26/03/2017.
 */
url="/laboratorio/protocolofiltro" ;
var table ;
var data ;
var  listarProtocolos= function(){
 var table = $('#myTable').DataTable( {
        "ajax": {
            "url":  host+url,
            "dataSrc": ""
        },
        "columns": [
            { data: "titulo" },
            { data: "descripcion" },
            { data: "version" },
            { data: "categoria" },
            { "defaultContent": "<a href='#'  id='btn' class='btn btn-info btn-round'><span class='glyphicon glyphicon-plus'></span></a>" },
        ]
        } );

        $('#myTable tbody').on( 'click', '#btn', function () {
            var data = table.row( $(this).parents('tr') ).data();
            crearVersion(data.id)

        } );
}

function crearVersion(id)
{
    var settings = {
    "async": true,
    "crossDomain": true,
    "url": host+"/laboratorio/protocolos/"+id+"/nuevaVersion/",
    "method": "POST",
    "headers": {}
    }

    if(confirm("Esta seguro de crear una nueva version ?")) {
        $.ajax(settings).done(function (response) {
            alert("Se registro con exito")
            location.reload();
        });
    }else{
        return false;
    }
}