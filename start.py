import subprocess
import sys

def install_requirements():
    """
    Install required packages by reading the `requirements.txt` file.
    """
    try:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Packages installed successfully.")
    except Exception as e:
        print(f"Error installing packages: {e}")
        sys.exit(1)

def run_streamlit_app():
    """
    Run the Streamlit application.
    """
    try:
        print("Starting Streamlit app...")
        subprocess.run(["streamlit", "run", "app.py"])  # Replace "app.py" with your app's filename.
    except Exception as e:
        print(f"Error running the app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Install requirements and run the app
    install_requirements()
    run_streamlit_app()
