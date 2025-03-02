import yaml

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

# Set persistent directory for ChromaDB from config
PERSIST_DIRECTORY = config["vector_db"]["persist_directory"]