# Real-Time Compliance Dashboard

React + TypeScript + Tailwind CSS frontend for the Real-Time Compliance monitoring system.

## Features

- 📊 **Dashboard Overview**: Real-time statistics, charts, and service summaries
- 📋 **Events List**: Browse and filter anomaly events
- 🔍 **Event Details**: View detailed information about specific events
- 🎨 **Modern UI**: Built with Tailwind CSS and responsive design
- 📈 **Charts**: Interactive charts using Recharts

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Routing
- **Axios** - HTTP client
- **Recharts** - Chart library
- **date-fns** - Date utilities
- **lucide-react** - Icons

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- FastAPI backend running on `http://localhost:8000`

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:3000`.

### Build

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Configuration

The API base URL can be configured via environment variable:

```bash
VITE_API_URL=http://localhost:8000 npm run dev
```

By default, it uses `http://localhost:8000` and the Vite dev server proxies `/api/*` requests to the backend.

## Project Structure

```
frontend/
├── src/
│   ├── api/           # API client
│   ├── components/    # Reusable components
│   ├── pages/         # Page components
│   ├── types/         # TypeScript types
│   ├── App.tsx        # Main app component
│   ├── main.tsx       # Entry point
│   └── index.css      # Global styles
├── public/            # Static assets
├── index.html         # HTML template
└── package.json       # Dependencies
```

## Available Routes

- `/` - Dashboard overview
- `/events` - Events list with filters
- `/events/:eventId` - Event detail page
