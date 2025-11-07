import streamlit as st
import cv2
import pickle
import numpy as np
from deepface import DeepFace
from scipy.spatial.distance import cosine
import os

# --- NEW: Set your minimum match requirement ---
SIMILARITY_THRESHOLD = 65.0 

# --- Helper function to find the celebrity's image file ---
def get_celebrity_image_path(name):
    for album_dir in ["./Celebrity_Album", "./Celebrity_Album_Set2"]:
        path = os.path.join(album_dir, name)
        if os.path.exists(path):
            try:
                for filename in os.listdir(path):
                     if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                        return os.path.join(path, filename)
            except Exception:
                pass
    return None

# --- Load and Cache the Database ---
@st.cache_data
def load_database():
    print("[INFO] Loading database... (This should only happen once)")
    try:
        with open("deepface_encodings_ALL_v2.pickle", "rb") as f:
            all_data = pickle.load(f)
        return all_data
    except FileNotFoundError:
        return None

# --- Main App Interface ---
st.set_page_config(layout="wide")
st.title("🧙‍♂️ Find Your Celebrity Twin! 🧙‍♀️")
st.write("Choose your filter, then take your photo using the camera button!")

# 1. Load the data
all_data = load_database()
if all_data is None:
    st.error("Database file (deepface_encodings_ALL_v2.pickle) not found. Please run the encode_ALL_faces.py script first.")
else:
    # 2. Add filters in a sidebar
    with st.sidebar:
        st.header("1. Setup Your Search")
        filter_mode = st.radio(
            "Show me matches for:",
            ("All", "Man", "Woman"),
            index=0 
        )
    
    st.header("2. Take Your Photo")

    # --- THIS IS THE KEY CHANGE ---
    # We replaced st.file_uploader with st.camera_input
    uploaded_file = st.camera_input(
        "Click here to open your camera and take a photo",
        help="Make sure you're in a well-lit room and facing the camera!"
    )
    # --- END OF CHANGE ---

    # 4. Filter the database
    known_names = []
    known_embeddings = []
    for data in all_data:
        if filter_mode == "All" or data.get("gender") == filter_mode:
            known_names.append(data["name"])
            known_embeddings.append(data["embedding"])

    # 5. Process the image AFTER it's captured
    if uploaded_file is not None:
        
        # The rest of the code is the same!
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        user_image = cv2.imdecode(file_bytes, 1)
        
        st.subheader("Your Photo:")
        st.image(user_image, channels="BGR", width=400)

        # 6. Run analysis on button click
        st.header("3. Find Your Match")
        if st.button("Analyze My Face!", type="primary"):
            
            with st.spinner("Analyzing your face..."):
                try:
                    # 1. Get user's face embedding
                    face_obj = DeepFace.represent(
                        img_path=user_image, 
                        model_name="VGG-Face", 
                        enforce_detection=True, 
                        detector_backend='opencv'
                    )
                    user_embedding = face_obj[0]["embedding"]

                    # 2. Compare to the database
                    distances = [cosine(user_embedding, celeb_embedding) for celeb_embedding in known_embeddings]
                    
                    best_match_index = np.argmin(distances)
                    best_match_name = known_names[best_match_index]
                    similarity_percent = (1 - distances[best_match_index]) * 100
                    
                    # 3. Check if the match is good enough
                    if similarity_percent >= SIMILARITY_THRESHOLD:
                        
                        celeb_path = get_celebrity_image_path(best_match_name)
                        celeb_image = cv2.imread(celeb_path)

                        st.success(f"🎉 Match Found! 🎉")
                        st.header(f"You look like {best_match_name}!")
                        st.subheader(f"Similarity Score: {similarity_percent:.1f}%")

                        col1, col2 = st.columns(2)
                        with col1:
                            st.image(user_image, caption="You", channels="BGR", use_column_width=True)
                        with col2:
                            st.image(celeb_image, caption=best_match_name, channels="BGR", use_column_width=True)
                    
                    else:
                        st.warning(f"No close match found!")
                        st.write(f"We found a similarity of {similarity_percent:.1f}%, which is below our {SIMILARITY_THRESHOLD}% threshold.")
                        st.write("Try a different photo or a clearer angle!")

                except ValueError as e:
                    st.error("We couldn't find a face in your photo. Please try a clearer, forward-facing picture.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")