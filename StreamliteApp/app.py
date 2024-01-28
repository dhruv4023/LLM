import streamlit as st
import requests
from RetrivalQAModel import RetrivalQAModel 
# Replace 'your_api_endpoint' with the actual API endpoint you want to use
API_ENDPOINT = 'http://127.0.0.1:8000/ask'

# Example usage:
RetrivalQAModel.files = ["IPC_186045.pdf"]

model = RetrivalQAModel()

def main():
    st.title("Indian Penal Code (IPC) Q&A")

    # st.image("indian_penal_code.jpg", caption="IPC Logo", use_column_width=True)

    # Create a stylish text input box with a button
    question = st.text_input("Ask a question about Indian Penal Code:", key="question_input")
    ask_button = st.button("Ask Question")

    if ask_button:
        answer = model.ask_question(question)

        # Display the answer with emojis and icons
        st.write(answer)

    # # Add some additional information or resources
    # st.markdown("### Additional Resources")
    # st.markdown("📚 [Indian Penal Code (IPC)](https://indiankanoon.org/doc/270187/)")
    # st.markdown("📖 [Code of Criminal Procedure (CrPC)](https://indiankanoon.org/doc/625254/)")
    # st.markdown("🔍 [Legal Terms Glossary](https://www.latestlaws.com/glossary/)")

if __name__ == "__main__":
    main()
