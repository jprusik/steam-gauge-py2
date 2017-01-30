import json
from flask import Flask, url_for, redirect, request, Markup, render_template, make_response, session, flash, g
from flask.ext.openid import OpenID
import model_v2, config

app = Flask(__name__)

# explicitly disable debug in production
app.debug = False

model_v2.setup_all()

app.secret_key = config.APP_SECRET
oid = OpenID(app, './openid_store')

# import steamapp
import steamfriends
import account_api

def clear_session():
    session['account_id'] = None
    session['admin_p'] = False
    session['last_action'] = None
    session['session_start'] = None
    session['full_response'] = None
    # using session.clear() nulls everything, including the session object itself, so you have to check for session AND session['account_id'] or pop(None) individual session keys
    # session.clear()


app.last_db_update = ''

@app.context_processor
def lastDatabaseUpdate():
    if app.last_db_update == '':
        app.last_db_update = model_v2.App.query.order_by(model_v2.App.last_updated.desc()).first().last_updated.strftime('%B %d, %Y')
    return dict(db_date=app.last_db_update)


@app.before_request
def before_request():
    if session and session['account_id']:
        # If more than x minutes have passed since the last time the user did anything, log them out
        minutes_expire = 720
        if (model_v2.datetime.datetime.now()-session['last_action']).seconds > (minutes_expire*60):
            clear_session()
        else:
            # check anything that might have changed
            if session['account_id'] in config.ADMIN_USERS:
                session['admin_p']=True
            else:
                session['admin_p']=False
            session['last_action'] = model_v2.datetime.datetime.now()
    else:
        clear_session()


@app.route('/')
def index():
    return render_template('index.html')


# # What version of python is active?
# import sys
# @app.route('/pyversion')
# def pyversion():
#     return sys.version


@app.route('/receipt')
def receipt():
    return render_template('receipt.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/friends', methods=['GET'])
def friends():
    # error = None
    searchword = request.args.get('username', '')
    if searchword == '':
        # TODO: fix this redirection logic. Attempts to pass null value for username should go to the error page. Move this search to main homepage.
        return render_template('friendindex.html')
    else:
        api_accounts = account_api.account_lookup(searchword, request_type='friends')
        if api_accounts['QueryStatus']['error'] == True:
            return render_template('error.html', error_code='app', error_message=api_accounts['QueryStatus']['error_message'])
        return render_template('friends.html', api_return=api_accounts)


@app.route('/account', methods=['GET'])
def account():
    searchword = request.args.get('username', '')
    if searchword == '':
        # api_accounts={'QueryStatus':{'error':True,'error_message':'No username was provided'},'Account':{'user_64id':'','user_persona':'','user_realname':'','user_country':'','user_state':'','user_cityid':'','user_primary_group':'','user_avatar_small':'','user_avatar_medium':'','user_avatar_large':'','user_account_link':'','account_public':'','account_creation_datetime':'','current_status':'','current_app_id':'','current_app_title':'','last_logoff_datetime':'','UserApps':{'app_count':'','Apps':[]},'HiddenApps':{'app_count':'','Apps':[]}}}
        # return render_template('account.html', api_return=api_accounts)
        return render_template('error.html', error_code='app', error_message='No username was provided')
    else:
        api_accounts = account_api.account_lookup(searchword)
        if api_accounts['QueryStatus']['error'] == True:
            return render_template('error.html', error_code='app', error_message=api_accounts['QueryStatus']['error_message'])
        return render_template('account.html', api_return=api_accounts)


# @app.route('/admin')
# def admin_index():
#     if session['admin_p'] == True:
#         api_accounts = account_api.all_games_account()
#         return render_template('account.html', api_return=api_accounts)
#     else:
#         return render_template('error.html')


# This is the old account summary path - redirect to new
@app.route('/search', methods=['GET'])
def search():
    searchword = request.args.get('username', '')
    return redirect("/account?username="+searchword, code=302)


# @app.route('/api', methods=['GET'])
# def api():
#     searchword = request.args.get('username', '')
#     if searchword == '':
#         return render_template('account_api.html', api_return=api_accounts)
#     else:
#         api_accounts = account_api.account_lookup(searchword, True)
#         return api_accounts
#         # return render_template('account_api.html', api_return=api_accounts)


@app.route('/login')
@oid.loginhandler
def login():
    return oid.try_login('http://steamcommunity.com/openid')


@oid.after_login
def login_reponse(resp):
    session['account_id'] = unicode(resp.identity_url.split('/')[len(resp.identity_url.split('/'))-1])
    # session['full_response'] = json.dumps(resp)
    session['session_start'] = model_v2.datetime.datetime.now()
    session['last_action'] = model_v2.datetime.datetime.now()
    if session['account_id'] in config.ADMIN_USERS:
        session['admin_p'] = True
    # return redirect(url_for('index'))
    return redirect(oid.get_next_url())


@app.route('/logout')
def logout():
    clear_session()
    return redirect(oid.get_next_url())


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error_code='404', error_message='Page not found'), 404


@app.errorhandler(500)
def internal_server_error(error):
    if session['account_id'] in config.ADMIN_USERS:
        return render_template('error.html', error_code='500', error_info='The server had a problem: '+error.args), 500
    else:
        return render_template('error.html', error_code='500', error_info='The server had a problem'), 500


@app.errorhandler(504)
def gateway_timeout(error):
    if session['account_id'] in config.ADMIN_USERS:
        return render_template('error.html', error_code='504', error_info='The request took too long: '+error.args), 504
    else:
        return render_template('error.html', error_code='504', error_info='The request took too long'), 504


if __name__ == '__main__':
    app.run()
