import os
import pickle
from deepface import DeepFace

print("[INFO] Starting to encode faces from ALL albums...")

# --- KEY CHANGE ---
# List of all your celebrity folders
album_dirs = ["./Celebrity_Album", "./Celebrity_Album_Set2"]
# --- END CHANGE ---

model_name = "VGG-Face"
all_encodings = []

# Loop over each main album directory (Set 1, Set 2, etc.)
for celebrity_dir in album_dirs:
    print(f"[INFO] Processing album: {celebrity_dir}")
    if not os.path.exists(celebrity_dir):
        print(f"[WARN] Directory not found, skipping: {celebrity_dir}")
        continue

    # Loop over each person in this album
    for person_name in os.listdir(celebrity_dir):
        person_dir = os.path.join(celebrity_dir, person_name)
        
        # Ensure it's a directory
        if not os.path.isdir(person_dir):
            continue
            
        print(f"  [INFO] Processing: {person_name}")
        
        # Loop over each image of that person
        for image_name in os.listdir(person_dir):
            image_path = os.path.join(person_dir, image_name)
            
            # Check for valid image extensions
            if not image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                print(f"    [SKIP] '{image_name}' is not an image.")
                continue
                
            try:
                # Get the "secret code" (embedding)
                embedding_obj = DeepFace.represent(
                    img_path=image_path, 
                    model_name=model_name,
                    enforce_detection=True # Crash if no face is found
                )
                
                embedding = embedding_obj[0]["embedding"]
                
                # Store the embedding and the name
                all_encodings.append({
                    "name": person_name,
                    "embedding": embedding
                })
                
            except Exception as e:
                # This will catch errors if DeepFace can't find a face
                print(f"    [ERROR] Could not process '{image_path}': {e}")

# --- KEY CHANGE ---
# Save all combined data to a new "master" file
output_file = "deepface_encodings_ALL.pickle"
print(f"\n[INFO] Serializing {len(all_encodings)} total encodings...")
with open(output_file, "wb") as f:
    f.write(pickle.dumps(all_encodings))

print(f"[INFO] All faces from both albums encoded and saved to '{output_file}'")