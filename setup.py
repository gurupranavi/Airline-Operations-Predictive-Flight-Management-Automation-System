import os
import json

def setup():
    print("="*60)
    print("AIRLINE OPERATIONS SYSTEM SETUP")
    print("="*60)
    
    directories = ['logs', 'data', 'output/reports', 'modules']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    with open('modules/__init__.py', 'w') as f:
        f.write('# Airline Operations System Modules\n')
    
    print("\nSetup complete!")
    print("\nNext steps:")
    print("1. Copy all module files to 'modules' directory")
    print("2. Install dependencies: pip install faker")
    print("3. Run: python main.py")
    print("="*60)

if __name__ == "__main__":
    setup()