import json
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError, NotFound
from datetime import datetime
from ..models import Proyecto, Patrocinador, Experimento, EstadoProyecto
from django.shortcuts import render
from rest_framework import generics
from ..serializers import ProyectoSerializer


class ProyectosLista(generics.ListAPIView):
    serializer_class = ProyectoSerializer
    def get_queryset(self):
        name = self.request.query_params.get('name')
        if(name):
           proyectos = Proyecto.objects.filter(nombre__icontains=name)
        else:
            proyectos = Proyecto.objects.all()
        return proyectos


def agregar_proyecto(request):
    return render(request, 'laboratorio/Proyecto/agregarProyecto.html')


def listar_proyectos(request):
    return render(request, 'laboratorio/Proyecto/proyectos.html')


def editar_proyecto(request, id):
    proyecto = Proyecto.objects.get(id=id)
    return render(request, 'laboratorio/Proyecto/editarProyecto.html', {"proyecto": proyecto})


#Atiende las peticiones de los Proyectos
@csrf_exempt
def proyectos(request):
    if request.method == 'POST':
        data = request.POST
        proyecto = Proyecto()
        if data.has_key("id"):
            proyecto.id = data["id"]
        if data.has_key("nombre"):
            proyecto.nombre = data["nombre"]
        if data.has_key("descripcion"):
            proyecto.descripcion = data["descripcion"]
        if data.has_key("fechaInicio"):
            fechaInicioUnicode = data["fechaInicio"]
            proyecto.fechaInicio = None
            if fechaInicioUnicode is not None:
                proyecto.fechaInicio = datetime.strptime(fechaInicioUnicode, '%Y-%m-%d')
        if data.has_key("fechaFinal"):
            fechaFinalUnicode = data["fechaFinal"]
            proyecto.fechaFinal = None
            if fechaFinalUnicode is not None:
                proyecto.fechaFinal = datetime.strptime(fechaFinalUnicode, '%Y-%m-%d')
        if data.has_key("prioridad"):
            proyecto.prioridad = data["prioridad"]
        if data.has_key("avance"):
            proyecto.avance = data["avance"]
        if data.has_key("estado"):
            proyecto.estado = data["estado"]
        if data.has_key("idPatrocinador"):
            idPatrocinador = data["idPatrocinador"]
            try:
                patrocinador = Patrocinador.objects.get(id=idPatrocinador)
            except:
                raise ValidationError({'idPatrocinador': ['No existe patrocinador ' + idPatrocinador]})
            proyecto.patrocinador = patrocinador
        proyecto.save()
        return HttpResponse(serializers.serialize("json", [proyecto]))
    # Si es GET Lista
    elif request.method == 'GET':
        proyectos = Proyecto.objects.all()
        return HttpResponse(serializers.serialize("json", proyectos))

#Atiende las peticiones de un Proyecto determinado
@csrf_exempt
def proyectos_id(request, id):

    # Si es DELETE Borra
    if request.method == 'DELETE':
        try:
            proyecto = Proyecto.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe Proyecto ' + id]})
        proyecto.delete()
        return JsonResponse({"Mensaje":"Proyecto " + id + " borrado"})
    # Si es PUT Actualiza
    elif request.method == 'PUT':
        try:
            proyecto = Proyecto.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe Proyecto ' + id]})
        data = json.loads(request.body)
        algoCambio = False
        if data.has_key("nombre"):
            proyecto.nombre = data["nombre"]
            algoCambio = True
        if data.has_key("descripcion"):
            proyecto.descripcion = data["descripcion"]
            algoCambio = True
        if data.has_key("fechaInicio"):
            fechaInicioUnicode = data["fechaInicio"]
            proyecto.fechaInicio = None
            if fechaInicioUnicode is not None:
                proyecto.fechaInicio = datetime.strptime(fechaInicioUnicode, '%Y-%m-%d')
            algoCambio = True
        if data.has_key("fechaFinal"):
            fechaFinalUnicode = data["fechaFinal"]
            proyecto.fechaFinal = None
            if fechaFinalUnicode is not None:
                proyecto.fechaFinal = datetime.strptime(fechaFinalUnicode, '%Y-%m-%d')
            algoCambio = True
        if data.has_key("prioridad"):
            proyecto.prioridad = data["prioridad"]
            algoCambio = True
        if data.has_key("avance"):
            proyecto.avance = data["avance"]
            algoCambio = True
        if data.has_key("estado"):
            proyecto.estado = data["estado"]
            algoCambio = True
        if data.has_key("idPatrocinador"):
            idPatrocinador = data["idPatrocinador"]
            algoCambio = True
            try:
                patrocinador = Patrocinador.objects.get(id=idPatrocinador)
            except:
                raise ValidationError({'idPatrocinador': ['No existe patrocinador ' + idPatrocinador]})
            proyecto.patrocinador = patrocinador
        if algoCambio:
            proyecto.save()
        return HttpResponse(serializers.serialize("json", [proyecto]), content_type="application/json")
    # Si es GET Lista
    elif request.method == 'GET':
        try:
            proyecto = Proyecto.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe Proyecto ' + id]})
        return HttpResponse(serializers.serialize("json", [proyecto]), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest proyectos/{id} con metodo " + request.method)


#Atiende las peticiones de un Proyecto determinado
@csrf_exempt
def proyectos_id_experimentos(request, id):
    # Si es GET Lista
    if request.method == 'GET':
        try:
            proyecto = Proyecto.objects.get(id=id)
        except:
            raise ValidationError({'id': ['No existe proyecto ' + id]})
        experimentos = Experimento.objects.filter(proyecto=proyecto)
        return HttpResponse(serializers.serialize("json", experimentos), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest proyectos/{id}/experimentos con metodo " + request.method)


#Atiende las peticiones de Estados de Proyecto
@csrf_exempt
def lista_estados_proyecto(request):
    # Si es GET Lista
    if request.method == 'GET':
        try:
            estados = EstadoProyecto().getDict()
        except:
            raise ValidationError({'id': ['No fue posible generar la lista de estados de proyecto']})
        return HttpResponse(json.dumps(estados), content_type="application/json")
    else:
        raise NotFound(detail="No se encuentra comando rest estadosproyecto/ con metodo " + request.method)


@csrf_exempt
def lista_estados_proyecto(request):
     # Si es GET Lista
     if request.method == 'GET':
         try:
             estados = EstadoProyecto().getDict()
         except:
             raise ValidationError({'id': ['No fue posible generar la lista de estados de proyecto']})
         return HttpResponse(json.dumps(estados), content_type="application/json")
     else:
         raise NotFound(detail="No se encuentra comando rest estadosproyecto/ con metodo " + request.method)