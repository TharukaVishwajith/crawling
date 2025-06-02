"""
Programmatic runner for E-Commerce Analytics Automation
Runs the main extraction script using subprocess for better isolation
"""
import subprocess
import sys
import os
import time
from pathlib import Path

def run_extraction_programmatically(visible=True, custom_url=None):
    """
    Run the extraction command programmatically using subprocess
    
    Args:
        visible (bool): Whether to run browser in visible mode
        custom_url (str, optional): Custom URL to extract from
    
    Returns:
        tuple: (success: bool, stdout: str, stderr: str)
    """
    try:
        # Build command arguments
        cmd_args = [sys.executable, "main.py", "--extract-url"]
        
        # Add custom URL if provided
        if custom_url:
            cmd_args.append(custom_url)
        
        # Add visible flag if requested
        if visible:
            cmd_args.append("--visible")
        
        print("🚀 Starting E-Commerce Analytics Extraction...")
        print(f"📍 Working directory: {os.getcwd()}")
        print(f"🔧 Command: {' '.join(cmd_args)}")
        print(f"🖥️  Browser mode: {'Visible' if visible else 'Headless'}")
        
        if custom_url:
            print(f"🌐 Custom URL: {custom_url}")
        
        print("-" * 60)
        
        # Record start time
        start_time = time.time()
        
        # Run the command
        result = subprocess.run(
            cmd_args,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        print(f"\n⏱️  Execution completed in {execution_time:.2f} seconds")
        print(f"🏁 Return code: {result.returncode}")
        print("-" * 60)
        
        # Print output
        if result.stdout:
            print("📤 STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("⚠️  STDERR:")
            print(result.stderr)
        
        # Determine success
        success = result.returncode == 0
        
        if success:
            print("\n✅ Extraction completed successfully!")
        else:
            print(f"\n❌ Extraction failed with return code: {result.returncode}")
        
        return success, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        print("\n⏰ Process timed out after 5 minutes")
        return False, "", "Process timed out"
    except Exception as e:
        print(f"\n💥 Error running command: {e}")
        return False, "", str(e)

def run_with_default_settings():
    """Run extraction with default settings (visible mode, default URL)"""
    return run_extraction_programmatically(visible=True)

def run_headless():
    """Run extraction in headless mode"""
    return run_extraction_programmatically(visible=False)

def run_with_custom_url(url):
    """Run extraction with a custom URL"""
    return run_extraction_programmatically(visible=True, custom_url=url)

def check_project_files():
    """Check if required project files exist"""
    required_files = ["main.py", "browser_utils.py", "config.py"]
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required project files found")
    return True

def main():
    """Main function with interactive options"""
    print("🔍 E-Commerce Analytics Automation Runner")
    print("=" * 50)
    
    # Check project files first
    if not check_project_files():
        return
    
    # Example usage patterns
    print("\n📋 Available options:")
    print("1. Run with default settings (visible, default URL)")
    print("2. Run in headless mode")
    print("3. Run with custom URL")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                print("\n🚀 Running with default settings...")
                success, stdout, stderr = run_with_default_settings()
                break
                
            elif choice == "2":
                print("\n🚀 Running in headless mode...")
                success, stdout, stderr = run_headless()
                break
                
            elif choice == "3":
                url = input("Enter custom URL: ").strip()
                if url:
                    print(f"\n🚀 Running with custom URL: {url}")
                    success, stdout, stderr = run_with_custom_url(url)
                    break
                else:
                    print("❌ Please enter a valid URL")
                    
            elif choice == "4":
                print("👋 Goodbye!")
                return
                
            else:
                print("❌ Invalid choice. Please enter 1-4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            return
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Quick run example - just run with default settings
    print("🚀 Quick Run: E-Commerce Analytics Extraction")
    print("Running with default settings (visible mode)...")
    
    if check_project_files():
        success, stdout, stderr = run_extraction_programmatically(visible=True)
        
        if success:
            print("\n🎉 All done! Check the output above for results.")
        else:
            print("\n💥 Something went wrong. Check the error messages above.")
    
    # Uncomment the line below if you want interactive mode instead
    # main() 