from django.contrib import admin
from models import Patrocinador
from models import Proyecto
from models import Responsable
from models import Experimento
from models import Protocolo
from models import ProtocolosExperimento
from models import Paso
from models import Elemento


# Register your models here.
admin.site.register(Patrocinador)
admin.site.register(Proyecto)
admin.site.register(Responsable)
admin.site.register(Experimento)
admin.site.register(Protocolo)
admin.site.register(ProtocolosExperimento)
admin.site.register(Paso)
admin.site.register(Elemento)

