import React, { createContext, useContext, useState, useEffect } from 'react';

const AppContext = createContext();

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within AppProvider');
  }
  return context;
};

export const AppProvider = ({ children }) => {
  // Auth state
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Resume state
  const [currentResume, setCurrentResume] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Initialize auth from localStorage
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
      setIsAuthenticated(true);
    }
  }, []);

  // Auth methods
  const login = (userData, userToken) => {
    setUser(userData);
    setToken(userToken);
    setIsAuthenticated(true);
    localStorage.setItem('token', userToken);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    setIsAuthenticated(false);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  // Resume methods
  const updateCurrentResume = (resume) => {
    setCurrentResume(resume);
  };

  const updateRecommendations = (recs) => {
    setRecommendations(recs);
  };

  const setLoadingState = (isLoading) => {
    setLoading(isLoading);
  };

  const setErrorState = (errorMessage) => {
    setError(errorMessage);
  };

  const clearError = () => {
    setError(null);
  };

  const value = {
    // Auth state
    user,
    token,
    isAuthenticated,
    login,
    logout,

    // Resume state
    currentResume,
    recommendations,
    loading,
    error,
    updateCurrentResume,
    updateRecommendations,
    setLoadingState,
    setErrorState,
    clearError,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};