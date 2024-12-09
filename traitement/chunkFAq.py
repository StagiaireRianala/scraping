import os


# Chunker le texte en sections gérables
def chunk_text(text, chunk_size=300):
    words = text.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

file_path = "Public/faq_scraping_result.txt"
text = load_text(file_path)
chunks = chunk_text(text, chunk_size=300)

print(f"Nombre de chunks : {len(chunks)}")
