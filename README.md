# 🤖 GalacticView AI Agent

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-Package%20Manager-blueviolet?style=for-the-badge&logo=poetry&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black?style=for-the-badge)
![Model](https://img.shields.io/badge/Llama-3.1-orange?style=for-the-badge)

> A specialized AI service powered by **Llama 3.1** and **Ollama**. Designed to answer astronomy-related questions and serve as the intelligent backend for the [GalacticView](https://github.com/[YOUR_USERNAME]/GalacticView) web application.

---

## 📖 Overview

This repository houses the backend logic for the GalacticView AI assistant. It utilizes the **Llama 3.1** Large Language Model (running locally via Ollama) to process natural language queries about space, galaxies, stars, and NASA data.

The goal is to provide context-aware, scientific, and engaging answers to users exploring the GalacticView dashboard.

### 🛠 Tech Stack

* **Language:** Python
* **Dependency Management:** Poetry
* **Inference Engine:** Ollama (Local)
* **Model:** Llama 3.1

---

## ⚙️ Prerequisites & Setup

Before running the agent, ensure you have the following installed on your machine.

### 1. Install System Tools
* **Python:** Version >=3.12, <3.14, 
* **Poetry:** [Installation Guide](https://python-poetry.org/docs/#installation).

### 2. Setup Ollama (The Brain)
You need Ollama installed and the Llama 3.1 model downloaded locally.

1.  **Install Ollama:**
2.  **Pull the Model:**
    ```bash
    ollama pull llama3.1
    ```
3.  **Start the Server:** Ensure Ollama is running in the background (usually on port `11434`).

---

## 🚀 Installation & Usage

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/levilevente/GalacticView-agent.git
    cd GalacticView-agent
    ```

2.  **Install Python Dependencies**
    Use Poetry to install the environment defined in `pyproject.toml`.
    ```bash
    poetry install
    ```

3.  **Run the Agent**
    Enter the Poetry shell or run the script directly.
    ```bash
    # Run the main entry point
    poetry run python main.py
    ```

---

## 🧪 Example Usage

Once the script is running, the agent allows for Q&A interaction.

**Input:**
> "What is the difference between a Red Giant and a White Dwarf?"

**Agent Response (Llama 3.1):**
> "A Red Giant is a dying star in the final stages of stellar evolution... whereas a White Dwarf is what remains of a star like our Sun after it has exhausted its nuclear fuel..."

---

## 🔗 Integration Roadmap

This agent is designed to connect with the **GalacticView Frontend**.
* **Current Status:** Standalone CLI / Python Script.
* **Next Steps:** Wrap the agent in a REST API (FastAPI/Flask) to allow the React frontend to send requests and receive answers via HTTP.

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.