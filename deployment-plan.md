# DigitalOcean App Platform Configuration

This document outlines the deployment configuration for the GenAI Marketing Webapp on DigitalOcean's App Platform.

## App Specification

We'll create a `.do/app.yaml` file to define the application components for DigitalOcean App Platform.

## Environment Variables

The following environment variables will be configured in the DigitalOcean App Platform:

- `DATABASE_URL`: Connection string for the database
- `SECRET_KEY`: Secret key for application security
- `OPENAI_API_KEY`: API key for OpenAI integration
- `ANTHROPIC_API_KEY`: API key for Anthropic Claude integration
- `GEMINI_API_KEY`: API key for Google Gemini integration
- `DEEPSEEK_API_KEY`: API key for DeepSeek integration
- `MANUS_API_KEY`: API key for Manus integration

## Domain Configuration

The application will be configured to use the custom domain:
- `marketinghub.adiance.com`

## Build and Run Commands

- Backend: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Frontend: `npm run build && serve -s build`

## Resource Allocation

- CPU-optimized instance
- Appropriate memory allocation for LLM processing
