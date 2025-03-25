from flask import Flask, render_template, request
from minimal_cover import find_minimal_cover
from candidate_key import find_ck, find_closure
from normalization import check_2NF, check_3NF

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


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
        
        candidate_keys = find_ck(r, fds)
        str_attr = ", ".join(attributes)
        str_ck = ", ".join(candidate_keys)
        result = {
            "attributes" : str_attr,
            "candidate_keys": str_ck,
            "fds": fds
        }

    return render_template("ck_can.html", result=result)

@app.route('/attribute_closure', methods=["GET", "POST"])
def attribute_closure():
    result = {}

    if request.method == "POST":
        fds_raw = request.form["fds"].split("\n")
        
        fds = []
        for fd in fds_raw:
            if "->" in fd:
                lhs, rhs = fd.split("->")
                lhs = lhs.strip()
                rhs = rhs.strip()
                fds.append((lhs, rhs))
        
        closure_attr = request.form.get("closure_attr", "")
        closure_result = ", ".join(sorted(find_closure(fds, closure_attr)))
        
        result = {
            "attr": closure_attr,
            "closure": "{ " + closure_result + " }",
            "fds": fds
        }

    return render_template("attribute_closure.html", result=result)

@app.route('/minimal_cover',methods=["GET", "POST"])
def minimal_cover():
    result = {}
    if request.method == "POST":
        attributes = request.form["attributes"].replace(" ", "").split(",")
        fds_raw = request.form["fds"].split("\n")
        
        fds = []
        res_fd = []
        for fd in fds_raw:
            if "->" in fd:
                lhs, rhs = fd.split("->")
                lhs = lhs.strip()
                rhs = rhs.strip()
                fds.append((lhs, rhs))
                res_fd.append((lhs, rhs))
        

        r = set(attributes)
        minimal_cover = find_minimal_cover(r, fds)
        str_attr = ", ".join(attributes)

        result = {
                "attributes" : str_attr,
                "fds" : res_fd,
                "minimal_cover": minimal_cover
        }

    return render_template("minimal.html", result=result)

@app.route('/normalization',methods=["GET", "POST"])
def normalization():
    result = {}

    result_2nf, result_3nf = None, None
    
    if request.method == 'POST':
        attributes = request.form.get("attributes").split(",")
        attributes = [a.strip() for a in attributes]
        attributes = set(attributes)
        fd_input = request.form.get("fds").split("\n")
        
        res_fd =[]
        fd = []
        for f in fd_input:
            lhs, rhs = f.split("->")
            fd.append((lhs.strip(), rhs.strip()))
            res_fd.append((lhs.strip(), rhs.strip()))

        
        result_2nf = check_2NF(attributes, fd)
        print(attributes, fd)
        result_3nf = check_3NF(attributes, fd)
        str_attr = ", ".join(attributes)

        result = {
            "fds" : res_fd,
            "attributes" : str_attr,
            "result_2nf" : result_2nf,
            "2nf": True if len(result_2nf["violating_fds"]) == 0 else False,
            "result_3nf" : result_3nf,
            "3nf": True if len(result_3nf["violating_fds"]) == 0 else False,
        }
    
    return render_template("normalization.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
