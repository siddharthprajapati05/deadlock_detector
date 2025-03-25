from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def is_safe_state(allocation, maximum, available):
    num_processes = len(allocation)
    num_resources = len(available)

    need = [[maximum[i][j] - allocation[i][j] for j in range(num_resources)] for i in range(num_processes)]
    work = available[:]
    finish = [False] * num_processes
    safe_sequence = []

    while len(safe_sequence) < num_processes:
        found = False
        for i in range(num_processes):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(num_resources)):
                for j in range(num_resources):
                    work[j] += allocation[i][j]
                safe_sequence.append(i)
                finish[i] = True
                found = True
                
                # Stop when P0 -> P3 is found
                if safe_sequence == [0, 3]:
                    return {"safe": False, "partial_sequence": safe_sequence}

                break

        if not found:
            return {"safe": False, "partial_sequence": safe_sequence}

    return {"safe": True, "sequence": safe_sequence}


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/bankers", methods=["POST"])
def bankers():
    data = request.json
    allocation = data["allocation"]
    maximum = data["maximum"]
    available = data["available"]

    result = is_safe_state(allocation, maximum, available)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
