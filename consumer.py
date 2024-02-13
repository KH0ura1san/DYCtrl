import pyautogui
import redis

channel_name = 'douyin'             # 频道名
key_list = ('w', 's', 'a', 'd')     # 允许指令列表


def init_redis():   # 初始化Redis连接
    return redis.Redis(host='localhost', port=6379, decode_responses=True)


def control(key_name):  # 指令控制处理
    key_name = key_name.lower()
    if key_name in key_list:
        print("Command Running:{}".format(key_name))
        pyautogui.keyDown(key_name)                 # 按键
        pyautogui.keyUp(key_name)                   # 按键
        print("Command Finished:{}".format(key_name))


if __name__ == '__main__':
    r = init_redis()                # 初始化Redis连接
    pub = r.pubsub()                # 初始化订阅器
    pub.subscribe(channel_name)     # 订阅频道
    msg_stream = pub.listen()       # 监听频道
    print("Listening...")
    for msg in msg_stream:
        if msg["type"] == "message":
            for i in msg["data"]:
                control(i)
        elif msg["type"] == "subscribe":
            print("Channel", str(msg["channel"]), 'Subscribed!')
