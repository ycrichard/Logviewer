# all the imports
import geoip2.database, re
from flask import Flask, render_template, url_for, request, redirect

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
app.config['SECRET_KEY'] = 'hugolege'

def split_logline(line):
    segments = line.split()
    # tuple of 3 elements
    newline = (' '.join(segments[0:2]),segments[2],' '.join(segments[3:]))
    return newline

@app.route('/viewlog/')
def viewlog_index():
    return redirect(url_for('viewlog',id='me'))

@app.route('/viewlog/<string:id>', methods=['GET', 'POST'])
def viewlog(id):
    # get ip address from request user
    ip = request.remote_addr
    # user agent
    UA_string  = request.user_agent.string 
    try:
        response = reader.city(ip)
        location = response.city.names['zh-CN'] +', '+ response.country.names['zh-CN']
    except:
        location = 'unknown location'

    # get log file
    with open(logfile,'r') as f:
        data = f.readlines()

    keyword=''

    if id == 'full':
        data = [ line for line in data]
        keyword='.*'
    elif id == 'me':
        data = [ line for line in data
         if line.find(ip) >=0 ]
        keyword=ip
    elif id == 'error':
        data = [ line for line in data
         if re.search(r'\s+ERROR\s+|\s+WARNING\s+',line)]
        keyword='ERROR|WARNING'

    if request.method == 'POST':
        data = [ line for line in data 
            if re.search(request.form['text'],line, re.IGNORECASE) ]
        keyword=keyword + "' --> '" + request.form['text']
        

    data.reverse()	# reverse the timeline order 
    results = [ split_logline(line) for line in data]

    return render_template('layout_log.html', logs=results, ip=ip, 
    	loc=location, UA=UA_string, key=keyword)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)