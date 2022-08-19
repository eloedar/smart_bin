from flask import Flask
from flask import request

from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

from duo import change_bag
from top import open_top, close_top, get_dis

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        token = 'Password'  # 注意！！！！！这里要和你公众号的一致

        echostr = request.args.get('echostr')

        try:
            check_signature(token, signature, timestamp, nonce)
        except InvalidSignatureException:
            print('error')

        # if signature == sha1_signature:
        return echostr
    elif request.method == 'POST':
        msg = parse_message(request.get_data())
        if msg.type == 'text':
            print(msg.content)
            if msg.content == "开启":
                open_top()
                reply = create_reply('收到，操作已发送', msg)
            if msg.content == "关闭":
                close_top()
                reply = create_reply('收到，操作已发送', msg)
            if msg.content == "换袋":
                change_bag()
                reply = create_reply('收到，操作已发送', msg)
    return reply.render()


if __name__ == '__main__':
    app.run(
        host='0.0.0.0', port=8080, debug=True,
    )
