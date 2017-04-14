import json
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError, NotFound
from ..models import Patrocinador, Proyecto


#Atiende las peticiones de los Patrocinadores
@csrf_exempt
def patrocinadores(request):

    # Si es POST Graba
    if request.method == 'POST':
        data = json.loads(request.body)
        patrocinador = Patrocinador()
        if data.has_key("id"):
            patrocinador.id = data["id"]
        if data.has_key("nombre"):
            patrocinador.nombre = data["nombre"]
        patrocinador.save()
        return HttpResponse(serializers.serialize("json", [patrocinador]), content_type="application/json")
    # Si es GET Lista
    elif request.method == 'GET':
        patrocinadores = Patrocinador.objects.all()
        return HttpResponse(serializers.serialize("json", patrocinadores), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest patrocinadores con metodo " + request.method)


#Atiende las peticiones de un Patrocinador determinado
@csrf_exempt
def patrocinadores_id(request, id):

    # Si es DELETE Borra
    if request.method == 'DELETE':
        try:
            patrocinador = Patrocinador.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe patrocinador ' + id]})
        patrocinador.delete()
        return JsonResponse({"Mensaje":"Patrocinador " + id + " borrado"})
    # Si es PUT Actualiza
    elif request.method == 'PUT':
        try:
            patrocinador = Patrocinador.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe patrocinador ' + id]})
        data = json.loads(request.body)
        algoCambio = False
        if data.has_key("nombre"):
            patrocinador.nombre = data["nombre"]
            algoCambio = True
        if algoCambio:
            patrocinador.save()
        return HttpResponse(serializers.serialize("json", [patrocinador]), content_type="application/json")
    # Si es GET Lista
    elif request.method == 'GET':
        try:
            patrocinador = Patrocinador.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe patrocinador ' + id]})
        return HttpResponse(serializers.serialize("json", [patrocinador]), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest patrocinadores/{id} con metodo " + request.method)

#Atiende las peticiones de un Patrocinador determinado
@csrf_exempt
def patrocinadores_id_proyectos(request, id):
    # Si es GET Lista
    if request.method == 'GET':
        try:
            patrocinador = Patrocinador.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe patrocinador ' + id]})
        proyectos = Proyecto.objects.filter(patrocinador=patrocinador)
        return HttpResponse(serializers.serialize("json", proyectos), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest patrocinadores/{id}/proyectos con metodo " + request.method)
