# 📱 Termux Deployment Guide

**Deploying Obsidian-to-Hermes Integration on Android/Termux**

---

## 🎯 Overview

This guide shows how to deploy the entire system on your Xiaomi Redmi (obsidian_eea) using Termux.

**Hardware:**
- Xiaomi Redmi Note 14 Pro+ (obsidian_eea)
- 240GB storage
- Android 16
- Termux (rootless)

**Software:**
- Python 3.11+
- Ollama (local LLM)
- ChromaDB
- Telegram bot

---

## 📋 Prerequisites

### 1. Install Termux

1. Open F-Droid
2. Install Termux
3. Update packages:
   ```bash
   pkg update && pkg upgrade
   ```

### 2. Install Python

Termux comes with Python 3.11+, but let's verify:

```bash
python --version
# Should be Python 3.11 or higher
```

### 3. Install Ollama for Android

Ollama doesn't have native Android support, but we can:

**Option A: Use Termux's CPU-based inference**
- Install Python packages locally
- Use smaller model (llama3.2:3b)

**Option B: Use remote inference (recommended)**
- Use LarkBox PC for Ollama
- Connect via SSH from Termux

---

## 🚀 Quick Start (Termux)

### Step 1: Create Project Directory

```bash
cd ~
mkdir -p obsidian-brain/{scripts,unified-brain,chromadb,templates,source}
cd obsidian-brain
```

### Step 2: Copy Files

Copy all created files to Termux:

```bash
# From your downloads folder
cp /data/data/com.termux/files/home/downloads/* .
cp -r /data/data/com.termux/files/home/downloads/scripts .
cp -r /data/data/com.termux/files/home/downloads/templates .
```

### Step 3: Install Python Dependencies

```bash
pip install chromadb langchain-community langchain-ollama python-telegram-bot python-dotenv
```

If you get errors, install manually:

```bash
pkg install python python-pip
pip install --upgrade pip
pip install chromadb langchain-community langchain-ollama python-telegram-bot python-dotenv
```

### Step 4: Setup Ollama (Remote)

Connect to LarkBox PC:

```bash
# From Termux
ssh guiboratto@192.168.1.103

# On LarkBox PC, ensure Ollama is running
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

### Step 5: Configure Environment

Create `.env` file:

```bash
cat > .env << 'EOF'
TELEGRAM_BOT_TOKEN=your_bot_token_here
UNIFIED_VAULT_PATH=./unified-brain
CHROMA_PATH=./chromadb
OLLAMA_BASE_URL=http://192.168.1.103:11434
OLLAMA_MODEL=llama3.2
EOF
```

### Step 6: Setup ChromaDB

```bash
python scripts/setup-chromadb.py
```

### Step 7: Deploy Hermes Bot

```bash
python hermes_bot.py
```

### Step 8: Test

Send a message to your Telegram bot:
```
Що мені потрібно робити сьогодні?
```

---

## 🔧 Advanced Setup

### 1. Install Node.js (for import script)

```bash
pkg install nodejs
npm install -g node
```

### 2. Import Obsidian Vaults

If you have source vaults cloned:

```bash
# Clone source vaults
git clone https://github.com/lukeinglis/work-vault.git source/work-vault

# Import
node scripts/import-vaults.js
```

### 3. Run Orchestrator in Terminal

```bash
python scripts/orchestrator.py --interactive
```

### 4. Run Router Tests

```bash
python scripts/router.py
```

---

## 📱 Mobile-Friendly Improvements

### 1. Add Termux widget to launcher

1. Long-press on home screen
2. Select "Widgets"
3. Find "Termux"
4. Add widget

### 2. Create quick-launch script

```bash
# Create launch script
cat > ~/launch-hermes.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd ~/obsidian-brain
python hermes_bot.py
EOF

# Make executable
chmod +x ~/launch-hermes.sh
```

### 3. Add to Termux:Boot

Edit `~/.termux/termux-boot.sh`:

```bash
#!/data/data/com.termux/files/usr/bin/bash

# Start Ollama (if using local)
# ollama serve &

# Start Hermes bot (if using remote Ollama)
cd ~/obsidian-brain
python hermes_bot.py &
```

Then enable in Termux settings:
- Settings → Boot → Enable termux-boot

---

## ⚡ Performance Optimization

### 1. Use Smaller Embedding Model

```bash
# Pull smaller model
ollama pull llama3.2:3b

# Update .env
OLLAMA_MODEL=llama3.2:3b
```

### 2. Reduce ChromaDB Size

```bash
# Remove old backups
rm -rf chromadb.backup.*

# Rebuild ChromaDB
python scripts/setup-chromadb.py
```

### 3. Optimize Python

```bash
# Install PyPy for faster Python
pkg install pypy3
```

### 4. Enable Termux optimizations

```bash
# Enable fast file I/O
termux-setup-storage
```

---

## 🔒 Security & Privacy

### 1. Set permissions on .env

```bash
chmod 600 .env
```

### 2. Use SSH keys for remote Ollama

```bash
# Generate SSH key
ssh-keygen -t ed25519

# Copy to LarkBox
ssh-copy-id guiboratto@192.168.1.103

# Test connection
ssh guiboratto@192.168.1.103 "ollama list"
```

### 3. Use VPN for Telegram

If you're in a region with restrictions:

```bash
# Install VPN client
pkg install openvpn

# Configure VPN
# (your VPN provider's instructions)
```

---

## 🐛 Troubleshooting

### Python package installation fails

```bash
# Update pip
pip install --upgrade pip

# Install with build dependencies
pkg install python build
pip install --no-cache-dir chromadb langchain-community langchain-ollama
```

### ChromaDB can't connect to Ollama

```bash
# Test Ollama connection
curl http://192.168.1.103:11434/api/tags

# If fails, check firewall on LarkBox
sudo ufw allow 11434
```

### Telegram bot doesn't respond

```bash
# Check bot is running
ps aux | grep hermes_bot

# Check logs
pm2 logs hermes-bot

# Restart
pm2 restart hermes-bot
```

### Out of storage space

```bash
# Clean Termux cache
pkg clean

# Remove old backups
rm -rf ~/obsidian-brain/chromadb.backup.*

# Check storage usage
df -h
```

---

## 📊 Monitoring

### 1. Monitor bot uptime

```bash
pm2 status
```

### 2. Monitor memory usage

```bash
free -h
```

### 3. Monitor storage

```bash
du -sh ~/obsidian-brain
```

### 4. View logs

```bash
pm2 logs hermes-bot
```

---

## 🔄 Auto-Restart on Boot

### Using Termux:Boot

1. Install termux-boot app
2. Enable in Termux settings
3. Edit `~/.termux/termux-boot.sh`:
   ```bash
   #!/data/data/com.termux/files/usr/bin/bash
   cd ~/obsidian-brain
   python hermes_bot.py &
   ```
4. Restart phone
5. Bot should start automatically

### Using Systemd (requires root)

If you have root, you can use systemd:

```bash
# Create service file
cat > /data/data/com.termux/files/usr/share/systemd/user/hermes-bot.service << 'EOF'
[Unit]
Description=Hermes Telegram Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/data/data/com.termux/files/home/obsidian-brain
ExecStart=/data/data/com.termux/files/usr/bin/python hermes_bot.py
Restart=always

[Install]
WantedBy=default.target
EOF

# Enable service
systemctl --user enable hermes-bot
systemctl --user start hermes-bot
```

---

## 📝 Maintenance

### Daily

- Check bot logs: `pm2 logs hermes-bot`
- Monitor storage: `du -sh ~/obsidian-brain`

### Weekly

- Backup ChromaDB: `cp -r chromadb chromadb.backup.$(date +%Y%m%d)`
- Backup vault: `git add . && git commit -m "weekly"`

### Monthly

- Rebuild ChromaDB: `python scripts/setup-chromadb.py`
- Update dependencies: `pip install --upgrade chromadb langchain-community langchain-ollama`
- Check disk space

---

## 🎯 Success Indicators

✅ Bot responds within 3 seconds
✅ Bot uptime > 99%
✅ No storage errors
✅ Ollama responds to requests
✅ ChromaDB has > 1000 documents indexed
✅ Questions are answered from knowledge base

---

**Created:** 2026-09-25
**Target Device:** Xiaomi Redmi (obsidian_eea)
**Termux Version:** Latest
