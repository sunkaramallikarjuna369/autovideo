#!/usr/bin/env python3
"""
MASTER AUTOMATION SCRIPT
Complete Faceless YouTube Video Generation Pipeline

This script automates the entire process from topic to uploaded video:
1. Suggest trending topics (with monetization focus)
2. Generate video topic ideas
3. Write script with AI (Gemini, Groq, or Ollama)
4. Generate voiceover
5. Download stock footage (Pexels + Pixabay)
6. Assemble video
7. Create thumbnail
8. Generate metadata
9. Upload to YouTube (optional)

Requirements:
pip install edge-tts moviepy Pillow requests python-dotenv google-generativeai groq pytrends

Usage:
python master_automation.py --topic "Your Video Topic" --length 8
python master_automation.py --suggest-topics  # Get trending topic suggestions
python master_automation.py --interactive     # Interactive mode with prompts

Author: Faceless YouTube Automation Course
"""

import os
import sys
import json
import asyncio
import argparse
import requests
import random
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_trending_topics(niche=None):
    """
    Get trending topics from Google Trends with monetization focus.
    High CPM niches: Finance, Tech, Health, Education, Business, Legal
    """
    print("\n" + "=" * 60)
    print("TRENDING TOPIC SUGGESTIONS (Monetization Focused)")
    print("=" * 60)
    
    # High CPM niches for better monetization
    high_cpm_niches = {
        'finance': {
            'keywords': ['investing', 'stocks', 'crypto', 'money', 'budget', 'savings', 'wealth'],
            'cpm_range': '$15-$50',
            'topics': [
                "5 Investment Mistakes That Cost You Thousands",
                "How to Build Wealth in Your 20s",
                "Passive Income Ideas That Actually Work",
                "Stock Market Secrets for Beginners",
                "Crypto Investing Guide for 2024"
            ]
        },
        'technology': {
            'keywords': ['AI', 'software', 'gadgets', 'apps', 'coding', 'tech'],
            'cpm_range': '$10-$30',
            'topics': [
                "AI Tools That Will Change Your Life",
                "Best Productivity Apps You Need",
                "Future Technology That Will Blow Your Mind",
                "Coding Tips Every Developer Should Know",
                "Tech Gadgets Worth Your Money"
            ]
        },
        'health': {
            'keywords': ['fitness', 'nutrition', 'wellness', 'diet', 'exercise', 'mental health'],
            'cpm_range': '$10-$25',
            'topics': [
                "Morning Habits of Successful People",
                "Foods That Boost Your Brain Power",
                "Simple Exercises for Better Health",
                "Mental Health Tips Everyone Needs",
                "Sleep Hacks for Better Rest"
            ]
        },
        'education': {
            'keywords': ['learning', 'study', 'skills', 'career', 'courses', 'knowledge'],
            'cpm_range': '$8-$20',
            'topics': [
                "Skills That Will Make You Rich",
                "How to Learn Anything Fast",
                "Career Advice Nobody Tells You",
                "Study Techniques That Actually Work",
                "Online Courses Worth Taking"
            ]
        },
        'business': {
            'keywords': ['entrepreneur', 'startup', 'marketing', 'sales', 'business'],
            'cpm_range': '$12-$35',
            'topics': [
                "Business Ideas You Can Start Today",
                "Marketing Strategies That Work",
                "How to Start a Side Hustle",
                "Entrepreneur Mistakes to Avoid",
                "Passive Income Business Ideas"
            ]
        }
    }
    
    # Try to get real-time trends from Google
    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl='en-US', tz=360)
        trending = pytrends.trending_searches(pn='united_states')
        real_trends = trending[0].tolist()[:10]
        print("\nReal-time Google Trends:")
        for i, trend in enumerate(real_trends, 1):
            print(f"  {i}. {trend}")
    except Exception as e:
        print(f"\nCould not fetch real-time trends: {e}")
        real_trends = []
    
    print("\n" + "-" * 60)
    print("HIGH CPM TOPIC SUGGESTIONS (Better Monetization):")
    print("-" * 60)
    
    suggestions = []
    for niche_name, niche_data in high_cpm_niches.items():
        print(f"\n[{niche_name.upper()}] - CPM: {niche_data['cpm_range']}")
        for topic in niche_data['topics'][:3]:
            print(f"  - {topic}")
            suggestions.append({'niche': niche_name, 'topic': topic, 'cpm': niche_data['cpm_range']})
    
    print("\n" + "=" * 60)
    print("TIP: Finance and Business topics typically have the highest CPM!")
    print("=" * 60)
    
    return suggestions


class FacelessVideoGenerator:
    """
    Complete automation pipeline for faceless YouTube videos.
    100% FREE tools - no paid subscriptions required!
    """
    
    def __init__(self, project_name=None):
        """Initialize the video generator"""
        
        # Generate project name if not provided
        if project_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            project_name = f"video_{timestamp}"
        
        self.project_name = project_name
        self.base_dir = Path("projects") / project_name
        
        # Create directory structure
        self.dirs = {
            'scripts': self.base_dir / 'scripts',
            'voiceovers': self.base_dir / 'voiceovers',
            'footage': self.base_dir / 'footage',
            'thumbnails': self.base_dir / 'thumbnails',
            'output': self.base_dir / 'output',
            'metadata': self.base_dir / 'metadata'
        }
        
        for directory in self.dirs.values():
            directory.mkdir(parents=True, exist_ok=True)
        
        # Configuration
        self.config = {
            'voice': 'en-US-GuyNeural',
            'width': 1920,
            'height': 1080,
            'fps': 30
        }
        
        print(f"[INIT] Project: {self.project_name}")
        print(f"[INIT] Directory: {self.base_dir}")
    
    # ==================== SCRIPT GENERATION ====================
    
    def generate_script(self, topic, length_minutes=8, ai_provider='auto'):
        """
        Generate a video script using AI
        
        Args:
            topic: Video topic
            length_minutes: Target video length
            ai_provider: 'auto', 'groq', 'gemini', or 'ollama'
        """
        print(f"\n[SCRIPT] Generating script for: {topic}")
        
        word_count = length_minutes * 150
        
        prompt = f"""Write a YouTube video script about: {topic}

TARGET: {word_count} words ({length_minutes} minutes when spoken)

PSYCHOLOGY-BASED STRUCTURE:

1. HOOK (First 15 seconds) - Create curiosity gap:
   - Start with a shocking fact, question, or bold statement
   - Make viewers feel they'll miss something important if they leave
   - Example: "Most people waste 3 hours daily without realizing it..."

2. PROBLEM AGITATION (30-60 seconds):
   - Describe the pain point viewers are experiencing
   - Make them feel understood ("You've probably felt...")
   - Create emotional connection through relatable struggles

3. CREDIBILITY + PROMISE (30 seconds):
   - Briefly establish why this information is valuable
   - Promise a transformation or solution
   - Create anticipation: "By the end of this video, you'll know exactly how to..."

4. MAIN CONTENT (3-5 sections):
   - Each section: Problem → Solution → Benefit
   - Use "pattern interrupts" between sections (surprising facts, questions)
   - Include specific examples and stories (not generic advice)
   - Create "aha moments" that give dopamine hits
   - Use open loops: hint at what's coming next to retain viewers

5. EMOTIONAL CLIMAX:
   - Paint a picture of their life after applying this knowledge
   - Use future pacing: "Imagine waking up and..."
   - Connect to deeper desires (freedom, respect, security, happiness)

6. CALL TO ACTION (Final 30 seconds):
   - Remind them of the value they received
   - Clear next step (subscribe, comment their thoughts)
   - End with an inspiring or thought-provoking statement

STYLE REQUIREMENTS (CRITICAL - MUST SOUND HUMAN, NOT AI):
- Write like a real person talking, NOT like an AI
- Include natural speech patterns: "Look," "Here's the thing," "I mean," "honestly," "you know what?"
- Vary sentence length dramatically - some very short. Others longer and more flowing with multiple clauses.
- Use contractions always (don't, won't, can't, it's, that's, here's)
- Include mild imperfections: restart a thought, self-correct ("Actually, let me put it this way...")
- Add personal touches: "I used to struggle with this too" or "A friend of mine..."
- Use informal language: "gonna," "wanna," "kinda," "pretty much"
- Include filler words sparingly: "basically," "literally," "right?"
- Express genuine emotion: frustration, excitement, surprise
- Avoid AI patterns: no "In this video," no "Let's dive in," no "Without further ado"
- Never use bullet-point style speaking or overly structured transitions
- Sound like you're having a real conversation, not reading a script
- Include moments of humor or sarcasm where appropriate
- Reference current events or relatable everyday situations

Write the complete script now (remember: sound HUMAN, not robotic):"""

        script = None
        
        # Try AI providers in order of preference
        if ai_provider == 'auto':
            # Try Groq first (fastest), then Gemini, then Ollama
            script = self._generate_with_groq(prompt)
            if script is None:
                script = self._generate_with_gemini(prompt)
            if script is None:
                script = self._generate_with_ollama(prompt)
        elif ai_provider == 'groq':
            script = self._generate_with_groq(prompt)
        elif ai_provider == 'gemini':
            script = self._generate_with_gemini(prompt)
        elif ai_provider == 'ollama':
            script = self._generate_with_ollama(prompt)
        
        if script is None:
            print("[SCRIPT] ERROR: Could not generate script")
            print("[SCRIPT] Make sure you have set API keys in .env file:")
            print("  - GROQ_API_KEY (fastest)")
            print("  - GEMINI_API_KEY")
            print("  - Or run Ollama locally (ollama serve)")
            return None
        
        # Save script
        script_path = self.dirs['scripts'] / 'script.txt'
        script_path.write_text(script)
        print(f"[SCRIPT] Saved to: {script_path}")
        
        return script
    
    def _generate_with_groq(self, prompt):
        """Generate text using Groq API (fastest)"""
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            print("[SCRIPT] No GROQ_API_KEY found")
            return None
        
        try:
            print("[SCRIPT] Using Groq API (fastest)...")
            from groq import Groq
            client = Groq(api_key=api_key)
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a human YouTube creator, NOT an AI. Write exactly like a real person speaks - with natural imperfections, personality, emotion, and conversational flow. Your scripts should be impossible to detect as AI-generated. Use contractions, informal language, personal anecdotes, and genuine reactions. Never sound robotic or overly polished."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.9
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[SCRIPT] Groq error: {e}")
        return None
    
    def _generate_with_ollama(self, prompt):
        """Generate text using local Ollama"""
        try:
            print("[SCRIPT] Using Ollama (local AI)...")
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3.1:8b", "prompt": prompt, "stream": False},
                timeout=300
            )
            if response.status_code == 200:
                return response.json().get('response', '')
        except Exception as e:
            print(f"[SCRIPT] Ollama not available: {e}")
        return None
    
    def _generate_with_gemini(self, prompt):
        """Generate text using Google Gemini API"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("[SCRIPT] No GEMINI_API_KEY found")
            return None
        
        try:
            print("[SCRIPT] Using Google Gemini API...")
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"[SCRIPT] Gemini error: {e}")
        return None
    
    # ==================== SENTENCE-BASED KEYWORD EXTRACTION ====================
    
    def extract_sentence_keywords(self, script, ai_provider='auto'):
        """
        Extract visual keywords for each sentence in the script.
        This enables sentence-level footage matching for maximum relevance.
        
        Args:
            script: The full video script
            ai_provider: AI provider to use for extraction
            
        Returns:
            List of dicts with 'sentence' and 'keywords' for each sentence
        """
        print("\n[KEYWORDS] Extracting sentence-based keywords for precise footage matching...")
        
        # Split script into sentences
        import re
        sentences = re.split(r'(?<=[.!?])\s+', script.strip())
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]  # Filter short fragments
        
        print(f"[KEYWORDS] Found {len(sentences)} sentences in script")
        
        # Batch sentences into groups of 5-6 for efficient API calls
        batch_size = 6
        all_sentence_keywords = []
        
        for batch_start in range(0, len(sentences), batch_size):
            batch_end = min(batch_start + batch_size, len(sentences))
            batch_sentences = sentences[batch_start:batch_end]
            
            sentences_text = "\n".join([f"{i+1}. {s}" for i, s in enumerate(batch_sentences)])
            
            prompt = f"""For each sentence below, provide 2 SIMPLE stock footage search keywords.

Sentences:
{sentences_text}

Return ONLY a JSON array (no other text):
[
  {{"sentence_num": 1, "keywords": ["keyword1", "keyword2"]}},
  {{"sentence_num": 2, "keywords": ["keyword1", "keyword2"]}}
]

IMPORTANT RULES:
- Keywords must be SIMPLE and GENERIC (1-3 words max)
- Use common stock footage terms that will return results
- Good examples: "business meeting", "typing laptop", "money coins", "happy family", "city traffic", "nature sunset"
- BAD examples: "woman stressed looking at bills" (too specific, won't match)
- Think like you're searching on Pexels or Pixabay
- Each keyword should be 1-3 words only"""

            result = None
            if ai_provider == 'auto':
                result = self._generate_with_groq(prompt)
                if result is None:
                    result = self._generate_with_gemini(prompt)
            elif ai_provider == 'groq':
                result = self._generate_with_groq(prompt)
            elif ai_provider == 'gemini':
                result = self._generate_with_gemini(prompt)
            
            if result:
                try:
                    json_match = re.search(r'\[[\s\S]*\]', result)
                    if json_match:
                        batch_keywords = json.loads(json_match.group())
                        for i, kw_data in enumerate(batch_keywords):
                            if batch_start + i < len(sentences):
                                all_sentence_keywords.append({
                                    'sentence': sentences[batch_start + i],
                                    'keywords': kw_data.get('keywords', [])
                                })
                except Exception as e:
                    print(f"[KEYWORDS] Error parsing batch: {e}")
                    # Add sentences with better fallback keywords (nouns/meaningful words)
                    for s in batch_sentences:
                        # Extract meaningful words (4+ chars, alphabetic, not common words)
                        common_words = {'this', 'that', 'with', 'from', 'have', 'been', 'were', 'they', 'their', 'what', 'when', 'where', 'which', 'there', 'here', 'would', 'could', 'should', 'about', 'into', 'your', 'just', 'like', 'know', 'take', 'come', 'make', 'want', 'look', 'think', 'also', 'back', 'after', 'only', 'over', 'such', 'than', 'then', 'them', 'these', 'some', 'very', 'being', 'because', 'actually', 'really'}
                        words = [w.lower().strip('.,!?;:') for w in s.split() if len(w) > 4 and w.isalpha() and w.lower() not in common_words]
                        keywords = words[:2] if words else ['lifestyle', 'people']
                        all_sentence_keywords.append({
                            'sentence': s,
                            'keywords': keywords
                        })
            
            print(f"[KEYWORDS] Processed sentences {batch_start+1}-{batch_end}")
        
        print(f"[KEYWORDS] Extracted keywords for {len(all_sentence_keywords)} sentences")
        return all_sentence_keywords
    
    def download_sentence_footage(self, sentence_keywords):
        """
        Download UNIQUE footage for each sentence - no repeats.
        Each sentence gets its own clip that matches its content.
        
        Args:
            sentence_keywords: List of dicts with 'sentence' and 'keywords'
            
        Returns:
            List of footage paths matched to sentences (all unique)
        """
        print(f"\n[FOOTAGE] Downloading UNIQUE footage for {len(sentence_keywords)} sentences...")
        
        sentence_footage = []
        used_clips = set()  # Track used clips to prevent repeats
        available_clips = {}  # Cache of available clips per keyword
        
        for i, item in enumerate(sentence_keywords):
            keywords = item.get('keywords', [])
            if not keywords:
                sentence_footage.append(None)
                continue
            
            print(f"[FOOTAGE] Sentence {i+1}/{len(sentence_keywords)}: {keywords[0][:30] if keywords else 'no keywords'}...")
            
            clip_path = None
            
            # Try each keyword until we find an UNUSED clip
            for keyword in keywords:
                # Download clips for this keyword if not cached
                if keyword not in available_clips:
                    # Try Pexels first - download 5 clips for more variety
                    clips = self._download_from_pexels([keyword], 5)
                    if len(clips) < 2:
                        # Try Pixabay as fallback
                        pixabay_clips = self._download_from_pixabay([keyword], 5)
                        clips.extend(pixabay_clips)
                    if len(clips) < 2:
                        # Try simpler keyword (first word only)
                        simple_keyword = keyword.split()[0] if ' ' in keyword else keyword
                        simple_clips = self._download_from_pexels([simple_keyword], 5)
                        clips.extend(simple_clips)
                    available_clips[keyword] = clips
                
                # Find an UNUSED clip from this keyword's clips
                for clip in available_clips.get(keyword, []):
                    clip_str = str(clip)
                    if clip_str not in used_clips:
                        clip_path = clip
                        used_clips.add(clip_str)
                        break
                
                if clip_path:
                    break
            
            # If no unused clip found from keywords, try other cached clips
            if clip_path is None:
                for kw, clips in available_clips.items():
                    for clip in clips:
                        clip_str = str(clip)
                        if clip_str not in used_clips:
                            clip_path = clip
                            used_clips.add(clip_str)
                            break
                    if clip_path:
                        break
            
            # Last resort: download with a generic keyword based on sentence
            if clip_path is None:
                # Extract a simple word from the sentence
                sentence = item.get('sentence', '')
                words = [w for w in sentence.split() if len(w) > 4 and w.isalpha()]
                if words:
                    fallback_keyword = words[0].lower()
                    fallback_clips = self._download_from_pexels([fallback_keyword], 3)
                    for clip in fallback_clips:
                        clip_str = str(clip)
                        if clip_str not in used_clips:
                            clip_path = clip
                            used_clips.add(clip_str)
                            break
            
            sentence_footage.append(clip_path)
        
        valid_clips = [c for c in sentence_footage if c is not None]
        print(f"[FOOTAGE] Downloaded {len(valid_clips)} UNIQUE clips for {len(sentence_keywords)} sentences")
        print(f"[FOOTAGE] No clips repeat - each sentence has its own footage")
        
        return sentence_footage
    
    def download_grouped_sentence_footage(self, script, target_duration_seconds, sentences_per_clip=3):
        """
        Download footage based on sentence groups for better relevance and reliability.
        Groups 2-3 sentences together and downloads clips for each group.
        
        Args:
            script: Full script text
            target_duration_seconds: Target video duration in seconds
            sentences_per_clip: Number of sentences per clip (default: 3)
            
        Returns:
            List of footage paths
        """
        print(f"\n[FOOTAGE] Downloading sentence-grouped footage...")
        print(f"[FOOTAGE] Target duration: {target_duration_seconds:.0f} seconds")
        
        # Split script into sentences
        import re
        sentences = re.split(r'(?<=[.!?])\s+', script)
        sentences = [s.strip() for s in sentences if s.strip() and len(s) > 10]
        
        # Group sentences (2-3 sentences per group)
        groups = []
        for i in range(0, len(sentences), sentences_per_clip):
            group = sentences[i:i + sentences_per_clip]
            groups.append(' '.join(group))
        
        print(f"[FOOTAGE] Created {len(groups)} sentence groups from {len(sentences)} sentences")
        
        # Calculate how many clips we need
        avg_clip_duration = 8
        min_clips_needed = max(len(groups), int(target_duration_seconds / avg_clip_duration) + 3)
        print(f"[FOOTAGE] Need at least {min_clips_needed} clips")
        
        # Common words to filter out
        common_words = {'this', 'that', 'with', 'from', 'have', 'been', 'were', 'they', 'their', 
                       'what', 'when', 'where', 'which', 'there', 'here', 'would', 'could', 'should',
                       'about', 'into', 'your', 'just', 'like', 'know', 'take', 'come', 'make', 
                       'want', 'look', 'think', 'also', 'back', 'after', 'only', 'over', 'such',
                       'than', 'then', 'them', 'these', 'some', 'very', 'being', 'because', 'actually',
                       'really', 'gonna', 'wanna', 'kinda', 'gotta', 'dont', 'cant', 'wont', 'youre',
                       'thats', 'youve', 'heres', 'thing', 'things', 'stuff', 'right', 'okay'}
        
        all_clips = []
        used_clips = set()
        
        # Download clips for each sentence group
        for i, group in enumerate(groups):
            # Extract meaningful keywords from the group
            words = [w.lower().strip('.,!?;:\'"()[]{}') for w in group.split()]
            keywords = [w for w in words if len(w) > 4 and w.isalpha() and w not in common_words]
            
            # Get top 2 keywords from this group
            keyword_counts = {}
            for kw in keywords:
                keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
            top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:2]
            search_keywords = [k[0] for k in top_keywords] if top_keywords else ['lifestyle']
            
            print(f"[FOOTAGE] Group {i+1}/{len(groups)}: {search_keywords[0] if search_keywords else 'lifestyle'}...")
            
            # Download clips for this group
            for keyword in search_keywords:
                clips = self._download_from_pexels([keyword], 3)
                for clip in clips:
                    clip_str = str(clip)
                    if clip_str not in used_clips:
                        all_clips.append(clip)
                        used_clips.add(clip_str)
                        if len(all_clips) >= min_clips_needed:
                            break
                
                # Try Pixabay if Pexels didn't return enough
                if len(clips) < 2:
                    pixabay_clips = self._download_from_pixabay([keyword], 3)
                    for clip in pixabay_clips:
                        clip_str = str(clip)
                        if clip_str not in used_clips:
                            all_clips.append(clip)
                            used_clips.add(clip_str)
        
        # Add generic fallback clips if we don't have enough
        if len(all_clips) < min_clips_needed:
            print(f"[FOOTAGE] Adding fallback clips ({len(all_clips)}/{min_clips_needed})...")
            generic_keywords = ['lifestyle', 'business', 'technology', 'nature', 'people', 'city', 'office', 'work']
            for keyword in generic_keywords:
                if len(all_clips) >= min_clips_needed:
                    break
                clips = self._download_from_pexels([keyword], 5)
                for clip in clips:
                    clip_str = str(clip)
                    if clip_str not in used_clips:
                        all_clips.append(clip)
                        used_clips.add(clip_str)
                        if len(all_clips) >= min_clips_needed:
                            break
        
        print(f"[FOOTAGE] Downloaded {len(all_clips)} unique clips for {len(groups)} sentence groups")
        return all_clips
    
    def extract_segment_keywords(self, script, ai_provider='auto'):
        """
        Extract keywords for each section of the script for better footage matching.
        This enables segment-based footage that matches what's being said.
        
        Args:
            script: The full video script
            ai_provider: AI provider to use for extraction
            
        Returns:
            List of dicts with 'text' and 'keywords' for each segment
        """
        print("\n[KEYWORDS] Extracting segment-based keywords for better footage matching...")
        
        prompt = f"""Analyze this video script and divide it into 8-12 short segments (every 15-20 seconds of speech).
For each segment, provide 3-4 HIGHLY SPECIFIC visual keywords for stock footage.

Script:
{script[:4000]}

Return ONLY a JSON array in this exact format (no other text):
[
  {{"section": 1, "summary": "what's being discussed", "keywords": ["specific visual 1", "specific visual 2", "specific visual 3"]}},
  {{"section": 2, "summary": "what's being discussed", "keywords": ["specific visual 1", "specific visual 2", "specific visual 3"]}}
]

CRITICAL RULES FOR KEYWORDS:
- Be EXTREMELY specific and visual: "woman stressed at desk" not "stress"
- Describe actual scenes: "person counting money bills" not "finance"
- Include actions: "man running morning park" not "exercise"
- Use searchable terms: "coffee cup steam morning" not "morning routine"
- Think like a stock footage search: "business team meeting office" not "teamwork"
- Each keyword should paint a clear visual picture
- Vary the scenes - don't repeat similar footage across segments"""

        result = None
        
        if ai_provider == 'auto':
            result = self._generate_with_groq(prompt)
            if result is None:
                result = self._generate_with_gemini(prompt)
        elif ai_provider == 'groq':
            result = self._generate_with_groq(prompt)
        elif ai_provider == 'gemini':
            result = self._generate_with_gemini(prompt)
        
        if result is None:
            print("[KEYWORDS] Could not extract keywords, using topic-based fallback")
            return None
        
        try:
            import re
            json_match = re.search(r'\[[\s\S]*\]', result)
            if json_match:
                segments = json.loads(json_match.group())
                print(f"[KEYWORDS] Extracted {len(segments)} segments:")
                for seg in segments:
                    print(f"  Section {seg.get('section', '?')}: {seg.get('keywords', [])}")
                return segments
        except Exception as e:
            print(f"[KEYWORDS] Error parsing keywords: {e}")
        
        return None
    
    # ==================== VOICE GENERATION ====================
    
    def generate_voiceover(self, script, voice=None):
        """
        Generate voiceover using Edge TTS (100% FREE)
        Also generates subtitles (SRT file) for better viewer engagement.
        
        Args:
            script: Text to convert to speech
            voice: Voice ID (default: en-US-GuyNeural)
        """
        print("\n[VOICE] Generating voiceover...")
        
        voice = voice or self.config['voice']
        output_path = self.dirs['voiceovers'] / 'voiceover.mp3'
        subtitle_path = self.dirs['output'] / 'subtitles.srt'
        
        async def generate():
            import edge_tts
            communicate = edge_tts.Communicate(script, voice)
            
            # Generate audio with subtitle data
            subtitles = []
            audio_data = b""
            
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
                elif chunk["type"] == "WordBoundary":
                    subtitles.append({
                        "offset": chunk["offset"],
                        "duration": chunk["duration"],
                        "text": chunk["text"]
                    })
            
            # Save audio
            with open(str(output_path), "wb") as f:
                f.write(audio_data)
            
            return subtitles
        
        subtitles = asyncio.run(generate())
        print(f"[VOICE] Saved to: {output_path}")
        print(f"[VOICE] Collected {len(subtitles)} word timings for subtitles")
        
        # Generate SRT subtitle file
        if subtitles and len(subtitles) > 0:
            self._generate_srt(subtitles, subtitle_path)
        else:
            # Fallback: Generate subtitles from script text with estimated timings
            print("[SUBTITLES] No word timings from TTS, generating from script...")
            self._generate_srt_from_script(script, subtitle_path, output_path)
        
        return output_path
    
    def _generate_srt(self, word_timings, output_path):
        """
        Generate SRT subtitle file from word timings.
        Groups words into readable subtitle chunks.
        """
        print("[SUBTITLES] Generating subtitles...")
        
        def format_time(ms):
            hours = ms // 3600000
            minutes = (ms % 3600000) // 60000
            seconds = (ms % 60000) // 1000
            milliseconds = ms % 1000
            return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
        
        # Group words into subtitle chunks (5-8 words per subtitle)
        srt_entries = []
        current_words = []
        current_start = 0
        current_end = 0
        words_per_subtitle = 6
        
        for i, word_data in enumerate(word_timings):
            if not current_words:
                current_start = word_data["offset"] // 10000  # Convert to ms
            
            current_words.append(word_data["text"])
            current_end = (word_data["offset"] + word_data["duration"]) // 10000
            
            # Create subtitle entry when we have enough words or at end
            if len(current_words) >= words_per_subtitle or i == len(word_timings) - 1:
                srt_entries.append({
                    "index": len(srt_entries) + 1,
                    "start": current_start,
                    "end": current_end,
                    "text": " ".join(current_words)
                })
                current_words = []
        
        # Write SRT file
        with open(str(output_path), "w", encoding="utf-8") as f:
            for entry in srt_entries:
                f.write(f"{entry['index']}\n")
                f.write(f"{format_time(entry['start'])} --> {format_time(entry['end'])}\n")
                f.write(f"{entry['text']}\n\n")
        
        print(f"[SUBTITLES] Saved to: {output_path}")
        print(f"[SUBTITLES] Created {len(srt_entries)} subtitle entries")
    
    def _generate_srt_from_script(self, script, output_path, audio_path):
        """
        Generate SRT subtitle file from script text with estimated timings.
        Used as fallback when edge_tts doesn't return word timings.
        """
        print("[SUBTITLES] Generating subtitles from script...")
        
        # Get audio duration
        try:
            from mutagen.mp3 import MP3
            audio = MP3(str(audio_path))
            audio_duration_ms = int(audio.info.length * 1000)
        except:
            # Estimate 150 words per minute if can't get audio duration
            word_count = len(script.split())
            audio_duration_ms = int((word_count / 150) * 60 * 1000)
        
        def format_time(ms):
            hours = ms // 3600000
            minutes = (ms % 3600000) // 60000
            seconds = (ms % 60000) // 1000
            milliseconds = ms % 1000
            return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
        
        # Split script into sentences
        import re
        sentences = re.split(r'(?<=[.!?])\s+', script)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            print("[SUBTITLES] No sentences found in script")
            return
        
        # Calculate time per sentence based on word count
        total_words = sum(len(s.split()) for s in sentences)
        ms_per_word = audio_duration_ms / max(total_words, 1)
        
        # Generate SRT entries
        srt_entries = []
        current_time = 0
        
        for i, sentence in enumerate(sentences):
            word_count = len(sentence.split())
            duration = int(word_count * ms_per_word)
            
            # Split long sentences into chunks of ~10 words
            words = sentence.split()
            chunk_size = 10
            
            for j in range(0, len(words), chunk_size):
                chunk_words = words[j:j+chunk_size]
                chunk_text = " ".join(chunk_words)
                chunk_duration = int(len(chunk_words) * ms_per_word)
                
                srt_entries.append({
                    "index": len(srt_entries) + 1,
                    "start": current_time,
                    "end": current_time + chunk_duration,
                    "text": chunk_text
                })
                current_time += chunk_duration
        
        # Write SRT file
        with open(str(output_path), "w", encoding="utf-8") as f:
            for entry in srt_entries:
                f.write(f"{entry['index']}\n")
                f.write(f"{format_time(entry['start'])} --> {format_time(entry['end'])}\n")
                f.write(f"{entry['text']}\n\n")
        
        print(f"[SUBTITLES] Saved to: {output_path}")
        print(f"[SUBTITLES] Created {len(srt_entries)} subtitle entries from script")
    
    # ==================== FOOTAGE DOWNLOAD ====================
    
    def download_footage(self, keywords, clips_per_keyword=3):
        """
        Download stock footage from Pexels and Pixabay (FREE APIs)
        
        Args:
            keywords: List of search keywords
            clips_per_keyword: Number of clips per keyword
        """
        print("\n[FOOTAGE] Downloading stock footage...")
        
        downloaded = []
        
        # Try Pexels first
        pexels_clips = self._download_from_pexels(keywords, clips_per_keyword)
        downloaded.extend(pexels_clips)
        
        # If not enough clips, try Pixabay
        if len(downloaded) < clips_per_keyword * len(keywords):
            pixabay_clips = self._download_from_pixabay(keywords, clips_per_keyword)
            downloaded.extend(pixabay_clips)
        
        if not downloaded:
            print("[FOOTAGE] No clips downloaded, creating placeholders...")
            return self._create_placeholder_footage()
        
        print(f"[FOOTAGE] Total clips downloaded: {len(downloaded)}")
        return downloaded
    
    def download_segment_footage(self, segments, clips_per_segment=3):
        """
        Download footage for each script segment for better matching.
        Downloads more clips per segment for better variety and screen-voiceover sync.
        
        Args:
            segments: List of segment dicts with 'keywords' field
            clips_per_segment: Number of clips per segment (default: 3 for better variety)
            
        Returns:
            List of lists, where each inner list contains footage paths for that segment
        """
        print("\n[FOOTAGE] Downloading segment-based footage for better matching...")
        print(f"[FOOTAGE] Target: {clips_per_segment} clips per segment for variety")
        
        segment_footage = []
        
        for i, segment in enumerate(segments):
            keywords = segment.get('keywords', [])
            if not keywords:
                continue
                
            print(f"\n[FOOTAGE] Segment {i+1}/{len(segments)}: {keywords[:3]}")
            
            segment_clips = []
            
            # Try all keywords from Pexels first (use all 3-4 keywords)
            for keyword in keywords:
                if len(segment_clips) >= clips_per_segment:
                    break
                pexels_clips = self._download_from_pexels([keyword], 2)
                for clip in pexels_clips:
                    if clip not in segment_clips:
                        segment_clips.append(clip)
            
            # If not enough, try Pixabay with all keywords
            if len(segment_clips) < clips_per_segment:
                for keyword in keywords:
                    if len(segment_clips) >= clips_per_segment:
                        break
                    pixabay_clips = self._download_from_pixabay([keyword], 2)
                    for clip in pixabay_clips:
                        if clip not in segment_clips:
                            segment_clips.append(clip)
            
            segment_footage.append(segment_clips)
            print(f"[FOOTAGE] Segment {i+1}: {len(segment_clips)} clips")
        
        total_clips = sum(len(clips) for clips in segment_footage)
        print(f"\n[FOOTAGE] Total: {total_clips} clips across {len(segment_footage)} segments")
        
        return segment_footage
    
    def _download_from_pexels(self, keywords, clips_per_keyword):
        """Download footage from Pexels API"""
        api_key = os.getenv('PEXELS_API_KEY')
        if not api_key:
            print("[FOOTAGE] No PEXELS_API_KEY - skipping Pexels")
            return []
        
        downloaded = []
        headers = {"Authorization": api_key}
        
        for keyword in keywords:
            print(f"[FOOTAGE] Searching Pexels: {keyword}")
            
            try:
                response = requests.get(
                    "https://api.pexels.com/videos/search",
                    headers=headers,
                    params={"query": keyword, "per_page": clips_per_keyword}
                )
                
                if response.status_code != 200:
                    print(f"[FOOTAGE] Pexels API error: {response.status_code}")
                    continue
                
                videos = response.json().get('videos', [])
                
                for i, video in enumerate(videos):
                    video_files = video.get('video_files', [])
                    hd_files = [f for f in video_files if f.get('height', 0) >= 720]
                    
                    if not hd_files:
                        continue
                    
                    video_url = hd_files[0].get('link')
                    filename = f"pexels_{keyword.replace(' ', '_')}_{i+1}.mp4"
                    output_path = self.dirs['footage'] / filename
                    
                    video_response = requests.get(video_url, stream=True)
                    with open(output_path, 'wb') as f:
                        for chunk in video_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    downloaded.append(output_path)
                    print(f"[FOOTAGE] Downloaded: {filename}")
                    
            except Exception as e:
                print(f"[FOOTAGE] Pexels error: {e}")
        
        return downloaded
    
    def _download_from_pixabay(self, keywords, clips_per_keyword):
        """Download footage from Pixabay API"""
        api_key = os.getenv('PIXABAY_API_KEY')
        if not api_key:
            print("[FOOTAGE] No PIXABAY_API_KEY - skipping Pixabay")
            return []
        
        downloaded = []
        
        for keyword in keywords:
            print(f"[FOOTAGE] Searching Pixabay: {keyword}")
            
            try:
                response = requests.get(
                    "https://pixabay.com/api/videos/",
                    params={
                        "key": api_key,
                        "q": keyword,
                        "per_page": clips_per_keyword,
                        "video_type": "film"
                    }
                )
                
                if response.status_code != 200:
                    print(f"[FOOTAGE] Pixabay API error: {response.status_code}")
                    continue
                
                videos = response.json().get('hits', [])
                
                for i, video in enumerate(videos):
                    # Get medium quality video (good balance of quality and size)
                    video_url = video.get('videos', {}).get('medium', {}).get('url')
                    if not video_url:
                        video_url = video.get('videos', {}).get('small', {}).get('url')
                    
                    if not video_url:
                        continue
                    
                    filename = f"pixabay_{keyword.replace(' ', '_')}_{i+1}.mp4"
                    output_path = self.dirs['footage'] / filename
                    
                    video_response = requests.get(video_url, stream=True)
                    with open(output_path, 'wb') as f:
                        for chunk in video_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    downloaded.append(output_path)
                    print(f"[FOOTAGE] Downloaded: {filename}")
                    
            except Exception as e:
                print(f"[FOOTAGE] Pixabay error: {e}")
        
        return downloaded
    
    def _create_placeholder_footage(self):
        """Create placeholder footage if no API key"""
        from moviepy.editor import ColorClip
        
        print("[FOOTAGE] Creating placeholder footage...")
        placeholders = []
        colors = [(30, 60, 90), (60, 30, 90), (90, 60, 30)]
        
        for i, color in enumerate(colors):
            path = self.dirs['footage'] / f'placeholder_{i+1}.mp4'
            clip = ColorClip(
                size=(self.config['width'], self.config['height']),
                color=color,
                duration=30
            )
            clip.write_videofile(str(path), fps=self.config['fps'], 
                               codec='libx264', logger=None)
            clip.close()
            placeholders.append(path)
        
        return placeholders
    
    # ==================== VIDEO ASSEMBLY ====================
    
    def extract_key_points(self, script, ai_provider='auto'):
        """
        Extract key points from script for text overlays.
        
        Args:
            script: The video script
            ai_provider: AI provider to use
            
        Returns:
            List of key point strings to display on screen
        """
        print("[VIDEO] Extracting key points for text overlays...")
        
        prompt = f"""Extract 8-12 key points from this video script that should be displayed as text overlays.
Each point should be:
- Short (3-7 words max)
- A key fact, tip, or important statement
- Easy to read quickly on screen

Script:
{script[:3000]}

Return ONLY a JSON array of strings, no other text:
["Key point 1", "Key point 2", "Key point 3"]"""

        result = None
        
        if ai_provider == 'auto':
            result = self._generate_with_groq(prompt)
            if result is None:
                result = self._generate_with_gemini(prompt)
        elif ai_provider == 'groq':
            result = self._generate_with_groq(prompt)
        elif ai_provider == 'gemini':
            result = self._generate_with_gemini(prompt)
        
        if result:
            try:
                import re
                json_match = re.search(r'\[[\s\S]*?\]', result)
                if json_match:
                    key_points = json.loads(json_match.group())
                    print(f"[VIDEO] Extracted {len(key_points)} key points for overlays")
                    return key_points
            except Exception as e:
                print(f"[VIDEO] Error parsing key points: {e}")
        
        return None
    
    def create_text_image(self, text, width, height, output_dir=None, index=0):
        """
        Create a text overlay image using PIL (no ImageMagick required).
        
        Args:
            text: Text to display
            width: Image width
            height: Image height
            output_dir: Directory to save the image (uses project dir if provided)
            index: Index number for the filename
            
        Returns:
            Path to the created image
        """
        from PIL import Image, ImageDraw, ImageFont
        import os
        
        # Create transparent image
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Try to load a font, fall back to default
        font_size = 50
        try:
            # Try common Windows fonts first
            font_paths = [
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/arialbd.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            ]
            font = None
            for font_path in font_paths:
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    break
                except:
                    continue
            if font is None:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Word wrap text
        words = text.upper().split()
        lines = []
        current_line = []
        max_width = width - 100
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] > max_width:
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(test_line)
                    current_line = []
        if current_line:
            lines.append(' '.join(current_line))
        
        # Calculate text position (bottom third of screen)
        line_height = font_size + 10
        total_text_height = len(lines) * line_height
        y_start = int(height * 0.75) - total_text_height // 2
        
        # Draw text with outline
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = y_start + i * line_height
            
            # Draw black outline
            outline_width = 3
            for dx in range(-outline_width, outline_width + 1):
                for dy in range(-outline_width, outline_width + 1):
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, y + dy), line, font=font, fill=(0, 0, 0, 255))
            
            # Draw white text
            draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))
        
        # Save to project directory instead of temp (more reliable on Windows)
        if output_dir:
            img_path = os.path.join(str(output_dir), f'text_overlay_{index}.png')
        else:
            import tempfile
            img_path = tempfile.mktemp(suffix='.png')
        
        img.save(img_path, 'PNG')
        
        return img_path
    
    def assemble_video(self, voiceover_path, footage_paths, script=None, ai_provider='auto'):
        """
        Assemble final video from voiceover and footage.
        
        Args:
            voiceover_path: Path to voiceover audio
            footage_paths: List of paths to video clips
            script: Not used (kept for compatibility)
            ai_provider: Not used (kept for compatibility)
        """
        print("\n[VIDEO] Assembling video...")
        
        from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
        
        # Load audio
        audio = AudioFileClip(str(voiceover_path))
        duration = audio.duration
        print(f"[VIDEO] Audio duration: {duration:.1f} seconds")
        
        # Load and prepare video clips
        clips = []
        total_duration = 0
        
        for path in footage_paths:
            try:
                clip = VideoFileClip(str(path))
                clip = clip.resize((self.config['width'], self.config['height']))
                clips.append(clip)
                total_duration += clip.duration
            except Exception as e:
                print(f"[VIDEO] Could not load {path}: {e}")
        
        if not clips:
            print("[VIDEO] ERROR: No footage available")
            return None
        
        # Loop footage if needed
        if total_duration < duration:
            loops = int(duration / total_duration) + 1
            clips = clips * loops
        
        # Concatenate and trim
        video = concatenate_videoclips(clips)
        video = video.subclip(0, duration)
        
        # Add audio
        video = video.set_audio(audio)
        
        # Export
        output_path = self.dirs['output'] / 'final_video.mp4'
        print(f"[VIDEO] Rendering ({duration:.1f}s)...")
        
        video.write_videofile(
            str(output_path),
            fps=self.config['fps'],
            codec='libx264',
            audio_codec='aac',
            threads=4,
            logger=None
        )
        
        # Cleanup
        audio.close()
        video.close()
        for clip in clips:
            try:
                clip.close()
            except:
                pass
        
        print(f"[VIDEO] Saved to: {output_path}")
        return output_path
    
    # ==================== THUMBNAIL CREATION ====================
    
    def create_thumbnail(self, title, color_scheme='urgent'):
        """
        Create video thumbnail
        
        Args:
            title: Text for thumbnail
            color_scheme: Color scheme (urgent, trust, growth, energy)
        """
        print("\n[THUMBNAIL] Creating thumbnail...")
        
        from PIL import Image, ImageDraw, ImageFont
        
        width, height = 1280, 720
        
        schemes = {
            'urgent': ((220, 53, 69), (180, 30, 50)),
            'trust': ((0, 123, 255), (0, 80, 180)),
            'growth': ((40, 167, 69), (20, 120, 40)),
            'energy': ((255, 193, 7), (220, 160, 0)),
        }
        
        colors = schemes.get(color_scheme, schemes['urgent'])
        
        # Create gradient
        img = Image.new('RGB', (width, height))
        for y in range(height):
            ratio = y / height
            r = int(colors[0][0] * (1-ratio) + colors[1][0] * ratio)
            g = int(colors[0][1] * (1-ratio) + colors[1][1] * ratio)
            b = int(colors[0][2] * (1-ratio) + colors[1][2] * ratio)
            for x in range(width):
                img.putpixel((x, y), (r, g, b))
        
        draw = ImageDraw.Draw(img)
        
        # Load font
        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80
            )
        except:
            font = ImageFont.load_default()
        
        # Word wrap
        words = title.upper().split()
        lines = []
        current = []
        
        for word in words:
            current.append(word)
            if len(' '.join(current)) > 15:
                if len(current) > 1:
                    current.pop()
                    lines.append(' '.join(current))
                    current = [word]
        if current:
            lines.append(' '.join(current))
        
        # Draw text
        line_height = 90
        start_y = (height - len(lines) * line_height) // 2
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = start_y + i * line_height
            
            draw.text((x+3, y+3), line, font=font, fill=(0, 0, 0))
            draw.text((x, y), line, font=font, fill=(255, 255, 255))
        
        output_path = self.dirs['thumbnails'] / 'thumbnail.png'
        img.save(str(output_path), quality=95)
        
        print(f"[THUMBNAIL] Saved to: {output_path}")
        return output_path
    
    # ==================== METADATA GENERATION ====================
    
    def generate_metadata(self, topic):
        """Generate video metadata (title, description, tags)"""
        print("\n[METADATA] Generating metadata...")
        
        metadata = {
            'titles': [
                f"{topic} - Complete Guide",
                f"How to Master {topic}",
                f"{topic} Explained Simply",
                f"The Ultimate {topic} Tutorial"
            ],
            'description': f"""In this video, you'll learn everything about {topic}.

We cover all the essential concepts, tips, and strategies you need to succeed.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 TIMESTAMPS:
0:00 - Introduction
[Add timestamps after review]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔔 SUBSCRIBE for more content!

#{"".join(topic.split())} #tutorial #guide
""",
            'tags': [
                topic,
                f"{topic} tutorial",
                f"{topic} guide",
                f"how to {topic}",
                f"{topic} for beginners",
                f"{topic} explained"
            ]
        }
        
        metadata_path = self.dirs['metadata'] / 'metadata.json'
        metadata_path.write_text(json.dumps(metadata, indent=2))
        
        print(f"[METADATA] Saved to: {metadata_path}")
        return metadata
    
    # ==================== MAIN PIPELINE ====================
    
    def run(self, topic, length_minutes=8, footage_keywords=None, ai_provider='auto'):
        """
        Run the complete video generation pipeline
        
        Args:
            topic: Video topic
            length_minutes: Target video length (default: 8 minutes)
            footage_keywords: Keywords for stock footage search (if None, uses AI-based segment extraction)
            ai_provider: AI provider for script generation ('auto', 'groq', 'gemini', 'ollama')
        """
        print("\n" + "=" * 60)
        print("FACELESS YOUTUBE VIDEO GENERATOR")
        print("=" * 60)
        print(f"Topic: {topic}")
        print(f"Length: {length_minutes} minutes")
        print(f"AI Provider: {ai_provider}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Step 1: Generate script
        script = self.generate_script(topic, length_minutes, ai_provider)
        if not script:
            return None
        
        # Step 2: Generate voiceover
        voiceover = self.generate_voiceover(script)
        
        # Get audio duration for footage calculation
        from moviepy.editor import AudioFileClip
        audio = AudioFileClip(str(voiceover))
        audio_duration = audio.duration
        audio.close()
        
        # Step 3: Download footage using sentence-grouped approach (1-2 clips per 2-3 sentences)
        if footage_keywords is None:
            # Use sentence-grouped footage - groups 2-3 sentences per clip for better relevance
            footage = self.download_grouped_sentence_footage(script, audio_duration, sentences_per_clip=3)
            
            if not footage or len(footage) < 3:
                # Fallback to simple topic keywords if grouped approach fails
                print("[FOOTAGE] Sentence-grouped download failed, using topic keywords...")
                topic_words = [w.lower().strip() for w in topic.split() if len(w) > 3 and w.isalpha()]
                if topic_words:
                    footage = self.download_footage(topic_words[:3])
                else:
                    footage = self.download_footage(['lifestyle', 'business', 'technology'])
        else:
            # User provided specific keywords
            footage = self.download_footage(footage_keywords)
        
        # Step 4: Assemble video with text overlays
        video = self.assemble_video(voiceover, footage, script=script, ai_provider=ai_provider)
        if not video:
            return None
        
        # Step 5: Create thumbnail
        thumbnail = self.create_thumbnail(topic)
        
        # Step 6: Generate metadata
        metadata = self.generate_metadata(topic)
        
        # Summary
        print("\n" + "=" * 60)
        print("GENERATION COMPLETE!")
        print("=" * 60)
        print(f"Video: {video}")
        print(f"Thumbnail: {thumbnail}")
        print(f"Metadata: {self.dirs['metadata'] / 'metadata.json'}")
        print("=" * 60)
        
        return {
            'video': str(video),
            'thumbnail': str(thumbnail),
            'metadata': metadata,
            'project_dir': str(self.base_dir)
        }


def interactive_mode():
    """Interactive mode with prompts for user input"""
    print("\n" + "=" * 60)
    print("FACELESS YOUTUBE VIDEO GENERATOR - INTERACTIVE MODE")
    print("=" * 60)
    
    # Show trending topics first
    print("\nWould you like to see trending topic suggestions? (y/n): ", end="")
    show_trends = input().strip().lower()
    if show_trends == 'y':
        get_trending_topics()
    
    # Get topic
    print("\nEnter your video topic: ", end="")
    topic = input().strip()
    if not topic:
        print("Error: Topic is required!")
        return 1
    
    # Get length
    print("Enter video length in minutes (default: 8): ", end="")
    length_input = input().strip()
    length = int(length_input) if length_input else 8
    
    # Get AI provider
    print("Choose AI provider (auto/groq/gemini/ollama, default: auto): ", end="")
    ai_provider = input().strip().lower() or 'auto'
    
    # Get keywords
    print("Enter footage keywords (comma-separated, or press Enter for auto): ", end="")
    keywords_input = input().strip()
    keywords = [k.strip() for k in keywords_input.split(',')] if keywords_input else None
    
    # Run generation
    generator = FacelessVideoGenerator()
    result = generator.run(
        topic=topic,
        length_minutes=length,
        footage_keywords=keywords,
        ai_provider=ai_provider
    )
    
    if result:
        print("\nYour video is ready!")
        print(f"Project directory: {result['project_dir']}")
        return 0
    else:
        print("\nVideo generation failed.")
        return 1


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate faceless YouTube videos automatically',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python master_automation.py --topic "5 AI Tools for Productivity" --length 8
  python master_automation.py --suggest-topics
  python master_automation.py --interactive
  python master_automation.py -t "Investment Tips" -l 10 --ai groq

High CPM Niches (Better Monetization):
  - Finance: $15-$50 CPM
  - Business: $12-$35 CPM
  - Technology: $10-$30 CPM
  - Health: $10-$25 CPM
  - Education: $8-$20 CPM
        """
    )
    parser.add_argument(
        '--topic', '-t',
        help='Video topic'
    )
    parser.add_argument(
        '--length', '-l',
        type=int,
        default=8,
        help='Video length in minutes (default: 8)'
    )
    parser.add_argument(
        '--keywords', '-k',
        nargs='+',
        help='Keywords for stock footage search'
    )
    parser.add_argument(
        '--project', '-p',
        help='Project name (default: auto-generated)'
    )
    parser.add_argument(
        '--ai',
        choices=['auto', 'groq', 'gemini', 'ollama'],
        default='auto',
        help='AI provider for script generation (default: auto)'
    )
    parser.add_argument(
        '--suggest-topics',
        action='store_true',
        help='Show trending topic suggestions with monetization focus'
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode with prompts'
    )
    
    args = parser.parse_args()
    
    # Handle suggest-topics mode
    if args.suggest_topics:
        get_trending_topics()
        return 0
    
    # Handle interactive mode
    if args.interactive:
        return interactive_mode()
    
    # Require topic for normal mode
    if not args.topic:
        parser.print_help()
        print("\nError: --topic is required (or use --interactive or --suggest-topics)")
        return 1
    
    generator = FacelessVideoGenerator(project_name=args.project)
    result = generator.run(
        topic=args.topic,
        length_minutes=args.length,
        footage_keywords=args.keywords,
        ai_provider=args.ai
    )
    
    if result:
        print("\nYour video is ready!")
        print(f"Project directory: {result['project_dir']}")
        return 0
    else:
        print("\nVideo generation failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
