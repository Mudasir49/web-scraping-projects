# Form Automation Agent

A Python-based Selenium automation script that interacts with a Microsoft Forms survey through a web browser. The script demonstrates automated navigation, element detection, dynamic form interaction, randomized option selection, and repeated execution for testing purposes.

## Features

- Automated browser control using Selenium WebDriver
- Automatic ChromeDriver installation via WebDriver Manager
- Dynamic button detection (Start, Next, Submit)
- Randomized radio button selection
- Checkbox selection with targeted and random options
- Multi-step form navigation
- Configurable number of execution cycles
- Error handling and screenshot capture on failures
- Supports multilingual button labels (e.g., English/German)

---

## Technologies Used

- Python 3.x
- Selenium
- WebDriver Manager
- Google Chrome

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/form-automation-agent.git
cd form-automation-agent
```

### 2. Create Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install selenium webdriver-manager
```

---

## Configuration

Inside the script:

```python
NUM_SUBMISSIONS = 100
```

Modify this value to control how many times the automation process runs.

Example:

```python
NUM_SUBMISSIONS = 10
```

---

## Usage

Run the script:

```bash
python form_agent.py
```

The script will:

1. Open Chrome browser
2. Navigate to the configured Microsoft Form
3. Click the Start button
4. Navigate through multiple pages
5. Select form options automatically
6. Submit the form
7. Repeat according to the configured iteration count

---

## Project Structure

```text
.
├── form_agent.py
├── README.md
└── requirements.txt
```

---

## Error Handling

If an error occurs during execution:

- The current iteration is marked as failed
- A screenshot is automatically saved

Example:

```text
error_run_5.png
```

This can help diagnose element location issues, page changes, or validation errors.

---

## Browser Configuration

Current settings:

```python
options.add_argument("--start-maximized")
```

To run without opening a visible browser window, enable headless mode:

```python
options.add_argument("--headless")
```

---

## Learning Objectives

This project demonstrates:

- Browser automation
- Selenium WebDriver usage
- Dynamic DOM interaction
- Waiting strategies with WebDriverWait
- Form automation workflows
- Exception handling in automation scripts

---

## Disclaimer

This project is intended for educational purposes, browser automation practice, testing workflows, and Selenium learning. Ensure you have permission to automate interactions with any website or online form and comply with the website's terms of service.

---

##  Contact
 
**Mudasir Ahmad**
📧 me.mudasirr@gmail.com
💼 [LinkedIn](https://www.linkedin.com/in/muhammad-mudasir-ahmad/)
