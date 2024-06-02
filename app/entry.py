import streamlit as st
import random
import time
import re
from PIL import Image
import requests
from io import BytesIO

from app.main import invoke_llm
from rag_for_realestate import get_context

# Streamed response emulator

def context_formatter(context):
    exterior_image_links = []
    interior_image_links = []

    for image in context['exterior_image']:
        exterior_image_links.append(f"[exterior_image]({image})")

    for image in context['interior_image']:
        interior_image_links.append(f"[interior_image]({image})")
    
    formatted_context = f"""
    - Location: {context['state']} \n
    - Price: {context['price']} \n 
    - Bedrooms: {context['bed']} \n 
    - Bathrooms: {context['bath']} \n 
    - Acre Lot: {context['acre_lot']} \n 
    - Neighborhood Safety: {context['neighborhood_safety']} \n 
    - Elementary School Rating: {context['elementary_school_rating']} \n
    - Middle School Rating: {context['middle_school_rating']} \n
    - High School Rating: {context['high_school_rating']} \n 
    - Exterior Images: {' '.join(exterior_image_links)} \n
    - Interior Images: {' '.join(interior_image_links)} \n
    """
    # content = render_images(formatted_context)
    st.write_stream(stream_generator(formatted_context))

    return exterior_image_links, interior_image_links
    

def summary_formatter(context):
    formatted_summary = f"""
    House Location: {context['state']},
    Summary: {context['consolidated_text']}
    """
    return formatted_summary

    
def response_generator(prompt: str):
    context_json = get_context(prompt) or ""
    summaries = ""
    context = "Found the following properties that match your criteria"

    st.write_stream(stream_generator(context))

    exterior_image_links = []
    interior_image_links = []

    for doc in context_json:
        exterior_image_links, interior_image_links =  context_formatter(doc)
        summaries += summary_formatter(doc)

    response = invoke_llm(prompt, summaries, "best property")

    content = f"{" ".join(exterior_image_links)} {" ".join(interior_image_links)}"
    

    return content, response

def stream_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.01)


def render_images(content, columns=3):
    image_links = image_links = re.findall(r'(https?://images.unsplash.com/\S+\?[^)]+)', content)
    if image_links:
        image_data = []
        for link in image_links:
            response = requests.get(link)
            img = Image.open(BytesIO(response.content))
            image_data.append((img, f""))
        content = re.sub(r'(https?://images.unsplash.com/\S+\?[^)]+)', '', content)

        num_images = len(image_data)
        cols = st.columns(columns)
        for i, col in enumerate(cols):
            for j in range(i, num_images, columns):
                img, caption = image_data[j]
                col.image(img, caption=caption, use_column_width=True)

    return content

st.title("DreamHome.ai 🏠")

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
if prompt := st.chat_input("What do you want to find today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        content, response = response_generator(prompt=prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.html(response)
        render_images(content)
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Request a Tour"):
                st.write("Tour requested!")
        with col2:
            if st.button("❤️", help="Like"):
                st.write("You liked this!")
        with col3:
            if st.button("👎", help="Dislike"):
                st.write("You disliked this!")

