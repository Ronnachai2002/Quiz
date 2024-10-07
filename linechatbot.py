from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate,
                            MessageTemplateAction, QuickReply, QuickReplyButton, CarouselTemplate, CarouselColumn)

app = Flask(__name__)

# กำหนดค่า Channel Secret และ Channel Access Token
line_bot_api = LineBotApi('U2i67Yhg7fMpww4mTvQiZCDJe9A2BgJpgS4vKhDA/N4qVW3RlRSkLF2R1bVbAOhKfVUrhyOCjCdznTNH1c+txyzvQmL1wbsh6+IHnrfwtPydM+T43zX9wVIbU+F1ns31ehDOG2gzNBKyGrE9lB7ckgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2f649b9a0b9fd0ee758a83020611e9ed')


@app.route("/callback", methods=['POST'])  # เปลี่ยนกลับมาเหลือเฉพาะ POST
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'





# ฟังก์ชันสำหรับการตอบกลับข้อความ
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.lower()

    # การตอบกลับแบบข้อความ
    if user_text == "text":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Hello! This is a simple text response.")
        )
    # การตอบกลับแบบปุ่ม (Button Template)
    elif user_text == "button":
        buttons_template = ButtonsTemplate(
            title='Menu', text='Please select an option:', actions=[
                MessageTemplateAction(label='Say Hello', text='Hello!'),
                MessageTemplateAction(label='Say Goodbye', text='Goodbye!')
            ]
        )
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='Buttons template', template=buttons_template)
        )
    # การตอบกลับแบบ Quick Reply
    elif user_text == "quickreply":
        quick_reply = QuickReply(items=[
            QuickReplyButton(action=MessageTemplateAction(label="Option 1", text="Option 1")),
            QuickReplyButton(action=MessageTemplateAction(label="Option 2", text="Option 2")),
        ])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Please choose an option:", quick_reply=quick_reply)
        )
    # การตอบกลับแบบ Carousel
    elif user_text == "carousel":
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(title="Option 1", text="Description 1", actions=[
                MessageTemplateAction(label='Select 1', text='You selected option 1')
            ]),
            CarouselColumn(title="Option 2", text="Description 2", actions=[
                MessageTemplateAction(label='Select 2', text='You selected option 2')
            ])
        ])
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='Carousel template', template=carousel_template)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Please send 'text', 'button', 'quickreply' or 'carousel'.")
        )


if __name__ == "__main__":
    app.run(port=5000)
