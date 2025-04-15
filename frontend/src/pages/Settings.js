import React, { useState, useEffect } from 'react';
import { useAppContext } from '../utils/AppContext';
import { getApiKeys, createApiKey, getConfigurations, createConfiguration } from '../services/api';

const Settings = () => {
  const { setLoading, handleError, showNotification } = useAppContext();
  
  const [apiKeys, setApiKeys] = useState({
    openai: '',
    claude: '',
    gemini: '',
    deepseek: '',
    manus: ''
  });
  
  const [configurations, setConfigurations] = useState({
    default_llm: 'openai',
    default_content_type: 'text',
    default_analysis_focus: 'blog'
  });
  
  useEffect(() => {
    fetchApiKeys();
    fetchConfigurations();
  }, []);
  
  const fetchApiKeys = async () => {
    try {
      setLoading(true);
      const data = await getApiKeys();
      
      // Update state with existing API keys (masked)
      const keys = { ...apiKeys };
      data.forEach(key => {
        keys[key.provider] = '************************';
      });
      
      setApiKeys(keys);
    } catch (error) {
      handleError(error);
    } finally {
      setLoading(false);
    }
  };
  
  const fetchConfigurations = async () => {
    try {
      setLoading(true);
      const data = await getConfigurations();
      
      // Update state with existing configurations
      const configs = { ...configurations };
      data.forEach(config => {
        configs[config.key] = config.value;
      });
      
      setConfigurations(configs);
    } catch (error) {
      handleError(error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleApiKeyChange = (provider, value) => {
    setApiKeys({
      ...apiKeys,
      [provider]: value
    });
  };
  
  const handleConfigChange = (key, value) => {
    setConfigurations({
      ...configurations,
      [key]: value
    });
  };
  
  const updateApiKey = async (provider) => {
    try {
      setLoading(true);
      
      // Only update if the key is not masked (i.e., user has entered a new key)
      if (apiKeys[provider] && !apiKeys[provider].includes('*')) {
        await createApiKey(provider, apiKeys[provider]);
        showNotification(`${provider} API key updated successfully`, 'success');
      } else {
        showNotification('Please enter a valid API key', 'warning');
      }
    } catch (error) {
      handleError(error);
    } finally {
      setLoading(false);
    }
  };
  
  const saveConfigurations = async () => {
    try {
      setLoading(true);
      
      // Update each configuration
      for (const [key, value] of Object.entries(configurations)) {
        await createConfiguration(key, value, `Default ${key.replace('_', ' ')}`);
      }
      
      showNotification('Settings saved successfully', 'success');
    } catch (error) {
      handleError(error);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold mb-6">Settings</h2>
      
      <div className="card mb-8">
        <h3 className="text-lg font-semibold mb-4">API Configuration</h3>
        
        <div className="space-y-4">
          <div>
            <label className="block mb-1">OpenAI API Key</label>
            <div className="flex space-x-2">
              <input
                type="password"
                className="input flex-grow"
                placeholder="Enter API key"
                value={apiKeys.openai}
                onChange={(e) => handleApiKeyChange('openai', e.target.value)}
              />
              <button 
                className="btn btn-primary"
                onClick={() => updateApiKey('openai')}
              >
                Update
              </button>
            </div>
          </div>
          
          <div>
            <label className="block mb-1">Claude API Key</label>
            <div className="flex space-x-2">
              <input
                type="password"
                className="input flex-grow"
                placeholder="Enter API key"
                value={apiKeys.claude}
                onChange={(e) => handleApiKeyChange('claude', e.target.value)}
              />
              <button 
                className="btn btn-primary"
                onClick={() => updateApiKey('claude')}
              >
                Update
              </button>
            </div>
          </div>
          
          <div>
            <label className="block mb-1">Gemini API Key</label>
            <div className="flex space-x-2">
              <input
                type="password"
                className="input flex-grow"
                placeholder="Enter API key"
                value={apiKeys.gemini}
                onChange={(e) => handleApiKeyChange('gemini', e.target.value)}
              />
              <button 
                className="btn btn-primary"
                onClick={() => updateApiKey('gemini')}
              >
                Update
              </button>
            </div>
          </div>
          
          <div>
            <label className="block mb-1">DeepSeek API Key</label>
            <div className="flex space-x-2">
              <input
                type="password"
                className="input flex-grow"
                placeholder="Enter API key"
                value={apiKeys.deepseek}
                onChange={(e) => handleApiKeyChange('deepseek', e.target.value)}
              />
              <button 
                className="btn btn-primary"
                onClick={() => updateApiKey('deepseek')}
              >
                Update
              </button>
            </div>
          </div>
          
          <div>
            <label className="block mb-1">Manus API Key</label>
            <div className="flex space-x-2">
              <input
                type="password"
                className="input flex-grow"
                placeholder="Enter API key"
                value={apiKeys.manus}
                onChange={(e) => handleApiKeyChange('manus', e.target.value)}
              />
              <button 
                className="btn btn-primary"
                onClick={() => updateApiKey('manus')}
              >
                Update
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div className="card">
        <h3 className="text-lg font-semibold mb-4">Default Settings</h3>
        
        <div className="space-y-4">
          <div>
            <label className="block mb-1">Default LLM</label>
            <select
              className="select"
              value={configurations.default_llm}
              onChange={(e) => handleConfigChange('default_llm', e.target.value)}
            >
              <option value="openai">OpenAI</option>
              <option value="claude">Claude</option>
              <option value="gemini">Gemini</option>
              <option value="deepseek">DeepSeek</option>
              <option value="manus">Manus</option>
            </select>
          </div>
          
          <div>
            <label className="block mb-1">Default Content Type</label>
            <select
              className="select"
              value={configurations.default_content_type}
              onChange={(e) => handleConfigChange('default_content_type', e.target.value)}
            >
              <option value="text">Text</option>
              <option value="image">Image</option>
              <option value="text+image">Text + Image</option>
            </select>
          </div>
          
          <div>
            <label className="block mb-1">Default Analysis Focus</label>
            <select
              className="select"
              value={configurations.default_analysis_focus}
              onChange={(e) => handleConfigChange('default_analysis_focus', e.target.value)}
            >
              <option value="blog">Blog content</option>
              <option value="social">Social media</option>
              <option value="website">Website copy</option>
            </select>
          </div>
          
          <button 
            className="btn btn-primary w-full"
            onClick={saveConfigurations}
          >
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
};

export default Settings;
