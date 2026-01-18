# AutoVideo - YouTube Faceless Video Generator

Automatically generate faceless YouTube videos with AI-powered scripts, voiceovers, stock footage, and SEO-optimized metadata.

## Features

- AI-generated scripts using Groq, Gemini, or Ollama
- Human-like script writing (avoids AI detection)
- Psychology-based engagement hooks
- Text-to-speech voiceover with edge-tts
- Sentence-grouped stock footage matching
- Auto-generated subtitles (SRT file)
- SEO-optimized metadata (titles, descriptions, tags)
- Thumbnail generation
- Google Trends topic suggestions
- One-click video generation

## Requirements

- Python 3.8+
- Windows, Linux, or macOS
- Internet connection (for AI APIs and stock footage)

## Quick Start

### Windows

1. Double-click `GENERATE_VIDEO.bat`
2. The script will automatically:
   - Create a virtual environment
   - Install all dependencies
   - Set up API keys
3. Follow the menu prompts to generate your video

### Linux/macOS

```bash
chmod +x generate_video.sh
./generate_video.sh
```

## API Keys

The tool uses these free APIs (keys are pre-configured):

| Service | Purpose | Get Your Own Key |
|---------|---------|------------------|
| Groq | AI script generation | https://console.groq.com/keys |
| Gemini | AI script generation (fallback) | https://aistudio.google.com/app/apikey |
| Pexels | Stock video footage | https://www.pexels.com/api/ |
| Pixabay | Stock video footage (fallback) | https://pixabay.com/api/docs/ |

To use your own keys, edit the `.env` file:

```
GROQ_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
PEXELS_API_KEY=your_key_here
PIXABAY_API_KEY=your_key_here
```

## Usage Options

### Option 1: Interactive Menu (Recommended)

Run `GENERATE_VIDEO.bat` (Windows) or `./generate_video.sh` (Linux/Mac) and choose from:

1. **Generate Video** - Create a new video
2. **Show Trending Topics** - Get monetization-focused topic ideas
3. **Interactive Mode** - Step-by-step guided generation
4. **Help** - Show all options
5. **Exit**

### Option 2: Command Line

```bash
# Basic usage
python autovideo.py --topic "5 AI Tools for Productivity" --length 8

# With specific AI provider
python autovideo.py --topic "Investment Tips" --length 10 --ai groq

# Show trending topics
python autovideo.py --suggest-topics

# Interactive mode
python autovideo.py --interactive
```

### Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--topic` | `-t` | Video topic | Required |
| `--length` | `-l` | Video length in minutes | 8 |
| `--ai` | | AI provider (auto/groq/gemini/ollama) | auto |
| `--keywords` | `-k` | Custom footage keywords | Auto-generated |
| `--project` | `-p` | Project name | Auto-generated |
| `--suggest-topics` | | Show trending topics | - |
| `--interactive` | `-i` | Interactive mode | - |

## Output Files

After generation, find your files in `projects/video_YYYYMMDD_HHMMSS/`:

```
projects/
  video_20260118_143000/
    output/
      final_video.mp4      # Your video (upload this)
      subtitles.srt        # Subtitle file
    footage/               # Downloaded stock clips
    voiceover/
      voiceover.mp3        # Audio narration
    thumbnail/
      thumbnail.png        # Video thumbnail
    metadata/
      metadata.json        # SEO data (titles, tags, description)
    script/
      script.txt           # Generated script
```

---

# YouTube Upload Guide

## Step 1: Prepare Your Files

After running the tool, gather these files from your project folder:

1. `output/final_video.mp4` - Your video
2. `thumbnail/thumbnail.png` - Thumbnail image
3. `metadata/metadata.json` - SEO data
4. `output/subtitles.srt` - Subtitles (optional)

## Step 2: Upload to YouTube

1. Go to [YouTube Studio](https://studio.youtube.com)
2. Click **Create** (top right) > **Upload videos**
3. Select your `final_video.mp4` file
4. While uploading, fill in the details (see Step 3)

## Step 3: Add Video Details

### Title
Open `metadata.json` and copy one of the titles from the `titles` array. The `recommended_title` is optimized for SEO.

**Tips:**
- Keep under 60 characters
- Put main keyword at the beginning
- Use numbers when possible (e.g., "5 Tips", "2024 Guide")

### Description
Copy the `description` from `metadata.json`. Then:

1. **Update timestamps** - Watch your video and add accurate timestamps
2. **Add related video links** - Link to your other videos
3. **Add affiliate links** (if applicable)

**First 150 characters are crucial** - they show in search results!

### Tags
Copy all tags from the `tags` array in `metadata.json`. Paste them comma-separated in YouTube's tag field.

### Thumbnail
1. Click **Upload thumbnail**
2. Select `thumbnail/thumbnail.png`
3. Or create a custom thumbnail using Canva (recommended for higher CTR)

### Subtitles/CC
1. Go to **Subtitles** tab
2. Click **Add** > **Upload file**
3. Select `subtitles.srt`
4. Choose **With timing**

## Step 4: Visibility Settings

1. **Visibility**: Choose "Public" for immediate publishing
2. **Schedule**: Or schedule for optimal time (Tuesday-Thursday, 2-4 PM EST)
3. **Premiere**: Consider premiering for engagement boost

## Step 5: Additional Settings

### Playlists
Add to relevant playlists to increase watch time.

### End Screen
Add end screen elements (subscribe button, related videos) in the last 20 seconds.

### Cards
Add info cards linking to related videos or playlists.

---

# SEO Optimization Guide

## Title Optimization

**Do:**
- Include main keyword in first 3 words
- Use power words: "Ultimate", "Complete", "Secret", "Proven"
- Add year for freshness: "(2024)"
- Use numbers: "7 Ways", "Top 10"

**Don't:**
- Exceed 60 characters (gets cut off)
- Use clickbait that doesn't deliver
- Stuff keywords unnaturally

**Examples:**
- "Passive Income 2024: 7 Proven Ways to Make Money While You Sleep"
- "How to Invest in Stocks for Beginners (Complete Guide)"

## Description Optimization

**Structure:**
```
[Hook - First 150 characters with main keyword]

[Detailed explanation - 200-300 words]

[Timestamps]

[Call to action - Subscribe, Like, Comment]

[Related links]

[Hashtags - 3-5 relevant ones]
```

**Tips:**
- Front-load keywords in first 2 sentences
- Include 2-3 keyword variations naturally
- Add timestamps (improves watch time)
- Use hashtags (max 15, but 3-5 is optimal)

## Tag Strategy

**Priority order:**
1. Exact match keyword (your topic)
2. Broad match variations
3. Related topics
4. Channel-specific tags

**Example for "Passive Income":**
```
passive income, passive income ideas, passive income 2024, 
how to make passive income, passive income for beginners,
make money online, side hustle, financial freedom,
investing, money tips
```

## Thumbnail Best Practices

**Design tips:**
- Use bright, contrasting colors (yellow, red, blue)
- Add large, readable text (3-5 words max)
- Include a face with expression (if possible)
- Use 1280x720 resolution
- Keep file under 2MB

**Tools:**
- Canva (free) - https://canva.com
- Photopea (free Photoshop alternative) - https://photopea.com

## Upload Timing

**Best times to upload (US audience):**
- Tuesday: 2-4 PM EST
- Wednesday: 2-4 PM EST
- Thursday: 12-3 PM EST
- Friday: 12-3 PM EST
- Saturday: 9-11 AM EST

**Why timing matters:**
- YouTube promotes new videos in first 24-48 hours
- Uploading when your audience is active = more initial views
- More initial views = better algorithm ranking

## Engagement Optimization

**In your video:**
- Ask viewers to like/subscribe (but don't overdo it)
- Ask a question to encourage comments
- Tease upcoming content

**After publishing:**
- Reply to every comment in first 24 hours
- Pin a comment with a question or CTA
- Share on social media

## Analytics to Track

**Key metrics:**
- **CTR (Click-Through Rate)**: Aim for 4-10%
- **Average View Duration**: Aim for 50%+ retention
- **Watch Time**: Total minutes watched

**If CTR is low:** Improve thumbnail and title
**If retention is low:** Improve content hooks and pacing

---

# High CPM Niches

For better monetization, focus on these niches:

| Niche | CPM Range | Example Topics |
|-------|-----------|----------------|
| Finance | $15-$50 | Investing, Credit Cards, Taxes |
| Business | $12-$35 | Entrepreneurship, Marketing, SaaS |
| Technology | $10-$30 | AI Tools, Software Reviews, Coding |
| Health | $10-$25 | Fitness, Nutrition, Mental Health |
| Education | $8-$20 | Online Courses, Study Tips, Career |

---

# Troubleshooting

## Common Issues

**"No module named 'moviepy'"**
- Delete the `venv` folder and run the batch file again

**"API key invalid"**
- Check your `.env` file has correct keys
- Get new keys from the API providers

**"No footage downloaded"**
- Check internet connection
- Pexels/Pixabay may be rate-limiting; wait a few minutes

**Video rendering is slow**
- Normal for longer videos (5-15 minutes for a 3-minute video)
- Close other applications to free up CPU

## Getting Help

If you encounter issues:
1. Check the error message in the console
2. Delete `venv` folder and try again
3. Ensure all API keys are valid

---

# License

This project is for educational purposes. Ensure you comply with:
- YouTube's Terms of Service
- Stock footage licensing (Pexels/Pixabay are free for commercial use)
- AI-generated content disclosure requirements

---

Made with AutoVideo - Generate faceless YouTube videos automatically!
