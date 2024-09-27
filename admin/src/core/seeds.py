from core import board
from core import ecuestre
from datetime import datetime

def run():
    equipo1 = board.create_equipo(
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
    equipo2 = board.create_equipo(
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
    equipo3 = board.create_equipo(
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

    ecuestre.assing_equipo(ecuestre1,equipo1)
    ecuestre.assing_equipo(ecuestre2,equipo2)