# all the imports
from flask import Flask, render_template
from configparser import ConfigParser

# instantiate
config = ConfigParser()
# parse existing file
try:
	config.read('logviewer.ini')
	# read values from a section
	logfile = config.get('DEFAULT', 'logfile')
	ip = config.get('DEFAULT', 'ip')
except:
	from initial import config_gen
	config_gen()


app = Flask(__name__)

@app.route('/viewlog')
def show_log():
    with open(logfile,'r') as f:
        data = f.read().split('\n')
        data.reverse()	# reverse the timeline sorting order
#    results = [ if line.find('188.') == True for line in data ]
    return render_template('logs.html', logs=data)

if __name__ == '__main__':
    app.run(debug=True)