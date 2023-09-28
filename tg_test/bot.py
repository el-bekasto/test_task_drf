import requests


class Chat:
    def __init__(self, data):
        self.id = data['id']
        self.type = data['type']
        self.title = data['title'] if 'title' in data else None
        self.username = data['username'] if 'username' in data else None
        self.first_name = data['first_name'] if 'first_name' in data else None
        self.last_name = data['last_name'] if 'last_name' in data else None


class User:
    def __init__(self, data):
        self.id = data['id']
        self.is_bot = data['is_bot']
        self.first_name = data['first_name']
        self.last_name = data['last_name'] if 'last_name' in data else None
        self.username = data['username'] if 'username' in data else None
        self.language_code = data['language_code']


class Message:
    def __init__(self, data):
        self.message_id = data['message_id']
        self.from_user = User(data['from'])
        self.chat = Chat(data['chat'])
        self.text = data['text'] if 'text' in data else None


class Bot:
    def __init__(self, token):
        self.api_url = f'https://api.telegram.org/bot{token}'

    def make_request(self, method, data):
        r = requests.get(
            self.api_url + method,
            params=data
        )

    def send_message(self, chat_id, text):
        self.make_request(
            '/sendMessage',
            {
                'chat_id': chat_id,
                'text': text
            }
        )

    def tokenregistered(self, user: User):
        self.send_message(
            chat_id=user.id,
            text='Токен успешно зарегистрирован.'
        )

    def notify_user(self, user_id, message):
        self.send_message(
            chat_id=user_id,
            text=message
        )

    def doesnotexist(self, user: User):
        self.send_message(
            chat_id=user.id,
            text='Неправильный токен. Попробуйте еще раз.'
        )

    def require_token(self, user: User):
        self.send_message(
            chat_id=user.id,
            text='Отправьте мне свой токен, который вы получили после регистрации на нашем сайте.'
        )

