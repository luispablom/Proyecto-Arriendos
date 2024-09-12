from main.models import UserProfile, Inmueble, Comuna, Region
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.db import connection
from django.db.models import Q
from django.contrib import messages
from django.core.exceptions import ValidationError
from data.sinonimos import sinomimos 

def crear_inmueble(nombre:str, descripcion:str, m2_construidos:int, m2_totales:int, num_estacionamientos:int, num_habitaciones:int, num_baños:int, direccion:str, precio_mensual_arriendo:int, tipo_de_inmueble:str, comuna_cod:str, rut_propietario:str, imagen:object):
    comuna = Comuna.objects.get(cod=comuna_cod)
    propietario = User.objects.get(username=rut_propietario)
    Inmueble.objects.create(
        nombre = nombre,
        descripcion = descripcion,
        m2_construidos = m2_construidos,
        m2_totales = m2_totales,
        num_estacionamientos = num_estacionamientos,
        num_habitaciones = num_habitaciones,
        num_baños = num_baños,
        direccion = direccion,
        precio_mensual_arriendo = precio_mensual_arriendo,
        tipo_de_inmueble = tipo_de_inmueble,
        comuna = comuna,
        propietario = propietario,
        imagen = imagen
    )
    return True

def editar_inmueble(inmueble_id:int, nombre:str, descripcion:str, m2_construidos:int, m2_totales:int, num_estacionamientos:int, num_habitaciones:int, num_baños:int, direccion:str, precio_mensual_arriendo:int, tipo_de_inmueble:str, comuna:str, rut_propietario:str, imagen:object):
    inmueble = Inmueble.objects.get(id=inmueble_id)
    comuna = Comuna.objects.get(cod=comuna)
    propietario = User.objects.get(username=rut_propietario)
    inmueble.nombre = nombre
    inmueble.descripcion = descripcion
    inmueble.m2_construidos = m2_construidos
    inmueble.m2_totales = m2_totales
    inmueble.num_estacionamientos = num_estacionamientos
    inmueble.num_habitaciones = num_habitaciones
    inmueble.num_baños = num_baños
    inmueble.direccion = direccion
    inmueble.precio_mensual_arriendo = precio_mensual_arriendo
    inmueble.tipo_de_inmueble = tipo_de_inmueble
    inmueble.comuna = comuna
    inmueble.propietario = propietario
    inmueble.imagen = imagen
    inmueble.save()
    return True


def eliminar_inmueble(inmueble_id):
    Inmueble.objects.get(id=inmueble_id).delete()
    return True

def crear_user(request, username:str, first_name:str, last_name:str, email:str, password:str, pass_confirm:str, direccion:str, rol:str, telefono:str=None) -> bool:
    if password != pass_confirm:
        messages.error(request, 'Las contraseñas no coinciden')
        return False
    try:
        user = User.objects.create_user(
            username,
            email,
            password,
            first_name=first_name,
            last_name=last_name,
        )
    except IntegrityError:
        messages.error(request, 'El rut ya está ingresado')
        return False
    except ValidationError:
        messages.error(request, 'El email ya existe')
        return False
    UserProfile.objects.create(
        direccion=direccion,
        telefono_personal=telefono,
        rol = rol,
        user=user
    )
    messages.success(request, 'Usuario creado con éxito! Por favor, ingrese')
    return True

def editar_user(username:str, first_name:str, last_name:str, email:str, password:str, pass_confirm:str, direccion:str, telefono:str=None):
    # 1. Nos traemos el user y modificamos sus datos
    user = User.objects.get(username=username)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.set_password(password)
    user.save()
    # 2. Nos traemosel UserProfile y modificamos su datos
    user_profile = UserProfile.objects.get(user=user)
    user_profile.direccion = direccion
    user_profile.telefono_personal = telefono
    user_profile.save()

def editar_user_sin_password(username:str, first_name:str, last_name:str, email:str, direccion:str, rol:str, telefono:str=None):
    user = User.objects.get(username=username)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.save()
    user_profile = UserProfile.objects.get(user=user)
    user_profile.direccion = direccion
    user_profile.telefono_personal = telefono
    user_profile.rol = rol
    user_profile.save()

def eliminar_user(rut:str):
    eliminar = User.objects.get(username=rut)
    eliminar.delete()

def obtener_propiedades_comunas(filtro):
    if filtro is None:  
        return Inmueble.objects.all().order_by('comuna') # Entrega un objeto, al poner .value() entrega un diccionario
    # Si llegamos, hay un filtro
    return Inmueble.objects.filter(Q(nombre__icontains=filtro) | Q(descripcion__icontains=filtro) ).order_by('comuna')

def cambio_password(request, password:str, password_repeat:str):
    if password != password_repeat:
       messages.warning(request, 'Las Contraseñas no coinciden')
       return False
    request.user.set_password(password)
    request.user.save()
    messages.success(request, 'Contraseña actualizada con exito') 
    return True

