features_str = None

symbol_dict = dict()
symbol_count_dict = dict()

with open('features.txt', 'r') as features_file:
    features_str = features_file.read()

features_lines = features_str.splitlines()

last_symbol = None

for feature_line in features_lines:
    if feature_line.startswith('item'):
        split = feature_line.split(';')
        
        status = split[1]
        symbol = split[2]
        name = split[3]
        
        symbol_dict[symbol] = ('item', name, status)
        symbol_count_dict[symbol] = 0
    elif feature_line.startswith('nested'):
        split = feature_line.split(';')
        
        symbol = split[1]
        name = split[2]
        
        symbol_dict[symbol] = ('nested', name, list())
        symbol_count_dict[symbol] = 0
        last_symbol = symbol
    elif feature_line.startswith('-'):
        split = feature_line.split(' ')
        
        symbol = split[1]
        
        symbol_dict[last_symbol][2].append(symbol)
        symbol_count_dict[symbol] += 1
        
print(symbol_dict)
print(symbol_count_dict)


def recursive_populate(symbol, symbols, features_html):
    symbol_expanded = symbols[symbol]
    symbol_type = symbol_expanded[0]
    if symbol_type == 'item':
        features_html += '<li><span class="' + symbol_expanded[2] + '">' + symbol_expanded[2] + '</span> ' + symbol_expanded[1] + '</li>\n'
        print('item ' + symbol)
    elif symbol_type == 'nested':
        features_html += '<li>\n'
        features_html += '<span class="caret">' + symbol_expanded[1] + '</span>\n'
        features_html += '<span class="progress">0%</span>\n'
        features_html += '<ul class="nested">\n'
        print('nested ' + symbol)
        for nested_symbol in symbols[symbol][2]:
            features_html = recursive_populate(nested_symbol, symbols, features_html)
        features_html += '</ul>\n'
        features_html += '</li>\n'
    return features_html

features_html = ''

features_html += '<ul id="tree">\n'
for key, value in symbol_count_dict.items():
    if value == 0:
        features_html = recursive_populate(key, symbol_dict, features_html)
features_html += '</ul>\n'


with open('template.txt', 'r') as template_file:
    template_str = template_file.read()
    template_str = template_str.replace('%feature_list%', features_html)
    
    with open('index.html', 'w') as output_file:
        output_file.write(template_str)