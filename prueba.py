import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

print(os.path.dirname(os.path.abspath(__file__)))
print("---------------")
print(sys.path.append(os.path.join(os.path.dirname(SCRIPT_DIR), '../')))