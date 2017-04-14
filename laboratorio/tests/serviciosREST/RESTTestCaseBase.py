import json

from rest_framework import status
from rest_framework.test import APITestCase


class RESTTestCaseTest(APITestCase) :

    def verificar_campo(self, key, dict_respuesta, operacion, nombre_objeto):
        self.assertEqual(dict_respuesta[key], self.dict_base[key], 'Comparacion ' + operacion + ' ' + nombre_objeto + ' campo ' + key)

    def verificar_campos(self, dict_respuesta, operacion, nombre_objeto):
        for key, value in dict_respuesta.iteritems():
            self.verificar_campo(self, key, dict_respuesta, operacion, nombre_objeto)

    def crear_objeto(self, singular, plural):
        response = self.client.post('/laboratorio/' + plural + '/', json.dumps(self.dict_base), content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Respuesta creacion ' + singular)
        self.verificar_campos(data, 'creacion', singular)
        self.creado = True
        if data.has_key('id'):
            self.dict_base['id'] = data['id']

    def probar_crear(self, singular, plural):
        self.crear_objeto(singular, plural)

    def probar_obtener(self, singular, plural):
        if not self.creado:
            self.crear_objeto(singular, plural)
        response = self.client.get('/laboratorio/' + plural + '/%s/' % self.dict_base['id'])
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Respuesta obtencion ' + singular)
        self.verificar_campos(data, 'obtencion', singular)

    def probar_obtener_lista(self, singular, plural):
        if not self.creado:
            self.crear_objeto(singular, plural)
        response = self.client.get('/laboratorio/' + plural + '/')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Respuesta obtencion ' + singular)
        self.assertEqual(len(data), 1, 'Cantidad obtencion ' + plural)

    def probar_actualizar(self, singular, plural):
        if not self.creado:
            self.crear_objeto(singular, plural)
        self.dict_base[self.campoModificar] = self.valorCampoModificar
        response = self.client.put('/laboratorio/' + plural + '/%s/' % self.dict_base['id'], json.dumps(self.dict_base), content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Respuesta actualizacion ' + singular)
        self.verificar_campos(data, 'actualizacion', singular)

    def probar_borrar(self, singular, plural):
        if not self.creado:
            self.crear_objeto(singular, plural)
        response = self.client.delete('/laboratorio/' + plural + '/%s/' % self.dict_base['id'])
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Respuesta borrado ' + singular)

    def probar_crud(self, singular, plural):
        self.probar_crear(singular, plural)
        self.probar_obtener(singular, plural)
        self.probar_obtener_lista(singular, plural)
        self.probar_actualizar(singular, plural)
        self.probar_borrar(singular, plural)
