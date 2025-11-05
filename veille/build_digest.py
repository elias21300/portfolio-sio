import feedparser
from datetime import datetime
from jinja2 import Template
from pathlib import Path

# --- Sources de ta veille ---
SOURCES = {
    "Développez.com (Réseaux)": "https://reseau.developpez.com/index/rss",
    "Le Monde Informatique": "https://www.lemondeinformatique.fr/actualites-rss.xml",
    "ZDNet Sécurité": "https://www.zdnet.fr/feeds/rss/actualites/securite/",
    "CERT-FR": "https://www.cert.ssi.gouv.fr/feed/",
    "LinuxFr.org": "https://linuxfr.org/news.atom",
    "Blog Cisco": "https://blogs.cisco.com/feed",
    "Docker Blog": "https://www.docker.com/blog/feed/",
    "Ansible Blog": "https://www.ansible.com/blog/rss.xml",
    "Fortinet Blog": "https://www.fortinet.com/blog/rss"
}

# --- Chemins ---
BASE_DIR = Path(__file__).parent
DIGEST_DIR = BASE_DIR / "digest"
DIGEST_DIR.mkdir(exist_ok=True)

# --- Récupération des flux ---
items = []
for name, url in SOURCES.items():
    feed = feedparser.parse(url)
    for entry in feed.entries[:5]:
        items.append({
            "source": name,
            "title": entry.get("title", "Sans titre"),
            "link": entry.get("link", "#"),
            "published": entry.get("published", "Non daté")
        })

# --- Génération HTML avec Jinja2 ---
template = Template(open(BASE_DIR / "template.html", encoding="utf-8").read())
html_output = template.render(
    date=datetime.now().strftime("%d/%m/%Y"),
    articles=items
)

# --- Sauvegarde du digest ---
filename = DIGEST_DIR / f"digest-{datetime.now().strftime('%Y%m%d')}.html"
filename.write_text(html_output, encoding="utf-8")

# --- Mise à jour du index.html ---
index_path = BASE_DIR / "index.html"
links = [
    f"<li><a href='digest/{p.name}'>{p.stem.replace('digest-', 'Veille du ')}</a></li>"
    for p in sorted(DIGEST_DIR.glob('*.html'), reverse=True)
]
index_html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Veille SISR</title>
  <link rel="stylesheet" href="https://cdn.simplecss.org/simple.css">
</head>
<body>
  <h1>Veille Technologique SISR</h1>
  <p>Actualités automatisées — dernière mise à jour : {datetime.now().strftime("%d/%m/%Y")}</p>
  <ul>{''.join(links)}</ul>
  <p><a href="/">⬅ Retour au portfolio</a></p>
</body>
</html>
"""
index_path.write_text(index_html, encoding="utf-8")

print(f"✅ Digest généré : {filename}")
