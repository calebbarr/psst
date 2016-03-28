from flask import Flask,request,render_template,g,url_for,session
from flask.ext.cache import Cache
import os,string,json
from flask_bootstrap import Bootstrap
import requests
from random import randint,SystemRandom
from utils import head,tail
from itertools import takewhile

#TODO add SSL

server = Flask(__name__,static_url_path='/static')
TTL = 2 * 120 # 2 minutes
DEBUG = debug=os.getenv("PORT") == None

# i tried to make this prettier honestly ... bit.ly/1RdJ2Gv
@server.route('/', methods=['POST','GET'])
def entry():
    if(request.method=="POST"):
        try:
            tokens = request.form['text'].split()
            if(tokens[0] == "help"):
                raise
            session_key = generate_key()
            server.cache.set(session_key,dict(request.form,**parse_command(tokens)))
            return "psst! type your message here: {url}\n".format(url=url_for("ui", key=session_key,_external=True))
        except Exception as e:
            if(DEBUG):
                print e
            return help()
    else:
        return render_template("secret.html", link="/")

def parse_command(tokens):
    ttl = TTL
    if(tokens[0].isdigit()):
        ttl = int(tokens[0])
        tokens = tokens[1:]
    recipients = get_recipients(tokens)
    message = _get_message(recipients,tokens)
    return {
        'ttl': min(ttl,60*120),
        'recipients': recipients,
        'message': message
    }

def help():
    return " ".join([
        "psst! did you know your boss can read your messages?  send super secret messages with /psst!\n",
        "usage (all arguments are optional):\n",
        "/psst",
        "<TTL> (in minutes, default is 2 -- max is 60)",
        "<recepients>",
        "<non-secret message (could be a password hint)>\n"
        "e.g. /psst 5 @user1 @user2 MORE LIKE BOROPHYLL"
    ])

def generate_key(n=randint(6,12)):
    return ''.join(SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))
    
def paste_url(response):
    paste_id = response.text[response.text\
    .find("<h1>paste id <code>")+len("<h1>paste id <code>"):response.text.find("</code></h1>\n")]
    return "https://pastee.org/{id}".format(id=paste_id)

@server.route('/psst/<key>', methods=['GET'])
def ui(key):
    try:
        session_data = server.cache.get(key)
        print "these are names: {names}".format(names=head(session_data['recipients']))
        print "these are session_data['recipients']: {names}".format(names=session_data['recipients'])
        return render_template('psst.html', names=session_data['recipients'], also_to=also_to(tail(session_data['recipients'])),key=key)
    except:
        return render_template("secret.html", link="/")

@server.route('/psst/<key>', methods=['POST'])
def whisper(key):
    try:
        session_data = server.cache.get(key)
        data = {'content': request.form['message'], 'lexer': 'text', 'ttl': session_data['ttl'], 'encrypt': 'on', 'key': request.form['password']}
        paste = paste_url(requests.post('https://pastee.org/submit', data=data ))
        outgoing = {
            "response_type": "in_channel",
            "text": "@{sender}: psst! {message}\n{url}".format(url=paste,message=session_data['message'],sender=str(session_data['user_name'][0]))
        }
        requests.post(session_data['response_url'][0],data=json.dumps(outgoing))
        return render_template("secret.html",link=paste)
    except:
        return render_template("secret.html", link="/")

def also_to(names):
    return " and "+" and ".join(names[1:]) if len(names) > 1 else []

def get_recipients(tokens,marker="." if(DEBUG) else "@"):
    return list(takewhile(lambda x: x.startswith(marker), tokens))
    
def _get_message(recipients,tokens):
    return " ".join(tokens[len(recipients):])

def run():
    Bootstrap(server)
    server.cache = Cache(server,config={'CACHE_TYPE': 'simple'})
    server.secret_key = generate_key()
    server.run(host="0.0.0.0", port=int(os.getenv("PORT",5000)), debug=DEBUG)

if __name__ == "__main__":
    run()