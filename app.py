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
# For deployment, use: openai.api_key = st.secrets.get("OPENAI_API_KEY")
openai.api_key = st.secrets.get("OPENAI_API_KEY")

# --- UI Controls with Session State ---
if 'prompt' not in st.session_state:
    st.session_state['prompt'] = ''

st.write("Or try one of these example prompts:")

# Example prompts (keys and values are the same for better UX)
example_prompts = [
    "What is 17823 * 472?",
    "Who is the current prime minister of France?",
    "What is the inflation rate in France?",
    "What is the current unemployment rate in Germany?",
    "Who is the mayor of Paris?",
    "What is the latest exchange rate between the Euro and the US Dollar?",
    "What is the price of crude oil per barrel today?",
    "Who's going to win the dessert competition?",
    "Who are the stormtroopers?",
    "Who is Nithin?",
    "What is the currency of Croatia?",
    "Who is the president of the United States?",
    "What’s the weather in Paris tomorrow and what time is sunset?",
    "What’s the weather in Tokyo tomorrow and when is sunset?"
]

selected_example = st.selectbox("Select an example prompt:", ["Select an example..."] + example_prompts)

if selected_example != "Select an example...":
    st.session_state['prompt'] = selected_example

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
        results.append("The weather in Paris tomorrow is Mostly cloudy, 29°C.")
    if "sunset" in cleaned_query and "paris" in cleaned_query and "tomorrow" in cleaned_query:
        results.append("The sunset time in Paris tomorrow is 9:58 PM.")

    if "weather" in cleaned_query and "tokyo" in cleaned_query and "tomorrow" in cleaned_query:
        results.append("The weather in Tokyo tomorrow is Cloudy with periodic rain showers, 33°C.")
    if "sunset" in cleaned_query and "tokyo" in cleaned_query and "tomorrow" in cleaned_query:
        results.append("The sunset time in Tokyo tomorrow is 7:01 PM.")

    # Exact or close matches
    if "prime minister of france" in cleaned_query:
        results.append("The current prime minister of France is François Bayrou (not for long though).")

    if "population of paris" in cleaned_query:
        results.append("The population of Paris is approximately 2.1 million people.")

    if "currency of croatia" in cleaned_query:
        results.append("The currency of Croatia is the Euro.")

    if "tallest mountain in the world" in cleaned_query:
        results.append("The tallest mountain in the world is Mount Everest.")

    if "president of the united states" in cleaned_query:
        results.append("The current president of the United States is Donald Trump.")

    if "inflation rate in france" in cleaned_query:
        results.append("The annual inflation rate in France in June 2025 is 0.6%.")

    if "unemployment rate in germany" in cleaned_query:
        results.append("The unemployment rate in Germany as of June 2025 is 6.3%.")

    if "mayor of paris" in cleaned_query:
        results.append("The current mayor of Paris is Anne Hidalgo.")

    if "exchange rate" in cleaned_query and "euro" in cleaned_query and "us dollar" in cleaned_query:
        results.append("As of 25th June 2025, 1 Euro equals 1.16 US Dollars.")

    if "price of crude oil" in cleaned_query or "oil per barrel" in cleaned_query:
        results.append("As of 25th June 2025, the prices are WTI: 65.00 USD, Brent: 67.83 USD, Murban: 68.44 USD, Natural Gas: 3.53 USD.")

    if "dessert competition" in cleaned_query:
        results.append("Hard question! I'm completely impartial but my vote goes for Jaime.")

    if "stormtrooper" in cleaned_query:
        results.append("The stormtrooper, named after the Star Wars imperial soldiers, is the best DS team at Shift technology, especially the \"mini-stormtroopers based in Paris.\".")

    if "tallulah" in cleaned_query:
        results.append("Lead of the mini-stormtroopers, the fastest of runners, and has the hard task of having to deal with a bunch of crazy people in her team.")

    if "kevin" in cleaned_query:
        results.append("US-based mini-stormtrooper contributor, master of reinforcement learning and everything complex.")

    if "jaime" in cleaned_query:
        results.append("Tech lead, does not play with good music and animes, speaks multiple languages and is good at desserts.")

    if "aasim" in cleaned_query:
        results.append("Stormtrooper in the making, master of Mafia, be careful with him because he's not easy to outsmart.")

    if "avantika" in cleaned_query:
        results.append("Avantika is the smartest member of the mini-stormtroopers, moved from Nice to Paris recently because of how much the team needed her there.")

    if "bhumik" in cleaned_query:
        results.append("Master of self-control: one month without sugar and still alive.\nBook challenge: successfully avoided.")

    if "felipe" in cleaned_query:
        results.append("Felipe is a brilliant guy, feed bubble tea, meat and sugar and he should be functional.")

    if "gaetan" in cleaned_query:
        results.append("Member of the mini-stormtroopers, master of games, dessert and DS ops.")

    if "marius" in cleaned_query:
        results.append("Elite member of the mini-stormtroopers, currently in a Asia journey where he will gain insights that will revolutionize the team upon his return.")

    if "nithin" in cleaned_query:
        results.append("Dangerous stormtrooper, looks like a cinamon roll, could actually kill you.")

    if "ruining" in cleaned_query:
        results.append("Ruining is an elite member of the mini-stormtroopers. Master of POCs, IDN, cooking and your go-to guy to ask for advice of hidden gems about asian gastronomy in Paris.")


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
