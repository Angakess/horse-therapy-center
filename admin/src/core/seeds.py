from core import equipo
from core import ecuestre
from core import user

from datetime import datetime
from core import jya

def run():
    equipo1 = equipo.create_equipo(
        nombre='Juan',
        apellido='Pérez',
        dni=12345678,
        dir='Calle Falsa 123',
        email='juan.perez@example.com',
        localidad='Buenos Aires',
        tel='1234-5678',
        profesion='Psicólogo/a',
        puesto='Terapeuta',
        fecha_inicio=datetime.now(),
        contacto_emergencia='Ana Martínez - 2345-6789',
        obra_social='Obra Social X',
        num_afiliado="11223344",
        condicion='Personal Rentado',
        activo=True
    )
    equipo2 = equipo.create_equipo(
        nombre='María',
        apellido='Gómez',
        dni=87654321,
        dir='Av. Siempreviva 742',
        email='maria.gomez@example.com',
        localidad='Rosario',
        tel='2345-6789',
        profesion='Otro',
        puesto='Administrativo/a',
        fecha_inicio=datetime(2022, 5, 15),  # Fecha de inicio específica
        fecha_fin=None,  # El campo es opcional, así que se puede omitir
        contacto_emergencia='Juan García - 1234-5678',
        obra_social='Obra Social Y',
        num_afiliado="33445566",
        condicion='Voluntario',
        activo=True
    )
    equipo3 = equipo.create_equipo(
        nombre='Carlos',
        apellido='López',
        dni=34567890,
        dir='Calle Nueva 456',
        email='carlos.lopez@example.com',
        localidad='Córdoba',
        tel='9876-5432',
        profesion='Veterinario/a',
        puesto='Profesor de Equitación',
        fecha_inicio=datetime(2023, 1, 10),  # Fecha de inicio específica
        fecha_fin=datetime(2024, 12, 31),  # Fecha de fin específica
        contacto_emergencia='Pedro Rodríguez - 3456-7890',
        obra_social='Obra Social Z',
        num_afiliado="77889900",
        condicion='Personal Rentado',
        activo=False
    )
    """ ecuestre1 = ecuestre.create_ecuestre(
        nombre = 'Ecuestre 1',
        fecha_nacimiento = datetime(2004,2,20),
        sexo = 'Macho',
        raza = 'Warmblood Westfaliano',
        pelaje = 'Marron',
        sede_asignada = 'Club hipico'
    )
    ecuestre2 = ecuestre.create_ecuestre(
        nombre = 'Ecuestre 2',
        fecha_nacimiento = datetime(2008,5,14),
        sexo = 'Hembra',
        raza = 'Warmblood Oldenburgo',
        pelaje = 'Blanco',
        sede_asignada = 'Club hipico Jujuy'
    )
    jya1 = jya.create_jinetes_amazonas(
        nombre = 'jya1',
        apellido = 'Gonzalez',
        dni = 44444441,
        edad = 23,
        fecha_nacimiento = datetime(2001,2,23),
        lugar_nacimiento = 'La Plata, Buenos Aires',
        domicilio_actual = 'Calle 3, 111, La Plata, La Plata, Buenos Aires',
        telefono_actual = '221221221',
        contacto_emergencia = '911',
        tel = '111222333',
        becado = True,
        porcentaje_beca = 0.7,
        profesionales_atienden = 'Aaa, Bbb'   
    )
    jya2 = jya.create_jinetes_amazonas(
        nombre = 'jya2',
        apellido = 'Ramirez',
        dni = 44444442,
        edad = 21,
        fecha_nacimiento = datetime(2003,1,30),
        lugar_nacimiento = 'Bahia Blanca, Buenos Aires',
        domicilio_actual = 'Calle Sarmiento, 111, Bahia Blanca, Bahia Blanca, Buenos Aires',
        telefono_actual = '291221221',
        contacto_emergencia = '911',
        tel = '111222444',
        becado = True,
        porcentaje_beca = 0.9,
        profesionales_atienden = 'Aaa, Bbb'   
    )"""

    #    VALID_ROLES = {"Técnica", "Ecuestre", "Voluntariado", "Administración"}

    role_admin = user.create_role(name="Administración")
    role_voluntario = user.create_role(name="Voluntariado")
    role_tec = user.create_role(name="Técnica")
    role_ec = user.create_role(name="Ecuestre")

    #superadmin
    user1 = user.create_user(
        alias='Admin',
        email='admin@example.com',
        password='adminpassword',
        role_id=role_admin.id,
        system_admin=True,
        enabled=True,
        inserted_at=datetime.now()
    )

    user2 = user.create_user(
    alias='AnaVoluntaria',
    email='ana.voluntaria@example.com',
    password='voluntariopassword1',
    role_id=role_voluntario.id,
    system_admin=False,  # No es system admin
    enabled=True,
    inserted_at=datetime.now()
)

    

    # Crear segundo usuario voluntario
    user3 = user.create_user(
        alias='CarlosGomez',
        email='carlos.gomez@example.com',
        password='password2',
        role_id=role_tec.id,
        system_admin=False,  # No es system admin
        enabled=True,
        inserted_at=datetime.now()
    )

    #Asignar rol de voluntariado al segundo usuario
    user.assign_role(user3, role_tec)
    user.assign_role(user2, role_voluntario)

    user.assign_role(user1, role_admin)

    """
    ecuestre.assing_equipo(ecuestre1,equipo1)
    ecuestre.assing_equipo(ecuestre2,equipo2)
    ecuestre.assing_j_y_a(ecuestre1,jya1)
    ecuestre.assing_j_y_a(ecuestre2,jya2)


    """""