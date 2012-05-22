#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import sys
import logging

### RESTful service routing
from optparse import OptionParser
from bottle import route, run, debug, request, static_file


_SENSOR_FULL_NAMES= {
           "t" : u"Temperature (ºC)",
           "p" : "Pressure (Pascal)",
           "a" : "Air Quality",
           "l" : "Luminosity (Lux)",
           "n" : "Noise (dB)",
           "h" : "Humidity",
        }


_SENSOR_PATH= {
        "temperature" : "t",
           "pressure" : "p",
        "air_quality" : "a",
         "luminosity" : "l",
              "noise" : "n",
           "humidity" : "h",
        }


_SENSOR_BOUNDARIES= {
           "t" : {"min" : 0, "max" : 50 },
           "p" : {"min" : 0, "max" : 100 },
           "a" : {"min" : 0, "max" : 200 },
           "l" : {"min" : 0, "max" : 1024},
           "n" : {"min" : 0, "max" : 1024},
           "h" : {"min" : 0, "max" : 1024},
        }

_SENSOR_FUNCTORS= {
           "t" : (lambda t: t/10),
           "p" : (lambda p: p/100),
           "a" : (lambda a: a),
           "l" : (lambda a: a),
           "n" : (lambda a: a),
           "h" : (lambda a: a),
        }

_SENSOR_TEMPLATE = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<title>Pollux'nz City Sensor charts -- %(uuid)s</title>
		<link rel="stylesheet" type="text/css" href="/css/basic.css" />
		
		<!-- 1. Add these JavaScript inclusions in the head of your page -->
		<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
		<script src="http://cdn.jquerytools.org/1.2.5/tiny/jquery.tools.min.js"></script>
		<script type="text/javascript" src="/js/highcharts.js"></script>
		
		<!-- 1a) Optional: add a theme file 
		<script type="text/javascript" src="/js/themes/gray.js"></script>-->
		
		
		<!-- 2. Add the JavaScript to initialize the chart on document ready -->
		<script type="text/javascript">
		var refreshRate = 30000 ;
		var infoBulle = true ;
		
		$(function() {
			// setup ul.tabs to work as tabs for each div directly under div.panes
			$("ul.tabs").tabs("div.panes > div");
		});
		
			Highcharts.setOptions({
				global: {
					useUTC: false
				}
			});
			
			var chart;
			$(document).ready(function() {
				chart0 = new Highcharts.Chart({
					chart: {
						renderTo: 'container0',
						defaultSeriesType: 'spline',
						marginRight: 10,
						events: {
							load: function() {
								// set up the updating of the chart each second
								var series = this.series[0];
								setInterval(function() {
									var x = (new Date()).getTime(); // current time
									var y = 0;
									jQuery.ajax({
										url:"/pull/pollux/%(uuid)s/luminosity.json",
										async:false,
										dataType:"json",
										success:function(data){
											y = data[0];
										}
									});
									series.addPoint([x, y], true, true);
								}, refreshRate);
							}
						}
					},
					title: {
						text: 'Lumière'
					},
					xAxis: {
						type: 'datetime',
						tickPixelInterval: 150
					},
					yAxis: {
						title: {
							text: 'Value'
						},
						plotLines: [{
							value: 0,
							width: 1,
							color: '#808080'
						}]
					},
					tooltip: {
						enabled: infoBulle,
						formatter: function() {
				                return '<b>'+ this.series.name +'</b><br/>'+
								Highcharts.dateFormat('%%Y-%%m-%%d %%H:%%M:%%S', this.x) +'<br/>'+ 
								Highcharts.numberFormat(this.y, 2);
						}
					},
					legend: {
						enabled: false
					},
					exporting: {
						enabled: false
					},
					series: [{
						name: 'Lumière',
						data: (function() {
							// generate an array of random data
							var data = [],
								time = (new Date()).getTime(),
								i, y = 0;
								
								jQuery.ajax({
										url:"/pull/pollux/%(uuid)s/luminosity.json",
										async:false,
										dataType:"json",
										success:function(data){
											y = data;
										}
									});
							for (i = -19; i <= 0; i++) {
								data.push({
									x: time + i * 1000,
									y: y[i*-1]
								});
							}
							return data;
						})()
					}]
				});
	
	chart1 = new Highcharts.Chart({
					chart: {
						renderTo: 'container1',
						defaultSeriesType: 'spline',
						marginRight: 10,
						events: {
							load: function() {
				
								// set up the updating of the chart each second
								var series = this.series[0];
								setInterval(function() {
									var x = (new Date()).getTime(); // current time
									var y = 0;
									jQuery.ajax({
										url:"/pull/pollux/%(uuid)s/temperature.json",
										async:false,
										dataType:"json",
										success:function(data){
											y = data[0];
										}
									});
									series.addPoint([x, y], true, true);
								}, refreshRate);
							}
						}
					},
					title: {
						text: 'Température'
					},
					xAxis: {
						type: 'datetime',
						tickPixelInterval: 150
					},
					yAxis: {
						title: {
							text: 'Value'
						},
						plotLines: [{
							value: 0,
							width: 1,
							color: '#808080'
						}]
					},
					tooltip: {
						enabled: infoBulle,
						formatter: function() {
				                return '<b>'+ this.series.name +'</b><br/>'+
								Highcharts.dateFormat('%%Y-%%m-%%d %%H:%%M:%%S', this.x) +'<br/>'+ 
								Highcharts.numberFormat(this.y, 2);
						}
					},
					legend: {
						enabled: false
					},
					exporting: {
						enabled: false
					},
					series: [{
						name: 'Température',
						data: (function() {
							// generate an array of random data
							var data = [],
								time = (new Date()).getTime(),
								i, y = 0;
								
								jQuery.ajax({
										url:"/pull/pollux/%(uuid)s/temperature.json",
										async:false,
										dataType:"json",
										success:function(data){
											y = data;
										}
									});
							for (i = -19; i <= 0; i++) {
								data.push({
									x: time + i * 1000,
									y: y[i*-1]
								});
							}
							return data;
						})()
					}]
				});

chart2 = new Highcharts.Chart({
					chart: {
						renderTo: 'container2',
						defaultSeriesType: 'spline',
						marginRight: 10,
						events: {
							load: function() {
				
								// set up the updating of the chart each second
								var series = this.series[0];
								setInterval(function() {
									var x = (new Date()).getTime(); // current time
									var y = 0;
									jQuery.ajax({
										url:"/pull/pollux/%(uuid)s/humidity.json",
										async:false,
										dataType:"json",
										success:function(data){
											y = data[0];
										}
									});
									series.addPoint([x, y], true, true);
								}, refreshRate);
							}
						}
					},
					title: {
						text: 'Humidité'
					},
					xAxis: {
						type: 'datetime',
						tickPixelInterval: 150
					},
					yAxis: {
						title: {
							text: 'Value'
						},
						plotLines: [{
							value: 0,
							width: 1,
							color: '#808080'
						}]
					},
					tooltip: {
						enabled: infoBulle,
						formatter: function() {
				                return '<b>'+ this.series.name +'</b><br/>'+
								Highcharts.dateFormat('%%Y-%%m-%%d %%H:%%M:%%S', this.x) +'<br/>'+ 
								Highcharts.numberFormat(this.y, 2);
						}
					},
					legend: {
						enabled: false
					},
					exporting: {
						enabled: false
					},
					series: [{
						name: 'Humidité',
						data: (function() {
							// generate an array of random data
							var data = [],
								time = (new Date()).getTime(),
								i, y = 0;
								
								jQuery.ajax({
										url:"/pull/pollux/%(uuid)s/humidity.json",
										async:false,
										dataType:"json",
										success:function(data){
											y = data;
										}
									});
							for (i = -19; i <= 0; i++) {
								data.push({
									x: time + i * 1000,
									y: y[i*-1]
								});
							}
							return data;
						})()
					}]
				});
			
			chart0 = new Highcharts.Chart({
					chart: {
						renderTo: 'container3',
						defaultSeriesType: 'spline',
						marginRight: 10,
						events: {
							load: function() {
								// set up the updating of the chart each second
								var series = this.series[0];
								setInterval(function() {
									var x = (new Date()).getTime(); // current time
									var y = 0;
									jQuery.ajax({
										url:"/pull/pollux/%(uuid)s/noise.json",
										async:false,
										dataType:"json",
										success:function(data){
											y = data[0];
										}
									});
									series.addPoint([x, y], true, true);
								}, refreshRate);
							}
						}
					},
					title: {
						text: 'Bruit'
					},
					xAxis: {
						type: 'datetime',
						tickPixelInterval: 150
					},
					yAxis: {
						title: {
							text: 'Value'
						},
						plotLines: [{
							value: 0,
							width: 1,
							color: '#808080'
						}]
					},
					tooltip: {
						enabled: infoBulle,
						formatter: function() {
				                return '<b>'+ this.series.name +'</b><br/>'+
								Highcharts.dateFormat('%%Y-%%m-%%d %%H:%%M:%%S', this.x) +'<br/>'+ 
								Highcharts.numberFormat(this.y, 2);
						}
					},
					legend: {
						enabled: false
					},
					exporting: {
						enabled: false
					},
					series: [{
						name: 'Bruit',
						data: (function() {
							// generate an array of random data
							var data = [],
								time = (new Date()).getTime(),
								i, y = 0;
								
								jQuery.ajax({
										url:"/pull/pollux/%(uuid)s/noise.json",
										async:false,
										dataType:"json",
										success:function(data){
											y = data;
										}
									});
							for (i = -19; i <= 0; i++) {
								data.push({
									x: time + i * 1000,
									y: y[i*-1]
								});
							}
							return data;
						})()
					}]
				});
chart0 = new Highcharts.Chart({
					chart: {
						renderTo: 'container4',
						defaultSeriesType: 'spline',
						marginRight: 10,
						events: {
							load: function() {
								// set up the updating of the chart each second
								var series = this.series[0];
								setInterval(function() {
									var x = (new Date()).getTime(); // current time
									var y = 0;
									jQuery.ajax({
										url:"/pull/pollux/%(uuid)s/air_quality.json",
										async:false,
										dataType:"json",
										success:function(data){
											y = data[0];
										}
									});
									series.addPoint([x, y], true, true);
								}, refreshRate);
							}
						}
					},
					title: {
						text: 'Qualité de l\\'air'
					},
					xAxis: {
						type: 'datetime',
						tickPixelInterval: 150
					},
					yAxis: {
						title: {
							text: 'Value'
						},
						plotLines: [{
							value: 0,
							width: 1,
							color: '#808080'
						}]
					},
					tooltip: {
						enabled: infoBulle,
						formatter: function() {
				                return '<b>'+ this.series.name +'</b><br/>'+
								Highcharts.dateFormat('%%Y-%%m-%%d %%H:%%M:%%S', this.x) +'<br/>'+ 
								Highcharts.numberFormat(this.y, 2);
						}
					},
					legend: {
						enabled: false
					},
					exporting: {
						enabled: false
					},
					series: [{
						name: 'Qualité de l\\'air',
						data: (function() {
							// generate an array of random data
							var data = [],
								time = (new Date()).getTime(),
								i, y = 0;
								
								jQuery.ajax({
										url:"/pull/pollux/%(uuid)s/air_quality.json",
										async:false,
										dataType:"json",
										success:function(data){
											y = data;
										}
									});
							for (i = -19; i <= 0; i++) {
								data.push({
									x: time + i * 1000,
									y: y[i*-1]
								});
							}
							return data;
						})()
					}]
				});
chart0 = new Highcharts.Chart({
					chart: {
						renderTo: 'container5',
						defaultSeriesType: 'spline',
						marginRight: 10,
						events: {
							load: function() {
								// set up the updating of the chart each second
								var series = this.series[0];
								setInterval(function() {
									var x = (new Date()).getTime(); // current time
									var y = 0;
									jQuery.ajax({
										url:"/pull/pollux/%(uuid)s/pressure.json",
										async:false,
										dataType:"json",
										success:function(data){
											y = data[0];
										}
									});
									series.addPoint([x, y], true, true);
								}, refreshRate);
							}
						}
					},
					title: {
						text: 'Pression de l\\'air'
					},
					xAxis: {
						type: 'datetime',
						tickPixelInterval: 150
					},
					yAxis: {
						title: {
							text: 'Value'
						},
						plotLines: [{
							value: 0,
							width: 1,
							color: '#808080'
						}]
					},
					tooltip: {
						enabled: infoBulle,
						formatter: function() {
				                return '<b>'+ this.series.name +'</b><br/>'+
								Highcharts.dateFormat('%%Y-%%m-%%d %%H:%%M:%%S', this.x) +'<br/>'+ 
								Highcharts.numberFormat(this.y, 2);
						}
					},
					legend: {
						enabled: false
					},
					exporting: {
						enabled: false
					},
					series: [{
						name: 'Pression de l\\'air',
						data: (function() {
							// generate an array of random data
							var data = [],
								time = (new Date()).getTime(),
								i, y = 0;
								
								jQuery.ajax({
										url:"/pull/pollux/%(uuid)s/pressure.json",
										async:false,
										dataType:"json",
										success:function(data){
											y = data;
										}
									});
							for (i = -19; i <= 0; i++) {
								data.push({
									x: time + i * 1000,
									y: y[i*-1]
								});
							}
							return data;
						})()
					}]
				});
			});
				
		</script>
		
	</head>
	<body>
	
<a href="/"><img src="/img/polluxnzcity.png" alt="Logo Pollux NZ City" /></a>
	
	<!-- the tabs -->
<ul class="tabs">
	<li><a href="#1">Lumière</a></li>
	<li><a href="#2">Température</a></li>
	<li><a href="#3">Humidité</a></li>
	<li><a href="#4">Bruit</a></li>
	<li><a href="#5">Qualité de l\'air</a></li>
	<li><a href="#6">Pression de l\'air</a></li>
</ul>

<br />
<br />

<!-- tab "panes" -->
<div class="panes">
	<div><div id="container0" style="width: 800px; height: 400px; margin: 0 auto"></div></div>
	<div><div id="container1" style="width: 800px; height: 400px; margin: 0 auto"></div></div>
	<div><div id="container2" style="width: 800px; height: 400px; margin: 0 auto"></div></div>
	<div><div id="container3" style="width: 800px; height: 400px; margin: 0 auto"></div></div>
	<div><div id="container4" style="width: 800px; height: 400px; margin: 0 auto"></div></div>
	<div><div id="container5" style="width: 800px; height: 400px; margin: 0 auto"></div></div>
</div>

<div id="footer">
<hr />
Pollux'NZ City Project by <a href="http://hackable-devices.org">CKAB</a>
</div>

	</body>
</html>
"""

_INDEX_TEMPLATE="""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
	<link rel="stylesheet" type="text/css" href="/css/basic.css" />
    <head>
        <title>PolluxNZCity</title>
    </head>
    <body>
        <div id="head">
            <a href="/"><img src="/img/polluxnzcity.png" alt="Logo Pollux NZ City" /></a>
        </div>

        <div id="main">
            <ul>
%s
            </ul>
        </div>
        <div id="foot">Pollux'NZCity project</div>
    </body>
</html>
"""


@route('/push/pollux/:serial:/values')
def push_data(serial="none"):
    """
    this is the URL that calls the arduino: 
    /push/pollux/5d47051f-d265-4e85-9316-b662ed3041f/values?a=0074&l=3890&n=0020&h=0349&p=10167&t=291
    where  t = temperature (21 degC = 210)
           p = pressure (*100 in pascal)
           a = air quality
           l = luminosity (lux)
           n = noise sensor
           h = humidity
    """
    log.debug('serial id is : %s' % serial)
    log.debug('got: a=%(a)s, l=%(l)s, n=%(n)s, h=%(h)s, t=%(t)s, p=%(p)s' % request.GET)
    
    if len(data) != 0:
        for k in data[serial]:
            if k in request.GET:
                try:
                    data[serial][k].append(_SENSOR_FUNCTORS[k](int(request.GET[k])))
                    if len(data[serial][k]) > 25:
                        data[serial][k] = data[serial][k][-25:]
                except KeyError:
                    data[serial][k].append(int(request.GET[k]))
    else:
        try:
            data[serial] = dict([(k,[_SENSOR_FUNCTORS[k](int(v))]) if k in _SENSOR_FUNCTORS.keys() else (k,[int(v)]) for k,v in request.GET.iteritems() ])
        except KeyError:
            data[serial] = dict([(k,[int(v)]) for k,v in request.GET.iteritems()])

    log.debug('data global is : %s ' % data)

    return 'OK'

@route('/pull/pollux/:serial:')
def visualize(serial):
    if serial in data.keys():
        return _SENSOR_TEMPLATE % {"uuid":serial}
    else:
        return """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
        <title>PolluxNZCity</title>
    </head>
    <body>
        <div id="head">
            <a href="/"><img src="/img/polluxnzcity.png" alt="Logo Pollux NZ City" /></a>
        </div>
        <div id="main">
        ERROR: This sensor did not send data to the platform.
        </div>
        <div id="foot">Pollux'NZCity project</div>
    </body>
</html>
"""

@route('/pull/pollux/:serial:/:sensor:.json')
def pull_sensor(serial, sensor):
    values = [str(i) for i in data[serial][_SENSOR_PATH[sensor]]]
    values.reverse()
    log.debug("content: %s" % values)
    if len(values) < 20:
        print '['+','.join(values+(20-len(values))*['0'])+']'
        return '['+','.join(values+(20-len(values))*['0'])+']'


    return '['+','.join(values)+']'

@route('')
@route('/')
@route('/index.html')
def index():
    pc_list = ""
    for serial in data.keys():
        pc_list += "            <li> PolluxNZCity sensor whose uuid is <a href='/pull/pollux/%s'>%s</a> </li>\n" % (serial, serial)
    if pc_list == "":
        pc_list = "<h1>No sensor has sent data to the platform.</h1>\nPlease wait for new data to come..."
    return _INDEX_TEMPLATE % pc_list

@route('/img/:img:')
def get_img(img):
    return static_file(img, root="img/")

@route('/css/:css:')
def get_css(css):
    return static_file(css, root="css/")

@route('/js/:js:')
def get_js(js):
    return static_file(js, root="js/")

@route('/favicon.ico')
def favicon():
    return ""

def init_service(host_addr, host_port, dbg=True):
    debug(dbg)
    run(host=host_addr, port=host_port)

if __name__ == '__main__':
    global log
    global data

    data = {}

    parser = OptionParser()
    parser.add_option("-H", "--host", dest="hostname",
                    help="IP address to start the service on", metavar="HOST", default="0.0.0.0")
    parser.add_option("-p", "--port", dest="port",
                    help="Port to start the service on", metavar="PORT", default="8000")
    parser.add_option("-v", "--verbose",
                    action="store_true", dest="verbose", default=False,
                    help="print more information messages to stdout")

    (options, args) = parser.parse_args()

    if options.verbose == True : level=logging.DEBUG
    else:                        level=logging.ERROR

    logging.basicConfig(stream=sys.stdout, level=level)
    log = logging.getLogger('polluxinthecloud')
    
    log.debug("starting service...")
    init_service(options.hostname, options.port, dbg=options.verbose)
