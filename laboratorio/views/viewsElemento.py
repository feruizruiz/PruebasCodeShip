import json
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError, NotFound
from ..models import Elemento, Paso, UnidadElemento

#Atiende las peticiones de los Elementos
@csrf_exempt
def elementos(request):

    # Si es POST Graba
    if request.method == 'POST':
        data = json.loads(request.body)
        elemento = Elemento()
        if data.has_key("id"):
            elemento.id = data["id"]
        if data.has_key("nombre"):
            elemento.nombre = data["nombre"]
        if data.has_key("cantidad"):
            elemento.cantidad = data["cantidad"]
        if data.has_key("unidades"):
            elemento.unidades = data["unidades"]
        if data.has_key("idPaso"):
            idPaso = data["idPaso"]
            try:
                paso = Paso.objects.get(id=idPaso)
            except:
                raise ValidationError({'idPaso': ['No existe paso ' + idPaso]})
            elemento.paso = paso
        elemento.save()
        return HttpResponse(serializers.serialize("json", [elemento]), content_type="application/json")
    # Si es GET Lista
    elif request.method == 'GET':
        elementos = Elemento.objects.all()
        return HttpResponse(serializers.serialize("json", elementos), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest elementos con metodo " + request.method)

#Atiende las peticiones de un Elemento determinado
@csrf_exempt
def elementos_id(request, id):

    # Si es DELETE Borra
    if request.method == 'DELETE':
        try:
            elemento = Elemento.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe elemento ' + id]})
        elemento.delete()
        return JsonResponse({"Mensaje":"Elemento " + id + " borrado"})
    # Si es PUT Actualiza
    elif request.method == 'PUT':
        try:
            elemento = Elemento.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe elemento ' + id]})
        data = json.loads(request.body)
        algoCambio = False
        if data.has_key("nombre"):
            elemento.nombre = data["nombre"]
            algoCambio = True
        if data.has_key("cantidad"):
            elemento.cantidad = data["cantidad"]
            algoCambio = True
        if data.has_key("unidades"):
            elemento.unidades = data["unidades"]
            algoCambio = True
        if data.has_key("idPaso"):
            idPaso = data["idPaso"]
            algoCambio = True
            try:
                paso = Paso.objects.get(id=idPaso)
            except:
                raise ValidationError({'idPaso': ['No existe paso ' + idPaso]})
            elemento.paso = paso
        if algoCambio:
            elemento.save()
        return HttpResponse(serializers.serialize("json", [elemento]), content_type="application/json")
    # Si es GET Lista
    elif request.method == 'GET':
        try:
            elemento = Elemento.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe elemento ' + id]})
        return HttpResponse(serializers.serialize("json", [elemento]), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest elementos/{id} con metodo " + request.method)


#Atiende las peticiones de Unidades de Elemento
@csrf_exempt
def lista_unidades_elemento(request):
    # Si es GET Lista
    if request.method == 'GET':
        try:
            unidades = UnidadElemento().getDict()
            print unidades
        except:
            raise ValidationError({'id': ['No fue posible generar la lista de unidades de elemento']})
        return HttpResponse(json.dumps(unidades), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest unidadeselemento/ con metodo " + request.method)
