# 👁️ Romankiv — OpenCV Vision Studio Web App

An interactive, high-performance Computer Vision web application named **Romankiv**, built with **OpenCV**, **Streamlit**, and **NumPy**. This app demonstrates the core digital image processing concepts covered in class:

1. **Drawing and Annotation**: Lines, circles, rectangles, anti-aliased text overlay with semi-transparent banners (`cv2.line`, `cv2.circle`, `cv2.rectangle`, `cv2.putText`, `cv2.getTextSize`).
2. **Image Arithmetic & Clipping**: Brightness offsets with `cv2.add` and `cv2.subtract`, contrast adjustment with `cv2.multiply`, and an interactive toggle demonstrating graceful saturation (`np.clip`) vs. modulo overflow rollover wrapping.
3. **Thresholding & Document Cleaning**: Global binary (`cv2.THRESH_BINARY`), global inverse (`cv2.THRESH_BINARY_INV`), Otsu's optimal automatic thresholding (`cv2.THRESH_OTSU`), and adaptive local thresholding (`cv2.adaptiveThreshold` with Mean or Gaussian kernels) for notes taken under uneven lighting.
4. **Alpha Channels & Transparent Backgrounds**: Color channel splitting (`cv2.split`), inverse mask generation (`cv2.bitwise_not`), opacity ceiling control, and merging into 4-channel BGRA arrays (`cv2.merge`) for transparent PNG export.

---

## 🚀 Live Demo & Free 1-Click Deployment

You can deploy this application publicly without requiring any user login:

### Option A: Streamlit Community Cloud (Recommended)
1. Fork or push this repository/folder (`cv_web_app`) to your [GitHub](https://github.com).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and click **"New app"**.
3. Select your repository, branch (`main`), and set **Main file path** to `app.py`.
4. Click **Deploy!** In less than 2 minutes, your app will be live at a public URL (e.g. `https://your-username-cv-studio.streamlit.app`).

### Option B: Hugging Face Spaces
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and click **"Create new Space"**.
2. Give your space a name, select **Space SDK** $\rightarrow$ **Streamlit**, and choose **Public**.
3. Upload `app.py`, `requirements.txt`, and the `sample_images/` folder (or push via Git).
4. Your app builds and runs instantly at `https://huggingface.co/spaces/<your-username>/<space-name>`.

---

## 💻 Running Locally

To run the application locally on your computer:

```bash
# 1. Open terminal in the app directory
cd cv_web_app

# 2. Activate the virtual environment
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate

# 3. Launch Streamlit
streamlit run app.py
```

Streamlit will automatically open your default browser to `http://localhost:8501`.

---

## 📸 Key Features & Controls

| Feature | OpenCV Concepts Used | Interactive Controls |
| :--- | :--- | :--- |
| **📄 Document & Note Cleaner** | `cv2.adaptiveThreshold`, `cv2.threshold` (Global & Otsu), `cv2.GaussianBlur` | Threshold method dropdown, cutoff slider, block size slider, C constant slider, Gaussian blur toggle |
| **⚡ Photo Arithmetic & Contrast** | `cv2.add`, `cv2.subtract`, `cv2.multiply`, `np.clip` | Brightness slider (-100 to +100), contrast factor slider (0.2x to 2.5x), clipping toggle |
| **✂️ Transparent Background Studio** | `cv2.split`, `cv2.bitwise_not`, `cv2.merge`, 4-channel BGRA | Light/Dark background selector, sensitivity slider, max opacity slider, feathering toggle, PNG download |
| **✏️ Meme & Annotation Studio** | `cv2.putText`, `cv2.rectangle`, `cv2.circle`, `cv2.line`, `cv2.LINE_AA` | Caption input, font picker, font scale/thickness sliders, color pickers, bounding box, circle & pointer line sliders |

---

## 📂 Project Structure

```
cv_web_app/
├── app.py                  # Main Streamlit web application
├── requirements.txt        # Python package dependencies
├── README.md               # App documentation & deployment guide
└── sample_images/          # Built-in sample images from class notebook
    ├── sheet_music.png     # Bad lighting sheet music for Document Cleaner
    ├── landscape.png       # Santorini landscape for Arithmetic & Contrast
    ├── kangaroo.png        # Kangaroo sign for Alpha Channel Transparency
    └── apollo_launch.png   # Apollo Saturn V launch for Annotation & Stamping
```
