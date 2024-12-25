import os
import re
import time
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tqdm import tqdm
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

class AIScraper:
    def __init__(self):
        """Initialize the AI-powered web scraper."""
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.user_agent = UserAgent()
        self.rate_limit = float(os.getenv('MAX_REQUESTS_PER_SECOND', 2))
        self.timeout = int(os.getenv('TIMEOUT_SECONDS', 30))
        self.last_request_time = 0
        self.google_api_key = os.getenv('CUSTOM_SEARCH_API_KEY')
        self.search_engine_id = os.getenv('SEARCH_ENGINE_ID')
        
    def search_web(self, query: str, max_results: int = 5) -> List[str]:
        """
        Search the web using Google Custom Search API.
        
        Args:
            query: Natural language search query
            max_results: Maximum number of results to return (default: 5)
            
        Returns:
            List of URLs from search results
        """
        if not self.google_api_key or not self.search_engine_id:
            raise ValueError("Google Custom Search API key and Search Engine ID are required")
            
        base_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': self.google_api_key,
            'cx': self.search_engine_id,
            'q': query,
            'num': min(max_results, 10)  # API limit is 10 results per query
        }
        
        try:
            response = requests.get(base_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            search_results = response.json()
            
            if 'items' not in search_results:
                return []
                
            return [item['link'] for item in search_results['items']]
        except Exception as e:
            print(f"Error performing Google search: {str(e)}")
            return []
        
    def _respect_rate_limit(self):
        """Ensure we don't exceed the rate limit."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < (1 / self.rate_limit):
            time.sleep((1 / self.rate_limit) - time_since_last_request)
        self.last_request_time = time.time()

    def get_page_content(self, url: str) -> Optional[str]:
        """
        Fetch the content of a webpage while respecting rate limits.
        
        Args:
            url: The URL to scrape
            
        Returns:
            The page content as string if successful, None otherwise
        """
        self._respect_rate_limit()
        
        headers = {'User-Agent': self.user_agent.random}
        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None

    def extract_emails(self, text: str) -> List[str]:
        """
        Extract email addresses from text using regex.
        
        Args:
            text: The text to search for emails
            
        Returns:
            List of found email addresses
        """
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return list(set(re.findall(email_pattern, text)))

    def analyze_with_ai(self, content: str, prompt: str) -> Dict:
        """
        Use OpenAI's API to analyze the content.
        
        Args:
            content: The content to analyze
            prompt: The prompt for the AI
            
        Returns:
            Dictionary containing AI's analysis
        """
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes web content."},
                    {"role": "user", "content": f"{prompt}\n\nContent: {content[:4000]}"}  # Truncate to avoid token limits
                ]
            )
            return {"success": True, "analysis": response.choices[0].message.content}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def scrape_website(self, url: str, ai_prompt: str) -> Dict:
        """
        Scrape a website and analyze its content.
        
        Args:
            url: The URL to scrape
            ai_prompt: The prompt for AI analysis
            
        Returns:
            Dictionary containing scraped data and analysis
        """
        content = self.get_page_content(url)
        if not content:
            return {"success": False, "error": "Failed to fetch content"}

        soup = BeautifulSoup(content, 'html.parser')
        text_content = soup.get_text()
        
        emails = self.extract_emails(content)
        ai_analysis = self.analyze_with_ai(text_content, ai_prompt)

        return {
            "success": True,
            "url": url,
            "emails": emails,
            "ai_analysis": ai_analysis.get("analysis") if ai_analysis["success"] else None
        }

    def search_and_analyze(self, search_query: str, ai_prompt: str, max_results: int = 5) -> pd.DataFrame:
        """
        Search the web and analyze the results.
        
        Args:
            search_query: Natural language search query
            ai_prompt: Prompt for AI analysis
            max_results: Maximum number of results to process
            
        Returns:
            DataFrame containing analysis of search results
        """
        # First, get URLs from Google Custom Search
        urls = self.search_web(search_query, max_results)
        if not urls:
            print("No search results found")
            return pd.DataFrame()
            
        # Then analyze each URL
        return self.bulk_scrape(urls, ai_prompt)

    def bulk_scrape(self, urls: List[str], ai_prompt: str) -> pd.DataFrame:
        """
        Scrape multiple websites and compile results into a DataFrame.
        
        Args:
            urls: List of URLs to scrape
            ai_prompt: The prompt for AI analysis
            
        Returns:
            DataFrame containing all scraped data
        """
        results = []
        for url in tqdm(urls, desc="Scraping websites"):
            result = self.scrape_website(url, ai_prompt)
            if result["success"]:
                results.append(result)

        df = pd.DataFrame(results)
        
        # Save to CSV
        output_dir = os.getenv('OUTPUT_DIR', 'output')
        os.makedirs(output_dir, exist_ok=True)
        csv_path = os.path.join(output_dir, os.getenv('CSV_FILENAME', 'scraped_data.csv'))
        df.to_csv(csv_path, index=False)
        
        return df 