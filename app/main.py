from graph import app
from graph_state import AgentState
from langchain_core.messages import HumanMessage

def main():
    """
    A simple command-line interface to interact with the LangGraph agent.
    """
    print("Welcome to the News Analysis Agent. Type 'exit' to quit.")
    
    # Initialize the state
    state = AgentState(messages=[], current_article=None)

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        # Append the new user message to the state
        state["messages"].append(HumanMessage(content=user_input))
        
        # Invoke the LangGraph app
        final_state = app.invoke(state)
        
        # Print the AI's response
        ai_response = final_state['messages'][-1].content
        print(f"Agent: {ai_response}")
        
        # Update the state for the next turn
        state = final_state

if __name__ == "__main__":
    main()
