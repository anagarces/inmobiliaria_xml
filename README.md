# inmobiliaria_xml

Entorno de desarrollo de **Odoo 19** con **PostgreSQL 16** sobre Docker.

## Requisitos

- Docker Engine + Docker Compose v2 (`docker compose version`)

## Estructura

```
.
├── docker-compose.yml          Servicios: odoo (19.0) + db (postgres:16)
├── .env.example                Plantilla de credenciales -> copiar a .env
├── .env                        Credenciales locales (IGNORADO por git)
├── config/
│   ├── odoo.conf.example       Plantilla de config de Odoo
│   └── odoo.conf               Config local con secretos (IGNORADO por git)
└── addons/                     Modulos personalizados -> /mnt/extra-addons
```

## Puesta en marcha

```bash
# 1. Clonar y entrar
git clone <url-del-repo> inmobiliaria_xml
cd inmobiliaria_xml

# 2. Crear los archivos locales a partir de las plantillas
cp .env.example .env
cp config/odoo.conf.example config/odoo.conf

# 3. Editar .env y config/odoo.conf con contrasenas propias.
#    IMPORTANTE: db_password (odoo.conf) debe coincidir con
#    POSTGRES_PASSWORD (.env), y admin_passwd con ODOO_MASTER_PASSWORD.

# 4. Levantar
docker compose up -d

# 5. Ver logs
docker compose logs -f odoo
```

Odoo queda disponible en http://localhost:8069
(en el primer arranque crea la base de datos desde el asistente web;
la contrasena maestra es `ODOO_MASTER_PASSWORD` / `admin_passwd`).

## Comandos utiles

```bash
docker compose stop                 # parar sin borrar
docker compose down                 # parar y eliminar contenedores
docker compose down -v              # + borrar volumenes (DATOS!)
docker compose restart odoo
docker compose exec odoo odoo shell -d <db>   # shell de Odoo
docker compose exec db psql -U odoo postgres  # consola psql
```

### Instalar / actualizar un modulo

```bash
docker compose exec odoo odoo -d <db> -i nombre_modulo --stop-after-init
docker compose exec odoo odoo -d <db> -u nombre_modulo --stop-after-init
```

### Copia de seguridad

```bash
docker compose exec db pg_dump -U odoo -Fc <db> > backups/<db>_$(date +%F).dump
```

## Seguridad y credenciales

- `.env` y `config/odoo.conf` **contienen secretos y estan en `.gitignore`**.
  Nunca se suben al repositorio.
- Solo se versionan las plantillas `*.example` con valores de marcador.
- Antes del primer `git push`, verifica que no hay secretos rastreados:

  ```bash
  git status --ignored
  git ls-files | grep -E '(\.env$|odoo\.conf$)'   # no debe devolver nada
  ```

- Para produccion: usa contrasenas largas y unicas, pon `list_db = False`,
  `proxy_mode = True` tras un reverse proxy con HTTPS, y ajusta `workers`.

## Publicar en GitHub

```bash
git init
git add .
git commit -m "Scaffold inicial: Odoo 19 + Postgres 16 en Docker"
git branch -M main
git remote add origin git@github.com:<usuario>/inmobiliaria_xml.git
git push -u origin main
```
