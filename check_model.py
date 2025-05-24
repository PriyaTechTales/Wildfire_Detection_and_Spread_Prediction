import os

# Get the absolute path to the model file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'best.pt')

print(f"Looking for model at: {MODEL_PATH}")
print(f"File exists: {os.path.exists(MODEL_PATH)}")

# Check if the file is in the parent directory
PARENT_DIR = os.path.dirname(BASE_DIR)
PARENT_MODEL_PATH = os.path.join(PARENT_DIR, 'best.pt')
print(f"Looking for model in parent directory: {PARENT_MODEL_PATH}")
print(f"File exists in parent: {os.path.exists(PARENT_MODEL_PATH)}")

# List files in the current directory
print("\nFiles in current directory:")
for file in os.listdir(BASE_DIR):
    print(f"- {file}")

# List files in the parent directory
print("\nFiles in parent directory:")
for file in os.listdir(PARENT_DIR):
    print(f"- {file}") 