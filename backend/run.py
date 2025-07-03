from app import create_app, db
from app.models.models import (
    LineaInvestigacion, Docente, Curso, PeriodoAcademico, 
    AsignacionDocente, ProduccionAcademica, DisponibilidadHoraria
)

app = create_app()

def create_tables():
    """Crear las tablas de la base de datos si no existen"""
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 