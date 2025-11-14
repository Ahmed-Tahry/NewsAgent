# News Agent

This project is a conversational AI agent that can fetch, analyze, and discuss news articles. It's built with FastAPI, LangChain, and LangGraph, and features a simple web interface for interaction.

## Features

*   **Conversational Interface:** Chat with the agent in natural language.
*   **News Fetching:** Ask the agent to fetch news articles on a specific topic.
*   **Article Analysis:** Request a detailed analysis of a fetched article, including named entity recognition, entity enrichment, and a generated analysis.
*   **Modular and Extensible:** The agent's capabilities can be easily extended by adding new tools.

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
    *   Add your `newsdata.io` API key to the `.env` file:
        ```
        NEWS_API_KEY=your_api_key
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

## Models

This project uses several different models to power its various capabilities:

*   **Router Model:** A Gemma model is used to classify user intent and extract topics from user input.
*   **Chat Model:** A TinyLlama model is used to handle casual conversation.
*   **NER Model:** A BERT-based model is used to perform named entity recognition on news articles.
*   **Analysis LLM:** A large language model is used to generate a detailed analysis of a news article.
