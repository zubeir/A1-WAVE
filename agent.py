"""
A1-WAVE Agent - Auto-refresh service
Runs in background and refreshes dashboard data every 2 hours
"""

import schedule
import time
import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List
import requests
from threading import Thread
import subprocess
import sys

from analytics import Analytics
from config import THEMES, DEFAULT_SETTINGS

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class A1WaveAgent:
    def __init__(self):
        self.analytics = Analytics()
        self.running = False
        self.dashboard_url = "http://localhost:7865"  # Updated to port 7865
        self.data_dir = "data"
        self.snapshots_dir = "snapshots"
        
        # Create directories
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.snapshots_dir, exist_ok=True)
        os.makedirs("logs", exist_ok=True)
    
    def collect_data(self) -> Dict:
        """Collect all dashboard data"""
        try:
            logger.info("Starting data collection...")
            
            all_data = {
                'timestamp': datetime.now().isoformat(),
                'themes': {}
            }
            
            # Collect data for each theme
            for theme_name, theme_info in THEMES.items():
                logger.info(f"Analyzing theme: {theme_name}")
                
                try:
                    # Analyze theme
                    theme_analysis = self.analytics.analyze_theme(theme_info['tickers'])
                    
                    # Get macro analysis
                    macro_analysis = self.analytics.get_macro_analysis()
                    
                    all_data['themes'][theme_name] = {
                        'theme_info': theme_info,
                        'analysis': theme_analysis,
                        'macro': macro_analysis,
                        'collected_at': datetime.now().isoformat()
                    }
                    
                    logger.info(f"Successfully analyzed {theme_name}: "
                              f"Green={len(theme_analysis.get('GREEN', []))}, "
                              f"Yellow={len(theme_analysis.get('YELLOW', []))}, "
                              f"Red={len(theme_analysis.get('RED', []))}")
                    
                except Exception as e:
                    logger.error(f"Error analyzing theme {theme_name}: {e}")
                    all_data['themes'][theme_name] = {
                        'error': str(e),
                        'collected_at': datetime.now().isoformat()
                    }
            
            # Save latest data
            latest_file = os.path.join(self.data_dir, 'latest_data.json')
            with open(latest_file, 'w') as f:
                json.dump(all_data, f, indent=2, default=str)
            
            # Create timestamped snapshot
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            snapshot_file = os.path.join(self.snapshots_dir, f'snapshot_{timestamp}.json')
            with open(snapshot_file, 'w') as f:
                json.dump(all_data, f, indent=2, default=str)
            
            logger.info(f"Data collection completed. Saved to {latest_file} and {snapshot_file}")
            
            # Clean old snapshots (keep last 24)
            self._cleanup_old_snapshots()
            
            return all_data
            
        except Exception as e:
            logger.error(f"Error in data collection: {e}")
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def _cleanup_old_snapshots(self, keep_count: int = 24):
        """Clean up old snapshot files, keeping only the most recent ones"""
        try:
            snapshot_files = []
            for file in os.listdir(self.snapshots_dir):
                if file.startswith('snapshot_') and file.endswith('.json'):
                    file_path = os.path.join(self.snapshots_dir, file)
                    snapshot_files.append((file_path, os.path.getctime(file_path)))
            
            # Sort by creation time (newest first)
            snapshot_files.sort(key=lambda x: x[1], reverse=True)
            
            # Delete old files
            for file_path, _ in snapshot_files[keep_count:]:
                os.remove(file_path)
                logger.info(f"Deleted old snapshot: {file_path}")
                
        except Exception as e:
            logger.error(f"Error cleaning up snapshots: {e}")
    
    def check_dashboard_health(self) -> bool:
        """Check if dashboard is running and responsive"""
        try:
            response = requests.get(f"{self.dashboard_url}", timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Dashboard health check failed: {e}")
            return False
    
    def send_notification(self, message: str, importance: str = "info"):
        """Send notification (placeholder for future notification integration)"""
        logger.info(f"NOTIFICATION [{importance.upper()}]: {message}")
        
        # Could integrate with:
        # - Email notifications
        # - Slack/Telegram bots
        # - Desktop notifications
        # - SMS alerts
    
    def analyze_changes(self, current_data: Dict, previous_data: Dict) -> List[str]:
        """Analyze changes between current and previous data collections"""
        changes = []
        
        if not previous_data or 'themes' not in previous_data:
            return changes
        
        try:
            for theme_name in current_data.get('themes', {}):
                if theme_name not in previous_data.get('themes', {}):
                    continue
                
                current_theme = current_data['themes'][theme_name]
                previous_theme = previous_data['themes'][theme_name]
                
                # Check for significant changes
                if 'analysis' in current_theme and 'analysis' in previous_theme:
                    current_analysis = current_theme['analysis']
                    previous_analysis = previous_theme['analysis']
                    
                    # Check for position changes
                    current_green = {pos['ticker'] for pos in current_analysis.get('GREEN', [])}
                    previous_green = {pos['ticker'] for pos in previous_analysis.get('GREEN', [])}
                    
                    new_green = current_green - previous_green
                    lost_green = previous_green - current_green
                    
                    if new_green:
                        changes.append(f"{theme_name}: New GREEN positions: {', '.join(new_green)}")
                    
                    if lost_green:
                        changes.append(f"{theme_name}: Positions moved from GREEN: {', '.join(lost_green)}")
                    
                    # Check for new RED positions
                    current_red = {pos['ticker'] for pos in current_analysis.get('RED', [])}
                    previous_red = {pos['ticker'] for pos in previous_analysis.get('RED', [])}
                    
                    new_red = current_red - previous_red
                    if new_red:
                        changes.append(f"{theme_name}: New RED positions: {', '.join(new_red)}")
                        self.send_notification(f"🔴 New RED positions in {theme_name}: {', '.join(new_red)}", "warning")
        
        except Exception as e:
            logger.error(f"Error analyzing changes: {e}")
        
        return changes
    
    def scheduled_job(self):
        """Main scheduled job that runs every 2 hours"""
        logger.info("=== Starting scheduled data collection ===")
        
        try:
            # Load previous data for comparison
            previous_data = {}
            latest_file = os.path.join(self.data_dir, 'latest_data.json')
            if os.path.exists(latest_file):
                with open(latest_file, 'r') as f:
                    previous_data = json.load(f)
            
            # Collect new data
            current_data = self.collect_data()
            
            # Analyze changes
            if 'error' not in current_data:
                changes = self.analyze_changes(current_data, previous_data)
                if changes:
                    logger.info("Changes detected:")
                    for change in changes:
                        logger.info(f"  - {change}")
                else:
                    logger.info("No significant changes detected")
            
            # Check dashboard health
            if not self.check_dashboard_health():
                self.send_notification("Dashboard is not responding", "error")
            
            logger.info("=== Scheduled job completed successfully ===")
            
        except Exception as e:
            logger.error(f"Error in scheduled job: {e}")
            self.send_notification(f"Agent error: {e}", "error")
    
    def start_dashboard(self):
        """Start the Streamlit dashboard"""
        try:
            logger.info("Starting Streamlit dashboard...")
            
            # Run streamlit in background with port 7865
            subprocess.Popen([
                sys.executable, "-m", "streamlit", "run", "dashboard.py",
                "--server.port", "7865",
                "--server.headless", "true",
                "--server.runOnSave", "false"
            ])
            
            # Wait a bit for startup
            time.sleep(5)
            
            if self.check_dashboard_health():
                logger.info("Dashboard started successfully")
                return True
            else:
                logger.error("Dashboard failed to start")
                return False
                
        except Exception as e:
            logger.error(f"Error starting dashboard: {e}")
            return False
    
    def run_scheduler(self):
        """Run the scheduler in a continuous loop"""
        logger.info("Starting A1-WAVE Agent scheduler...")
        
        # Schedule the job to run every 2 hours
        schedule.every(2).hours.do(self.scheduled_job)
        
        # Run once immediately on startup
        self.scheduled_job()
        
        # Keep the scheduler running
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def start(self, start_dashboard: bool = True):
        """Start the agent"""
        logger.info("Starting A1-WAVE Agent...")
        self.running = True
        
        # Start dashboard if requested
        if start_dashboard:
            if not self.start_dashboard():
                logger.error("Failed to start dashboard, continuing with data collection only...")
        
        # Start the scheduler in a separate thread
        scheduler_thread = Thread(target=self.run_scheduler, daemon=True)
        scheduler_thread.start()
        
        logger.info("A1-WAVE Agent started successfully!")
        logger.info("Dashboard: http://localhost:8501")
        logger.info("Data collection: Every 2 hours")
        
        return scheduler_thread
    
    def stop(self):
        """Stop the agent"""
        logger.info("Stopping A1-WAVE Agent...")
        self.running = False
        logger.info("A1-WAVE Agent stopped")

def main():
    """Main function to run the agent"""
    import argparse
    
    parser = argparse.ArgumentParser(description='A1-WAVE Dashboard Agent')
    parser.add_argument('--no-dashboard', action='store_true', 
                       help='Do not start the dashboard, only run data collection')
    parser.add_argument('--once', action='store_true',
                       help='Run data collection once and exit')
    
    args = parser.parse_args()
    
    agent = A1WaveAgent()
    
    if args.once:
        # Run once and exit
        logger.info("Running data collection once...")
        agent.collect_data()
        logger.info("Data collection completed. Exiting.")
    else:
        # Start the agent
        try:
            scheduler_thread = agent.start(start_dashboard=not args.no_dashboard)
            
            # Keep the main thread alive
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Received interrupt signal...")
            agent.stop()
        except Exception as e:
            logger.error(f"Agent error: {e}")
            agent.stop()

if __name__ == "__main__":
    main()
