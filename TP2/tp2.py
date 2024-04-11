import sys
import re
import functools

##################################    BASIC FUNCTIONS    ##################################

##### Headers

def convert_header(text):
    pattern = re.compile(r'^[ ]{0,3}(#{1,6})(?:[ ]+(.*)|\n)$', re.MULTILINE)
    # re.MULTILINE is needed to match the start of each line, since we're passing the whole text at once
    def replace(match):
        level = len(match.group(1))
        content = match.group(2) if match.group(2) else ""
        return f"<h{level}>{content}</h{level}>"
    
    return re.sub(pattern, replace, text)

##### Bold

def convert_bold(text):
    pattern = r'(\*\*|__)([^*_].+?)\1'
    return re.sub(pattern, lambda m: f"<strong>{m.group(2)}</strong>", text)

##### Italic

def convert_italic(text):
    pattern = r'(?<!\\)(\*|_)([^*_\n]+(?:\n[^*_\n]+)*)\1'
    return re.sub(pattern, lambda m: f"<em>{m.group(2)}</em>", text)

##### Blockquotes

def convert_blockquote(text):
    comp_pattern = re.compile(r'^(>.*(?:\n.+)*)', re.MULTILINE)
    return comp_pattern.sub(process_blockquote, text)

def process_blockquote(match):
    comp_pattern = re.compile(r'^(>+)[ ]*')
    lines = match.group(0).split('\n') # convert match object to string
    zipped_lines = [(len(inner_match.group(1)) if (inner_match := comp_pattern.match(line)) else 1, comp_pattern.sub('', line)) for line in lines]
    
    string = [] # optimize with join instead of multiple concatenations (+=)
    prev_content = False
    cur_level = 0
    
    for num, line in zipped_lines:
        if prev_content and line and num <= cur_level:
            string.append(f"{line}\n")
        else:
            if num > cur_level:
                string.append("<blockquote>\n" * (num - cur_level)) # optimize with string multiplication and arithmetic instead of loops
                cur_level = num
            elif num < cur_level:
                string.append("</blockquote>\n" * (cur_level - num))
                cur_level = num
            if (prev_content := bool(line)): # optimize with walrus operator to avoid double check on line (if line)
                string.append(f"{line}\n")
    
    string.append("</blockquote>\n" * cur_level)
    
    return "".join(string)

##### Lists

def convert_list(text):
    comp_pattern = re.compile(r'(?:(?<=\A)|(?<=\n{2}))[ ]*(?:\d+\.|[+*-])(?=\s).*(?:\n[ ]*.+)*')
    return comp_pattern.sub(process_list, text)

def process_list(match):
    comp_pattern = re.compile(r'^([ ]*)(\d+\.|-|\*|\+)([ ]*)')
    lines = match.group(0).split('\n') # convert match object to string
    zipped_lines = [(len(inner_match.group(1)), inner_match.group(2)[-1] == ".", len(inner_match.group(0)), comp_pattern.sub('', line)) for line in lines if (inner_match := comp_pattern.match(line))]

    string = [] # optimize with join instead of multiple concatenations (+=)
    need_ident = 0
    tag_stack = []

    for ident, type, needed_identation, line in zipped_lines:
        if ident >= need_ident:
            cur_type = ("<ol>", "</ol>") if type else ("<ul>", "</ul>")
            string.append(f"{cur_type[0]}\n<li>{line}")
            tag_stack.append((cur_type[1], need_ident))
        elif ident < tag_stack[-1][1]: # won't enter if tag_stack is empty
            string.append(f"</li>\n{tag_stack.pop()[0]}\n</li>\n<li>{line}")
        else:
            string.append(f"</li>\n<li>{line}")
        need_ident = needed_identation
    
    while tag_stack:
        string.append(f"</li>\n{tag_stack.pop()[0]}\n")
    
    return "".join(string)

##### Code

def convert_code(text):
    pattern = r'(`{1,2})([\s\S]+?)\1' # could use re.DOTALL to match newlines

    def replace(match):
        pattern2 = r'^[ ](.*)[ ]$'
        formatted_content = re.sub(pattern2, r'\1', match.group(2).replace("\n", " ")) # replace function to avoid another re.sub
        return f"<code>{formatted_content}</code>"

    return re.sub(pattern, replace, text)

##### Images

def convert_image(text):
    pattern = r'!\[(.*?)\]\((.*?)\)'
    return re.sub(pattern, lambda m: f"<img src=\"{m.group(2)}\" alt=\"{m.group(1)}\">", text)

##### Links

def convert_link(text):
    pattern = r'\[(.*?)\]\((.*?)\)'
    return re.sub(pattern, lambda m: f"<a href=\"{m.group(2)}\">{m.group(1)}</a>", text)
    
##### Line Breaks

def convert_line_break(text):
    pattern = re.compile(r'([ ]{2,}|\\$)\n', re.MULTILINE)
    return re.sub(pattern, "<br>", text)

##### Horizontal Rule

def convert_horizontal_rule(text):
    pattern = re.compile(r'^\n(-|\*|_)\1{2,}\n$', re.MULTILINE)
    return pattern.sub("<hr>\n", text)

##### Paragraphs

def convert_paragraph(text):
    allowed_starts = r'[A-Za-z&\-\d*~#]|<(?:(?:u|strong|em|del|code)>|(?:a|img)[ ])'
    pattern = re.compile(rf'^[ ]{{0,3}}(?:{allowed_starts}).*(?:\n(?:{allowed_starts}).*)*', re.MULTILINE)

    # there's no easy way to exclude matches inside code blocks
    code_block_pattern = re.compile(r'<pre><code.*?>[\s\S]*?</code></pre>')
    cb_intervals = [m.span() for m in re.finditer(code_block_pattern, text)] # m.span() == (m.start(), m.end())

    def allowed_sub(match):
        result = not any(start <= match.start() <= end and start <= match.end() <= end for start, end in cb_intervals)
        return f"<p>{match.group(0)}</p>" if result else match.group(0)

    return pattern.sub(allowed_sub, text)

#################################    ADVANCED FUNCTIONS    #################################

##### Fenced Code Blocks

def convert_fenced_code_block(text):
    pattern = r'`{3}(.+)?\n([\s\S]*?)\n`{3}'
    # [\s\S] is a hack to go around the fact that . does not match newlines (can also be solved with re.DOTALL)

    def replace(match):
        res = f"{match.group(2)}\n</code></pre>"
        if match.group(1) is None:
            res = f"<pre><code>{res}"       
        else:
            res = f"<pre><code class=\"language-{match.group(1)}\">{res}"
        return res

    return re.sub(pattern, replace, text)

##### Strikethrough

def convert_strikethrough(text):
    pattern = r'~~([^~].+?)~~'
    return re.sub(pattern, lambda m: f"<del>{m.group(1)}</del>", text)

############################################################################################

LT = "&lt;"
GT = "&gt;"
QUOTE = "&quot;"
APOSTROPHE = "&#39;" # &apos; is not officially supported in HTML4

def convert_ambiguous_symbols(text):
    symbols = [
        (r'\\<', LT),
        (r'\\>', GT),
        (r'"', QUOTE),
        (r'\'', APOSTROPHE),
        (r'\\\*', '*'),
        (r'\\_', '_'),
        (r'\\~', '~'),
        (r'(^[ ]{4,}|(?<!<)(?<!</)\b\w+[ ]*)(>+)', lambda m: m.group(1) + GT * len(m.group(2)), re.MULTILINE), # preserve the other parts of the match
        (r'(<+)(?!\w+>|/)', lambda m: LT * len(m.group(1)))
    ]
    
    for pattern, replacement, *args in symbols:
        text = re.sub(pattern, replacement, text, flags=functools.reduce(lambda x, y: x | y, args, 0))
    
    return text

def clear_empty_lines(text):
    pattern = r'\n{2,}'

    # again, code block problems
    code_block_pattern = re.compile(r'<pre><code.*?>[\s\S]*?</code></pre>')
    cb_intervals = [m.span() for m in re.finditer(code_block_pattern, text)]

    def allowed_sub(match):
        result = not any(start <= match.start() <= end and start <= match.end() <= end for start, end in cb_intervals)
        return f"\n" if result else match.group(0)
    
    return re.sub(pattern, allowed_sub, text)

conversion_functions = [
    convert_header,
    convert_bold,
    convert_italic,
    convert_strikethrough,
    convert_ambiguous_symbols, # must be converted after bold, italic and strikethrough because of the conversion of escaped characters
    convert_blockquote,
    convert_list,
    convert_image,
    convert_link,
    convert_line_break,
    convert_horizontal_rule,
    convert_fenced_code_block,
    convert_code, # code must be converted after fenced code blocks
    convert_paragraph, # paragraph must be converted last because there are lots of cases that can be hard to predict before other conversions
    clear_empty_lines # format the output to match the expected one
]

def main():
    text = sys.stdin.read()

    for func in conversion_functions:
        text = func(text)

    with open("output.html", "w") as output:
        output.write(text)

if __name__ == '__main__':
    main()
