from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
from sso import Looker, L_User, URL
import random
import time
import yaml
engine = create_engine('sqlite:///sso.db', echo=True)

f = open('config.yml')
params = yaml.load(f)
f.close()

host = 'cs_eng'

my_host = params['hosts'][host]['host']
my_secret = params['hosts'][host]['secret']
embed_domain = params['hosts'][host]['embed_domain']

app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
          looker = Looker(my_host, my_secret)
          session2 = dict(session)

          user = L_User(id = session['user_id'],
                      first_name = session['first_name'],
                      last_name = session['last_name'],
                      permissions = session2['permissions'],
                      models = session2['models'],
                      access_filters = {},
                      group_ids = [7],
                      external_group_id = "demo-3",
                      user_attributes = {"state": session2['state']}
                      )
          fifteen_minutes = 15 * 60
          url = {'url':'https://' + URL(looker, user, fifteen_minutes, "/embed/dashboards/9?embed_domain=" + embed_domain, force_logout_login=True).to_string()}

          return render_template('home.html', url = url['url'])

          # return url



# @app.route('/second_page')
# def second_page():
#     if not session.get('logged_in'):
#         return render_template('login.html')
#     else:
#           looker = Looker(my_host, my_secret)
#
#
#           user = L_User(external_user_id = session['user_id'],
#                       permissions = str(session['permissions'].append('explore')),
#                       models = session['models'],
#                       access_filters = {},
#                       group_ids = [7]
#                       external_group_id = "demo-2",
#                       user_attributes = {"state": session['state']}
#                       )
#           fifteen_minutes = 15 * 60
#           url = {'url':'https://' + URL(looker, user, fifteen_minutes, "/embed/dashboards/the_look::bar_chart_2?embed_domain=" + embed_domain, force_logout_login=True)}
#           return render_template('home.html', url = url['url'])

@app.route('/login', methods=['POST'])
def do_admin_login():

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
        session['permissions'] = str(result.permissions).split(',')
        session['user_id'] = str(result.id)
        session['models'] = str(result.models).split(',')
        session['state'] = str(result.state)
        session['first_name'] = str(result.first_name)
        session['last_name'] = str(result.last_name)

    else:
        flash('wrong password!')
    return home()

@app.route("/logout", methods = ['POST'])
def logout():
    session['logged_in'] = False
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000, ssl_context='adhoc')
