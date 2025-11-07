import os
import pickle
from deepface import DeepFace

# --- NEW: We must manually teach the script the gender of each celebrity ---
# I have sorted the 84 names from your log file.
male_list = [
    "Adam Driver", "Ajith Kumar", "Allu Arjun", "Benedict Cumberbatch", "Brad Pitt",
    "Chris Hemsworth", "Chris Pratt", "Cillian Murphy", "Cristiano Ronaldo", "David Beckham",
    "Denzel Washington", "Dwayne Johnson", "George Clooney", "Hrithik Roshan", "Idris Elba",
    "Jackie Chan", "Keanu Reeves", "Kumar Sangakkara", "Leonardo DiCaprio", "Lionel Messi",
    "Mads Mikkelsen", "Mahela Jayawardene", "Matt Damon", "Michael B. Jordan", "Morgan Freeman",
    "Prabhas", "Ram Charan", "Robert Downey Jr", "Roshan Ranawana", "Ryan Gosling",
    "Ryan Reynolds", "Salman Khan", "Samuel L. Jackson", "Sanath Gunathilake", "Shah Rukh Khan",
    "Suriya", "Timothee Chalamet", "Tom Cruise", "Tom Hanks", "Tom Holland", "Vijay",
    "Vikram", "Will Smith", "Yash"
]

female_list = [
    "Aishwarya Rai", "Alia Bhatt", "Angelina Jolie", "Anne Hathaway", "Anushka Shetty",
    "Anya Taylor-Joy", "Ariana Grande", "Beyonce", "Cate Blanchett", "Charlize Theron",
    "Deepika Padukone", "Dinakshie Priyasad", "Emily Blunt", "Emma Watson", "Gal Gadot",
    "Jacqueline Fernandez", "Jenna Ortega", "Jennifer Aniston", "Jennifer Lawrence",
    "Jessica Chastain", "Julia Roberts", "Kajol", "Kareena Kapoor", "Katrina Kaif",
    "Margot Robbie", "Meryl Streep", "Michelle Yeoh", "Natalie Portman", "Nayanthara",
    "Nicole Kidman", "Penelope Cruz", "Pooja Umashankar", "Priyanka Chopra", "Rashmika Mandanna",
    "Rihanna", "Salma Hayek", "Samantha Ruth Prabhu", "Sandra Bullock", "Scarlett Johansson",
    "Serena Williams", "Taylor Swift", "Tilda Swinton", "Trisha Krishnan", "Udari Warnakulasooriya",
    "Viola Davis", "Yashoda Wimaladharma", "Zendaya"
]

print("[INFO] Starting to encode faces from ALL albums...")
album_dirs = ["./Celebrity_Album", "./Celebrity_Album_Set2"]
model_name = "VGG-Face"
all_encodings = []

# Loop over each main album directory
for celebrity_dir in album_dirs:
    print(f"[INFO] Processing album: {celebrity_dir}")
    if not os.path.exists(celebrity_dir):
        print(f"[WARN] Directory not found, skipping: {celebrity_dir}")
        continue

    # Loop over each person in this album
    for person_name in os.listdir(celebrity_dir):
        person_dir = os.path.join(celebrity_dir, person_name)
        
        if not os.path.isdir(person_dir):
            continue

        # --- NEW: Determine gender ---
        gender = "Unknown"
        if person_name in male_list:
            gender = "Man"
        elif person_name in female_list:
            gender = "Woman"
        
        if gender == "Unknown":
            print(f"  [WARN] Skipping {person_name}: Not found in gender lists.")
            continue
            
        print(f"  [INFO] Processing: {person_name} (Gender: {gender})")
        
        # Loop over each image
        for image_name in os.listdir(person_dir):
            image_path = os.path.join(person_dir, image_name)
            
            if not image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            try:
                embedding_obj = DeepFace.represent(
                    img_path=image_path, 
                    model_name=model_name,
                    enforce_detection=True
                )
                embedding = embedding_obj[0]["embedding"]
                
                # --- NEW: Save gender in the database ---
                all_encodings.append({
                    "name": person_name,
                    "embedding": embedding,
                    "gender": gender
                })
                
            except Exception as e:
                print(f"    [ERROR] Could not process '{image_path}': {e}")

# --- NEW: Save to a new v2 file ---
output_file = "deepface_encodings_ALL_v2.pickle"
print(f"\n[INFO] Serializing {len(all_encodings)} total encodings...")
with open(output_file, "wb") as f:
    f.write(pickle.dumps(all_encodings))

print(f"[INFO] All faces encoded and saved to '{output_file}'")