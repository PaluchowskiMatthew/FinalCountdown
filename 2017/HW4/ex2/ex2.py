# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, request
import bcrypt

# Initialize the Flask application
app = Flask(__name__)
# app.config['DEBUG'] = True


# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is
# accepting: POST requests in this case
@app.route('/hw4/ex2', methods=['POST'])
def ex2():
    content = request.get_json()
    # print(content)
    if 'user' not in content or 'pass' not in content:
        return ('', 404)
    else:
        password = content['pass'].encode()
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        return (hashed, 200) #.decode("utf-8") #jsonify({"hash": hashed.decode("utf-8") })

# Run the app :)
if __name__ == '__main__':
  app.run(
        host="127.0.0.1",
        port=5000
  )
