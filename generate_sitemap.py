

import os
from datetime import datetime
from urllib.parse import quote

# ==================== НАСТРОЙКИ ====================
BASE_DIR = "d:/work/github/ai-news"  # Путь к корневой директории сайта
BASE_URL = "https://omogr.github.io"   # Базовый URL вашего сайта

SITEMAP_FILE = "sitemap.xml"
HTML_EXTENSIONS = {'.html', '.htm'}
DEFAULT_PRIORITY = "0.5"
DEFAULT_CHANGEFREQ = "monthly"
# ==================================================

def get_last_mod_date(filepath):
    """Получение даты последней модификации файла."""
    timestamp = os.path.getmtime(filepath)
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S+00:00')

def get_url_path(root, filename, base_dir):
    """Формирование относительного URL пути из файловой системы."""
    relative_path = os.path.relpath(os.path.join(root, filename), base_dir)
    url_path = relative_path.replace(os.sep, '/')
    
    # Обработка index-файлов
    if url_path.endswith(('index.html', 'index.htm')):
        url_path = os.path.dirname(url_path)
        if url_path == '':
            url_path = '/'
        else:
            url_path = '/' + url_path + '/'
    else:
        # Удаляем расширение
        for ext in HTML_EXTENSIONS:
            if url_path.endswith(ext):
                url_path = url_path[:-len(ext)]
                break
        # Добавляем ведущий слеш
        if not url_path.startswith('/'):
            url_path = '/' + url_path
    
    # Кодируем специальные символы
    return quote(url_path, safe='/:@!$&\'()*+,;=')

def generate_sitemap(base_dir, base_url, output_file):
    """Генерация sitemap.xml."""
    urls = []
    
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for filename in files:
            if any(filename.lower().endswith(ext) for ext in HTML_EXTENSIONS):
                filepath = os.path.join(root, filename)
                url_path = get_url_path(root, filename, base_dir)
                
                # ВОТ ЭТА СТРОКА ИСПРАВЛЕНА
                full_url = f"{base_url.rstrip('/')}/{url_path.lstrip('/')}"
                
                lastmod = get_last_mod_date(filepath)
                depth = url_path.count('/') - 1
                priority = max(0.1, float(DEFAULT_PRIORITY) - depth * 0.1)
                
                if 'yandex_1523a6f7ab9df206' in full_url:
                    continue
                if 'googleeaa269f218e1c5fa' in full_url:
                    continue
                if 'omogr.github.io/articles' in full_url:
                    continue
                changefreq = DEFAULT_CHANGEFREQ
                if 'omogr.github.io/pages' in full_url:
                    priority = 0.8
                if 'https://omogr.github.io/' == full_url:
                    priority = 0.9
                    changefreq = 'daily'
                urls.append({
                    'loc': full_url,
                    'lastmod': lastmod,
                    'changefreq': changefreq,
                    'priority': f"{priority:.1f}"
                })
    
    # Сортировка: главная страница первой
    urls.sort(key=lambda x: (x['loc'].count('/'), x['loc']))
    if urls and urls[0]['loc'].endswith('//'):
        urls[0]['loc'] = urls[0]['loc'].rstrip('/') + '/'
    
    # Генерация XML
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{url["loc"]}</loc>\n'
        xml_content += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
        xml_content += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml_content += f'    <priority>{url["priority"]}</priority>\n'
        xml_content += '  </url>\n'
    
    xml_content += '</urlset>\n'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    return len(urls)

def main():
    try:
        print(f"🔍 Сканирование директории: {BASE_DIR}")
        count = generate_sitemap(BASE_DIR, BASE_URL, SITEMAP_FILE)
        print(f"✅ Готово! Сгенерировано {count} URL")
        print(f"💾 Sitemap сохранен в: {os.path.abspath(SITEMAP_FILE)}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        exit(1)

if __name__ == "__main__":
    main()
    