from random import randint

GREETINGS_LIST = [
    ("Привет! Похоже, мы с тобой еще не знакомы. Я бот-помошник, "
     "умею напоминать тебе про твои привычки и помогать прививать полезные. Но,"
     " чтобы нам с тобой начать работать, нужно познакомиться поближе."),
    ("Приветствую! Мы с тобой еще не знакомы? Чтобы продолжить общение"
     " нужно для начала обменяться кодами допуска."),
    ("Дарова! Нам бы, для начала, узнать друг-друга получше. У тебя ведь "
     "уже есть аккаунт в нашем сервисе по постановке привычек? Если нет, то нужно"
     " зарегистрироваться."),
    "Так, давай сразу к делу.",
]


def greetings(greetings_list: list[str]) -> str:
    num = randint(0, len(greetings_list)-1)
    return greetings_list[num]


CODE_DESCRIPTION = "Для верификации используй предоставленный мной токен."

RECREATE_VER_CODE = (
    "Похоже вы еще не подключили оповещение в Телеграм. Если нужна помощь в "
    "активации то обратитесь за помощью к кому нибудь. Если потеряли код "
    "верификации то можно запросить новый."
)

GOOD_NEWS = (
    "У вас и так всё хорошо. Ждите оповещений в соответствии с настройками "
    "вашего аккаунта. Спасибо что пользуетесь нашей системой :)."
)
