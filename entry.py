import streamlit as st
import pathlib

# Load CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Speak4Earth: Empowering the Future", layout="centered", initial_sidebar_state="expanded")

    load_css("styles.css")

        # Hero Image
    st.markdown(
        """
        <div class="hero-image">
            <img src="hero.png" alt="Hero Image">
        </div>
        """,
        unsafe_allow_html=True
    )


    # Title and Description
    st.title("Speak4Earth: Let's Empower the Future!", anchor="center")
    st.markdown("""
    Welcome to Speak4Earth, an innovative platform designed to educate and inspire action on environmental issues. Customize your report by selecting the options below.
    """)

    st.header("Let's generate your personalized earth report!")

    # Input Sections
    col1, col2 = st.columns([1, 5])

    with col1:
        # st.image("thumbnails/biodiversity.png", width=50)
        st.image("thumbnails/knowledge_level.png", width=50)
    with col2:
        domain = st.selectbox(
            "Select the Environmental Domain",
            ["Loss of Biodiversity", "Wildfires", "Drought", "Floods", "Tornadoes"]
        )

    col1, col2 = st.columns([1, 5])

    with col1:
        # st.image("thumbnails/location.png", width=50)
        st.image("thumbnails/knowledge_level.png", width=50)
    with col2:
        location = st.text_input("Enter the Geographic Location")

    col1, col2 = st.columns([1, 5])

    with col1:
        # st.image("thumbnails/age_group.png", width=50)
        st.image("thumbnails/knowledge_level.png", width=50)
    with col2:
        age_group = st.selectbox(
            "Select the Age Group",
            ["Young Children (5-8 years)", "Older Children (9-12 years)", "Teenagers (13-18 years)", "Adults (19-60 years)", "Seniors (60+ years)"]
        )

    col1, col2 = st.columns([1, 5])

    with col1:
        # st.image("thumbnails/format_preference.png", width=50)
        st.image("thumbnails/knowledge_level.png", width=50)
    with col2:
        format_preference = st.radio(
            "Preferred Format (Optional)",
            ["PDF", "Slides", "No Preference"],
            index=2
        )

    col1, col2 = st.columns([1, 5])

    with col1:
        # st.image("thumbnails/learning_style.png", width=50)
        st.image("thumbnails/knowledge_level.png", width=50)
    with col2:
        learning_style = st.radio(
            "Preferred Learning Style (Optional)",
            ["Visual", "Auditory", "Kinesthetic", "No Preference"],
            index=3
        )

    col1, col2 = st.columns([1, 5])

    with col1:
        st.image("thumbnails/knowledge_level.png", width=50)
    with col2:
        knowledge_level = st.select_slider(
            "Select Your Prior Climate Knowledge Level",
            options=["Beginner", "Intermediate", "Advanced"]
        )

    # Submit Button
    if st.button("Generate Report"):
        st.success("Your report is being generated with the following options:")
        st.write(f"**Environmental Domain:** {domain}")
        st.write(f"**Geographic Location:** {location}")
        st.write(f"**Age Group:** {age_group}")
        st.write(f"**Format Preference:** {format_preference}")
        st.write(f"**Learning Style:** {learning_style}")
        st.write(f"**Prior Climate Knowledge Level:** {knowledge_level}")

if __name__ == "__main__":
    main()

# import streamlit as st

# # Load CSS
# def load_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# def main():
#     st.set_page_config(page_title="EarthSense: Empowering the Future", layout="wide", initial_sidebar_state="expanded")

#     load_css("styles.css")

#     # Custom CSS for hero image opacity
#     st.markdown(
#         """
#         <style>
#         .hero-image {
#             position: relative;
#             text-align: center;
#             color: white;
#         }
#         .hero-image img {
#             width: 100%;
#             opacity: 0.2;
#         }
#         .grid-container {
#             display: grid;
#             grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
#             gap: 20px;
#             padding: 20px;
#         }
#         .grid-item {
#             background-color: #ffffff;
#             padding: 20px;
#             border-radius: 10px;
#             box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
#         }
#         </style>
#         """, 
#         unsafe_allow_html=True
#     )

#     # Hero Image
#     st.markdown(
#         """
#         <div class="hero-image">
#             <img src="path/to/hero_image.png" alt="Hero Image">
#         </div>
#         """,
#         unsafe_allow_html=True
#     )  # Replace with the actual path

#     # Title and Description
#     st.title("EarthSense: Empowering the Future")
#     st.markdown("""
#     Welcome to EarthSense, an innovative platform designed to educate and inspire action on environmental issues. Customize your report by selecting the options below.
#     """)

#     st.header("Customize Your Report")

#     # Grid Layout for Inputs
#     st.markdown('<div class="grid-container">', unsafe_allow_html=True)

#     # Climate Domain
#     st.markdown('<div class="grid-item">', unsafe_allow_html=True)
#     # st.image("thumbnails/climate_domain.png", width=50)  # Replace with actual path
#     st.image("thumbnails/knowledge_level.png", width=50)  # Replace with actual path
#     domain = st.selectbox(
#         "Select the Environmental Domain",
#         ["Loss of Biodiversity", "Wildfires", "Drought", "Floods", "Tornadoes"]
#     )
#     st.markdown('</div>', unsafe_allow_html=True)

#     # Geographic Location
#     st.markdown('<div class="grid-item">', unsafe_allow_html=True)
#     # st.image("thumbnails/geographic_location.png", width=50)  # Replace with actual path
#     st.image("thumbnails/knowledge_level.png", width=50)  # Replace with actual path
#     location = st.text_input("Enter the Geographic Location")
#     st.markdown('</div>', unsafe_allow_html=True)

#     # Age Group
#     st.markdown('<div class="grid-item">', unsafe_allow_html=True)
#     # st.image("thumbnails/age_group.png", width=50)  # Replace with actual path
#     st.image("thumbnails/knowledge_level.png", width=50)  # Replace with actual path
#     age_group = st.selectbox(
#         "Select the Age Group",
#         ["Young Children (5-8 years)", "Older Children (9-12 years)", "Teenagers (13-18 years)", "Adults (19-60 years)", "Seniors (60+ years)"]
#     )
#     st.markdown('</div>', unsafe_allow_html=True)

#     # Format Preference
#     st.markdown('<div class="grid-item">', unsafe_allow_html=True)
#     # st.image("thumbnails/format_preference.png", width=50)  # Replace with actual path
#     st.image("thumbnails/knowledge_level.png", width=50)  # Replace with actual path
#     format_preference = st.radio(
#         "Preferred Format (Optional)",
#         ["PDF", "Slides", "No Preference"],
#         index=2
#     )
#     st.markdown('</div>', unsafe_allow_html=True)

#     # Learning Style
#     st.markdown('<div class="grid-item">', unsafe_allow_html=True)
#     # st.image("thumbnails/learning_style.png", width=50)  # Replace with actual path
#     st.image("thumbnails/knowledge_level.png", width=50)  # Replace with actual path
#     learning_style = st.radio(
#         "Preferred Learning Style (Optional)",
#         ["Visual", "Auditory", "Kinesthetic", "No Preference"],
#         index=3
#     )
#     st.markdown('</div>', unsafe_allow_html=True)

#     # Prior Climate Knowledge Level
#     st.markdown('<div class="grid-item">', unsafe_allow_html=True)
#     st.image("thumbnails/knowledge_level.png", width=50)  # Replace with actual path
#     knowledge_level = st.select_slider(
#         "Select Your Prior Climate Knowledge Level",
#         options=["Beginner", "Intermediate", "Advanced"]
#     )
#     st.markdown('</div>', unsafe_allow_html=True)

#     st.markdown('</div>', unsafe_allow_html=True)

#     # Submit Button
#     if st.button("Generate Report"):
#         st.success("Your report is being generated with the following options:")
#         st.write(f"**Environmental Domain:** {domain}")
#         st.write(f"**Geographic Location:** {location}")
#         st.write(f"**Age Group:** {age_group}")
#         st.write(f"**Format Preference:** {format_preference}")
#         st.write(f"**Learning Style:** {learning_style}")
#         st.write(f"**Prior Climate Knowledge Level:** {knowledge_level}")

# if __name__ == "__main__":
#     main()
