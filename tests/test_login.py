import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:5000"

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_backend_health():
    import requests
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        assert response.status_code == 200
        assert response.json()["status"] == "OK"
        print("✓ Backend health check passed")
    except Exception as e:
        pytest.fail(f"Backend no está disponible: {str(e)}")

def test_login_page_loads(driver):
    driver.get(FRONTEND_URL)
    
    try:
        title = driver.find_element(By.TAG_NAME, "h1")
        assert "Iniciar Sesión" in title.text
        print("✓ Página de login cargada correctamente")
    except NoSuchElementException:
        pytest.fail("No se encontró el título de la página")

def test_login_form_elements_exist(driver):
    driver.get(FRONTEND_URL)
    
    try:
        username_input = driver.find_element(By.ID, "username")
        assert username_input is not None
        assert username_input.get_attribute("type") == "text"
        print("✓ Campo username encontrado con ID correcto")
        
        password_input = driver.find_element(By.ID, "password")
        assert password_input is not None
        assert password_input.get_attribute("type") == "password"
        print("✓ Campo password encontrado con ID correcto")
        
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        assert login_button is not None
        print("✓ Botón de login encontrado")
        
    except NoSuchElementException as e:
        pytest.fail(f"Elemento del formulario no encontrado: {str(e)}")

def test_successful_login(driver):
    driver.get(FRONTEND_URL)
    
    wait = WebDriverWait(driver, 10)
    
    username_input = wait.until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    username_input.clear()
    username_input.send_keys("admin")
    
    password_input.clear()
    password_input.send_keys("admin123")
    
    login_button.click()
    
    try:
        success_message = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Bienvenido')]"))
        )
        assert success_message is not None
        print("✓ Login exitoso - Usuario autenticado correctamente")
        
        user_info = driver.find_element(By.CLASS_NAME, "user-info")
        assert "admin" in user_info.text
        print("✓ Información de usuario mostrada correctamente")
        
    except TimeoutException:
        pytest.fail("No se mostró el mensaje de éxito después del login")

def test_failed_login_wrong_password(driver):
    driver.get(FRONTEND_URL)
    
    wait = WebDriverWait(driver, 10)
    
    username_input = wait.until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    username_input.clear()
    username_input.send_keys("admin")
    
    password_input.clear()
    password_input.send_keys("wrongpassword")
    
    login_button.click()
    
    try:
        error_message = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "error"))
        )
        assert "inválidas" in error_message.text.lower() or "error" in error_message.text.lower()
        print("✓ Error de credenciales inválidas detectado correctamente")
        
    except TimeoutException:
        pytest.fail("No se mostró el mensaje de error con credenciales incorrectas")

def test_failed_login_empty_fields(driver):
    driver.get(FRONTEND_URL)
    
    wait = WebDriverWait(driver, 10)
    
    login_button = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
    )
    
    login_button.click()
    
    username_input = driver.find_element(By.ID, "username")
    
    is_valid = driver.execute_script(
        "return arguments[0].validity.valid;", username_input
    )
    assert not is_valid
    print("✓ Validación de campos vacíos funciona correctamente")

def test_logout_functionality(driver):
    driver.get(FRONTEND_URL)
    
    wait = WebDriverWait(driver, 10)
    
    username_input = wait.until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    username_input.send_keys("admin")
    password_input.send_keys("admin123")
    login_button.click()
    
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Bienvenido')]"))
    )
    
    logout_button = driver.find_element(By.CLASS_NAME, "logout-button")
    logout_button.click()
    
    try:
        login_form = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "login-form"))
        )
        assert login_form is not None
        print("✓ Logout exitoso - Regresó a la página de login")
        
    except TimeoutException:
        pytest.fail("No se regresó a la página de login después del logout")

def test_username_field_has_correct_attributes(driver):
    driver.get(FRONTEND_URL)
    
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
