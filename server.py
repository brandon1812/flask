import os
import csv
import signal
from flask import Flask, render_template, request

app = Flask(__name__)

# File paths
csv_file_path = 'subform.csv'
backup_csv_file_path = 'subform_backup.csv'

# Function to write header row to CSV file
def write_csv_header():
    # Check if the file already exists
    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Name', 'Email', 'Message'])

# Function to backup CSV file
def backup_csv():
    # Copy the content of the original CSV file to the backup file
    with open(csv_file_path, 'r') as original_csv, open(backup_csv_file_path, 'w', newline='') as backup_csv:
        backup_csv.write(original_csv.read())

# Initialize CSV file with header if it doesn't exist
write_csv_header()

@app.route('/')
def home():
    return render_template('index.html')

# This HTML5 template is using one-page, all sections are all in the index.html
# Otherwise, put xx.html files into templates folder, and call them in this pattern
# @app.route("/<string:page_name>")
# def html_page(page_name):
#     return render_template(page_name)

@app.route('/submit-form', methods=['POST'])
def handle_form_submission():
    # Get form data from the request
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Save data to text file (subform.txt)
    with open('subform.txt', 'a') as text_file:
        text_file.write(f'Name: {name}\nEmail: {email}\nMessage: {message}\n\n')

    # Save data to CSV file (subform.csv)
    with open(csv_file_path, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([name, email, message])

    # Your form handling logic goes here
    return "Form submitted successfully"

# Signal handler for backing up CSV file before exiting
def handle_exit(signal, frame):
    print("Backup CSV file before exiting...")
    backup_csv()
    print("Backup completed. Exiting.")
    exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, handle_exit)

if __name__ == '__main__':
    app.run(debug=True)
