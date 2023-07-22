from flask import Flask, jsonify, render_template
import datetime
import pytz

app = Flask(__name__)

def get_match_date():
    match_date_str = "2023-08-11 15:00:00"
    match_date = datetime.datetime.strptime(match_date_str, "%Y-%m-%d %H:%M:%S")
    # Convert the match date to the desired timezone (UTC in this case)
    match_date = pytz.timezone('UTC').localize(match_date)
    return match_date

def get_remaining_time():
    # Get the match date once
    match_date = get_match_date()

    # Get the current time with the same timezone as the match date (UTC)
    current_time = datetime.datetime.now(pytz.timezone('UTC'))

    remaining_time = match_date - current_time

    # return remaining time in seconds
    return max(remaining_time.total_seconds(), 0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/countdown')
def countdown():
    remaining_time = get_remaining_time()
    return jsonify({"remaining_time": int(remaining_time)})

if __name__ == '__main__':
    app.run(debug=True)
