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
- You can also choose which tool the agent should try first.
""")

# Replace this with your API key for local testing
openai.api_key = "sk-your-key-here"
# For deployment, use: openai.api_key = st.secrets.get("OPENAI_API_KEY")

# --- UI Controls with Session State ---
if 'prompt' not in st.session_state:
    st.session_state['prompt'] = ''

st.write("Or try one of these example prompts:")

# Example prompt options
example_prompts = {
    "Select an example...": "",
    "Calculator Example": "What is 17823 * 472?",
    "Search Example 1": "What is the capital of Australia?",
    "Search Example 2": "Who is the current prime minister of France?",
    "Search Example 3": "What’s the population of Paris?",
    "Search Example 4": "What’s the population of Tokyo?",
    "Search Example 5": "What is the currency of Japan?",
    "Search Example 6": "What is the currency of Croatia?",
    "Search Example 7": "What is the tallest mountain in the world?",
    "Search Example 8": "Who is the president of the United States?",
    "Multi-step Example 1": "What’s the weather in Paris tomorrow and what time is sunset?",
    "Multi-step Example 2": "What’s the weather in Tokyo tomorrow and when is sunset?"
}

selected_example = st.selectbox("Select an example prompt:", list(example_prompts.keys()))

if selected_example != "Select an example...":
    st.session_state['prompt'] = example_prompts[selected_example]

prompt = st.text_input("Enter your prompt:", value=st.session_state['prompt'])

use_calculator = st.checkbox("Use Calculator Tool")
use_search = st.checkbox("Use Search Tool")

# Tool prioritization dropdown
tool_priority = st.selectbox("Which tool should the agent try first?", ["Calculator", "Search"])

submit = st.button("Submit")

# --- Mock Tool Functions ---
def calculator_tool(expression):
    try:
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
    results = []

    # Flexible matching for multi-step example
    if "weather" in cleaned_query and "paris" in cleaned_query and "tomorrow" in cleaned_query:
        results.append("The weather in Paris tomorrow is Sunny, 29°C.")
    if "sunset" in cleaned_query and "paris" in cleaned_query and "tomorrow" in cleaned_query:
        results.append("The sunset time in Paris tomorrow is 9:58 PM.")

    if "weather" in cleaned_query and "tokyo" in cleaned_query and "tomorrow" in cleaned_query:
        results.append("The weather in Tokyo tomorrow is Cloudy, 21°C.")
    if "sunset" in cleaned_query and "tokyo" in cleaned_query and "tomorrow" in cleaned_query:
        results.append("The sunset time in Tokyo tomorrow is 6:48 PM.")

    # Exact or close matches
    if "capital of australia" in cleaned_query:
        results.append("The capital of Australia is Canberra.")

    if "prime minister of france" in cleaned_query:
        results.append("The current prime minister of France is François Bayrou.")

    if "population of paris" in cleaned_query:
        results.append("The population of Paris is approximately 2.1 million people.")

    if "population of tokyo" in cleaned_query:
        results.append("The population of Tokyo is approximately 14 million people.")

    if "currency of japan" in cleaned_query:
        results.append("The currency of Japan is the Japanese Yen.")

    if "currency of croatia" in cleaned_query:
        results.append("The currency of Croatia is the Euro.")

    if "tallest mountain in the world" in cleaned_query:
        results.append("The tallest mountain in the world is Mount Everest.")

    if "president of the united states" in cleaned_query:
        results.append("The current president of the United States is Donald Trump.")

    if results:
        return " ".join(results)
    else:
        return "No search results found."


# --- LLM + Tools Logic ---
if submit and prompt:
    with st.spinner("Generating response..."):
        tools_used = []
        reasoning_steps = []

        tool_order = []
        if use_calculator:
            tool_order.append("Calculator")
        if use_search:
            tool_order.append("Search")

        # Prioritize the user-selected tool
        if tool_priority in tool_order:
            tool_order.remove(tool_priority)
            tool_order.insert(0, tool_priority)

        for tool in tool_order:
            if tool == "Calculator":
                reasoning_steps.append("Calculator tool was enabled by the user and was prioritized.")
                result = calculator_tool(prompt)
                tools_used.append(f"Calculator result: {result}")
            elif tool == "Search":
                reasoning_steps.append("Search tool was enabled by the user and was prioritized.")
                result = search_tool(prompt)
                tools_used.append(f"Search result: {result}")

        if not tool_order:
            reasoning_steps.append("No tools were selected by the user. The agent will use only the LLM.")

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
            st.subheader("Tools Used by Agent (in order):")
            for tool_result in tools_used:
                st.write(f"- {tool_result}")
        else:
            st.write("No tools used.")
