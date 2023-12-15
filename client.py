import socket
import os
import re
import time
import email.utils
from config import SERVER_ADDRESS, SMTP_PORT, POP3_PORT, USERNAME, PASSWORD, Autoload, FILTER_RULES, DEFAULT_FOLDER

def send_attachments(client, attachment_paths):
    # Biến để theo dõi tổng dung lượng của các file đính kèm
    total_attachment_size = 0

    # Kiểm tra số lượng file và tổng dung lượng
    max_attachments = 3
    max_attachment_size = 3 * 1024 * 1024  # 3MB

    # Đính kèm các file
    for attachment_path in attachment_paths:
        if max_attachments <= 0 or total_attachment_size >= max_attachment_size:
            print("Exceeded maximum number of attachments or total size. Ignoring additional attachments.")
            break

        client.sendall(b"Attachment data:\r\n")
        if attachment_path:  # Kiểm tra xem có đường dẫn được nhập không
            try:
                with open(attachment_path, "rb") as attachment_file:
                    attachment_data = attachment_file.read()
                    attachment_filename = os.path.basename(attachment_path)
                    attachment_size = len(attachment_data)

                    # Kiểm tra kích thước của file
                    if attachment_size <= max_attachment_size - total_attachment_size:
                        total_attachment_size += attachment_size
                    else:
                        print(f"Error: Exceeded maximum attachment size - {attachment_path}")
                        continue  # Chuyển đến file đính kèm tiếp theo nếu kích thước vượt quá

                    # Giảm số lượng file còn được phép đính kèm
                    max_attachments -= 1

                    # Gửi lệnh để bắt đầu đính kèm file
                    client.sendall(f"Content-Type: application/octet-stream; name={attachment_filename}\r\n".encode())
                    client.sendall(f"Content-Disposition: attachment; filename={attachment_filename}\r\n".encode())
                    client.sendall(b"\r\n")

                    # Gửi dữ liệu của file đính kèm
                    client.sendall(attachment_data)

            except FileNotFoundError:
                print(f"Error: File not found - {attachment_path}")
                continue  # Chuyển đến file đính kèm tiếp theo nếu file không tồn tại

    if total_attachment_size == 0:
        print("No attachment path provided.")

def send_email(to_address, cc_addresses, bcc_addresses, email_subject, email_body, attachment_paths):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_ADDRESS, SMTP_PORT))

        # Nhận lời chào từ server
        response = client.recv(1024).decode()
        print("Server response:", response)

        # Gửi EHLO để bắt đầu phiên giao tiếp
        client.send(b"EHLO example.com\r\n")
        response = client.recv(1024).decode()
        print("Server response:", response)

        # Gửi lệnh MAIL FROM
        client.send(f"MAIL FROM: {USERNAME}\r\n".encode())
        response = client.recv(1024).decode()
        print("Server response:", response)

        # Gửi lệnh RCPT TO
        to_addresses_list = [to_address] + cc_addresses + bcc_addresses
        to_addresses_list_to_cc = [to_address] + cc_addresses
        for addr in to_addresses_list:
            if addr:
                client.send(f"RCPT TO: {addr}\r\n".encode())
                response = client.recv(1024).decode()
                print("Server response:", response)

        # Gửi lệnh DATA
        print("Sending DATA command...")
        client.send(b"DATA\r\n")
        response = client.recv(1024).decode()
        print("Server response:", response)

        # Xây dựng nội dung email với danh sách người nhận
        mime_version = "1.0"
        user_agent = "Your User Agent"
        content_language = "en-US"
        content_type = "text/plain"
        content_transfer_encoding = "quoted-printable"

        if (len(bcc_addresses) != 0):
            if to_addresses_list_to_cc:
                for i in range(len(to_addresses_list_to_cc)):
                    msg_id = email.utils.make_msgid()
                    date = email.utils.formatdate(time.time())
                    to_address_item = to_addresses_list_to_cc[i]
                    to_addresses_list_to_cc_temp = filter(lambda x: x != to_address_item, to_addresses_list_to_cc)
                    email_content = f"Message-ID: {msg_id}\r\n"
                    email_content += f"Date: {date}\r\n"
                    email_content += f"MIME-version: {mime_version}\r\n"
                    email_content += f"User-Agent: {user_agent}\r\n"
                    email_content += f"Content-Language: {content_language}\r\n"
                    email_content += f"To: {to_address_item}, {', '.join(to_addresses_list_to_cc_temp)}\r\n"
                    email_content += f"From: {USERNAME}\r\n"
                    email_content += f"Subject: {email_subject}\r\n"
                    email_content += f"Content-type: {content_type}\r\n"
                    email_content += f"Content-Transfer-Encoding: {content_transfer_encoding}\r\n"
                    email_content += f"Body:\r\n {email_body}\r\n\r\n"
                    client.sendall(email_content.encode())
                for bcc_address in bcc_addresses:
                    msg_id = email.utils.make_msgid()
                    date = email.utils.formatdate(time.time())
                    email_content = f"Message-ID: {msg_id}\r\n"
                    email_content += f"Date: {date}\r\n"
                    email_content += f"MIME-version: {mime_version}\r\n"
                    email_content += f"User-Agent: {user_agent}\r\n"
                    email_content += f"Content-Language: {content_language}\r\n"
                    email_content += f"To: {bcc_address}\r\n"
                    email_content += f"From: {USERNAME}\r\n"
                    email_content += f"Subject: {email_subject}\r\n"
                    email_content += f"Content-type: {content_type}\r\n"
                    email_content += f"Content-Transfer-Encoding: {content_transfer_encoding}\r\n"
                    email_content += f"Body:\r\n {email_body}\r\n\r\n"
                    client.sendall(email_content.encode())
            else:
                for to_address_item in to_addresses_list:
                    msg_id = email.utils.make_msgid()
                    date = email.utils.formatdate(time.time())
                    email_content = f"Message-ID: {msg_id}\r\n"
                    email_content += f"Date: {date}\r\n"
                    email_content += f"MIME-version: {mime_version}\r\n"
                    email_content += f"User-Agent: {user_agent}\r\n"
                    email_content += f"Content-Language: {content_language}\r\n"
                    email_content += f"To: {to_address_item}\r\n"
                    email_content += f"From: {USERNAME}\r\n"
                    email_content += f"Subject: {email_subject}\r\n"
                    email_content += f"Content-type: {content_type}\r\n"
                    email_content += f"Content-Transfer-Encoding: {content_transfer_encoding}\r\n"
                    email_content += f"Body:\r\n {email_body}\r\n\r\n"
                    client.sendall(email_content.encode())
        else:
            if (len(cc_addresses) != 0):
                for i in range(len(to_addresses_list_to_cc)):
                    msg_id = email.utils.make_msgid()
                    date = email.utils.formatdate(time.time())
                    to_address_item = to_addresses_list_to_cc[i]
                    to_addresses_list_to_cc_temp = filter(lambda x: x != to_address_item, to_addresses_list_to_cc)
                    email_content = f"Message-ID: {msg_id}\r\n"
                    email_content += f"Date: {date}\r\n"
                    email_content += f"MIME-version: {mime_version}\r\n"
                    email_content += f"User-Agent: {user_agent}\r\n"
                    email_content += f"Content-Language: {content_language}\r\n"
                    email_content += f"To: {to_address_item}, {', '.join(to_addresses_list_to_cc_temp)}\r\n"
                    email_content += f"From: {USERNAME}\r\n"
                    email_content += f"Subject: {email_subject}\r\n"
                    email_content += f"Content-type: {content_type}\r\n"
                    email_content += f"Content-Transfer-Encoding: {content_transfer_encoding}\r\n"
                    email_content += f"Body:\r\n {email_body}\r\n\r\n"""
                    client.sendall(email_content.encode())
            else:
                msg_id = email.utils.make_msgid()
                date = email.utils.formatdate(time.time())
                email_content = f"Message-ID: {msg_id}\r\n"
                email_content += f"Date: {date}\r\n"
                email_content += f"MIME-version: {mime_version}\r\n"
                email_content += f"User-Agent: {user_agent}\r\n"
                email_content += f"Content-Language: {content_language}\r\n"
                email_content += f"To: {to_address}\r\n"
                email_content += f"From: {USERNAME}\r\n"
                email_content += f"Subject: {email_subject}\r\n"
                email_content += f"Content-type: {content_type}\r\n"
                email_content += f"Content-Transfer-Encoding: {content_transfer_encoding}\r\n"
                email_content += f"Body:\r\n {email_body}\r\n\r\n"
                client.sendall(email_content.encode())


        # Đính kèm các file
        send_attachments(client, attachment_paths)

        # Kết thúc dữ liệu email
        print("Sending end-of-email command...")
        client.send(b"\r\n.\r\n")
        response = client.recv(1024).decode()
        print("Server response:", response)

        # Gửi lệnh QUIT
        print("Sending QUIT command...")
        client.send(b"QUIT\r\n")
        response = client.recv(1024).decode()
        print("Server response:", response)
        client.close()
        if "500" in response:
            print("Server returned an error:", response)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.close()

def retrieve_email_and_retrieve_specific_emails(username, password):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_ADDRESS, POP3_PORT))

        # Send POP3 commands
        client.sendall(f"USER {username}\r\n".encode())
        client.sendall(f"PASS {password}\r\n".encode())
        client.sendall(b"LIST\r\n") # Retrieve a summary of all messages

        # Receive the response to the LIST command
        list_response = b""
        while True:
            line = client.recv(1024)
            list_response += line
            if line.endswith(b".\r\n"):
                break

        # Process the list response as needed
        print("Received email list:", list_response.decode())

        # Get mail with index in above list
        email_index = input("Mail index from above list: ") # replace with the actual email index
        client.send(f'RETR {email_index}\r\n'.encode())
        email_data = client.recv(1024)
        if isinstance(email_data, bytes):
            email_data = email_data.decode('utf-8')
        print(email_data)
        #You may need to implement a function to extract email information (e.g., sender, subject, body) from email_data
        email = process_email_data(email_data)
        mark_email_as_read(email_index)
        # Apply filters and classify email
        folder = move_email_to_folder(email)

        # Print the folder where the email is classified
        print(f"Email index: {email_index} classified into folder: {folder}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.close()

def only_retrieve_email(username, password):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_ADDRESS, POP3_PORT))

        # Send POP3 commands
        client.sendall(f"USER {username}\r\n".encode())
        client.sendall(f"PASS {password}\r\n".encode())
        client.sendall(b"LIST\r\n") # Retrieve a summary of all messages

        # Receive the response to the LIST command
        list_response = b""
        while True:
            line = client.recv(1024)
            list_response += line
            if line.endswith(b".\r\n"):
                break

        # Process the list response as needed
        print("Received email list:", list_response.decode())

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.close()

def process_email_data(email_data):
    from_regex = re.compile(r'From: (.+)')
    to_regex = re.compile(r'To: (.+)')
    subject_regex = re.compile(r'Subject: (.+)')
    body_regex = re.compile(r'Body:(.+?)Attachment data:', re.DOTALL)
    
    # Use regular expressions to find matches
    from_match = from_regex.search(email_data)
    to_match = to_regex.search(email_data)
    subject_match = subject_regex.search(email_data)
    body_match = body_regex.search(email_data)
    
    # Extract data from matches
    from_address = from_match.group(1) if from_match else None
    to_address = to_match.group(1) if to_match else None
    subject = subject_match.group(1) if subject_match else None
    body = body_match.group(1) if body_match else None

    email_info = {"from": from_address, "to": to_address, "subject": subject, "body": body}

    return email_info

def move_email_to_folder(email):
    folder_name = DEFAULT_FOLDER;
    subject_content = email["subject"]
    body_content = email["body"]
    for rule in FILTER_RULES:
        if rule["type"] == "spam":
            for keyword in rule["keywords"]:
                keyword_in_subject = keyword.lower() in subject_content.lower()
                keyword_in_body = keyword.lower() in body_content.lower()
                
                if keyword_in_subject or keyword_in_body:
                    folder_name = rule["folder"]
        else:
            if rule["type"] == "from" and any(address.lower() in email["from"].lower() for address in rule.get("addresses", [])):
                folder_name = rule["folder"]
            elif rule["type"] == "to" and any(address.lower() in email["to"].lower() for address in rule.get("addresses", [])):
                folder_name = rule["folder"]
            elif rule["type"] == "subject" and any(keyword.lower() in subject_content.lower() for keyword in rule.get("keywords", [])):
                folder_name = rule["folder"]
            elif rule["type"] == "content":
                if body_content is not None and any(keyword.lower() in body_content.lower() for keyword in rule.get("keywords", [])):
                    folder_name = rule["folder"]

        
    return folder_name


def mark_email_as_read(email_index):
    try:
        # Check if the email has already been marked as read
        if check_email_read_status(email_index):
            return

        with open("email_states.txt", "a") as state_file:
            # Mark the email as read and write to the file
            state_file.write(f"{email_index} Read\n")

        print(f"Email {email_index} marked as read.")

    except Exception as e:
        print(f"Error marking email as read: {e}")

def check_email_read_status(email_index):
    try:
        with open("email_states.txt", "r") as state_file:
            for line in state_file:
                parts = line.split()
                if len(parts) == 2 and parts[0] == email_index:
                    print("Email has been read")
                    return True  # Email đã được đọc
        
        print("Email has not been read")
        return False  # Email chưa được đọc

    except FileNotFoundError:
        return False  # File không tồn tại, giả sử email chưa được đọc
    except Exception as e:
        print(f"Error checking email status: {e}")
        return False


def email_automatic_download():
    check = True;
    while check:
        only_retrieve_email(USERNAME, PASSWORD)
        check_stop = input("Press Enter to stop auto-retrieving...")
        if check_stop:
            check = False;
        time.sleep(10)

if __name__ == "__main__":

    while True:
        print("Menu:")
        print("1. Send Email")
        print("2. Retrieve Email")
        print("3. Enable/Disable Auto Retrieve Email")
        print("4. Exit")

        choice = input("Enter your choice (1, 2, 3 or 4): ")

        if choice == '1':
            # Nhập thông tin và gửi email
            to_address = input("To address: ")
            cc_addresses_input = input("CC addresses (comma-separated, optional): ")
            bcc_addresses_input = input("BCC addresses (comma-separated, optional): ")

            # Kiểm tra nếu người dùng không nhập gì thì gán danh sách rỗng
            cc_addresses = cc_addresses_input.split(',') if cc_addresses_input else []
            bcc_addresses = bcc_addresses_input.split(',') if bcc_addresses_input else []

            email_subject = input("Email subject: ")
            email_body = input("Email body: ")
            attachment_paths = input("Attachment paths (comma-separated, optional): ").split(',')
            send_email(to_address, cc_addresses, bcc_addresses, email_subject, email_body, attachment_paths)

        elif choice == '2':
            # Lấy email
            retrieve_email_and_retrieve_specific_emails(USERNAME, PASSWORD)

        elif choice == '3':
            email_automatic_download()

        elif choice == '4':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")