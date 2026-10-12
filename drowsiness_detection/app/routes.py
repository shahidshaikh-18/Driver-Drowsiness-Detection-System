from flask import Blueprint, render_template, request, redirect, url_for, session, Response, jsonify
import mysql.connector
from database.db_config import get_db_connection
from app.camera import gen_frames
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import subprocess
import psutil

main = Blueprint('main', __name__)

# Home route
@main.route('/')
def home():
    return redirect(url_for('main.login'))

# Login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return "Missing fields. Please fill out the form completely.", 400

        # === Hardcoded admin credentials ===
        ADMIN_USERNAME = "admin"
        ADMIN_PASSWORD = "admin123"

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['user_id'] = 0
            session['username'] = ADMIN_USERNAME
            return redirect(url_for('main.admin_dashboard'))

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                stored_password_hash = user['password']
                if check_password_hash(stored_password_hash, password):
                    session['user_id'] = user['id']
                    session['username'] = user['username']

                    cursor.execute("UPDATE users SET last_login = %s WHERE id = %s", (datetime.now(), user['id']))
                    conn.commit()

                    cursor.close()
                    conn.close()

                    return redirect(url_for('main.dashboard'))
                else:
                    cursor.close()
                    conn.close()
                    return "Invalid password!"
            else:
                cursor.close()
                conn.close()
                return "Invalid Username!"

        except Exception as e:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return f"An error occurred during login: {e}", 500

    return render_template('login.html')

# Signup
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not password or not confirm_password:
            return "Please fill all the fields!", 400

        if password != confirm_password:
            return "Passwords do not match!", 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Check if username exists
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return "Username already exists!", 400

            # Check if email exists
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return "Email already exists!", 400

            # Insert new user
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                           (username, email, hashed_password))
            conn.commit()

            cursor.close()
            conn.close()
            return redirect(url_for('main.login'))

        except Exception as e:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return f"An error occurred during signup: {e}", 500

    return render_template('signup.html')


# Dashboard for normal users
@main.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session['user_id'] == 0:
        return redirect(url_for('main.login'))
    return render_template('dashboard.html')

# Admin dashboard
@main.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['user_id'] != 0:
        return redirect(url_for('main.login'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total_users FROM users")
        result = cursor.fetchone()
        total_users = result['total_users'] if result else 0

        cursor.execute("SELECT id, email, password, last_login, last_logout FROM users")
        users = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('admin_dashboard.html', total_users=total_users, users=users)

    except Exception as e:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        return f"An error occurred loading admin dashboard: {e}", 500

# Detection Page
@main.route('/detection')
def detection():
    return render_template('detection.html')

# Video Feed Route
@main.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Start detection
@main.route('/start-detection', methods=['POST'])
def start_detection():
    try:
        subprocess.Popen(["python", "app/utils/detection.py"])
        return jsonify({'message': 'Detection started successfully.'}), 200
    except Exception as e:
        return jsonify({'message': f'Error starting detection: {str(e)}'}), 500

# Stop detection and redirect to dashboard
@main.route('/stop-detection', methods=['POST'])
def stop_detection():
    try:
        # Kill the detection.py process if it is running
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            cmdline = proc.info.get('cmdline')
            if cmdline and any('detection.py' in part for part in cmdline):
                proc.kill()
                break
        return redirect(url_for('main.dashboard'))
    except Exception as e:
        return f"Failed to stop detection: {e}", 500

# Logout
@main.route('/logout', methods=['POST'])
def logout():
    try:
        if 'user_id' in session and session['user_id'] != 0:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET last_logout = %s WHERE id = %s", (datetime.now(), session['user_id']))
            conn.commit()
            cursor.close()
            conn.close()
    except Exception as e:
        print(f"Error during logout DB update: {e}")

    session.clear()
    return redirect(url_for('main.logout_page'))

# Logout page with thank you message
@main.route('/logout-page')
def logout_page():
    return render_template('logout.html')
