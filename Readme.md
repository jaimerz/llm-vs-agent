# LLM vs Agent Sandbox

This project is a **Streamlit-based sandbox** that demonstrates the difference between using a plain LLM (Language Model) and an agent equipped with tools like a calculator or search capability.

The sandbox is interactive and allows you to:

* Compare LLM-only answers vs. agent-augmented answers.
* Toggle tools like calculator and search.
* Prioritize tool usage to simulate agent decision paths.
* Select from dynamic example prompts that showcase multi-step reasoning and real-time information retrieval.

---

## 🚀 Live Demo

👉 [Launch the app on Streamlit Cloud](https://your-streamlit-cloud-url-here)
*(Replace this link with your deployed URL)*

---

## ✨ Features

* 🔄 **Dropdown with example prompts** that participants can try instantly.
* 🛠️ **Calculator and Search Tool toggles** to control agent assistance.
* 🔀 **Tool prioritization selector** to define agent decision order.
* 🔍 **Search examples with up-to-date or uncommon information** to illustrate LLM limitations.
* 📜 **Agent reasoning steps** displayed to visualize the decision flow.

---

## 🛠️ Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/llm-vs-agent-sandbox.git
cd llm-vs-agent-sandbox
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

#### Option A: Local Testing

In your `app.py`, you can **temporarily hardcode your API key** (for local use only):

```python
openai.api_key = "sk-your-api-key"
```

#### Option B: Streamlit Cloud Deployment

Store your API key securely in **Streamlit Cloud Secrets**:

```plaintext
OPENAI_API_KEY = sk-your-api-key
```

In the code, use:

```python
openai.api_key = st.secrets.get("OPENAI_API_KEY")
```

---

## 🌐 Deployment

1. Push your project to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) → **New app.**
3. Connect your GitHub repo.
4. Configure your API key in **Settings → Secrets.**
5. Click **Deploy.**

---

## 🧪 Example Prompts to Try

| Prompt                                                               | Tool Required for Reliable Answer   |
| -------------------------------------------------------------------- | ----------------------------------- |
| What is 17823 \* 472?                                                | Calculator                          |
| Who is the current prime minister of France?                         | Search                              |
| What is the inflation rate in France?                                | Search                              |
| What is the current unemployment rate in Germany?                    | Search                              |
| Who is the mayor of Paris?                                           | Search                              |
| What is the latest exchange rate between the Euro and the US Dollar? | Search                              |
| What is the price of crude oil per barrel today?                     | Search                              |
| What is the currency of Croatia?                                     | LLM is unreliable, search preferred |
| Who is the president of the United States?                           | Search                              |
| What’s the weather in Paris tomorrow and what time is sunset?        | Multi-Step Search                   |
| What’s the weather in Tokyo tomorrow and when is sunset?             | Multi-Step Search                   |

---

## 📚 Notes

* All search results are **mocked** for demo purposes.
* The app demonstrates tool usage but does not query real APIs (you can extend this in future versions).
* The agent reasoning path is **user-controlled** to highlight decision-making and chaining.

---

## 📄 License

MIT License.
