import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Configuration API
export const getApiKeys = async () => {
  const response = await axios.get(`${API_URL}/config/api-keys`);
  return response.data;
};

export const createApiKey = async (provider, apiKey) => {
  const response = await axios.post(`${API_URL}/config/api-keys`, {
    provider,
    api_key: apiKey
  });
  return response.data;
};

export const deleteApiKey = async (provider) => {
  const response = await axios.delete(`${API_URL}/config/api-keys/${provider}`);
  return response.data;
};

export const getConfigurations = async () => {
  const response = await axios.get(`${API_URL}/config/configurations`);
  return response.data;
};

export const createConfiguration = async (key, value, description) => {
  const response = await axios.post(`${API_URL}/config/configurations`, {
    key,
    value,
    description
  });
  return response.data;
};

// Analysis API
export const analyzeCompetitor = async (competitorUrl, analysisType, provider) => {
  const response = await axios.post(`${API_URL}/analysis/analyze`, {
    competitor_url: competitorUrl,
    analysis_type: analysisType,
    provider
  });
  return response.data;
};

export const getAnalyses = async () => {
  const response = await axios.get(`${API_URL}/analysis/analyses`);
  return response.data;
};

export const getAnalysis = async (analysisId) => {
  const response = await axios.get(`${API_URL}/analysis/analyses/${analysisId}`);
  return response.data;
};

export const generatePromptIdeas = async (analysisId, provider, numIdeas = 5) => {
  const response = await axios.post(`${API_URL}/analysis/generate-prompts`, {
    analysis_id: analysisId,
    provider,
    num_ideas: numIdeas
  });
  return response.data;
};

export const getPromptIdeas = async (analysisId = null) => {
  const url = analysisId 
    ? `${API_URL}/analysis/prompt-ideas?analysis_id=${analysisId}` 
    : `${API_URL}/analysis/prompt-ideas`;
  const response = await axios.get(url);
  return response.data;
};

export const getPromptIdea = async (promptId) => {
  const response = await axios.get(`${API_URL}/analysis/prompt-ideas/${promptId}`);
  return response.data;
};

// Content API
export const generateContent = async (promptId, contentType, provider, parameters = {}) => {
  const response = await axios.post(`${API_URL}/content/generate`, {
    prompt_id: promptId,
    content_type: contentType,
    provider,
    parameters
  });
  return response.data;
};

export const getContent = async (promptId = null) => {
  const url = promptId 
    ? `${API_URL}/content/content?prompt_id=${promptId}` 
    : `${API_URL}/content/content`;
  const response = await axios.get(url);
  return response.data;
};

export const getContentById = async (contentId) => {
  const response = await axios.get(`${API_URL}/content/content/${contentId}`);
  return response.data;
};

export const deleteContent = async (contentId) => {
  const response = await axios.delete(`${API_URL}/content/content/${contentId}`);
  return response.data;
};
