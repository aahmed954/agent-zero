# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Essential Commands

### Development Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install browser binaries (required for browser agent)
playwright install chromium
```

### Running Agent Zero
```bash
# Main entry point - start web UI
python run_ui.py

# Run with specific port
python run_ui.py --port=5555

# Run tunnel server for remote access
python run_tunnel.py

# Initialize/preload models for performance
python initialize.py
python preload.py
```

### Docker Operations
```bash
# Pull and run official image
docker pull agent0ai/agent-zero
docker run -p 50001:80 agent0ai/agent-zero

# Build local development image
docker build -f DockerfileLocal -t agent-zero-local .
```

### Testing
```bash
# Run available tests
python tests/chunk_parser_test.py
python tests/rate_limiter_test.py
python tests/test_fasta2a_client.py

# Test components manually
python -m python.helpers.whisper    # Speech-to-text
python -m python.helpers.kokoro_tts # Text-to-speech
```

## Architecture Overview

Agent Zero is a dynamic, organic agentic framework built as a general-purpose personal assistant. The system is designed around these core principles:

### Multi-Agent Hierarchy
- **Superior-Subordinate Structure**: Every agent has a superior (human user for Agent 0) and can create subordinate agents for subtasks
- **Context Isolation**: Each agent maintains clean, focused context through delegation
- **Communication-Driven**: Real-time streaming with intervention capabilities

### Core Components Integration

**Agent System** (`agent.py`, `models.py`):
- LiteLLM-based model abstraction supporting multiple providers
- Hierarchical multi-agent coordination with persistent memory
- Dynamic context management and conversation state

**Tool Framework** (`python/tools/`):
- Auto-discovered tools with no single-purpose limitations
- Key tools: code execution, browser automation, memory management, search, subordinate delegation
- Tools create their own utilities as needed rather than using pre-programmed functions

**Extension System** (`python/extensions/`):
- Numbered execution order (`_NN_description.py` pattern)
- Hooks at critical points: agent_init, message_loop, tool_execute, response_stream, monologue
- Completely customizable behavior modification

**Memory Architecture** (`python/helpers/memory.py`):
- FAISS vector database for semantic retrieval
- AI consolidation when saving memories
- Persistent learning across sessions

**Web Interface** (`webui/`):
- Flask-based real-time streaming interface
- WebSocket communication for live interaction
- File browser, settings management, session logging

### Prompt-Driven Behavior
The entire framework is controlled by the `prompts/` directory:
- `agent.system.md` - Core system behavior (most important file)
- Tool-specific prompts for usage instructions
- Agent profiles in `agents/` for subordinate specialization
- No hard-coded rails or limitations

## Key Architectural Patterns

### Dynamic Tool Creation
- Agent writes and executes its own code rather than using fixed tools
- Default tools: search, memory, communication, code/terminal execution
- Everything else is created dynamically by the agent

### Safe Execution Environment
- Docker containers for code execution sandbox
- Configurable work directory (typically `tmp/`)
- Runtime isolation for dangerous operations

### Persistent Context
- Session logs saved as HTML in `logs/`
- Vector-based memory retrieval with embedding similarity
- Cross-session learning and solution reuse

## Development Guidelines

### File Organization
- **Tools**: Place in `python/tools/` with `*_tool.py` naming
- **Extensions**: Use `python/extensions/` with numbered prefixes for execution order
- **Prompts**: Modify behavior via `prompts/` directory templates
- **Agent Configs**: Subordinate agent profiles in `agents/`

### Extension Development
Extensions execute in numbered order and hook into:
1. Agent initialization
2. Message loop processing  
3. Tool execution
4. Response streaming
5. Internal monologue/reasoning

### Memory System Usage
- Agent automatically saves/loads memories
- AI consolidation prevents memory bloat
- Embedding-based retrieval for relevant context
- Memory located in `memory/` directory

### Configuration
- API keys and settings via web UI at `/settings`
- Environment variables in `.env` file
- Model providers configured through settings interface
- No traditional config files - everything through UI or prompts

## Important Notes

### No Traditional Linting/Formatting
Agent Zero does not use standard Python tooling like black, ruff, or mypy. Code quality is maintained through:
- Runtime error checking and Docker sandboxing
- Manual code review
- Extension-based validation hooks
- Dynamic behavior prioritized over static analysis

### Security Considerations
Agent Zero is designed to be powerful and potentially dangerous:
- Always run in isolated Docker environment
- Agent can execute arbitrary code and system commands
- Persistent memory means learned behaviors carry forward
- Real-time intervention capabilities are essential safety feature

### Customization Philosophy
Almost nothing is hard-coded - the framework is designed to be completely malleable through prompts and extensions rather than code changes.