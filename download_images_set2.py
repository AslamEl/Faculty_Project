import os
from bing_image_downloader import downloader

# --- The List of Celebrities (Set 2) ---

celebrity_men = [
    "Ryan Gosling", "Matt Damon", "Mark Ruffalo", "George Clooney", "Samuel L. Jackson",
    "Morgan Freeman", "Johnny Depp", "Tom Holland", "Benedict Cumberbatch", "Ram Charan",
    "Jr. NTR", "Prabhas", "Ajith Kumar", "Suriya", "Vikram",
    "Roshan Ranawana", "Sanath Gunathilake", "David Beckham", "Neymar Jr.", "Timothée Chalamet",
    "Adam Driver", "Chris Pratt", "Idris Elba", "Channing Tatum", "Mads Mikkelsen"
]

celebrity_women = [
    "Emily Blunt", "Jessica Chastain", "Viola Davis", "Meryl Streep", "Julia Roberts",
    "Cate Blanchett", "Nicole Kidman", "Salma Hayek", "Penélope Cruz", "Kareena Kapoor",
    "Kajol", "Samantha Ruth Prabhu", "Anushka Shetty", "Trisha Krishnan", "Yashoda Wimaladharma",
    "Dinakshie Priyasad", "Udari Warnakulasooriya", "Rihanna", "Lady Gaga", "Ariana Grande",
    "Anya Taylor-Joy", "Florence Pugh", "Jenna Ortega", "Eva Green", "Tilda Swinton"
]

all_celebrities = celebrity_men + celebrity_women

# This is the main folder where all sub-folders will be created
base_output_dir = 'Celebrity_Album_Set2' 

# --- The Download Loop ---

print(f"Starting download for {len(all_celebrities)} celebrities...")

for name in all_celebrities:
    
    # --- THIS IS THE FIX ---
    # The query is JUST the name. This will become the folder name.
    query = name
    # --- END OF FIX ---

    print(f"\nDownloading images for: {name}")
    
    downloader.download(
        query=query,
        limit=15,
        
        # The output_dir is the PARENT folder
        output_dir=base_output_dir,
        
        # We still use this filter to avoid cartoons
        filter='photo',
        
        force_replace=False,
        timeout=60,
        verbose=True
    )

print("\n--- All downloads complete. ---")
print(f"All images are saved in: '{base_output_dir}/[Celebrity Name]/'")
print("Please manually clean the folders before the next step.")