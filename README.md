# sso-example-django-keycloak
A Single sign-on (SSO) example using Django and Keycloak

## Requirement

Python3, pipenv and docker.
I cheked by the following versions.

- Python 3.10.5
- pipenv, version 2022.6.7
- Docker version 20.10.16, build aa7e414

## Overview

- Demonstrates SSO between 2 Django web apps by using Keycloak as OpenID provider(OP).
- I used [Authlib](https://github.com/lepture/authlib) to write Relying Party(RP).
- This tool uses the following local ports.

| Name | Role | Port |
| ---- | ---- | ---- |
| Keycloak | OP | 8080 |
| app1 | RP | 8001 |
| app2 | RP | 8002 |

## Setup

### Keycloak
see [Keycloak's Getting started](https://www.keycloak.org/getting-started/getting-started-docker) for detail

1. Start keycloak container

```bash
docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:18.0.1 start-dev
```
2. Login to admin console

- http://localhost:8080/admin
- Username: admin
- Password: admin

3. Add realm

- Name: test

4. Add user

- Username: myuser
- Password: myuser

5. Add Client(app1)

- Client ID: app1
- Access Type: confidential
- Valid Redirect URIs: http://localhost:8001/oidc/login/
- Proof Key for Code Exchange Code Challenge Method: S256

6. Add Client(app2)

- Client ID: app2
- Access Type: confidential
- Valid Redirect URIs: http://localhost:8002/oidc/login/
- Proof Key for Code Exchange Code Challenge Method: S256

7. Note 'Secret' of app1 and app2

### Django

1. Clone code and install dependencies

```bash
git clone https://github.com/yazawa-takayuki/sso-example-django-keycloak.git
cd sso-example-django-keycloak
pipenv install
```

2. Set 'Secret' of app1 to project1/project1/settings.py

```python
OIDC_CLIENT_SECRET = 'set your secret'
```

3. Set 'Secret' of app2 to project2/project2/settings.py

4. Start app1

```bash
pipenv shell
cd project1
python manage.py migrate
python manage.py runserver 8001
```

5. Start app2

```bash
cd sso-example-django-keycloak
pipenv shell
export PYTHONPATH=`pwd`/project1
cd project2
python manage.py migrate
python manage.py runserver 8002
```

## Usage

1. Access to http://localhost:8001/app1 and login

- Username: myuser
- Password: myuser

2. Access to http://localhost:8002/app2 and **see being able to view the page without authentication**
