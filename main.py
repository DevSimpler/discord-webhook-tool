import discord_webhook
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# Global variables to store the webhook URLs and message formatting options
WEBHOOK_URLS = []  # Store multiple webhook URLs
WEBHOOK_URL = ""   # Currently selected webhook URL
MESSAGE_COLOR = "" # Message color (for embeds)

def set_webhook_url():
    global WEBHOOK_URL
    url = webhook_entry.get()
    WEBHOOK_URLS.append(url)  # Add the URL to the list
    update_webhook_list()     # Update the listbox
    set_current_webhook(url)  # Set the current webhook

def update_webhook_list():
    webhook_listbox.delete(0, tk.END)  # Clear the listbox
    for url in WEBHOOK_URLS:
        webhook_listbox.insert(tk.END, url)  # Insert URLs into the listbox

def set_current_webhook(url):
    global WEBHOOK_URL
    WEBHOOK_URL = url

def set_message_color(color):
    global MESSAGE_COLOR
    MESSAGE_COLOR = color

def send_message():
    message_type = message_type_var.get()
    content = message_content_entry.get()

    if message_type == "Text":
        webhook = discord_webhook.DiscordWebhook(url=WEBHOOK_URL, content=content)
    elif message_type == "Embed":
        embed = discord_webhook.DiscordEmbed(description=content)
        if MESSAGE_COLOR:
            embed.set_color(MESSAGE_COLOR)  # Set message color
        webhook = discord_webhook.DiscordWebhook(url=WEBHOOK_URL, embeds=[embed])
    elif message_type == "File":
        file_path = file_label.cget("text")
        if file_path:
            with open(file_path, "rb") as file:
                webhook = discord_webhook.DiscordWebhook(url=WEBHOOK_URL)
                webhook.add_file(file.read(), filename=file_path)
        else:
            return
    else:
        return

    webhook.execute()

def browse_file():
    message_type = message_type_var.get()
    file_path = filedialog.askopenfilename()
    file_label.config(text=file_path)

    # Hide the browse button when the message type is not "File"
    if message_type != "File":
        browse_button.pack_forget()
    else:
        browse_button.pack(side=tk.LEFT, padx=5)  # Display the button on the left side with padding


# Create the main window
root = tk.Tk()
root.title("Webhook Multi")


# Create a frame for webhook URL input
webhook_frame = ttk.Frame(root)
webhook_frame.pack(padx=10, pady=10)

webhook_entry = ttk.Entry(webhook_frame, width=40)
webhook_entry.pack()

set_webhook_button = ttk.Button(webhook_frame, text="Add Webhook URL", command=set_webhook_url)
set_webhook_button.pack(pady=5)

# Create a listbox to display added webhook URLs
webhook_listbox = tk.Listbox(webhook_frame, width=40)
webhook_listbox.pack()
webhook_listbox.bind('<<ListboxSelect>>', lambda event: set_current_webhook(webhook_listbox.get(webhook_listbox.curselection())))

# Create a label to instruct the user to click on the webhook URL
click_label = ttk.Label(webhook_frame, text="Click on the Webhook URL you want to message from you can add multiple webhooks: ")
click_label.pack()

# Create a frame for message options
message_frame = ttk.Frame(root)
message_frame.pack(padx=10, pady=10)

message_type_var = tk.StringVar(value="Text")

message_type_label = ttk.Label(message_frame, text="Message Type:")
message_type_label.pack(anchor="w")

message_type_dropdown = ttk.OptionMenu(message_frame, message_type_var, "Text", "Text", "Embed", "File")
message_type_dropdown.pack()

message_content_label = ttk.Label(message_frame, text="Message Content:")
message_content_label.pack(anchor="w")

message_content_entry = ttk.Entry(message_frame, width=40)
message_content_entry.pack()

# Create a frame for file upload
file_frame = ttk.Frame(root)
file_frame.pack(padx=10, pady=10)

file_label = ttk.Label(file_frame, text="")
file_label.pack(anchor="w")

browse_button = ttk.Button(file_frame, text="Browse File", command=browse_file)
browse_button.pack()

# Create a frame for message sending
send_frame = ttk.Frame(root)
send_frame.pack(pady=10)

send_button = ttk.Button(send_frame, text="Send Message", command=send_message)
send_button.pack()

# Main loop
root.mainloop()

