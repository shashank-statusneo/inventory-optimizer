from flask import Flask
# from flask_restx import api

app = Flask(__name__)

@app.route("/ping")
def ping():
    return True, 200

if __name__ == ("__main__"):
    app.run()
    
    