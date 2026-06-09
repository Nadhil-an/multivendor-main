import os
import re

static_dir = r'c:\Users\NADIL\OneDrive\Desktop\deployment-project\multivendor-main\foodonline_main\foodonline_main\static'

for root, dirs, files in os.walk(static_dir):
    for file in files:
        if file.endswith('.css'):
            css_path = os.path.join(root, file)
            with open(css_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            urls = re.findall(r'url\((.*?)\)', content)
            for u in urls:
                u = u.strip('\'" \n\r\t')
                if u.startswith('data:') or u.startswith('http'):
                    continue
                
                u_clean = u.split('?')[0].split('#')[0]
                if not u_clean:
                    continue
                
                p = os.path.normpath(os.path.join(root, u_clean))
                if not os.path.exists(p):
                    os.makedirs(os.path.dirname(p), exist_ok=True)
                    open(p, 'a').close()
                    print(f"Created dummy file: {p}")
