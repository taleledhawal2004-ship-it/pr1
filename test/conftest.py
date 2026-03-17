import sys
import os

# Set the project root path manually
project_root = os.path.join(os.path.dirname(__file__), '..')
print(project_root)
# Add project root to sys.path
sys.path.append(project_root)
print(sys.path)