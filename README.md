# Test Fintech - Django (SQLite / PostgreSQL Docker)

Projet backend Django avec support de deux bases de données :
- SQLite (par défaut, simple et immédiat)
- PostgreSQL (via Docker pour environnement proche production)

---

## Stack technique

- Python 3.12+
- Django
- Django REST Framework (si utilisé)
- SQLite (par défaut Django)
- PostgreSQL 15 (Docker optionnel)
- psycopg2 / psycopg
- Docker & Docker Compose

---

## Prérequis

Avant de commencer :

- Python 3.12 installé
- Docker Desktop installé (si utilisation PostgreSQL)
- Vérifier Docker :

```bash
docker --version
docker compose version
```

---

### MODE 1 : SQLITE (par défaut, recommandé pour démarrer)

Django utilise SQLite automatiquement si aucune config PostgreSQL n’est définie.

###### Lancer le projet
1. Créer l’environnement virtuel
```bash
py -3.12 -m venv .venv
.venv\Scripts\activate
```

2. Installer les dépendances
```bash
pip install -r requirements.txt
```

ou :

pip install django djangorestframework
3. Migrer la base SQLite
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Lancer le serveur
```bash
python manage.py runserver
```
Accès : http://127.0.0.1:8000

---

### MODE 2 : POSTGRESQL (Docker)

Utilisé pour simuler un environnement production. Créer le fichier docker-compose.yml, à la racine du projet. 

###### docker-compose.yml
```bash
services:
  db:
    image: postgres:15
    container_name: fintech_postgres
    restart: always
    environment:
      POSTGRES_DB: fintech
      POSTGRES_USER: fintech_user
      POSTGRES_PASSWORD: fintech_pass
      LANG: C.UTF-8
      LC_ALL: C.UTF-8
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

###### Lancer PostgreSQL
```bash
docker compose up -d
```

###### Lancer PostgreSQL
```bash
docker ps
```

###### Configuration Django (PostgreSQL)

Dans `settings.py`
```bash
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "fintech",
        "USER": "fintech_user",
        "PASSWORD": "fintech_pass",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

###### Migration PostgreSQL
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### IMPORTANT : différences SQLite vs PostgreSQL
| Mode       | Base utilisée            | Avantage            |
| ---------- | ------------------------ | ------------------- |
| SQLite     | local fichier db.sqlite3 | rapide, zéro config |
| PostgreSQL | Docker container         | proche production   |

**Remarque: Il peut souvent y avoir des problèmes liés à l'installation de postgres avec docker, dans ce cas, il est souvent bon de faire un reset complet, et recommencer les étapes au cas où**

--- 

## Documentation API

La documentation interactive de l'API est disponible via Swagger une fois le serveur Django lancé.

### Swagger UI

```text
http://127.0.0.1:8000/api/docs/
```

### Schéma OpenAPI

```text
http://127.0.0.1:8000/api/schema/
```

--- 

## Test avec insomnia (équivalent de Postman)

**Il y a une variable d'environnement dont la valeur est la suivante: `http://127.0.0.1:8000/api/`**