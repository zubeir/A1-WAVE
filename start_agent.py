"""
A1-WAVE Dashboard Startup Script
Quick start script for the A1-WAVE dashboard and agent
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit', 'yfinance', 'pandas', 'numpy', 
        'requests', 'plotly', 'beautifulsoup4', 'feedparser', 'schedule'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing missing packages...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Packages installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run: pip install -r requirements.txt")
            return False
    
    print("✅ All dependencies are installed")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['data', 'exports', 'snapshots', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Directories created/verified")

def start_dashboard_only():
    """Start only the Streamlit dashboard"""
    print("🚀 Starting A1-WAVE Dashboard...")
    
    try:
        # Start Streamlit with port 7865 and external access
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "dashboard.py",
            "--server.port", "7865",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped")

def start_agent_mode():
    """Start the full agent with auto-refresh"""
    print("🤖 Starting A1-WAVE Agent (Auto-refresh mode)...")
    print("📊 Dashboard will be available at: http://localhost:7865")
    print("🌐 For external access, use your machine's IP address")
    print("🔄 Data will refresh every 2 hours")
    print("📝 Logs will be saved to logs/agent.log")
    print("\n⚠️  Press Ctrl+C to stop the agent")
    
    try:
        # Import and start the agent
        from agent import A1WaveAgent
        
        agent = A1WaveAgent()
        scheduler_thread = agent.start(start_dashboard=True)
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n👋 Agent stopped")
        if 'agent' in locals():
            agent.stop()

def show_menu():
    """Show the startup menu"""
    print("\n" + "="*60)
    print("🌊 A1-WAVE DASHBOARD - STARTUP MENU")
    print("="*60)
    print("1. Start Dashboard Only (Manual refresh)")
    print("2. Start Agent Mode (Auto-refresh every 2 hours)")
    print("3. Run Data Collection Once")
    print("4. Exit")
    print("="*60)

def run_data_collection():
    """Run data collection once"""
    print("🔄 Running data collection once...")
    
    try:
        from agent import A1WaveAgent
        agent = A1WaveAgent()
        data = agent.collect_data()
        
        if 'error' in data:
            print(f"❌ Data collection failed: {data['error']}")
        else:
            print("✅ Data collection completed successfully!")
            print(f"📁 Data saved to: data/latest_data.json")
            
            # Show summary
            for theme_name, theme_data in data.get('themes', {}).items():
                if 'analysis' in theme_data:
                    analysis = theme_data['analysis']
                    print(f"\n📊 {theme_name}:")
                    print(f"   🟢 Green: {len(analysis.get('GREEN', []))}")
                    print(f"   🟡 Yellow: {len(analysis.get('YELLOW', []))}")
                    print(f"   🔴 Red: {len(analysis.get('RED', []))}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main startup function"""
    print("🌊 A1-WAVE Dashboard Startup")
    print("Ride macro waves. Exit before they break.")
    
    # Check prerequisites
    if not check_python_version():
        return
    
    if not check_dependencies():
        return
    
    create_directories()
    
    # Command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['--dashboard', '-d']:
            start_dashboard_only()
            return
        elif arg in ['--agent', '-a']:
            start_agent_mode()
            return
        elif arg in ['--collect', '-c']:
            run_data_collection()
            return
        elif arg in ['--help', '-h']:
            print("\nUsage:")
            print("  python start_agent.py [option]")
            print("\nOptions:")
            print("  --dashboard, -d    Start dashboard only")
            print("  --agent, -a        Start agent with auto-refresh")
            print("  --collect, -c      Run data collection once")
            print("  --help, -h         Show this help")
            return
    
    # Interactive menu
    while True:
        show_menu()
        
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                start_dashboard_only()
                break
            elif choice == '2':
                start_agent_mode()
                break
            elif choice == '3':
                run_data_collection()
                input("\nPress Enter to continue...")
            elif choice == '4':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-4.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
