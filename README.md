# News Agent

This project is a conversational AI agent that can fetch, analyze, and discuss news articles. It's built with FastAPI, LangChain, and LangGraph, and features a simple web interface for interaction.

## Features

*   **Conversational Interface:** Chat with the agent in natural language.
*   **News Fetching:** Ask the agent to fetch news articles on a specific topic.
*   **Article Analysis:** Request a detailed analysis of a fetched article, including named entity recognition, entity enrichment, and a generated analysis.
*   **Fake News Detection:** Verify the claims in a news article using a RAG pipeline with LangChain.
*   **YouTube Integration:** Fetch, transcribe, and summarize YouTube videos.
*   **Social Media Content Generation:** Generate social media posts from a given text.
*   **Modular and Extensible:** The agent's capabilities can be easily extended by adding new tools and services.

## Architecture

The project is composed of two main parts:

1.  **Backend:** A Python application built with FastAPI that serves the conversational agent. The agent itself is built with LangGraph, which orchestrates a graph of tools to handle user requests.
2.  **Frontend:** A Next.js application that provides a simple web interface for interacting with the agent.

The core of the backend is a LangGraph agent that uses a router to determine the user's intent and direct the conversation to the appropriate tool.

## Getting Started

### Prerequisites

*   Python 3.8+
*   Node.js and npm
*   An API key from [newsdata.io](https://newsdata.io/)
*   An API key from [SerpAPI](https://serpapi.com/)
*   An API key from [NewsAPI](https://newsapi.org/)
*   A Google API key with the YouTube Data API v3 enabled
*   A Hugging Face API key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/news-agent.git
    cd news-agent
    ```

2.  **Backend Setup:**
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

3.  **Frontend Setup:**
    ```bash
    cd ../agent_interface
    npm install
    ```

4.  **Configuration:**
    *   Create a `.env` file in the `backend` directory.
    *   Add your API keys to the `.env` file:
        ```
        NEWS_API_KEY=your_newsdata_api_key
        SERPAPI_API_KEY=your_serpapi_api_key
        NEWSAPI_KEY=your_newsapi_api_key
        YOUTUBE_API_KEY=your_youtube_api_key
        GEMINI_API_KEY=your_gemini_api_key
        HUGGINGFACE_API_KEY=your_huggingface_api_key
        ```

### Running the Application

1.  **Start the backend server:**
    ```bash
    cd backend
    uvicorn app.main:fastapi_app --host 0.0.0.0 --port 8000
    ```

2.  **Start the frontend development server:**
    ```bash
    cd ../agent_interface
    npm run dev
    ```

The application will be available at `http://localhost:3000`.

## Usage

You can interact with the agent by sending messages to the chat interface. Here are a few examples:

*   **Chat:**
    > "Hello, how are you?"

*   **Fetch News:**
    > "Fetch news about Tesla"

*   **Analyze Article:**
    > "Analyze the article"

## Tools

### Router Tool

The router tool is the entry point for all user messages. It uses a hybrid approach to routing, with a set of rules for common cases and a Gemma model as a fallback for more ambiguous inputs.

### Chat Tool

The chat tool handles general conversation and small talk. It's powered by a TinyLlama model, which is a lightweight and efficient model that's well-suited for this purpose.

### News Fetcher Tool

The news fetcher tool is responsible for fetching news articles from the [newsdata.io](https://newsdata.io/) API. It takes a topic as input and returns the full text of a relevant article.

### Analysis Tool

The analysis tool performs a detailed analysis of a fetched news article. It's a sophisticated tool that uses a combination of a BERT-based NER model, a RAG system with ChromaDB and Wikipedia, and a large language model to perform a detailed analysis of a news article.

## Services

### Content Processor

The content processor service provides functionality to extract the main content from a URL and summarize text using the Hugging Face Inference API.

### Deep Analyzer

The deep analyzer service is similar to the analysis tool, but it's designed to be initialized with pre-loaded models for better performance.

### Fake News Checker

The fake news checker service uses a RAG pipeline with LangChain to verify claims. It retrieves evidence from SerpAPI and NewsAPI, uses a FAISS vector store for semantic caching, and a Gemini model to generate a verdict.

### Model Loader

The model loader service is responsible for loading all the models used in the application.

### Social Poster

The social poster service is designed to generate social media posts from a given text. It uses a combination of NLP models to summarize the text, extract keywords, and determine the sentiment. It also includes functionality to generate an image using Stable Diffusion.

### YouTube Service

The YouTube service provides functionality to fetch YouTube videos based on interests, transcribe the audio of a video using Whisper, and summarize the transcript using a Gemini model.

## Models

This project uses several different models to power its various capabilities:

*   **Router Model:** A Gemma model is used to classify user intent and extract topics from user input.
*   **Chat Model:** A TinyLlama model is used to handle casual conversation.
*   **NER Model:** A BERT-based model is used to perform named entity recognition on news articles.
*   **Analysis LLM:** A large language model is used to generate a detailed analysis of a news article.
*   **Summarization Model:** A DistilBART model from Hugging Face is used to summarize text.
*   **Sentiment Analysis Model:** A Hugging Face model is used to determine the sentiment of a text.
*   **Keyword Extraction Model:** A KeyBERT model is used to extract keywords from a text.
*   **Image Generation Model:** A Stable Diffusion model is used to generate images.
*   **Transcription Model:** A Whisper model is used to transcribe audio.
*   **Verification Model:** A Gemini model is used to verify claims.
