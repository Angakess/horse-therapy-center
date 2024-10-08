from core import equipo
from core import ecuestre
from core import user
from core import jya
from core.jya import situacion_previsional
from core.jya import institucion_escolar
from core.jya import pariente_tutor
from core.jya import trabajo

from datetime import datetime

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
    ecuestre1 = ecuestre.create_ecuestre(
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
        profesionales_atienden = 'Aaa, Bbb',
        certificado_discapacidad = True,
        asignacion_familiar = True,
        tipo_asignacion_familiar = 'Universal por hijo con discapacidad',
        beneficiario_pension = True,
        beneficiario_pension_tipo = 'Nacional',
        discapacidad = 'ECNE',
        tipo_discapacidad = 'Mental',
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
        profesionales_atienden = 'Aaa, Bbb',
        certificado_discapacidad = False,
        asignacion_familiar = False,
        beneficiario_pension = False,
    )
    situacion_previsional1 = situacion_previsional.create_situacion_previsional(
        obra_social = 'IOMA',
        nroafiliado = 5643,
        curatela = False,
    )
    situacion_previsional2 = situacion_previsional.create_situacion_previsional(
        obra_social = 'OSDE',
        nroafiliado = 8231,
        curatela = True,
        observaciones = 'Hola'
    )
    institucion_escolar1 = institucion_escolar.create_institucion_escolar(
        nombre = 'Escuela 1',
        direccion = 'Calle 1 y 50',
        telefono = '221345',
        grado_actual = 4,
    )
    institucion_escolar2 = institucion_escolar.create_institucion_escolar(
        nombre = 'Escuela 2',
        direccion = 'Calle 2 y 50',
        telefono = '221346',
        grado_actual = 2,
        observaciones = 'Capo total',
    )
    pariente = pariente_tutor.create_parentesco_tutor(
        parentesco = 'Padre',
        nombre = 'Alejandro',
        apellido = 'UNLP',
        dni = 441,
        domicilio_actual = 'Calle 531',
        celular_actual = '224214',
        email = 'ale@mail.com',
        nivel_escolaridad = 'Universitario',
        actividad_ocupacion = 'Abogado',
    )
    tutor = pariente_tutor.create_parentesco_tutor(
        parentesco = 'Tutora',
        nombre = 'Alejandra',
        apellido = 'UNLP',
        dni = 442,
        domicilio_actual = 'Calle 532',
        celular_actual = '3214',
        email = 'ale2@mail.com',
        nivel_escolaridad = 'Universitario',
        actividad_ocupacion = 'Medica',
    )
    trabajo1 = trabajo.create_trabajo(
        propuestra_trabajo_institucional = 'Equitacion',
        condicion = 'Regular',
        sede = 'CASJ',
        dia = 'Domingo',
    )
    trabajo2 = trabajo.create_trabajo(
        propuestra_trabajo_institucional = 'Actividades recreativas',
        condicion = 'De baja',
        sede = 'HLP',
        dia = 'Jueves',
    )

    role_admin = user.create_role(name="Administración")
    role_user = user.create_role(name="User")

    user1 = user.create_user(
        alias='JuanAdmin',
        email='juan.admin@example.com',
        password='adminpassword',
        role_id=role_admin.id,
        system_admin=True,
        enabled=True,
        inserted_at=datetime.now()
    )

    #Prueba de que funciona mail único
    user2 = user.create_user(
        alias='MariaUser',
        email='juan.admin@example.com',
        password='userpassword',
        role_id=role_user.id,
        system_admin=False,
        enabled=True,
        inserted_at=datetime.now()
    )

    user.assign_role(user1, role_admin)
    user.assign_role(user2,role_user)

    ecuestre.assing_equipo(ecuestre1,equipo1)
    ecuestre.assing_equipo(ecuestre2,equipo2)
    ecuestre.assing_j_y_a(ecuestre1,jya1)
    ecuestre.assing_j_y_a(ecuestre2,jya2)

    jya.assing_situacion_previsional(jya1,situacion_previsional1)
    jya.assing_situacion_previsional(jya2,situacion_previsional2)
    jya.assing_institucion_escolar(jya1,institucion_escolar1)
    jya.assing_institucion_escolar(jya2,institucion_escolar2)
    jya.assing_parentesco_tutor(jya1,pariente)
    jya.assing_parentesco_tutor(jya2,tutor)

    trabajo.assing_profesor(trabajo1,equipo1)
    trabajo.assing_conductor(trabajo1,equipo2)
    trabajo.assing_caballo(trabajo1,ecuestre1)
    trabajo.assing_auxiliar_pista(trabajo1,equipo3)

    trabajo.assing_profesor(trabajo2,equipo2)
    trabajo.assing_conductor(trabajo2,equipo3)
    trabajo.assing_caballo(trabajo2,ecuestre2)
    trabajo.assing_auxiliar_pista(trabajo2,equipo1)

    jya.assing_trabajo(jya1,trabajo1)
    jya.assing_trabajo(jya2,trabajo2)
