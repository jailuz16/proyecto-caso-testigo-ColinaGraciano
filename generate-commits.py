import os
import subprocess
from datetime import datetime

def generate_builds():
    for i in range(1, 11):
        # Crear cambio pequeño
        with open('build-log.md', 'a') as f:
            f.write(f"\n# Build {i} - {datetime.now()}\n")
        
        # Commit y push
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', f'ci: Build automatizado #{i}'])
        subprocess.run(['git', 'push'])
        print(f"✅ Build {i} completado")
        
        # Pequeña pausa
        import time
        time.sleep(60)  # Esperar 1 minuto entre builds

if __name__ == "__main__":
    generate_builds()