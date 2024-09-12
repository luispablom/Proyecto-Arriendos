from functools import wraps # Para preservar los metadatos y la firma de la función original (view_func)
from django.shortcuts import get_object_or_404 # Para obtener el inmueble por su ID
from main.models import Inmueble
from django.contrib import messages
from django.shortcuts import redirect

# Test que solo pasan los no autentificados
def solo_no_autentificado(user):
    return not user.is_authenticated


# Test que solo pasan los arrendadores
def solo_arrendadores(user):
    return True if user.is_staff == True or user.userprofile.rol == 'arrendador' else False


# Verifica si el usuario es el propietario del inmueble.
def solo_propietario_staff(view_func): # Toma como argumento la vista que queremos decorar
    @wraps(view_func) # Detalles abajo
    def _wrapped_view(request, id, *args, **kwargs):
        inmueble = get_object_or_404(Inmueble, id=id) # Busca el inmueble por su ID. Si no existe, devuelve un error 404
        if request.user == inmueble.propietario or request.user.is_staff: # Verificación
            return view_func(request, id, *args, **kwargs) # Si es el propietario, se ejecuta la vista original (edit_propiedad) que fue decorada
        else:
            messages.error(request, f'No tienes permiso para editar la propiedad {id}')
            return redirect('profile')
    return _wrapped_view