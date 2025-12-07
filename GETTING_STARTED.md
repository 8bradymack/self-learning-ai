# Getting Started with Self-Learning AI

## Overview

You've just created a self-learning AI system that can:
- ✓ Learn from other AIs via APIs
- ✓ Store knowledge in a vector database
- ✓ Continuously improve over time
- ✓ Modify its own code (with safety constraints)
- ✓ Run training on cloud GPUs for free

## Quick Start

### 1. Install Dependencies

```bash
cd ~/self-learning-ai
./setup.sh
```

This will:
- Create a Python virtual environment
- Install all required packages
- Set up the project structure

### 2. Configure API Keys

```bash
cp .env.example .env
nano .env  # or use your preferred editor
```

Get free API keys:
- **Groq** (recommended - fast & free): https://console.groq.com
- **HuggingFace**: https://huggingface.co/settings/tokens
- **OpenAI** (optional): https://platform.openai.com

Add them to `.env`:
```
GROQ_API_KEY=your_key_here
HUGGINGFACE_TOKEN=your_token_here
```

### 3. Run Your First Learning Cycle

```bash
source venv/bin/activate
python main.py --mode learn --iterations 3
```

This will:
- Query AI APIs with questions
- Store learned knowledge in the vector database
- Show progress and statistics

### 4. Try Interactive Mode

```bash
python main.py --mode interactive
```

Commands:
- `learn 5` - Run 5 learning iterations
- `ask <question>` - Ask the AI something
- `search <query>` - Search the knowledge base
- `stats` - Show statistics
- `modify <goal>` - Propose a self-modification
- `exit` - Quit

## Architecture

```
Your M3 Mac (Control Center)
├── Base Model (Llama 3.2 3B)
├── Vector Memory (ChromaDB)
│   └── Stores all learned knowledge
├── Learning Loop
│   ├── Queries AI APIs
│   ├── Learns from responses
│   └── Stores in memory
├── Self-Modifier
│   ├── Generates code improvements
│   ├── Tests modifications safely
│   └── Creates backups
└── Cloud GPU Integration
    └── Sends training to Colab/Kaggle
```

## Learning Process

### Phase 1: Learn from AIs
The system asks questions to external AI APIs:
- Groq (Llama 70B)
- HuggingFace models
- OpenAI GPT (if configured)

Responses are stored in the vector database.

### Phase 2: Generate Training Data
Knowledge from memory is converted into training examples:
- Question-answer pairs
- Formatted for fine-tuning
- Exported to JSON

### Phase 3: Cloud Training
1. Export training data: `python scripts/export_training_data.py`
2. Upload to Google Colab
3. Open `notebooks/cloud_training.ipynb`
4. Run training on free GPU
5. Download improved model
6. Load on your Mac

### Phase 4: Self-Modification
The AI can propose improvements to its own code:
- Analyzes performance
- Generates code modifications
- Tests in sandbox
- Applies if safe and beneficial

## Cloud GPU Training

### Google Colab (Free)
1. Go to https://colab.research.google.com
2. Upload `notebooks/cloud_training.ipynb`
3. Upload your training data
4. Run cells sequentially
5. Download trained model
6. Extract to `data/models/`

**Free tier:** ~15-20 GPU hours/week

### Kaggle (Free)
1. Go to https://kaggle.com
2. Create new notebook
3. Enable GPU accelerator
4. Upload training code
5. Run training
6. Download results

**Free tier:** ~30 GPU hours/week

## Self-Modification

The AI can modify its own code with these safety constraints:

**Allowed modifications:**
- Learning hyperparameters
- Training strategies
- Data collection methods
- Question generation

**Forbidden modifications:**
- Safety constraints
- Evaluation metrics
- Core safety systems

**Safety features:**
- Automatic backups before changes
- Code safety analysis
- Sandboxed testing
- Rollback capability
- Optional human approval

### Try it:
```bash
python main.py --mode modify
```

Or in interactive mode:
```
modify Improve the learning rate for faster training
```

## Monitoring Progress

### Knowledge Base Stats
```python
from src.memory.vector_store import VectorMemory

memory = VectorMemory()
stats = memory.get_stats()
print(stats)
```

### Learning History
Check `data/logs/learning_history.json` for:
- Number of items learned per cycle
- Evaluation scores
- Timestamps

### Modification History
Check `data/logs/modification_history.json` for:
- Proposed modifications
- Success/failure status
- Backup locations

## Tips for Best Results

### 1. Start Small
- Run 1-3 learning iterations first
- Check that APIs are working
- Verify knowledge is being stored

### 2. Use Cloud GPUs
- Your M3 Mac is great for orchestration
- But use Colab/Kaggle for actual training
- Much faster and free!

### 3. Monitor Knowledge Quality
Search the knowledge base to see what it's learning:
```
search machine learning
```

### 4. Regular Backups
Self-modifications create automatic backups, but you can also:
```bash
cp -r data/knowledge data/knowledge_backup_$(date +%Y%m%d)
```

### 5. Incremental Improvements
Don't expect overnight superintelligence. Look for:
- Better answers to specific questions
- Broader knowledge coverage
- Improved reasoning in narrow domains

## Troubleshooting

### "No API clients initialized"
- Check your `.env` file has API keys
- Verify keys are valid
- Try `source .env` in terminal

### "Model loading failed"
- Ensure you have 16GB RAM
- Check internet connection (downloads model)
- Try smaller model in `configs/config.yaml`

### "CUDA not available" (on Colab)
- Go to Runtime → Change runtime type
- Select GPU
- Restart runtime

### Training is slow
- Use cloud GPUs (Colab/Kaggle)
- Reduce batch size in config
- Use smaller model

## What's Next?

### Short Term (Days-Weeks)
- Accumulate knowledge from APIs
- Build up vector database
- Try first cloud training run
- Test self-modifications

### Medium Term (Weeks-Months)
- Regular training cycles
- Specialized knowledge in domains
- Optimized learning strategies
- Better question generation

### Long Term (Months+)
- Highly specialized capabilities
- Multi-modal learning (images, video)
- Advanced self-improvement
- Novel combinations of knowledge

## Realistic Expectations

**Will achieve:**
- Continual learning and improvement
- Personalized knowledge base
- Specialized expertise in focus areas
- Working self-modification system

**Won't achieve:**
- Surpassing GPT-4/Claude in general capability
- Superintelligence
- Novel fundamental insights
- Revolutionary AI breakthrough

**But it will be:**
- A real, working learning system
- Educational and fun
- Genuinely useful
- Yours to control and customize

## Need Help?

- Check `README.md` for architecture details
- Review code comments in `src/`
- Examine `configs/config.yaml` for settings
- Look at logs in `data/logs/`

## Have Fun!

You've built something genuinely interesting. Watch it learn and grow!

Start with:
```bash
source venv/bin/activate
python main.py --mode interactive
```

Then type:
```
learn 5
```

And watch it begin to learn!
