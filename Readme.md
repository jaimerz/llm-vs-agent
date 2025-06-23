# LLM vs Agent Sandbox

This project is a Streamlit-based sandbox that demonstrates the difference between using a plain LLM and an agent with tools like calculators and search capabilities.

---

## 🚀 Quick Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/llm-vs-agent.git
cd llm-vs-agent
````

### 2. Create and Activate Virtual Environment

```bash
# Create the virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

---

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

---

### 4. Configure OpenAI API Key

#### Option A: Local Testing

In `app.py`, temporarily add your API key:

```python
openai.api_key = "sk-your-api-key"
```

#### Option B: Streamlit Cloud Deployment

Add your API key to **Streamlit Cloud Secrets**:

```plaintext
OPENAI_API_KEY = sk-your-api-key
```

---

### 5. Run the App Locally

```bash
python -m streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`.

---

## 🌐 Deployment (Streamlit Cloud)

1. Push your project to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and click **New app**.
3. Connect your GitHub repo.
4. Add your OpenAI API key in **Secrets** (Settings > Secrets).
5. Click **Deploy** — you’ll get a shareable link.

---

## 🛠️ Key Features

* Toggle use of:

  * Calculator Tool
  * Search Tool (mocked)
* Compare LLM-only answers vs agent-augmented answers
* Visualize when tools are used

---

## ✨ Example Prompts to Try

* **Calculation:** `What is 45 * 78?`
* **Search:** `What is the capital of Australia?`
* **Multi-step:** `What’s the weather in Paris tomorrow and what time is sunset?`

---

## 📚 Notes

* This app uses mocked search results for simplicity.
* Each feature can be extended or replaced with live API calls if desired.

---

## 📄 License

MIT License

```