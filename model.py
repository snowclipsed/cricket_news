from ollama import Client


class Model:
    def __init__(self, model_name):
        self.model_name = model_name
        self.client = Client(host='http://localhost:11434')

    def get_prompt_template(self, task):
        file_path = 'prompt_templates'
        with open(f'{file_path}/{task}.txt', 'r') as file:
            content = file.read()
        return content
    
    def response(self, text, template):
        messages = [
            {
                'role': 'user',
                'content': template + text,
            },
        ]
        response = self.client.chat(model=self.model_name, messages=messages)
        return response['message']['content']