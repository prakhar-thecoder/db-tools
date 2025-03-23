from flask import Flask, render_template, request
from minimal_cover import find_minimal_cover
from candidate_key import find_ck, find_closure

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')
    
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/ck_can', methods=["GET", "POST"])
def ck_can():
    result = {}
    if request.method == "POST":
        attributes = request.form["attributes"].replace(" ", "").split(",")
        fds_raw = request.form["fds"].split("\n")
        
        fds = []
        for fd in fds_raw:
            if "->" in fd:
                lhs, rhs = fd.split("->")
                lhs = lhs.strip()
                rhs = rhs.strip()
                fds.append((lhs, rhs))
        
        r = set(attributes)
        
        minimal_cover = find_minimal_cover(r, fds)
        candidate_keys = find_ck(r, fds)
        
        closure_attr = request.form.get("closure_attr", "")
        closure_result = find_closure(fds, closure_attr) if closure_attr else "N/A"
        
        result = {
            "minimal_cover": minimal_cover,
            "candidate_keys": candidate_keys,
            "closure": closure_result,
        }

    return render_template("ck_can.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
