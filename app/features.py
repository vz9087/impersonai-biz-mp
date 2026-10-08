import re
import tldextract
from urllib.parse import urlparse
import Levenshtein

def extract_features(url, reference_domain=None):
    """Extract lexical features from URL"""
    features = {}
    
    parsed = urlparse(url if url.startswith('http') else f'http://{url}')
    domain = parsed.netloc or parsed.path.split('/')[0]
    ext = tldextract.extract(domain)
    
    features['url_length'] = len(url)
    features['domain_length'] = len(domain)
    features['path_length'] = len(parsed.path)
    features['query_length'] = len(parsed.query)
    
    features['count_digits'] = sum(c.isdigit() for c in url)
    features['count_letters'] = sum(c.isalpha() for c in url)
    features['count_special'] = len(re.findall(r'[^a-zA-Z0-9]', url))
    features['count_dots'] = url.count('.')
    features['count_hyphens'] = url.count('-')
    features['count_underscores'] = url.count('_')
    features['count_at'] = url.count('@')
    features['count_question'] = url.count('?')
    features['count_percent'] = url.count('%')
    features['count_slash'] = url.count('/')
    
    features['subdomain_count'] = len(ext.subdomain.split('.')) if ext.subdomain else 0
    features['tld_length'] = len(ext.suffix) if ext.suffix else 0
    features['has_www'] = 1 if 'www' in domain else 0
    features['has_ip'] = 1 if re.match(r'\d+\.\d+\.\d+\.\d+', domain) else 0
    features['has_https'] = 1 if url.startswith('https') else 0
    
    suspicious_tlds = ['tk', 'ml', 'ga', 'cf', 'gq', 'xyz', 'top', 'work', 'click']
    features['suspicious_tld'] = 1 if ext.suffix in suspicious_tlds else 0
    
    features['digit_ratio'] = features['count_digits'] / max(len(url), 1)
    
    if reference_domain:
        features['levenshtein_dist'] = Levenshtein.distance(domain, reference_domain)
        features['similarity_ratio'] = Levenshtein.ratio(domain, reference_domain)
    else:
        features['levenshtein_dist'] = 0
        features['similarity_ratio'] = 0
    
    return features