import React, { useState, useEffect } from 'react';
import { useAppContext } from '../utils/AppContext';
import { analyzeCompetitor, getAnalyses } from '../services/api';

const CompetitorAnalysis = () => {
  const { setLoading, handleError, showNotification, setSelectedAnalysis } = useAppContext();
  
  const [competitorUrl, setCompetitorUrl] = useState('');
  const [analysisType, setAnalysisType] = useState('blog');
  const [provider, setProvider] = useState('openai');
  const [analyses, setAnalyses] = useState([]);
  const [analysisResult, setAnalysisResult] = useState(null);
  
  useEffect(() => {
    fetchAnalyses();
  }, []);
  
  const fetchAnalyses = async () => {
    try {
      setLoading(true);
      const data = await getAnalyses();
      setAnalyses(data);
    } catch (error) {
      handleError(error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleAnalyze = async (e) => {
    e.preventDefault();
    
    if (!competitorUrl) {
      showNotification('Please enter a competitor URL', 'warning');
      return;
    }
    
    try {
      setLoading(true);
      const result = await analyzeCompetitor(competitorUrl, analysisType, provider);
      setAnalysisResult(result);
      showNotification('Analysis completed successfully', 'success');
      fetchAnalyses(); // Refresh the list
    } catch (error) {
      handleError(error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleSelectAnalysis = (analysis) => {
    setAnalysisResult(analysis);
    setSelectedAnalysis(analysis);
  };
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold mb-6">Competitor Analysis</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">New Analysis</h3>
          
          <form onSubmit={handleAnalyze} className="space-y-4">
            <div>
              <label className="block mb-1">Competitor URL</label>
              <input
                type="text"
                className="input"
                placeholder="https://example.com"
                value={competitorUrl}
                onChange={(e) => setCompetitorUrl(e.target.value)}
              />
            </div>
            
            <div>
              <label className="block mb-1">Analysis Focus</label>
              <div className="flex space-x-4">
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="analysisType"
                    value="blog"
                    checked={analysisType === 'blog'}
                    onChange={() => setAnalysisType('blog')}
                    className="mr-1"
                  />
                  Blog content
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="analysisType"
                    value="social"
                    checked={analysisType === 'social'}
                    onChange={() => setAnalysisType('social')}
                    className="mr-1"
                  />
                  Social media
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="analysisType"
                    value="website"
                    checked={analysisType === 'website'}
                    onChange={() => setAnalysisType('website')}
                    className="mr-1"
                  />
                  Website copy
                </label>
              </div>
            </div>
            
            <div>
              <label className="block mb-1">Select LLM for analysis</label>
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
            
            <button type="submit" className="btn btn-primary w-full">
              Start Analysis
            </button>
          </form>
        </div>
        
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Previous Analyses</h3>
          
          {analyses.length === 0 ? (
            <p className="text-gray-500">No analyses yet. Start by analyzing a competitor.</p>
          ) : (
            <ul className="space-y-2 max-h-60 overflow-y-auto">
              {analyses.map((analysis) => (
                <li 
                  key={analysis.id}
                  className="p-2 hover:bg-gray-100 rounded cursor-pointer"
                  onClick={() => handleSelectAnalysis(analysis)}
                >
                  <div className="flex justify-between">
                    <span className="font-medium">{analysis.competitor_url}</span>
                    <span className="text-sm text-gray-500">{analysis.analysis_type}</span>
                  </div>
                  <div className="text-sm text-gray-500">
                    {new Date(analysis.created_at).toLocaleString()}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
      
      {analysisResult && (
        <div className="mt-8 card">
          <h3 className="text-lg font-semibold mb-4">Analysis Results</h3>
          
          <div className="space-y-6">
            <div>
              <h4 className="font-medium mb-2">Content Themes:</h4>
              <ul className="list-disc pl-5 space-y-1">
                {analysisResult.content_themes.map((theme, index) => (
                  <li key={index}>
                    {typeof theme === 'string' 
                      ? theme 
                      : `${theme.theme || theme.name || 'Theme'} (${theme.confidence || theme.score || 0}% confidence)`}
                  </li>
                ))}
              </ul>
            </div>
            
            <div>
              <h4 className="font-medium mb-2">Content Strategy:</h4>
              <ul className="list-disc pl-5 space-y-1">
                {analysisResult.content_strategy.map((strategy, index) => (
                  <li key={index}>{strategy}</li>
                ))}
              </ul>
            </div>
            
            <div className="flex space-x-4">
              <button 
                className="btn btn-primary"
                onClick={() => {
                  setSelectedAnalysis(analysisResult);
                  showNotification('Analysis saved', 'success');
                }}
              >
                Save Analysis
              </button>
              
              <button 
                className="btn btn-secondary"
                onClick={() => {
                  setSelectedAnalysis(analysisResult);
                  // Navigate to prompt ideas page
                  document.getElementById('prompts-tab').click();
                }}
              >
                Generate Prompt Ideas
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CompetitorAnalysis;
