from ollama import Client

with open('/home/snow/NEU/CS6120/cricket_news/match.txt', 'r') as file:
    content = file.read()

print(content[8000:10000] + '\n \n \n \n')
client = Client(host='http://localhost:11434')
response = client.chat(model='gemma:2b', messages=[
  {
    'role': 'user',
    'content': 'Extract the most essential points out of this small part of cricket commentary into key points. Do not deviate from topic.' + content[8000:10000],
  },
])
print(response['message']['content'])

response = client.chat(model='mistral', messages=[
  {
    'role': 'user',
    'content': 'Use the notes provided to write a cricket news article. Have a heading, make it engaging and write lengthily about players. Do not write in note form, include paragraphs. Make sure to paraphrase and do not use the same language as the notes.' + response['message']['content'],
  },
])
print(response['message']['content'])