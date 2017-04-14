import json

from rest_framework import status
from rest_framework.test import APITestCase


class PatrocinadorTest(APITestCase) :

    def verificar_campos(self, dict_respuesta, operacion, nombre_objeto):
        self.assertEqual(dict_respuesta['pk'], self.dict_base['id'], 'Comparacion llave ' + operacion + ' ' + nombre_objeto)
        dict_fields = dict_respuesta['fields']
        for key, value in dict_fields.iteritems():
            self.assertEqual(dict_fields[key], self.dict_base[key], 'Comparacion ' + operacion + ' ' + nombre_objeto + ' campo ' + key)

    def crear_objeto(self, singular, plural):
        response = self.client.post('/laboratorio/' + plural + '/', json.dumps(self.dict_base), content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Respuesta creacion ' + singular)
        self.verificar_campos(data[0], 'creacion', singular)
        self.creado = True

    def probar_crear_patrocinador(self, singular, plural):
        self.crear_objeto(singular, plural)

    def probar_obtener_patrocinador(self, singular, plural):
        if not self.creado:
            self.crear_objeto(singular, plural)
        response = self.client.get('/laboratorio/' + plural + '/%s/' % self.dict_base['id'])
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Respuesta obtencion ' + singular)
        self.verificar_campos(data[0], 'obtencion', singular)

    def probar_obtener_patrocinadores(self, singular, plural):
        if not self.creado:
            self.crear_objeto(singular, plural)
        response = self.client.get('/laboratorio/' + plural + '/%s/' % self.dict_base['id'])
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Respuesta obtencion ' + singular)
        self.assertEqual(len(data), 1, 'Cantidad obtencion ' + plural)

    def probar_actualizar_patrocinador(self, singular, plural):
        if not self.creado:
            self.crear_objeto(singular, plural)
        self.dict_base['nombre'] = 'patrocinador ' + ' Modificado'
        response = self.client.put('/laboratorio/' + plural + '/%s/' % self.dict_base['id'], json.dumps(self.dict_base), content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Respuesta actualizacion ' + singular)
        self.verificar_campos(data[0], 'actualizacion', singular)

    def probar_borrar_patrocinador(self, singular, plural):
        if not self.creado:
            self.crear_objeto(singular, plural)
        response = self.client.delete('/laboratorio/' + plural + '/%s/' % self.dict_base['id'])
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Respuesta borrado ' + singular)

    def probar_crud(self, singular, plural):
        self.probar_crear_patrocinador(singular, plural)
        self.probar_obtener_patrocinador(singular, plural)
        self.probar_obtener_patrocinadores(singular, plural)
        self.probar_actualizar_patrocinador(singular, plural)
        self.probar_borrar_patrocinador(singular, plural)

    def test_views(self):
        self.dict_base = {'id': 9999, 'nombre': 'Patrocinador de Prueba'}
        self.creado = False
        self.probar_crud('patrocinador', 'patrocinadores')
