from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('main/dashboard.html', active_page='dashboard')

@app.route('/users')
def users():
    return render_template('main/users.html', active_page='users')

@app.route('/history')
def history():
    return render_template('main/history.html', active_page='history')

@app.route('/analytics')
def analytics():
    return render_template('main/analytics.html', active_page='analytics')

@app.route('/tickets')
def tickets():
    return render_template('main/tickets.html', active_page='tickets')

@app.route('/sale_list')
def sale_list():
    return render_template('main/sale_list.html', active_page='sale_list')

@app.route('/reports')
def reports():
    return render_template('main/reports.html', active_page='reports')

@app.route('/settings')
def settings():
    return render_template('main/settings.html', active_page='settings')

@app.route('/new_login')
def new_login():
    return render_template('main/new_login.html', active_page='new_login')

if __name__ == '__main__':
    app.run(debug=True)