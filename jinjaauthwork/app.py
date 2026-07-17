from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

logged_in = False

@app.route("/", methods=["GET", "POST"])
def login():
    global logged_in

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin":
            logged_in = True
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid Credentials"
        )

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if not logged_in:
        return redirect(url_for("login"))

    api_keys = [
        "ABC123",
        "XYZ456"
    ]

    return render_template(
        "dashboardwithauth.html",
        user="admin",
        api_keys=api_keys
    )


@app.route("/logout")
def logout():
    global logged_in
    logged_in = False
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
