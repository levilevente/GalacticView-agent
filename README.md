# 🤖 GalacticView AI Agent

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-Package%20Manager-blueviolet?style=for-the-badge&logo=poetry&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Fast%20Inference-f55036?style=for-the-badge)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Orchestration-1c2c4c?style=for-the-badge)
![Tavily](https://img.shields.io/badge/Tavily-Search%20Tool-000000?style=for-the-badge)

> A specialized AI service powered by **Groq** (Llama 3.1) and **LangGraph**. Designed to answer astronomy-related questions with real-time web search capabilities using **Tavily**.

---

## 📖 Overview

This repository houses the intelligent backend for the [GalacticView](https://github.com/levilevente/GalacticView) ecosystem. 

Unlike standard chatbots, this agent is built using **LangGraph**, allowing it to perform complex reasoning loops. It leverages **Groq** for ultra-fast Llama 3.1 inference and utilizes **Tavily** to search the internet for real-time astronomical data and news, ensuring answers are not limited to the model's training cutoff.

### 🛠 Tech Stack

* **Language:** Python
* **Orchestration:** LangGraph (LangChain)
* **Inference Engine:** Groq API
* **Model:** Llama 3.1 (via Groq)
* **Tools:** Tavily Search API
* **Dependency Management:** Poetry

---

## ⚙️ Prerequisites & Setup

Before running the agent, ensure you have the necessary tools and API keys.

### 1. Install System Tools
* **Python:** Version >=3.12, <3.14
* **Poetry:** [Installation Guide](https://python-poetry.org/docs/#installation).

### 2. Obtain API Keys
Since this agent runs on the cloud, you need keys for the inference engine and the search tool:

* **Groq API Key:** Sign up at [console.groq.com](https://console.groq.com) to use Llama 3.1.
* **Tavily API Key:** Sign up at [tavily.com](https://tavily.com) to enable internet search capabilities.

---

## 🚀 Installation & Usage

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/levilevente/GalacticView-agent.git](https://github.com/levilevente/GalacticView-agent.git)
    cd GalacticView-agent
    ```

2.  **Install Python Dependencies**
    Use Poetry to install the environment defined in `pyproject.toml`.
    ```bash
    poetry install
    ```

3.  **Configure Environment Variables**
    Create a `.env` file in the root directory and add your keys:
    ```bash
    # .env file content
    GROQ_API_KEY=gsk_your_groq_key_here
    TAVILY_API_KEY=tvly-your_tavily_key_here
    MODEL_NAME=llama-3.1
    LLM_LOCAL=False #LLM_LOCAL=True in case you have a local llama3.1 running.
    ```

    

4.  **Run the Agent**
    Enter the Poetry shell or run the script directly.
    ```bash
    # Run the main entry point
    poetry run galacticview
    ```

---

## 🧪 Example Usage

Once running, the agent can answer static questions or perform research.

**Input:**
> "What is the latest news about the Artemis mission?"

**Agent Logic:**
1.  *LangGraph* detects the need for recent information.
2.  Calls *Tavily* to search the web for "latest Artemis mission updates".
3.  *Groq (Llama 3.1)* synthesizes the search results.

**Agent Response:**
```json
{
  "content": "The Artemis mission has been delayed due to damage found to the heat shield of the uncrewed Orion capsule. Artemis 2 remains on track for late 2024, but Artemis 3 has been pushed back to mid-2027.",
  "key_metrics": [
    "Artemis 2: late 2024",
    "Artemis 3: mid-2027"
  ],
  "title": "Artemis Mission Delay"
}
```


---

## 🔗 Integration Roadmap

This agent is designed to connect with the **GalacticView Frontend**.
* **Current Status:** CLI-based Agent with Search Tools.
* **Next Steps:** Wrap the LangGraph workflow in a REST API (FastAPI) to allow the React frontend to send requests and receive streaming answers.

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.