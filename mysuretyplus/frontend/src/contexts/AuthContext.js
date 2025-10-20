import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

// Configuration de base pour axios
axios.defaults.baseURL = 'http://localhost:8000';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  // Configurer axios avec le token
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Token ${token}`;
      // Vérifier si le token est toujours valide
      checkAuthStatus();
    } else {
      setLoading(false);
    }
  }, [token]);

  const checkAuthStatus = async () => {
    try {
      const response = await axios.get('/api/users/profile/', {
        headers: { 'Authorization': `Token ${token}` }
      });
      setUser(response.data);
      setLoading(false);
    } catch (error) {
      // Token invalide, déconnexion
      // Token invalide, déconnecter l'utilisateur
      setToken(null);
      setUser(null);
      localStorage.removeItem('token');
      delete axios.defaults.headers.common['Authorization'];
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    try {
      const response = await axios.post('/api/users/login/', {
        username,
        password
      });
      
      const { token: authToken, ...userData } = response.data;
      
      setToken(authToken);
      setUser(userData);
      localStorage.setItem('token', authToken);
      axios.defaults.headers.common['Authorization'] = `Token ${authToken}`;
      
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Erreur de connexion'
      };
    }
  };

  const register = async (username, email, password) => {
    try {
      const response = await axios.post('/api/users/register/', {
        username,
        email,
        password
      });
      
      // Ne pas connecter automatiquement après l'inscription
      // Juste retourner le succès pour rediriger vers la page de connexion
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Erreur d\'inscription'
      };
    }
  };

  const logout = async () => {
    try {
      if (token) {
        await axios.post('/api/users/logout/', {}, {
          headers: { 'Authorization': `Token ${token}` }
        });
      }
    } catch (error) {
      console.error('Erreur lors de la déconnexion:', error);
    } finally {
      setToken(null);
      setUser(null);
      localStorage.removeItem('token');
      delete axios.defaults.headers.common['Authorization'];
    }
  };

  const updateProfile = async (profileData) => {
    try {
      const response = await axios.put('/api/users/profile/', profileData);
      setUser(response.data);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Erreur de mise à jour du profil'
      };
    }
  };

  const value = {
    user,
    token,
    isAuthenticated: !!token,
    loading,
    login,
    register,
    logout,
    updateProfile
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};




