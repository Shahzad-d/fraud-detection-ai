from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))

# 🔥 mapping (text → number)
time_map = {"day": 1, "evening": 2, "night": 3}
location_map = {"karachi": 1, "lahore": 2, "islamabad": 3}
device_map = {"mobile": 1, "other": 2}

# 📊 Dashboard counters
total = 0
fraud_count = 0
safe_count = 0

@app.route("/", methods=["GET", "POST"])
def home():
    global total, fraud_count, safe_count

    result = ""

    if request.method == "POST":
        total += 1

        # ✅ get inputs safely
        amount = float(request.form["amount"])
        time = request.form["time"].strip().lower()
        location = request.form["location"].strip().lower()
        device = request.form["device"].strip().lower()

        # ✅ convert text → numbers
        time = time_map.get(time, 1)
        location = location_map.get(location, 1)
        device = device_map.get(device, 1)

        # ✅ prediction
        prediction = model.predict([[amount, time, device, location]])

        if prediction[0] == 1:
            result = "⚠️ Fraud Transaction!"
            fraud_count += 1
        else:
            result = "✅ Safe Transaction"
            safe_count += 1

    return render_template("index.html",
                           result=result,
                           total=total,
                           fraud=fraud_count,
                           safe=safe_count)

if __name__ == "__main__":
    app.run(debug=True)