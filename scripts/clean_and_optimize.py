import json
import re

def decode_cf(enc):
    r = int(enc[:2], 16)
    return "".join([chr(int(enc[i:i+2], 16) ^ r) for i in range(2, len(enc), 2)])

def clean_cf_emails(html_str):
    if not html_str:
        return html_str
    
    # Pattern 1: <a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="HEX">...</a>
    pattern = r'<a\s+href=["\'](?:/cdn-cgi/l/email-protection)?["\']\s+class=["\']__cf_email__["\']\s+data-cfemail=["\']([0-9a-fA-F]+)["\'][^>]*>.*?</a>'
    
    def repl(match):
        hex_code = match.group(1)
        return decode_cf(hex_code)
    
    cleaned = re.sub(pattern, repl, html_str, flags=re.IGNORECASE)
    
    # Catch any variants where order of attributes is different
    pattern2 = r'<a\s+class=["\']__cf_email__["\']\s+href=["\'][^"\']*["\']\s+data-cfemail=["\']([0-9a-fA-F]+)["\'][^>]*>.*?</a>'
    cleaned = re.sub(pattern2, repl, cleaned, flags=re.IGNORECASE)

    pattern3 = r'<a\s+[^>]*data-cfemail=["\']([0-9a-fA-F]+)["\'][^>]*>.*?</a>'
    cleaned = re.sub(pattern3, repl, cleaned, flags=re.IGNORECASE)

    # In case [email\xa0protected] or [email protected] remained without <a> tag
    cleaned = cleaned.replace("[email\xa0protected]", "you@example.com").replace("[email protected]", "you@example.com")
    return cleaned

def extract_interactive_script(srcdoc):
    if not srcdoc:
        return ""
    
    scripts = re.findall(r"<script>(.*?)</script>", srcdoc, re.DOTALL)
    non_resize_scripts = []
    for s in scripts:
        if "vp-height" in s and "ResizeObserver" in s:
            continue
        cleaned = s.strip()
        if cleaned:
            non_resize_scripts.append(cleaned)
            
    return "\n\n".join(non_resize_scripts)

def main():
    json_path = "data/prompts.json"
    with open(json_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    cf_fixed = 0
    interactive_scripts_count = 0

    for it in items:
        code = it.get("code", "")
        srcdoc = it.get("srcdoc", "")

        # 1. Clean Cloudflare obfuscation
        if "__cf_email__" in code or "email-protection" in code or "[email" in code:
            new_code = clean_cf_emails(code)
            if new_code != code:
                cf_fixed += 1
                it["code"] = new_code

        # 2. Extract script from srcdoc
        script = extract_interactive_script(srcdoc)
        if script:
            # Also clean any cf emails inside script if any
            it["script"] = clean_cf_emails(script)
            interactive_scripts_count += 1
        else:
            it["script"] = ""

        # 3. Remove redundant srcdoc field to shrink JSON size
        if "srcdoc" in it:
            del it["srcdoc"]

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print(f"✅ Processed {len(items)} items:")
    print(f" - Fixed Cloudflare email obfuscation in {cf_fixed} snippets")
    print(f" - Extracted interactive scripts in {interactive_scripts_count} snippets")
    print(f" - Removed redundant 'srcdoc' field to optimize bundle size")

if __name__ == "__main__":
    main()
