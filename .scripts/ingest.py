import os
import re
import shutil

raw_dir = "/Users/engindenizdogu/Desktop/workspace/cuddly-enigma/.raw_sources"
base_dir = "/Users/engindenizdogu/Desktop/workspace/cuddly-enigma"
index_path = os.path.join(base_dir, "INDEX.md")

def clean_summary(body):
    body_text = re.sub(r'#.*?\n', '', body).strip()
    body_text = re.sub(r'\|.*?\|', '', body_text, flags=re.DOTALL)
    body_text = re.sub(r'\s+', ' ', body_text).strip()
    summary = body_text[:100] + "..." if len(body_text) > 100 else body_text
    summary = summary.replace('**', '')
    return summary if summary else "Stub."

def append_to_index(domain, moc_name):
    with open(index_path, 'r') as f:
        content = f.read()
    
    if f"| `/{domain}/` |" in content:
        return # Already exists
        
    new_line = f"| `/{domain}/` | {domain} | [[{moc_name}]] | Auto-ingested domain. |"
    
    with open(index_path, 'a') as f:
        f.write(f"{new_line}\n")

for item in os.listdir(raw_dir):
    item_path = os.path.join(raw_dir, item)
    if item.startswith('.'): continue
    
    if os.path.isdir(item_path):
        domain = item
        dest_folder = os.path.join(base_dir, domain)
        os.makedirs(dest_folder, exist_ok=True)
        
        moc_name = f"{domain} MOC.md"
        moc_path = os.path.join(dest_folder, moc_name)
        
        moc_lines = []
        tags_str = domain.lower().replace(" ", "-")
        
        for filename in os.listdir(item_path):
            if not filename.endswith(".md"): continue
            
            src_file = os.path.join(item_path, filename)
            with open(src_file, 'r') as f:
                content = f.read()
                
            title_match = re.search(r'^---\n(title:\s*(.*?))\n---', content, re.MULTILINE)
            if title_match:
                title = title_match.group(2).strip()
                body = content[title_match.end():]
            else:
                title = filename[:-3]
                body = content
                
            new_fm = f"---\ntitle: {title}\ntags: [{tags_str}]\nreviewed: true\naliases: [{title}]\n---\n"
            
            dest_file = os.path.join(dest_folder, filename)
            with open(dest_file, 'w') as f:
                f.write(new_fm + body)
                
            summary = clean_summary(body)
            moc_lines.append(f"- [[{filename[:-3]}]] - {summary}")
            
        if not os.path.exists(moc_path):
            content = f"---\ntitle: {domain} MOC\ntags: [{tags_str}, moc]\nreviewed: true\naliases: []\n---\n"
            content += f"# {domain} MOC\n\nWelcome to this Map of Content.\n\n## 📚 Notes\n"
        else:
            with open(moc_path, 'r') as f:
                content = f.read()
                
        if "## 📥 To Research" in content:
            parts = content.split("## 📥 To Research")
            content = parts[0] + "\n".join(moc_lines) + "\n\n## 📥 To Research" + parts[1]
        else:
            content += "\n".join(moc_lines) + "\n\n---\n## 📥 To Research / Inbox\n"
            
        with open(moc_path, 'w') as f:
            f.write(content)
            
        append_to_index(domain, moc_name)
        shutil.rmtree(item_path)

print("Automated ingestion complete.")
