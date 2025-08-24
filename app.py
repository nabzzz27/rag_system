import streamlit as st
import sys
import os

# Add the 'src' directory to the Python path to allow for module imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# It's important to import your rag_chain module AFTER updating the path
from rag_chain import create_rag_chain

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="Silat Rulebook Q&A",
    page_icon="🥋",
    layout="wide"
)

# --- Caching the RAG Chain ---
# Use st.cache_resource to load the model only once
@st.cache_resource
def load_rag_chain():
    """
    Loads the RAG chain and caches it for the entire session.
    This is a heavy operation and should only run once.
    """
    st.write("Loading RAG chain... This may take a moment.")
    try:
        chain = create_rag_chain()
        st.success("RAG chain loaded successfully!")
        return chain
    except Exception as e:
        st.error(f"Failed to load RAG chain: {e}")
        return None

# --- Main Application Logic ---
def main():
    st.title("🥋 Silat Rulebook Q&A System")
    st.markdown("""
    Ask a question about the Silat rulebook. The system will retrieve relevant information
    from the official document and generate a comprehensive answer.
    """)

    # Load the RAG chain from the cache
    rag_chain = load_rag_chain()

    if rag_chain is None:
        st.stop()

    # --- User Input and Response Handling ---
    st.sidebar.header("Controls")
    query = st.sidebar.text_area("Enter your question:", placeholder="e.g., What are the legal targets for an attack?")

    if st.sidebar.button("Get Answer"):
        if query:
            with st.spinner("Searching the rulebook and generating an answer..."):
                try:
                    response = rag_chain.invoke(query)
                    
                    st.markdown("## Answer")
                    st.markdown(response)
                    
                except Exception as e:
                    st.error(f"An error occurred while generating the answer: {e}")
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
