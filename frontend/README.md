# Frontend — React + Vite App

The frontend is a React application built with Vite. It renders the simulation UI, handles click detection on screenshots, and communicates with the FastAPI backend.

---

## Requirements

- Node.js 18+
- npm

---

## Setup

**1. Install dependencies**
```bash
npm install
```

**2. Start the dev server**
```bash
npm run dev
```

The app runs at `http://localhost:5173`.

> The backend must also be running at `http://localhost:8000` for the simulation to load.

---

## Build for Production

```bash
npm run build
```

Output goes to `dist/`. Deploy this folder as a static site (e.g. Render Static Site, Netlify, Vercel).

---

## File Structure

```
frontend/
├── src/
│   ├── App.jsx                  # Root component — routing between screens
│   ├── App.css                  # Global layout + shared styles
│   ├── index.css                # CSS variables (light/dark theme tokens)
│   └── components/
│       ├── Sidebar.jsx          # Collapsible sidebar with sim selector
│       ├── SimulationStep.jsx   # Screenshot + hotspot click handler
│       ├── EndScreen.jsx        # Completion screen
│       ├── ChatBar.jsx          # Ask a question input bar
│       └── SettingsMenu.jsx     # Theme toggle dropdown (⚙)
├── images/                      # Logo and brand images
├── public/                      # Static assets (favicon)
└── index.html
```

---

## Theme System

Light / Dark / System themes are controlled via CSS variables in `src/index.css`. The active theme is set as a `data-theme` attribute on `<html>`. Toggle it using the ⚙ settings menu in the top-right of the header.

---

## Backend Connection

The API base URL is set at the top of `src/components/SimulationStep.jsx`:

```js
const API = "http://localhost:8000";
```

Update this value when deploying to production.
