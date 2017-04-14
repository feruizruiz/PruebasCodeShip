import json

from rest_framework import status

from laboratorio.tests.serviciosREST.RESTTestCaseBase import RESTTestCaseTest


class UserTest(RESTTestCaseTest) :

    def verificar_campos(self, dict_respuesta, operacion, nombre_objeto):
        self.verificar_campo('username', dict_respuesta, operacion, nombre_objeto)
        self.verificar_campo('first_name', dict_respuesta, operacion, nombre_objeto)
        self.verificar_campo('last_name', dict_respuesta, operacion, nombre_objeto)
        self.verificar_campo('email', dict_respuesta, operacion, nombre_objeto)

    def probar_inicio_sesion(self):
        response = self.client.post('/laboratorio/iniciarSesion/', json.dumps(self.dict_base), content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Respuesta inicio sesion')
        self.assertEqual(data['mensaje'], 'ok', 'Respuesta creacion no es ok')

    def probar_esta_logueado(self):
        response = self.client.get('/laboratorio/estaLogueado/')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Respuesta esta logueado')
        self.assertNotEqual(data['mensaje'], 'no', 'Respuesta esta logueado es no')

    def probar_cerrar_sesion(self):
        response = self.client.get('/laboratorio/cerrarSesion/')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Respuesta cierre de sesion')
        self.assertEqual(data['mensaje'], 'ok', 'Respuesta cierre de sesion no es ok')

    def test_view_usuario(self):
        self.dict_base = {'username':'usuarioprueba', 'password': 'agiles123',
                          'first_name': 'Usuario Prueba', 'last_name': 'Prueba',
                          'email': 'usuarioprueba@hotmail.com'}
        self.campoModificar = 'first_name'
        self.valorCampoModificar = 'Usuario Prueba modificado'
        self.creado = False
        # Inicio crud
        self.probar_crear('usuario', 'usuarios')
        self.probar_obtener('usuario', 'usuarios')
        self.probar_obtener_lista('usuario', 'usuarios')
        # Login
        self.probar_inicio_sesion()
        self.probar_esta_logueado()
        self.probar_cerrar_sesion()
        # Continuar crud
        self.probar_actualizar('usuario', 'usuarios')
        self.probar_borrar('usuario', 'usuarios')

