# all the imports
import geoip2.database, re
from flask import Flask, render_template, url_for, request, redirect, session

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

def user_info():
    # get ip address from request user
    session['ip']=request.remote_addr
    session['UA']=request.user_agent.string
    try:
        response = reader.city(session['ip'])
        location = response.city.names['zh-CN'] +', '+ response.country.names['zh-CN']
    except:
        location = 'unknown location'
    session['location']=location

@app.route('/viewlog/')
def viewlog_index():
    if 'ip' not in session:
        user_info()
    return redirect(url_for('viewlog_page',id='me',page=1))

@app.route('/viewlog/<string:id>/')
def viewlog(id):

    if 'ip' not in session:
        user_info()
    if 'keyword' not in session:
        session['keyword']=''
    return redirect(url_for('viewlog_page',id=id,page=1))


@app.route('/viewlog/<string:id>/<int:page>', methods=['GET', 'POST'])
def viewlog_page(id, page):

    if request.method == 'POST':
        session['keyword']=request.form['text']
        return redirect(url_for('viewlog_page',id='search',page=1))

    if 'ip' not in session:
        user_info()

    # read log file
    with open(logfile,'r') as f:
        data = f.readlines()
    if id == 'full':
        session['keyword']='.*'
    elif id == 'me':
        data = [ line for line in data
         if line.find(session['ip']) >=0 ]
        session['keyword']=session['ip']
    elif id == 'error':
        data = [ line for line in data
         if re.search(r'\s+ERROR\s+|\s+WARNING\s+',line)]
        session['keyword']='ERROR|WARNING'
    elif id == 'search':
        data = [ line for line in data
         if re.search(session['keyword'],line, re.IGNORECASE) ]
    else:
        return 'Page do not existe'

    if (page > len(data) //100 +1)|(page <=0) :
       return 'Page index out of range'

    data.reverse()	# reverse the timeline order
    results = [ split_logline(line) for line in data] # table structure

    return render_template('layout_log.html', logs=results, numpage=page, key=session['keyword'],
        ip=session['ip'], loc=session['location'], UA=session['UA'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001， debug=True)
