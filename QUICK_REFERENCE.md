# Quick Reference Card

## Installation
```bash
cd ~/self-learning-ai
./setup.sh
cp .env.example .env
# Edit .env and add API keys
```

## Running the System

### Interactive Mode
```bash
source venv/bin/activate
python main.py --mode interactive
```

### Learning Mode
```bash
python main.py --mode learn --iterations 10
```

### Self-Modification Mode
```bash
python main.py --mode modify
```

## Interactive Commands

| Command | Description |
|---------|-------------|
| `learn <n>` | Run n learning iterations |
| `ask <question>` | Ask the AI a question |
| `search <query>` | Search knowledge base |
| `stats` | Show statistics |
| `modify <goal>` | Propose modification |
| `help` | Show help |
| `exit` | Quit |

## Common Tasks

### Export Training Data
```bash
python scripts/export_training_data.py
```

### Check Knowledge Stats
```python
from src.memory.vector_store import VectorMemory
memory = VectorMemory()
print(memory.get_stats())
```

### View Logs
```bash
cat data/logs/learning_history.json
cat data/logs/modification_history.json
```

### Backup Knowledge
```bash
cp -r data/knowledge data/knowledge_backup_$(date +%Y%m%d)
```

## API Keys

Get free keys from:
- **Groq**: https://console.groq.com
- **HuggingFace**: https://huggingface.co/settings/tokens
- **OpenAI** (optional): https://platform.openai.com

Add to `.env`:
```
GROQ_API_KEY=your_key_here
HUGGINGFACE_TOKEN=your_token_here
```

## File Locations

- **Config**: `configs/config.yaml`
- **Models**: `data/models/`
- **Knowledge**: `data/knowledge/`
- **Logs**: `data/logs/`
- **Backups**: `data/backups/`

## Cloud Training

1. Export data: `python scripts/export_training_data.py`
2. Upload to Colab: https://colab.research.google.com
3. Open `notebooks/cloud_training.ipynb`
4. Run training cells
5. Download trained model
6. Extract to `data/models/`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No API clients | Add keys to `.env` |
| Model not found | Will download on first run |
| Out of memory | Use smaller model in config |
| Rate limit | Wait, or use different API |

## Configuration

Edit `configs/config.yaml`:

```yaml
# Change model
model:
  base_model: "meta-llama/Llama-3.2-3B"

# Adjust learning
learning:
  learning_rate: 2e-4
  batch_size: 4

# Enable/disable features
self_modification:
  enabled: true
  human_approval_required: false
```

## Safety

- All modifications create backups in `data/backups/`
- Rollback: `python -c "from src.safety.self_modifier import SelfModifier; SelfModifier().rollback_to_backup('backup_TIMESTAMP')"`
- Dangerous code is blocked automatically
- Sandboxed testing before applying changes

## Performance Tips

1. Use Groq API (fastest free option)
2. Train on Colab/Kaggle, not Mac
3. Start with 3B model, upgrade later
4. Regular backups of knowledge
5. Monitor free tier limits

## Quick Start

```bash
cd ~/self-learning-ai
./setup.sh
source venv/bin/activate
python main.py --mode interactive
```

Then: `learn 5`

## Documentation

- Full docs: `README.md`
- Getting started: `GETTING_STARTED.md`
- Summary: `PROJECT_SUMMARY.md`
- This card: `QUICK_REFERENCE.md`

---

**Keep this file handy for quick lookups!**
