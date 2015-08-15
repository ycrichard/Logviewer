# all the imports
from flask import Flask, render_template, request
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
	# ip = config.get('DEFAULT', 'ip')
except:
	from initial import config_gen
	config_gen()


app = Flask(__name__)

@app.route('/viewlog')
def show_log():	
    with open(logfile,'r') as f:
    	data = f.readlines()
    # get ip address from request user
    ip = request.remote_addr
    results = [ line for line in data if line.find(ip) >=0 ]
    results.reverse()	# reverse the timeline order
    # user agent
    UA_string  = request.user_agent.string 
    return render_template('logs.html', logs=results, ip=ip, UA=UA_string, len=len(results))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)