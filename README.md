# Homework Helper for Busy Parents

An AI-powered web application to help Kenyan parents support their children with CBC (Competency-Based Curriculum) homework. The tool provides child-friendly explanations of homework questions through text, image, or voice input.

![Screenshot 2025-07-07 113708 png 12](https://github.com/user-attachments/assets/69e5daea-b63b-48bd-8cef-1d5c8d41afc1)


## Features

- **Multiple Input Methods**:
  - Type questions directly
  - Upload images of homework (OCR processing)
  - Voice input (browser microphone)

- **AI-Powered Explanations**:
  - Automatic subject detection
  - Child-friendly explanations
  - Step-by-step breakdown option
  - Simplified explanations toggle (for 10-year-olds)

- **User Experience**:
  - Conversation history
  - PDF export of conversations
  - Feedback system
  - Responsive design with dark mode

- **CBC-Aligned**:
  - Supports Grades 4-9 Kenyan CBC curriculum
  - Daily tips for parents
  - Subject-specific explanations

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8+
- Tesseract OCR installed on your system
- wkhtmltopdf for PDF generation (optional)
- OpenAI API key
- (Optional) M-Pesa API credentials for payment integration

## Installation

### Windows Setup

1. **Install Python**:
   - Download from [python.org](https://www.python.org/downloads/)
   - Check "Add Python to PATH" during installation

2. **Install Tesseract OCR**:
   - Download installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - Add to PATH (usually `C:\Program Files\Tesseract-OCR`)

3. **Install wkhtmltopdf** (optional for PDF export):
   - Download from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html)

### macOS/Linux Setup
  bash
  # macOS (using Homebrew)
      brew install python tesseract wkhtmltopdf

# Ubuntu/Debian
    sudo apt update
    sudo apt install python3 python3-pip tesseract-ocr wkhtmltopdf
## Project Setup
Clone the repository:
    bash
    git clone https://github.com/Bettylizzie/Homework-Helper/tree/main
    cd homework-helper
Create and activate virtual environment:
    bash
    python -m venv homework-helper-env

# Windows
homework-helper-env\Scripts\activate

# macOS/Linux
source homework-helper-env/bin/activate
Install dependencies:
bash
pip install -r requirements.txt
Create a .env file with your API keys:
env
OPENAI_API_KEY=your_openai_api_key
MPESA_CONSUMER_KEY=your_mpesa_consumer_key
MPESA_CONSUMER_SECRET=your_mpesa_consumer_secret
MPESA_PASSKEY=your_mpesa_passkey
MPESA_SHORTCODE=your_mpesa_shortcode
Running the Application
bash
streamlit run app.py
# The application will be available at:
Local URL: http://localhost:8501

Network URL: http://<your-ip>:8501

## Project Structure
text
/homework-helper/
├── app.py               # Main Streamlit application
├── ocr.py               # Image text extraction (OCR)
├── ai.py                # OpenAI response generation
├── mpesa.py             # Payment processing
├── static/
│   ├── style.css        # Custom styles
│   └── scripts.js       # Client-side JavaScript
├── templates/
│   └── layout.html      # HTML template
├── requirements.txt     # Python dependencies
└── README.md            # This file
Configuration
## Customize these settings in app.py:

Free question limit (free_questions_limit)

Subscription pricing

Color theme

Default explanation style

Troubleshooting
Pillow Installation Issues:

bash
# Try these if Pillow fails to install
pip install --upgrade pip setuptools wheel
pip install --only-binary=:all: Pillow
Tesseract Not Found:
    python
    # Add this to ocr.py if Tesseract isn't in PATH
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
wkhtmltopdf Issues:
Ensure the binary is in your PATH
On Windows, you may need to specify the path in code:
    python
    config = pdfkit.configuration(wkhtmltopdf=r'C:\path\to\wkhtmltopdf.exe')
# Contributing
  1. To contribute to Homework Helper, follow these steps:
  2. Fork this repository
  3. Create a branch (git checkout -b feature/amazing-feature)
  4. Commit your changes (git commit -m 'Add some amazing feature')
  5.  Push to the branch (git push origin feature/amazing-feature)
  6. Open a Pull Request

# License
This project uses the MIT License.

# Disclaimer:
This AI tool does not store homework content or personal data. Always review AI responses before sharing with your child. AI responses may not always be 100% accurate. Double-check when in doubt.
