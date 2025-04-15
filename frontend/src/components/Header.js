import React from 'react';
import { useAppContext } from '../utils/AppContext';

const Header = () => {
  const { activeTab, setActiveTab } = useAppContext();
  
  const tabs = [
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'analysis', label: 'Competitor Analysis' },
    { id: 'prompts', label: 'Prompt Ideas' },
    { id: 'content', label: 'Content Generation' },
    { id: 'history', label: 'History' },
  ];
  
  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-4 flex flex-col md:flex-row items-center justify-between">
        <div className="flex items-center mb-4 md:mb-0">
          <img 
            src="/logo.svg" 
            alt="GenAI Marketing" 
            className="h-10 w-auto mr-3"
            onError={(e) => {
              e.target.onerror = null;
              e.target.src = 'https://via.placeholder.com/40x40?text=GM';
            }}
          />
          <h1 className="text-2xl font-bold text-primary-blue">GenAI Marketing</h1>
        </div>
        
        <button 
          className="btn btn-primary md:hidden mb-4"
          onClick={() => document.getElementById('mobile-menu').classList.toggle('hidden')}
        >
          Menu
        </button>
        
        <nav className="hidden md:flex" id="mobile-menu">
          <ul className="flex flex-col md:flex-row">
            {tabs.map((tab) => (
              <li key={tab.id}>
                <button
                  className={`tab ${activeTab === tab.id ? 'tab-active' : ''} mx-1`}
                  onClick={() => setActiveTab(tab.id)}
                >
                  {tab.label}
                </button>
              </li>
            ))}
          </ul>
        </nav>
        
        <button 
          className="btn btn-outline hidden md:block"
          onClick={() => setActiveTab('settings')}
        >
          Settings
        </button>
      </div>
    </header>
  );
};

export default Header;
