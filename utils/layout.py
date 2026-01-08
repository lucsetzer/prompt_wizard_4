# utils/layout.py - BRAND COLORS ONLY
from fastapi.responses import HTMLResponse

def brand_layout(title: str, content: str, current_app: str = "dashboard") -> HTMLResponse:
    """Shared layout with Prompts Alchemy brand colors"""
    
    # Brand colors
    primary_color = "#00f5d4"      # Aqua blue
    primary_hover = "#00b4a0"      # Dark turquoise
    primary_focus = "rgba(0, 245, 212, 0.2)"
    
    # App-specific colors (subtle variations)
    app_colors = {
        "dashboard": primary_color,
        "prompt_wizard": primary_color,
        "script_wizard": primary_color,  # Same brand color!
        "hook_wizard": primary_color,
        "document_wizard": primary_color,
        "video_wizard": primary_color,
        "thumbnail_wizard": primary_color,
    }
    
    current_color = app_colors.get(current_app, primary_color)
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <title>{title} - Prompts Alchemy</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --primary: {current_color};
            --primary-hover: {primary_hover};
            --primary-focus: {primary_focus};
        }}
        
        /* Common styles for all wizards */
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
        
        .progress-bar {{
            height: 8px;
            background: #e5e7eb;
            border-radius: 4px;
            overflow: hidden;
            margin: 1rem 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--primary), #00d9ff);
            transition: width 0.5s ease;
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
            <li><a href="/dashboard"><i class="fas fa-home"></i> Dashboard</a></li>
            <li>
                <details role="list" dir="rtl">
                    <summary aria-haspopup="listbox" role="link">
                        <i class="fas fa-hat-wizard"></i> Wizards
                    </summary>
                    <ul role="listbox">
                        <li><a href="/prompt-wizard/step/1"><i class="fas fa-magic"></i> Prompt Wizard</a></li>
                        <li><a href="/script-wizard"><i class="fas fa-scroll"></i> Script Wizard</a></li>
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
