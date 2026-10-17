"""
CoinVault iOS Platform Runner
Starts the CoinVault server on 0.0.0.0:8000
Displays local and LAN IP addresses for easy iPhone access.
"""

import socket
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))
from main import app

def get_local_ip():
    """Retrieve the primary local LAN IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Does not actually establish connection
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == "__main__":
    local_ip = get_local_ip()
    port = int(os.environ.get("PORT", 8000))
    
    print("=" * 64)
    print("🪙  COINVAULT — iOS NUMISMATIC AI & eBAY LISTING PLATFORM")
    print("=" * 64)
    print(f"🖥️  Local Browser:     http://localhost:{port}")
    print(f"📱  iPhone on Wi-Fi:   http://{local_ip}:{port}")
    print("-" * 64)
    print("💡 iOS Safari Tip: Tap 'Share' -> 'Add to Home Screen' to install as native app!")
    print("=" * 64)
    print("\nStarting server...\n")
    
    app.run(host="0.0.0.0", port=port, debug=False)
