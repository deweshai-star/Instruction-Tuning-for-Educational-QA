import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # 6 is the layout index for a blank slide in default python-pptx template
    blank_layout = prs.slide_layouts[6]
    
    # Define Color Palette (Cool Tech / Modern Academic theme)
    BG_LIGHT = RGBColor(248, 250, 252)       # Slate 50 (Very light gray-blue)
    BG_DARK = RGBColor(15, 23, 42)          # Slate 900 (Deep Indigo/Dark Gray)
    TEXT_DARK = RGBColor(15, 23, 42)        # Slate 900
    TEXT_MUTED = RGBColor(71, 85, 105)      # Slate 600 (Muted blue-gray)
    ACCENT_GOLD = RGBColor(197, 160, 89)     # Soft Gold (Highlight)
    ACCENT_BLUE = RGBColor(37, 99, 235)      # Royal Blue
    WHITE = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(226, 232, 240)    # Slate 200
    
    # Helper to set background
    def set_bg(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    # Helper to add standard titles to content slides
    def add_slide_header(slide, title_text, category_text=""):
        # Category/Tracker text
        if category_text:
            cat_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12.133), Inches(0.3))
            tf_cat = cat_box.text_frame
            tf_cat.word_wrap = True
            tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
            p_cat = tf_cat.paragraphs[0]
            p_cat.text = category_text.upper()
            p_cat.font.name = "Calibri"
            p_cat.font.size = Pt(10)
            p_cat.font.bold = True
            p_cat.font.color.rgb = ACCENT_GOLD
            p_cat.font.letter_spacing = Pt(2)
        
        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.7), Inches(12.133), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Calibri"
        p_title.font.size = Pt(32)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_DARK

    # ==========================================
    # SLIDE 1: Title Slide (Dark Background)
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_bg(slide1, BG_DARK)
    
    # Left decorative bar
    bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.12), Inches(3.8))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT_GOLD
    bar.line.color.rgb = ACCENT_GOLD
    
    # Title & Subtitle block
    title_box = slide1.shapes.add_textbox(Inches(1.2), Inches(1.7), Inches(11.0), Inches(3.0))
    tf1 = title_box.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0
    
    # Title
    p1 = tf1.paragraphs[0]
    p1.text = "Instruction Tuning for Educational QA"
    p1.font.name = "Calibri"
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_after = Pt(12)
    
    # Subtitle
    p2 = tf1.add_paragraph()
    p2.text = "Parameter-Efficient Fine-Tuning of TinyLlama 1.1B on Consumer Hardware"
    p2.font.name = "Calibri"
    p2.font.size = Pt(20)
    p2.font.color.rgb = ACCENT_GOLD
    p2.space_after = Pt(24)
    
    # Description
    p3 = tf1.add_paragraph()
    p3.text = "A framework for training and deploying domain-specific educational assistants locally on CPU"
    p3.font.name = "Calibri"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(148, 163, 184) # Slate 400
    
    # Footer metadata
    footer_box = slide1.shapes.add_textbox(Inches(1.2), Inches(5.6), Inches(6.0), Inches(1.0))
    tf_f = footer_box.text_frame
    p_f1 = tf_f.paragraphs[0]
    p_f1.text = "IITM DS AI - Natural Language Processing Project"
    p_f1.font.name = "Calibri"
    p_f1.font.size = Pt(12)
    p_f1.font.bold = True
    p_f1.font.color.rgb = WHITE
    
    p_f2 = tf_f.add_paragraph()
    p_f2.text = "Methodology: PEFT / LoRA (Low-Rank Adaptation)"
    p_f2.font.name = "Calibri"
    p_f2.font.size = Pt(11)
    p_f2.font.color.rgb = RGBColor(148, 163, 184)

    # ==========================================
    # SLIDE 2: Project Pipeline (Light Background)
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_bg(slide2, BG_LIGHT)
    add_slide_header(slide2, "End-to-End Development Pipeline", "Pipeline & Architecture")
    
    # Subtitle explanation
    desc_box = slide2.shapes.add_textbox(Inches(0.6), Inches(1.5), Inches(12.133), Inches(0.4))
    desc_tf = desc_box.text_frame
    desc_p = desc_tf.paragraphs[0]
    desc_p.text = "The complete cycle from instruction data engineering to local execution."
    desc_p.font.name = "Calibri"
    desc_p.font.size = Pt(15)
    desc_p.font.color.rgb = TEXT_MUTED
    
    # Define Card Details
    cards = [
        {
            "num": "01",
            "title": "Data Engineering",
            "bullets": [
                "Dataset: tatsu-lab/alpaca on HuggingFace",
                "Subset: 1,000 instruction-following samples",
                "Split: 900 training, 100 evaluation samples",
                "Format: Formatted into Prompt templates: Instruction, Input, and Response",
                "Max Length: 512 tokens (optimized for local memory)"
            ]
        },
        {
            "num": "02",
            "title": "Model Adaptation",
            "bullets": [
                "Base model: TinyLlama 1.1B (Chat-v1.0)",
                "Size: 1.1B parameters, decoder-only LLaMA",
                "Adaptation: LoRA (Low-Rank Adaptation) PEFT",
                "Target Modules: q_proj and v_proj",
                "Trainable params: 1.12 Million (only 0.1% of model)"
            ]
        },
        {
            "num": "03",
            "title": "CPU-Optimized Training",
            "bullets": [
                "Device: CPU-only execution (zero GPU required)",
                "Precision: Float32 for model stability on CPU",
                "Batch size: 1 per device with gradient accumulation of 4 (effective batch = 4)",
                "Optimizer: AdamW (PyTorch CPU native)",
                "Technique: Gradient Checkpointing enabled"
            ]
        },
        {
            "num": "04",
            "title": "Streamlit App",
            "bullets": [
                "Weights: Adapter output saved to safetensors (~4.5MB)",
                "Interface: Streamlit web interface (app.py)",
                "Loading: Dynamic fallback to checkpoint-25 if final adapter is absent",
                "User prompt: Generates educational QA on the fly"
            ]
        }
    ]
    
    card_width = Inches(2.8)
    card_height = Inches(4.5)
    top_pos = Inches(2.1)
    spacing = Inches(0.31)
    left_start = Inches(0.6)
    
    for i, c in enumerate(cards):
        left_pos = left_start + i * (card_width + spacing)
        
        # Base Card Shape
        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, card_width, card_height)
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.5)
        
        # Gold Accent Line at the top of the card
        accent_line = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos, top_pos, card_width, Inches(0.12))
        accent_line.fill.solid()
        accent_line.fill.fore_color.rgb = ACCENT_GOLD
        accent_line.line.color.rgb = ACCENT_GOLD
        
        # Text Frame
        tb = slide2.shapes.add_textbox(left_pos + Inches(0.15), top_pos + Inches(0.25), card_width - Inches(0.3), card_height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        
        # Number Circle Text (Simulated)
        p_num = tf.paragraphs[0]
        p_num.text = c["num"]
        p_num.font.name = "Calibri"
        p_num.font.size = Pt(28)
        p_num.font.bold = True
        p_num.font.color.rgb = ACCENT_GOLD
        p_num.space_after = Pt(2)
        
        # Title
        p_title = tf.add_paragraph()
        p_title.text = c["title"]
        p_title.font.name = "Calibri"
        p_title.font.size = Pt(16)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_DARK
        p_title.space_after = Pt(8)
        
        # Bullets
        for b in c["bullets"]:
            p_bullet = tf.add_paragraph()
            p_bullet.text = "• " + b
            p_bullet.font.name = "Calibri"
            p_bullet.font.size = Pt(9.5)
            p_bullet.font.color.rgb = TEXT_MUTED
            p_bullet.space_before = Pt(3)
            p_bullet.alignment = PP_ALIGN.LEFT

    # ==========================================
    # SLIDE 3: Methodology (Light Background)
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_bg(slide3, BG_LIGHT)
    add_slide_header(slide3, "Methodology: Low-Rank Adaptation (LoRA)", "Method & PEFT Core")
    
    # Subtitle
    desc_box3 = slide3.shapes.add_textbox(Inches(0.6), Inches(1.5), Inches(12.133), Inches(0.4))
    desc_tf3 = desc_box3.text_frame
    desc_p3 = desc_tf3.paragraphs[0]
    desc_p3.text = "Reducing trainable parameter count by 99.9% for high-efficiency adaptation on CPU hardware."
    desc_p3.font.name = "Calibri"
    desc_p3.font.size = Pt(15)
    desc_p3.font.color.rgb = TEXT_MUTED
    
    # Left Column: The Challenge
    col1_left = Inches(0.6)
    col_width = Inches(5.8)
    col_height = Inches(4.6)
    
    card_challenge = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, col1_left, Inches(2.1), col_width, col_height)
    card_challenge.fill.solid()
    card_challenge.fill.fore_color.rgb = WHITE
    card_challenge.line.color.rgb = CARD_BORDER
    card_challenge.line.width = Pt(1)
    
    # Left Column Accent top border
    accent_challenge = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, col1_left, Inches(2.1), col_width, Inches(0.1))
    accent_challenge.fill.solid()
    accent_challenge.fill.fore_color.rgb = TEXT_MUTED
    accent_challenge.line.color.rgb = TEXT_MUTED
    
    tb_c = slide3.shapes.add_textbox(col1_left + Inches(0.3), Inches(2.4), col_width - Inches(0.6), col_height - Inches(0.6))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    
    p_c_title = tf_c.paragraphs[0]
    p_c_title.text = "The Challenge: Full Parameter Tuning"
    p_c_title.font.name = "Calibri"
    p_c_title.font.size = Pt(20)
    p_c_title.font.bold = True
    p_c_title.font.color.rgb = TEXT_DARK
    p_c_title.space_after = Pt(14)
    
    bullets_c = [
        "TinyLlama contains 1,101,174,784 parameters.",
        "Full fine-tuning updates every weight tensor, requiring gradients and optimizer states for all 1.1 Billion parameters.",
        "GPU memory requirements exceed 24 GB for full float32 training, making laptop execution completely impossible.",
        "CPU training without modification results in Out-Of-Memory (OOM) errors and extremely slow iteration times."
    ]
    for b in bullets_c:
        p_b = tf_c.add_paragraph()
        p_b.text = "• " + b
        p_b.font.name = "Calibri"
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = TEXT_MUTED
        p_b.space_before = Pt(8)
        
    # Right Column: The Solution (LoRA)
    col2_left = Inches(6.933)
    
    card_solution = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, col2_left, Inches(2.1), col_width, col_height)
    card_solution.fill.solid()
    card_solution.fill.fore_color.rgb = WHITE
    card_solution.line.color.rgb = CARD_BORDER
    card_solution.line.width = Pt(1.5)
    
    # Right Column Accent top border (Gold)
    accent_solution = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, col2_left, Inches(2.1), col_width, Inches(0.1))
    accent_solution.fill.solid()
    accent_solution.fill.fore_color.rgb = ACCENT_GOLD
    accent_solution.line.color.rgb = ACCENT_GOLD
    
    tb_s = slide3.shapes.add_textbox(col2_left + Inches(0.3), Inches(2.4), col_width - Inches(0.6), col_height - Inches(0.6))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True
    
    p_s_title = tf_s.paragraphs[0]
    p_s_title.text = "The PEFT Solution: Low-Rank Adaptation"
    p_s_title.font.name = "Calibri"
    p_s_title.font.size = Pt(20)
    p_s_title.font.bold = True
    p_s_title.font.color.rgb = TEXT_DARK
    p_s_title.space_after = Pt(14)
    
    bullets_s = [
        "Freezes the pre-trained model weights (99.9% of base model remains unchanged).",
        "Injects low-rank trainable decomposition matrices (A and B) into attention layers.",
        "Target Modules: Query projection (q_proj) and Value projection (v_proj).",
        "LoRA Hyperparameters: Rank (r) = 8, Alpha = 16, Dropout = 0.05.",
        "Trainable parameters: 1,126,400 (just 0.1023% of total).",
        "Storage footprint: Lightweight adapters weigh only 4.5 MB on disk."
    ]
    for b in bullets_s:
        p_b = tf_s.add_paragraph()
        p_b.text = "• " + b
        p_b.font.name = "Calibri"
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = TEXT_MUTED
        p_b.space_before = Pt(5)

    # ==========================================
    # SLIDE 4: Training & System Configuration (Light Background)
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_bg(slide4, BG_LIGHT)
    add_slide_header(slide4, "Training Configuration & Loss Performance", "Setup & Results")
    
    # Subtitle
    desc_box4 = slide4.shapes.add_textbox(Inches(0.6), Inches(1.5), Inches(12.133), Inches(0.4))
    desc_tf4 = desc_box4.text_frame
    desc_p4 = desc_tf4.paragraphs[0]
    desc_p4.text = "Detailed execution arguments and empirical training loss trends."
    desc_p4.font.name = "Calibri"
    desc_p4.font.size = Pt(15)
    desc_p4.font.color.rgb = TEXT_MUTED
    
    # Left Column: Configuration Parameters Card
    col1_left = Inches(0.6)
    col_width = Inches(5.8)
    col_height = Inches(4.6)
    
    card_config = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, col1_left, Inches(2.1), col_width, col_height)
    card_config.fill.solid()
    card_config.fill.fore_color.rgb = WHITE
    card_config.line.color.rgb = CARD_BORDER
    card_config.line.width = Pt(1)
    
    accent_config = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, col1_left, Inches(2.1), col_width, Inches(0.1))
    accent_config.fill.solid()
    accent_config.fill.fore_color.rgb = TEXT_DARK
    accent_config.line.color.rgb = TEXT_DARK
    
    tb_cf = slide4.shapes.add_textbox(col1_left + Inches(0.3), Inches(2.4), col_width - Inches(0.6), col_height - Inches(0.6))
    tf_cf = tb_cf.text_frame
    tf_cf.word_wrap = True
    
    p_cf_title = tf_cf.paragraphs[0]
    p_cf_title.text = "Training Arguments (CPU Optimized)"
    p_cf_title.font.name = "Calibri"
    p_cf_title.font.size = Pt(20)
    p_cf_title.font.bold = True
    p_cf_title.font.color.rgb = TEXT_DARK
    p_cf_title.space_after = Pt(12)
    
    configs = [
        "Device: Forced CPU (use_cpu=True)",
        "Precision: Float32 (no FP16/BF16 on CPU)",
        "Batch Size: 1 sample per device",
        "Gradient Accumulation: 4 steps (Effective Batch Size = 4)",
        "Optimizer: AdamW (PyTorch native CPU)",
        "Learning Rate: 2e-4 (Constant scheduler, Warmup steps = 5)",
        "Gradient Checkpointing: Enabled to minimize CPU RAM",
        "Save Strategy: Saves checkpoint every 25 steps"
    ]
    for c in configs:
        p_c = tf_cf.add_paragraph()
        p_c.text = "• " + c
        p_c.font.name = "Calibri"
        p_c.font.size = Pt(12)
        p_c.font.color.rgb = TEXT_MUTED
        p_c.space_before = Pt(6)
        
    # Right Column: Empirical Loss Progression (using a beautiful Table)
    col2_left = Inches(6.933)
    
    card_loss = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, col2_left, Inches(2.1), col_width, col_height)
    card_loss.fill.solid()
    card_loss.fill.fore_color.rgb = WHITE
    card_loss.line.color.rgb = CARD_BORDER
    card_loss.line.width = Pt(1.5)
    
    accent_loss = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, col2_left, Inches(2.1), col_width, Inches(0.1))
    accent_loss.fill.solid()
    accent_loss.fill.fore_color.rgb = ACCENT_GOLD
    accent_loss.line.color.rgb = ACCENT_GOLD
    
    tb_l = slide4.shapes.add_textbox(col2_left + Inches(0.3), Inches(2.3), col_width - Inches(0.6), Inches(0.8))
    tf_l = tb_l.text_frame
    p_l_title = tf_l.paragraphs[0]
    p_l_title.text = "Empirical Training Loss Metrics"
    p_l_title.font.name = "Calibri"
    p_l_title.font.size = Pt(20)
    p_l_title.font.bold = True
    p_l_title.font.color.rgb = TEXT_DARK
    
    # Add table inside the right card
    rows = 6
    cols = 4
    table_left = col2_left + Inches(0.3)
    table_top = Inches(2.95)
    table_width = col_width - Inches(0.6)
    table_height = Inches(3.2)
    
    table_shape = slide4.shapes.add_table(rows, cols, table_left, table_top, table_width, table_height)
    table = table_shape.table
    
    # Set Column Widths
    table.columns[0].width = Inches(1.1)
    table.columns[1].width = Inches(1.2)
    table.columns[2].width = Inches(1.4)
    table.columns[3].width = Inches(1.5)
    
    # Headers
    headers = ["Step", "Epoch", "Training Loss", "Learning Rate"]
    for col_idx, text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = TEXT_DARK
        cell.text = text
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        
    # Data Rows from trainer_state.json
    data = [
        ["5", "0.022", "1.8983", "2.0e-4"],
        ["10", "0.044", "1.8030", "2.0e-4"],
        ["15", "0.067", "1.6545", "2.0e-4"],
        ["20", "0.089", "1.4351", "2.0e-4"],
        ["25", "0.111", "1.5245", "2.0e-4"]
    ]
    
    for row_idx, row_data in enumerate(data):
        for col_idx, value in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            # Alternating row colors
            if row_idx % 2 == 0:
                cell.fill.fore_color.rgb = RGBColor(241, 245, 249) # Slate 100
            else:
                cell.fill.fore_color.rgb = WHITE
            cell.text = value
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.font.name = "Calibri"
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_MUTED if col_idx != 2 else TEXT_DARK
            if col_idx == 2:
                p.font.bold = True

    # ==========================================
    # SLIDE 5: Results & Classroom Deployment (Dark Background)
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_bg(slide5, BG_DARK)
    
    # Title
    t_box5 = slide5.shapes.add_textbox(Inches(0.6), Inches(0.7), Inches(12.133), Inches(0.8))
    tf5 = t_box5.text_frame
    p_t5 = tf5.paragraphs[0]
    p_t5.text = "Results & Classroom Deployment"
    p_t5.font.name = "Calibri"
    p_t5.font.size = Pt(32)
    p_t5.font.bold = True
    p_t5.font.color.rgb = WHITE
    
    # Subtitle
    sub_box5 = slide5.shapes.add_textbox(Inches(0.6), Inches(1.4), Inches(12.133), Inches(0.4))
    sub_tf5 = sub_box5.text_frame
    sub_p5 = sub_tf5.paragraphs[0]
    sub_p5.text = "Interactive local deployment with highly structured educational responses."
    sub_p5.font.name = "Calibri"
    sub_p5.font.size = Pt(16)
    sub_p5.font.color.rgb = ACCENT_GOLD
    
    # Two Columns for Results: Streamlit App layout vs Output Showcase
    # Col 1: Streamlit App Representation
    col_w = Inches(5.8)
    col_h = Inches(4.5)
    
    c1_shape = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(2.0), col_w, col_h)
    c1_shape.fill.solid()
    c1_shape.fill.fore_color.rgb = RGBColor(30, 41, 59) # Slate 800 (Card background)
    c1_shape.line.color.rgb = ACCENT_GOLD
    c1_shape.line.width = Pt(1)
    
    tb_ui = slide5.shapes.add_textbox(Inches(0.9), Inches(2.2), col_w - Inches(0.6), col_h - Inches(0.4))
    tf_ui = tb_ui.text_frame
    tf_ui.word_wrap = True
    
    p_ui_t = tf_ui.paragraphs[0]
    p_ui_t.text = "Streamlit Web App (app.py)"
    p_ui_t.font.name = "Calibri"
    p_ui_t.font.size = Pt(20)
    p_ui_t.font.bold = True
    p_ui_t.font.color.rgb = WHITE
    p_ui_t.space_after = Pt(10)
    
    ui_points = [
        "Interactive Graphical User Interface (GUI) running in the web browser locally.",
        "Proactively checks directory for fine-tuned LoRA adapters (final-adapter/ or checkpoint-25/).",
        "Graceful Fallback: Detects missing adapter directory and auto-loads base TinyLlama model.",
        "Input interface: Custom prompt text area for entering instructions + context text box.",
        "GPU-Free Generation: Executes tokenizer and PeftModel inference directly on CPU in under 45s."
    ]
    for pt in ui_points:
        p_pt = tf_ui.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.name = "Calibri"
        p_pt.font.size = Pt(11.5)
        p_pt.font.color.rgb = RGBColor(203, 213, 225) # Slate 300
        p_pt.space_before = Pt(6)
        
    # Col 2: Sample QA Output (Card Box)
    c2_shape = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.933), Inches(2.0), col_w, col_h)
    c2_shape.fill.solid()
    c2_shape.fill.fore_color.rgb = WHITE
    c2_shape.line.color.rgb = CARD_BORDER
    c2_shape.line.width = Pt(1)
    
    tb_qa = slide5.shapes.add_textbox(Inches(7.233), Inches(2.2), col_w - Inches(0.6), col_h - Inches(0.4))
    tf_qa = tb_qa.text_frame
    tf_qa.word_wrap = True
    
    p_qa_t = tf_qa.paragraphs[0]
    p_qa_t.text = "Sample Inference Performance"
    p_qa_t.font.name = "Calibri"
    p_qa_t.font.size = Pt(20)
    p_qa_t.font.bold = True
    p_qa_t.font.color.rgb = TEXT_DARK
    p_qa_t.space_after = Pt(10)
    
    # Custom Question Block
    p_q = tf_qa.add_paragraph()
    p_q.text = "Instruction (Question):"
    p_q.font.name = "Calibri"
    p_q.font.size = Pt(11)
    p_q.font.bold = True
    p_q.font.color.rgb = ACCENT_GOLD
    p_q.space_before = Pt(4)
    
    p_q_val = tf_qa.add_paragraph()
    p_q_val.text = '“Explain the process of photosynthesis to a middle school student.”'
    p_q_val.font.name = "Calibri"
    p_q_val.font.size = Pt(12)
    p_q_val.font.italic = True
    p_q_val.font.color.rgb = TEXT_DARK
    p_q_val.space_after = Pt(8)
    
    # Custom Answer Block
    p_a = tf_qa.add_paragraph()
    p_a.text = "Fine-Tuned Response Output:"
    p_a.font.name = "Calibri"
    p_a.font.size = Pt(11)
    p_a.font.bold = True
    p_a.font.color.rgb = ACCENT_BLUE
    
    p_a_val = tf_qa.add_paragraph()
    p_a_val.text = (
        "“Photosynthesis is the process by which green plants and some other organisms "
        "use sunlight to synthesize foods from carbon dioxide and water. Photosynthesis in plants "
        "generally involves the green pigment chlorophyll and generates oxygen as a byproduct.\n\n"
        "Simply put: Plants use solar energy, water, and air to make their own food and release "
        "clean air for us to breathe!”"
    )
    p_a_val.font.name = "Calibri"
    p_a_val.font.size = Pt(11)
    p_a_val.font.color.rgb = TEXT_MUTED
    p_a_val.space_before = Pt(2)
    
    # Save Presentation
    output_filename = "Instruction Tuning for Educational QA.pptx"
    prs.save(output_filename)
    print(f"Presentation saved successfully as '{output_filename}'!")

if __name__ == "__main__":
    create_presentation()
