# Two-Factor Authentication System

## Overview

This project implements a Two-Factor Authentication (2FA) system using TOTP (Time-based One-Time Password) to enhance the security of user accounts. Users can register, set up 2FA, and log in with an additional layer of security beyond just a password.

## Features

- **User Registration**: Users can create an account and set up 2FA.
- **2FA Setup**: Users receive a QR code to scan with an authenticator app.
- **Secure Login**: Users log in with their password and a TOTP code.
- **Backup Codes**: Users can download backup codes to access their account if they lose access to their authenticator app.

## Technologies

- **Backend**: Flask
- **Frontend**: HTML, CSS, JavaScript
- **2FA Library**: PyOTP
- **QR Code Generation**: qrcode

## Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/Two-Factor-Authentication-System.git
   cd Two-Factor-Authentication-System



python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


pip install -r requirements.txt


python app.py
