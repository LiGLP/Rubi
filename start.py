import re
import time
import os

class RubiInterpreter:
    def __init__(self):
        self.running = True
        
        self.token_spec = [
            ('KEYWORD',    r'\b(title|type|cmd|timeout|closescript)\b'),
            ('PAREN_L',    r'\('),
            ('PAREN_R',    r'\)'),
            ('COLON',      r':'),
            ('VALUE',      r'[^():\n]+'), 
            ('NEWLINE',    r'\n'),
            ('SKIP',       r'[ \t]+'),
        ]
        self.tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_spec)

    def run(self, filename):
        if not os.path.exists(filename):
            print(f"Fehler: '{filename}' nicht gefunden.")
            return

        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        i = 0
        while i < len(lines) and self.running:
            line = lines[i].strip()
            
            # TITLE
            if line.startswith("title:"):
                title_text = line.split(":", 1)[1].strip()
                if os.name == 'nt': os.system(f"title {title_text}")
                i += 1

            # TIMEOUT
            elif line.startswith("timeout"):
                ms = int(re.search(r'\((.*?)\)', line).group(1).replace('ms', ''))
                time.sleep(ms / 1000.0)
                i += 1

            # CMD(WRITE) mit ( ) Block
            elif line.startswith("cmd(write):"):
                i += 1
                block_content = []
                
                while i < len(lines) and lines[i].strip() != ")":
                    content = lines[i].rstrip() 
                    
                    if "(leerzeile)" in content.lower():
                        block_content.append("")
                    else:
                        block_content.append(content)
                    i += 1
                
                print("\n".join(block_content))
                i += 1 

            # CMD(PAUSE)
            elif "cmd(pause)" in line:
                input("\n[PAUSE] Drücke Enter...")
                i += 1

            # CLOSESCRIPT
            elif "closescript" in line:
                self.running = False
                break
            
            else:
                i += 1

if __name__ == "__main__":
    print("--- RUBI DEBUGGER ---")
    datei = input("Datei: ").strip()
    if not datei.endswith('.rubi'): datei += ".rubi"
    
    RubiInterpreter().run(datei)