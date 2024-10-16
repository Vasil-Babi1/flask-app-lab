from flask import Flask, request, redirect, url_for

app = Flask(__name__)    

@app.route('/')
def main():
    return '<h1>Hello, world!</h1>', 200

@app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent = request.user_agent

    return f"This is your homepage :)  - {agent} " 

@app.route("/hi/<string:name>") #/hi/Vasyl?age
def greetings(name):
    name = name.upper()
    age = request.args.get("age")
    year = 2024 - int(age)

    return f"Welcome, {name}  {year}"

@app.route("/admin")
def admin():
    to_url = url_for("greetings", name="administrator", age = 20, _external=True)
    print(to_url)
    return redirect(to_url)

if __name__ == "__main__":
    app.run()  # Launch built-in web server and run this Flask webapp, debug=True
 
