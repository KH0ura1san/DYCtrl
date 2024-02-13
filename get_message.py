import json
import websockets
import asyncio
import redis

channel_name = 'douyin'    # 频道名称


def init_redis():  # 方法: 初始化Redis
    return redis.Redis(host='localhost', port=6379, decode_responses=True)


async def process():  # 方法: 获取弹幕并推送
    async with websockets.connect("ws://127.0.0.1:8888/", ping_interval=None) as ws:  # 防止WebSocket断开
        while True:
            try:
                message = await asyncio.wait_for(ws.recv(), timeout=30)  # 从WebSocket读取消息
                # print('Received: ' + message) # 原始消息
                message = json.loads(message)               # 以JSON格式解析消息
                if message.get("Type") == 1 or \
                        message.get("Type") == 2 or \
                        message.get("Type") == 5:           # 1: 弹幕  2: 点赞 5: 礼物
                    data = json.loads(message.get("Data"))  # 读取数据
                    speak_message = data.get("Content")     # 获取
                    r.publish(channel_name, speak_message)     # 推送数据到Redis频道
                    print("Published:", speak_message)
            except asyncio.TimeoutError:
                continue
            except websockets.exceptions.ConnectionClosed as e:
                print('连接已经关闭', e)
                continue


r = init_redis()                    # 初始化Redis连接
r.publish(channel_name, "")   # 发送空消息，创建频道
asyncio.run(process())              # 异步运行process()方法
