from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main/home.html', active_page='home')

@app.route('/tracker')
def tracker():
    return render_template('main/tracker.html', active_page='tracker')

@app.route('/goals')
def goals():
    return render_template('main/goals.html', active_page='goals')

@app.route('/analysis')
def analysis():
    return render_template('main/analysis.html', active_page='analysis')

@app.route('/reports')
def reports():
    return render_template('main/reports.html', active_page='reports')

@app.route('/feedbacks')
def feedbacks():
    return render_template('main/feedbacks.html', active_page='feedbacks')

@app.route('/history')
def history():
    return render_template('main/history.html', active_page='history')

@app.route('/profile')
def profile():
    return render_template('main/profile.html', active_page='profile')

@app.route('/settings')
def settings():
    return render_template('main/settings.html', active_page='settings')

@app.route('/support')
def support():
    return render_template('main/support.html', active_page='support')

if __name__ == '__main__':
    app.run(debug=True)