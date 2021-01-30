import asyncio
import socketio


sio = socketio.Client()


@sio.event
def connect():
    print('connected to server')
    sio.emit('testing', {'data' : "Client data"})


@sio.event
def disconnect():
    print('disconnected from server')


@sio.event
def hello(a, b, c):
    print(a, b, c)


if __name__ == '__main__':
    sio.connect('http://localhost:5000')
    sio.wait()

# sio = socketio.AsyncClient()

# # async def send_ping():
# #     print ('sending ping')
# #     await sio.emit('testing', {'data' : "Client data"})

# # @sio.event
# # async def connect():
# #     print('connected to server')
# #     await send_ping()


# # @sio.event
# # async def disconnect():
# #     print('disconnected from server')


# # @sio.event
# # def hello(a, b, c):
# #     print(a, b, c)


# # async def start_server():
# #     await sio.connect('http://localhost:5000')
# #     await sio.wait()


# # if __name__ == '__main__':
# #     asyncio.run(start_server())