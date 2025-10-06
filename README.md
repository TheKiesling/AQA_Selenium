# Sistema de Login con CI/CD y Tests Automatizados

Sistema completo de autenticación con frontend en React, backend en Node.js, tests automatizados con Selenium y pipeline de CI/CD con GitHub Actions.

## 📋 Características

- ✅ **Frontend en React** con diseño moderno y responsivo
- ✅ **Backend en Node.js** con Express y JWT
- ✅ **Tests automatizados** con Selenium y Pytest
- ✅ **CI/CD Pipeline** con GitHub Actions
- ✅ **Docker & Docker Compose** para despliegue fácil
- ✅ **Detección de errores** que previene avance a siguientes entornos

## 🏗️ Estructura del Proyecto

```
AQA_Selenium/
├── backend/                 # Backend Node.js
│   ├── server.js           # Servidor Express con API de login
│   ├── package.json        # Dependencias del backend
│   ├── Dockerfile          # Imagen Docker del backend
│   └── .env                # Variables de entorno
├── frontend/               # Frontend React
│   ├── src/
│   │   ├── App.js         # Componente principal con formulario
│   │   ├── App.css        # Estilos modernos
│   │   └── index.js       # Punto de entrada
│   ├── public/
│   │   └── index.html     # HTML base
│   ├── package.json       # Dependencias del frontend
│   ├── Dockerfile         # Imagen Docker del frontend
│   └── nginx.conf         # Configuración de Nginx
├── tests/                  # Tests de Selenium
│   ├── test_login.py      # Suite de tests automatizados
│   ├── requirements.txt   # Dependencias de Python
│   └── pytest.ini         # Configuración de Pytest
├── .github/
│   └── workflows/
│       └── ci-cd.yml      # Pipeline de CI/CD
├── docker-compose.yml     # Orquestación de servicios
└── README.md              # Este archivo
```

## 🚀 Inicio Rápido

### Opción 1: Con Docker Compose (Recomendado)

```bash
# Construir y levantar todos los servicios
docker-compose up --build

# Acceder a:
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
# Selenium Grid: http://localhost:4444
```

### Opción 2: Instalación Local

#### Backend

```bash
cd backend
npm install
npm start
```

El backend estará disponible en `http://localhost:5000`

#### Frontend

```bash
cd frontend
npm install
npm start
```

El frontend estará disponible en `http://localhost:3000`

#### Tests

```bash
cd tests
pip install -r requirements.txt
pytest test_login.py -v
```

## 🧪 Ejecutar Tests

### Tests Locales

```bash
# Asegúrate de que backend y frontend estén corriendo
cd tests
pytest test_login.py -v --html=test-report.html
```

### Tests con Docker

```bash
# Levantar servicios
docker-compose up -d

# Ejecutar tests
docker-compose exec selenium-chrome pytest /tests/test_login.py
```

## 📊 Suite de Tests

Los tests incluyen:

1. ✅ **test_backend_health** - Verifica que el backend esté disponible
2. ✅ **test_login_page_loads** - Verifica que la página cargue correctamente
3. ✅ **test_login_form_elements_exist** - Verifica que existan todos los elementos del formulario
4. ✅ **test_successful_login** - Prueba login exitoso con credenciales válidas
5. ✅ **test_failed_login_wrong_password** - Prueba login con contraseña incorrecta
6. ✅ **test_failed_login_empty_fields** - Prueba validación de campos vacíos
7. ✅ **test_logout_functionality** - Prueba funcionalidad de logout
8. ✅ **test_username_field_has_correct_attributes** - Verifica atributos del campo username

## 🔐 Credenciales de Prueba

```
Usuario: admin
Contraseña: admin123

Usuario: usuario
Contraseña: usuario123
```

## 🔄 Pipeline CI/CD

El workflow de GitHub Actions se ejecuta en:
- Push a `main` o `develop`
- Pull requests a `main` o `develop`

### Flujo del Pipeline

```
1. Checkout código
2. Configurar Node.js y Python
3. Instalar dependencias
4. Iniciar backend
5. Build y servir frontend
6. Ejecutar tests de Selenium
7. ❌ Si fallan tests → Pipeline se detiene
8. ✅ Si pasan tests → Continuar a deploy
9. Deploy a Staging (branch develop)
10. Deploy a Production (branch main)
```

### Ejemplo de Detección de Errores

Si modificas el ID del campo username en el frontend:

```jsx
// Antes (correcto)
<input id="username" ... />

// Después (incorrecto)
<input id="user-name" ... />
```

El test `test_login_form_elements_exist` fallará:

```
FAILED test_login.py::test_login_form_elements_exist
❌ Los tests fallaron. El pipeline se detendrá aquí.
No se puede avanzar al siguiente entorno debido a errores en las pruebas.
```

## 📈 Ver Resultados

### Reporte HTML

Después de ejecutar los tests, se genera `test-report.html`:

```bash
cd tests
open test-report.html  # macOS
start test-report.html # Windows
xdg-open test-report.html # Linux
```

### GitHub Actions

1. Ve a la pestaña "Actions" en tu repositorio
2. Selecciona el workflow run
3. Descarga el artefacto "test-report" para ver el reporte HTML

## 🛠️ Tecnologías Utilizadas

### Backend
- Node.js
- Express
- JWT (jsonwebtoken)
- bcryptjs
- CORS

### Frontend
- React 18
- Axios
- CSS3 con animaciones

### Testing
- Selenium WebDriver
- Pytest
- pytest-html

### DevOps
- Docker
- Docker Compose
- GitHub Actions
- Nginx

## 📝 Endpoints del Backend

### GET /health
Verifica el estado del servidor

**Response:**
```json
{
  "status": "OK",
  "message": "Server is running"
}
```

### POST /api/login
Autentica un usuario

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response (éxito):**
```json
{
  "success": true,
  "message": "Login exitoso",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  }
}
```

**Response (error):**
```json
{
  "success": false,
  "message": "Credenciales inválidas"
}
```

## 🐛 Troubleshooting

### Backend no inicia
```bash
# Verifica que el puerto 5000 esté libre
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Mata el proceso si es necesario
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Frontend no conecta con backend
Verifica la variable de entorno:
```bash
# En frontend/.env
REACT_APP_API_URL=http://localhost:5000
```

### Tests fallan por timeout
Aumenta el tiempo de espera en `test_login.py`:
```python
wait = WebDriverWait(driver, 20)  # Aumentar de 10 a 20 segundos
```

## 🎯 Demostración de Casos de Uso

### 1. Login Exitoso
1. Abre `http://localhost:3000`
2. Ingresa: usuario `admin`, contraseña `admin123`
3. Click en "Iniciar Sesión"
4. ✅ Verás mensaje de bienvenida con datos del usuario

### 2. Login Fallido
1. Ingresa: usuario `admin`, contraseña `incorrecta`
2. Click en "Iniciar Sesión"
3. ❌ Verás mensaje de error "Credenciales inválidas"

### 3. Detección de Error en Tests
1. Modifica `frontend/src/App.js`:
   ```jsx
   // Cambia id="username" por id="user-name"
   ```
2. Commit y push
3. GitHub Actions ejecutará tests
4. ❌ Test fallará y pipeline se detendrá
5. No se desplegará a staging/production

## 📚 Recursos Adicionales

- [Documentación de Selenium](https://www.selenium.dev/documentation/)
- [Documentación de Pytest](https://docs.pytest.org/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [React Documentation](https://react.dev/)
- [Express.js Guide](https://expressjs.com/)

## 👥 Autor

Proyecto desarrollado para demostración de CI/CD con tests automatizados.

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.
