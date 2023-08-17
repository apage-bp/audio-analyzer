import streamlit as st
import modal
import json
import os

def main():
    # CSS Styles
    st.markdown("""
        <style>
            body {
                background: linear-gradient(45deg, #f3ec78, #af4261);
                font-family: 'Arial', sans-serif;
            }
            h1, h2, h3 {
                color: #ffffff;
            }
            .stButton>button {
                background-color: #8e44ad;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 10px 25px;
                font-size: 1em;
                box-shadow: 0px 0px 15px rgba(0,0,0,0.2);
            }
            .stButton>button:hover {
                background-color: #682773;
            }
            .stMarkdown p {
                margin-bottom: 15px;
                color: #ffffff;
            }
            .stSidebar {
                background-color: #ffffff;
                border-radius: 0 15px 15px 0;
            }
            .stTextInput input[type="text"] {
                padding: 10px 15px;
                border-radius: 15px;
                border: 2px solid #8e44ad;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("Newsletter Dashboard")

    available_podcast_info = create_dict_from_json_files('.')

    # Left section - Input fields
    st.sidebar.header("Podcast RSS Feeds")

    # Dropdown box
    st.sidebar.subheader("Available Podcasts Feeds")
    selected_podcast = st.sidebar.selectbox("Select Podcast", options=available_podcast_info.keys())

    if selected_podcast:
        podcast_info = available_podcast_info[selected_podcast]
        display_podcast_info(podcast_info)
    
    # User Input box
    st.sidebar.subheader("Add and Process New Podcast Feed")
    url = st.sidebar.text_input("Link to RSS Feed")
    process_button = st.sidebar.button("Process Podcast Feed")
    st.sidebar.markdown("**Note**: Podcast processing can take upto 5 mins, please be patient.")

    if process_button:

        # Call the function to process the URLs and retrieve podcast guest information
        podcast_info = process_podcast_info(url)

        # Right section - Newsletter content
        st.header("Newsletter Content")

        # Display the podcast title
        st.subheader("Episode Title")
        st.write(podcast_info['podcast_details']['episode_title'])

        # Display the podcast summary and the cover image in a side-by-side layout
        col1, col2 = st.columns([7, 3])

        with col1:
            # Display the podcast episode summary
            st.subheader("Podcast Episode Summary")
            st.write(podcast_info['podcast_summary'])

        with col2:
            st.image(podcast_info['podcast_details']['episode_image'], caption="Podcast Cover", width=300, use_column_width=True)

        # Display the podcast guest and their details in a side-by-side layout
        col3, col4 = st.columns([3, 7])

        with col3:
            st.subheader("Podcast Guest")
            st.write(podcast_info['podcast_guest']['name'])

        with col4:
            st.subheader("Podcast Guest Details")
            st.write(podcast_info["podcast_guest"]['summary'])

        # Display the five key moments
        st.subheader("Key Moments")
        key_moments = podcast_info['podcast_highlights']
        for moment in key_moments.split('\n'):
            st.markdown(
                f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)

def display_podcast_info(podcast_info):
    # Right section - Newsletter content
    st.header("Newsletter Content")
    st.subheader("Episode Title")
    st.write(podcast_info['podcast_details']['episode_title'])

    # Display the podcast summary and the cover image in a side-by-side layout
    col1, col2 = st.columns([7, 3])
    with col1:
        st.subheader("Podcast Episode Summary")
        st.write(podcast_info['podcast_summary'])
    with col2:
        st.image(podcast_info['podcast_details']['episode_image'], caption="Podcast Cover", width=300, use_column_width=True)

    # Display the podcast guest and their details in a side-by-side layout
    col3, col4 = st.columns([3, 7])
    with col3:
        st.subheader("Podcast Guest")
        st.write(podcast_info['podcast_guest']['name'])
    with col4:
        st.subheader("Podcast Guest Details")
        st.write(podcast_info["podcast_guest"]['summary'])

    # Display the five key moments
    st.subheader("Key Moments")
    key_moments = podcast_info['podcast_highlights']
    for moment in key_moments.split('\n'):
        st.markdown(
            f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)

def create_dict_from_json_files(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    data_dict = {}

    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            podcast_info = json.load(file)
            podcast_name = podcast_info['podcast_details']['podcast_title']
            # Process the file data as needed
            data_dict[podcast_name] = podcast_info

    return data_dict

def process_podcast_info(url):
    f = modal.Function.lookup("corise-podcast-project", "process_podcast")
    output = f.call(url, '/content/podcast/')
    return output

if __name__ == '__main__':
    main()
