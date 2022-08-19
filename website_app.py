import re

from duo import distance
import duo
import cv2
import eventlet
import send_wechat as sw
from top import open_top, close_top
from temperature import read_dht11_dat
from flask import Flask, render_template, Response, request

app = Flask(__name__)

cam_ava = True

humidity_l = 0
temperature = 0
result = False
flag = True


@app.route('/', methods=['GET', 'POST'])
def index():
    global result
    result = read_dht11_dat()
    eventlet.monkey_patch()

    with eventlet.Timeout(3, False):
        while not result:
            result = read_dht11_dat()

    if result:
        global humidity_l
        global temperature
        humidity_l, temperature = result
        return render_template('index.html', temp=str(temperature) + str(u'\u2103'), humidity=str(humidity_l) + '%',
                               height=str(30))
    else:
        return render_template('index.html', temp=str("传感器故障"), humidity=str("传感器故障"),
                               height=str(30))


@app.route("/open_top/", methods=['GET', 'POST'])
def openTop():
    forward_message = "开盖中"
    global flag
    if flag:
        flag = False
        open_top()
    flag = True
    if result:
        return render_template('index.html', temp=str(temperature) + str(u'\u2103'), humidity=str(humidity_l) + '%',
                               height=str(30), forward_message=forward_message)
    else:
        return render_template('index.html', temp=str("传感器故障"), humidity=str("传感器故障"),
                               height=str(30), forward_message=forward_message)


@app.route("/control/", methods=['GET', 'POST'])
def cont():
    return render_template('DTHweb.html')


@app.route("/close_top/", methods=['GET', 'POST'])
def closeTop():
    forward_message = "关盖中"
    global flag
    if flag:
        flag = False
        close_top()
    flag = True
    if result:
        return render_template('index.html', temp=str(temperature) + str(u'\u2103'), humidity=str(humidity_l) + '%',
                               height=str(30), forward_message=forward_message)
    else:
        return render_template('index.html', temp=str("传感器故障"), humidity=str("传感器故障"),
                               height=str(30), forward_message=forward_message)


@app.route("/change_bag/", methods=['GET', 'POST'])
def change_bag():
    forward_message = "换袋中"
    duo.change_bag()
    if result:
        return render_template('index.html', temp=str(temperature) + str(u'\u2103'), humidity=str(humidity_l) + '%',
                               height=str(30), forward_message=forward_message)
    else:
        return render_template('index.html', temp=str("传感器故障"), humidity=str("传感器故障"),
                               height=str(30), forward_message=forward_message)



@app.route("/input/", methods=['GET', 'POST'])
def add_post_address():
    local_address = request.form.get('address')

    if local_address not in sw.urls and re.match(r'^https?:/{2}\w.+$', local_address):
        sw.urls.append(local_address)
        return "添加成功！"
    elif local_address in sw.urls:
        return "url重复！"
    elif not re.match(r'^https?:/{2}\w.+$', local_address):
        return "不合法的地址！"


@app.route("/img/", methods=['GET', 'POST'])
def img():
    return render_template('img.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/release/', methods=['POST'])
def img_release():
    if result:
        return render_template('index.html', temp=str(temperature) + str(u'\u2103'), humidity=str(humidity_l) + '%',
                               height=str(30))
    else:
        return render_template('index.html', temp=str("传感器故障"), humidity=str("传感器故障"),
                               height=str(30))


def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=4000, debug=True)
