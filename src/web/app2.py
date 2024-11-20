from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('main/dashboard.html')

@app.route('/users')
def users():
    return render_template('main/users.html')

@app.route('/history')
def history():
    return render_template('main/history.html')

@app.route('/analytics')
def analytics():
    return render_template('main/analytics.html')

@app.route('/tickets')
def tickets():
    return render_template('main/tickets.html')

@app.route('/sale_list')
def sale_list():
    return render_template('main/sale_list.html')

@app.route('/reports')
def reports():
    return render_template('main/reports.html')

@app.route('/settings')
def settings():
    return render_template('main/settings.html')

@app.route('/new_login')
def new_login():
    return render_template('main/new_login.html')

if __name__ == '__main__':
    app.run(debug=True)