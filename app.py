# all the imports
from flask import Flask, render_template
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

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
        # data = f.read().split('\n')
        data = f.readlines()
    results = [ line for line in data if line.find(ip) >=0 ]
    results.reverse()	# reverse the timeline order
    return render_template('logs.html', logs=results)

if __name__ == '__main__':
    app.run(debug=True)