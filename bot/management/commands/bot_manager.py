import uuid

from django.core.exceptions import ObjectDoesNotExist

from bot.management.commands.dialogs import greetings, GREETINGS_LIST, CODE_DESCRIPTION, RECREATE_VER_CODE, GOOD_NEWS
from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import UpdateObj


class BotManager:
    def __init__(self, tg_token: str) -> None:
        self.tg_token = tg_token
        self.tg_client = TgClient(tg_token)

    def run_bot(self):
        offset = 0
        polling = True

        while polling:
            # Запускаем проверку обновлений
            response = self.tg_client.get_updates(offset=offset)

            # Обработка полученных обновлений
            offset = self.upd_handler(response.result)

    def upd_handler(self, upd_objects: list[UpdateObj]) -> int:
        """
        Основной обработчик обновлений от Телеграма. Получает
        список объектов обновлений. По очереди обрабатывает
        каждое обновление в цикле.

        Возвращает offset на "1" больше чем у последнего обновления
        для подтверждения получения текущих сообщений.
        """
        offset = 0

        for upd_obj in upd_objects:
            offset = upd_obj.update_id + 1

            # Можно удалить. Печатает в консоль полученное сообщение
            # от пользователя. Нужно ли оно мне сейчас?
            # print(upd_obj.message)

            # Будем обрабатывать новые сообщения только если
            # они содержат поле ТЕКСТ
            if hasattr(upd_obj.message, 'text'):
                message = str(upd_obj.message.text)
                chat_id = upd_obj.message.chat.id

                self.message_handler(message, chat_id)

        return offset

    def get_tg_user(self, user_id: int) -> TgUser:
        """
        Получает модель TgUser на основе user_id
        """
        try:
            tg_user = TgUser.objects.get(chat_id=user_id)

        except ObjectDoesNotExist:
            tg_user = TgUser(chat_id=user_id)
            tg_user.save()

        return tg_user

    def set_verification_code(self, tg_user: TgUser) -> int:
        """
        Генерирует код аутентификации и сохраняет его в
        БД для связи с пользователем сервиса
        """
        verification_code = str(uuid.uuid4().hex[:12])  # Генерируем код длиной 12 символов из случайного UUID
        tg_user.verification_code = verification_code
        tg_user.save()

        return verification_code

    def message_handler(self, message: str, chat_id: int):
        """
        Основной обработчик сообщений от пользователя.
        - Если пользователь новый (т.е. у него еще нет кода верификации),
        то создаём код и предлагаем его активировать.
        - Если пользователь уже знакомый, но еще не активирован (нет поля User),
        то предлагаем таки активировать аккаунт или поменять код активации.
        - Если знакомый и активированный то предлагаем ждать уведомлений :)
        """
        tg_user = self.get_tg_user(chat_id)
        verification_code = tg_user.verification_code

        if not tg_user.verification_code and not tg_user.user:
            # Приветствие только тому кто написал впервые
            # И еще вообще не имеет записи в БД
            msg_to_user = greetings(GREETINGS_LIST)
            self.tg_client.send_message(chat_id, msg_to_user)

            verification_code = self.set_verification_code(tg_user)
            self.tg_client.send_message(chat_id, CODE_DESCRIPTION)
            self.tg_client.send_message(chat_id, f'ТВОЙ КОД: {verification_code}')
            self.tg_client.send_message(
                chat_id, (f'Или перейди по ссылке: /api/verify/{verification_code}/ '
                          'с токеном авторизации своего пользователя')
            )
        else:
            # Тут у пользователя уже есть код верификации.
            if not tg_user.user:
                if message == "ПОЛУЧИТЬ НОВЫЙ КОД":
                    keyboard = self.tg_client.create_keyboard()
                    verification_code = self.set_verification_code(tg_user)
                    self.tg_client.send_message(
                        chat_id, f'ТВОЙ НОВЫЙ КОД: {verification_code}', reply_markup=keyboard
                    )
                else:
                    keyboard = self.tg_client.create_keyboard(["ПОЛУЧИТЬ НОВЫЙ КОД"])
                    self.tg_client.send_message(
                        chat_id, RECREATE_VER_CODE, reply_markup=keyboard
                    )
            else:
                self.tg_client.send_message(chat_id, GOOD_NEWS)
