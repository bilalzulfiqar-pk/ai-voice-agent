# ai-voice-agent / Auralis

Auralis is a browser-based realtime AI voice agent built with LiveKit, Next.js, and a Python LiveKit worker.

The app is centered on open-ended conversation, live transcript rendering, agent state, interruptions, and visible voice-pipeline status.

## What It Does

- Connects the browser to a LiveKit session
- Captures microphone audio and plays agent audio back in realtime
- Runs a LiveKit voice pipeline with:
  - BVC noise cancellation
  - Silero VAD
  - Deepgram STT
  - OpenAI LLM
  - Cartesia TTS
  - LiveKit multilingual turn detection
  - preemptive generation
  - adaptive interruption handling
- Shows:
  - listening / thinking / speaking states
  - live user and agent transcript
  - partial transcript updates
  - interrupted assistant speech markers
  - a pipeline status rail
- Supports:
  - auto mode
  - push-to-talk mode
  - mute / unmute
  - typed fallback messages
  - clear session reset
  - debug drawer

## Architecture

```text
Browser (Next.js)
  -> POST /api/livekit/token
  -> joins LiveKit room with Session API
  -> streams mic audio and renders transcript/state

LiveKit
  -> room transport
  -> turn handling
  -> text + transcript streams
  -> interruption-aware voice session plumbing

Python Agent Worker
  -> STT: deepgram/flux-general-en
  -> LLM: openai/gpt-4.1-mini
  -> TTS: cartesia/sonic-3
  -> VAD: Silero
  -> turn detector: MultilingualModel
  -> publishes app.voice metadata to the frontend
```

## Frontend Shape

The web app uses a dark aurora design with:

- premium header
- central animated voice orb
- live transcript panel
- control deck
- pipeline rail
- collapsible debug drawer

The main UI entrypoint is [voice-agent-app.tsx](/C:/Villaex%20Technologies/FastAPI/ai-voice-agent/apps/web/src/components/voice-agent-app.tsx).

## Backend Shape

The Python worker now lives in [apps/agent/voice_agent](/C:/Villaex%20Technologies/FastAPI/ai-voice-agent/apps/agent/voice_agent).

Key files:

- [agent_server.py](/C:/Villaex%20Technologies/FastAPI/ai-voice-agent/apps/agent/voice_agent/agent_server.py)
- [config.py](/C:/Villaex%20Technologies/FastAPI/ai-voice-agent/apps/agent/voice_agent/config.py)
- [models.py](/C:/Villaex%20Technologies/FastAPI/ai-voice-agent/apps/agent/voice_agent/models.py)

Frontend metadata contract:

- `app.voice.capabilities`
- `app.voice.session`

## Local Setup

### 1. Web app

```powershell
cd "C:\Villaex Technologies\FastAPI\ai-voice-agent\apps\web"
Copy-Item .env.example .env.local
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

### 2. Agent worker

If this repository was copied from the older project, rebuild the virtual environment instead of trusting the copied `.venv`.

```powershell
cd "C:\Villaex Technologies\FastAPI\ai-voice-agent\apps\agent"
Remove-Item -LiteralPath .venv -Recurse -Force
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python agent.py dev
```

Python 3.11+ is the target for this setup.

## Environment Variables

### `apps/web/.env.local`

```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
NEXT_PUBLIC_LIVEKIT_URL=wss://your-project.livekit.cloud
NEXT_PUBLIC_LIVEKIT_AGENT_NAME=auralis-agent
```

### `apps/agent/.env`

```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
LIVEKIT_AGENT_NAME=auralis-agent
AURALIS_STT_MODEL=deepgram/flux-general-en
AURALIS_LLM_MODEL=openai/gpt-4.1-mini
AURALIS_TTS_MODEL=cartesia/sonic-3
AURALIS_TTS_VOICE=9626c31c-bec5-4cca-baa8-f8ba9e84c8bc
```

## Scripts

From the repo root:

```powershell
npm run lint:web
npm run typecheck:web
npm run build:web
```

From [apps/agent](/C:/Villaex%20Technologies/FastAPI/ai-voice-agent/apps/agent):

```powershell
python -m unittest discover -s tests -v
```

## Tests Included

- web lint
- web typecheck
- web production build
- agent config serialization tests
- agent metadata payload tests

## Scope Notes

This MVP intentionally does not include:

- long-term memory
- database persistence
- calendar workflows
- CRM integrations
- auth
- telephony
- multi-agent orchestration
- RAG

## References

- [LiveKit agent sessions](https://docs.livekit.io/agents/logic/sessions/)
- [LiveKit turns](https://docs.livekit.io/agents/logic/turns/)
- [LiveKit frontend sessions](https://docs.livekit.io/frontends/build/sessions/)
- [LiveKit voice-agent workshop](https://worksh.app/tutorials/livekit-voice-agent/introduction)
