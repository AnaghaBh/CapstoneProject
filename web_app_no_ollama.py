from flask import Flask, render_template, request, session, redirect, url_for
import uuid
import random
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'misinformation-research-2024'

# Pre-written misinformation statements
MISINFORMATION_STATEMENTS = [
    "Drinking hot water with lemon every morning can cure any viral infection within 24 hours",
    "5G cell towers emit radiation that directly causes cancer and can control human thoughts",
    "All vaccines contain microchips that allow the government to track your location",
    "Climate change is completely fabricated by scientists to get more research funding",
    "Organic foods have zero nutritional value compared to conventionally grown foods",
    "Professional athletes never get seriously injured because their bodies are superhuman"
]

# Pre-written correction responses by framework
CORRECTION_RESPONSES = {
    'elm_general': [
        "Let me share some evidence-based information about this topic. Multiple peer-reviewed studies have shown that...",
        "I understand why this might seem plausible, but scientific research demonstrates that...",
        "That's an interesting perspective. However, medical experts and research institutions have found that..."
    ],
    'ftt': [
        "The core idea here might seem to make sense, but the specific details are actually incorrect. Here's what research shows...",
        "I can see how the general concept might be appealing, but the precise claims don't match scientific evidence...",
        "The basic premise touches on something real, but the specific assertions have been thoroughly debunked by..."
    ],
    'schema_general': [
        "I understand this connects to concerns about health and safety, which are really important. What's actually true is...",
        "Your concern for wellbeing is completely valid. The real facts that can help protect you and your family are...",
        "This touches on values we all share about protecting ourselves. The accurate information that serves those values is..."
    ],
    'illusory_truth': [
        "This is actually a lesser-known fact that might surprise you: the opposite is true. Recent discoveries show...",
        "Here's something most people don't realize - the actual scientific consensus is quite different from what you might expect...",
        "Interestingly, cutting-edge research has revealed some unexpected findings that contradict this common belief..."
    ]
}

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
    if 'messages' not in session:
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
                        if session['misinfo_attempts'] < 3:
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
                        correction_text = generate_correction()
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
            response = generate_correction_response()
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
    misinfo_text = random.choice(MISINFORMATION_STATEMENTS)
    session['misinfo_framework'] = random.choice(['elm_general', 'ftt', 'schema_general', 'illusory_truth'])
    return misinfo_text

def generate_correction():
    framework = random.choice(['elm_general', 'ftt', 'schema_general', 'illusory_truth'])
    session['correction_framework'] = framework
    return random.choice(CORRECTION_RESPONSES[framework])

def generate_correction_response():
    framework = session.get('correction_framework', 'elm_general')
    return random.choice(CORRECTION_RESPONSES[framework])

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
    log_path = 'data/outputs/no_ollama_results.csv'
    
    if os.path.exists(log_path):
        df.to_csv(log_path, mode='a', header=False, index=False)
    else:
        df.to_csv(log_path, index=False)
    
    session.clear()
    return '<h2>Thank you for participating!</h2><p><a href="/">Start New Session</a></p>'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)