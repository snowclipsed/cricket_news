from ollama import Client


class Model:
    def __init__(self, model_name):
        self.model_name = model_name
        self.client = Client(host='http://localhost:11434')

    def get_prompt_template(self, task, type):
        file_path = 'prompt_templates'
        with open(f'{file_path}/{task}/{type}.txt', 'r') as file:
            content = file.read()
        return content
    
    def response(self, template, text):
        # messages = [
        #     {
        #         'role': 'user',
        #         'content': template + text,
        #     },
        # ]
        if self.model_name == 'llama3':
            response = self.client.generate(self.model_name, template + text, options={'num_ctx': 5000})
        else:
            response = self.client.generate(self.model_name, template + text)
        # print(response['response'])
        return response['response']