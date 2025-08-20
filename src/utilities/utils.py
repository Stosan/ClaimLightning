# Helper function to clean up old files (optional)
from datetime import datetime
from pathlib import Path


async def cleanup_old_files(UPLOAD_DIR:str,days_old: int = 30):
    """
    Clean up files older than specified days.
    Run this as a background task or cron job.
    """
    try:
        upload_path = Path(UPLOAD_DIR)
        if not upload_path.exists():
            return
        
        cutoff_time = datetime.now().timestamp() - (days_old * 24 * 3600)
        
        for file_path in upload_path.glob("*"):
            if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                file_path.unlink()
                print(f"Deleted old file: {file_path}")
                
    except Exception as e:
        print(f"Error cleaning up old files: {e}")