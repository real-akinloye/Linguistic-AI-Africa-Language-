#!/usr/bin/env python3
# NO TRIBALISM I'M DOING FOR ALL LANG WITH SAME PROCESS
"""
Yoruba Data Collection Toolkit
A comprehensive toolkit for collecting Yoruba text data from various sources
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from urllib.parse import urljoin, urlparse
import re
from pathlib import Path
import logging
from typing import List, Dict, Optional
import feedparser
import tweepy  # You'll need to install and configure
from selenium import webdriver
from selenium.webdriver.common.by import By
import wikipedia

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YorubaDataCollector:
    def __init__(self, output_dir: str = "yoruba_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def collect_bbc_yoruba(self) -> List[Dict]:
        """Collect articles from BBC Yoruba"""
        articles = []
        base_url = "https://www.bbc.com/yoruba"
        
        try:
            response = self.session.get(base_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find article links (adjust selectors based on current BBC structure)
            article_links = soup.find_all('a', href=True)
            
            for link in article_links[:50]:  # Limit to first 50
                if '/yoruba/' in link['href']:
                    article_url = urljoin(base_url, link['href'])
                    article_data = self._scrape_bbc_article(article_url)
                    if article_data:
                        articles.append(article_data)
                    time.sleep(1)  # Be respectful
                    
        except Exception as e:
            logger.error(f"Error collecting BBC Yoruba: {e}")
            
        return articles
    
    def _scrape_bbc_article(self, url: str) -> Optional[Dict]:
        """Scrape individual BBC Yoruba article"""
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract article content (adjust selectors as needed)
            title = soup.find('h1')
            title_text = title.get_text().strip() if title else ""
            
            # Find main content area
            content_div = soup.find('div', {'data-component': 'text-block'}) or \
                         soup.find('div', class_='story-body__inner') or \
                         soup.find('article')
            
            content = ""
            if content_div:
                paragraphs = content_div.find_all('p')
                content = "\n".join([p.get_text().strip() for p in paragraphs])
            
            if title_text and content:
                return {
                    'source': 'BBC Yoruba',
                    'url': url,
                    'title': title_text,
                    'content': content,
                    'date_collected': pd.Timestamp.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error scraping BBC article {url}: {e}")
            
        return None
    
    def collect_voa_yoruba(self) -> List[Dict]:
        """Collect articles from VOA Yoruba"""
        articles = []
        base_url = "https://www.voaafrica.com/z/3273"  # VOA Yoruba section
        
        try:
            response = self.session.get(base_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find article links
            article_links = soup.find_all('a', href=True)
            
            for link in article_links[:50]:
                if any(keyword in link.get('href', '') for keyword in ['/a/', '/episode/']):
                    article_url = urljoin(base_url, link['href'])
                    article_data = self._scrape_voa_article(article_url)
                    if article_data:
                        articles.append(article_data)
                    time.sleep(1)
                    
        except Exception as e:
            logger.error(f"Error collecting VOA Yoruba: {e}")
            
        return articles
    
    def _scrape_voa_article(self, url: str) -> Optional[Dict]:
        """Scrape individual VOA Yoruba article"""
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.find('h1', class_='title')
            title_text = title.get_text().strip() if title else ""
            
            content_div = soup.find('div', class_='entry-content') or \
                         soup.find('div', class_='content')
            
            content = ""
            if content_div:
                paragraphs = content_div.find_all('p')
                content = "\n".join([p.get_text().strip() for p in paragraphs])
            
            if title_text and content:
                return {
                    'source': 'VOA Yoruba',
                    'url': url,
                    'title': title_text,
                    'content': content,
                    'date_collected': pd.Timestamp.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error scraping VOA article {url}: {e}")
            
        return None
    
    def collect_wikipedia_yoruba(self) -> List[Dict]:
        """Collect articles from Yoruba Wikipedia"""
        articles = []
        
        try:
            # Set Wikipedia to Yoruba
            wikipedia.set_lang("yo")
            
            # Get random articles
            random_titles = wikipedia.random(50)
            
            for title in random_titles:
                try:
                    page = wikipedia.page(title)
                    articles.append({
                        'source': 'Wikipedia Yoruba',
                        'url': page.url,
                        'title': page.title,
                        'content': page.content,
                        'date_collected': pd.Timestamp.now().isoformat()
                    })
                    time.sleep(0.5)
                except Exception as e:
                    logger.warning(f"Error getting Wikipedia page {title}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error collecting Wikipedia Yoruba: {e}")
            
        return articles
    
    def collect_yoruba_proverbs(self) -> List[Dict]:
        """Collect Yoruba proverbs from various sources"""
        proverbs = []
        
        # Sample proverbs - you'd expand this with more sources
        sample_proverbs = [
            "Ẹni tí ó bá ní ìyá ní ó mọ iye òkúta.",
            "Bí a bá ń gun igi tí ó ga, a ó rí àwọn ẹyẹ tí ó wà lókè.",
            "Ẹni tí ó bá fẹ́ lọ sí ọjà Ìbàdàn, kò gbọdọ̀ fohùn kálẹ̀.",
            # Add more proverbs here
        ]
        
        for proverb in sample_proverbs:
            proverbs.append({
                'source': 'Traditional Proverbs',
                'type': 'proverb',
                'text': proverb,
                'date_collected': pd.Timestamp.now().isoformat()
            })
            
        return proverbs
    
    def collect_social_media_data(self):
        """
        Placeholder for social media collection
        Note: Requires proper API keys and follows platform ToS
        """
        # Twitter/X API would require authentication
        # Facebook would require Graph API access
        # This is just a framework
        
        logger.warning("Social media collection requires API keys and proper authentication")
        return []
    
    def collect_bible_yoruba(self) -> List[Dict]:
        """Collect Yoruba Bible text"""
        bible_texts = []
        
        # Bible Gateway or similar sources would need to be accessed respectfully
        # This is a placeholder showing the structure
        
        sample_verses = [
            {
                'book': 'Genesis',
                'chapter': 1,
                'verse': 1,
                'text': 'Ní ìbẹ̀rẹ̀ ni Ọlọ́run dá ọ̀run àti ayé.'
            },
            # Add more verses
        ]
        
        for verse in sample_verses:
            bible_texts.append({
                'source': 'Bible (Yoruba)',
                'book': verse['book'],
                'chapter': verse['chapter'],
                'verse': verse['verse'],
                'text': verse['text'],
                'date_collected': pd.Timestamp.now().isoformat()
            })
            
        return bible_texts
    
    def save_data(self, data: List[Dict], filename: str):
        """Save collected data to file"""
        if not data:
            logger.warning(f"No data to save for {filename}")
            return
            
        # Save as JSON
        json_path = self.output_dir / f"{filename}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # Save as CSV
        csv_path = self.output_dir / f"{filename}.csv"
        df = pd.DataFrame(data)
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        logger.info(f"Saved {len(data)} records to {json_path} and {csv_path}")
    
    def clean_text(self, text: str) -> str:
        """Basic text cleaning for Yoruba text"""
        if not text:
            return ""
            
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove unwanted characters but preserve Yoruba diacritics
        text = re.sub(r'[^\w\s\.,!?;:\'\"\-àáèéẹ́ẹ̀ìíòóọ́ọ̀ùúṣ]', '', text)
        
        return text.strip()
    
    def run_full_collection(self):
        """Run complete data collection process"""
        logger.info("Starting Yoruba data collection...")
        
        # Collect from various sources
        collections = [
            ("bbc_yoruba", self.collect_bbc_yoruba),
            ("voa_yoruba", self.collect_voa_yoruba),
            ("wikipedia_yoruba", self.collect_wikipedia_yoruba),
            ("yoruba_proverbs", self.collect_yoruba_proverbs),
            ("bible_yoruba", self.collect_bible_yoruba),
        ]
        
        for name, collector_func in collections:
            logger.info(f"Collecting {name}...")
            try:
                data = collector_func()
                if data:
                    # Clean the text data
                    for item in data:
                        if 'content' in item:
                            item['content'] = self.clean_text(item['content'])
                        if 'text' in item:
                            item['text'] = self.clean_text(item['text'])
                    
                    self.save_data(data, name)
                else:
                    logger.warning(f"No data collected for {name}")
            except Exception as e:
                logger.error(f"Error in {name} collection: {e}")
        
        logger.info("Data collection completed!")

# Usage example and setup instructions
def main():
    """Main function with usage examples"""
    
    print("""
    Yoruba Data Collection Toolkit
    ==============================
    
    IMPORTANT LEGAL AND ETHICAL CONSIDERATIONS:
    
    1. RESPECT ROBOTS.TXT: Always check site's robots.txt file
    2. RATE LIMITING: Don't overload servers (use delays)
    3. TERMS OF SERVICE: Review and comply with website ToS
    4. COPYRIGHT: Ensure data usage complies with copyright laws
    5. ATTRIBUTION: Credit sources appropriately
    6. PRIVACY: Respect user privacy in social media data
    
    SETUP REQUIREMENTS:
    
    1. Install dependencies:
       pip install requests beautifulsoup4 pandas feedparser tweepy selenium wikipedia
    
    2. For social media APIs:
       - Twitter: Get API keys from developer.twitter.com
       - Facebook: Get Graph API access
    
    3. For browser automation (if needed):
       - Install ChromeDriver for Selenium
    
    USAGE:
    collector = YorubaDataCollector()
    collector.run_full_collection()
    """)
    
    # Initialize and run collector
    collector = YorubaDataCollector()
    
    # Run specific collections or full collection
    # collector.run_full_collection()
    
    # Or run individual collections:
    # bbc_data = collector.collect_bbc_yoruba()
    # collector.save_data(bbc_data, "bbc_test")

if __name__ == "__main__":
    main()

# Additional utility functions for data processing

def merge_datasets(data_dir: str = "yoruba_data") -> pd.DataFrame:
    """Merge all collected datasets into one master dataset"""
    data_path = Path(data_dir)
    all_data = []
    
    for json_file in data_path.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_data.extend(data)
    
    df = pd.DataFrame(all_data)
    
    # Add metadata
    df['text_length'] = df.apply(lambda x: len(x.get('content', '') + x.get('text', '')), axis=1)
    df['has_diacritics'] = df.apply(lambda x: bool(re.search(r'[àáèéẹ́ẹ̀ìíòóọ́ọ̀ùúṣ]', 
                                                            x.get('content', '') + x.get('text', ''))), axis=1)
    
    return df

def analyze_corpus_stats(df: pd.DataFrame):
    """Analyze corpus statistics"""
    print("Yoruba Corpus Statistics")
    print("=" * 30)
    print(f"Total documents: {len(df)}")
    print(f"Total words (approx): {df['text_length'].sum() // 5}")  # Rough estimate
    print(f"Documents with diacritics: {df['has_diacritics'].sum()} ({df['has_diacritics'].mean()*100:.1f}%)")
    print(f"Sources: {df['source'].value_counts().to_dict()}")
    print(f"Average document length: {df['text_length'].mean():.0f} characters")

# Example diacritic restoration function
def restore_diacritics_simple(text: str) -> str:
    """
    Simple diacritic restoration using common patterns
    This is a basic implementation - you'd want more sophisticated methods
    """
    # Common word mappings (expand this significantly)
    diacritic_map = {
        'eni': 'ẹni',
        'eyi': 'èyí',
        'fun': 'fún',
        'wa': 'wá',
        'lo': 'lọ',
        'se': 'ṣe',
        'si': 'sí',
        'ni': 'ní',
        'ti': 'tí',
        'ko': 'kò',
        'ba': 'bá',
        'mo': 'mọ',
        'ro': 'rò',
        'bi': 'bí',
        'pe': 'pé',
        'je': 'jẹ',
        # Add hundreds more mappings
    }
    
    words = text.split()
    restored_words = []
    
    for word in words:
        # Clean word (remove punctuation for lookup)
        clean_word = re.sub(r'[^\w]', '', word.lower())
        
        if clean_word in diacritic_map:
            # Replace while preserving case and punctuation
            restored = word.replace(clean_word, diacritic_map[clean_word])
            restored_words.append(restored)
        else:
            restored_words.append(word)
    
    return ' '.join(restored_words)
