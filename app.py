import io
import os
import cv2
import numpy as np
from PIL import Image
import streamlit as st

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Romankiv — Computer Vision Studio",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #090d16 0%, #1e1b4b 50%, #312e81 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 18px;
        margin-bottom: 2rem;
        border: 1px solid rgba(129, 140, 248, 0.25);
        box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.4);
    }
    .main-header h1 {
        color: #f8fafc;
        font-weight: 800;
        font-size: 2.5rem;
        margin: 0;
        letter-spacing: -0.03em;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .main-header h1 span.brand-accent {
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .main-header p {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 0.6rem;
        margin-bottom: 0;
    }
    .badge-container {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
        margin-top: 1.1rem;
    }
    .concept-badge {
        background: rgba(99, 102, 241, 0.18);
        color: #c7d2fe;
        border: 1px solid rgba(129, 140, 248, 0.35);
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.01em;
    }
    .info-card {
        background: #1e293b;
        border-left: 4px solid #6366f1;
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #cbd5e1;
        font-size: 0.92rem;
    }
    .stat-box {
        background: #0f172a;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        border: 1px solid #334155;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown("""
<div class="main-header">
    <h1>👁️ <span class="brand-accent">Romankiv</span> Vision Studio</h1>
    <p>Interactive Computer Vision Web Application demonstrating core digital image processing concepts from class.</p>
    <div class="badge-container">
        <span class="concept-badge">✨ Concept 1: Drawing & Annotation</span>
        <span class="concept-badge">⚡ Concept 2: Image Arithmetic & Clipping</span>
        <span class="concept-badge">📄 Concept 3: Thresholding & Binarization</span>
        <span class="concept-badge">✂️ Concept 4: Alpha Channels & Transparency</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sample images directory
SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "sample_images")
SAMPLE_MAP = {
    "Sheet Music (Bad Lighting - for Thresholding)": "sheet_music.png",
    "Santorini Landscape (for Arithmetic & Contrast)": "landscape.png",
    "Kangaroo Sign (for Alpha Channel & Masks)": "kangaroo.png",
    "Apollo Launch (for Annotation & Stamping)": "apollo_launch.png",
}

# Sidebar - Image Input & Mode Selection
with st.sidebar:
    st.header("🖼️ Input Image")
    input_source = st.radio(
        "Choose image source:",
        ["Upload your own image", "Use class sample image"],
        index=0
    )
    
    current_image_bgr = None
    
    if input_source == "Upload your own image":
        uploaded_file = st.file_uploader(
            "Upload JPG, PNG, or WEBP",
            type=["jpg", "jpeg", "png", "webp"]
        )
        if uploaded_file is not None:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            current_image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    else:
        sample_choice = st.selectbox("Select sample image:", list(SAMPLE_MAP.keys()))
        sample_path = os.path.join(SAMPLE_DIR, SAMPLE_MAP[sample_choice])
        if os.path.exists(sample_path):
            current_image_bgr = cv2.imread(sample_path, cv2.IMREAD_COLOR)
        else:
            st.warning("Sample image not found on disk. Please upload an image.")

    st.markdown("---")
    st.header("🛠️ Vision Lab Tool")
    mode = st.selectbox(
        "Select active module:",
        [
            "📄 Document & Note Cleaner (Thresholding)",
            "⚡ Photo Arithmetic & Contrast Lab (Arithmetic & Clipping)",
            "✂️ Transparent Background Studio (Alpha Channels & Masks)",
            "✏️ Meme & Annotation Studio (Drawing & Annotation)"
        ]
    )
    
    st.markdown("---")
    st.caption("Developed with OpenCV, Streamlit & NumPy")

# Fallback placeholder if no image loaded
if current_image_bgr is None:
    # Generate default demo canvas if user hasn't uploaded or selected yet
    current_image_bgr = np.zeros((400, 600, 3), dtype=np.uint8)
    cv2.rectangle(current_image_bgr, (50, 50), (550, 350), (45, 45, 60), -1)
    cv2.putText(current_image_bgr, "Please upload an image", (90, 190),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (200, 200, 255), 2, cv2.LINE_AA)
    cv2.putText(current_image_bgr, "or select a sample from sidebar", (110, 240),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (150, 150, 180), 1, cv2.LINE_AA)

# Prepare original RGB
orig_rgb = cv2.cvtColor(current_image_bgr, cv2.COLOR_BGR2RGB)
h, w, c = current_image_bgr.shape

# Main layout tabs / controls
processed_display = None
processed_download_bytes = None
download_filename = "processed_image.png"
mime_type = "image/png"

# ==========================================
# MODULE 1: THRESHOLDING & DOCUMENT CLEANER
# ==========================================
if "Thresholding" in mode:
    st.subheader("📄 Document & Note Cleaner")
    st.markdown(
        "Isolate text or notes taken under uneven lighting conditions using **Global**, **Adaptive**, or **Otsu** thresholding."
    )
    
    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
    
    with col_ctrl1:
        method = st.selectbox(
            "Thresholding Method",
            [
                "Adaptive Gaussian (Recommended for uneven lighting)",
                "Adaptive Mean",
                "Otsu's Automatic Thresholding",
                "Global Binary",
                "Global Inverse Binary"
            ]
        )
    
    gray = cv2.cvtColor(current_image_bgr, cv2.COLOR_BGR2GRAY)
    otsu_val = None
    
    with col_ctrl2:
        if "Adaptive" in method:
            block_size = st.slider("Block Size (Neighbourhood Size)", min_value=3, max_value=75, value=25, step=2)
            c_val = st.slider("Constant C (Subtracted from mean)", min_value=-30, max_value=30, value=10, step=1)
        elif "Otsu" in method:
            st.info("Otsu's binarization automatically calculates the optimal threshold value by minimizing intraclass variance.")
            otsu_invert = st.checkbox("Invert Output (Black background / White foreground)", value=False)
        else:
            thresh_val = st.slider("Global Threshold Cutoff", min_value=0, max_value=255, value=130, step=1)
            
    with col_ctrl3:
        apply_blur = st.checkbox("Pre-smooth noise with Gaussian Blur (5x5)", value=False)
        st.markdown(f"**Image Dimensions:** `{w} x {h} px`")
        
    # Processing
    src_gray = cv2.GaussianBlur(gray, (5, 5), 0) if apply_blur else gray

    if "Adaptive Gaussian" in method:
        processed_bin = cv2.adaptiveThreshold(
            src_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, c_val
        )
        explanation = f"Applied `cv2.adaptiveThreshold` with `ADAPTIVE_THRESH_GAUSSIAN_C`, block size `{block_size}`, and C constant `{c_val}`."
    elif "Adaptive Mean" in method:
        processed_bin = cv2.adaptiveThreshold(
            src_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, c_val
        )
        explanation = f"Applied `cv2.adaptiveThreshold` with `ADAPTIVE_THRESH_MEAN_C`, block size `{block_size}`, and C constant `{c_val}`."
    elif "Otsu" in method:
        thresh_flag = cv2.THRESH_BINARY_INV if otsu_invert else cv2.THRESH_BINARY
        otsu_val, processed_bin = cv2.threshold(src_gray, 0, 255, thresh_flag + cv2.THRESH_OTSU)
        explanation = f"Applied Otsu binarization: automatically calculated threshold cutoff = **{otsu_val:.1f}**."
    elif "Global Inverse" in method:
        _, processed_bin = cv2.threshold(src_gray, thresh_val, 255, cv2.THRESH_BINARY_INV)
        explanation = f"Applied global inverse thresholding with cutoff `{thresh_val}` (`cv2.THRESH_BINARY_INV`)."
    else:
        _, processed_bin = cv2.threshold(src_gray, thresh_val, 255, cv2.THRESH_BINARY)
        explanation = f"Applied global binary thresholding with cutoff `{thresh_val}` (`cv2.THRESH_BINARY`)."

    st.markdown(f"<div class='info-card'>💡 {explanation}</div>", unsafe_allow_html=True)
    
    # Converted for display
    processed_display = cv2.cvtColor(processed_bin, cv2.COLOR_GRAY2RGB)
    
    # Buffer for download
    success, encoded_img = cv2.imencode(".png", processed_bin)
    if success:
        processed_download_bytes = encoded_img.tobytes()
        download_filename = "thresholded_clean.png"

# ========================================================
# MODULE 2: PHOTO ARITHMETIC, CONTRAST & CLIPPING LAB
# ========================================================
elif "Arithmetic" in mode:
    st.subheader("⚡ Photo Arithmetic & Contrast Lab")
    st.markdown(
        "Control brightness using `cv2.add` / `cv2.subtract`, contrast with `cv2.multiply`, and toggle `np.clip` to witness uint8 overflow wrapping!"
    )
    
    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
    
    with col_ctrl1:
        brightness_val = st.slider("Brightness Offset (`cv2.add` / `cv2.subtract`)", min_value=-100, max_value=100, value=30, step=5)
    
    with col_ctrl2:
        contrast_val = st.slider("Contrast Factor (`cv2.multiply`)", min_value=0.2, max_value=2.5, value=1.2, step=0.05)
        
    with col_ctrl3:
        enable_clip = st.checkbox(
            "Enable Clipping with np.clip(0, 255)",
            value=True,
            help="When checked, values above 255 saturate gracefully. When unchecked, values wrap around via uint8 modulo, revealing the overflow bug taught in class!"
        )

    # 1. Apply Contrast multiplication
    # As taught in Cell 25-29 of the class notebook:
    # cv2.multiply(np.float64(img), matrix_ones, scale=contrast)
    mult_matrix = np.ones(current_image_bgr.shape, dtype=np.float64) * contrast_val
    scaled = cv2.multiply(np.float64(current_image_bgr), mult_matrix)
    
    # 2. Apply Brightness offset
    if brightness_val >= 0:
        add_matrix = np.ones(scaled.shape, dtype=np.float64) * brightness_val
        arith_result = cv2.add(scaled, add_matrix)
    else:
        sub_matrix = np.ones(scaled.shape, dtype=np.float64) * abs(brightness_val)
        arith_result = cv2.subtract(scaled, sub_matrix)
        
    # 3. Handle clipping vs raw uint8 cast
    if enable_clip:
        final_bgr = np.uint8(np.clip(arith_result, 0, 255))
        st.markdown(
            "<div class='info-card'>✅ <b>Clipping Enabled:</b> Values saturated between <code>[0, 255]</code> using <code>np.clip()</code> before casting to <code>np.uint8</code>. Highlights and shadows remain stable.</div>",
            unsafe_allow_html=True
        )
    else:
        # Intentionally casting directly to uint8 without clip to demonstrate the overflow bug from notebook!
        final_bgr = np.uint8(arith_result)
        st.markdown(
            "<div class='info-card' style='border-left-color: #ef4444;'>⚠️ <b>Overflow Active (Clipping OFF):</b> Floating-point values were cast directly to <code>np.uint8</code>. Pixels exceeding 255 roll over modulo 256 (e.g. 260 becomes 4), causing solarized, inverted rainbow artifacts!</div>",
            unsafe_allow_html=True
        )

    processed_display = cv2.cvtColor(final_bgr, cv2.COLOR_BGR2RGB)
    success, encoded_img = cv2.imencode(".png", final_bgr)
    if success:
        processed_download_bytes = encoded_img.tobytes()
        download_filename = "photo_arithmetic.png"

# ========================================================
# MODULE 3: ALPHA CHANNELS & TRANSPARENT BACKGROUND
# ========================================================
elif "Alpha Channels" in mode:
    st.subheader("✂️ Transparent Background Studio")
    st.markdown(
        "Extract foreground objects and generate transparent PNGs with 4-channel BGRA arrays using `cv2.split`, `cv2.bitwise_not`, and `cv2.merge`."
    )
    
    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
    
    with col_ctrl1:
        bg_target = st.selectbox(
            "Background Color Type to Remove",
            ["Bright / Light Background (e.g., White canvas)", "Dark / Black Background"]
        )
        
    with col_ctrl2:
        alpha_threshold = st.slider("Alpha Threshold Sensitivity", min_value=1, max_value=254, value=220, step=1)
        invert_mask = st.checkbox("Invert Foreground / Background Mask (`cv2.bitwise_not`)", value=False)
        
    with col_ctrl3:
        max_opacity = st.slider(
            "Max Opacity (Alpha Ceiling)",
            min_value=50, max_value=255, value=255, step=5,
            help="Setting below 255 produces a semi-transparent foreground, as practiced in notebook Cell 50/55."
        )
        smooth_edges = st.checkbox("Feather Mask Edges (Soft blur)", value=False)

    # Grayscale conversion
    gray = cv2.cvtColor(current_image_bgr, cv2.COLOR_BGR2GRAY)
    
    # Compute threshold mask
    if "Bright" in bg_target:
        # Background is light (e.g., > 220), foreground is darker
        _, thresh = cv2.threshold(gray, alpha_threshold, max_opacity, cv2.THRESH_BINARY)
        # Background gets 255, foreground gets 0. We invert so foreground is opaque
        mask = cv2.bitwise_not(thresh) if not invert_mask else thresh
    else:
        # Background is dark (e.g., < threshold)
        _, thresh = cv2.threshold(gray, alpha_threshold, max_opacity, cv2.THRESH_BINARY)
        # Foreground is bright
        mask = thresh if not invert_mask else cv2.bitwise_not(thresh)
        
    if smooth_edges:
        mask = cv2.GaussianBlur(mask, (5, 5), 0)

    # Split channels and merge with alpha channel
    # Exact technique from Notebook Cell 53 & 55:
    b, g, r = cv2.split(current_image_bgr)
    rgba = cv2.merge([b, g, r, mask])
    
    # For Streamlit display (convert BGRA to RGBA)
    display_rgba = cv2.cvtColor(rgba, cv2.COLOR_BGRA2RGBA)
    processed_display = display_rgba
    
    st.markdown(
        f"<div class='info-card'>✂️ <b>Alpha Channel Created:</b> Extracted channels with <code>cv2.split()</code>, generated binary transparency mask (opacity ceiling = <code>{max_opacity}</code>), and merged into 4-channel RGBA with <code>cv2.merge()</code>.</div>",
        unsafe_allow_html=True
    )
    
    success, encoded_img = cv2.imencode(".png", rgba)
    if success:
        processed_download_bytes = encoded_img.tobytes()
        download_filename = "transparent_background.png"

# ========================================================
# MODULE 4: DRAWING & ANNOTATION / MEME STUDIO
# ========================================================
elif "Annotation" in mode:
    st.subheader("✏️ Meme & Annotation Studio")
    st.markdown(
        "Draw shapes, highlight regions, and place anti-aliased text annotations using `cv2.putText`, `cv2.rectangle`, `cv2.circle`, and `cv2.line`."
    )
    
    annotated_bgr = current_image_bgr.copy()
    
    col_ctrl1, col_ctrl2 = st.columns(2)
    
    with col_ctrl1:
        st.markdown("##### 📝 Text Annotation (`cv2.putText`)")
        caption_text = st.text_input("Caption Text", value="Apollo Saturn V Launch")
        font_choice = st.selectbox(
            "Font Face",
            [
                "FONT_HERSHEY_SIMPLEX",
                "FONT_HERSHEY_PLAIN",
                "FONT_HERSHEY_DUPLEX",
                "FONT_HERSHEY_COMPLEX",
                "FONT_HERSHEY_TRIPLEX"
            ]
        )
        font_face = getattr(cv2, font_choice)
        font_scale = st.slider("Font Scale", min_value=0.5, max_value=3.0, value=1.0, step=0.1)
        font_thickness = st.slider("Font Thickness", min_value=1, max_value=6, value=2, step=1)
        font_color_hex = st.color_picker("Text Color", value="#FFFFFF")
        
        # Position presets
        pos_mode = st.selectbox("Text Position", ["Bottom Banner", "Top Header", "Center", "Custom Coordinates"])
        
    with col_ctrl2:
        st.markdown("##### 📐 Geometric Annotations (`cv2.rectangle`, `cv2.circle`, `cv2.line`)")
        add_rect = st.checkbox("Draw Bounding Box (`cv2.rectangle`)", value=True)
        if add_rect:
            rx1 = st.slider("Box X1", 0, w - 10, int(w * 0.25))
            ry1 = st.slider("Box Y1", 0, h - 10, int(h * 0.1))
            rx2 = st.slider("Box X2", 10, w, int(w * 0.75))
            ry2 = st.slider("Box Y2", 10, h, int(h * 0.85))
            rect_color_hex = st.color_picker("Box Color", value="#FF007F")
            rect_thickness = st.slider("Box Thickness", 1, 10, 3)

        add_circle = st.checkbox("Draw Focus Circle (`cv2.circle`)", value=False)
        if add_circle:
            cx = st.slider("Center X", 0, w, int(w * 0.5))
            cy = st.slider("Center Y", 0, h, int(h * 0.5))
            rad = st.slider("Radius", 5, min(w, h) // 2, 40)
            circ_color_hex = st.color_picker("Circle Color", value="#00FF88")
            circ_thick = st.slider("Circle Thickness", 1, 10, 2)
            
        add_line = st.checkbox("Draw Pointer Line (`cv2.line`)", value=False)
        if add_line:
            lx1 = st.slider("Line Start X", 0, w, 0)
            ly1 = st.slider("Line Start Y", 0, h, int(h * 0.5))
            lx2 = st.slider("Line End X", 0, w, int(w * 0.5))
            ly2 = st.slider("Line End Y", 0, h, int(h * 0.5))
            line_color_hex = st.color_picker("Line Color", value="#FFE600")
            line_thick = st.slider("Line Thickness", 1, 10, 3)

    # Color conversion helper (HEX to BGR)
    def hex_to_bgr(hex_str):
        hex_str = hex_str.lstrip('#')
        r, g, b = tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
        return (b, g, r)

    # Draw Rectangle
    if add_rect:
        cv2.rectangle(
            annotated_bgr,
            (int(rx1), int(ry1)),
            (int(rx2), int(ry2)),
            hex_to_bgr(rect_color_hex),
            thickness=rect_thickness
        )
        
    # Draw Circle
    if add_circle:
        cv2.circle(
            annotated_bgr,
            (int(cx), int(cy)),
            int(rad),
            hex_to_bgr(circ_color_hex),
            thickness=circ_thick,
            lineType=cv2.LINE_AA
        )
        
    # Draw Line
    if add_line:
        cv2.line(
            annotated_bgr,
            (int(lx1), int(ly1)),
            (int(lx2), int(ly2)),
            hex_to_bgr(line_color_hex),
            thickness=line_thick,
            lineType=cv2.LINE_AA
        )

    # Draw Text
    if caption_text.strip():
        text_size, _ = cv2.getTextSize(caption_text, font_face, font_scale, font_thickness)
        tw, th = text_size
        
        if pos_mode == "Bottom Banner":
            tx = max(10, int((w - tw) / 2))
            ty = h - 25
            # Draw semi-transparent background banner for high readability
            overlay = annotated_bgr.copy()
            cv2.rectangle(overlay, (0, h - th - 40), (w, h), (15, 23, 42), -1)
            cv2.addWeighted(overlay, 0.6, annotated_bgr, 0.4, 0, annotated_bgr)
        elif pos_mode == "Top Header":
            tx = max(10, int((w - tw) / 2))
            ty = th + 25
            overlay = annotated_bgr.copy()
            cv2.rectangle(overlay, (0, 0), (w, th + 40), (15, 23, 42), -1)
            cv2.addWeighted(overlay, 0.6, annotated_bgr, 0.4, 0, annotated_bgr)
        elif pos_mode == "Center":
            tx = max(10, int((w - tw) / 2))
            ty = int((h + th) / 2)
        else:
            tx = st.slider("Text Custom X", 0, max(1, w - tw), 20)
            ty = st.slider("Text Custom Y", th, h, th + 30)

        cv2.putText(
            annotated_bgr,
            caption_text,
            (int(tx), int(ty)),
            font_face,
            font_scale,
            hex_to_bgr(font_color_hex),
            font_thickness,
            lineType=cv2.LINE_AA
        )

    processed_display = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)
    success, encoded_img = cv2.imencode(".png", annotated_bgr)
    if success:
        processed_download_bytes = encoded_img.tobytes()
        download_filename = "annotated_image.png"

# ========================================================
# COMPARISON DISPLAY (ORIGINAL VS PROCESSED)
# ========================================================
st.markdown("---")
st.subheader("👀 Live Comparison")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### 📷 Original Image")
    st.image(orig_rgb, width="stretch", caption=f"Original ({w}x{h} px)")

with col_right:
    st.markdown("#### 🚀 Processed Output")
    if processed_display is not None:
        st.image(processed_display, width="stretch", caption="Live Processed Result")
        if processed_download_bytes:
            st.download_button(
                label=f"💾 Download {download_filename}",
                data=processed_download_bytes,
                file_name=download_filename,
                mime=mime_type,
                use_container_width=True  # kept for download_button (not deprecated here)
            )

# Technical CV Concepts Summary
with st.expander("📚 OpenCV Concepts & Notebook Mapping"):
    st.markdown("""
    This application directly implements all four computer vision concepts covered in class:
    
    1. **Drawing and Annotation**:
       - `cv2.line(img, pt1, pt2, color, thickness, lineType=cv2.LINE_AA)`
       - `cv2.circle(img, center, radius, color, thickness)`
       - `cv2.rectangle(img, pt1, pt2, color, thickness)`
       - `cv2.putText(img, text, org, fontFace, fontScale, color, thickness, cv2.LINE_AA)`
    
    2. **Image Arithmetic & Clipping**:
       - Brightness offset with `cv2.add(img, matrix)` and `cv2.subtract(img, matrix)`
       - Contrast scaling with `cv2.multiply(np.float64(img), matrix)`
       - Dynamic toggle between graceful saturation (`np.clip(..., 0, 255)`) and modulo uint8 rollover overflow artifacts.
    
    3. **Thresholding**:
       - Global binary: `cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)`
       - Global inverse: `cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY_INV)`
       - Otsu's optimal binarization: `cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)`
       - Adaptive Mean & Gaussian: `cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, C)`
    
    4. **Alpha Channels and Transparency**:
       - Split color channels: `b, g, r = cv2.split(img)`
       - Generate foreground alpha mask with `cv2.threshold()` and `cv2.bitwise_not()`
       - Assemble 4-channel BGRA with `cv2.merge([b, g, r, alpha_mask])`
    """)
