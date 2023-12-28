import os
import json

with open('output.txt', 'r', encoding='utf-8') as file:
    data = file.read()

#替换单引号为双引号
data = data.replace("'", "\"")

with open('fixed_output.json', 'w', encoding='utf-8') as json_file:
    json_file.write(data)

with open('fixed_output.json', 'r', encoding='utf-8') as json_file:
    data = json_file.readlines()

#导出html
html_content = '<html><head><title>QQ Group Messages</title></head><body>'

for item in data:
    item_data = json.loads(item)
    qq_name = item_data['qq_name']
    content = item_data['content']

    html_content += f'<p><b>{qq_name}:</b>'

    for msg in content:
        if msg.startswith('http'):
            img_name = os.path.basename(msg)
            html_content += f'<br><img src="img/{img_name}" alt="{img_name}">'
        else:
            html_content += f'<br>{msg}'

    html_content += '</p>'

html_content += '</body></html>'

with open('messages.html', 'w', encoding='utf-8') as html_file:
    html_file.write(html_content)

print('HTML 文件已创建。')