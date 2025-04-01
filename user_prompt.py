# Contact Form Submission Script
# This script prompts the user for input regarding a contact form submission process.
# It collects the path to a text file containing URLs, an email address, a phone number,
# a message to send, and a delay between requests. The script then returns this information
# in a dictionary format.
def get_user_inputs():
    print("=== Contact Form Submission Script ===")
    txt_file = input("Enter the path to your .txt file with URLs (e.g. websites.txt): ").strip()
    email = input("Enter the email address to use in forms: ").strip()
    phone = input("Enter the phone number to use in forms: ").strip()
    message = input("Enter the message to send in the contact forms: ").strip()
    
    delay = input("Enter delay (in seconds) between requests [default = 3]: ").strip()
    delay = int(delay) if delay.isdigit() else 3  # Default to 3 seconds if left blank

    return {
        "txt_file": txt_file,
        "email": email,
        "phone": phone,
        "message": message,
        "delay": delay
    }

# Main function to execute the script
if __name__ == "__main__":
    config = get_user_inputs()
    print("\nUser Input Summary:")
    for key, value in config.items():
        print(f"{key}: {value}")