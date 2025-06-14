# Project Documentation Agent System

A sophisticated, multi-agent system designed to automate software project documentation. It leverages a team of specialized AI agents to analyze a codebase, generate documentation, create architectural diagrams, and produce README files, all managed through an interactive web interface.

## 🚀 Overview

This project combines a powerful Python backend with a modern React frontend to provide a seamless documentation experience. At its core, a `ProjectDocumentationCoordinator` agent orchestrates a team of sub-agents, each specializing in a specific task.

### Key Features:
-   **Automated Code Analysis**: The `CodeReaderAgent` scans the project's file structure and content.
-   **Detailed Documentation**: The `DocumentationAgent` generates in-depth documentation from the analyzed code.
-   **Architectural Graphs**: The `GraphCreationAgent` produces visual diagrams of the project architecture.
-   **Interactive UI**: A React-based frontend allows users to easily interact with the agent system.

## 🛠️ Tech Stack

-   **Backend**: Python, FastAPI, Google Agent Development Kit (ADK), LiteLLM
-   **Frontend**: React, TypeScript, Vite, Tailwind CSS
-   **Package Management**: `uv` (Python), `yarn` / `npm` (Node.js)

## ⚙️ Installation & Setup

### Prerequisites
-   Python 3.12+ and `uv` (`pip install uv`)
-   Node.js and `yarn` or `npm`

### 1. Backend Setup

First, set up and run the Python backend.

```bash
# Install Python dependencies
uv sync
```

### 2. Frontend Setup

Next, set up the React frontend.

```bash
# 1. Navigate to the frontend directory
cd fe

# 2. Install Node.js dependencies
yarn install
# or
npm install
```

## ▶️ Terminal Usage


### 0. Activate venv

```bash
source .venv/bin/activate
```

### 1. Start prompting the Agent in terminal

```bash
python3 app_main.py
```

## ▶️ GUI Usage

To run the application, you need to start both the backend server and the frontend development server.

### 1. Start the Backend Server

From the project's **root directory**:

```bash
uvicorn api_server:app --reload
```
The API server will be running at `http://127.0.0.1:8000`.

### 2. Start the Frontend Server

In a **new terminal**, navigate to the `fe` directory:

```bash
# Navigate to the frontend directory
cd fe

# Start the development server
yarn dev
# or
npm run dev
```

The React application will be available in your browser at `http://localhost:5173` (or another port if 5173 is busy). You can now use the web interface to interact with the documentation agent system.
