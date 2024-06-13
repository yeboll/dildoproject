from state import State
from flask import Flask, render_template, request, redirect, url_for
from cron import manage_cron_jobs
import json

app = Flask(__name__)
state = State()

@app.route('/')
def home():
    ticker_states = state.states
    available_tfs = State.available_tfs
    return render_template('index.html', ticker_states=ticker_states, available_tfs=available_tfs)

@app.route('/update', methods=['POST'])
def update():
    for ticker in state.states:
        selected_tfs = request.form.getlist(ticker)
        state.states[ticker]['recv_tf'] = selected_tfs

    manage_cron_jobs(state.states, state.available_tfs)
    
    return redirect(url_for('home'))

@app.route('/edit', methods=['GET'])
def edit():
    tik = request.args.get('ticker')
    return render_template('edit_ticker.html', state=state.states[tik], 
                           strategies=state.available_strategies, name=tik)

if __name__ == '__main__':
    app.run(debug=True)

