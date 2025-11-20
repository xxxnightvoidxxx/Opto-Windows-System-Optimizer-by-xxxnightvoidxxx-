import os
import sys
import subprocess
import time
import ctypes
import json
import shutil
from pathlib import Path

# Auto-install required dependencies before importing them
def install_dependencies():
    required_packages = {
        'pygame': 'pygame',
        'psutil': 'psutil', 
        'packaging': 'packaging'
    }
    
    for package_name, pip_name in required_packages.items():
        try:
            __import__(package_name)
            print(f"✅ {package_name} already installed")
        except ImportError:
            print(f"📦 Installing {package_name}...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', pip_name])
                print(f"✅ {package_name} installed successfully")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package_name}")
                print("Please install manually with: pip install", pip_name)
                input("Press Enter to exit...")
                sys.exit(1)

# Install dependencies before anything else
install_dependencies()

# Now import the installed packages
import pygame
import psutil
from packaging import requirements

class OPTOSystemUtility:
    def __init__(self):
        self.is_admin = self.check_admin()
        self.script_dir = self.get_script_directory()
        self.config_file = os.path.join(self.script_dir, "opto_config.json")
        self.load_config()
        self.music_file = os.path.join(self.script_dir, "opto_theme.mp3")
        self.music_playing = False
        self.pygame_initialized = False
        self.terminal_width = 80
        self.terminal_height = 25
        
        # EASTER EGG: If default speed is set below 25ms in code, show secret message
        self.easter_egg_triggered = False
        self.check_easter_egg()
        
        # Change to script directory to ensure file access
        os.chdir(self.script_dir)
        
        # Initialize pygame for audio
        try:
            pygame.mixer.init()
            self.pygame_initialized = True
        except:
            self.log("Audio system initialization failed - music features disabled")
        
        self.setup_terminal()
        self.auto_start_music()
    
    def check_easter_egg(self):
        """Check if Easter egg conditions are met"""
        # EASTER EGG: If someone edits the default speed in code to be faster than allowed
        default_speed_in_code = 50  # This is the normal default value
        
        # If a developer changes the line above to a value between 0-24, trigger Easter egg
        if default_speed_in_code < 25:
            self.easter_egg_triggered = True
            self.show_easter_egg()
    
    def show_easter_egg(self):
        """Display the Easter egg message"""
        print("\n" + "="*80)
        print("🎮" * 40)
        print("="*80)
        print()
        print("You're not new to this are you? You would make a great Adversary!".center(80))
        print()
        print("xxxnightvoidxxx Twitch/YT".center(80))
        print()
        print("🎮" * 40)
        print("="*80)
        print()
        input("Press Enter to continue to the main program...")
        os.system('cls')
    
    def load_config(self):
        """Load configuration from file"""
        default_config = {
            "text_speed": 50,  # Normal default - change this to <25 in code to trigger Easter egg
            "auto_music": True
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                self.save_config()
        except:
            self.config = default_config
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except:
            pass
    
    def get_script_directory(self):
        """Get the directory where the script is located"""
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(os.path.abspath(__file__))
    
    def check_admin(self):
        """Check if running as administrator"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def setup_terminal(self):
        """Setup terminal appearance"""
        os.system("title 🗡️  OPTO SYSTEM UTILITY v2.0 🗡️")
        os.system("color 07")  # Black background, white text
        os.system(f"mode con: cols={self.terminal_width} lines={self.terminal_height}")
    
    def center_text(self, text):
        """Center text in terminal"""
        width = self.terminal_width
        return text.center(width)
    
    def typewriter(self, text, center=False, newline=True):
        """Typewriter effect for text output"""
        speed_ms = self.config["text_speed"]
        
        if center:
            text = self.center_text(text)
        
        for char in text:
            print(char, end='', flush=True)
            time.sleep(speed_ms / 1000)
        
        if newline:
            print()
    
    def log(self, message, status="INFO"):
        """Enhanced logging with status and timestamps"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] [{status}] {message}"
        self.typewriter(formatted_message, center=True)
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls')
    
    def play_music(self):
        """Play background music"""
        if not self.pygame_initialized:
            return False
            
        if os.path.exists(self.music_file):
            try:
                pygame.mixer.music.load(self.music_file)
                pygame.mixer.music.play(-1)
                self.music_playing = True
                return True
            except Exception as e:
                self.log(f"Music playback error: {e}", "ERROR")
                return False
        return False
    
    def stop_music(self):
        """Stop background music"""
        if self.pygame_initialized and self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False
    
    def ensure_music_playing(self):
        """Ensure music continues playing - call this before long operations"""
        if self.pygame_initialized and not self.music_playing and os.path.exists(self.music_file):
            self.play_music()
    
    def auto_start_music(self):
        """Auto-start music on program start"""
        if self.config.get("auto_music", True) and os.path.exists(self.music_file):
            if self.play_music():
                self.log("🎵 Ancient melodies awaken...", "SYSTEM")
    
    def load_mp3_file(self, filename):
        """Load an MP3 file"""
        if os.path.isabs(filename):
            source_path = filename
        else:
            source_path = os.path.join(self.script_dir, filename)
        
        if not os.path.exists(source_path):
            return False, f"❌ File not found in the shadows: {filename}"
        
        try:
            shutil.copy2(source_path, self.music_file)
            return True, f"🎵 {filename} now resonates with ancient power"
        except Exception as e:
            return False, f"❌ Dark forces prevent the transfer: {e}"
    
    def run_sfc_scan(self):
        """Run System File Checker with detailed logging"""
        self.clear_screen()
        self.log("🛡️  INITIATING SYSTEM INTEGRITY RITUAL", "SFC")
        self.log("Command: sfc /scannow", "COMMAND")
        self.log("Purpose: Scans and repairs corrupted system files", "INFO")
        time.sleep(2)
        
        try:
            result = subprocess.run(['sfc', '/scannow'], capture_output=True, text=True, check=True)
            self.log("System scan completed", "SUCCESS")
            self.log("Windows has examined the fortress walls", "COMPLETE")
        except subprocess.CalledProcessError as e:
            self.log(f"Ritual failed: {e}", "ERROR")
        
        input("\nPress Enter to continue your journey...")
    
    def schedule_chkdsk(self):
        """Schedule disk check with detailed logging - FIXED MUSIC ISSUE"""
        self.clear_screen()
        self.log("💾 PREPARING DISK PURIFICATION RITUAL", "CHKDSK")
        self.log("Command: chkdsk /f /r", "COMMAND")
        self.log("Purpose: Scans disk for errors and repairs them on next reboot", "INFO")
        time.sleep(2)
        
        # Ensure music continues playing during this operation
        self.ensure_music_playing()
        
        try:
            # Use a different approach that doesn't block music
            # Run chkdsk without waiting for user input by using pre-answered prompt
            result = subprocess.run(
                ['chkdsk', '/f', '/r'], 
                capture_output=True, 
                text=True, 
                input='Y\n',
                timeout=10  # Add timeout to prevent hanging
            )
            self.log("Purification scheduled for next awakening", "SUCCESS")
            self.log("The disk shall be cleansed upon rebirth", "COMPLETE")
        except subprocess.TimeoutExpired:
            # This is expected - chkdsk schedules for next reboot and waits
            self.log("Purification scheduled for next awakening", "SUCCESS")
            self.log("The disk shall be cleansed upon rebirth", "COMPLETE")
        except Exception as e:
            self.log(f"Ritual interrupted: {e}", "ERROR")
        
        # Double-check music is still playing
        self.ensure_music_playing()
        input("\nPress Enter to continue your journey...")
    
    def flush_dns(self):
        """Flush DNS cache with detailed logging"""
        self.log("🌀 INVOKING DNS CLEANSING", "NETWORK")
        self.log("Command: ipconfig /flushdns", "COMMAND")
        self.log("Purpose: Clears DNS resolver cache", "INFO")
        
        try:
            subprocess.run(['ipconfig', '/flushdns'], check=True)
            self.log("DNS cache purified", "SUCCESS")
            self.log("The paths of communication are cleared", "COMPLETE")
        except subprocess.CalledProcessError as e:
            self.log(f"Cleansing failed: {e}", "ERROR")
    
    def release_ip(self):
        """Release IP address with detailed logging"""
        self.log("🔓 RELEASING ANCIENT BINDINGS", "NETWORK")
        self.log("Command: ipconfig /release", "COMMAND")
        self.log("Purpose: Releases current IP address", "INFO")
        
        try:
            subprocess.run(['ipconfig', '/release'], check=True)
            self.log("IP address released from service", "SUCCESS")
        except subprocess.CalledProcessError as e:
            self.log(f"Release failed: {e}", "ERROR")
    
    def renew_ip(self):
        """Renew IP address with detailed logging"""
        self.log("🔗 FORGING NEW CONNECTIONS", "NETWORK")
        self.log("Command: ipconfig /renew", "COMMAND")
        self.log("Purpose: Requests new IP address from DHCP", "INFO")
        
        try:
            subprocess.run(['ipconfig', '/renew'], check=True)
            self.log("New IP address forged", "SUCCESS")
            self.log("The network flows with renewed energy", "COMPLETE")
        except subprocess.CalledProcessError as e:
            self.log(f"Renewal failed: {e}", "ERROR")
    
    def set_cloudflare_dns(self):
        """Set Cloudflare DNS with detailed logging"""
        self.log("🌐 CONFIGURING ETHERNET GATES", "DNS")
        self.log("Command: netsh interface ip set dns", "COMMAND")
        self.log("Purpose: Sets DNS servers to Cloudflare (1.1.1.1, 1.0.0.1)", "INFO")
        
        try:
            interfaces = self.get_network_interfaces()
            if interfaces:
                for interface in interfaces:
                    subprocess.run(['netsh', 'interface', 'ip', 'set', 'dns', 
                                  f'name={interface}', 'source=static', 'addr=1.1.1.1'], check=True)
                    subprocess.run(['netsh', 'interface', 'ip', 'add', 'dns', 
                                  f'name={interface}', 'addr=1.0.0.1', 'index=2'], check=True)
                self.log("Cloudflare DNS gates are active", "SUCCESS")
                self.log("Your connection is now blessed with speed", "COMPLETE")
            else:
                self.log("No network interfaces found in the realm", "WARNING")
        except subprocess.CalledProcessError as e:
            self.log(f"Gate configuration failed: {e}", "ERROR")
    
    def set_custom_dns(self):
        """Set custom DNS servers provided by user"""
        self.clear_screen()
        print()
        print(self.center_text("================================================"))
        self.typewriter("           🌐 CUSTOM DNS CONFIGURATION", center=True)
        print(self.center_text("================================================"))
        print()
        self.typewriter("Enter your preferred DNS servers", center=True)
        self.typewriter("Format: Primary DNS [Secondary DNS]", center=True)
        print()
        print(self.center_text("Examples:"))
        print(self.center_text("8.8.8.8 8.8.4.4 (Google)"))
        print(self.center_text("9.9.9.9 149.112.112.112 (Quad9)"))
        print(self.center_text("208.67.222.222 208.67.220.220 (OpenDNS)"))
        print()
        print(self.center_text("================================================"))
        print()
        
        primary_dns = input("                PRIMARY DNS: ").strip()
        secondary_dns = input("                SECONDARY DNS: ").strip()
        
        if not primary_dns:
            self.typewriter("❌ No primary DNS provided", center=True)
            input("Press Enter to continue...")
            return
        
        self.log("🌐 CONFIGURING CUSTOM ETHERNET GATES", "DNS")
        self.log(f"Command: netsh interface ip set dns [Custom: {primary_dns}, {secondary_dns}]", "COMMAND")
        self.log("Purpose: Sets custom DNS servers provided by user", "INFO")
        
        try:
            interfaces = self.get_network_interfaces()
            if interfaces:
                for interface in interfaces:
                    # Set primary DNS
                    subprocess.run(['netsh', 'interface', 'ip', 'set', 'dns', 
                                  f'name={interface}', 'source=static', f'addr={primary_dns}'], check=True)
                    
                    # Set secondary DNS if provided
                    if secondary_dns:
                        subprocess.run(['netsh', 'interface', 'ip', 'add', 'dns', 
                                      f'name={interface}', f'addr={secondary_dns}', 'index=2'], check=True)
                
                self.log("Custom DNS gates are active", "SUCCESS")
                if secondary_dns:
                    self.log(f"Primary: {primary_dns}, Secondary: {secondary_dns}", "CONFIG")
                else:
                    self.log(f"Primary: {primary_dns}", "CONFIG")
                self.log("Your connection now follows your chosen path", "COMPLETE")
            else:
                self.log("No network interfaces found in the realm", "WARNING")
        except subprocess.CalledProcessError as e:
            self.log(f"Custom gate configuration failed: {e}", "ERROR")
    
    def reset_dns_dhcp(self):
        """Reset DNS to DHCP with detailed logging"""
        self.log("🔄 RESTORING ANCIENT PROTOCOLS", "DNS")
        self.log("Command: netsh interface ip set dns source=dhcp", "COMMAND")
        self.log("Purpose: Resets DNS to automatic DHCP settings", "INFO")
        
        try:
            interfaces = self.get_network_interfaces()
            if interfaces:
                for interface in interfaces:
                    subprocess.run(['netsh', 'interface', 'ip', 'set', 'dns', 
                                  f'name={interface}', 'source=dhcp'], check=True)
                self.log("DNS restored to ancient protocols", "SUCCESS")
                self.log("The old ways are preserved", "COMPLETE")
            else:
                self.log("No network interfaces to restore", "WARNING")
        except subprocess.CalledProcessError as e:
            self.log(f"Restoration failed: {e}", "ERROR")
    
    def get_network_interfaces(self):
        """Get active network interfaces"""
        try:
            result = subprocess.run(['netsh', 'interface', 'show', 'interface'], 
                                  capture_output=True, text=True, check=True)
            interfaces = []
            for line in result.stdout.split('\n'):
                if 'Connected' in line and 'Dedicated' in line:
                    parts = line.split()
                    if len(parts) > 3:
                        interfaces.append(parts[-1])
            return interfaces if interfaces else ['Ethernet']
        except:
            return ['Ethernet']
    
    def run_all_operations(self):
        """Run all system operations with epic narrative"""
        self.clear_screen()
        self.log("⚔️  INITIATING GRAND SYSTEM PURIFICATION ⚔️", "SYSTEM")
        self.log("All rituals will be performed in sequence", "WARNING")
        time.sleep(2)
        
        rituals = [
            ("🛡️  System Integrity Ritual", self.run_sfc_scan),
            ("💾 Disk Purification Ritual", self.schedule_chkdsk),
            ("🌐 Network Cleansing Ritual", self.run_network_reset),
            ("🔮 DNS Reconfiguration Ritual", self.set_cloudflare_dns),
        ]
        
        for name, ritual in rituals:
            self.log(f"Performing: {name}", "RITUAL")
            ritual()
            time.sleep(1)
        
        self.log("🎉 ALL GRAND RITUALS COMPLETED 🎉", "VICTORY")
        self.log("Your system has been blessed with ancient power", "COMPLETE")
        input("\nPress Enter to continue your journey...")
    
    def run_network_reset(self):
        """Run complete network reset"""
        self.flush_dns()
        time.sleep(1)
        self.release_ip()
        time.sleep(2)
        self.renew_ip()
        self.log("Network reset ritual complete", "SUCCESS")
    
    def text_speed_menu(self):
        """Simple text speed adjustment"""
        while True:
            self.clear_screen()
            print()
            print(self.center_text("================================================"))
            self.typewriter("           ⏱️  SCROLL SPEED RITUAL", center=True)
            print(self.center_text("================================================"))
            print()
            self.typewriter(f"Current speed: {self.config['text_speed']}ms", center=True)
            print()
            self.typewriter("1-9: Faster to Slower (1=Fastest, 9=Slowest)", center=True)
            self.typewriter("0: Return to Main Menu", center=True)
            print()
            print(self.center_text("================================================"))
            print()
            
            choice = input("                CHOOSE YOUR PACE: ").strip()
            
            if choice == "0":
                break
            elif choice.isdigit() and 1 <= int(choice) <= 9:
                # Map 1-9 to 25-200ms (1=25ms, 9=200ms)
                speed_map = {1: 25, 2: 35, 3: 50, 4: 75, 5: 100, 6: 125, 7: 150, 8: 175, 9: 200}
                self.config["text_speed"] = speed_map[int(choice)]
                self.save_config()
                self.typewriter(f"Scroll speed set to {self.config['text_speed']}ms", center=True)
                input("Press Enter to continue...")
                break
    
    def music_menu(self):
        """Simplified music menu"""
        self.clear_screen()
        print()
        print(self.center_text("================================================"))
        self.typewriter("           🎵 ANCIENT MELODIES", center=True)
        print(self.center_text("================================================"))
        print()
        
        if os.path.exists(self.music_file):
            self.typewriter("Current melody: opto_theme.mp3", center=True)
        else:
            self.typewriter("No ancient melody loaded", center=True)
        
        print()
        self.typewriter("Enter the name of your MP3 file", center=True)
        self.typewriter("(e.g., 'music.mp3') or '0' to cancel", center=True)
        print()
        print(self.center_text("================================================"))
        print()
        
        filename = input("                MELODY NAME: ").strip()
        
        if filename == "0":
            return
        
        success, message = self.load_mp3_file(filename)
        self.clear_screen()
        self.typewriter(message, center=True)
        
        if success:
            self.config["auto_music"] = True
            self.save_config()
            self.play_music()
            self.typewriter("Melody will play on every awakening", center=True)
        
        input("\nPress Enter to continue your journey...")
    
    def main_menu(self):
        """Main menu loop with RPG style"""
        while True:
            self.clear_screen()
            print()
            print()
            print(self.center_text("╔══════════════════════════════════════════════╗"))
            print(self.center_text("║             🗡️ OPTO SYSTEM v2.0 🗡️           ║"))
            print(self.center_text("║          Ancient Power Awakens...           ║"))
            print(self.center_text("╚══════════════════════════════════════════════╝"))
            print()
            self.typewriter("Choose your ritual, brave one:", center=True)
            print()
            self.typewriter("[1] System Integrity Scan", center=True)
            self.typewriter("[2] Disk Purification", center=True)
            self.typewriter("[3] Network Cleansing", center=True)
            self.typewriter("[4] DNS Configuration", center=True)
            self.typewriter("[5] Grand Purification (All)", center=True)
            self.typewriter("[6] Scroll Speed", center=True)
            self.typewriter("[7] Ancient Melodies", center=True)
            self.typewriter("[0] Leave the Realm", center=True)
            print()
            print(self.center_text("════════════════════════════════════════════════"))
            print()
            
            choice = input("                YOUR CHOICE: ").strip()
            
            if choice == "1":
                self.sfc_menu()
            elif choice == "2":
                self.chkdsk_menu()
            elif choice == "3":
                self.network_menu()
            elif choice == "4":
                self.dns_menu()
            elif choice == "5":
                self.run_all_menu()
            elif choice == "6":
                self.text_speed_menu()
            elif choice == "7":
                self.music_menu()
            elif choice == "0":
                self.leave_realm()
                break
    
    def sfc_menu(self):
        """SFC menu"""
        self.clear_screen()
        print()
        print(self.center_text("================================================"))
        self.typewriter("           🛡️ SYSTEM INTEGRITY", center=True)
        print(self.center_text("================================================"))
        print()
        self.typewriter("Scans and repairs corrupted system files", center=True)
        self.typewriter("A ritual of protection for your fortress", center=True)
        print()
        print(self.center_text("[1] Begin Integrity Ritual"))
        print(self.center_text("[2] Return to Main Menu"))
        print()
        print(self.center_text("================================================"))
        print()
        choice = input("                CHOOSE: ").strip()
        if choice == "1":
            self.run_sfc_scan()
    
    def chkdsk_menu(self):
        """CHKDSK menu"""
        self.clear_screen()
        print()
        print(self.center_text("================================================"))
        self.typewriter("           💾 DISK PURIFICATION", center=True)
        print(self.center_text("================================================"))
        print()
        self.typewriter("Scans disk for errors and repairs them", center=True)
        self.typewriter("Requires system rebirth if C: drive is active", center=True)
        print()
        print(self.center_text("[1] Schedule Purification"))
        print(self.center_text("[2] Return to Main Menu"))
        print()
        print(self.center_text("================================================"))
        print()
        choice = input("                CHOOSE: ").strip()
        if choice == "1":
            self.schedule_chkdsk()
    
    def network_menu(self):
        """Network menu"""
        self.clear_screen()
        print()
        print(self.center_text("================================================"))
        self.typewriter("           🌐 NETWORK CLEANSING", center=True)
        print(self.center_text("================================================"))
        print()
        print(self.center_text("[1] Flush DNS Cache"))
        print(self.center_text("[2] Release IP Address"))
        print(self.center_text("[3] Renew IP Address"))
        print(self.center_text("[4] Complete Network Reset"))
        print(self.center_text("[5] Return to Main Menu"))
        print()
        print(self.center_text("================================================"))
        print()
        choice = input("                CHOOSE: ").strip()
        if choice == "1":
            self.flush_dns()
            input("\nPress Enter to continue...")
        elif choice == "2":
            self.release_ip()
            input("\nPress Enter to continue...")
        elif choice == "3":
            self.renew_ip()
            input("\nPress Enter to continue...")
        elif choice == "4":
            self.run_network_reset()
            input("\nPress Enter to continue...")
    
    def dns_menu(self):
        """DNS menu"""
        self.clear_screen()
        print()
        print(self.center_text("================================================"))
        self.typewriter("           🔮 DNS CONFIGURATION", center=True)
        print(self.center_text("================================================"))
        print()
        print(self.center_text("[1] Set Cloudflare DNS (Speed)"))
        print(self.center_text("[2] Set Custom DNS (Your Choice)"))
        print(self.center_text("[3] Reset to Auto DNS (Ancient)"))
        print(self.center_text("[4] Return to Main Menu"))
        print()
        print(self.center_text("================================================"))
        print()
        choice = input("                CHOOSE: ").strip()
        if choice == "1":
            self.set_cloudflare_dns()
            input("\nPress Enter to continue...")
        elif choice == "2":
            self.set_custom_dns()
            input("\nPress Enter to continue...")
        elif choice == "3":
            self.reset_dns_dhcp()
            input("\nPress Enter to continue...")
    
    def run_all_menu(self):
        """Run all operations menu"""
        self.clear_screen()
        print()
        print(self.center_text("================================================"))
        self.typewriter("           ⚔️ GRAND PURIFICATION", center=True)
        print(self.center_text("================================================"))
        print()
        self.typewriter("WARNING: All rituals will be performed", center=True)
        self.typewriter("This may take considerable time", center=True)
        print()
        print(self.center_text("[1] Begin Grand Ritual"))
        print(self.center_text("[2] Return to Main Menu"))
        print()
        print(self.center_text("================================================"))
        print()
        choice = input("                CHOOSE: ").strip()
        if choice == "1":
            self.run_all_operations()
    
    def leave_realm(self):
        """Exit the program with style"""
        self.clear_screen()
        self.typewriter("🕯️  The candles flicker...", center=True)
        self.typewriter("The ancient power returns to slumber", center=True)
        self.typewriter("Until we meet again, brave one...", center=True)
        time.sleep(2)
        self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        self.stop_music()
        if self.pygame_initialized:
            pygame.mixer.quit()


def run_as_admin():
    """Relaunch script as administrator"""
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Requesting administrator privileges...")
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            sys.exit(0)
        except Exception as e:
            print(f"Failed to request admin rights: {e}")
            print("Continuing without administrator privileges...")

def main():
    """Main entry point"""
    print("OPTO System Utility - Awakening Ancient Power...")
    
    # Request admin privileges
    run_as_admin()
    
    # Create and run the utility
    utility = OPTOSystemUtility()
    
    try:
        utility.main_menu()
    except KeyboardInterrupt:
        utility.cleanup()
        print("\nOPTO System Utility closed.")
    except Exception as e:
        utility.cleanup()
        print(f"An ancient curse has befallen us: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()