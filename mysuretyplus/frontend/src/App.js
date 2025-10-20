import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import frFR from 'antd/locale/fr_FR';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Home from './screens/Home';
import About from './screens/About';
import FAQ from './screens/FAQ';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import ForgotPassword from './components/auth/ForgotPassword';
import ResetPassword from './components/auth/ResetPassword';
import Dashboard from './components/dashboard/Dashboard';
import Layout from './components/layout/Layout';
import './App.css';

// Composant de protection des routes
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <div>Chargement...</div>;
  }
  
  return isAuthenticated ? children : <Navigate to="/login" />;
};

// Composant principal de l'application
const AppContent = () => {
  const { isAuthenticated } = useAuth();

  return (
    <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Routes>
        {/* Page d'accueil - PREMIÈRE PAGE */}
        <Route path="/" element={<Home />} />
        
        {/* Pages d'information */}
        <Route path="/about" element={<About />} />
        <Route path="/faq" element={<FAQ />} />
        
        {/* Routes d'authentification */}
        <Route 
          path="/login" 
          element={<Login />} 
        />
        <Route 
          path="/register" 
          element={<Register />} 
        />
        <Route 
          path="/forgot-password" 
          element={isAuthenticated ? <Navigate to="/dashboard" /> : <ForgotPassword />} 
        />
        <Route 
          path="/reset-password/:token" 
          element={isAuthenticated ? <Navigate to="/dashboard" /> : <ResetPassword />} 
        />
        
        {/* Routes protégées */}
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <Layout>
                <Dashboard />
              </Layout>
            </ProtectedRoute>
          } 
        />
      </Routes>
    </Router>
  );
};

// Composant racine avec le provider d'authentification
const App = () => {
  return (
    <ConfigProvider locale={frFR}>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </ConfigProvider>
  );
};

export default App;



