import time
import json
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class DirectoryMonitor(FileSystemEventHandler):
    def __init__(self, watch_dir, log_file):
        self.watch_dir = Path(watch_dir)
        self.log_file = Path(log_file)
        self.ensure_log_directory()
        
    def ensure_log_directory(self):
        """Log dosyası dizininin varlığını kontrol eder ve gerekirse oluşturur."""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_file.exists():
            self.log_file.write_text('[]')

    def log_change(self, event_type, path, is_directory):
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'path': str(path),
            'is_directory': is_directory
        }
        
        logs.append(log_entry)
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        
        print(f"Olay Kaydedildi: {event_type} - {path}")  # Ekrana yazdırma eklendi

    def on_created(self, event):
        self.log_change('oluşturuldu', event.src_path, event.is_directory)

    def on_modified(self, event):
        self.log_change('değiştirildi', event.src_path, event.is_directory)

    def on_deleted(self, event):
        self.log_change('silindi', event.src_path, event.is_directory)

    def on_moved(self, event):
        self.log_change('taşındı', f"{event.src_path} -> {event.dest_path}", event.is_directory)

def main():
    WATCH_DIR = r'C:\Dersler\BSM101\Ödevler'
    LOG_FILE = r'C:\Dersler\BSM101\changes.json'
    
    print(f"İzlenen klasör: {WATCH_DIR}")
    print(f"Log dosyası: {LOG_FILE}")
    print("Program başlatıldı. Klasörde yapılan değişiklikler izleniyor...")
    
    Path(WATCH_DIR).mkdir(parents=True, exist_ok=True)
    
    event_handler = DirectoryMonitor(WATCH_DIR, LOG_FILE)
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=True)
    
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Program durduruldu")
    
    observer.join()

if __name__ == "__main__":
    main()