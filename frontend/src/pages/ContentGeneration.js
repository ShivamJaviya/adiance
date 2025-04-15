import React, { useState, useEffect } from 'react';
import { useAppContext } from '../utils/AppContext';
import { generateContent, getContent } from '../services/api';

const ContentGeneration = () => {
  const { 
    setLoading, 
    handleError, 
    showNotification, 
    selectedPrompt 
  } = useAppContext();
  
  const [contentType, setContentType] = useState('text');
  const [provider, setProvider] = useState('openai');
  const [length, setLength] = useState('medium');
  const [tone, setTone] = useState('professional');
  const [generatedContent, setGeneratedContent] = useState(null);
  const [contentHistory, setContentHistory] = useState([]);
  
  useEffect(() => {
    fetchContentHistory();
  }, []);
  
  const fetchContentHistory = async () => {
    try {
      setLoading(true);
      const data = await getContent();
      setContentHistory(data);
    } catch (error) {
      handleError(error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleGenerateContent = async () => {
    if (!selectedPrompt) {
      showNotification('Please select a prompt first', 'warning');
      return;
    }
    
    const parameters = {
      length,
      tone,
      max_tokens: length === 'short' ? 500 : length === 'medium' ? 1000 : 2000
    };
    
    try {
      setLoading(true);
      const result = await generateContent(selectedPrompt.id, contentType, provider, parameters);
      setGeneratedContent(result);
      showNotification('Content generated successfully', 'success');
      fetchContentHistory(); // Refresh the list
    } catch (error) {
      handleError(error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleExport = () => {
    if (!generatedContent) return;
    
    // Create a blob with the content
    const blob = new Blob([generatedContent.content_text || ''], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    
    // Create a link and trigger download
    const a = document.createElement('a');
    a.href = url;
    a.download = `content-${generatedContent.id}.txt`;
    document.body.appendChild(a);
    a.click();
    
    // Clean up
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification('Content exported successfully', 'success');
  };
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold mb-6">Content Generation</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Generate New Content</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block mb-1">Selected Prompt</label>
              {selectedPrompt ? (
                <div className="p-2 bg-gray-100 rounded">
                  <p>{selectedPrompt.prompt_text}</p>
                </div>
              ) : (
                <p className="text-gray-500">No prompt selected. Please select a prompt from the Prompt Ideas page.</p>
              )}
            </div>
            
            <div>
              <label className="block mb-1">Content Type</label>
              <div className="flex space-x-4">
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="contentType"
                    value="text"
                    checked={contentType === 'text'}
                    onChange={() => setContentType('text')}
                    className="mr-1"
                  />
                  Text
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="contentType"
                    value="image"
                    checked={contentType === 'image'}
                    onChange={() => setContentType('image')}
                    className="mr-1"
                  />
                  Image
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="contentType"
                    value="text+image"
                    checked={contentType === 'text+image'}
                    onChange={() => setContentType('text+image')}
                    className="mr-1"
                  />
                  Text + Image
                </label>
              </div>
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
              <label className="block mb-1">Additional Parameters</label>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm mb-1">Length</label>
                  <select
                    className="select"
                    value={length}
                    onChange={(e) => setLength(e.target.value)}
                  >
                    <option value="short">Short</option>
                    <option value="medium">Medium</option>
                    <option value="long">Long</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm mb-1">Tone</label>
                  <select
                    className="select"
                    value={tone}
                    onChange={(e) => setTone(e.target.value)}
                  >
                    <option value="professional">Professional</option>
                    <option value="casual">Casual</option>
                    <option value="enthusiastic">Enthusiastic</option>
                  </select>
                </div>
              </div>
            </div>
            
            <button 
              className="btn btn-primary w-full"
              onClick={handleGenerateContent}
              disabled={!selectedPrompt}
            >
              Generate Content
            </button>
          </div>
        </div>
        
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Content History</h3>
          
          {contentHistory.length === 0 ? (
            <p className="text-gray-500">No content generated yet. Generate some content based on a prompt.</p>
          ) : (
            <ul className="space-y-2 max-h-60 overflow-y-auto">
              {contentHistory.map((content) => (
                <li 
                  key={content.id}
                  className="p-2 hover:bg-gray-100 rounded cursor-pointer"
                  onClick={() => setGeneratedContent(content)}
                >
                  <div className="flex justify-between">
                    <span className="font-medium">{content.content_type}</span>
                    <span className="text-sm text-gray-500">{content.provider}</span>
                  </div>
                  <div className="text-sm text-gray-500">
                    {new Date(content.created_at).toLocaleString()}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
      
      {generatedContent && (
        <div className="mt-8 card">
          <h3 className="text-lg font-semibold mb-4">Generated Content</h3>
          
          <div className="space-y-4">
            {generatedContent.content_text && (
              <div className="p-4 bg-gray-100 rounded whitespace-pre-wrap">
                {generatedContent.content_text}
              </div>
            )}
            
            {generatedContent.content_url && (
              <div className="text-center">
                <img 
                  src={generatedContent.content_url} 
                  alt="Generated content" 
                  className="max-w-full mx-auto rounded"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = 'https://via.placeholder.com/400x300?text=Image+Not+Available';
                  }}
                />
              </div>
            )}
            
            <div className="flex space-x-4">
              <button 
                className="btn btn-primary"
                onClick={() => showNotification('Content saved', 'success')}
              >
                Save
              </button>
              
              <button 
                className="btn btn-outline"
                onClick={handleExport}
              >
                Export
              </button>
              
              <button 
                className="btn btn-secondary"
                onClick={handleGenerateContent}
              >
                Regenerate
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ContentGeneration;
