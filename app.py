import os.path
import os
import pygame
from flask import Flask, jsonify, render_template
import datetime
import pytz
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

def get_match_date():
    match_date_str = "2023-08-11 15:00:00"
    match_date = datetime.datetime.strptime(match_date_str, "%Y-%m-%d %H:%M:%S")
    return match_date

def get_remaining_time():
    # Get the current time (naive datetime without timezone info)
    current_time = datetime.datetime.now()

    # Get the match date
    match_date = get_match_date()

    remaining_time = match_date - current_time

    # return remaining time in seconds
    return max(remaining_time.total_seconds(), 0)

# function to play the beep tone
def play_beep():
    # Replace the path with the path to your beep sound file
    # Make sure the file is in the "Resources" directory within my project
    beep_sound_path = os.path.join(os.path.dirname(__file__), "resources", "emergency-alarm-with-reverb-29431.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load(beep_sound_path)
    pygame.mixer.music.play()

def send_email_notification():
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'ariembadavy@gmail.com'
    receiver_email = 'ogutud811@gmail.com'
    password = os.environ.get('GMAIL_PASSWORD') # Gets the Gmail password from the environment variable
    # Create the email message

    message = MIMEText("The Premier League has returned!")
    message['Subject'] = 'Premier League Return Notification'
    message['From'] = sender_email
    message['To'] = receiver_email

    # Connect to the Gmail SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, [receiver_email], message.as_string())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/countdown')
def countdown():
    remaining_time = get_remaining_time()
    if remaining_time <= 0:
        play_beep()
        send_email_notification()
    return jsonify({"remaining_time": int(remaining_time)})

if __name__ == '__main__':
    app.run(debug=True)
