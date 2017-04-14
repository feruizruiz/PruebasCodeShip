import json
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError, NotFound
from ..models import Protocolo, Experimento, Paso, CategoriaProtocolo
from django.shortcuts import render
from rest_framework import generics
from ..serializers import ProtocoloSerializer
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

class ProtocoloList(generics.ListAPIView):
    serializer_class = ProtocoloSerializer
    def get_queryset(self):
        titulo = self.request.query_params.get('titulo')
        if(titulo) :
           protocolo = Protocolo.objects.filter(titulo__icontains=titulo)
        else :
            protocolo = Protocolo.objects.all()
        return protocolo

def listar_protocolos(request):
    return render(request, 'laboratorio/Protocolo/protocolos.html', {"protocolos": Protocolo.objects.all()})

#Atiende las peticiones de los Protocolos
@csrf_exempt
def protocolos(request):
    # Si es POST Graba
    if request.method == 'POST':
        data = json.loads(request.body)
        protocolo = Protocolo()
        if data.has_key("id"):
            protocolo.id = data["id"]
        if data.has_key("titulo"):
            protocolo.titulo = data["titulo"]
        if data.has_key("descripcion"):
            protocolo.descripcion = data["descripcion"]
        if data.has_key("version"):
            protocolo.version = data["version"]
        if data.has_key("categoria"):
            protocolo.categoria = data["categoria"]
        protocolo.save()
        return HttpResponse(serializers.serialize("json", [protocolo]), content_type="application/json")
    # Si es GET Lista
    elif request.method == 'GET':
        protocolos = Protocolo.objects.all()
        return HttpResponse(serializers.serialize("json", protocolos), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest protocolos con metodo " + request.method)

#Atiende las peticiones de un Protocolo determinado
@csrf_exempt
def protocolos_id(request, id):

    # Si es DELETE Borra
    if request.method == 'DELETE':
        try:
            protocolo = Protocolo.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe protocolo ' + id]})
        protocolo.delete()
        return JsonResponse({"Mensaje":"Protocolo " + id + " borrado"})
    # Si es PUT Actualiza
    elif request.method == 'PUT':
        try:
            protocolo = Protocolo.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe protocolo ' + id]})
        data = json.loads(request.body)
        algoCambio = False
        if data.has_key("titulo"):
            protocolo.titulo = data["titulo"]
            algoCambio = True
        if data.has_key("descripcion"):
            protocolo.descripcion = data["descripcion"]
            algoCambio = True
        if data.has_key("version"):
            protocolo.version = data["version"]
            algoCambio = True
        if data.has_key("categoria"):
            protocolo.categoria = data["categoria"]
            algoCambio = True
        if algoCambio:
            protocolo.save()
        return HttpResponse(serializers.serialize("json", [protocolo]), content_type="application/json")
    # Si es GET Lista
    elif request.method == 'GET':
        try:
            protocolo = Protocolo.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe protocolo ' + id]})
        return HttpResponse(serializers.serialize("json", [protocolo]), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest protocolos/{id} con metodo " + request.method)

#Atiende las peticiones de un Experimento determinado
@csrf_exempt
def protocolos_id_experimentos(request, id):
    # Si es GET Lista
    if request.method == 'GET':
        try:
            protocolo = Protocolo.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe protocolo ' + id]})
        experimentos = Experimento.objects.filter(protocolo=protocolo)
        return HttpResponse(serializers.serialize("json", experimentos), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest protocolos/{id}/experimentos con metodo " + request.method)

#Atiende las peticiones de un Experimento determinado
@csrf_exempt
def protocolos_id_pasos(request, id):
    # Si es GET Lista
    if request.method == 'GET':
        try:
            protocolo = Protocolo.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe protocolo ' + id]})
        pasos = Paso.objects.filter(protocolo=protocolo)
        return HttpResponse(serializers.serialize("json", pasos), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest protocolos/{id}/pasos con metodo " + request.method)

#Atiende las peticiones de un Protocolo determinado duplicandolo sumandole uno a la version
@csrf_exempt
def protocolos_id_nueva_version(request, id):
    # Si es POST crea la nueva version
    if request.method == 'POST':
        try:
            protocolo = Protocolo.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe protocolo ' + id]})
        if protocolo.version is None:
            protocolo.version = 0
        else:
            protocolo.version = protocolo.version + 1
        protocolo.pk = None
        protocolo.save()
        return HttpResponse(serializers.serialize("json", [protocolo]), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest protocolos/{id}/nuevaVersion/ con metodo " + request.method)


#Atiende las peticiones de Categorias de Protocolo
@csrf_exempt
def lista_categorias_protocolo(request):
    # Si es GET Lista
    if request.method == 'GET':
        try:
            categorias = CategoriaProtocolo().getDict()
            print categorias
        except:
            raise ValidationError({'id': ['No fue posible generar la lista de categorias de protocolo']})
        return HttpResponse(json.dumps(categorias), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest categoriasprotocolo/ con metodo " + request.method)