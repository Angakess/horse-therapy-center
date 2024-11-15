import random
from src.core.contacto import create_consulta
from core import (
    equipo,
    ecuestre,
    user,
    jya,
    situacionPrevisional,
    institucion,
    parienteTutor,
    trabajo,
    pago,
    cobro,
)
from core.user import Role, RolePermission, Permission
from datetime import datetime


def run():
    pago1 = pago.create_pago(
        monto=10000,
        fecha=datetime(2022, 1, 1),
        tipo="Honorario",
        desc="Primer pago de prueba",
    )
    pago2 = pago.create_pago(
        monto=20000,
        fecha=datetime(2022, 2, 2),
        tipo="Proveedor",
        desc="Segundo pago de prueba",
    )
    pago3 = pago.create_pago(
        monto=30000,
        fecha=datetime(2022, 3, 3),
        tipo="Gastos varios",
        desc="Tercer pago de prueba",
    )

    equipo1 = equipo.create_equipo(
        nombre="Juan",
        apellido="Pérez",
        dni=12345678,
        dir="Calle Falsa 123",
        email="juan.perez@example.com",
        localidad="Buenos Aires",
        tel="1234-5678",
        profesion="Psicólogo/a",
        puesto="Terapeuta",
        fecha_inicio=datetime.now(),
        contacto_emergencia_nombre="Ana Martínez",
        contacto_emergencia_tel="2345-6789",
        obra_social="Obra Social X",
        num_afiliado="11223344",
        condicion="Personal Rentado",
        activo=True,
    )
    equipo2 = equipo.create_equipo(
        nombre="María",
        apellido="Gómez",
        dni=87654321,
        dir="Av. Siempreviva 742",
        email="maria.gomez@example.com",
        localidad="Rosario",
        tel="2345-6789",
        profesion="Otro",
        puesto="Administrativo/a",
        fecha_inicio=datetime(2022, 5, 15),  # Fecha de inicio específica
        fecha_fin=None,  # El campo es opcional, así que se puede omitir
        contacto_emergencia_nombre="Juan García",
        contacto_emergencia_tel="1234-5678",
        obra_social="Obra Social Y",
        num_afiliado="33445566",
        condicion="Voluntario",
        activo=True,
    )
    equipo3 = equipo.create_equipo(
        nombre="Carlos",
        apellido="López",
        dni=34567890,
        dir="Calle Nueva 456",
        email="carlos.lopez@example.com",
        localidad="Córdoba",
        tel="9876-5432",
        profesion="Veterinario/a",
        puesto="Profesor de Equitación",
        fecha_inicio=datetime(2023, 1, 10),  # Fecha de inicio específica
        fecha_fin=datetime(2024, 12, 31),  # Fecha de fin específica
        contacto_emergencia_nombre="Pedro Rodríguez",
        contacto_emergencia_tel="3456-7890",
        obra_social="Obra Social Z",
        num_afiliado="77889900",
        condicion="Personal Rentado",
        activo=False,
    )
    ecuestre1 = ecuestre.create_ecuestre(
        nombre="Ecuestre 1",
        fecha_nacimiento=datetime(2004, 2, 20),
        sexo="Macho",
        raza="Warmblood Westfaliano",
        pelaje="Marron",
        tipo_adquisicion="Compra",
        fecha_ingreso=datetime(2006, 3, 15),
        sede_asignada="Club hipico",
    )
    ecuestre2 = ecuestre.create_ecuestre(
        nombre="Ecuestre 2",
        fecha_nacimiento=datetime(2008, 5, 14),
        sexo="Hembra",
        raza="Warmblood Oldenburgo",
        pelaje="Blanco",
        tipo_adquisicion="Donación",
        fecha_ingreso=datetime(2011, 9, 18),
        sede_asignada="Club hipico Jujuy",
    )
    jya1 = jya.create_jinetes_amazonas(
        nombre="jya1",
        apellido="Gonzalez",
        dni=44444441,
        edad=23,
        fecha_nacimiento=datetime(2001, 2, 23),
        lugar_nacimiento="La Plata, Buenos Aires",
        domicilio_actual="Calle 3, 111, La Plata, La Plata, Buenos Aires",
        telefono_actual="221221221",
        contacto_emergencia="911",
        tel="111222333",
        becado=True,
        porcentaje_beca=0.7,
        profesionales_atienden="Aaa, Bbb",
        certificado_discapacidad=True,
        asignacion_familiar=True,
        tipo_asignacion_familiar="Universal por hijo con discapacidad",
        beneficiario_pension=True,
        beneficiario_pension_tipo="Nacional",
        discapacidad="ECNE",
        tipo_discapacidad="Mental",
        tiene_deuda=False,
    )
    jya2 = jya.create_jinetes_amazonas(
        nombre="jya2",
        apellido="Ramirez",
        dni=44444442,
        edad=21,
        fecha_nacimiento=datetime(2003, 1, 30),
        lugar_nacimiento="Bahia Blanca, Buenos Aires",
        domicilio_actual="Calle Sarmiento, 111, Bahia Blanca, Bahia Blanca, Buenos Aires",
        telefono_actual="291221221",
        contacto_emergencia="911",
        tel="111222444",
        becado=True,
        porcentaje_beca=0.9,
        profesionales_atienden="Aaa, Bbb",
        certificado_discapacidad=False,
        asignacion_familiar=False,
        beneficiario_pension=False,
        tiene_deuda=True,
    )
    situacion_previsional1 = situacionPrevisional.create_situacion_previsional(
        obra_social="IOMA",
        nroafiliado=5643,
        curatela=False,
    )
    situacion_previsional2 = situacionPrevisional.create_situacion_previsional(
        obra_social="OSDE", nroafiliado=8231, curatela=True, observaciones="Hola"
    )
    institucion_escolar1 = institucion.create_institucion_escolar(
        nombre="Escuela 1",
        direccion="Calle 1 y 50",
        telefono="221345",
        grado_actual=4,
    )
    institucion_escolar2 = institucion.create_institucion_escolar(
        nombre="Escuela 2",
        direccion="Calle 2 y 50",
        telefono="221346",
        grado_actual=2,
        observaciones="Capo total",
    )
    pariente = parienteTutor.create_parentesco_tutor(
        parentesco="Padre",
        nombre="Alejandro",
        apellido="UNLP",
        dni=441,
        domicilio_actual="Calle 531",
        celular_actual="224214",
        email="ale@mail.com",
        nivel_escolaridad="Universitario",
        actividad_ocupacion="Abogado",
    )
    tutor = parienteTutor.create_parentesco_tutor(
        parentesco="Tutora",
        nombre="Alejandra",
        apellido="UNLP",
        dni=442,
        domicilio_actual="Calle 532",
        celular_actual="3214",
        email="ale2@mail.com",
        nivel_escolaridad="Universitario",
        actividad_ocupacion="Medica",
    )
    trabajo1 = trabajo.create_trabajo(
        propuestra_trabajo_institucional="Equitación",
        condicion="Regular",
        sede="CASJ",
        lunes=True,
        martes=False,
        miercoles=True,
        jueves=False,
        viernes=True,
        sabado=False,
        domingo=True,
    )
    trabajo2 = trabajo.create_trabajo(
        propuestra_trabajo_institucional="Actividades recreativas",
        condicion="De baja",
        sede="HLP",
        lunes=False,
        martes=True,
        miercoles=False,
        jueves=True,
        viernes=False,
        sabado=True,
        domingo=False,
    )
    #    VALID_ROLES = {"Técnica", "Ecuestre", "Voluntariado", "Administración"}

    role_admin = user.create_role(name="Administración")
    role_voluntario = user.create_role(name="Voluntariado")
    role_tec = user.create_role(name="Técnica")
    role_ec = user.create_role(name="Ecuestre")

    # superadmin
    user1 = user.create_user(
        alias="Admin",
        email="admin@example.com",
        password="adminpassword",
        role_id=role_admin.id,
        system_admin=True,
        enabled=True,
        inserted_at=datetime.now(),
    )

    user2 = user.create_user(
        alias="AnaVoluntaria",
        email="ana.voluntaria@example.com",
        password="voluntariopassword1",
        role_id=role_voluntario.id,
        system_admin=False,  # No es system admin
        enabled=True,
        inserted_at=datetime.now(),
    )

    # Crear segundo usuario voluntario
    user3 = user.create_user(
        alias="CarlosGomez",
        email="carlos.gomez@example.com",
        password="password2",
        role_id=role_tec.id,
        system_admin=False,  # No es system admin
        enabled=True,
        inserted_at=datetime.now(),
    )
    user4 = user.create_user(
        alias="MarcosZ",
        email="marcos.zapata@example.com",
        password="passwordMarcos",
        role_id=role_admin.id,
        system_admin=False,  # No es system admin
        enabled=True,
        inserted_at=datetime.now(),
    )
    user5 = user.create_user(
        alias="Rocky",
        email="ryland.grace@hailmary.com",
        password="astrofagos",
        role_id=role_ec.id,
        system_admin=False,  # No es system admin
        enabled=True,
        inserted_at=datetime.now(),
    )

    for i in range(1, 24):
        alias = f"Usuario{i}"
        email = f"usuario{i}@example.com"
        password = f"password{i}"

        # Asignar rol de manera aleatoria
        roles = [role_admin, role_voluntario, role_tec, role_ec]
        selected_role = random.choice(roles)

        # Asignar estado enabled aleatoriamente
        enabled_status = random.choice([True, False])

        # Crear usuario
        new_user = user.create_user(
            alias=alias,
            email=email,
            password=password,
            role_id=selected_role.id,
            system_admin=False,  # Ningún usuario es system admin
            enabled=enabled_status,
            inserted_at=datetime.now(),
        )

        # Asignar rol al usuario recién creado
        user.assign_role(new_user, selected_role)

        print(f"Usuario {alias} creado con rol {selected_role.name}")

    # Asignar rol de voluntariado al segundo usuario
    user.assign_role(user3, role_tec)
    user.assign_role(user2, role_voluntario)

    user.assign_role(user1, role_admin)  # super admin
    user.assign_role(user4, role_admin)  # admin normal
    user.assign_role(user5, role_ec)

    ecuestre.assing_equipo(ecuestre1, equipo1)
    ecuestre.assing_equipo(ecuestre1, equipo2)
    ecuestre.assing_equipo(ecuestre2, equipo2)
    ecuestre.assing_j_y_a(ecuestre1, jya1)
    ecuestre.assing_j_y_a(ecuestre2, jya2)

    jya.assing_situacion_previsional(jya1, situacion_previsional1)
    jya.assing_situacion_previsional(jya2, situacion_previsional2)
    jya.assing_institucion_escolar(jya1, institucion_escolar1)
    jya.assing_institucion_escolar(jya2, institucion_escolar2)
    jya.assing_parentesco_tutor(jya1, pariente)
    jya.assing_parentesco_tutor(jya2, tutor)

    trabajo.assing_profesor(trabajo1, equipo1)
    trabajo.assing_conductor(trabajo1, equipo2)
    trabajo.assing_caballo(trabajo1, ecuestre1)
    trabajo.assing_auxiliar_pista(trabajo1, equipo3)

    trabajo.assing_profesor(trabajo2, equipo2)
    trabajo.assing_conductor(trabajo2, equipo3)
    trabajo.assing_caballo(trabajo2, ecuestre2)
    trabajo.assing_auxiliar_pista(trabajo2, equipo1)

    jya.assing_trabajo(jya1, trabajo1)
    jya.assing_trabajo(jya2, trabajo2)

    pago.assign_pago(equipo1, pago1)

    todosLosPermisos = [
        "users_index",
        "users_activar_usuario",
        "users_edit_user",
        "users_delete_user_controller",
        "users_register_user",
        "equipo_index",
        "equipo_toggle_activate",
        "equipo_get_profile",
        "equipo_enter_edit",
        "equipo_save_edit",
        "equipo_enter_add",
        "equipo_add_equipo",
        "equipo_download_archivo",
        "equipo_delete",
        "jya_index",
        "jya_get_profile",
        "jya_enter_add",
        "jya_add_jya",
        "jya_delete",
        "jya_enter_edit",
        "jya_save_edit",
        "jya_download_archivo",
        "jya_str_to_bool",
        "jya_enter_docs",
        "jya_add_archivo",
        "jya_add_enlace",
        "jya_delete_archivo",
        "jya_delete_enlace",
        "ecuestre_index",
        "ecuestre_get_profile",
        "ecuestre_enter_edit",
        "ecuestre_save_edit",
        "ecuestre_enter_add",
        "ecuestre_add_ecuestre",
        "ecuestre_delete",
        "ecuestre_download_archivo",
        "ecuestre_enter_docs",
        "ecuestre_add_archivo",
        "ecuestre_add_enlace",
        "ecuestre_delete_archivo",
        "ecuestre_delete_enlace",
        "issues_index",
        "pago_index",
        "pago_get_info",
        "pago_enter_edit",
        "pago_save_edit",
        "pago_delete",
        "pago_enter_add",
        "pago_add",
        "cobro_index",
        "cobro_get_info",
        "cobro_enter_edit",
        "cobro_save_edit",
        "cobro_delete",
        "cobro_enter_add",
        "cobro_add",
        "cobro_set_endeudado",
        "contacto_index",
        "contacto_update",
        "contacto_destroy",
        "contacto_show"
    ]
    PERMISSIONS = {
        "Administración": [
            "equipo_index",
            "equipo_toggle_activate",
            "equipo_get_profile",
            "equipo_enter_edit",
            "equipo_save_edit",
            "equipo_enter_add",
            "equipo_add_equipo",
            "equipo_download_archivo",
            "equipo_delete",
            "jya_index",
            "jya_get_profile",
            "jya_enter_add",
            "jya_add_jya",
            "jya_delete",
            "jya_enter_edit",
            "jya_download_archivo",
            "jya_save_edit",
            "jya_enter_docs",
            "jya_add_archivo",
            "jya_add_enlace",
            "jya_delete_archivo",
            "jya_delete_enlace",
            "ecuestre_index",
            "ecuestre_get_profile",
            "ecuestre_enter_docs",
            "ecuestre_download_archivo",
            "issues_index",
            "pago_index",
            "pago_get_info",
            "pago_enter_edit",
            "pago_save_edit",
            "pago_delete",
            "pago_enter_add",
            "pago_add",
            "cobro_index",
            "cobro_get_info",
            "cobro_enter_edit",
            "cobro_save_edit",
            "cobro_delete",
            "cobro_enter_add",
            "cobro_add",
            "cobro_set_endeudado",
            "contacto_index",
            "contacto_update",
            "contacto_destroy",
            "contacto_show",
        ],
        "Voluntariado": [],
        "Técnica": [
            "jya_index",
            "jya_get_profile",
            "jya_enter_add",
            "jya_add_jya",
            "jya_delete",
            "jya_enter_edit",
            "jya_save_edit",
            "jya_download_archivo",
            "jya_enter_docs",
            "jya_add_archivo",
            "jya_add_enlace",
            "jya_delete_archivo",
            "jya_delete_enlace",
            "ecuestre_index",
            "ecuestre_get_profile",
            "ecuestre_enter_docs",
            "ecuestre_download_archivo",
            "cobro_index",
            "cobro_get_info",
        ],
        "Ecuestre": [
            "jya_index",
            "jya_get_profile",
            "jya_enter_docs",
            "jya_download_archivo",
            "ecuestre_index",
            "ecuestre_get_profile",
            "ecuestre_enter_edit",
            "ecuestre_save_edit",
            "ecuestre_enter_add",
            "ecuestre_add_ecuestre",
            "ecuestre_delete",
            "ecuestre_enter_docs",
            "ecuestre_add_archivo",
            "ecuestre_add_enlace",
            "ecuestre_delete_archivo",
            "ecuestre_delete_enlace",
            "ecuestre_download_archivo",
        ],
    }

    def find_permission_by_name(permiso):
        return Permission.query.filter_by(name=permiso).first()

    def find_role_by_name(rol):
        return Role.query.filter_by(name=rol).first()

    for per in todosLosPermisos:
        permission = user.create_permission(per)

    for rol in PERMISSIONS:
        for per in PERMISSIONS[rol]:
            user.assign_permission(
                (find_role_by_name(rol)).id, (find_permission_by_name(per)).id
            )

    medioDePago1 = cobro.create_medio_pago(name="Efectivo")
    medioDePago2 = cobro.create_medio_pago(name="Tarjeta de débito")
    medioDePago3 = cobro.create_medio_pago(name="Tarjeta de crédito")

    cobro1 = cobro.create_cobro(
        monto=100,
        fecha=datetime(2024, 3, 3),
        observaciones="Te observo 1",
        medio_pago=medioDePago1,
        jya=jya1,
        equipo=equipo1,
    )
    cobro2 = cobro.create_cobro(
        monto=2000,
        fecha=datetime(2021, 7, 3),
        observaciones="Te observo 2",
        medio_pago=medioDePago2,
        jya=jya2,
        equipo=equipo2,
    )
    cobro3 = cobro.create_cobro(
        monto=100132,
        fecha=datetime(2026, 3, 3),
        observaciones="Te observo 3",
        medio_pago=medioDePago3,
        jya=jya1,
        equipo=equipo3,
    )

    consulta1 = create_consulta(
        nya="Juan Perez",
        email="juan.perez@example.com",
        cuerpo="Consulta sobre sedes.",
        fecha=datetime(2024, 3, 3),
        estado="Pendiente",
        desc="Es una consulta general."
    )
    consulta2 = create_consulta(
        nya="Mario Vargas",
        email="mariovargas@example.com",
        cuerpo="Consulta sobre equitación.",
        fecha=datetime(2024, 6, 10),
        estado="Pendiente",
        desc="Es una consulta general."
    )
    consulta3 = create_consulta(
        nya="Carlos Lopez",
        email="carloslopez@example.com",
        cuerpo="Consulta sobre disponibilidad de cupos.",
        fecha=datetime(2024, 3, 5),
        estado="Resuelta",
        desc="Es una consulta general."
    )
    