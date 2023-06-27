import os
import telebot
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# id of chat where calculate shipment messages should be forward
SHIPMENT_CHAT = os.getenv('SHIPMENT_CHAT')

# bot's id
BOT_ID = os.getenv('BOT_ID')

# director's id
DIRECTOR_ID = os.getenv('DIRECTOR_ID')

# time after which bot informs managers about users, who didn't contact them
INFORM_TIME = 15

# name of the document with contract example
CONTRACT = 'договор.docx'

# name of the document with application example
APPLICATION = 'заявка.xlsx'

# the message that displays with main menu
START_MESSAGE = 'Выберите интересующий вас раздел:'

# message that displays when user chooses 'about' section
ABOUT_MESSAGE = 'Узнайте подробнее о нас:'

# message that displays when user choose 'networks' section
NETWORKS_MESSAGE = 'Следите за нами в социальных сетях:'

# message that displays when user choose 'addresses' section
ADDRESSES_MESSAGE = 'Узнайте интересующий адрес:'

# message that displays when user choose 'rules' section
RULES_MESSAGE = 'Узнайте о деталях работы с нами:'

# message with bank account details
DETAILS_MESSAGE = '''
                \nНазвание организации: *ИНДИВИДУАЛЬНЫЙ ПРЕДПРИНИМАТЕЛЬ ТИТОВ АНТОН АНАТОЛЬЕВИЧ*,\
                \nЮридический адрес организации: *654250, РОССИЯ, КЕМЕРОВСКАЯ ОБЛАСТЬ - КУЗБАСС, НОВОКУЗНЕЦКИЙ Р-Н, ПОСЕЛОК КУЗЕДЕЕВО, УЛ ПУШКИНА, Д 7*,\
                \nИНН: *421813661482*,\
                \nОГРН: *322420500103891*,\
                \nРасчетный счет: *40802810100004072445*,\
                \nБанк: *АО "ТИНЬКОФФ БАНК"*,\
                \nИНН банка: *7710140679*,\
                \nБИК банка: *044525974*,\
                \nКорреспондентский счет банка: *30101810145250000974*,\
                \nЮридический адрес банка: *Москва, 127287, ул. Хуторская 2-я, д. 38А, стр. 26*.
                ''' 

# message with GuangZhou address
GUANGZHOU_MESSAGE = '''
                \nАдрес Гуанчжоу (на китайском языке):\
                \n*广东省广州市白云区同德街道西城鞋业基地G栋118-2*\
                \nПолучатель: *王洪威*,\
                \nСотовый телефон: *18520718666*,\
                \nПочтовый индекс: *510407*.\
                \n\
                \nАдрес Гуанчжоу (на английском языке), для отправки образцов из России в Китай:\
                \n*118-2 Building G, Xichengxeiyejidi Xichalu Road, Baiyun District Guangzhou city, China*\
                \nПолучатель : *Wanghongwei*,\
                \nНомер телефона : *+8618520718666*,\
                \nПочтовый индекс: *510407*,\
                \nПаспорт: *13098419820204213X*.
                '''

# message with Beijing address
BEIJING_MESSAGE = '''
                \n*Внимание, в Пекине только отправить экспресс* (рейсы каждые 2-3 дня)\
                                        
                \nАдрес Пекин: *日区阳朝市京北, 层二下地际国, 288A B. 座 房库*,\
                \nПолучатель: *东启戈*,\
                \nСотовый телефон: *18520718666*,\
                \nПочтовый индекс: *100020*.
                '''

# message with Moscow address
MOSCOW_MESSAGE = '''
                \nМосква, ТЯК Люблино, Тихорецкий бульвар дом 1 (вход- 7 и 7А).\
                \n\
                \nМосква, Южные ворота, МКАД 19 км. Вход 15 напротив карго "Сбор грузов".\
                '''

# message with cost of service
COST_MESSAGE = '''
                \n✅ Доставка:\
                \n🚀 Экспресс: *1-3дн. (от 1 кг)*\
                \n🛫 Самолет: *10-12дн.*\
                \n🚈 Быстрый поезд: *13-15дн.*\
                \n🚛 Быстрый авто: *13-15дн.*\
                \n🚂 Медленный поезд: *25-30дн.*\
                \n🛳 Море: *35-45дн.*\
                \nМинимум *от 10кг*.\
                \n\
                \nСтоимость доставки зависит от *габаритов, плотности и веса*.\
                \n\
                \nДоставка товаров оплачивается *при получении в РФ*.\
                '''

# message with terms of service
TERMS_MESSAGE = '''
                \nНайдем любой товар/ проверим на качество/ упакуем/ фото-видео отчет/ отправим нашим карго без посредников по честным ценам. 🚀\
                \n\
                \n✅ Стоимость наших услуг\
                \nДо *50т.₽* услуги *5000₽*\
                \nОт *50-100т.₽* услуги *7000₽*\
                \nОт *100-200т.₽* услуги *10.000₽*\
                \nОт *200-1млн.₽* услуги *5%*\
                \n✅ Свыше *1млн.руб* цена договорная!
                '''

# message with terms of poizon usage
POIZON_MESSAGE = '''
                \n*Стоимость:*\
                \nВыкупаем мы: *10$ за кг*, *10-12 дней* 🛫 до РФ. *УСЛУГИ БЕСПЛАТНО* отправляем *от 10кг*, можем отправить меньше 1-9 кг, оплата будет за *10кг/100$*, в стоимость входит (перевод средств в юани без посредников, выкуп, проверка на брак, подробный фото и видеоотчет каждой единицы товара).\
                \n\
                \nВыкупаете вы: *6,8$ за кг*, *10-12 дней* 🛫 до РФ, отправляем *от 10кг*, можем отправить меньше 1-9 кг, оплата будет за *10кг/68$* (если необходимо фото товара - стоимость 10 юаней/фото одной единицы товара).\
                \n\
                \nЭкспресс доставка за *3-5 дней до РФ* 📦🚀\
                \nВыкупаем мы: *42$ за кг*\
                \nВыкупаете вы: *32$ за кг*\
                '''

# message with alipay terms
ALIPAY_MESSAGE = '''
                \nПополнение Alipay *1500₽* до *10.000 RMB*\
                \nСвыше *10.000 RMB 2%*.\
                '''

# message with currency rate
CURRENCY_MESSAGE = '''
                \nКурс доллара к оплате при получении зависит от ЦБ и бирж, есть комиссия за конвертацию и оплату *(+1.5-2₽ к текущему курсу Сбербанка)*.\
                \n\
                \nКурс юаня при оплате берется *+7-10%* за конвертации и переводы в Китай.\
                '''

# message that displays when user wants to contact a manager
MANAGER_MESSAGE = 'Нажмите на кнопку ниже, чтобы перейти в чат с менеджером.'

# files that displays when user wants to see details about stock
STOCK_MEDIA = [telebot.types.InputMediaPhoto(media='AgACAgIAAxkBAAICc2RX3ePhhboOam0gmxS69BxdRDIwAAIYyjEbVDLASjcYjc2DN9ZbAQADAgADdwADLwQ'),
           telebot.types.InputMediaPhoto(media='AgACAgIAAxkBAAICdGRX3eMdIUSxJJTh8iInHPXV52CyAAIXyjEbVDLASu6cd9dsS309AQADAgADdwADLwQ'),
           telebot.types.InputMediaPhoto(media='AgACAgIAAxkBAAICdmRX3ePVG6gByCk8dt74w4HErFL1AAIZyjEbVDLASo61_9TIpqunAQADAgADdwADLwQ'),
           telebot.types.InputMediaPhoto(media='AgACAgIAAxkBAAICdWRX3ePatHiIUNyFRo1hwc4yFnD0AAIWyjEbVDLAStMqYNtNmUyTAQADAgADeQADLwQ'),
           telebot.types.InputMediaVideo(media='BAACAgIAAxkBAAIFJmRbi0AGMMbOU_YzWPVqlwAB7MjGtQACji8AAta-2Uq0ss2F4mWrRi8E'),
           ]

# message that displays when user chooses review section
REVIEWS_MESSAGE = 'Больше отзывов в нашем [ТГ канале](https://t.me/china_travel_ru)\.'

# message that displays when user chooses stock section
STOCK_MESSAGE = 'Адреса складов можно посмотреть в разделе "наши адреса".'

# message that display when user wants to calculate the delivery cost
SHIPMENT_MESSAGE = 'В ответ на это сообщение пришлите *одну* фотографию/видео отправляемого товара и все известные характеристики *(вес, объем, плотность, количество)*.'

# message that displays when user send information to calculate
SHIPMENT_FORWARD_MESSAGE = 'Данные переданы для расчета нашему персоналу, ответ поступит в этот чат в ближайшее время.'

# message that displays when user wrong send information to calculate
SHIPMENT_WRONG_MESSAGE = '''
                        \nДанные не соответствуют одному или нескольким параметрам:\
                        \n1. Прикреплена *одна фотография* или *одно видео*\
                        \n2. Есть описание для расчета *(вес, объем, количество)*\
                        '''
# text that appears when managers asks user to send photo of product to calculate the shipment
SHIPMENT_PHOTO_MESSAGE = 'Для расчета стоимости доставки товара необходимо его фото, пожалуйста, пришлите его в ответ на это сообщение.'

# files that displays when user wants to see reviews
REVIEWS_MEDIA_IMAGES = [telebot.types.InputMediaPhoto(media='AgACAgIAAxkBAAICvGRX5ZE7joQLtWUfttxpq3Yir6y6AALbyjEbVDLASo_Cy4gJ6rtUAQADAgADeAADLwQ'),
           telebot.types.InputMediaPhoto(media='AgACAgIAAxkBAAICvWRX5ZFR3RiQliOJPSKq2IbNWIFQAALdyjEbVDLASvNv-zgDlZz-AQADAgADeAADLwQ'),
           telebot.types.InputMediaPhoto(media='AgACAgIAAxkBAAICv2RX5ZFzDX1nvwhh4nP3vJsBTLP9AALeyjEbVDLASo56xquz-ehWAQADAgADeAADLwQ'),
           telebot.types.InputMediaPhoto(media='AgACAgIAAxkBAAICwGRX5ZGOe9HKcdRbJc1ZE9bz5DrsAALfyjEbVDLAShQJ3NiiNsQsAQADAgADeAADLwQ'),
           telebot.types.InputMediaPhoto(media='AgACAgIAAxkBAAICwWRX5ZHNC5mHWsRIv4TqCJtckrc6AALcyjEbVDLASqkIbZ4PdPbbAQADAgADeQADLwQ'),
           telebot.types.InputMediaPhoto(media='AgACAgIAAxkBAAICvmRX5ZH219LNxOiZDJqCtNWJLF4fAALgyjEbVDLASjJnlv92bxvNAQADAgADeAADLwQ'),
           ]

REVIEWS_MEDIA_VIDEO = [telebot.types.InputMediaVideo(media='BAACAgIAAxkBAAICx2RX5s1n-ceSijEDiXXluNWexum8AALoMgACVDLASqqyEpfppHOJLwQ'),
           telebot.types.InputMediaVideo(media='BAACAgIAAxkBAAICyGRX5s0AAfo1fcMT-WP02XZqxP0RqgAC5zIAAlQywEpm-4o0YgHJ4C8E'),
           telebot.types.InputMediaVideo(media='BAACAgIAAxkBAAICzGRX53BmF5UfrxzXtmSRxFrnTSP2AALwMgACVDLASvyX_8AhThYOLwQ'),
           telebot.types.InputMediaVideo(media='BAACAgIAAxkBAAIC0mRX6DhdG3O1Z4JvwVk3wCu4bJhJAALyMgACVDLASrRbd0DJcERkLwQ'),
           telebot.types.InputMediaVideo(media='BAACAgIAAxkBAAIC02RX6DjXxZfq_mgFJSdPOGGXWaY7AALzMgACVDLASkgpLrOrR7pgLwQ'),
           telebot.types.InputMediaVideo(media='BAACAgIAAxkBAAIC2GRX6OdWJuJBiQFFt0tzR72p8fToAAL6MgACVDLASmH6AqpO53WjLwQ'),
           telebot.types.InputMediaVideo(media='BAACAgIAAxkBAAIC2WRX6OcB-ZleDvIHEd27gyCDTZSMAAL7MgACVDLASt6KPWXzhYgVLwQ'),
           telebot.types.InputMediaVideo(media='BAACAgIAAxkBAAIC_mRX7Xf6VckZREB4syMKn2z5JzypAAI4MwACVDLASjW_sOA7sOEXLwQ'),
           ]
