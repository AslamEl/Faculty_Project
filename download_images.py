import os
from bing_image_downloader import downloader

# --- The List of Celebrities ---

celebrity_men = [
    "Keanu Reeves", "Dwayne Johnson", "Chris Hemsworth", "Tom Hanks", "Leonardo DiCaprio",
    "Robert Downey Jr.", "Will Smith", "Cillian Murphy", "Ryan Reynolds", "Tom Cruise",
    "Brad Pitt", "Shah Rukh Khan", "Salman Khan", "Vijay", "Hrithik Roshan",
    "Allu Arjun", "Yash", "Mahela Jayawardene", "Kumar Sangakkara", "Lionel Messi",
    "Cristiano Ronaldo", "Denzel Washington", "Idris Elba", "Jackie Chan", "Michael B. Jordan"
]

celebrity_women = [
    "Emma Watson", "Scarlett Johansson", "Zendaya", "Margot Robbie", "Jennifer Lawrence",
    "Angelina Jolie", "Gal Gadot", "Anne Hathaway", "Priyanka Chopra", "Deepika Padukone",
    "Aishwarya Rai", "Alia Bhatt", "Katrina Kaif", "Jacqueline Fernandez", "Pooja Umashankar",
    "Rashmika Mandanna", "Nayanthara", "Serena Williams", "Taylor Swift", "Beyoncé",
    "Jennifer Aniston", "Sandra Bullock", "Natalie Portman", "Michelle Yeoh", "Charlize Theron"
]

all_celebrities = celebrity_men + celebrity_women

# This is the main folder for everything
base_output_dir = 'Celebrity_Album'

# --- The Download Loop ---

print(f"Starting download for {len(all_celebrities)} celebrities...")

for name in all_celebrities:
    # We add "face portrait" to the query to get better, clearer headshots
    query = f"{name} face portrait"

    # --- THIS IS THE FIX ---
    # Create the specific sub-folder path for this person
    # e.g., "Celebrity_Album/Keanu Reeves"
    person_output_dir = os.path.join(base_output_dir, name)
    # --- END OF FIX ---

    print(f"\nDownloading images for: {name} (Query: '{query}')")
    
    downloader.download(
        query=query,
        limit=20,  # Download 20 images, so we can delete bad ones and keep 5-10
        
        # Pass the CORRECT, specific path here
        output_dir=person_output_dir,
        
        # We removed the 'person_dir' argument which was causing the crash
        filter='photo',
        
        force_replace=False,
        timeout=60,
        verbose=True
    )

print("\n--- All downloads complete. ---")
print("IMPORTANT: Go to the 'Celebrity_Album' folder and manually clean the images.")