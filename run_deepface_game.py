import cv2
import pickle
import numpy as np
from deepface import DeepFace
from scipy.spatial.distance import cosine
import os # We need 'os' to find the celebrity's photo file

print("[INFO] Loading 'VGG-Face' model...")
DeepFace.build_model("VGG-Face")
print("[INFO] Model loaded.")

print("[INFO] Loading ALL celebrity encodings...")
with open("deepface_encodings_ALL.pickle", "rb") as f:
    all_data = pickle.load(f)

known_names = [data["name"] for data in all_data]
known_embeddings = [data["embedding"] for data in all_data]

print(f"[INFO] Database of {len(known_names)} celebrities is ready.")
print("[INFO] Starting video stream...")
cap = cv2.VideoCapture(0)

SIMILARITY_THRESHOLD = 0.60 

# --- NEW: State variable to control the app flow ---
# 'live' = searching for faces
# 'paused' = showing the match
app_mode = 'live' 
visitor_photo = None
match_display_image = None
# --- END NEW ---


# --- NEW: Helper function to get the celebrity's image path ---
def get_celebrity_image_path(name):
    """Finds the first image for a given celebrity name in our albums."""
    # Check the first album
    path1 = os.path.join("./Celebrity_Album", name)
    if os.path.exists(path1):
        try:
            filename = os.listdir(path1)[0] # Get first image in folder
            return os.path.join(path1, filename)
        except Exception:
            pass # Folder might be empty

    # Check the second album
    path2 = os.path.join("./Celebrity_Album_Set2", name)
    if os.path.exists(path2):
        try:
            filename = os.listdir(path2)[0]
            return os.path.join(path2, filename)
        except Exception:
            pass
            
    return None # Return None if we can't find them

# --- NEW: Helper function to create the final side-by-side image ---
def create_match_display(visitor_img, celeb_name, celeb_img_path, similarity_percent):
    """Creates a single image showing the visitor and celebrity side-by-side."""
    
    # 1. Load the celebrity image
    if celeb_img_path:
        celeb_img = cv2.imread(celeb_img_path)
    else:
        # Create a black image if we failed to find one
        celeb_img = np.zeros((400, 400, 3), dtype="uint8")

    # 2. Resize both images to be the same height for stacking
    img_height = 400
    
    # Resize visitor photo
    h, w, _ = visitor_img.shape
    scale = img_height / h
    visitor_img_resized = cv2.resize(visitor_img, (int(w * scale), img_height))

    # Resize celebrity photo
    h, w, _ = celeb_img.shape
    scale = img_height / h
    celeb_img_resized = cv2.resize(celeb_img, (int(w * scale), img_height))

    # 3. Create text labels
    cv2.putText(visitor_img_resized, "You", (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    cv2.putText(celeb_img_resized, celeb_name, (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                
    # 4. Stack them horizontally
    combined_image = np.hstack([visitor_img_resized, celeb_img_resized])

    # 5. Add the match percentage at the bottom
    # Create a new black "footer"
    footer = np.zeros((100, combined_image.shape[1], 3), dtype="uint8")
    text = f"Match Found: {similarity_percent:.1f}% Similarity"
    cv2.putText(footer, text, (20, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

    # Stack the main image on top of the footer
    final_display = np.vstack([combined_image, footer])
    
    return final_display

# --- Main App Loop ---
while True:
    
    # --- Part 1: LIVE MODE ---
    if app_mode == 'live':
        ret, frame = cap.read()
        if not ret:
            break
        
        # We'll make a copy to draw on, and one to save later
        frame_display = frame.copy() 
        
        try:
            # Find all faces in the frame
            face_objs = DeepFace.represent(
                img_path=frame, 
                model_name="VGG-Face", 
                enforce_detection=False, 
                detector_backend='ssd' 
            )
            
            # --- NEW: Check if any face is found ---
            if len(face_objs) > 0:
                # We'll only process the first face we find
                face_obj = face_objs[0] 
                
                user_embedding = face_obj["embedding"]
                facial_area = face_obj["facial_area"]
                x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']
                
                # --- High-speed comparison ---
                distances = [cosine(user_embedding, celeb_embedding) for celeb_embedding in known_embeddings]
                
                best_match_index = np.argmin(distances)
                best_match_distance = distances[best_match_index]
                similarity = 1 - best_match_distance
                
                name = "Unknown"
                color = (0, 0, 255) # Red

                if similarity > SIMILARITY_THRESHOLD:
                    name = known_names[best_match_index]
                    color = (0, 255, 0) # Green
                    
                # Draw the box and label
                cv2.rectangle(frame_display, (x, y), (x + w, y + h), color, 2)
                text = f"{name} ({similarity * 100:.1f}%)"
                y_text = y - 10 if y - 10 > 10 else y + h + 20
                cv2.putText(frame_display, text, (x, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                
                # --- NEW: Save data for capture ---
                # Save the *clean* frame (no text) and the match details
                visitor_photo = frame 
                best_match_name = name
                best_match_similarity = similarity * 100

            else:
                # No face detected
                visitor_photo = None # Clear previous capture
                cv2.putText(frame_display, "Looking for a face...", (30, 80), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

        except Exception as e:
            pass # Continue to the next frame

        # Show the live feed
        cv2.imshow("Celebrity Look-Alike (Press SPACE to Capture, 'q' to quit)", frame_display)

    # --- Part 2: PAUSED MODE (Showing the Match) ---
    elif app_mode == 'paused':
        # Show the saved "match_display_image"
        # We do this in a loop so it stays on screen until the user resets
        cv2.imshow("Celebrity Look-Alike (Press 'r' to Reset, 'q' to quit)", match_display_image)

    # --- Part 3: KEYBOARD CONTROLS ---
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break # Quit the app
    
    elif key == 32: # SPACEBAR
        # Check if we are in 'live' mode and have a valid photo
        if app_mode == 'live' and visitor_photo is not None and best_match_name != "Unknown":
            print(f"Capture! Match: {best_match_name}")
            
            # 1. Find the celebrity's photo
            celeb_path = get_celebrity_image_path(best_match_name)
            
            # 2. Create the side-by-side display
            match_display_image = create_match_display(
                visitor_photo, 
                best_match_name, 
                celeb_path, 
                best_match_similarity
            )
            
            # 3. Save the visitor's photo (optional)
            cv2.imwrite("visitor_photo.jpg", visitor_photo)
            
            # 4. Switch to paused mode
            app_mode = 'paused'
            
            # Close the live window
            cv2.destroyWindow("Celebrity Look-Alike (Press SPACE to Capture, 'q' to quit)")

    elif key == ord('r'):
        # Reset the app back to 'live' mode
        if app_mode == 'paused':
            print("Resetting to live feed...")
            app_mode = 'live'
            # Close the results window
            cv2.destroyWindow("Celebrity Look-Alike (Press 'r' to Reset, 'q' to quit)")

# Clean up
print("[INFO] Cleaning up...")
cap.release()
cv2.destroyAllWindows()