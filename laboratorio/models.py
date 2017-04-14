from __future__ import unicode_literals
from django.db import models


# Clase Patrocinador: Define un Patrocinador de proyectos
class Patrocinador(models.Model):
    nombre = models.CharField(max_length=250, null=True)

# Clase EstadoProyecto: Define los posibles estados de un Proyecto
class EstadoProyecto:
    INICIADO = 0
    TERMINADO = 1
    EN_PROGRESO = 2
    CANCELADO = 3
    PAUSADO = 4
    CHOICES = (
        (INICIADO, 'Iniciado'),
        (TERMINADO, 'Terminado'),
        (EN_PROGRESO, 'En Progreso'),
        (CANCELADO, 'Cancelado'),
        (PAUSADO, 'Pausado')
    )

    def getDict(self):
        return [{'id': estado[0], 'estado': estado[1]} for estado in self.CHOICES]

# Clase Proyecto: Define un Proyecto del Laboratorio auspiciado por una persona
class Proyecto(models.Model):
    nombre = models.CharField(max_length=100, null=True)
    descripcion = models.CharField(max_length=1000, null=True)
    fechaInicio = models.DateField(null=True)
    fechaFinal = models.DateField(null=True)
    prioridad = models.IntegerField(null=True)
    avance = models.FloatField(null=True)
    estado = models.IntegerField(choices=EstadoProyecto.CHOICES, null=True)
    patrocinador = models.ForeignKey(Patrocinador, related_name='proyectos', null=True, on_delete=models.CASCADE)


# Clase Responsable: Define un responsable de proyecto
class Responsable(models.Model):
    nombre = models.CharField(max_length=250, null=True)

# Clase ResultadoExperimento: Define los posibles resultados de un Experimento
class ResultadoExperimento:
    ACTIVO = 0
    INACTIVO = 1
    RESULTADO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo')
    )
    EXITOSO = 0
    FALLIDO = 1
    CHOICES = (
        (EXITOSO, 'Exitoso'),
        (FALLIDO, 'Fallido')
    )

    def getDict(self):
        return [{'id': resultado[0], 'resultado': resultado[1]} for resultado in self.CHOICES]

    def getDictStates(self):
        return [{'id': resultado[0], 'estado': resultado[1]} for resultado in self.RESULTADO_CHOICES]


# Clase Experimento: Define un experimento dentro de un proyecto
class Experimento(models.Model):
    nombre = models.CharField(max_length=100, null=True)
    descripcion = models.CharField(max_length=1000, null=True)
    fechaInicio = models.DateField(null=True)
    prioridad = models.IntegerField(null=True)
    estado = models.IntegerField(choices=ResultadoExperimento.RESULTADO_CHOICES, null=True)
    resultado = models.IntegerField(choices=ResultadoExperimento.CHOICES, null=True)
    proyecto = models.ForeignKey(Proyecto, related_name='experimentos', null=True, on_delete=models.CASCADE)
    responsable = models.ForeignKey(Responsable, related_name='experimentos', null=True, on_delete=models.CASCADE)


# Clase CategoriaProtocolo: Define las posibles categorias de un Protocolo
class CategoriaProtocolo:
    HONGOS = 0
    BACTERIAS = 1
    ADN_EXTRACCION = 2
    PRUEBAS_BIOLOGICAS = 3
    CHOICES = (
        (HONGOS, 'Hongos'),
        (BACTERIAS, 'Bacterias'),
        (ADN_EXTRACCION, 'Extraccion ADN'),
        (PRUEBAS_BIOLOGICAS, 'Pruebas Biologicas'),
    )

    def getDict(self):
        return [{'id': categoria[0], 'estado': categoria[1]} for categoria in self.CHOICES]


# Clase Protocolo: Define los protocolos que pueden ir en un experimento
class Protocolo(models.Model):
    titulo = models.CharField(max_length=250, null=True)
    descripcion = models.CharField(max_length=1000, null=True)
    version = models.IntegerField(null=True)
    categoria = models.IntegerField(choices=CategoriaProtocolo.CHOICES, null=True)
    experimentos = models.ManyToManyField(Experimento, through='ProtocolosExperimento')


# Clase ProtocolosExperimento: Define los protocolos de un experimento
class ProtocolosExperimento(models.Model):
    protocolo = models.ForeignKey(Protocolo)
    experimento = models.ForeignKey(Experimento)


# Clase Paso: Define un paso de un protocolo
class Paso(models.Model):
    nombre = models.CharField(max_length=250, null=True)
    protocolo = models.ForeignKey(Protocolo, related_name='pasos', null=True, on_delete=models.CASCADE)


# Clase UnidadElemento: Define las posibles unidades de un Elemento
class UnidadElemento:
    CMS = 0
    GRAMOS = 1
    CM_CUBICO = 2
    UNIDADES = 3
    CHOICES = (
        (CMS, 'Centimetros'),
        (GRAMOS, 'Gramos'),
        (CM_CUBICO, 'Centimetros cubicos'),
        (UNIDADES, 'Unidades')
    )

    def getDict(self):
        return [{'id': unidad[0], 'estado': unidad[1]} for unidad in self.CHOICES]


# Clase Elemento: Define un elemento del laboratorio
class Elemento(models.Model):
    nombre = models.CharField(max_length=250, null=True)
    cantidad = models.FloatField(null=True)
    unidades = models.IntegerField(choices=UnidadElemento.CHOICES, null=True)
    paso = models.ForeignKey(Paso, related_name='elementos', null=True, on_delete=models.CASCADE)

