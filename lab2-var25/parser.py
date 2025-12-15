import re
import json
from typing import List
from bs4 import BeautifulSoup


def parse_audio_urls_from_html(html_content: str, base_url: str = "https://mixkit.co") -> List[str]:
    """Парсит аудио URL из HTML содержимого."""
    all_audio_urls: List[str] = []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    try:
        script_tags = soup.find_all('script', type='application/ld+json')
        for script in script_tags:
            try:
                data = json.loads(script.string)
                def find_urls(obj):
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            if isinstance(value, str) and value.endswith('.mp3'):
                                if value.startswith('//'):
                                    value = 'https:' + value
                                elif value.startswith('/'):
                                    value = base_url + value
                                all_audio_urls.append(value)
                            elif isinstance(value, (dict, list)):
                                find_urls(value)
                    elif isinstance(obj, list):
                        for item in obj:
                            find_urls(item)
                
                find_urls(data)
            except:
                pass
        
        script_tags = soup.find_all('script')
        for script in script_tags:
            if script.string:
                content = script.string
                patterns = [
                    r'https?://[^"\'\s<>]+?\.mp3',
                    r'"url"\s*:\s*"([^"]+?\.mp3)"',
                    r"'url'\s*:\s*'([^']+?\.mp3)'",
                    r'audio-src="([^"]+)"',
                    r"audio-src='([^']+)'",
                    r'src="([^"]+?\.mp3)"',
                    r"src='([^']+?\.mp3)'"
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        url = match if isinstance(match, str) else match[0] if match else None
                        if url and '.mp3' in url.lower():
                            if url.startswith('//'):
                                url = 'https:' + url
                            elif url.startswith('/'):
                                url = base_url + url
                            if url.startswith('http'):
                                all_audio_urls.append(url)
        
        for tag in soup.find_all(True):  
            for attr_name, attr_value in tag.attrs.items():
                if isinstance(attr_value, str) and '.mp3' in attr_value.lower():
                    if attr_value.startswith('//'):
                        attr_value = 'https:' + attr_value
                    elif attr_value.startswith('/'):
                        attr_value = base_url + attr_value
                    if attr_value.startswith('http'):
                        all_audio_urls.append(attr_value)
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '.mp3' in href.lower():
                if href.startswith('//'):
                    href = 'https:' + href
                elif href.startswith('/'):
                    href = base_url + href
                if href.startswith('http'):
                    all_audio_urls.append(href)
        
        for source in soup.find_all('source', src=True):
            src = source['src']
            if '.mp3' in src.lower():
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = base_url + src
                if src.startswith('http'):
                    all_audio_urls.append(src)
                    
    except Exception as e:
        print(f"Ошибка при парсинге: {e}")
    
    all_audio_urls = list(set(all_audio_urls))
    valid_audio_urls = [
        url for url in all_audio_urls 
        if url.startswith('http') and '.mp3' in url.lower()
    ]
    
    return valid_audio_urls