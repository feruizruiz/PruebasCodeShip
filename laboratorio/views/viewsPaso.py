import json
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError, NotFound
from ..models import Paso, Protocolo, Elemento

#Atiende las peticiones de los Pasos
@csrf_exempt
def pasos(request):

    # Si es POST Graba
    if request.method == 'POST':
        data = json.loads(request.body)
        paso = Paso()
        if data.has_key("id"):
            paso.id = data["id"]
        if data.has_key("nombre"):
            paso.nombre = data["nombre"]
        if data.has_key("idProtocolo"):
            idProtocolo = data["idProtocolo"]
            try:
                protocolo = Protocolo.objects.get(id=idProtocolo)
            except:
                raise ValidationError({'idProtocolo': ['No existe protocolo ' + idProtocolo]})
            paso.protocolo = protocolo
        paso.save()
        return HttpResponse(serializers.serialize("json", [paso]), content_type="application/json")
    # Si es GET Lista
    elif request.method == 'GET':
        pasos = Paso.objects.all()
        return HttpResponse(serializers.serialize("json", pasos), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest pasos con metodo " + request.method)

#Atiende las peticiones de un Paso determinado
@csrf_exempt
def pasos_id(request, id):

    # Si es DELETE Borra
    if request.method == 'DELETE':
        try:
            paso = Paso.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe paso ' + id]})
        paso.delete()
        return JsonResponse({"Mensaje":"Paso " + id + " borrado"})
    # Si es PUT Actualiza
    elif request.method == 'PUT':
        try:
            paso = Paso.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe paso ' + id]})
        data = json.loads(request.body)
        algoCambio = False
        if data.has_key("nombre"):
            paso.nombre = data["nombre"]
            algoCambio = True
        if data.has_key("idProtocolo"):
            idProtocolo = data["idProtocolo"]
            algoCambio = True
            try:
                protocolo = Protocolo.objects.get(id=idProtocolo)
            except:
                raise ValidationError({'idProtocolo': ['No existe protocolo ' + idProtocolo]})
            paso.protocolo = protocolo
        if algoCambio:
            paso.save()
        return HttpResponse(serializers.serialize("json", [paso]), content_type="application/json")
    # Si es GET Lista
    elif request.method == 'GET':
        try:
            paso = Paso.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe paso ' + id]})
        return HttpResponse(serializers.serialize("json", [paso]), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest pasos/{id} con metodo " + request.method)

#Atiende las peticiones de un Experimento determinado
@csrf_exempt
def pasos_id_elementos(request, id):
    # Si es GET Lista
    if request.method == 'GET':
        try:
            paso = Paso.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe paso ' + id]})
        elementos = Elemento.objects.filter(paso=paso)
        return HttpResponse(serializers.serialize("json", elementos), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest elementos/{id}/pasos con metodo " + request.method)