#!/usr/bin/env python3
"""
Script to download HTML files from topology.nipissingu.ca
Downloads files from https://topology.nipissingu.ca/tp/reprints/v#{n}/r2.htm
where n ranges from 01 to 67.
"""

import os
import sys
import requests
from pathlib import Path


def download_html_files(output_dir="downloads"):
    """
    Download HTML files from topology.nipissingu.ca for volumes 01-67.
    
    Args:
        output_dir: Directory where downloaded files will be saved
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    base_url = "https://topology.nipissingu.ca/tp/reprints/v{}/r2.htm"
    
    successful_downloads = 0
    failed_downloads = []
    
    # Download files for volumes 01 through 67
    for n in range(1, 68):
        volume_num = str(n).zfill(2)  # Zero-pad to 2 digits (01, 02, ..., 67)
        url = base_url.format(volume_num)
        
        # Create filename based on volume number
        filename = f"v{volume_num}_r2.html"
        filepath = os.path.join(output_dir, filename)
        
        print(f"Downloading {url}...", end=" ")
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Save the HTML content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"✓ Saved to {filepath}")
            successful_downloads += 1
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed: {e}")
            failed_downloads.append((volume_num, str(e)))
    
    # Print summary
    print("\n" + "="*60)
    print(f"Download Summary:")
    print(f"Successful: {successful_downloads}/67")
    print(f"Failed: {len(failed_downloads)}/67")
    
    if failed_downloads:
        print("\nFailed downloads:")
        for volume, error in failed_downloads:
            print(f"  Volume {volume}: {error}")
    
    return successful_downloads, failed_downloads


if __name__ == "__main__":
    # Allow custom output directory from command line
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "downloads"
    
    print(f"Starting download of HTML files to '{output_dir}' directory...")
    print("="*60)
    
    successful, failed = download_html_files(output_dir)
    
    # Exit with error code if any downloads failed
    sys.exit(0 if len(failed) == 0 else 1)
