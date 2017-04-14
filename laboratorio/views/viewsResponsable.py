import json
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError, NotFound
from ..models import Responsable, Experimento

#Atiende las peticiones de los Responsables
@csrf_exempt
def responsables(request):

    # Si es POST Graba
    if request.method == 'POST':
        data = json.loads(request.body)
        responsable = Responsable()
        if data.has_key("id"):
            responsable.id = data["id"]
        if data.has_key("nombre"):
            responsable.nombre = data["nombre"]
        responsable.save()
        return HttpResponse(serializers.serialize("json", [responsable]), content_type="application/json")
    # Si es GET Lista
    elif request.method == 'GET':
        responsables = Responsable.objects.all()
        return HttpResponse(serializers.serialize("json", responsables), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest responsables con metodo " + request.method)

#Atiende las peticiones de un Responsable determinado
@csrf_exempt
def responsables_id(request, id):

    # Si es DELETE Borra
    if request.method == 'DELETE':
        try:
            responsable = Responsable.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe responsable ' + id]})
        responsable.delete()
        return JsonResponse({"Mensaje":"Responsable " + id + " borrado"})
    # Si es PUT Actualiza
    elif request.method == 'PUT':
        try:
            responsable = Responsable.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe responsable ' + id]})
        data = json.loads(request.body)
        algoCambio = False
        if data.has_key("nombre"):
            responsable.nombre = data["nombre"]
            algoCambio = True
        if algoCambio:
            responsable.save()
        return HttpResponse(serializers.serialize("json", [responsable]), content_type="application/json")
    # Si es GET Lista
    elif request.method == 'GET':
        try:
            responsable = Responsable.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe responsable ' + id]})
        return HttpResponse(serializers.serialize("json", [responsable]), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest responsables/{id} con metodo " + request.method)

#Atiende las peticiones de un Responsable determinado
@csrf_exempt
def responsables_id_experimentos(request, id):
    # Si es GET Lista
    if request.method == 'GET':
        try:
            responsable = Responsable.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe responsable ' + id]})
        experimentos = Experimento.objects.filter(responsable=responsable)
        return HttpResponse(serializers.serialize("json", experimentos), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest proyectos/{id}/experimentos con metodo " + request.method)