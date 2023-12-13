# import socket
# import base64
# import getpass
# import os
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email import encoders
# import ssl
# from config import SERVER_ADDRESS, USERNAME, PASSWORD, SMTP_server, SMTP, POP_server, POP3, Autoload

# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# class MailClient:
#     def __init__(self, SERVER_ADDRESS, USERNAME, PASSWORD, SMTP_server, SMTP, POP_server, POP3, Autoload):
#         self.server_address = SERVER_ADDRESS
#         self.username = USERNAME
#         self.password = PASSWORD
#         self.stmp_server = SMTP_server 
#         self.stmp = SMTP 
#         print(f"Connecting to {self.stmp_server} on port {self.stmp}")
#         self.pop_server = POP_server
#         self.pop3 = POP3
#         self.autoload = Autoload
#         self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.client_socket.connect(SERVER_ADDRESS)
#         self.run_menu()

#     def run_menu(self):
#         try:
#             while True:
#                 print("\nVui lòng chọn Menu:")
#                 print("1. Để gửi email")
#                 print("2. Để xem danh sách các email đã nhận")
#                 print("3. Để xem nội dung email")
#                 print("4. Để lọc và di chuyển email")
#                 print("5. Để thoát")
#                 choice = input("Nhập lựa chọn của bạn: ")

#                 if choice == '1':
#                     self.send_email()
#                 elif choice == '2':
#                     self.fetch_emails()
#                 elif choice == '3':
#                     self.fetch_email_content()
#                 elif choice == '4':
#                     self.filter_and_move()
#                 elif choice == '5':
#                     self.send_command("QUIT\r\n")
#                     print("Tạm biệt!")
#                     break
#                 else:
#                     print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
#         finally:
#             self.client_socket.close()
#     def start_tls(self):
#         try:
#             self.send_command(f"EHLO {self.stmp_server}\r\n")
#             response = self.client_socket.recv(1024).decode()
#             print(response)

#             self.send_command("STARTTLS\r\n")
#             response = self.client_socket.recv(1024).decode()
#             print(response)

#             context = ssl.create_default_context()
#             self.client_socket = context.wrap_socket(self.client_socket, server_hostname=self.stmp_server)
#         except Exception as e:
#             print(f"Error starting TLS: {e}")
    
#     def send_command(self, command):
#         self.client_socket.sendall(command.encode())
#         response = self.client_socket.recv(1024).decode()
#         print(response)

#     def send_email(self):
#         # self.start_tls()

#         sender_email = self.username
#         sender_password = self.password
#         to_address = input("Enter recipient email address: ")
#         cc_address = input("Enter CC email address (leave blank if none): ")
#         bcc_address = input("Enter BCC email address (leave blank if none): ")
#         email_subject = input("Enter email subject: ")
#         email_body = input("Enter email body: ")

#         attachment_paths = []
#         for i in range(3):
#             attachment = input(f"Enter path to attachment {i + 1} (leave blank if none): ")
#             if attachment:
#                 attachment_paths.append(attachment)

#         # # Danh sách file đính kèm
#         # attachments = self.get_attachments()

#         try:
#             # Connect to SMTP server
#             with socket.create_connection((self.stmp_server, self.stmp)) as server_socket:
#                 server_socket = ssl.wrap_socket(server_socket, ssl_version=ssl.PROTOCOL_TLSv1)
#                 server_socket.sendall(b"HELO example.com\r\n")
#                 # ...

#                 # Authenticate
#                 server_socket.sendall(b"AUTH LOGIN\r\n")
#                 server_socket.sendall(base64.b64encode(sender_email.encode()) + b"\r\n")
#                 server_socket.sendall(base64.b64encode(sender_password.encode()) + b"\r\n")

#                 # Compose email
#                 msg = MIMEMultipart()
#                 msg["From"] = sender_email
#                 msg["To"] = to_address
#                 if cc_address:
#                     msg["Cc"] = cc_address
#                 if bcc_address:
#                     msg["Bcc"] = bcc_address
#                 msg["Subject"] = email_subject
#                 msg.attach(MIMEText(email_body, "plain"))

#                 for attachment in attachment_paths:
#                     with open(attachment, "rb") as file:
#                         part = MIMEBase('application', 'octet-stream')
#                         part.set_payload(file.read())
#                         encoders.encode_base64(part)
#                         part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment)}"')
#                         msg.attach(part)

#                         # Send email
#                         server_socket.sendall(f"MAIL FROM: {sender_password}\r\n".encode())
#                         server_socket.sendall(f"RCPT TO: {to_address}\r\n".encode())
#                         if cc_address:
#                             server_socket.sendall(f"RCPT TO: {cc_address}\r\n".encode())
#                         if bcc_address:
#                             server_socket.sendall(f"RCPT TO: {bcc_address}\r\n".encode())
#                         server_socket.sendall(b"DATA\r\n")
#                         server_socket.sendall(msg.as_string().encode())
#                         server_socket.sendall(b".\r\n")

#                     print("Email sent successfully.")
#         except Exception as e:
#             print(f"Error sending email: {e}")

#     def get_attachments(self):
#         attachments = []
#         while True:
#             attachment_path = input("Nhập đường dẫn đến file đính kèm (nhập để bỏ qua): ")
#             if not attachment_path:
#                 break

#             # Kiểm tra kích thước file
#             if os.path.exists(attachment_path) and os.path.getsize(attachment_path) <= (3 * 1024 * 1024):  # 3MB
#                 attachments.append(attachment_path)
#             else:
#                 print("File không tồn tại hoặc vượt quá dung lượng cho phép.")

#             if len(attachments) >= 3:
#                 print("Đã đạt đến giới hạn số lượng file đính kèm (3).")
#                 break

#         return attachments

#     def send_attachment(self, attachment_path):
#         try:
#             with open(attachment_path, 'rb') as file:
#                 file_data = base64.b64encode(file.read()).decode()
#                 self.send_command(f"\r\nAttachment: {os.path.basename(attachment_path)}\r\n{file_data}\r\n")
#         except FileNotFoundError:
#             print(f"File {attachment_path} không tồn tại. Vui lòng kiểm tra lại.")


#     def fetch_emails(self):
#         self.send_command("FETCH\r\n")

#     def fetch_email_content(self):
#         email_id = int(input("Nhập ID của email cần xem: "))
#         self.send_command(f"FETCH CONTENT {email_id}\r\n")

#     def filter_and_move(self):
#         criteria = input("Nhập tiêu chí lọc email (contains): ")
#         keyword = input("Nhập từ khóa lọc: ")
#         folder = input("Nhập tên thư mục muốn di chuyển: ")
#         self.send_command(f"FILTER {criteria} {keyword} {folder}\r\n")

# if __name__ == "__main__":
#     mail_client = MailClient(SERVER_ADDRESS, USERNAME, PASSWORD, SMTP_server, SMTP, POP_server, POP3, Autoload)
# client.py
import socket
import os
from config import SERVER_ADDRESS, SMTP_PORT, POP3_PORT, USERNAME, PASSWORD, FILTER_RULES

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
            client.send(f"RCPT TO: {addr}\r\n".encode())
            response = client.recv(1024).decode()
            print("Server response:", response)

        # Gửi lệnh DATA
        print("Sending DATA command...")
        client.send(b"DATA\r\n")
        response = client.recv(1024).decode()
        print("Server response:", response)

        # Xây dựng nội dung email với danh sách người nhận
        
        if bcc_addresses:
            if to_addresses_list_to_cc:
                for i in range(len(to_addresses_list_to_cc)):
                    to_address_item = to_addresses_list_to_cc[i]
                    to_addresses_list_to_cc_temp = filter(lambda x: x != to_address_item, to_addresses_list_to_cc)
                    email_content = f"""From: {USERNAME}\r\nTo: {to_address_item}, {', '.join(to_addresses_list_to_cc_temp)}\r\nSubject: {email_subject}\r\n\r\n{email_body}\r\n"""
                    client.sendall(email_content.encode())
                for bcc_address in bcc_addresses:
                    email_content = f"""From: {USERNAME}\r\nTo: {bcc_address}\r\nSubject: {email_subject}\r\nBody: {email_body}\r\n"""
                    client.sendall(email_content.encode())
            else:
                for to_address_item in to_addresses_list:
                    email_content = f"""From: {USERNAME}\r\nTo: {to_address_item}\r\nSubject: {email_subject}\r\nBody: {email_body}\r\n"""
                    client.sendall(email_content.encode())
        else:
            for to_address_item in to_addresses_list_to_cc:
                email_content = f"""From: {USERNAME}\r\nTo: {', '.join(to_addresses_list_to_cc)}\r\nSubject: {email_subject}\r\n\r\n{email_body}\r\n"""
                client.sendall(email_content.encode())


        # Đính kèm các file
        for attachment_path in attachment_paths:
            client.sendall(b"Attachment data:\r\n")
            if attachment_path:  # Kiểm tra xem có đường dẫn được nhập không
                try:
                    with open(attachment_path, "rb") as attachment_file:
                        attachment_data = attachment_file.read()
                        attachment_filename = os.path.basename(attachment_path)

                        # Gửi lệnh để bắt đầu đính kèm file
                        client.sendall(f"Content-Type: application/octet-stream; name={attachment_filename}\r\n".encode())
                        client.sendall(f"Content-Disposition: attachment; filename={attachment_filename}\r\n".encode())
                        client.sendall(b"\r\n")

                        # Gửi dữ liệu của file đính kèm
                        client.sendall(attachment_data)

                except FileNotFoundError:
                    print(f"Error: File not found - {attachment_path}")
                    break  # Thoát khỏi vòng lặp nếu có lỗi
            else:
                print("No attachment path provided.")

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
        if "500" in response:
            print("Server returned an error:", response)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.close()

def retrieve_email(username, password):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_ADDRESS, POP3_PORT))

        # Read previously downloaded UIDLs from a file
        try:
            with open("downloaded_uidls.txt", "r") as file:
                downloaded_uidls = set(file.read().splitlines())
        except FileNotFoundError:
            downloaded_uidls = set()

        # Send POP3 commands
        client.sendall(f"USER {username}\r\n".encode())
        client.sendall(f"PASS {password}\r\n".encode())
        client.sendall(b"UIDL\r\n")  # Retrieve unique identifiers for each email

        # Receive email UIDL list
        email_uidl_response = client.recv(1024).decode()
        print("Received email UIDL list:", email_uidl_response)

        # Check if the response starts with "+OK"
        if email_uidl_response.startswith("+OK"):
            # Extract the number of emails using a more robust method
            email_uidl_lines = email_uidl_response.split("\r\n")
            num_emails = len(email_uidl_lines) - 2  # Subtract 2 for the "+OK" line and the empty line at the end
            print("Number of emails:", num_emails)

            # Check if there are any new emails
            new_uidls = [line.split()[1] for line in email_uidl_lines[1:-1]]
            new_uidls = set(new_uidls) - downloaded_uidls

            if not new_uidls:
                print("No new emails to retrieve.")
                return

            # Retrieve each new email
            for uidl in new_uidls:
                client.sendall(f"RETR {uidl}\r\n".encode())
                email_data = b""
                while True:
                    line = client.recv(1024)
                    if line.strip() == b".":
                        break
                    email_data += line

                # Process the email data as needed
                print(f"Received email {uidl} data:", email_data.decode())

            # Update the downloaded UIDLs file
            downloaded_uidls.update(new_uidls)
            with open("downloaded_uidls.txt", "a") as file:
                for uidl in new_uidls:
                    file.write(uidl + "\n")

        else:
            print("Failed to retrieve email UIDL list.")
            return

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.close()


def apply_filters(email):
    for rule in FILTER_RULES:
        if rule["type"] == "from" and any(sender in email["from"] for sender in rule["addresses"]):
            return rule["folder"]
        elif rule["type"] == "subject" and any(keyword in email["subject"] for keyword in rule["keywords"]):
            return rule["folder"]
        elif rule["type"] == "content" and any(keyword in email["body"] for keyword in rule["keywords"]):
            return rule["folder"]
        elif rule["type"] == "spam" and (any(keyword in email["subject"] for keyword in rule["keywords"]) or any(keyword in email["body"] for keyword in rule["keywords"])):
            return rule["folder"]
    return "Inbox"  # Nếu không khớp với bất kỳ quy tắc nào, đưa vào thư mục Inbox

    # Ví dụ về cách sử dụng
    email_data = {
        "from": "ahihi@testing.com",
        "subject": "Urgent report",
        "body": "Please find the attached report ASAP.",
    }

    folder = apply_filters(email_data)
    print(f"Move email to folder: {folder}")


if __name__ == "__main__":
    while True:
        print("Menu:")
        print("1. Send Email")
        print("2. Retrieve Email")
        print("3. Exit")

        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            # Nhập thông tin và gửi email
            to_address = input("To address: ")
            cc_addresses = input("CC addresses (comma-separated, optional): ").split(',')
            bcc_addresses = input("BCC addresses (comma-separated, optional): ").split(',')
            email_subject = input("Email subject: ")
            email_body = input("Email body: ")
            attachment_paths = input("Attachment paths (comma-separated, optional): ").split(',')
            send_email(to_address, cc_addresses, bcc_addresses, email_subject, email_body, attachment_paths)

        elif choice == '2':
            # Lấy email
            retrieve_email(USERNAME, PASSWORD)

        elif choice == '3':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")



