# all the imports
from flask import Flask, render_template, url_for, request
import geoip2.database
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

reader = geoip2.database.Reader('static/GeoLite2-City.mmdb')

app = Flask(__name__)

def split_logline(line):
    segments = line.split()
    newline = ['','','']
    newline[0] = ' '.join(segments[0:2])
    newline[1] = segments[2]
    newline[2] = ' '.join(segments[3:])
    return newline


@app.route('/viewlog')
def viewlog():
	# get ip address from request user
    ip = request.remote_addr
	# user agent
    UA_string  = request.user_agent.string 
    try:
    	response = reader.city(ip)
    	location = response.city.names['zh-CN'] +', '+ response.country.names['zh-CN']
    except:
    	location = 'unknow location'

    # get log file
    with open(logfile,'rb') as f:
    	data = f.readlines()
    
    results = [ split_logline(line) for line in data if line.find(ip) >=0 ]
    results.reverse()	# reverse the timeline order
    
    return render_template('logs.html', logs=results, ip=ip, 
    	loc=location, UA=UA_string)

@app.route('/viewlog/full')
def fulllog():
    # get ip address from request user
    ip = request.remote_addr
    # user agent
    UA_string  = request.user_agent.string 
    try:
        response = reader.city(ip)
        location = response.city.names['zh-CN'] +', '+ response.country.names['zh-CN']
    except:
        location = 'unknow location'

    # get log file
    with open(logfile,'rb') as f:
        data = f.readlines()
    results = [ split_logline(line) for line in data]
    results.reverse()   # reverse the timeline order 
    return render_template('logs_full.html', logs=results, ip=ip, 
        loc=location, UA=UA_string)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)