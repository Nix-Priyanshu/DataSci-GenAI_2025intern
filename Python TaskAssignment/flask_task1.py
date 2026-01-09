from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <body style="font-family: Arial; background-color:black;">
        <center><h1 style="color:lime">Welcome to My Flask Page</h1>
        <hr>
        <p style="color:white; font-size:30px;">Home Page</p></center>
        <p style="color:white; font-size:20px;">Use the following routes:</p>
        
        <p style="color:lime; font-size:18px;">/info</p>
        <p style="color:white; font-size: 15">Format: http://127.0.0.1:5000/<b style="color:red">info?name=yourname&dep=depname&id=yourID</b></p>
        <p style="color:white; font-size: 15">Example: http://127.0.0.1:5000/<b style="color:blue">info?name=Potato&dep=UnderGround&id=123</b></p></center>
        <br>
        
        <p style="color:lime; font-size:18px;">/details</p>
        <p style="color:white; font-size: 15">Format: http://127.0.0.1:5000/<b style="color:red">details?name=yourname&age=yourage</b></p>
        <p style="color:white; font-size: 15">Example: http://127.0.0.1:5000/<b style="color:blue">details?name=Potato&age=5</b></p></center>

    </body>
    </html>

                """

@app.route("/info")
def info():
    name = request.args.get("name")
    dep = request.args.get("dep")
    dep_id = request.args.get("id")

    if name:
        return f"""
        <html>
        <body style="font-family: Arial; background-color:black; padding:40px;">
            <h1 style="color:lime">Hello {name.upper()}</h1>
            <hr>
            <p style="color:white"><b style="color:lime">Department:</b> {dep}</p>
            <p style="color:lime"><b style="color:white">Dep_ID:</b> {dep_id}</p>

            </body>
         </html>
        """
    else:
        return """<center><h2>Please provide a name in the URL</h2>
                            <h2></h2>
                          <p style="font-size: 20">Format: http://127.0.0.1:5000/<b style="color:red">info?name=yourname&dep=depname&id=yourID</b></p>
                          <p style="font-size: 20">Example: http://127.0.0.1:5000/<b style="color:blue">info?name=Potato&dep=UnderGround&id=123</b></p></center>
                          <p>
         """
    
@app.route("/details")
def details():
    name = request.args.get("name")
    age = request.args.get("age")

    if name: 
        return f"""
    <html>
        <body style="font-family: Arial; background-color:black; padding:40px;">
            <h1 style="color:lime">Hello {name.upper()}</h1>
            <hr>
            <p style="color:white"><b style="color:lime">Uppercase:</b> {name.upper()}</p>
            <p style="color:lime"><b style="color:white">Lowercase:</b> {name.lower()}</p>
            <p style="color:white"><b style="color:lime">Reversed:</b> {name[::-1]}</p>
            <p style="color:lime"><b style="color:white">Length:</b> {len(name)} characters</p>
            <p style="color:white"><b style="color:lime">Age:</b> {age}</p>
            <p style="color:lime"><b style="color:white">Colour: </b>Brown</p>
        </body>
    </html>
    """

    else:
        return """<center><h2>Please provide a name in the URL</h2>
                            <h2></h2>
                          <p style="font-size: 20">Format: http://127.0.0.1:5000/<b style="color:red">details?name=yourname&age=yourage</b></p>
                          <p style="font-size: 20">Example: http://127.0.0.1:5000/<b style="color:blue">details?name=Potato&age=5</b></p></center>
                     """

if __name__ == "__main__":
    app.run(debug=True)
