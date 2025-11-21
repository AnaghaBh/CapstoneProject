from flask import Flask, render_template, request, session, redirect, url_for
from controller import MisinformationController
import uuid
import random
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'misinformation-research-2024'

controller = MisinformationController()

# Sample misinformation claims
SAMPLE_CLAIMS = [
    "Drinking hot water cures all viruses instantly",
    "5G towers cause cancer and control people's minds", 
    "Vaccines contain microchips for government surveillance",
    "Climate change is completely fake and made up",
    "Organic food has zero nutritional value compared to regular food",
    "Professional athletes never get injured because they're superhuman"
]

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/demographics', methods=['GET', 'POST'])
def demographics():
    if request.method == 'POST':
        # Store participant info
        session['participant_id'] = str(uuid.uuid4())[:8]
        session['age'] = request.form['age']
        session['occupation'] = request.form['occupation']
        session['education'] = request.form['education']
        
        # Select frameworks and claim randomly
        session['misinfo_framework'] = random.choice(list(controller.frameworks.keys()))
        session['correction_framework'] = random.choice(list(controller.frameworks.keys()))
        session['claim'] = random.choice(SAMPLE_CLAIMS)
        
        return redirect(url_for('show_misinformation'))
    
    return render_template('demographics.html')

@app.route('/misinformation', methods=['GET', 'POST'])
def show_misinformation():
    if request.method == 'POST':
        belief = int(request.form['belief_rating'])
        session['belief_before'] = belief
        
        # If belief is lowest (1), try another misinformation
        if belief == 1:
            # Generate new misinformation
            session['misinfo_framework'] = random.choice(list(controller.frameworks.keys()))
            session['claim'] = random.choice(SAMPLE_CLAIMS)
            return redirect(url_for('show_misinformation'))
        else:
            # Auto-start conversation
            return redirect(url_for('chat_correction'))
    
    # Generate misinformation using selected framework
    try:
        misinfo_module = controller.frameworks[session['misinfo_framework']]
        params = controller._get_default_params(session['misinfo_framework'])
        misinfo_text, misinfo_metadata = misinfo_module.simulate_misinformation(params)
        
        session['misinfo_text'] = misinfo_text
        session['misinfo_metadata'] = misinfo_metadata
        
    except Exception as e:
        # Fallback to original claim if generation fails
        session['misinfo_text'] = session['claim']
        session['misinfo_metadata'] = {}
    
    return render_template('misinformation.html', 
                         misinformation=session['misinfo_text'])

@app.route('/chat', methods=['GET', 'POST'])
def chat_correction():
    # Auto-start with correction if no conversation exists
    if 'conversation' not in session:
        session['conversation'] = []
        try:
            correction_module = controller.frameworks[session['correction_framework']]
            correction_text, _ = correction_module.generate_correction(
                session['misinfo_text'], 
                session.get('misinfo_metadata', {}), 
                tone="conversational", 
                cohort=session['occupation']
            )
        except Exception as e:
            correction_text = "I understand your concern. Let me provide some factual information to help clarify this topic."
        
        session['conversation'].append({
            'user': '',
            'bot': correction_text
        })
        session.modified = True
    
    if request.method == 'POST':
        if 'final_rating' in request.form:
            # Final belief rating
            session['belief_after'] = int(request.form['final_rating'])
            return redirect(url_for('complete_experiment'))
        
        # Handle chat message
        user_message = request.form['message']
        
        try:
            # Generate correction response
            correction_module = controller.frameworks[session['correction_framework']]
            correction_text, _ = correction_module.generate_correction(
                session['misinfo_text'], 
                session.get('misinfo_metadata', {}), 
                tone="conversational", 
                cohort=session['occupation']
            )
        except Exception as e:
            correction_text = "I understand your concern. Let me provide some factual information to help clarify this topic."
        
        # Store conversation
        if 'conversation' not in session:
            session['conversation'] = []
        
        session['conversation'].append({
            'user': user_message,
            'bot': correction_text
        })
        
        session.modified = True
        
        return render_template('chat.html', 
                             conversation=session['conversation'],
                             misinformation=session['misinfo_text'])
    
    return render_template('chat.html', 
                         misinformation=session['misinfo_text'],
                         conversation=session.get('conversation', []))

@app.route('/complete')
def complete_experiment():
    # Save experiment data
    experiment_data = {
        'timestamp': datetime.now().isoformat(),
        'participant_id': session['participant_id'],
        'age': session['age'],
        'occupation': session['occupation'],
        'education': session['education'],
        'original_claim': session['claim'],
        'misinfo_framework': session['misinfo_framework'],
        'correction_framework': session['correction_framework'],
        'misinfo_text': session['misinfo_text'],
        'belief_before': session['belief_before'],
        'belief_after': session['belief_after'],
        'effectiveness': session['belief_before'] - session['belief_after'],
        'conversation_length': len(session.get('conversation', []))
    }
    
    # Log to CSV
    df = pd.DataFrame([experiment_data])
    log_path = 'data/outputs/web_experiment_results.csv'
    
    if os.path.exists(log_path):
        df.to_csv(log_path, mode='a', header=False, index=False)
    else:
        df.to_csv(log_path, index=False)
    
    effectiveness = experiment_data['effectiveness']
    
    # Clear session and show completion message
    session.clear()
    return '<h2>Thank you for participating!</h2><p><a href="/">Start New Session</a></p>'

@app.route('/reset')
def reset_session():
    session.clear()
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)