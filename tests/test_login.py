import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

FRONTEND_URL = "http://login-frontend:80"
BACKEND_URL = "http://login-backend:5000"
SELENIUM_GRID_URL = "http://selenium-chrome:4444"

@pytest.fixture(scope="session")
def driver():
    """
    Fixture con scope='session' para que TODOS los tests 
    usen la MISMA sesión del navegador.
    Puedes ver la sesión en tiempo real en:
    - Grid Console: http://localhost:4444
    - VNC Viewer: http://localhost:7900 (password: secret)
    """
    chrome_options = Options()
    # SIN --headless para que puedas ver la sesión
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--start-maximized')
    
    # Conectar a Selenium Grid
    driver = webdriver.Remote(
        command_executor=SELENIUM_GRID_URL,
        options=chrome_options
    )
    driver.implicitly_wait(10)
    
    print("\n" + "="*80)
    print("🔥 SESIÓN INICIADA - Puedes verla en:")
    print("   📺 VNC: http://localhost:7900 (password: secret)")
    print("   🌐 Grid: http://localhost:4444")
    print("="*80 + "\n")
    
    yield driver
    
    print("\n" + "="*80)
    print("✅ TODOS LOS TESTS COMPLETADOS - Cerrando sesión...")
    print("="*80 + "\n")
    
    driver.quit()

def test_backend_health():
    import requests
    try:
        print("⏳ Verificando conexión con el backend...")
        time.sleep(1)
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        assert response.status_code == 200
        assert response.json()["status"] == "OK"
        print("✓ Backend health check passed")
        time.sleep(2)
    except Exception as e:
        pytest.fail(f"Backend no está disponible: {str(e)}")

def test_login_page_loads(driver):
    print("🌐 Cargando página de login...")
    driver.get(FRONTEND_URL)
    time.sleep(2)
    
    try:
        wait = WebDriverWait(driver, 10)
        title = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        wait.until(lambda d: len(title.text) > 0)
        assert "Iniciar Sesión" in title.text
        print("✓ Página de login cargada correctamente")
        time.sleep(2)
    except (NoSuchElementException, TimeoutException):
        pytest.fail("No se encontró el título de la página o no se cargó correctamente")

def test_login_form_elements_exist(driver):
    print("🔍 Verificando elementos del formulario...")
    driver.get(FRONTEND_URL)
    time.sleep(2)
    
    try:
        username_input = driver.find_element(By.ID, "username")
        assert username_input is not None
        assert username_input.get_attribute("type") == "text"
        print("✓ Campo username encontrado con ID correcto")
        time.sleep(1)
        
        password_input = driver.find_element(By.ID, "password")
        assert password_input is not None
        assert password_input.get_attribute("type") == "password"
        print("✓ Campo password encontrado con ID correcto")
        time.sleep(1)
        
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        assert login_button is not None
        print("✓ Botón de login encontrado")
        time.sleep(2)
        
    except NoSuchElementException as e:
        pytest.fail(f"Elemento del formulario no encontrado: {str(e)}")

def test_successful_login(driver):
    print("✅ Probando login exitoso...")
    driver.get(FRONTEND_URL)
    time.sleep(2)
    
    wait = WebDriverWait(driver, 10)
    
    username_input = wait.until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    print("⌨️  Ingresando usuario...")
    username_input.clear()
    username_input.send_keys("admin")
    time.sleep(1)
    
    print("🔑 Ingresando contraseña...")
    password_input.clear()
    password_input.send_keys("admin123")
    time.sleep(1)
    
    print("🖱️  Haciendo click en 'Iniciar Sesión'...")
    login_button.click()
    time.sleep(2)
    
    try:
        success_message = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Bienvenido')]"))
        )
        assert success_message is not None
        print("✓ Login exitoso - Usuario autenticado correctamente")
        time.sleep(2)
        
        user_info = driver.find_element(By.CLASS_NAME, "user-info")
        assert "admin" in user_info.text
        print("✓ Información de usuario mostrada correctamente")
        time.sleep(3)
        
    except TimeoutException:
        pytest.fail("No se mostró el mensaje de éxito después del login")

def test_failed_login_wrong_password(driver):
    print("❌ Probando login con contraseña incorrecta...")
    driver.get(FRONTEND_URL)
    time.sleep(2)
    
    wait = WebDriverWait(driver, 10)
    
    username_input = wait.until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    print("⌨️  Ingresando usuario correcto...")
    username_input.clear()
    username_input.send_keys("admin")
    time.sleep(1)
    
    print("🔑 Ingresando contraseña INCORRECTA...")
    password_input.clear()
    password_input.send_keys("wrongpassword")
    time.sleep(1)
    
    print("🖱️  Haciendo click en 'Iniciar Sesión'...")
    login_button.click()
    time.sleep(2)
    
    try:
        error_message = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "error"))
        )
        
        wait.until(lambda d: len(error_message.text) > 0)
        
        assert "inválidas" in error_message.text.lower() or "error" in error_message.text.lower()
        print("✓ Error de credenciales inválidas detectado correctamente")
        time.sleep(3)
        
    except TimeoutException:
        pytest.fail("No se mostró el mensaje de error con credenciales incorrectas")

def test_failed_login_empty_fields(driver):
    print("⚠️  Probando validación de campos vacíos...")
    driver.get(FRONTEND_URL)
    time.sleep(2)
    
    wait = WebDriverWait(driver, 10)
    
    login_button = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
    )
    
    print("🖱️  Haciendo click en 'Iniciar Sesión' sin llenar campos...")
    login_button.click()
    time.sleep(2)
    
    username_input = driver.find_element(By.ID, "username")
    
    is_valid = driver.execute_script(
        "return arguments[0].validity.valid;", username_input
    )
    assert not is_valid
    print("✓ Validación de campos vacíos funciona correctamente")
    time.sleep(2)

def test_logout_functionality(driver):
    print("🚪 Probando funcionalidad de logout...")
    driver.get(FRONTEND_URL)
    time.sleep(2)
    
    wait = WebDriverWait(driver, 10)
    
    username_input = wait.until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    print("🔐 Iniciando sesión...")
    username_input.send_keys("admin")
    time.sleep(0.5)
    password_input.send_keys("admin123")
    time.sleep(0.5)
    login_button.click()
    time.sleep(2)
    
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Bienvenido')]"))
    )
    time.sleep(2)
    
    print("👋 Haciendo click en 'Cerrar Sesión'...")
    logout_button = driver.find_element(By.CLASS_NAME, "logout-button")
    logout_button.click()
    time.sleep(2)
    
    try:
        login_form = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "login-form"))
        )
        assert login_form is not None
        print("✓ Logout exitoso - Regresó a la página de login")
        time.sleep(2)
        
    except TimeoutException:
        pytest.fail("No se regresó a la página de login después del logout")

def test_username_field_has_correct_attributes(driver):
    print("🔎 Verificando atributos del campo username...")
    driver.get(FRONTEND_URL)
    time.sleep(2)
    
    wait = WebDriverWait(driver, 10)
    username_input = wait.until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    
    assert username_input.get_attribute("id") == "username"
    assert username_input.get_attribute("type") == "text"
    assert username_input.get_attribute("data-testid") == "username-input"
    
    print("✓ Campo username tiene todos los atributos correctos")
    print(f"  - ID: {username_input.get_attribute('id')}")
    print(f"  - Type: {username_input.get_attribute('type')}")
    print(f"  - TestID: {username_input.get_attribute('data-testid')}")
    time.sleep(2)
