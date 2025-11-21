📖 Overview
OPTO System Utility is a comprehensive Windows optimization tool that combines powerful system maintenance commands with an immersive RPG-style interface. Perform essential system repairs while feeling like you're casting ancient rituals!

✨ Features
🛡️ System Integrity Scan - Run SFC to repair corrupted system files

💾 Disk Purification - Schedule CHKDSK for disk error checking

🌐 Network Cleansing - Flush DNS, release/renew IP addresses

🔮 DNS Configuration - Set Cloudflare, custom, or reset to automatic DNS

🎵 Ancient Melodies - Custom background music support

⚔️ Grand Purification - Run all optimizations in sequence

⏱️ Adjustable Text Speed - Customize the typewriter effect

🛠️ System Requirements
OS: Windows 10 or Windows 11

Architecture: 64-bit recommended

Permissions: Administrator rights required

Python: 3.6 or higher

📥 Installation Instructions
Step-by-Step Installation
Step 1: Install Python
Download Python

Go to python.org

Click "Download Python 3.x.x" (latest version)

Run the downloaded installer

Python Installation Setup

IMPORTANT: Check the box "Add Python to PATH" at the bottom

Click "Install Now"

Wait for installation to complete

Click "Close" when finished

Verify Python Installation

Press Windows + R, type cmd, press Enter

Type python --version and press Enter

You should see Python version information

If not, restart your computer and try again

Step 2: Download the OPTO Script
Get the Script File

Download opto_system_utility.py from the source

Save it to a memorable location like:

C:\OPTO\

Your Desktop

Documents folder

Create a Dedicated Folder (Recommended)

cmd
C:\OPTO\
Create this folder and place the script inside

This makes it easy to find and add music files later

Step 3: Run OPTO System Utility
First Time Setup

Navigate to where you saved opto_system_utility.py

Right-click on the file

Select "Run with Python" (if available) OR

Use the method below:

Recommended Method - Command Prompt

Press Windows + S, type "cmd"

Right-click "Command Prompt" and select "Run as administrator"

Navigate to your script location:

cmd
cd C:\OPTO
or

cmd
cd Desktop
Run the script:

cmd
python opto_system_utility.py
Automatic Dependency Installation

On first run, the script will automatically install required packages:

pygame (for music)

psutil (for system info)

packaging (for version checks)

Wait for "All dependencies installed" message

The main menu will appear once ready

🎮 How to Use
First Time Setup
Always Run as Administrator: Required for system operations

Initial Configuration:

Text speed automatically set to optimal (25ms)

Music feature enabled by default

Add Custom Music (Optional):

Place an MP3 file named opto_theme.mp3 in the same folder as the script

Or use the "Ancient Melodies" menu to load custom music

Main Menu Navigation
text
╔══════════════════════════════════════════════╗
║             🗡️ OPTO SYSTEM v2.0 🗡️           ║
║          Ancient Power Awakens...           ║
╚══════════════════════════════════════════════╝

Choose your ritual, brave one:

[1] System Integrity Scan
[2] Disk Purification  
[3] Network Cleansing
[4] DNS Configuration
[5] Grand Purification (All)
[6] Scroll Speed
[7] Ancient Melodies
[0] Leave the Realm
Feature Details
🛡️ System Integrity Scan

Runs sfc /scannow command

Scans and repairs Windows system files

Time: 10-30 minutes

💾 Disk Purification

Schedules chkdsk /f /r on next reboot

Checks and repairs disk errors

Requires system restart

🌐 Network Cleansing

Flush DNS - Clears DNS cache

Release IP - Releases current IP address

Renew IP - Requests new IP address

Complete Reset - All three operations

🔮 DNS Configuration

Cloudflare DNS - Fast DNS (1.1.1.1, 1.0.0.1)

Custom DNS - Your preferred DNS servers

Reset to Auto - Back to DHCP automatic settings

⚔️ Grand Purification

Runs all optimizations in sequence

Complete system maintenance routine

⏱️ Scroll Speed

Adjust text display speed (1-9)

1 = Fastest (25ms), 9 = Slowest (200ms)

🎵 Ancient Melodies

Load custom MP3 background music

Toggle auto-music on startup

⚠️ Important Notes
Administrator Rights
Required for system file repairs and network changes

Program automatically requests elevation

If denied, most features will not work properly

System Requirements
Windows 10/11 only - Not compatible with Mac or Linux

Python 3.6+ required

Internet connection needed for first-time dependency installation

Safety Precautions
Create a system restore point before major changes

Close other applications during system scans

Some operations may require reboot

🔧 Troubleshooting
Common Installation Issues
"Python is not recognized as an internal or external command"

Python wasn't added to PATH during installation

Reinstall Python and check "Add Python to PATH"

Or use full path: C:\Users\[YourName]\AppData\Local\Programs\Python\Python3x\python.exe opto_system_utility.py

"Access denied" or permission errors

Always run Command Prompt as Administrator

Right-click → "Run as administrator"

Dependencies fail to install

Check internet connection

Try manual installation:

cmd
pip install pygame psutil packaging
Music not playing

Verify MP3 file is in same folder as script

Check file name is exactly opto_theme.mp3

Ensure system volume is not muted

Running the Script
Easy Method - Create a Batch File

Create a new text file in the same folder as the script

Name it Run_OPTO.bat

Edit the file and add:

batch
@echo off
python opto_system_utility.py
pause
Save and right-click → "Run as administrator"

📝 Configuration
The program automatically creates opto_config.json:

json
{
    "text_speed": 25,
    "auto_music": true
}
🚨 Disclaimer
This tool performs system-level operations that can affect your computer's functionality. Use at your own risk. Always:

Backup important data before system maintenance

Create a system restore point

Understand the commands being executed

The developers are not responsible for any system instability or data loss resulting from improper use.

💡 Pro Tips
Quick Access: Create a shortcut to the batch file on your desktop

Custom Music: Use the "Ancient Melodies" menu to load your preferred background music

Text Speed: Adjust to your reading preference in the Scroll Speed menu

Network Issues: Use the Complete Network Reset for stubborn connection problems

Embark on your system optimization journey!
May your frames be high and your ping be low! 🗡️

For technical support, ensure you've followed all installation steps carefully before seeking assistance.
