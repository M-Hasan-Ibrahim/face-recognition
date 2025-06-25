"""
Simple HTTP Client - Sends image and message to Raspberry Pi
No SSL, no certificates, just works!
Supports sending message only (no image) or message + image
"""

import requests
import os
from datetime import datetime
from PIL import Image
import io

class PiSender:
    def __init__(self, pi_ip_address, port=8000):
        """
        Initialize the Pi sender with IP address and port
        
        Args:
            pi_ip_address (str): IP address of the Raspberry Pi
            port (int): Port number (default: 8000)
        """
        self.base_url = f"http://{pi_ip_address}:{port}"
        self.upload_url = f"{self.base_url}/upload"
        self.status_url = f"{self.base_url}/status"
        self.pi_ip = pi_ip_address
        self.port = port
    
    def send_to_pi(self, image_input, message_text):
        """
        Send image and message to Raspberry Pi
        
        Args:
            image_input: Can be None (message only), PIL Image object, or string path to image file
            message_text (str): Message to send
            
        Returns:
            dict: Server response or error info
        """
        try:
            # Handle None case - message only
            if image_input is None:
                print(f"📤 SENDING MESSAGE ONLY TO RASPBERRY PI")
                print(f"   Target: {self.upload_url}")
                print(f"   Image: None (message only)")
                print(f"   Message: {message_text}")
                print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Don't send image field at all when None
                data = {
                    'message': message_text
                }
                # No files parameter - just send data only
                
                print(f"   Status: Uploading message only...")
                response = requests.post(
                    self.upload_url,
                    data=data,  # Only data, no files
                    timeout=30
                )
            
            # Handle file path input
            elif isinstance(image_input, str):
                if not os.path.exists(image_input):
                    return {'error': f'Image file not found: {image_input}'}
                
                file_size = os.path.getsize(image_input)
                image_name = os.path.basename(image_input)
                
                print(f"📤 SENDING MESSAGE + IMAGE TO RASPBERRY PI")
                print(f"   Target: {self.upload_url}")
                print(f"   Image: {image_name} ({file_size:,} bytes)")
                print(f"   Message: {message_text}")
                print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Prepare files and data for file path
                with open(image_input, 'rb') as image_file:
                    files = {
                        'image': (image_name, image_file, 'image/jpeg')
                    }
                    data = {
                        'message': message_text
                    }
                    
                    # Send POST request
                    print(f"   Status: Uploading...")
                    response = requests.post(
                        self.upload_url,
                        files=files,
                        data=data,
                        timeout=30
                    )
            
            # Handle PIL Image input
            else:
                # It's a PIL Image object
                # Convert PIL Image to bytes
                img_buffer = io.BytesIO()
                image_input.save(img_buffer, format='JPEG')
                img_buffer.seek(0)
                
                # Get buffer size for display
                buffer_size = len(img_buffer.getvalue())
                
                print(f"📤 SENDING MESSAGE + IMAGE TO RASPBERRY PI")
                print(f"   Target: {self.upload_url}")
                print(f"   Image: PIL Image ({buffer_size:,} bytes)")
                print(f"   Message: {message_text}")
                print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Prepare files and data for PIL Image
                files = {
                    'image': ('pil_image.jpg', img_buffer, 'image/jpeg')
                }
                data = {
                    'message': message_text
                }
                
                # Send POST request
                print(f"   Status: Uploading...")
                response = requests.post(
                    self.upload_url,
                    files=files,
                    data=data,
                    timeout=30
                )
            
            # Process response
            if response.status_code == 200:
                result = response.json()
                success_type = "MESSAGE ONLY" if image_input is None else "MESSAGE + IMAGE"
                print(f"   Status: ✓ {success_type} SUCCESS!")
                print(f"   Server response: {result.get('message', 'OK')}")
                
                # Only show filename if image was sent
                if image_input is not None and 'filename' in result:
                    print(f"   Filename on Pi: {result.get('filename', 'Unknown')}")
                
                return result
            else:
                error_msg = f"Server error {response.status_code}: {response.text}"
                print(f"   Status: ✗ FAILED - {error_msg}")
                return {'error': error_msg}
                    
        except requests.exceptions.ConnectionError:
            error_msg = f"Cannot connect to Pi at {self.pi_ip}:{self.port}. Check IP address and network."
            print(f"   Status: ✗ CONNECTION FAILED")
            print(f"   Error: {error_msg}")
            return {'error': error_msg}
            
        except requests.exceptions.Timeout:
            error_msg = "Upload timed out. Check network connection or try smaller image."
            print(f"   Status: ✗ TIMEOUT")
            print(f"   Error: {error_msg}")
            return {'error': error_msg}
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"   Status: ✗ ERROR")
            print(f"   Error: {error_msg}")
            return {'error': error_msg}
    
    def check_status(self):
        """
        Check if the Pi server is running and get status info
        
        Returns:
            dict: Status information or error
        """
        try:
            print(f"🔍 CHECKING RASPBERRY PI STATUS")
            print(f"   Target: {self.status_url}")
            
            response = requests.get(self.status_url, timeout=10)
            
            if response.status_code == 200:
                status = response.json()
                print(f"   Status: ✓ ONLINE")
                print(f"   Server: {status.get('server', 'Unknown')}")
                print(f"   Features: Message only ✓, Message + Image ✓")
                return status
            else:
                error_msg = f"Status check failed: {response.status_code}"
                print(f"   Status: ✗ ERROR - {error_msg}")
                return {'error': error_msg}
                
        except requests.exceptions.ConnectionError:
            error_msg = f"Cannot connect to Pi at {self.pi_ip}:{self.port}"
            print(f"   Status: ✗ OFFLINE")
            print(f"   Error: {error_msg}")
            return {'error': error_msg}
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"   Status: ✗ ERROR - {error_msg}")
            return {'error': error_msg}
