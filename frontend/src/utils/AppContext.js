import React, { createContext, useContext, useState } from 'react';

// Create Context
const AppContext = createContext();

// Provider Component
export const AppProvider = ({ children }) => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);
  const [selectedPrompt, setSelectedPrompt] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [notification, setNotification] = useState(null);

  // Show notification
  const showNotification = (message, type = 'info') => {
    setNotification({ message, type });
    setTimeout(() => {
      setNotification(null);
    }, 5000);
  };

  // Handle errors
  const handleError = (error) => {
    console.error('Error:', error);
    setError(error.message || 'An unexpected error occurred');
    showNotification(error.message || 'An unexpected error occurred', 'error');
  };

  // Clear error
  const clearError = () => {
    setError(null);
  };

  return (
    <AppContext.Provider
      value={{
        activeTab,
        setActiveTab,
        selectedAnalysis,
        setSelectedAnalysis,
        selectedPrompt,
        setSelectedPrompt,
        loading,
        setLoading,
        error,
        setError,
        handleError,
        clearError,
        notification,
        showNotification,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

// Custom Hook to use the AppContext
export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};
