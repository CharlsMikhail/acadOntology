#!/usr/bin/env python3
"""
Script para inicializar la base de datos con datos de ejemplo
"""

from app import create_app, db
from app.models.models import (
    LineaInvestigacion, Docente, Curso, PeriodoAcademico, 
    AsignacionDocente, ProduccionAcademica, DisponibilidadHoraria
)
from datetime import date, time

def init_database():
    """Inicializar la base de datos con datos de ejemplo"""
    app = create_app()
    
    with app.app_context():
        # Crear tablas
        db.create_all()
        
        print("Creando líneas de investigación...")
        
        # Crear líneas de investigación
        lineas = [
            LineaInvestigacion(nombre="Inteligencia Artificial"),
            LineaInvestigacion(nombre="Machine Learning"),
            LineaInvestigacion(nombre="Sistemas Distribuidos"),
            LineaInvestigacion(nombre="Ingeniería de Software"),
            LineaInvestigacion(nombre="Ciberseguridad")
        ]
        
        for linea in lineas:
            db.session.add(linea)
        db.session.commit()
        
        print("Creando docentes...")
        
        # Crear docentes
        docentes = [
            Docente(
                nombre="Dr. Juan Pérez",
                grado_academico="Doctorado en Ciencias de la Computación",
                orcid="0000-0001-2345-6789",
                correo="juan.perez@universidad.edu",
                linea_investigacion_id=1
            ),
            Docente(
                nombre="Dra. María García",
                grado_academico="Doctorado en Inteligencia Artificial",
                orcid="0000-0002-3456-7890",
                correo="maria.garcia@universidad.edu",
                linea_investigacion_id=2
            ),
            Docente(
                nombre="Dr. Carlos López",
                grado_academico="Doctorado en Sistemas Distribuidos",
                orcid="0000-0003-4567-8901",
                correo="carlos.lopez@universidad.edu",
                linea_investigacion_id=3
            ),
            Docente(
                nombre="Dra. Ana Rodríguez",
                grado_academico="Doctorado en Ingeniería de Software",
                orcid="0000-0004-5678-9012",
                correo="ana.rodriguez@universidad.edu",
                linea_investigacion_id=4
            ),
            Docente(
                nombre="Dr. Luis Martínez",
                grado_academico="Doctorado en Ciberseguridad",
                orcid="0000-0005-6789-0123",
                correo="luis.martinez@universidad.edu",
                linea_investigacion_id=5
            )
        ]
        
        for docente in docentes:
            db.session.add(docente)
        db.session.commit()
        
        print("Creando cursos...")
        
        # Crear cursos
        cursos = [
            Curso(nombre="Introducción a la Inteligencia Artificial", linea_investigacion_id=1),
            Curso(nombre="Machine Learning Avanzado", linea_investigacion_id=2),
            Curso(nombre="Sistemas Distribuidos", linea_investigacion_id=3),
            Curso(nombre="Ingeniería de Software", linea_investigacion_id=4),
            Curso(nombre="Ciberseguridad Aplicada", linea_investigacion_id=5),
            Curso(nombre="Redes Neuronales", linea_investigacion_id=1),
            Curso(nombre="Deep Learning", linea_investigacion_id=2),
            Curso(nombre="Computación en la Nube", linea_investigacion_id=3),
            Curso(nombre="Arquitectura de Software", linea_investigacion_id=4),
            Curso(nombre="Criptografía", linea_investigacion_id=5)
        ]
        
        for curso in cursos:
            db.session.add(curso)
        db.session.commit()
        
        print("Creando períodos académicos...")
        
        # Crear períodos académicos
        periodos = [
            PeriodoAcademico(
                nombre="2025-I",
                fecha_inicio=date(2025, 1, 15),
                fecha_fin=date(2025, 5, 30)
            ),
            PeriodoAcademico(
                nombre="2025-II",
                fecha_inicio=date(2025, 8, 15),
                fecha_fin=date(2025, 12, 30)
            )
        ]
        
        for periodo in periodos:
            db.session.add(periodo)
        db.session.commit()
        
        print("Creando asignaciones de docentes...")
        
        # Crear asignaciones de docentes
        asignaciones = [
            AsignacionDocente(docente_id=1, curso_id=1, periodo_id=1, horas_asignadas=4),
            AsignacionDocente(docente_id=1, curso_id=6, periodo_id=1, horas_asignadas=3),
            AsignacionDocente(docente_id=2, curso_id=2, periodo_id=1, horas_asignadas=4),
            AsignacionDocente(docente_id=2, curso_id=7, periodo_id=1, horas_asignadas=3),
            AsignacionDocente(docente_id=3, curso_id=3, periodo_id=1, horas_asignadas=4),
            AsignacionDocente(docente_id=3, curso_id=8, periodo_id=1, horas_asignadas=3),
            AsignacionDocente(docente_id=4, curso_id=4, periodo_id=1, horas_asignadas=4),
            AsignacionDocente(docente_id=4, curso_id=9, periodo_id=1, horas_asignadas=3),
            AsignacionDocente(docente_id=5, curso_id=5, periodo_id=1, horas_asignadas=4),
            AsignacionDocente(docente_id=5, curso_id=10, periodo_id=1, horas_asignadas=3)
        ]
        
        for asignacion in asignaciones:
            db.session.add(asignacion)
        db.session.commit()
        
        print("Creando producción académica...")
        
        # Crear producción académica
        producciones = [
            ProduccionAcademica(
                docente_id=1,
                tipo="Artículo",
                titulo="Aplicación de Redes Neuronales en el Reconocimiento de Patrones",
                anio=2024,
                revista="Journal of Artificial Intelligence",
                doi="10.1000/ai.2024.001",
                enlace="https://doi.org/10.1000/ai.2024.001"
            ),
            ProduccionAcademica(
                docente_id=2,
                tipo="Artículo",
                titulo="Algoritmos de Machine Learning para Predicción de Datos",
                anio=2024,
                revista="Machine Learning Quarterly",
                doi="10.1000/ml.2024.002",
                enlace="https://doi.org/10.1000/ml.2024.002"
            ),
            ProduccionAcademica(
                docente_id=3,
                tipo="Libro",
                titulo="Sistemas Distribuidos: Teoría y Práctica",
                anio=2023,
                revista="Editorial Universitaria",
                doi="10.1000/book.2023.001",
                enlace="https://doi.org/10.1000/book.2023.001"
            ),
            ProduccionAcademica(
                docente_id=4,
                tipo="Ponencia",
                titulo="Metodologías Ágiles en el Desarrollo de Software",
                anio=2024,
                revista="Conferencia Internacional de Ingeniería de Software",
                doi="10.1000/conf.2024.001",
                enlace="https://doi.org/10.1000/conf.2024.001"
            ),
            ProduccionAcademica(
                docente_id=5,
                tipo="Artículo",
                titulo="Nuevas Técnicas de Criptografía para la Seguridad Informática",
                anio=2024,
                revista="Journal of Cybersecurity",
                doi="10.1000/cyber.2024.001",
                enlace="https://doi.org/10.1000/cyber.2024.001"
            )
        ]
        
        for produccion in producciones:
            db.session.add(produccion)
        db.session.commit()
        
        print("Creando disponibilidad horaria...")
        
        # Crear disponibilidad horaria
        disponibilidades = [
            DisponibilidadHoraria(
                docente_id=1,
                dia_semana="Lunes",
                hora_inicio=time(8, 0),
                hora_fin=time(12, 0)
            ),
            DisponibilidadHoraria(
                docente_id=1,
                dia_semana="Martes",
                hora_inicio=time(14, 0),
                hora_fin=time(18, 0)
            ),
            DisponibilidadHoraria(
                docente_id=2,
                dia_semana="Miércoles",
                hora_inicio=time(8, 0),
                hora_fin=time(12, 0)
            ),
            DisponibilidadHoraria(
                docente_id=2,
                dia_semana="Jueves",
                hora_inicio=time(14, 0),
                hora_fin=time(18, 0)
            ),
            DisponibilidadHoraria(
                docente_id=3,
                dia_semana="Viernes",
                hora_inicio=time(8, 0),
                hora_fin=time(12, 0)
            ),
            DisponibilidadHoraria(
                docente_id=4,
                dia_semana="Lunes",
                hora_inicio=time(14, 0),
                hora_fin=time(18, 0)
            ),
            DisponibilidadHoraria(
                docente_id=5,
                dia_semana="Martes",
                hora_inicio=time(8, 0),
                hora_fin=time(12, 0)
            )
        ]
        
        for disponibilidad in disponibilidades:
            db.session.add(disponibilidad)
        db.session.commit()
        
        print("¡Base de datos inicializada exitosamente!")
        print("\nDatos creados:")
        print(f"- {len(lineas)} líneas de investigación")
        print(f"- {len(docentes)} docentes")
        print(f"- {len(cursos)} cursos")
        print(f"- {len(periodos)} períodos académicos")
        print(f"- {len(asignaciones)} asignaciones de docentes")
        print(f"- {len(producciones)} producciones académicas")
        print(f"- {len(disponibilidades)} disponibilidades horarias")

if __name__ == '__main__':
    init_database() 