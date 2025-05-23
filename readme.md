## 🔧 Instalación del entorno backend (Flask)

Crear un entorno virtual:

```bash
python3 -m venv venv

source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate     # En Windows

pip install flask

pip install flask-cors python-dotenv

pip install -r requirements.txt

para agregar las instalaciones: pip freeze > requirements.txt