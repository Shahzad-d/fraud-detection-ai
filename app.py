from flask import Flask, request, render_template
import pickle
import os

app = Flask(__name__)

# 🔥 SAFE MODEL PATH (IMPORTANT FOR RENDER)
try:
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")

    # 👇 ADDED LINE (FILE CHECK)
    print("CHECK MODEL FILE EXISTS:", os.path.exists(model_path))

    model = pickle.load(open(model_path, "rb"))
    print("MODEL LOADED SUCCESSFULLY")

except Exception as e:
    print("MODEL LOAD ERROR:", e)
    model = None

time_map = {"day": 1, "evening": 2, "night": 3}
location_map = {"karachi": 1, "lahore": 2, "islamabad": 3}
device_map = {"mobile": 1, "other": 2}

total = 0
fraud_count = 0
safe_count = 0

@app.route("/", methods=["GET", "POST"])
def home():
    global total, fraud_count, safe_count

    result = ""

    if request.method == "POST":
        try:
            total += 1

            amount = float(request.form.get("amount", 0))
            time = time_map.get(request.form.get("time","day").lower(), 1)
            location = location_map.get(request.form.get("location","karachi").lower(), 1)
            device = device_map.get(request.form.get("device","mobile").lower(), 1)

            if model is None:
                result = "❌ Model not loaded"
            else:
                prediction = model.predict([[amount, time, device, location]])

                if prediction[0] == 1:
                    result = "⚠️ Fraud Transaction!"
                    fraud_count += 1
                else:
                    result = "✅ Safe Transaction"
                    safe_count += 1

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html",
                           result=result,
                           total=total,
                           fraud=fraud_count,
                           safe=safe_count)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)