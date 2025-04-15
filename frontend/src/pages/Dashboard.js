import React from 'react';
import { useAppContext } from '../utils/AppContext';

const Dashboard = () => {
  const { setActiveTab } = useAppContext();
  
  // Mock data for dashboard
  const stats = {
    promptsGenerated: 24,
    contentCreated: 18,
    competitorsAnalyzed: 5
  };
  
  const recentActivities = [
    { id: 1, text: 'Generated blog post about AI trends', time: '2 hours ago' },
    { id: 2, text: 'Analyzed competitor website', time: '4 hours ago' },
    { id: 3, text: 'Created new prompt for social media', time: '1 day ago' }
  ];
  
  const llmStatus = [
    { provider: 'OpenAI', status: 'Connected' },
    { provider: 'Claude', status: 'Connected' },
    { provider: 'Gemini', status: 'Connected' },
    { provider: 'DeepSeek', status: 'Not configured' },
    { provider: 'Manus', status: 'Connected' }
  ];
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold mb-6">Welcome to GenAI Marketing Assistant</h2>
      
      <div className="bento-grid">
        {/* Quick Stats */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Quick Stats</h3>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>Prompts Generated:</span>
              <span className="font-medium">{stats.promptsGenerated}</span>
            </div>
            <div className="flex justify-between">
              <span>Content Created:</span>
              <span className="font-medium">{stats.contentCreated}</span>
            </div>
            <div className="flex justify-between">
              <span>Competitors Analyzed:</span>
              <span className="font-medium">{stats.competitorsAnalyzed}</span>
            </div>
          </div>
        </div>
        
        {/* Recent Activities */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Recent Activities</h3>
          <ul className="space-y-3">
            {recentActivities.map(activity => (
              <li key={activity.id} className="border-b pb-2 last:border-0">
                <p>{activity.text}</p>
                <p className="text-sm text-gray-500">{activity.time}</p>
              </li>
            ))}
          </ul>
        </div>
        
        {/* LLM Status */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">LLM Status</h3>
          <ul className="space-y-2">
            {llmStatus.map((llm, index) => (
              <li key={index} className="flex justify-between">
                <span>{llm.provider}:</span>
                <span className={`font-medium ${llm.status === 'Connected' ? 'text-success' : 'text-error'}`}>
                  {llm.status}
                </span>
              </li>
            ))}
          </ul>
        </div>
        
        {/* Quick Actions */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <button 
              className="btn btn-primary w-full"
              onClick={() => setActiveTab('analysis')}
            >
              New Analysis
            </button>
            <button 
              className="btn btn-primary w-full"
              onClick={() => setActiveTab('prompts')}
            >
              Generate Prompt
            </button>
            <button 
              className="btn btn-primary w-full"
              onClick={() => setActiveTab('content')}
            >
              Create Content
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
