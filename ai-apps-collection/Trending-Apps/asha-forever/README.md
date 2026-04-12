# 🎵 Asha Forever

**Asha Forever** is a beautiful, AI-powered tribute web application dedicated to the legendary Indian playback singer Asha Bhosle (1933–2026). 

The application utilizes Google's Gemini AI to dynamically generate curated Top 10 playlist cards based on a user's selected mood (Romantic, Sad/Nostalgic, Dance/Cabaret, Ghazal, or Devotional). It is designed with a dark, cinematic visual theme featuring warm gold and dusty rose accents to emulate a vintage Bollywood aesthetic.

## ✨ Features

- **Dynamic Curated Playlists**: Generates Top 10 Asha Bhosle songs in JSON format perfectly parsed from the Gemini 2.5 Flash model API.
- **Cinematic Aesthetics**: Stunning dark UI with interactive hover effects, animated `shimmer` typography, golden accents, and a faint film-grain noise overlay.
- **Direct YouTube Links**: Instantly builds smart YouTube search URLs allowing users to immediately listen to generated tracks.
- **Share Tributes**: Easily copy beautifully formatted plain-text tributes to the clipboard, or auto-generate a Draft Tweet on X (Twitter).
- **Client-Side Rendering**: A modern, single-page application built entirely in React/Vite without requiring a heavy backend.

## 🛠️ Tech Stack

- **Framework**: [React](https://reactjs.org/) + [Vite](https://vitejs.dev/)
- **Styling**: Vanilla Custom CSS + [Tailwind CSS v4](https://tailwindcss.com/)
- **AI Integration**: [Google Gemini Pro / Flash API](https://ai.google.dev/) (Client-side implementation)
- **Typography**: Google Fonts (*Playfair Display* & *DM Sans*)

## 🚀 Getting Started

### Prerequisites
- Node.js installed on your machine
- A [Google Gemini API Key](https://aistudio.google.com/app/apikey)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shubh-vedi/asha-forever.git
   cd asha-forever
   ```

2. **Install Dependencies:**
   ```bash
   npm install
   ```

3. **Run the Development Server:**
   ```bash
   npm run dev
   ```

4. **Access the App:** 
   Open your browser and navigate to `http://localhost:5173`. You will be prompted to enter your Gemini API key in the UI securely.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 🙏 Tribute 
Built as a tribute to Asha Bhosle ji (1933–2026). Her voice will live forever.

---
*Powered by Google Gemini*
