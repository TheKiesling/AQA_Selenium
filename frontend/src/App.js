import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');

    try {
      const response = await axios.post(`${API_URL}/api/login`, {
        username,
        password
      });

      if (response.data.success) {
        setMessage('¡Login exitoso!');
        setIsLoggedIn(true);
        setUserData(response.data.user);
        localStorage.setItem('token', response.data.token);
      }
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Error al iniciar sesión';
      setMessage(errorMessage);
      setIsLoggedIn(false);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserData(null);
    setUsername('');
    setPassword('');
    setMessage('');
    localStorage.removeItem('token');
  };

  if (isLoggedIn && userData) {
    return (
      <div className="container">
        <div className="success-card">
          <div className="success-icon">✓</div>
          <h1>¡Bienvenido!</h1>
          <div className="user-info">
            <p><strong>Usuario:</strong> {userData.username}</p>
            <p><strong>Email:</strong> {userData.email}</p>
          </div>
          <button 
            onClick={handleLogout}
            className="logout-button"
          >
            Cerrar Sesión
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="login-card">
        <h1>Iniciar Sesión</h1>
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Usuario</label>
            <input
              type="text"
              id="user"
              data-testid="username-input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Ingresa tu usuario"
              required
              disabled={isLoading}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <input
              type="password"
              id="password"
              data-testid="password-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Ingresa tu contraseña"
              required
              disabled={isLoading}
            />
          </div>

          <button 
            type="submit" 
            className="submit-button"
            data-testid="login-button"
            disabled={isLoading}
          >
            {isLoading ? 'Cargando...' : 'Iniciar Sesión'}
          </button>
        </form>

        {message && (
          <div className={`message ${message.includes('exitoso') ? 'success' : 'error'}`}>
            {message}
          </div>
        )}

        <div className="demo-credentials">
          <p><strong>Credenciales de prueba:</strong></p>
          <p>Usuario: admin | Contraseña: admin123</p>
          <p>Usuario: usuario | Contraseña: usuario123</p>
        </div>
      </div>
    </div>
  );
}

export default App;
