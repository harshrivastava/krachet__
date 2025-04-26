import os
import shutil
import ctypes
import urllib.request
import zipfile
from pathlib import Path

def install_fonts():
    try:
        # Get the system fonts directory
        if os.name == 'nt':  # Windows
            fonts_dir = os.path.join(os.environ['WINDIR'], 'Fonts')
        else:  # Linux/Mac
            fonts_dir = os.path.expanduser('~/.fonts')
            os.makedirs(fonts_dir, exist_ok=True)

        # Create Assets directory if it doesn't exist
        assets_dir = os.path.join('Frontend', 'Assets')
        os.makedirs(assets_dir, exist_ok=True)

        # Download and install Inter font
        inter_url = "https://github.com/rsms/inter/releases/download/v3.19/Inter-3.19.zip"
        inter_zip = os.path.join(assets_dir, "Inter.zip")
        
        print("Downloading Inter font...")
        urllib.request.urlretrieve(inter_url, inter_zip)
        
        # Extract the font
        print("Extracting font...")
        with zipfile.ZipFile(inter_zip, 'r') as zip_ref:
            zip_ref.extractall(assets_dir)
        
        # Copy font files to system fonts directory
        print("Installing fonts...")
        for font_file in Path(assets_dir).rglob('*.ttf'):
            try:
                shutil.copy2(font_file, fonts_dir)
                print(f"Installed: {font_file.name}")
            except PermissionError:
                print(f"Warning: Could not install {font_file.name} - Permission denied. Try running as administrator.")
                continue
        
        # Clean up
        try:
            os.remove(inter_zip)
            shutil.rmtree(os.path.join(assets_dir, 'Inter-3.19'))
        except Exception as e:
            print(f"Warning: Could not clean up temporary files: {e}")
        
        # Refresh font cache
        if os.name == 'nt':
            try:
                ctypes.windll.gdi32.AddFontResourceW(fonts_dir)
                ctypes.windll.user32.SendMessageW(0xFFFF, 0x001D, 0, 0)
            except Exception as e:
                print(f"Warning: Could not refresh font cache: {e}")
        else:
            try:
                os.system('fc-cache -f -v')
            except Exception as e:
                print(f"Warning: Could not refresh font cache: {e}")
        
        print("Font installation completed!")
        
    except Exception as e:
        print(f"Error during font installation: {e}")
        return False
    
    return True

if __name__ == "__main__":
    install_fonts() 