import random
import string
import pandas as pd

random.seed(42)

# Expanded brand list
brands = [
    'google.com', 'paypal.com', 'amazon.com', 'microsoft.com', 'apple.com',
    'facebook.com', 'netflix.com', 'instagram.com', 'linkedin.com', 'github.com',
    'dropbox.com', 'twitter.com', 'whatsapp.com', 'youtube.com', 'wikipedia.org',
    'yahoo.com', 'reddit.com', 'pinterest.com', 'spotify.com',
    'adobe.com', 'oracle.com', 'ibm.com', 'intel.com', 'nvidia.com',
    'bankofamerica.com', 'wellsfargo.com', 'chase.com', 'citibank.com', 'hsbc.com',
    'walmart.com', 'target.com', 'bestbuy.com', 'costco.com', 'ebay.com',
    'airbnb.com', 'uber.com', 'lyft.com', 'doordash.com', 'instacart.com',
]

def random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_typo_variants(domain, count=30):
    """Generate diverse typosquatting patterns"""
    name = domain.split('.')[0]
    tld = domain.split('.')[-1]
    variants = set()

    # 1. Character substitution
    subs = {'o': '0', 'i': '1', 'l': '1', 'e': '3', 'a': '@', 's': '5', 'g': '9'}
    for i, c in enumerate(name):
        if c in subs:
            variants.add(name[:i] + subs[c] + name[i+1:] + '.' + tld)

    # 2. Character deletion
    for i in range(len(name)):
        variants.add(name[:i] + name[i+1:] + '.' + tld)

    # 3. Character insertion
    for i in range(len(name) + 1):
        variants.add(name[:i] + random.choice(string.ascii_lowercase) + name[i:] + '.' + tld)

    # 4. Adjacent character swap
    for i in range(len(name) - 1):
        variants.add(name[:i] + name[i+1] + name[i] + name[i+2:] + '.' + tld)

    # 5. Character doubling
    for i in range(len(name)):
        variants.add(name[:i] + name[i] + name[i:] + '.' + tld)

    # 6. Homoglyph substitutions
    homoglyphs = {'m': 'rn', 'n': 'm', 'u': 'v', 'v': 'u', 'w': 'vv', 'b': 'h', 'h': 'b'}
    for i, c in enumerate(name):
        if c in homoglyphs:
            variants.add(name[:i] + homoglyphs[c] + name[i+1:] + '.' + tld)

    # 7. Suspicious affixes
    affixes = ['secure', 'login', 'verify', 'account', 'update', 'support',
               'auth', 'signin', 'help', 'service', 'official', 'customer']
    for affix in affixes:
        variants.add(f"{name}-{affix}.{tld}")
        variants.add(f"{name}{affix}.{tld}")
        variants.add(f"{affix}-{name}.{tld}")

    # 8. Suspicious TLD swaps
    alt_tlds = ['tk', 'xyz', 'top']
    for alt in alt_tlds:
        variants.add(f"{name}.{alt}")

    # 9. Subdomain tricks
    variants.add(f"{name}.{random_string(6)}.com")
    variants.add(f"{random_string(4)}.{name}.com")
    variants.add(f"{name}-{random_string(5)}.com")

    # 10. Random extra letters
    for _ in range(5):
        pos = random.randint(0, len(name))
        variants.add(name[:pos] + random_string(1) + name[pos:] + '.' + tld)

    random.shuffle(list(variants))  # not needed since set
    return list(variants)[:count]

def generate_legit_variants(domain, count=30):
    """Generate legitimate-looking domain variations"""
    name = domain.split('.')[0]
    variants = set()

    # 1. With www
    variants.add(f"www.{domain}")

    # 2. Subdomains
    subdomains = ['mail', 'blog', 'shop', 'store', 'api', 'dev', 'support',
                  'help', 'docs', 'news', 'careers', 'about', 'login', 'auth']
    for sub in subdomains:
        variants.add(f"{sub}.{domain}")

    # 3. Paths
    paths = ['/about', '/contact', '/products', '/services', '/blog',
             '/news', '/help', '/faq', '/terms', '/privacy']
    for path in paths:
        variants.add(f"{domain}{path}")

    # 4. Country TLDs
    country_tlds = ['co.uk', 'co.in', 'com.au', 'de', 'fr', 'jp', 'ca']
    for ctld in country_tlds:
        variants.add(f"{name}.{ctld}")

    # 5. Common legit patterns
    variants.add(f"{name}shop.com")
    variants.add(f"my{name}.com")
    variants.add(f"{name}app.com")
    variants.add(f"{name}inc.com")
    variants.add(f"{name}labs.com")

    # 6. Longer legitimate-looking domains
    legit_extra = [
        'example.com', 'testsite.com', 'mycompany.org', 'business.net',
        'stackoverflow.com', 'medium.com', 'quora.com'
    ]
    variants.update(legit_extra)

    return list(variants)[:count]

# Generate data
data = []

for brand in brands:
    # Legitimate samples
    legit_variants = generate_legit_variants(brand, count=22)
    for variant in legit_variants:
        data.append({'url': f"https://{variant}", 'label': 0})
        data.append({'url': f"http://{variant}", 'label': 0})

    # Malicious samples
    typo_variants = generate_typo_variants(brand, count=35)
    for variant in typo_variants:
        scheme = random.choice(['http://', 'https://'])
        data.append({'url': f"{scheme}{variant}", 'label': 1})

# Shuffle and save
df = pd.DataFrame(data)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv('data/training_data.csv', index=False)

print(f"Total samples: {len(df)}")
print(f"Legitimate:    {len(df[df['label']==0])}")
print(f"Malicious:     {len(df[df['label']==1])}")
print(f"Ratio:         {len(df[df['label']==0]) / len(df) * 100:.1f}% legit")