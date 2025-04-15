import React, { useState, useEffect } from 'react';
import { useAppContext } from '../utils/AppContext';
import { getPromptIdeas, generatePromptIdeas } from '../services/api';

const PromptIdeas = () => {
  const { 
    setLoading, 
    handleError, 
    showNotification, 
    selectedAnalysis, 
    setSelectedPrompt 
  } = useAppContext();
  
  const [provider, setProvider] = useState('openai');
  const [promptIdeas, setPromptIdeas] = useState([]);
  const [numIdeas, setNumIdeas] = useState(5);
  
  useEffect(() => {
    if (selectedAnalysis) {
      fetchPromptIdeas(selectedAnalysis.id);
    }
  }, [selectedAnalysis]);
  
  const fetchPromptIdeas = async (analysisId) => {
    try {
      setLoading(true);
      const data = await getPromptIdeas(analysisId);
      setPromptIdeas(data);
    } catch (error) {
      handleError(error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleGenerateIdeas = async () => {
    if (!selectedAnalysis) {
      showNotification('Please select an analysis first', 'warning');
      return;
    }
    
    try {
      setLoading(true);
      const result = await generatePromptIdeas(selectedAnalysis.id, provider, numIdeas);
      setPromptIdeas(result);
      showNotification('Prompt ideas generated successfully', 'success');
    } catch (error) {
      handleError(error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleUsePrompt = (prompt) => {
    setSelectedPrompt(prompt);
    showNotification('Prompt selected for content generation', 'success');
    // Navigate to content generation page
    document.getElementById('content-tab').click();
  };
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold mb-6">Prompt Ideas</h2>
      
      <div className="card mb-8">
        <h3 className="text-lg font-semibold mb-4">Generate New Prompt Ideas</h3>
        
        <div className="space-y-4">
          <div>
            <label className="block mb-1">Based on Analysis</label>
            {selectedAnalysis ? (
              <div className="p-2 bg-gray-100 rounded">
                <div className="font-medium">{selectedAnalysis.competitor_url}</div>
                <div className="text-sm text-gray-500">
                  {selectedAnalysis.analysis_type} analysis from {new Date(selectedAnalysis.created_at).toLocaleString()}
                </div>
              </div>
            ) : (
              <p className="text-gray-500">No analysis selected. Please select an analysis from the Competitor Analysis page.</p>
            )}
          </div>
          
          <div>
            <label className="block mb-1">Generate using</label>
            <select
              className="select"
              value={provider}
              onChange={(e) => setProvider(e.target.value)}
            >
              <option value="openai">OpenAI</option>
              <option value="claude">Claude</option>
              <option value="gemini">Gemini</option>
              <option value="deepseek">DeepSeek</option>
              <option value="manus">Manus</option>
            </select>
          </div>
          
          <div>
            <label className="block mb-1">Number of Ideas</label>
            <input
              type="number"
              className="input"
              min="1"
              max="10"
              value={numIdeas}
              onChange={(e) => setNumIdeas(parseInt(e.target.value))}
            />
          </div>
          
          <button 
            className="btn btn-primary w-full"
            onClick={handleGenerateIdeas}
            disabled={!selectedAnalysis}
          >
            Generate Ideas
          </button>
        </div>
      </div>
      
      <h3 className="text-lg font-semibold mb-4">Generated Prompt Ideas</h3>
      
      {promptIdeas.length === 0 ? (
        <p className="text-gray-500">No prompt ideas yet. Generate some ideas based on an analysis.</p>
      ) : (
        <div className="bento-grid">
          {promptIdeas.map((prompt) => (
            <div key={prompt.id} className="card">
              <div className="mb-2">
                <span className="inline-block bg-primary-blue text-white text-xs px-2 py-1 rounded-full">
                  {prompt.confidence_score ? `${Math.round(prompt.confidence_score)}% confidence` : 'New Prompt'}
                </span>
              </div>
              <p className="mb-4">{prompt.prompt_text}</p>
              <button 
                className="btn btn-secondary w-full"
                onClick={() => handleUsePrompt(prompt)}
              >
                Use This Prompt
              </button>
            </div>
          ))}
        </div>
      )}
      
      {promptIdeas.length > 0 && (
        <div className="mt-6 text-center">
          <button 
            className="btn btn-outline"
            onClick={handleGenerateIdeas}
          >
            Generate More Ideas
          </button>
        </div>
      )}
    </div>
  );
};

export default PromptIdeas;
