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

@app.route('/')
def welcome():
    return render_template('welcome_chat.html')

@app.route('/demographics', methods=['GET', 'POST'])
def demographics():
    if request.method == 'POST':
        session['participant_id'] = str(uuid.uuid4())[:8]
        session['age'] = request.form['age']
        session['occupation'] = request.form['occupation']
        session['education'] = request.form['education']
        return redirect(url_for('chat'))
    
    return render_template('demographics.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    # Always start fresh for new participants
    if 'messages' not in session or request.method == 'GET':
        session['messages'] = []
        session['stage'] = 'presenting_misinfo'
        session['misinfo_attempts'] = 0
        
        # Start with misinformation
        misinfo_text = generate_misinformation()
        session['messages'].append({
            'role': 'bot',
            'content': misinfo_text,
            'type': 'misinformation'
        })
        session['current_misinfo'] = misinfo_text
        session.modified = True
    
    if request.method == 'POST':
        user_input = request.form['message'].strip()
        
        if session['stage'] == 'presenting_misinfo':
            # Expecting belief rating (1-5)
            try:
                belief = int(user_input)
                if 1 <= belief <= 5:
                    session['messages'].append({
                        'role': 'user', 
                        'content': f"My belief level: {belief}",
                        'type': 'belief_rating'
                    })
                    
                    if belief == 1:
                        # Try new misinformation
                        session['misinfo_attempts'] += 1
                        if session['misinfo_attempts'] < 3:  # Max 3 attempts
                            misinfo_text = generate_misinformation()
                            session['messages'].append({
                                'role': 'bot',
                                'content': f"Let me share something else with you: {misinfo_text}",
                                'type': 'misinformation'
                            })
                            session['current_misinfo'] = misinfo_text
                        else:
                            # End experiment if no belief after 3 attempts
                            return redirect(url_for('complete'))
                    else:
                        # Start correction conversation
                        session['belief_before'] = belief
                        session['stage'] = 'correcting'
                        correction_text = generate_correction(session['current_misinfo'])
                        session['messages'].append({
                            'role': 'bot',
                            'content': correction_text,
                            'type': 'correction'
                        })
                    
                    session.modified = True
                else:
                    session['messages'].append({
                        'role': 'bot',
                        'content': "Please rate your belief from 1 (completely false) to 5 (completely true).",
                        'type': 'prompt'
                    })
            except ValueError:
                session['messages'].append({
                    'role': 'bot',
                    'content': "Please respond with a number from 1 to 5 indicating your belief level.",
                    'type': 'prompt'
                })
        
        elif session['stage'] == 'correcting':
            # Normal conversation during correction
            session['messages'].append({
                'role': 'user',
                'content': user_input,
                'type': 'conversation'
            })
            
            # Generate response
            response = generate_correction_response(user_input, session['current_misinfo'])
            session['messages'].append({
                'role': 'bot',
                'content': response,
                'type': 'correction'
            })
            
            # Check if ready for final rating
            if len([m for m in session['messages'] if m['type'] == 'conversation']) >= 4:
                session['stage'] = 'final_rating'
                session['messages'].append({
                    'role': 'bot',
                    'content': "After our discussion, please rate your belief in the original statement again (1-5):",
                    'type': 'final_prompt'
                })
        
        elif session['stage'] == 'final_rating':
            try:
                belief_after = int(user_input)
                if 1 <= belief_after <= 5:
                    session['belief_after'] = belief_after
                    session['messages'].append({
                        'role': 'user',
                        'content': f"Final belief level: {belief_after}",
                        'type': 'final_rating'
                    })
                    return redirect(url_for('complete'))
                else:
                    session['messages'].append({
                        'role': 'bot',
                        'content': "Please rate from 1 to 5.",
                        'type': 'prompt'
                    })
            except ValueError:
                session['messages'].append({
                    'role': 'bot',
                    'content': "Please respond with a number from 1 to 5.",
                    'type': 'prompt'
                })
        
        session.modified = True
    
    return render_template('chat_unified.html', messages=session['messages'], stage=session['stage'])

def generate_misinformation():
    frameworks = list(controller.frameworks.keys())
    framework = random.choice(frameworks)
    session['misinfo_framework'] = framework
    
    try:
        module = controller.frameworks[framework]
        params = controller._get_default_params(framework)
        misinfo_text, metadata = module.simulate_misinformation(params)
        session['misinfo_metadata'] = metadata
        return misinfo_text
    except:
        # Fallback to sample claims
        claims = [
            "Drinking hot water cures all viruses instantly",
            "5G towers cause cancer and control minds",
            "Vaccines contain microchips for surveillance",
            "Climate change is completely fake"
        ]
        return random.choice(claims)

def generate_correction(misinfo_text):
    frameworks = list(controller.frameworks.keys())
    framework = random.choice(frameworks)
    session['correction_framework'] = framework
    
    try:
        module = controller.frameworks[framework]
        correction_text, metadata = module.generate_correction(
            misinfo_text,
            session.get('misinfo_metadata', {}),
            tone="conversational",
            cohort=session.get('occupation', 'general')
        )
        session['correction_metadata'] = metadata
        return correction_text
    except:
        return "I understand your perspective. Let me share some factual information that might help clarify this topic."

def generate_correction_response(user_input, misinfo_text):
    try:
        module = controller.frameworks[session['correction_framework']]
        response, _ = module.generate_correction(
            misinfo_text,
            session.get('misinfo_metadata', {}),
            tone="conversational",
            cohort=session.get('occupation', 'general')
        )
        return response
    except:
        return "That's an interesting point. Let me provide more information to help you understand this better."

@app.route('/complete')
def complete():
    # Save experiment data
    experiment_data = {
        'timestamp': datetime.now().isoformat(),
        'participant_id': session['participant_id'],
        'age': session['age'],
        'occupation': session['occupation'],
        'education': session['education'],
        'misinfo_framework': session.get('misinfo_framework'),
        'correction_framework': session.get('correction_framework'),
        'misinfo_text': session.get('current_misinfo'),
        'belief_before': session.get('belief_before'),
        'belief_after': session.get('belief_after'),
        'effectiveness': session.get('belief_before', 0) - session.get('belief_after', 0),
        'misinfo_attempts': session.get('misinfo_attempts', 0),
        'conversation_length': len(session.get('messages', []))
    }
    
    # Save to CSV
    os.makedirs('data/outputs', exist_ok=True)
    df = pd.DataFrame([experiment_data])
    log_path = 'data/outputs/chat_experiment_results.csv'
    
    if os.path.exists(log_path):
        df.to_csv(log_path, mode='a', header=False, index=False)
    else:
        df.to_csv(log_path, index=False)
    
    session.clear()
    return '<h2>Thank you for participating!</h2><p><a href="/">Start New Session</a></p>'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)