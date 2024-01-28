import streamlit as st
import requests

# Replace 'your_api_endpoint' with the actual API endpoint you want to use
API_ENDPOINT = 'https://dhruv4023-llmproject.hf.space/ask'
# API_ENDPOINT = "http://localhost:8000/ask"

def ask(question):
    # Send a POST request to the API
    data = {'q': question}
    response = requests.post(API_ENDPOINT, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        return response.json() #.get('answer', 'Error: No answer received from the API')
    else:
        return f"Error: Failed to get an answer. Status code: {response.status_code}"

def main():
    st.title("Indian Penal Code (IPC) Q&A")

    # st.image("https://www.google.com/imgres?imgurl=https%3A%2F%2Fthink360studio-media.s3.ap-south-1.amazonaws.com%2Fdownload%2Findia-flag-2021-wallpaper-1.png&tbnid=avMGtXMrg4Od7M&vet=12ahUKEwioxOX8nf-DAxWrmWMGHUWeCEoQMygLegUIARCNAQ..i&imgrefurl=https%3A%2F%2Fthink360studio.com%2Fblog%2Fbeautiful-india-flag-wallpapers-happy-independence-day&docid=NH42YRcPRUFRUM&w=1280&h=720&q=indian%20flag&ved=2ahUKEwioxOX8nf-DAxWrmWMGHUWeCEoQMygLegUIARCNAQ", caption="IPC Logo", use_column_width=True)

    # Create a stylish text input box with a button
    question = st.text_input("Ask a question about Indian Penal Code:", key="question_input")
    ask_button = st.button("Ask Question")

    if ask_button:
        # Call your ask function with the user's question
        answer = ask(question)

        # Display the answer with emojis and icons
        st.write(answer["result"])

if __name__ == "__main__":
    main()
