from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

WINDOW_SIZE = 10
test_server_url = "20.244.56.144/test"  
auth_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzE3MDc3MTc0LCJpYXQiOjE3MTcwNzY4NzQsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjllM2U1YmFmLWZlYzAtNGVjMS1iM2NiLTY3YTJmYWY2ODc4NSIsInN1YiI6InNyZWVqYWtvZGl0YWxhQGdtYWlsLmNvbSJ9LCJjb21wYW55TmFtZSI6Iktlc2hhdiBtZW1vcmlhbCBpbnN0aXR1dGUgb2YgdGVjaG5vbG9neSIsImNsaWVudElEIjoiOWUzZTViYWYtZmVjMC00ZWMxLWIzY2ItNjdhMmZhZjY4Nzg1IiwiY2xpZW50U2VjcmV0IjoiRVR2VlZCZ2R4VkdTZklGaSIsIm93bmVyTmFtZSI6IlNyZWVqYSBLb2RpdGFsYSIsIm93bmVyRW1haWwiOiJzcmVlamFrb2RpdGFsYUBnbWFpbC5jb20iLCJyb2xsTm8iOiIyMUJEMUEwNTRWIn0.4H7vnEHweVCSYHgreuHbgO-eRBR8qCkjOkMajJzB0sA"  # Replace with the actual auth key
window = []

@app.route('/numbers/<string:number_id>', methods=['GET'])
def get_numbers(number_id):
    if number_id not in ['p', 'f', 'e', 'r']:
        return jsonify({"error": "Invalid number ID"}), 400
    global window
    prev_state = list(window)  
    if number_id=='p':
        op_string="primes"
    elif number_id=='f':
        op_string="fibo"
    elif number_id=='e':
        op_string="even"
    elif number_id=='r':
        op_string="rand"

    headers = {"Authorization": f"Bearer {auth_key}"}
    try:
        response = requests.get(f"{test_server_url}/{op_string}", headers=headers, timeout=0.5)
        response.raise_for_status()
        numbers = response.json().get('numbers', [])
    except requests.RequestException:
        return jsonify({"error": "failed to fetch from test server"}), 500

    unique_numbers = set(window)
    new_numbers = []
    for number in numbers:
        if number not in unique_numbers:
            new_numbers.append(number)
            unique_numbers.add(number)

    window.extend(new_numbers)
    if len(window) > WINDOW_SIZE:
        window = window[-WINDOW_SIZE:]

    if window:
        avg = sum(window) / len(window)
    else:
        avg = 0.0

    return jsonify({
        "numbers": numbers,
        "windowPrevState": prev_state,
        "windowCurrState": window,
        "avg": round(avg, 2)
    }), 200

if __name__ == '__main__':
    try:
        app.run("localhost", port=9876,debug=True)
    except Exception as e:
        print(f"err creating app-{e}")
