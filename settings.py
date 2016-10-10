#coding:utf-8
bind = 'unix:/var/run/gunicorn.sock'

workers = 4

# you should change this
user = 'root'

# maybe you like error
loglevel = 'debug'
errorlog = '-'
logfile = '/var/log/gunicorn/debug.log'
timeout = 300

secure_scheme_headers = {
    'X-SCHEME': 'https',
}
x_forwarded_for_header = 'X-FORWARDED-FOR'
