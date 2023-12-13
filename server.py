# import socket

# from config import SERVER_ADDRESS, USERNAME, PASSWORD, SMTP_server, SMTP, POP_server, POP3, Autoload

# class MailServer:
#     def __init__(self, SERVER_ADDRESS):
#         self.server_address = SERVER_ADDRESS;
#         self.emails = []
#         self.users = {}

#     def start_server(self):
#         server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server_socket.bind(SERVER_ADDRESS)
#         server_socket.listen(5)
#         print("Mail Server listening on {}:{}".format(*SERVER_ADDRESS))

#         while True:
#             client_socket, client_address = server_socket.accept()
#             print("Accepted connection from {}:{}".format(*client_address))
#             self.handle_client(client_socket)

#     def handle_client(self, client_socket):
#         try:
#             while True:
#                 data = client_socket.recv(1024).decode()
#                 print("Received:", data)

#                 # Process client commands
#                 if "SEND" in data:
#                     client_socket.sendall("250 OK\r\n".encode())
#                     self.receive_email(client_socket)
#                 elif "FETCH" in data:
#                     email_list = "\r\n".join(self.emails)
#                     client_socket.sendall(email_list.encode())
#                 elif "VIEW" in data:
#                     # Process VIEW command here (for displaying email content)
#                     pass
#                 elif "FILTER" in data:
#                     # Process FILTER command here (for filtering and moving emails)
#                     pass
#                 elif "EXIT" in data:
#                     print("Client disconnected.")
#                     break
#                 else:
#                     client_socket.sendall("500 Command not recognized\r\n".encode())
#         except Exception as e:
#             print(f"Error handling client: {e}")
#         finally:
#             client_socket.close()

#     def receive_email(self, client_socket):
#         client_socket.sendall("354 Start mail input; end with <CRLF>.<CRLF>\r\n".encode())
#         email_data = ""
#         while True:
#             line = client_socket.recv(1024).decode()
#             if line.strip() == ".":
#                 break
#             email_data += line
#         self.emails.append(email_data)
#         client_socket.sendall("250 OK\r\n".encode())

# if __name__ == "__main__":
#     mail_server = MailServer(SERVER_ADDRESS)
#     mail_server.start_server()

# server.py
# import socket
# import threading

# from config import SERVER_ADDRESS, SMTP_PORT, POP3_PORT, USERNAME, FILTER_RULES

# def handle_client(client_socket):
#     try:
#         # Send welcome message
#         client_socket.send(b"220 Welcome to the SMTP server\r\n")

#         while True:
#             command = client_socket.recv(1024).decode()
#             if not command:
#                 break

#             if command.startswith("EHLO"):
#                 client_socket.send(b"250 Hello\r\n")
#             elif command.startswith("MAIL FROM"):
#                 client_socket.send(b"250 OK\r\n")
#             elif command.startswith("RCPT TO"):
#                 client_socket.send(b"250 OK\r\n")
#             elif command.startswith("DATA"):
#                 client_socket.send(b"354 Start mail input; end with <CRLF>.<CRLF>\r\n")
#                 data = client_socket.recv(1024).decode()
#                 print("Received email data:", data)
#                 client_socket.send(b"250 OK\r\n")
#             elif command.startswith("QUIT"):
#                 client_socket.send(b"221 Bye\r\n")
#                 break
#             else:
#                 client_socket.send(b"500 Command not recognized\r\n")

#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         client_socket.close()

# def main():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((SERVER_ADDRESS, SMTP_PORT))
#     server.listen(5)

#     print(f"SMTP Server listening on {SERVER_ADDRESS}:{SMTP_PORT}")

#     while True:
#         client_socket, client_address = server.accept()
#         print(f"Accepted connection from {client_address}")

#         client_handler = threading.Thread(target=handle_client, args=(client_socket,))
#         client_handler.start()

# if __name__ == "__main__":
#     main()

