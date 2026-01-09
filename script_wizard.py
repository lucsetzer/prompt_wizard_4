# script_wizard.py - COMPLETE WITH ALL 6 STEPS AND AI GENERATION
from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse
import requests
import json


from utils.api_config import api_config
from utils.layout import brand_layout

router = APIRouter()

# ========== CONFIGURATION ==========
# ========== CONFIGURATION ==========
from utils.api_config import api_config
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

# ========== ICON MAPPING ==========
SCRIPT_ICON_MAP = {
    # Script Types
    "youtube": "fa-solid fa-youtube",
    "podcast": "fa-solid fa-podcast",
    "presentation": "fa-solid fa-presentation-screen",
    "commercial": "fa-solid fa-tv",
    "tutorial": "fa-solid fa-graduation-cap",
    "story": "fa-solid fa-book",
    
    # Audiences
    "general": "fa-solid fa-users",
    "business": "fa-solid fa-briefcase",
    "students": "fa-solid fa-graduation-cap",
    "teens": "fa-solid fa-gamepad",
    "experts": "fa-solid fa-user-tie",
    "children": "fa-solid fa-child",
    
    # Durations
    "short": "fa-solid fa-clock",
    "medium": "fa-solid fa-hourglass-half",
    "long": "fa-solid fa-hourglass-end",
    "custom": "fa-solid fa-sliders",
    
    # Styles
    "formal": "fa-solid fa-suitcase",
    "casual": "fa-solid fa-tshirt",
    "educational": "fa-solid fa-chalkboard-teacher",
    "entertaining": "fa-solid fa-laugh-beam",
    "inspirational": "fa-solid fa-fire",
    "persuasive": "fa-solid fa-bullhorn",
    
    # Tones/Voices
    "professional": "fa-solid fa-handshake",
    "friendly": "fa-solid fa-handshake-angle",
    "authoritative": "fa-solid fa-crown",
    "enthusiastic": "fa-solid fa-star",
    "humorous": "fa-solid fa-face-laugh",
    "serious": "fa-solid fa-scale-balanced",
}

# ========== NAME MAPPINGS FOR DISPLAY ==========
TYPE_NAMES = {
    "youtube": "YouTube Video",
    "podcast": "Podcast Episode",
    "presentation": "Presentation",
    "commercial": "Commercial/Ad",
    "tutorial": "Tutorial",
    "story": "Story/Narrative",
}

AUDIENCE_NAMES = {
    "general": "General Audience",
    "business": "Business Professionals",
    "students": "Students",
    "teens": "Teenagers",
    "experts": "Experts",
    "children": "Children",
}

DURATION_NAMES = {
    "short": "Short (30-60 seconds)",
    "medium": "Medium (1-3 minutes)",
    "long": "Long (5+ minutes)",
    "custom": "Custom Length",
}

STYLE_NAMES = {
    "formal": "Formal",
    "casual": "Casual",
    "educational": "Educational",
    "entertaining": "Entertaining",
    "inspirational": "Inspirational",
    "persuasive": "Persuasive",
}

VOICE_NAMES = {
    "professional": "Professional",
    "friendly": "Friendly",
    "authoritative": "Authoritative",
    "enthusiastic": "Enthusiastic",
    "humorous": "Humorous",
    "serious": "Serious",
}

# ========== LAYOUT FUNCTION ==========
def script_layout(title: str, content: str, step: int = 1) -> HTMLResponse:
    """Layout with Prompts Alchemy brand colors"""
    
    progress_percent = (step / 6) * 100 if step <= 6 else 100
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <title>{title} - Prompts Alchemy</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --primary: #00f5d4;
            --primary-hover: #00b4a0;
            --primary-focus: rgba(0, 245, 212, 0.2);
        }}
        
        .step-card {{
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
            color: inherit;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.75rem;
            min-height: 180px;
            justify-content: center;
        }}
        
        .step-card:hover {{
            border-color: var(--primary);
            transform: translateY(-4px);
            box-shadow: 0 4px 12px rgba(0, 245, 212, 0.15);
            background: rgba(0, 245, 212, 0.03);
        }}
        
        .step-icon {{
            font-size: 2.5rem;
            color: var(--primary);
            margin-bottom: 0.5rem;
        }}
        
        .progress-container {{
            margin: 2rem 0;
        }}
        
        .progress-bar {{
            height: 8px;
            background: #e5e7eb;
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--primary), #00d9ff);
            width: {progress_percent}%;
            transition: width 0.5s ease;
        }}
        
        .progress-steps {{
            display: flex;
            justify-content: space-between;
            margin-top: 0.5rem;
            font-size: 0.85rem;
            color: #666;
        }}
        
        .progress-step {{
            text-align: center;
            flex: 1;
        }}
        
        .progress-step.active {{
            color: var(--primary);
            font-weight: bold;
        }}
        
        /* Script output styling */
        .script-output {{
            background: white;
            color: #1f2937;
            padding: 2rem;
            border-radius: 8px;
            border: 1px solid #e5e7eb;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            position: relative;
            margin: 2rem 0;
            line-height: 1.6;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        
        .script-output::before {{
            content: '📜';
            position: absolute;
            top: -15px;
            left: 20px;
            background: white;
            padding: 0 10px;
            font-size: 1.5rem;
        }}
    </style>
</head>
<body>
    <nav class="container">
        <ul>
            <li><strong><a href="/" style="text-decoration:none; color: var(--primary);">
                <i class="fas fa-flask"></i> Prompts Alchemy
            </a></strong></li>
        </ul>
        <ul>
            
            <li>
                <details role="list" dir="rtl">
                    <summary aria-haspopup="listbox" role="link">
                        <i class="fas fa-hat-wizard"></i> Wizards
                    </summary>
                    <ul role="listbox">
                        <li><a href="/prompt-wizard/step/1"><i class="fas fa-magic"></i> Prompt Wizard</a></li>
                        <li><a href="/script-wizard/step/1"><i class="fas fa-scroll"></i> Script Wizard</a></li>
                        <li><a href="#"><i class="fas fa-fish"></i> Hook Wizard</a></li>
                        <li><a href="#"><i class="fas fa-file-alt"></i> Document Wizard</a></li>
                        <li><a href="#"><i class="fas fa-video"></i> Video Wizard</a></li>
                        <li><a href="#"><i class="fas fa-image"></i> Thumbnail Wizard</a></li>
                    </ul>
                </details>
            </li>
        </ul>
    </nav>
    
    <main class="container">
        {content}
    </main>
</body>
</html>'''
    return HTMLResponse(content=html)

# ========== SCRIPT WIZARD HOME ==========
@router.get("/")
async def home():
    """Standalone home page for Script Wizard"""
    content = '''
    <div style="text-align: center; padding: 4rem 0;">
        <h1 style="color: #8b5cf6;">
            <i class="fas fa-scroll"></i><br>
            Script Wizard
        </h1>
        <p style="font-size: 1.25rem; color: #6b7280; max-width: 500px; margin: 1rem auto;">
            Generate professional scripts for videos, podcasts, and presentations.
        </p>
        
        <div style="margin: 3rem 0;">
            <a href="/script-wizard/step/1" role="button" style="padding: 1rem 2.5rem; font-size: 1.25rem;">
                <i class="fas fa-magic"></i> Start Script Wizard
            </a>
        </div>
    </div>
    '''
    return script_layout("Script Wizard Home", content, step=0)  # step=0 for no progress bar


@router.get("/script-wizard")
async def script_wizard_home():
    content = '''
    <article style="text-align: center; padding: 3rem 0;">
        <h1><i class="fas fa-scroll" style="color: var(--primary);"></i> Script Wizard</h1>
        <p class="lead" style="font-size: 1.25rem; color: #666; margin: 1rem 0 2rem 0;">
            Transform your ideas into professional scripts
        </p>
        
        <div style="max-width: 600px; margin: 0 auto 3rem auto; text-align: left;">
            <div class="card" style="margin-bottom: 1rem;">
                <h4><i class="fas fa-film" style="color: var(--primary);"></i> Multiple Formats</h4>
                <p>YouTube videos, podcasts, presentations, commercials</p>
            </div>
            
            <div class="card" style="margin-bottom: 1rem;">
                <h4><i class="fas fa-clock" style="color: var(--primary);"></i> Time-Based</h4>
                <p>Generate scripts for 30s, 1min, 5min, or custom lengths</p>
            </div>
            
            <div class="card">
                <h4><i class="fas fa-robot" style="color: var(--primary);"></i> AI-Powered</h4>
                <p>DeepSeek AI crafts professional, engaging scripts</p>
            </div>
        </div>
        
        <a href="/script-wizard/step/1" role="button" class="primary" style="padding: 1rem 2rem; font-size: 1.1rem;">
            <i class="fas fa-play-circle"></i> Start Script Wizard
        </a>
        
        
    </article>
    '''
    return script_layout("Script Wizard", content, step=0)

# ========== STEP 1: SCRIPT TYPE ==========
@router.get("/script-wizard/step/1")
async def script_step1():
    script_types = [
        ("youtube", "YouTube Video", "Video scripts for YouTube"),
        ("podcast", "Podcast Episode", "Audio scripts for podcasts"),
        ("presentation", "Presentation", "Slide decks and speeches"),
        ("commercial", "Commercial/Ad", "Advertisement scripts"),
        ("tutorial", "Tutorial", "Step-by-step guides"),
        ("story", "Story/Narrative", "Short stories or narratives"),
    ]
    
    type_cards = ""
    for value, label, description in script_types:
        icon_class = SCRIPT_ICON_MAP.get(value, "fa-solid fa-question")
        
        type_cards += f'''
        <a href="/script-wizard/step/2?script_type={value}" class="step-card">
            <div class="step-icon">
                <i class="{icon_class}"></i>
            </div>
            <h3 style="margin: 0; color: #333;">{label}</h3>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">{description}</p>
        </a>
        '''
    
    content = f'''
    <article>
        <header style="text-align: center; margin-bottom: 2rem;">
            <hgroup>
                <h1><i class="fas fa-scroll"></i> Script Wizard - Step 1</h1>
                <p>What type of script do you need?</p>
            </hgroup>
            
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <div class="progress-steps">
                    <div class="progress-step active">1. Type</div>
                    <div class="progress-step">2. Audience</div>
                    <div class="progress-step">3. Duration</div>
                    <div class="progress-step">4. Style</div>
                    <div class="progress-step">5. Voice</div>
                    <div class="progress-step">6. Generate</div>
                </div>
            </div>
        </header>
        
        <div class="grid" style="grid-template-columns: repeat(2, 1fr); gap: 1rem;">
            {type_cards}
        </div>
        
        <div style="text-align: center; margin-top: 3rem;">
            <a href="/script-wizard" class="secondary">
                <i class="fas fa-arrow-left"></i> Back to Script Wizard
            </a>
        </div>
    </article>
    '''
    
    return script_layout("Script Wizard - Step 1: Type", content, step=1)

# ========== STEP 2: AUDIENCE ==========
@router.get("/script-wizard/step/2")
async def script_step2(script_type: str = Query("youtube")):
    audiences = [
        ("general", "General Audience", "Everyone, all ages"),
        ("business", "Business Professionals", "Executives, managers, teams"),
        ("students", "Students", "High school or college"),
        ("teens", "Teenagers", "13-19 year olds"),
        ("experts", "Experts/Professionals", "People in the field"),
        ("children", "Children", "Under 12 years old"),
    ]
    
    audience_cards = ""
    for value, label, description in audiences:
        icon_class = SCRIPT_ICON_MAP.get(value, "fa-solid fa-question")
        
        audience_cards += f'''
        <a href="/script-wizard/step/3?script_type={script_type}&audience={value}" class="step-card">
            <div class="step-icon">
                <i class="{icon_class}"></i>
            </div>
            <h3 style="margin: 0; color: #333;">{label}</h3>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">{description}</p>
        </a>
        '''
    
    content = f'''
    <article>
        <header style="text-align: center; margin-bottom: 2rem;">
            <hgroup>
                <h1><i class="fas fa-scroll"></i> Script Wizard - Step 2</h1>
                <p>Who is your audience?</p>
            </hgroup>
            
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <div class="progress-steps">
                    <div class="progress-step">1. Type</div>
                    <div class="progress-step active">2. Audience</div>
                    <div class="progress-step">3. Duration</div>
                    <div class="progress-step">4. Style</div>
                    <div class="progress-step">5. Voice</div>
                    <div class="progress-step">6. Generate</div>
                </div>
            </div>
            
            <div class="card secondary" style="margin: 1rem auto; max-width: 600px; text-align: left;">
                <p><strong>Selected:</strong> {TYPE_NAMES.get(script_type, script_type)}</p>
            </div>
        </header>
        
        <div class="grid" style="grid-template-columns: repeat(2, 1fr); gap: 1rem;">
            {audience_cards}
        </div>
        
        <div style="text-align: center; margin-top: 3rem;">
            <a href="/script-wizard/step/1" class="secondary">
                <i class="fas fa-arrow-left"></i> Back to Step 1
            </a>
        </div>
    </article>
    '''
    
    return script_layout("Script Wizard - Step 2: Audience", content, step=2)

# ========== STEP 3: DURATION ==========
@router.get("/script-wizard/step/3")
async def script_step3(
    script_type: str = Query("youtube"),
    audience: str = Query("general")
):
    durations = [
        ("short", "Short (30-60 seconds)", "Quick ads, social media clips"),
        ("medium", "Medium (1-3 minutes)", "Standard videos, short presentations"),
        ("long", "Long (5+ minutes)", "Detailed tutorials, full episodes"),
        ("custom", "Custom Length", "Specify exact duration"),
    ]
    
    duration_cards = ""
    for value, label, description in durations:
        icon_class = SCRIPT_ICON_MAP.get(value, "fa-solid fa-question")
        
        duration_cards += f'''
        <a href="/script-wizard/step/4?script_type={script_type}&audience={audience}&duration={value}" class="step-card">
            <div class="step-icon">
                <i class="{icon_class}"></i>
            </div>
            <h3 style="margin: 0; color: #333;">{label}</h3>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">{description}</p>
        </a>
        '''
    
    content = f'''
    <article>
        <header style="text-align: center; margin-bottom: 2rem;">
            <hgroup>
                <h1><i class="fas fa-scroll"></i> Script Wizard - Step 3</h1>
                <p>How long should it be?</p>
            </hgroup>
            
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <div class="progress-steps">
                    <div class="progress-step">1. Type</div>
                    <div class="progress-step">2. Audience</div>
                    <div class="progress-step active">3. Duration</div>
                    <div class="progress-step">4. Style</div>
                    <div class="progress-step">5. Voice</div>
                    <div class="progress-step">6. Generate</div>
                </div>
            </div>
            
            <div class="card secondary" style="margin: 1rem auto; max-width: 600px; text-align: left;">
                <p><strong>Selected:</strong> {TYPE_NAMES.get(script_type)} for {AUDIENCE_NAMES.get(audience)}</p>
            </div>
        </header>
        
        <div class="grid" style="grid-template-columns: repeat(2, 1fr); gap: 1rem;">
            {duration_cards}
        </div>
        
        <div style="text-align: center; margin-top: 3rem;">
            <a href="/script-wizard/step/2?script_type={script_type}" class="secondary">
                <i class="fas fa-arrow-left"></i> Back to Step 2
            </a>
        </div>
    </article>
    '''
    
    return script_layout("Script Wizard - Step 3: Duration", content, step=3)

# ========== STEP 4: STYLE SELECTION ==========
@router.get("/script-wizard/step/4")
async def script_step4(
    script_type: str = Query("youtube"),
    audience: str = Query("general"),
    duration: str = Query("medium")
):
    styles = [
        ("formal", "Formal", "Structured, business-like"),
        ("casual", "Casual", "Relaxed, conversational"),
        ("educational", "Educational", "Teaching, informative"),
        ("entertaining", "Entertaining", "Fun, engaging"),
        ("inspirational", "Inspirational", "Motivating, uplifting"),
        ("persuasive", "Persuasive", "Convincing, sales-oriented"),
    ]
    
    style_cards = ""
    for value, label, description in styles:
        icon_class = SCRIPT_ICON_MAP.get(value, "fa-solid fa-question")
        
        style_cards += f'''
        <a href="/script-wizard/step/5?script_type={script_type}&audience={audience}&duration={duration}&style={value}" class="step-card">
            <div class="step-icon">
                <i class="{icon_class}"></i>
            </div>
            <h3 style="margin: 0; color: #333;">{label}</h3>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">{description}</p>
        </a>
        '''
    
    content = f'''
    <article>
        <header style="text-align: center; margin-bottom: 2rem;">
            <hgroup>
                <h1><i class="fas fa-scroll"></i> Script Wizard - Step 4</h1>
                <p>What style should the script have?</p>
            </hgroup>
            
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <div class="progress-steps">
                    <div class="progress-step">1. Type</div>
                    <div class="progress-step">2. Audience</div>
                    <div class="progress-step">3. Duration</div>
                    <div class="progress-step active">4. Style</div>
                    <div class="progress-step">5. Voice</div>
                    <div class="progress-step">6. Generate</div>
                </div>
            </div>
            
            <div class="card secondary" style="margin: 1rem auto; max-width: 600px; text-align: left;">
                <p><strong>Selected:</strong> {TYPE_NAMES.get(script_type)} for {AUDIENCE_NAMES.get(audience)} ({DURATION_NAMES.get(duration)})</p>
            </div>
        </header>
        
        <div class="grid" style="grid-template-columns: repeat(2, 1fr); gap: 1rem;">
            {style_cards}
        </div>
        
        <div style="text-align: center; margin-top: 3rem;">
            <a href="/script-wizard/step/3?script_type={script_type}&audience={audience}" class="secondary">
                <i class="fas fa-arrow-left"></i> Back to Step 3
            </a>
        </div>
    </article>
    '''
    
    return script_layout("Script Wizard - Step 4: Style", content, step=4)

# ========== STEP 5: VOICE/TONE SELECTION ==========
@router.get("/script-wizard/step/5")
async def script_step5(
    script_type: str = Query("youtube"),
    audience: str = Query("general"),
    duration: str = Query("medium"),
    style: str = Query("casual")
):
    voices = [
        ("professional", "Professional", "Formal, business-appropriate"),
        ("friendly", "Friendly", "Warm, approachable, casual"),
        ("authoritative", "Authoritative", "Confident, expert-like"),
        ("enthusiastic", "Enthusiastic", "Energetic, passionate"),
        ("humorous", "Humorous", "Funny, lighthearted"),
        ("serious", "Serious", "Solemn, no-nonsense"),
    ]
    
    voice_cards = ""
    for value, label, description in voices:
        icon_class = SCRIPT_ICON_MAP.get(value, "fa-solid fa-question")
        
        voice_cards += f'''
        <a href="/script-wizard/step/6?script_type={script_type}&audience={audience}&duration={duration}&style={style}&voice={value}" class="step-card">
            <div class="step-icon">
                <i class="{icon_class}"></i>
            </div>
            <h3 style="margin: 0; color: #333;">{label}</h3>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">{description}</p>
        </a>
        '''
    
    content = f'''
    <article>
        <header style="text-align: center; margin-bottom: 2rem;">
            <hgroup>
                <h1><i class="fas fa-scroll"></i> Script Wizard - Step 5</h1>
                <p>What voice or tone should it use?</p>
            </hgroup>
            
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <div class="progress-steps">
                    <div class="progress-step">1. Type</div>
                    <div class="progress-step">2. Audience</div>
                    <div class="progress-step">3. Duration</div>
                    <div class="progress-step">4. Style</div>
                    <div class="progress-step active">5. Voice</div>
                    <div class="progress-step">6. Generate</div>
                </div>
            </div>
            
            <div class="card secondary" style="margin: 1rem auto; max-width: 600px; text-align: left;">
                <p><strong>Selected:</strong> {TYPE_NAMES.get(script_type)} for {AUDIENCE_NAMES.get(audience)}<br>
                {DURATION_NAMES.get(duration)} • {STYLE_NAMES.get(style)} Style</p>
            </div>
        </header>
        
        <div class="grid" style="grid-template-columns: repeat(2, 1fr); gap: 1rem;">
            {voice_cards}
        </div>
        
        <div style="text-align: center; margin-top: 3rem;">
            <a href="/script-wizard/step/4?script_type={script_type}&audience={audience}&duration={duration}" class="secondary">
                <i class="fas fa-arrow-left"></i> Back to Step 4
            </a>
        </div>
    </article>
    '''
    
    return script_layout("Script Wizard - Step 5: Voice", content, step=5)

# ========== STEP 6: KEY POINTS INPUT ==========
@router.get("/script-wizard/step/6")
async def script_step6(
    script_type: str = Query("youtube"),
    audience: str = Query("general"),
    duration: str = Query("medium"),
    style: str = Query("casual"),
    voice: str = Query("friendly")
):
    
    # Summary of selections
    selections = f'''
    <div class="card secondary" style="margin: 1rem 0 2rem 0;">
        <div class="grid" style="grid-template-columns: repeat(5, 1fr); gap: 0.5rem; text-align: center;">
            <div>
                <small>Type</small><br>
                <strong>{TYPE_NAMES.get(script_type)}</strong>
            </div>
            <div>
                <small>Audience</small><br>
                <strong>{AUDIENCE_NAMES.get(audience)}</strong>
            </div>
            <div>
                <small>Duration</small><br>
                <strong>{DURATION_NAMES.get(duration)}</strong>
            </div>
            <div>
                <small>Style</small><br>
                <strong>{STYLE_NAMES.get(style)}</strong>
            </div>
            <div>
                <small>Voice</small><br>
                <strong>{VOICE_NAMES.get(voice)}</strong>
            </div>
        </div>
    </div>
    '''
    
    content = f'''
    <article>
        <header style="text-align: center; margin-bottom: 2rem;">
            <hgroup>
                <h1><i class="fas fa-scroll"></i> Script Wizard - Step 6</h1>
                <p>Add your key points, and AI will create the script</p>
            </hgroup>
            
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <div class="progress-steps">
                    <div class="progress-step">1. Type</div>
                    <div class="progress-step">2. Audience</div>
                    <div class="progress-step">3. Duration</div>
                    <div class="progress-step">4. Style</div>
                    <div class="progress-step">5. Voice</div>
                    <div class="progress-step active">6. Generate</div>
                </div>
            </div>
            
            {selections}
        </header>
        
        <form id="scriptForm" action="/script-wizard/generate" method="get" 
              onsubmit="showLoading(); return true;">
            <!-- Hidden fields to pass selections -->
            <input type="hidden" name="script_type" value="{script_type}">
            <input type="hidden" name="audience" value="{audience}">
            <input type="hidden" name="duration" value="{duration}">
            <input type="hidden" name="style" value="{style}">
            <input type="hidden" name="voice" value="{voice}">
            
            <div class="grid">
                <div>
                    <label for="key_points">
                        <h3>Your Key Points:</h3>
                        <p>What should the script include?</p>
                    </label>
                    <textarea 
                        id="key_points" 
                        name="key_points" 
                        rows="8" 
                        placeholder="Example: 'Explain how to bake chocolate chip cookies step by step' or 'Promote our new productivity app focusing on time-saving features'"
                        required
                        style="font-size: 1rem; padding: 1rem;"
                    ></textarea>
                </div>
                
                <div>
                    <h3>Tips for Great Scripts:</h3>
                    <div class="card" style="height: 100%;">
                        <ul style="margin: 0; padding-left: 1.5rem;">
                            <li>List 3-5 main points you want to cover</li>
                            <li>Mention any specific calls to action</li>
                            <li>Include examples or stories if relevant</li>
                            <li>Note any important facts or statistics</li>
                            <li>Don't worry about formatting - AI will handle it!</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 2rem;">
                <button type="submit" class="primary" style="padding: 1rem 2rem; font-size: 1.1rem;">
                    <i class="fas fa-magic"></i> Generate Professional Script
                </button>
                
                <a href="/script-wizard/step/5?script_type={script_type}&audience={audience}&duration={duration}&style={style}" 
                   class="secondary" style="margin-left: 1rem;">
                    <i class="fas fa-arrow-left"></i> Back
                </a>
            </div>
        </form>
        
        <!-- Loading animation -->
        <div id="loading" style="display: none; text-align: center; padding: 3rem;">
            <div style="padding: 3rem;">
                <div style="display: inline-block;">
                    <span style="animation: pulse 1.5s infinite; opacity: 0.3; display: inline-block; font-size: 2rem; margin: 0 0.25rem;">●</span>
                    <span style="animation: pulse 1.5s infinite 0.3s; opacity: 0.3; display: inline-block; font-size: 2rem; margin: 0 0.25rem;">●</span>
                    <span style="animation: pulse 1.5s infinite 0.6s; opacity: 0.3; display: inline-block; font-size: 2rem; margin: 0 0.25rem;">●</span>
                </div>
                <h3 style="margin-top: 1rem;">AI is writing your script...</h3>
                <p>This usually takes 15-30 seconds</p>
                <div class="progress-bar" style="max-width: 400px; margin: 2rem auto;">
                    <div class="progress-fill" style="width: 100%; animation: pulse 2s infinite;"></div>
                </div>
                <p><small>Do not refresh the page</small></p>
            </div>
        </div>
    </article>
    
    <style>
        @keyframes pulse {{
            0%, 100% {{ opacity: 0.3; transform: scale(0.9); }}
            50% {{ opacity: 1; transform: scale(1.1); }}
        }}
    </style>
    
    <script>
        function showLoading() {{
            document.getElementById('loading').style.display = 'block';
            document.getElementById('scriptForm').style.display = 'none';
            document.getElementById('loading').scrollIntoView({{ behavior: 'smooth' }});
        }}
    </script>
    '''
    
    return script_layout("Script Wizard - Step 6: Generate", content, step=6)

# ========== AI FUNCTION FOR SCRIPT GENERATION ==========
def generate_script_with_ai(script_type: str, audience: str, duration: str, 
                           style: str, voice: str, key_points: str) -> str:
    """Call DeepSeek API to generate a script"""
    
    # Your existing prompt building...
    prompt = f"""
    Create a {duration.lower()} {script_type} script...
    """
    
    # Your existing API call - make sure it uses api_key
    headers = {
        "Authorization": f"Bearer {api_key}",  # ← USE api_key here
        "Content-Type": "application/json"
    }
    
    # Rest of your function...
    
    system_prompt = """You are a Professional Scriptwriter and Content Creator. Create engaging, ready-to-use scripts.

CRITICAL RULES:
1. DO write complete scripts with dialogue, directions, and timing
2. DO format properly with speaker labels and directions in parentheses
3. DO make it engaging and appropriate for the audience
4. DO NOT write meta-instructions or prompts
5. DO NOT say "here is a script" - just OUTPUT the script

FORMATTING:
- Use [SPEAKER]: for dialogue
- Use (directions) for actions or notes
- Use [TIME: 00:00] for timing if relevant
- Include scene descriptions where needed

EXAMPLE OUTPUT:
[HOST]: Welcome to our channel!
(Smiling warmly to camera)
Today we're talking about baking the perfect chocolate chip cookies.

BAD: "Here's a script for a YouTube video about..."
GOOD: "[HOST]: Welcome to our channel! Today we're talking about..."
"""

    # Map durations to actual times
    duration_times = {
        "short": "30-60 seconds",
        "medium": "1-3 minutes", 
        "long": "5+ minutes",
        "custom": "custom length"
    }
    
    # Map script types to specific guidance
    type_guidance = {
        "youtube": "Create a YouTube video script with engaging visuals and calls to action.",
        "podcast": "Create a podcast script with host banter, interview questions, or monologue.",
        "presentation": "Create a presentation script with slide notes and speaker remarks.",
        "commercial": "Create a commercial script with persuasive messaging and clear call to action.",
        "tutorial": "Create a tutorial script with clear step-by-step instructions.",
        "story": "Create a narrative script with character dialogue and scene descriptions.",
    }
    
    user_message = f"""Create a {duration_times.get(duration, duration)} {script_type} script.

CONTEXT:
- Target Audience: {audience}
- Style: {style}
- Voice/Tone: {voice}
- Key Points: {key_points}

SPECIFIC REQUIREMENTS:
{type_guidance.get(script_type, "Create a professional script.")}

Make it:
- Professionally formatted with speaker labels and directions
- Ready for production/recording
- Engaging for {audience} audience
- {style} in style with {voice} tone
- Approximately {duration_times.get(duration, duration)} in length
- Include all key points mentioned above"""

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.8,
        "max_tokens": 2500,
        "stream": False
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            script = result["choices"][0]["message"]["content"].strip()
            return script
        else:
            return f"## Script Generation Error\n\nAPI returned status {response.status_code}\n\n### Sample Script Structure:\n\n[SPEAKER]: Dialogue would go here\n(Directions or actions in parentheses)\n[TIME: 00:00] Timing notes if needed\n\nKey points to cover:\n1. {key_points}"
            
    except Exception as e:
        return f"## Script Generation Error\n\n{str(e)}\n\n### Sample Script Structure:\n\n[SPEAKER]: Dialogue would go here\n(Directions or actions in parentheses)\n[TIME: 00:00] Timing notes if needed\n\nBased on your request for: {script_type} about {key_points[:50]}..."

# ========== GENERATE FINAL SCRIPT ==========
@router.get("/script-wizard/generate")
async def generate_script(
    script_type: str = Query("youtube"),
    audience: str = Query("general"),
    duration: str = Query("medium"),
    style: str = Query("casual"),
    voice: str = Query("friendly"),
    key_points: str = Query("")
):
    # Build prompt
    prompt = f"""Create a {duration} {script_type} script for {audience} audience.
    Style: {style}
    Voice: {voice}
    Key points to include: {key_points}
    
    Format as a timed script with speaker notes."""
    
    # Call DeepSeek API
    import httpx
    from config.script_config import script_config
    
    headers = {
        "Authorization": f"Bearer {script_config.API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
        "temperature": 0.7
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.deepseek.com/chat/completions",
            headers=headers,
            json=payload,
            timeout=30.0
        )
        response.raise_for_status()
        result = response.json()
        generated_text = result["choices"][0]["message"]["content"]
    
    # Your existing HTML template
    content = f'''
    <article>
        <header style="text-align: center; margin-bottom: 2rem;">
            <hgroup>
                <h1><i class="fas fa-check-circle" style="color: var(--primary);"></i> Script Ready!</h1>
                <p>Your AI-generated {script_type} script</p>
            </hgroup>
            
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <div class="progress-steps">
                    <div class="progress-step">1. Type</div>
                    <div class="progress-step">2. Audience</div>
                    <div class="progress-step">3. Duration</div>
                    <div class="progress-step">4. Style</div>
                    <div class="progress-step">5. Voice</div>
                    <div class="progress-step active">Complete!</div>
                </div>
            </div>
        </header>
        
        <div style="background: #f9fafb; padding: 2rem; border-radius: 0.75rem; margin: 2rem 0;">
            <h3>Your Generated Script:</h3>
            <pre style="white-space: pre-wrap; background: white; padding: 1.5rem; border-radius: 0.5rem; border: 1px solid #e5e7eb;">
{generated_text}
            </pre>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/script-wizard" role="button">
                <i class="fas fa-redo"></i> Create Another Script
            </a>
        </div>
    </article>
    '''
    
    return script_layout("Script Generated", content, step=6)
