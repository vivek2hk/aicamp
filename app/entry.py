import streamlit as st
import random
import time
import re
from PIL import Image
import requests
from io import BytesIO

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?,Text in the middle https://realestateexposures.com/wp-content/uploads/2022/10/sue-3.jpg , https://realestateexposures.com/wp-content/uploads/2022/10/RandyG-5.jpg, https://realestateexposures.com/wp-content/uploads/2022/11/DSC09356.jpg",
        ]
    )

    return response

def stream_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


def render_images(content, columns=3):
    image_links = re.findall(r'(https?://\S+\.(?:jpg|png|gif))', content)
    if image_links:
        image_data = []
        for link in image_links:
            response = requests.get(link)
            img = Image.open(BytesIO(response.content))
            image_data.append((img, f"Image from {link}"))
        content = re.sub(r'(https?://\S+\.(?:jpg|png|gif))', '', content)

        num_images = len(image_data)
        cols = st.columns(columns)
        for i, col in enumerate(cols):
            for j in range(i, num_images, columns):
                img, caption = image_data[j]
                col.image(img, caption=caption, use_column_width=True)

    return content

st.title("Virtual Real Estate Agent")

# Sidebar for user preferences
preferences = st.sidebar.text_area("Enter your preferences for the house you're looking for (e.g., location, number of bedrooms, budget, etc.)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        content = message["content"]
        content = render_images(content)
        st.markdown(content)

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = "".join(response_generator())
        st.session_state.messages.append({"role": "assistant", "content": response})
        content = render_images(response)
        st.write_stream(stream_generator(content))