# 🐾 CSE 312 — Web Application Project

> A full-stack real-time web application built by a team of 5, featuring user authentication, a live chat system, a number-guessing mini-game, leaderboards, and media uploads. Deployed on DigitalOcean with a custom domain, HTTPS via Let's Encrypt, and served through NGINX inside Docker.

<img width="2357" height="1228" alt="image" src="https://github.com/user-attachments/assets/edb15d23-c63f-446f-9407-4a2cec6fea4f" />


---

## 🌐 Live Demo

🔗 **[https://interns20.com](https://interns20.com)** *(deployed 2024–2025)*

Deployed on **DigitalOcean** using a custom domain purchased through the **GitHub Student Developer Pack**.  
Secured with **Let's Encrypt** (SSL/TLS) and served via **NGINX** as a reverse proxy.



---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python · Flask |
| **Frontend** | HTML · CSS · JavaScript |
| **Web Server / Reverse Proxy** | NGINX |
| **Containerization** | Docker · Docker Compose |
| **SSL/TLS** | Let's Encrypt (Certbot) |
| **Cloud Hosting** | DigitalOcean (Linux Droplet) |
| **Domain** | GitHub Student Developer Pack |
| **OS** | Ubuntu (Linux) |
| **Version Control** | Git · GitHub |

---

## ✨ Features

### 💬 Real-Time Chat
- Users can post messages to a shared chat room
- Supports **scheduled message delivery** — set a delay (in seconds) before a message is posted
- Content moderation reminder shown to all users

### 🔐 User Authentication
- **Sign Up** with username, password, and password confirmation
- **Login / Logout** system with session management
- Guest access available (limited permissions — guests cannot appear on leaderboards)

### 🏆 Leaderboard
- Tracks the **most active users** based on number of comments posted
- Displays **1st, 2nd, and 3rd place** rankings
- Shows the **Previous Winner**
- Lists all currently active players

### 🎮 Number Guessing Mini-Game
- Users guess a number between **0 and 100**
- Game state is tracked and displayed in real time
- Integrated directly into the main interface

### 📁 Media Upload
- Users can **upload media files** directly through the interface
- Upload query is submitted to the backend via a dedicated form

---

## 🏗️ Architecture Overview

```
Client Browser
      │
      ▼
  NGINX (Reverse Proxy + SSL Termination)
      │
      ▼
  Flask App (Python Backend)   ←── Docker Container
      │
      ├── Authentication & Session Management
      ├── Chat / Message Scheduling API
      ├── Leaderboard Logic
      ├── Game State Management
      └── Media Upload Handler
```

---

## 🚀 Deployment

The application runs on a **DigitalOcean Linux Droplet** with the following setup:

1. **Docker & Docker Compose** — the Flask app and NGINX run as separate containers, orchestrated via `docker-compose.yml`
2. **NGINX** — acts as a reverse proxy, routing traffic to the Flask container and handling static file serving
3. **Let's Encrypt / Certbot** — provides free SSL certificates for HTTPS; auto-renews on the server
4. **Custom Domain** — registered using a free domain credit from the **GitHub Student Developer Pack**

### Running Locally

```bash
# Clone the repository
git clone https://github.com/The-interns-2-0/CSE-312-Project-group.git
cd CSE-312-Project-group

# Build and start the containers
docker-compose up --build
```

Visit `http://localhost` in your browser.

---


## 📁 Project Structure

```
CSE-312-Project-group/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── auth.py          # Login, signup, logout
│   │   ├── chat.py          # Message posting & scheduling
│   │   ├── game.py          # Number guessing game
│   │   └── leaderboard.py   # Rankings & player list
│   ├── templates/           # HTML templates (Frontend)
│   └── static/              # CSS, JS, images (Frontend)
├── nginx/
│   └── nginx.conf           # NGINX reverse proxy config
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## 🔒 Security

- Passwords are **hashed** before storage — plaintext passwords are never saved
- HTTPS enforced via **Let's Encrypt** SSL certificates
- Input validation and sanitization on all user-facing forms
- Content guidelines displayed to users in the chat interface

