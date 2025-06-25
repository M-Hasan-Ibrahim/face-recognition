# In another Python file
from pi_sender import PiSender

# Create sender instance
sender = PiSender("192.168.137.210")  # Your Pi's IP address

# Send data
result = sender.send_to_pi("download.png", "Second test of the callable class!")

# Check result
if 'error' not in result:
    print("Data sent successfully!")
else:
    print(f"Failed to send: {result['error']}")