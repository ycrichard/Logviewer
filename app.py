# all the imports
from flask import Flask, render_template

# configuration
LOGFILE = 'shadowsocks.logs'
# SECRET_KEY = 'qweR'

app = Flask(__name__)

@app.route('/viewlog')
def show_log():
    with open(LOGFILE,'r') as f:
        data = f.read().split('\n')
#    results = [ if line.find('188.') == True for line in data ]
    return render_template('logs.html', logs=data)

if __name__ == '__main__':
    app.run(debug=True)