import streamlit as st
import openai

# --- Setup ---
st.title("LLM vs Agent Sandbox")

# Replace this with your API key for local testing
# In Streamlit Cloud, you'll store it in app secrets
#openai.api_key = st.secrets.get("OPENAI_API_KEY")
openai.api_key = "sk-your-key-here"

# --- UI Controls ---
st.write("Test how an agent uses tools vs a plain LLM.")

prompt = st.text_input("Enter your prompt:")

use_calculator = st.checkbox("Use Calculator Tool")
use_search = st.checkbox("Use Search Tool")

submit = st.button("Submit")

# --- Mock Tool Functions ---
def calculator_tool(expression):
    try:
        return str(eval(expression))
    except:
        return "Error in calculation."

def search_tool(query):
    mock_database = {
        "capital of australia": "Canberra",
        "weather in paris tomorrow": "Partly cloudy, 23°C",
        "sunset time in paris tomorrow": "9:58 PM"
    }
    return mock_database.get(query.lower(), "No search results found.")

# --- LLM + Tools Logic ---
if submit and prompt:
    with st.spinner("Generating response..."):
        tools_used = []

        if use_calculator and any(char.isdigit() for char in prompt):
            result = calculator_tool(prompt)
            tools_used.append(f"Calculator result: {result}")
        
        if use_search and ("capital" in prompt.lower() or "weather" in prompt.lower() or "sunset" in prompt.lower()):
            result = search_tool(prompt)
            tools_used.append(f"Search result: {result}")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        llm_response = response.choices[0].message.content

        st.subheader("LLM Response (without tools):")
        st.write(llm_response)

        if tools_used:
            st.subheader("Tools Used by Agent:")
            for tool_result in tools_used:
                st.write(f"- {tool_result}")
        else:
            st.write("No tools used.")
