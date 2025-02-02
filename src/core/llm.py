from typing import List, Dict
import openai
from src.config.settings import Settings

class LLMWrapper:
    def __init__(self):
        settings = Settings()
        openai.api_key = settings.OPENAI_API_KEY
        
    async def generate_post(self, news_items: List[Dict], platform: str) -> str:
        """
        Generate a social media post based on news items
        
        Args:
            news_items: List of news items with title, url, and summary
            platform: Target social media platform (e.g., 'linkedin', 'twitter')
            
        Returns:
            str: Generated post content
        """
        prompt = self._create_prompt(news_items, platform)
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional social media content creator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    def _create_prompt(self, news_items: List[Dict], platform: str) -> str:
        """Create a prompt for the LLM based on news items and platform"""
        items_text = "\n".join([
            f"- {item['title']}: {item['summary']}" 
            for item in news_items
        ])
        
        return f"""
        Create a {platform} post summarizing these news items:
        
        {items_text}
        
        Include relevant hashtags and maintain the platform's style.
        For LinkedIn, be professional and insightful.
        For Twitter, be concise and engaging.
        Include URLs where appropriate.
        """ 