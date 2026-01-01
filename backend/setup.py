#!/usr/bin/env python3
"""
Setup script for initial configuration of the Hybrid Chatbot System
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    """Print welcome header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}")
    print("=" * 60)
    print("   🤖 HYBRID CHATBOT SYSTEM - INITIAL SETUP 🤖")
    print("=" * 60)
    print(f"{Colors.ENDC}\n")

def print_step(step_num, message):
    """Print step message"""
    print(f"{Colors.GREEN}[Step {step_num}]{Colors.ENDC} {message}")

def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.ENDC}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}❌ {message}{Colors.ENDC}")

def check_python_version():
    """Check if Python version is 3.11+"""
    print_step(1, "Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print_error(f"Python 3.11+ required. You have {version.major}.{version.minor}")
        return False
    
    print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_virtual_environment():
    """Create virtual environment"""
    print_step(2, "Creating virtual environment...")
    
    if os.path.exists("venv"):
        response = input("Virtual environment already exists. Recreate? (y/n): ")
        if response.lower() != 'y':
            print("Skipping virtual environment creation")
            return True
        shutil.rmtree("venv")
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print_success("Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to create virtual environment: {e}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print_step(3, "Installing dependencies...")
    
    # Determine pip path
    pip_path = "./venv/Scripts/pip" if sys.platform == "win32" else "./venv/bin/pip"
    
    if not os.path.exists(pip_path):
        print_warning("Virtual environment not found. Using system pip.")
        pip_path = "pip"
    
    try:
        # Upgrade pip
        subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print_success("Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        return False

def setup_environment_file():
    """Setup .env file"""
    print_step(4, "Setting up environment file...")
    
    if os.path.exists(".env"):
        response = input(".env file already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Keeping existing .env file")
            return True
    
    try:
        shutil.copy(".env.example", ".env")
        print_success(".env file created from .env.example")
        
        # Ask for Google API key
        print(f"\n{Colors.YELLOW}Please configure your Google Gemini API key:{Colors.ENDC}")
        print("1. Get your API key from: https://makersuite.google.com/app/apikey")
        api_key = input("2. Enter your API key (or press Enter to configure later): ").strip()
        
        if api_key:
            # Update .env file with API key
            with open(".env", "r") as f:
                content = f.read()
            
            content = content.replace("your-gemini-api-key-here", api_key)
            
            with open(".env", "w") as f:
                f.write(content)
            
            print_success("API key configured")
        else:
            print_warning("Remember to add your API key to .env before running the app")
        
        return True
    except Exception as e:
        print_error(f"Failed to setup .env file: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print_step(5, "Creating directory structure...")
    
    directories = [
        "logs",
        "data/database",
        "data/embeddings",
        "data/vectorstore",
        "backups",
        "temp"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print_success("Directory structure created")
    return True

def check_docker():
    """Check if Docker is installed"""
    print_step(6, "Checking Docker installation...")
    
    try:
        result = subprocess.run(["docker", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"Docker found: {result.stdout.strip()}")
            
            # Check docker-compose
            result = subprocess.run(["docker-compose", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print_success(f"Docker Compose found: {result.stdout.strip()}")
            else:
                print_warning("Docker Compose not found")
        return True
    except FileNotFoundError:
        print_warning("Docker not found. Docker is optional but recommended for production.")
        return True

def populate_initial_data():
    """Populate initial data"""
    print_step(7, "Populating initial data...")
    
    response = input("Would you like to populate the database with sample documents? (y/n): ")
    if response.lower() != 'y':
        print("Skipping database population")
        return True
    
    # Use the appropriate Python path
    python_path = "./venv/Scripts/python" if sys.platform == "win32" else "./venv/bin/python"
    if not os.path.exists(python_path):
        python_path = sys.executable
    
    try:
        subprocess.run([python_path, "scripts/populate_db.py", "populate"], check=True)
        print_success("Database populated with documents")
        return True
    except subprocess.CalledProcessError as e:
        print_warning(f"Failed to populate database: {e}")
        print("You can populate it later with: python scripts/populate_db.py populate")
        return True

def run_initial_tests():
    """Run initial tests"""
    print_step(8, "Running initial tests...")
    
    response = input("Would you like to run tests to verify the setup? (y/n): ")
    if response.lower() != 'y':
        print("Skipping tests")
        return True
    
    python_path = "./venv/Scripts/python" if sys.platform == "win32" else "./venv/bin/python"
    if not os.path.exists(python_path):
        python_path = sys.executable
    
    try:
        subprocess.run([python_path, "-m", "pytest", "tests/unit", "-v"], check=False)
        print_success("Tests completed")
        return True
    except Exception as e:
        print_warning(f"Some tests failed: {e}")
        print("This is normal if the API key is not configured yet")
        return True

def print_next_steps():
    """Print next steps for the user"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}")
    print("=" * 60)
    print("   🎉 SETUP COMPLETE! 🎉")
    print("=" * 60)
    print(f"{Colors.ENDC}\n")
    
    print(f"{Colors.GREEN}Next steps:{Colors.ENDC}")
    print("\n1. Configure your API key in .env file (if not done)")
    print("   Edit .env and add your Google Gemini API key")
    
    print("\n2. Start the application:")
    print("   With Flask (default):")
    print(f"   {Colors.YELLOW}python main.py{Colors.ENDC}")
    print("   With FastAPI:")
    print(f"   {Colors.YELLOW}USE_FASTAPI=true python main.py{Colors.ENDC}")
    
    print("\n3. Access the application:")
    print(f"   Chat API: {Colors.BLUE}http://localhost:5000/api/chat{Colors.ENDC}")
    print(f"   Dashboard: {Colors.BLUE}http://localhost:5000/api/monitoring/dashboard{Colors.ENDC}")
    
    print("\n4. For Docker deployment:")
    print(f"   {Colors.YELLOW}docker-compose up -d{Colors.ENDC}")
    
    print(f"\n{Colors.GREEN}Useful commands:{Colors.ENDC}")
    print("   make help           - Show all available commands")
    print("   make run           - Start the application")
    print("   make test          - Run tests")
    print("   make populate      - Populate database")
    print("   make health        - Check system health")
    
    print(f"\n{Colors.BLUE}Documentation:{Colors.ENDC}")
    print("   See README.md for detailed documentation")
    print("   API docs (FastAPI): http://localhost:8000/docs")
    
    print(f"\n{Colors.GREEN}Happy coding! 🚀{Colors.ENDC}\n")

def main():
    """Main setup function"""
    print_header()
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Creating virtual environment", create_virtual_environment),
        ("Installing dependencies", install_dependencies),
        ("Setting up environment", setup_environment_file),
        ("Creating directories", create_directories),
        ("Checking Docker", check_docker),
        ("Populating data", populate_initial_data),
        ("Running tests", run_initial_tests)
    ]
    
    failed = False
    for i, (description, func) in enumerate(steps, 1):
        if not func():
            print_error(f"Setup failed at step {i}: {description}")
            failed = True
            break
    
    if not failed:
        print_next_steps()
        return 0
    else:
        print(f"\n{Colors.RED}Setup incomplete. Please fix the errors and try again.{Colors.ENDC}")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Setup interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
