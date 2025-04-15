import React from 'react';
import { AppProvider, useAppContext } from './utils/AppContext';
import Header from './components/Header';
import Notification from './components/Notification';
import Dashboard from './pages/Dashboard';
import CompetitorAnalysis from './pages/CompetitorAnalysis';
import PromptIdeas from './pages/PromptIdeas';
import ContentGeneration from './pages/ContentGeneration';
import Settings from './pages/Settings';
import './styles/index.css';

const AppContent = () => {
  const { activeTab } = useAppContext();
  
  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'analysis':
        return <CompetitorAnalysis />;
      case 'prompts':
        return <PromptIdeas />;
      case 'content':
        return <ContentGeneration />;
      case 'settings':
        return <Settings />;
      default:
        return <Dashboard />;
    }
  };
  
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main>
        {renderContent()}
      </main>
      <Notification />
    </div>
  );
};

const App = () => {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
};

export default App;
