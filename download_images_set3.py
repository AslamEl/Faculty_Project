import os
from bing_image_downloader import downloader

# --- The List of Celebrities (Set 3) ---

celebrity_men = [
    "Aaron Paul", "Akshay Kumar", "Amitabh Bachchan", "Andrew Garfield", "Andy Samberg",
    "Anthony Hopkins", "Antonio Banderas", "Ben Affleck", "Bruce Lee", "Bruce Willis",
    "Chiwetel Ejiofor", "Christian Bale", "Colin Farrell", "Daniel Craig", "Daniel Kaluuya",
    "Ewan McGregor", "Forest Whitaker", "Gerard Butler", "Hugh Jackman", "Jared Leto",
    "Jason Statham", "Javier Bardem", "Jeff Goldblum", "Jeremy Renner", "Joaquin Phoenix",
    "John Cena", "John Krasinski", "John Travolta", "Jude Law", "Karl Urban",
    "Liam Neeson", "Luke Evans", "Mark Wahlberg", "Martin Freeman", "Matthew McConaughey",
    "Michael Caine", "Michael Fassbender", "Oscar Isaac", "Pedro Pascal", "Robert Pattinson",
    "Rowan Atkinson", "Seth Rogen", "Simon Pegg", "Stanley Tucci", "Taika Waititi",
    "Tom Hiddleston", "Viggo Mortensen", "Vin Diesel", "Wentworth Miller", "Willem Dafoe"
]

celebrity_women = [
    "Adwoa Aboah", "Amanda Seyfried", "Amy Adams", "Ana de Armas", "Awkwafina",
    "Brie Larson", "Cameron Diaz", "Carey Mulligan", "Carrie-Anne Moss", "Dakota Johnson",
    "Diane Keaton", "Drew Barrymore", "Elisabeth Moss", "Elizabeth Olsen", "Elle Fanning",
    "Ellen DeGeneres", "Eva Mendes", "Gemma Chan", "Gwyneth Paltrow", "Halle Berry",
    "Helena Bonham Carter", "Hilary Swank", "Jamie Lee Curtis", "Jodie Foster", "Judi Dench",
    "Julianne Moore", "Kate Beckinsale", "Kate Hudson", "Kate Winslet", "Keira Knightley",
    "Kerry Washington", "Kristen Stewart", "Kristin Scott Thomas", "Lupita Nyong'o",
    "Maggie Smith", "Marion Cotillard", "Mila Kunis", "Millie Bobby Brown", "Mindy Kaling",
    "Naomi Scott", "Naomi Watts", "Olivia Colman", "Rachel McAdams", "Rachel Weisz",
    "Reese Witherspoon", "Saoirse Ronan", "Sigourney Weaver", "Sofía Vergara", "Uma Thurman",
    "Zoe Saldana"
]

all_celebrities = celebrity_men + celebrity_women

# --- We use a NEW folder name ---
base_output_dir = 'Celebrity_Album_Set3' 

# --- The Download Loop ---
print(f"Starting download for {len(all_celebrities)} celebrities...")

for name in all_celebrities:
    query = name
    print(f"\nDownloading images for: {name}")
    
    downloader.download(
        query=query,
        limit=15,
        output_dir=base_output_dir,
        filter='photo',
        force_replace=False,
        timeout=60,
        verbose=True
    )

print("\n--- All downloads complete. ---")
print(f"All images are saved in: '{base_output_dir}/[Celebrity Name]/'")
print("Please manually clean the folders before the next step.")