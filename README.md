# Lista de comandos

py -m venv venv (cria o ambiente)

source venv/Scripts/activate (ativa o ambiente)

pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] python-dotenv python-multipart alembic (instala todas as bibliotecas dentro do ambiente)

pip freeze > requirements.txt (copia as bibliotecas instaladas para o arquivo requirements.txt)

uvicorn main:app --reload = Rodar o projeto (criar um servidor usando uvicorn, executando o arquivo 'main', e em cada alteração feita, ele faz um reload)

alembic init alembic = cria diretorio alembic

alembic revision --autogenerate -m "mensagem" = Cria a migration do banco

alembic upgrade head = executa a migration


# Configurar alembic ( para migrations )
alembic.ini = alterar o valor de sqlalchemy.url colocando o endereço do meu banco

alembic -> env.py =  importa o sys e os :
import sys
import os
e poe esse caminho
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

e altera isso o target_metadata para isso: 
from models import Base
target_metadata = Base.metadata

# OBSERVAÇÕES
o bcrypt fica com erro, então ´preciso executar os comandos:

pip uninstall bcrypt
pip install bcrypt==4.0.1

# Anotações

 Se der erro na migration, deleta a migration que deu erro 
