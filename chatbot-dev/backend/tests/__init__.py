"""
Tests package for the hybrid chatbot system
"""

import os
import sys
from pathlib import Path

# Agregar el directorio padre al path para importar el módulo app
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Configuración de testing
os.environ['TESTING'] = 'true'
os.environ['DEBUG'] = 'false'
