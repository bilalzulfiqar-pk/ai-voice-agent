# Auralis - AI Voice Agent

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![LiveKit](https://img.shields.io/badge/LiveKit_Agents-1.5-FF6B00?logo=livekit&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-16-000000?logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-06B6D4?logo=tailwindcss&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green?logo=open-source-initiative&logoColor=white)

Auralis is a browser-based realtime AI voice agent built with **LiveKit**, **Next.js**, and a **Python LiveKit agent worker**.

It is designed as a focused realtime voice-agent demo: a voice-native AI studio with live conversation, transcript rendering, turn detection, interruption handling, and a visible voice pipeline.

## Demo

![Auralis demo](assets/demo.gif)

## Features

- Browser-based voice conversation UI
- Realtime LiveKit session connection
- Python LiveKit agent worker
- Voice pipeline with:
  - BVC noise cancellation
  - Silero VAD
  - LiveKit multilingual turn detection
  - Deepgram STT through LiveKit Inference
  - OpenAI LLM through LiveKit Inference
  - Cartesia TTS through LiveKit Inference
  - preemptive generation
  - adaptive interruption handling
- Live transcript for user and agent messages
- Agent state display:
  - listening
  - thinking
  - speaking
  - reconnecting / failed states
- Voice controls:
  - start / end session
  - mute / unmute
  - auto mode
  - push-to-talk
  - text fallback
  - clear session
- Dark aurora UI with animated voice orb
- Collapsible system status and debug panels

## What Auralis Can Do

Auralis is intentionally conversational in the current version. It can answer questions, explain concepts, brainstorm ideas, help with writing, summarize content the user provides, and reason through coding or product ideas.

It does **not** currently browse the web, check live weather, set reminders, play music, book meetings, send email, access local files, or control external apps.

## Architecture

```text
Browser / Next.js
  -> requests a LiveKit token from /api/livekit/token
  -> joins a LiveKit room
  -> streams microphone audio
  -> plays agent audio
  -> renders transcript, state, controls, and pipeline status

LiveKit Cloud
  -> realtime media transport
  -> room/session orchestration
  -> transcript and text streams
  -> LiveKit Inference

Python Agent Worker
  -> VAD + turn detection
  -> STT -> LLM -> TTS voice pipeline
  -> interruption handling
  -> short in-session context
  -> publishes app.voice metadata to the frontend
```

## Project Structure

```text
.
+-- apps
|   +-- agent
|   |   +-- agent.py
|   |   +-- requirements.txt
|   |   +-- tests
|   |   +-- voice_agent
|   |       +-- agent_server.py
|   |       +-- config.py
|   |       +-- models.py
|   +-- web
|       +-- package.json
|       +-- public
|       +-- src
|           +-- app
|           +-- components
|           +-- lib
+-- package.json
+-- README.md
```

## Tech Stack

- **Frontend:** Next.js 16, React 19, TypeScript, Tailwind CSS 4
- **Voice transport:** LiveKit
- **Agent runtime:** LiveKit Agents for Python
- **STT:** `deepgram/flux-general-en`
- **LLM:** `openai/gpt-4.1-mini`
- **TTS:** `cartesia/sonic-3`
- **VAD:** Silero
- **Turn detection:** LiveKit multilingual turn detector

The default model stack uses **LiveKit Inference**, so you do not need separate OpenAI, Deepgram, or Cartesia API keys for the current setup. Usage still consumes LiveKit Cloud quota or billing credits.

## Prerequisites

- Node.js 18+
- Python 3.11+
- A LiveKit Cloud project
- LiveKit project credentials:
  - `LIVEKIT_URL`
  - `LIVEKIT_API_KEY`
  - `LIVEKIT_API_SECRET`

## Environment Setup

Create the frontend environment file:

```powershell
cd apps/web
Copy-Item .env.example .env.local
```

Create the agent environment file:

```powershell
cd ../agent
Copy-Item .env.example .env
```

Update both files with your LiveKit project values.

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

For lower-cost testing, you can set:

```env
AURALIS_LLM_MODEL=openai/gpt-4.1-nano
```

## Install And Run

Use two terminals: one for the agent worker and one for the web app.

### 1. Start the agent worker

```powershell
cd apps/agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python agent.py download-files
python agent.py dev
```

`download-files` downloads the local VAD and turn detection assets used by the LiveKit plugins.

### 2. Start the web app

```powershell
cd apps/web
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Useful Commands

From the repository root:

```powershell
npm run lint:web
npm run typecheck:web
npm run build:web
```

From `apps/agent`:

```powershell
.\.venv\Scripts\python -m unittest discover -s tests -v
```

## Manual Test Checklist

After starting both the agent and web app:

- Open the app and click **Start conversation**
- Allow microphone permission
- Confirm the agent greets you
- Ask a short question and verify:
  - user transcript appears
  - agent transcript appears
  - agent state changes between listening / thinking / speaking
  - audio playback works
- Try interrupting the agent while it is speaking
- Test mute / unmute
- Test push-to-talk mode
- Test text fallback
- End the session and start a new one
- Open the system status and debug panels

## Notes About Logs

Some LiveKit development logs are expected:

- `closing agent session due to participant disconnect` appears when the browser leaves the room.
- Adaptive interruption can occasionally fall back to VAD-based interruption if the cloud interruption inference request times out.

## Scope

Auralis focuses on realtime voice conversation rather than external tool automation.

This version is intentionally scoped to voice chat, transcript rendering, turn detection, interruptions, and session controls. Features like long-term memory, web browsing, calendar actions, telephony, RAG, latency analytics, and multi-agent workflows are outside the current scope.

## References

- [LiveKit Agents](https://docs.livekit.io/agents/)
- [LiveKit Agent Sessions](https://docs.livekit.io/agents/logic/sessions/)
- [LiveKit Turns](https://docs.livekit.io/agents/logic/turns/)
- [LiveKit Frontend Sessions](https://docs.livekit.io/frontends/build/sessions/)
- [LiveKit Voice Agent Workshop](https://worksh.app/tutorials/livekit-voice-agent/introduction)
