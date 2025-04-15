# Deployment Instructions for GenAI Marketing Webapp

This document provides step-by-step instructions for deploying the GenAI Marketing Webapp to DigitalOcean App Platform.

## Prerequisites

1. DigitalOcean account with access to App Platform
2. GitHub repository with the application code
3. API keys for the LLM providers (OpenAI, Claude, Gemini, DeepSeek, Manus)
4. Custom domain (marketinghub.adiance.com) DNS access

## Deployment Steps

### 1. Prepare Your Repository

1. Push the application code to your GitHub repository
2. Ensure the repository structure matches the configuration in `.do/app.yaml`
3. Make sure Dockerfiles are in their correct locations:
   - `backend/Dockerfile.backend`
   - `frontend/Dockerfile.frontend`

### 2. Create App on DigitalOcean App Platform

1. Log in to your DigitalOcean account
2. Navigate to App Platform
3. Click "Create App"
4. Select your GitHub repository
5. Choose "Use existing app spec" and select the `.do/app.yaml` file
6. Review the configuration and click "Next"

### 3. Configure Environment Variables

Set up the following environment variables in the App Platform UI:
- `SECRET_KEY`: Generate a secure random string
- `OPENAI_API_KEY`: Your OpenAI API key
- `ANTHROPIC_API_KEY`: Your Anthropic Claude API key
- `GEMINI_API_KEY`: Your Google Gemini API key
- `DEEPSEEK_API_KEY`: Your DeepSeek API key
- `MANUS_API_KEY`: Your Manus API key

### 4. Configure Custom Domain

1. In the App Platform UI, go to the "Domains" tab
2. Add your custom domain: marketinghub.adiance.com
3. Follow the instructions to verify domain ownership
4. Set up the required DNS records:
   - CNAME record pointing to your DigitalOcean app URL
   - TXT record for domain verification

### 5. Deploy the Application

1. Click "Deploy to Production"
2. Monitor the build and deployment process
3. Once complete, your application will be available at marketinghub.adiance.com

### 6. Post-Deployment Verification

1. Visit your custom domain to ensure the application is running
2. Test all functionality:
   - Competitor analysis
   - Prompt generation
   - Content creation
   - LLM integrations

## Troubleshooting

- Check application logs in the DigitalOcean App Platform UI
- Verify environment variables are correctly set
- Ensure DNS records are properly configured
- Check that the database is properly initialized

## Maintenance

- Monitor resource usage in the DigitalOcean dashboard
- Set up alerts for high CPU/memory usage
- Regularly update API keys and dependencies
