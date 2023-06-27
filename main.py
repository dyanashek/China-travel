import telebot
import logging
import threading

import config
import keyboards
import functions
import utils

logging.basicConfig(level=logging.INFO, 
                    filename="py_log.log", 
                    filemode="w", 
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    )

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

threading.Thread(daemon=True, target=functions.inform_managers).start()

@bot.message_handler(commands=['start'])
def start_message(message):
    """Handles the 'start' command."""

    user_id = message.from_user.id
    count = functions.count_associated_manager(user_id)

    if count == 0:
        manager_name, manager_username = functions.choose_manager()
        threading.Thread(daemon=True, 
                        target=functions.associate_manager, 
                        args=(user_id, manager_name, manager_username),
                        ).start()

    threading.Thread(daemon=True, 
                            target=functions.add_user, 
                            args=(message,),
                            ).start()

    reply_text = f'''
                \nПривет, {message.from_user.first_name}!\
                \nЗдесь ты можешь узнать о нас все 📌\
                \n\
                \nПредлагаю познакомиться 🤝\
                \nГуляй по боту там, где хочешь🚶🏽‍♂️\
                \n\
                \nИ знай, в любой непонятной ситуации - жми кнопку "менеджер", он всегда тут как тут 👉👨‍💼\
                '''
    bot.send_message(message.chat.id, text=reply_text, reply_markup=keyboards.reply_menu())
    bot.send_message(message.chat.id, text=config.START_MESSAGE, reply_markup=keyboards.main_keyboard())


@bot.message_handler(commands=['menu'])
def start_message(message):
    """Handles the 'menu' command."""

    bot.send_message(message.chat.id, text=config.START_MESSAGE, reply_markup=keyboards.main_keyboard())


@bot.message_handler(commands=['stat'])
def stats_message(message):
    """Handles the 'stat' command. Provides an answer with users stat."""
    
    if str(message.from_user.id) == config.DIRECTOR_ID:
        replies = functions.construct_users_stat()
        print(replies)
        for reply in replies:
            try:
                bot.send_message(chat_id=message.chat.id,
                                 text=reply,
                                 )
            except:
                pass
    

@bot.callback_query_handler(func = lambda call: True)
def callback_query(call):
    """Handles query from inline keyboard."""

    # getting message's and user's ids
    message_id = call.message.id
    chat_id=call.message.chat.id
    user_id = call.from_user.id

    if call.data == 'about':
        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.ABOUT_MESSAGE,
                              )
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup = keyboards.about_keyboard(),
                                      )

    elif call.data == 'manager' or call.data == 'calculate':

        manager_name, manager_username = functions.get_associated_manager(user_id)

        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.MANAGER_MESSAGE,
                              )
        
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                    message_id=message_id, 
                                    reply_markup = keyboards.manager_keyboard(manager_username, manager_name),
                                    )
        
    elif call.data == 'rules':
        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.RULES_MESSAGE,
                              )
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup = keyboards.rules_keyboard(),
                                      )
        
    elif call.data == 'download':
        threading.Thread(daemon=True, 
                            target=functions.track_action, 
                            args=(user_id, call.data,),
                            ).start()
        
        with open(f'static/{config.APPLICATION}', "rb") as f:
            file_data = f.read()

        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass
            
        bot.send_document(chat_id=chat_id, 
                            document=file_data, 
                            visible_file_name=f'{config.APPLICATION}', 
                            reply_markup=keyboards.back_main_delete_keyboard(),
                            )

    elif call.data == 'shipment':
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        bot.send_message(chat_id=chat_id, 
                        text=config.SHIPMENT_MESSAGE,
                        parse_mode='Markdown',
                        reply_markup = telebot.types.ForceReply(input_field_placeholder='Фото/видео + описание'),
                        )

    elif call.data == 'stocks':
        threading.Thread(daemon=True, 
                            target=functions.track_action, 
                            args=(user_id, call.data,),
                            ).start()
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        try:
            bot.send_media_group(chat_id=chat_id, media=config.STOCK_MEDIA, timeout=30)
        except:
            pass

        bot.send_message(user_id, text=config.STOCK_MESSAGE, reply_markup=keyboards.back_about_keyboard())

    elif call.data == 'reviews':
        threading.Thread(daemon=True, 
                            target=functions.track_action, 
                            args=(user_id, call.data,),
                            ).start()
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        try:
            bot.send_media_group(chat_id=chat_id, media=config.REVIEWS_MEDIA_IMAGES, timeout=30)
            bot.send_media_group(chat_id=chat_id, media=config.REVIEWS_MEDIA_VIDEO, timeout=30)
        except:
            pass

        bot.send_message(user_id, text=config.REVIEWS_MESSAGE, 
                         reply_markup=keyboards.back_about_keyboard(), 
                         parse_mode='MarkdownV2',
                         )

    elif call.data == 'networks':
        threading.Thread(daemon=True, 
                            target=functions.track_action, 
                            args=(user_id, call.data,),
                            ).start()
        
        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.NETWORKS_MESSAGE,
                              )
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup = keyboards.networks_keyboard(),
                                      )

    elif call.data == 'addresses':
        threading.Thread(daemon=True, 
                            target=functions.track_action, 
                            args=(user_id, call.data,),
                            ).start()
        
        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.NETWORKS_MESSAGE,
                              )
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup = keyboards.addresses_keyboard(),
                                      )
        
    elif call.data == 'details':
        threading.Thread(daemon=True, 
                            target=functions.track_action, 
                            args=(user_id, call.data,),
                            ).start()
        
        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.DETAILS_MESSAGE,
                              parse_mode='Markdown',
                              )
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup = keyboards.back_about_keyboard(),
                                      )
        
    elif call.data == 'back_main':
        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.START_MESSAGE,
                              )
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup = keyboards.main_keyboard(),
                                      )
        
    elif call.data == 'guangzhou':
        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.GUANGZHOU_MESSAGE,
                              parse_mode='Markdown',
                              )
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup = keyboards.back_addresses_keyboard(),
                                      )
        
    elif call.data == 'beijing':
        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.BEIJING_MESSAGE,
                              parse_mode='Markdown',
                              )
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup = keyboards.back_addresses_keyboard(),
                                      )
        
    elif call.data == 'moscow':
        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.MOSCOW_MESSAGE,
                              parse_mode='Markdown',
                              )
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup = keyboards.back_addresses_keyboard(),
                                      )
        
    elif call.data == 'back_about':
        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.ABOUT_MESSAGE,
                              )
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup = keyboards.about_keyboard(),
                                      )
        
    elif call.data == 'cost':
        threading.Thread(daemon=True, 
                            target=functions.track_action, 
                            args=(user_id, call.data,),
                            ).start()
        
        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.COST_MESSAGE,
                              parse_mode='Markdown',
                              )
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup = keyboards.back_rules_keyboard(),
                                      )
        
    elif call.data == 'terms':
        threading.Thread(daemon=True, 
                            target=functions.track_action, 
                            args=(user_id, call.data,),
                            ).start()
        
        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.TERMS_MESSAGE,
                              parse_mode='Markdown',
                              )
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup = keyboards.back_rules_keyboard(),
                                      )
        
    elif call.data == 'poizon':
        threading.Thread(daemon=True, 
                            target=functions.track_action, 
                            args=(user_id, call.data,),
                            ).start()
        
        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.POIZON_MESSAGE,
                              parse_mode='Markdown',
                              )
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup = keyboards.back_rules_keyboard(),
                                      )
        
    elif call.data == 'alipay':
        threading.Thread(daemon=True, 
                            target=functions.track_action, 
                            args=(user_id, call.data,),
                            ).start()
        
        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.ALIPAY_MESSAGE,
                              parse_mode='Markdown',
                              )
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup = keyboards.back_rules_keyboard(),
                                      )
        
    elif call.data == 'currency':
        threading.Thread(daemon=True, 
                            target=functions.track_action, 
                            args=(user_id, call.data,),
                            ).start()
        
        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.CURRENCY_MESSAGE,
                              parse_mode='Markdown',
                              )
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup = keyboards.back_rules_keyboard(),
                                      )
        
    elif call.data == 'contract':
        threading.Thread(daemon=True, 
                            target=functions.track_action, 
                            args=(user_id, call.data,),
                            ).start()
        
        with open(f'static/{config.CONTRACT}', "rb") as f:
            file_data = f.read()

        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass
            
        bot.send_document(chat_id=chat_id, 
                            document=file_data, 
                            visible_file_name=f'{config.CONTRACT}', 
                            reply_markup=keyboards.back_rules_delete_keyboard(),
                            )

    elif call.data == 'another_question':
        bot.send_message(user_id, text=config.START_MESSAGE, reply_markup=keyboards.main_keyboard())

    elif call.data == 'back_addresses':
        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.NETWORKS_MESSAGE,
                              )
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup = keyboards.addresses_keyboard(),
                                      )
        
    elif call.data == 'back_rules':
        bot.edit_message_text(chat_id=chat_id, 
                              message_id=message_id, 
                              text=config.RULES_MESSAGE,
                              )
        bot.edit_message_reply_markup(chat_id=chat_id, 
                                      message_id=message_id, 
                                      reply_markup = keyboards.rules_keyboard(),
                                      )
        
    elif call.data == 'back_rules_delete':
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        bot.send_message(chat_id=chat_id, 
                              reply_markup = keyboards.rules_keyboard(),
                              text=config.RULES_MESSAGE,
                              parse_mode='Markdown'
                              )
    
    elif call.data == 'back_main_delete':
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        bot.send_message(chat_id=chat_id, 
                              reply_markup = keyboards.main_keyboard(),
                              text=config.START_MESSAGE,
                              parse_mode='Markdown'
                              )
        

@bot.message_handler(commands=['user'])
def settings_message(message):
    """Handles the 'user' command. Increases managers users amount."""

    managers = functions.get_managers()
    if str(message.from_user.id) in managers:

        user_username = message.text.replace('/user', '').replace(' ', '')
        user_username = utils.username_transform(user_username)
        manager_action = functions.manager_action(message.from_user.username, user_username)

        if manager_action:
            text = functions.construct_reply(user_username)
            reply_text = f'Лид учтен.{text}'
        else:
            reply_text = 'Лид не из бота или был учтен ранее.'

        bot.send_message(message.chat.id, text=reply_text, parse_mode='Markdown')


@bot.message_handler(content_types=['photo', 'video'])
def handle_media(message):
    """Handles message with type photo or video."""
    try:
        print(message.video.file_id)
    except:
        pass

    try:
        print(message.photo[-1].file_id)
    except:
        pass
    

    shipment_message = config.SHIPMENT_MESSAGE.replace('*', '')
    shipment_wrong_message = config.SHIPMENT_WRONG_MESSAGE.replace('*', '').replace('\\', '').replace('n', '')

    if (message.reply_to_message is not None) and (message.caption is not None) and\
    ((message.reply_to_message.text == shipment_message) or\
    (message.reply_to_message.text in shipment_wrong_message)):
        
        bot.forward_message(chat_id=config.SHIPMENT_CHAT, 
                            from_chat_id=message.chat.id, 
                            message_id=message.id,
                            )
        threading.Thread(daemon=True, 
                            target=functions.track_action, 
                            args=(message.from_user.id, 'shipment',),
                            ).start()
        
        bot.send_message(chat_id=message.chat.id,
                        text=config.SHIPMENT_FORWARD_MESSAGE,
                        reply_markup=keyboards.back_main_keyboard(),
                        )
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=message.reply_to_message.id)
        except:
            pass

        try:
            bot.delete_message(chat_id=message.chat.id, message_id=message.id)
        except:
            pass
    
    elif (message.reply_to_message is not None) and\
    ((message.reply_to_message.text == shipment_message) or\
    (message.reply_to_message.text in shipment_wrong_message)):
        bot.send_message(chat_id=message.chat.id,
                        text=config.SHIPMENT_WRONG_MESSAGE,
                        parse_mode='Markdown'
                        )
    
    elif (message.reply_to_message is not None) and\
    (config.SHIPMENT_PHOTO_MESSAGE in message.reply_to_message.text):
        bot.forward_message(chat_id=config.SHIPMENT_CHAT, 
                            from_chat_id=message.chat.id, 
                            message_id=message.id,
                            )
        bot.send_message(chat_id=message.chat.id,
                        text=config.SHIPMENT_FORWARD_MESSAGE,
                        reply_markup=keyboards.back_main_keyboard(),
                        )
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=message.reply_to_message.id)
        except:
            pass

        try:
            bot.delete_message(chat_id=message.chat.id, message_id=message.id)
        except:
            pass


@bot.message_handler(content_types=['text'])
def handle_text(message):
    """Handles message with type text.
    Sends a reply to user who wanted to calculate shipment cost.
    """

    if message.text == '📱 Меню':
        bot.send_message(message.chat.id, text=config.START_MESSAGE, reply_markup=keyboards.main_keyboard())
    elif message.text == '👨‍💼 Менеджер':
        manager_name, manager_username = functions.get_associated_manager(message.from_user.id)

        bot.send_message(chat_id=message.chat.id,
                        text=config.MANAGER_MESSAGE,
                        reply_markup = keyboards.manager_keyboard(manager_username, manager_name),
                        )
        
    shipment_message = config.SHIPMENT_MESSAGE.replace('*', '')
    shipment_wrong_message = config.SHIPMENT_WRONG_MESSAGE.replace('*', '').replace('\\', '').replace('n', '')

    if (str(message.chat.id) == config.SHIPMENT_CHAT) and (message.reply_to_message is not None)\
    and (str(message.reply_to_message.from_user.id) == config.BOT_ID):
        
        params = message.reply_to_message.caption
        if params is None:
            params = message.reply_to_message.text
        if params is None:
            params = 'не определены'

        manager_name, manager_username = functions.get_associated_manager(message.reply_to_message.forward_from.id)

        try:
            reply_text = f'Ответ специалиста по стоимости доставки товара с параметрами ({params}):\n{message.text}'
            bot.send_message(chat_id=message.reply_to_message.forward_from.id,
                        text=reply_text,
                        reply_markup=keyboards.only_manager_keyboard(manager_username),
                        )
            
            success_text = f'Стоимость доставки отправлена пользователю @{message.reply_to_message.forward_from.username}.'
            bot.send_message(chat_id=message.chat.id,
                             text=success_text,
                             )
            
            if config.SHIPMENT_PHOTO_MESSAGE not in message.text:
                manager_id = functions.get_manager_id(manager_username)

                text = (
                    f'Закрепленный за вами пользователь @{message.reply_to_message.forward_from.username} запросил расчет стоимости доставки:\n'
                    f'C параметрами: {params}\n'
                    f'Получил ответ: {message.text}'
                    )
                
                bot.send_message(chat_id=manager_id,
                                 text=text,
                                 )
        except Exception as ex:
            print(ex)

    elif (message.reply_to_message is not None) and\
    ((message.reply_to_message.text == shipment_message) or\
    (message.reply_to_message.text in shipment_wrong_message)):
        
        bot.forward_message(chat_id=config.SHIPMENT_CHAT, 
                            from_chat_id=message.chat.id, 
                            message_id=message.id,
                            )
        threading.Thread(daemon=True, 
                            target=functions.track_action, 
                            args=(message.from_user.id, 'shipment',),
                            ).start()
        
        bot.send_message(chat_id=message.chat.id,
                        text=config.SHIPMENT_FORWARD_MESSAGE,
                        reply_markup=keyboards.back_main_keyboard(),
                        )
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=message.reply_to_message.id)
        except:
            pass

        try:
            bot.delete_message(chat_id=message.chat.id, message_id=message.id)
        except:
            pass


if __name__ == '__main__':
    while True:
        try:
            bot.polling()
        except:
            pass