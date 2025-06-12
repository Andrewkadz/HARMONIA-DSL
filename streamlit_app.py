import streamlit as st
from ollama_agent import OllamaAgent
import json

# Initialize the agent
agent = OllamaAgent()

# Streamlit UI
def main():
    st.title("HΛRM AI Agent")
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        # Model selection
        model = st.selectbox(
            "Select Model",
            ["llama2", "mistral", "codellama", "mixtral"]
        )
        
        # Temperature slider
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1
        )
        
        # Context window
        context_window = st.slider(
            "Context Window",
            min_value=512,
            max_value=8192,
            value=4096,
            step=512
        )
        
        # Apply settings
        if st.button("Apply Settings"):
            agent.model = model
            # Update configuration
            st.success("Settings applied!")
    
    # Main content
    st.header("Query")
    
    # Query input
    query = st.text_area(
        "Enter your query",
        height=100
    )
    
    # Process query
    if st.button("Process"):
        if query:
            with st.spinner("Processing..."):
                response = agent.process_query(query)
                
                # Display response
                st.subheader("Response")
                st.json(response)
                
                # Display analysis
                if "analysis" in response:
                    st.subheader("Analysis")
                    st.json(response["analysis"])
                    
                # Display recommendations
                if "recommendations" in response:
                    st.subheader("Recommendations")
                    st.json(response["recommendations"])
        else:
            st.warning("Please enter a query")
    
    # File analysis
    st.header("File Analysis")
    
    # File upload
    uploaded_file = st.file_uploader("Upload a file to analyze")
    
    if uploaded_file is not None:
        # Save uploaded file
        file_path = f"uploaded_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        # Analyze file
        if st.button("Analyze File"):
            with st.spinner("Analyzing file..."):
                analysis = agent.analyze_file(file_path)
                
                # Display analysis
                st.subheader("File Analysis")
                st.json(analysis)

if __name__ == "__main__":
    main()
