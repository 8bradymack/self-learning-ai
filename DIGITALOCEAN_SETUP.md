# DigitalOcean Cloud Deployment Guide

## After Creating Your Droplet

### Step 1: Connect to Your Server

Open Terminal on your Mac and run:

```bash
# Replace YOUR_IP with your Droplet's IP address
ssh root@YOUR_IP
```

Enter password when prompted (if you chose password authentication).

### Step 2: Install Dependencies

Once connected to your server, run these commands:

```bash
# Update system
apt update && apt upgrade -y

# Install Python and essential tools
apt install -y python3 python3-pip python3-venv git

# Create directory for AI
mkdir -p ~/ai
cd ~/ai
```

### Step 3: Clone Your Repository

```bash
# Clone your AI code from GitHub
git clone https://github.com/8bradymack/self-learning-ai.git
cd self-learning-ai
```

### Step 4: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 5: Add Your API Keys

```bash
# Create .env file
cat > .env << 'EOF'
GROQ_API_KEY=your_groq_key_here
HUGGINGFACE_TOKEN=your_huggingface_token_here
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
EOF

# Replace with your actual keys from the local .env file
# You can find them in your local repo
```

### Step 6: Download Your Knowledge Database

```bash
# Your knowledge backup is in GitHub
# It should already be in the cloned repo
cd data
tar -xzf ../knowledge_backup.tar.gz
cd ..
```

### Step 7: Start Web Dashboard

```bash
# Run web dashboard (accessible from anywhere!)
python scripts/web_dashboard.py --host 0.0.0.0 --port 5000
```

### Step 8: Access Your Dashboard

Open browser on ANY device:
```
http://YOUR_IP:5000
```

Replace YOUR_IP with your Droplet's IP address.

### Step 9: Run Continuous Learning (Optional)

Open a new SSH session (keep dashboard running in first one):

```bash
ssh root@YOUR_IP
cd ~/ai/self-learning-ai
source venv/bin/activate
python scripts/true_recursive_learning.py
```

Your AI will learn forever in the cloud!

### Step 10: Keep Processes Running (Advanced)

Use `screen` to keep processes running when you disconnect:

```bash
# Install screen
apt install -y screen

# Start a screen session for dashboard
screen -S dashboard
cd ~/ai/self-learning-ai
source venv/bin/activate
python scripts/web_dashboard.py --host 0.0.0.0 --port 5000
# Press Ctrl+A then D to detach

# Start another screen for learning
screen -S learning
cd ~/ai/self-learning-ai
source venv/bin/activate
python scripts/true_recursive_learning.py
# Press Ctrl+A then D to detach

# List screens
screen -ls

# Reattach to a screen
screen -r dashboard
```

## Troubleshooting

### Can't Connect to Dashboard?

Check firewall settings in DigitalOcean:
1. Go to your Droplet → Networking → Firewalls
2. Add inbound rule for TCP port 5000
3. Or disable firewall for testing: `ufw disable`

### Out of Memory?

Upgrade to larger Droplet:
- Go to Droplet → Resize
- Choose $18/month (4GB RAM) or $24/month (8GB RAM)

### Want HTTPS/Domain Name?

1. Buy domain (like myai.com) or use free subdomain
2. Point DNS to your Droplet IP
3. Install nginx: `apt install nginx`
4. Set up SSL with Let's Encrypt (free)

## Monitoring Your AI

### Check if processes are running:
```bash
ps aux | grep python
```

### View dashboard logs:
```bash
screen -r dashboard
```

### View learning logs:
```bash
screen -r learning
```

### Check disk space:
```bash
df -h
```

### Check knowledge count:
```bash
python -c "from src.memory.vector_store import VectorMemory; m = VectorMemory(); print(f'Knowledge: {m.collection.count():,}')"
```

## Your AI is Now:
- ✅ Running in the cloud 24/7
- ✅ Zero stress on your Mac
- ✅ Accessible from any device
- ✅ Learning continuously
- ✅ FREE for 16+ months!

## Backup Your Data

Periodically backup to GitHub:

```bash
cd ~/ai/self-learning-ai
git add .
git commit -m "Progress update - $(date)"
git push
```

Your knowledge database stays safe!
