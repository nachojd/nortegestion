#!/usr/bin/env python
"""
Script simple para iniciar MotoCenter en desarrollo
"""
import os
import subprocess
import sys
import time
import webbrowser

def start_backend():
    """Inicia el servidor Django"""
    print("🔧 Iniciando backend Django...")
    backend_process = subprocess.Popen([
        sys.executable, "manage.py", "runserver", "192.168.1.18:8000"
    ], cwd=os.getcwd())
    return backend_process

def start_frontend():
    """Inicia el servidor Next.js"""
    print("⚡ Iniciando frontend Next.js...")
    frontend_process = subprocess.Popen([
        "npm", "run", "dev", "--", "--hostname", "0.0.0.0"
    ], cwd="frontend", shell=True)
    return frontend_process

def main():
    print("🏍️  MotoCenter - Modo Desarrollo")
    print("=" * 40)
    
    try:
        # Iniciar backend
        backend = start_backend()
        time.sleep(3)
        
        # Iniciar frontend
        frontend = start_frontend()
        time.sleep(5)
        
        print("\n✅ Servidores iniciados:")
        print("🔧 Backend:  http://192.168.1.18:8000/")
        print("⚡ Frontend: http://192.168.1.18:3002/")
        print("📱 App:      http://192.168.1.18:3002/")
        
        print("\n⏹️  Presiona Ctrl+C para parar ambos servidores")
        
        # Abrir navegador
        time.sleep(2)
        webbrowser.open("http://192.168.1.18:3002/")
        
        # Esperar hasta que el usuario presione Ctrl+C
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo servidores...")
            frontend.terminate()
            backend.terminate()
            frontend.wait()
            backend.wait()
            print("✅ Servidores detenidos")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())