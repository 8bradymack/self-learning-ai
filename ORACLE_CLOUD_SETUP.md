# Oracle Cloud Always Free Setup - Your AI Forever!

## Why Oracle Cloud?
- **FREE FOREVER** - Not credits, truly free
- **4 ARM CPUs** + **24GB RAM** + **200GB storage**
- **No time limits** - Run your AI 24/7 forever
- **Better than Student Pack** - More powerful than $100 Azure credit

---

## Step 1: Create Oracle Cloud Account (5 minutes)

1. **Go to:** https://www.oracle.com/cloud/free/
2. **Click "Start for free"**
3. **Sign up with email** (they ask for credit card but WON'T charge for Always Free tier)
4. **Choose "Home Region"** - Pick closest to you (can't change later!)
5. **Verify email and complete signup**

Wait for account approval (usually instant, sometimes takes 1 hour).

---

## Step 2: Create Your Free VM (10 minutes)

Once logged into Oracle Cloud Console:

### Create the VM

1. **Click "Create a VM instance"** (or hamburger menu → Compute → Instances → Create Instance)

2. **Name:** `my-ai-server`

3. **Placement:** Leave default

4. **Image and Shape:**
   - Click **"Change Shape"**
   - Select **"Ampere"** (ARM-based)
   - Choose **"VM.Standard.A1.Flex"**
   - Set **4 OCPUs** and **24GB memory** (this is FREE!)
   - Click "Select Shape"

5. **Image:**
   - Click **"Change Image"**
   - Select **"Ubuntu"** → **"22.04"**
   - Click "Select Image"

6. **Networking:**
   - Leave "Create new virtual cloud network" selected
   - Check **"Assign a public IPv4 address"**

7. **Add SSH Keys:**
   - Select **"Generate SSH key pair"**
   - Click **"Save Private Key"** (downloads a .key file)
   - Click **"Save Public Key"** (optional)
   - **IMPORTANT:** Save the private key - you'll need it to connect!

8. **Boot Volume:** Leave defaults (200GB is free!)

9. **Click "Create"**

Wait 2-3 minutes for the VM to provision.

---

## Step 3: Configure Firewall

### In Oracle Cloud Console:

1. **On your instance page, under "Instance Details":**
   - Click on the **VCN (Virtual Cloud Network)** name

2. **Click "Security Lists"** on left sidebar

3. **Click the default security list**

4. **Click "Add Ingress Rules":**
   - **Source CIDR:** `0.0.0.0/0`
   - **Destination Port Range:** `5000`
   - **Description:** `Web Dashboard`
   - Click **"Add Ingress Rules"**

5. **Repeat for SSH (if not already there):**
   - **Source CIDR:** `0.0.0.0/0`
   - **Destination Port Range:** `22`
   - **Description:** `SSH`
   - Click **"Add Ingress Rules"**

### On the VM itself (you'll do this after connecting):

```bash
# Open firewall for web dashboard
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 5000 -j ACCEPT
sudo netfilter-persistent save
```

---

## Step 4: Connect to Your VM

### Find Your IP Address:
- On the instance details page, copy the **Public IP address**

### Connect from your Mac:

```bash
# Move the downloaded key to .ssh folder
mv ~/Downloads/ssh-key-*.key ~/.ssh/oracle-ai.key
chmod 400 ~/.ssh/oracle-ai.key

# Connect to your server (replace YOUR_IP with the actual IP)
ssh -i ~/.ssh/oracle-ai.key ubuntu@YOUR_IP
```

**You're now in your cloud server!**

---

## Step 5: Install Everything

Run these commands on your Oracle Cloud VM:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and tools
sudo apt install -y python3 python3-pip python3-venv git iptables-persistent

# Clone your AI from GitHub
cd ~
git clone https://github.com/8bradymack/self-learning-ai.git
cd self-learning-ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (this takes 5-10 minutes)
pip install -r requirements.txt
```

---

## Step 6: Add Your API Keys

```bash
# Still in ~/self-learning-ai directory
cat > .env << 'EOF'
GROQ_API_KEY=your_groq_key_here
HUGGINGFACE_TOKEN=your_huggingface_token_here
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
EOF

# Edit with your actual keys
nano .env
# Paste your keys, then Ctrl+X, Y, Enter to save
```

---

## Step 7: Restore Your Knowledge Database

```bash
# Your knowledge backup is in the repo
cd ~/self-learning-ai
tar -xzf knowledge_backup.tar.gz
echo "Knowledge database restored!"
```

---

## Step 8: Configure Firewall (on VM)

```bash
# Open port 5000 for web dashboard
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 5000 -j ACCEPT
sudo netfilter-persistent save
```

---

## Step 9: Start Your AI!

### Option A: Run Web Dashboard

```bash
cd ~/self-learning-ai
source venv/bin/activate
python scripts/web_dashboard.py --host 0.0.0.0 --port 5000
```

Then open in browser: `http://YOUR_IP:5000`

### Option B: Keep It Running Forever

Use `screen` so it keeps running when you close terminal:

```bash
# Install screen
sudo apt install -y screen

# Start dashboard in a screen session
screen -S dashboard
cd ~/self-learning-ai
source venv/bin/activate
python scripts/web_dashboard.py --host 0.0.0.0 --port 5000
```

Press **Ctrl+A** then **D** to detach (keeps running in background)

```bash
# Start learning in another screen
screen -S learning
cd ~/self-learning-ai
source venv/bin/activate
python scripts/true_recursive_learning.py
```

Press **Ctrl+A** then **D** to detach

**Now you can close terminal and your AI keeps running!**

### Reattach to screens later:

```bash
screen -ls              # List screens
screen -r dashboard     # Reattach to dashboard
screen -r learning      # Reattach to learning
```

---

## Step 10: Access Your AI From Anywhere!

Open browser on ANY device (Mac, phone, tablet):

```
http://YOUR_IP:5000
```

You'll see:
- Real-time knowledge count
- Chat with your AI
- Learning activity
- All your 13,000+ knowledge items working!

---

## Monitoring & Maintenance

### Check if everything is running:
```bash
ssh -i ~/.ssh/oracle-ai.key ubuntu@YOUR_IP
screen -ls
```

### View dashboard:
```bash
screen -r dashboard
```

### View learning progress:
```bash
screen -r learning
```

### Check disk space:
```bash
df -h
```

### Backup to GitHub periodically:
```bash
cd ~/self-learning-ai
git add data/
git commit -m "Backup - $(date)"
git push
```

### Check knowledge count:
```bash
cd ~/self-learning-ai
source venv/bin/activate
python -c "from src.memory.vector_store import VectorMemory; m = VectorMemory(); print(f'Knowledge: {m.collection.count():,}')"
```

---

## Troubleshooting

### Can't connect to IP:5000?
```bash
# Check firewall on VM
sudo iptables -L -n | grep 5000

# If not there, add it:
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 5000 -j ACCEPT
sudo netfilter-persistent save
```

### Out of disk space?
```bash
# Check usage
df -h

# Clean up if needed
sudo apt clean
sudo apt autoremove
```

### Want to add a domain name?
1. Buy domain (like myai.com) from Namecheap (~$10/year)
2. Point A record to your VM's IP
3. Access at http://myai.com:5000
4. Optional: Set up nginx + SSL for https://myai.com

---

## Your AI is Now:
✅ **Running in cloud 24/7**
✅ **FREE FOREVER** (Oracle Always Free tier)
✅ **4 CPUs, 24GB RAM, 200GB storage**
✅ **Accessible from any device**
✅ **Zero stress on your Mac**
✅ **Learning continuously**

---

## Cost Breakdown:
- **Oracle Cloud VM:** $0/month (always free)
- **Total:** **$0/month FOREVER**

This is better than:
- GitHub Codespaces: 60 hrs/month limit
- DigitalOcean: $200 credit runs out
- Azure: $100 credit runs out
- **Oracle:** FREE FOREVER with great specs!

---

## Next Steps:

1. **Set it and forget it** - Your AI runs 24/7
2. **Check from phone** - Open http://YOUR_IP:5000 anytime
3. **Watch it get smarter** - Knowledge grows every day
4. **Chat with it** - Ask questions using its 13K+ knowledge
5. **Backup to GitHub** - Keep your progress safe

**You now have a truly free, powerful AI running forever in the cloud!**
