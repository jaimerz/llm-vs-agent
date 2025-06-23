import streamlit as st
import openai
import re
from openai import OpenAI

# --- Setup ---
st.title("LLM vs Agent Sandbox")

st.write("""
Test how an agent uses tools vs a plain LLM.

- Enter your own prompt OR try the example prompts below.
- Toggle the tools to see how the response changes.
""")

# Replace this with your API key for local testing
openai.api_key = "sk-your-key-here"
# For deployment, use: openai.api_key = st.secrets.get("OPENAI_API_KEY")

# --- UI Controls with Session State ---
if 'prompt' not in st.session_state:
    st.session_state['prompt'] = ''

st.write("Or try one of these example prompts:")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Calculator Example"):
        st.session_state['prompt'] = "What is 17823 * 472?"

with col2:
    if st.button("Search Example"):
        st.session_state['prompt'] = "What is the capital of Australia?"

with col3:
    if st.button("Multi-step Example"):
        st.session_state['prompt'] = "What’s the weather in Paris tomorrow and what time is sunset?"

prompt = st.text_input("Enter your prompt:", value=st.session_state['prompt'])

use_calculator = st.checkbox("Use Calculator Tool")
use_search = st.checkbox("Use Search Tool")

submit = st.button("Submit")

# --- Mock Tool Functions ---
def calculator_tool(expression):
    try:
        # Extract math expression using regex
        match = re.search(r'(\d+\s*[\+\-\*/]\s*\d+)', expression)
        if match:
            calculation = match.group(1)
            return f"{calculation} = {eval(calculation)}"
        else:
            return "Calculation error: no valid math expression found."
    except:
        return "Calculation error."

def search_tool(query):
    cleaned_query = query.lower()

    if "capital of australia" in cleaned_query:
        return "Canberra"
    if "weather in paris" in cleaned_query:
        return "Sunny, 29°C"
    if "sunset time in paris" in cleaned_query:
        return "9:58 PM"
    if "prime minister of france" in cleaned_query:
        return "François Bayrou"

    return "No search results found."

# --- LLM + Tools Logic ---
if submit and prompt:
    with st.spinner("Generating response..."):
        tools_used = []
        reasoning_steps = []

        if use_calculator:
            reasoning_steps.append("Calculator tool was enabled by the user.")
            result = calculator_tool(prompt)
            tools_used.append(f"Calculator result: {result}")
        else:
            reasoning_steps.append("Calculator tool was not used.")

        if use_search:
            reasoning_steps.append("Search tool was enabled by the user.")
            result = search_tool(prompt)
            tools_used.append(f"Search result: {result}")
        else:
            reasoning_steps.append("Search tool was not used.")

        client = OpenAI(api_key=openai.api_key)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        llm_response = response.choices[0].message.content

        st.subheader("Agent Reasoning Steps:")
        for step in reasoning_steps:
            st.write(f"- {step}")

        st.subheader("LLM Response (without tools):")
        st.write(llm_response)

        if tools_used:
            st.subheader("Tools Used by Agent:")
            for tool_result in tools_used:
                st.write(f"- {tool_result}")
        else:
            st.write("No tools used.")
