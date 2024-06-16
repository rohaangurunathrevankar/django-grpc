import grpc
import time
from myapp.protos import helloworld_pb2, helloworld_pb2_grpc

CLIENT_ID = 1


# def simple_method(stub):
#     print("--------------Call SimpleMethod Begin--------------")
#     request = helloworld_pb2.Request(
#         client_id=CLIENT_ID, request_data="called by Python client"
#     )
#     response = stub.SimpleMethod(request)
#     print(
#         "resp from server(%d), the message=%s"
#         % (response.server_id, response.response_data)
#     )
#     print("--------------Call SimpleMethod Over---------------")


# # stream-unary (In a single call, the client can transfer data to the server several times,
# # but the server can only return a response once.)
# def client_streaming_method(stub):
#     print("--------------Call ClientStreamingMethod Begin--------------")
#
#     # 创建一个生成器
#     # create a generator
#     def request_messages():
#         for i in range(5):
#             request = helloworld_pb2.Request(
#                 client_id=CLIENT_ID,
#                 request_data="called by Python client, message:%d" % i,
#             )
#             yield request
#
#     response = stub.ClientStreamingMethod(request_messages())
#     print(
#         "resp from server(%d), the message=%s"
#         % (response.server_id, response.response_data)
#     )
#     print("--------------Call ClientStreamingMethod Over---------------")
#
#
# # unary-stream (In a single call, the client can only transmit data to the server at one time,
# # but the server can return the response many times.)
# def server_streaming_method(stub):
#     print("--------------Call ServerStreamingMethod Begin--------------")
#     request = helloworld_pb2.Request(
#         client_id=CLIENT_ID, request_data="called by Python client"
#     )
#     response_iterator = stub.ServerStreamingMethod(request)
#     for response in response_iterator:
#         print(
#             "recv from server(%d), message=%s"
#             % (response.server_id, response.response_data)
#         )
#
#     print("--------------Call ServerStreamingMethod Over---------------")
#
#
# # stream-stream (In a single call, both client and server can send and receive data
# # to each other multiple times.)
# def bidirectional_streaming_method(stub):
#     print(
#         "--------------Call BidirectionalStreamingMethod Begin---------------"
#     )
#
#     # create a generator
#     def request_messages():
#         for i in range(5):
#             request = helloworld_pb2.Request(
#                 client_id=CLIENT_ID,
#                 request_data="called by Python client, message: %d" % i,
#             )
#             yield request
#             time.sleep(1)
#
#     response_iterator = stub.BidirectionalStreamingMethod(request_messages())
#     for response in response_iterator:
#         print(
#             "recv from server(%d), message=%s"
#             % (response.server_id, response.response_data)
#         )
#
#     print("--------------Call BidirectionalStreamingMethod Over---------------")
#

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='world'))
        # stub1 = helloworld_pb2_grpc.GRPCDemoStub(channel)
        #
        # simple_method(stub1)
        #
        # # client_streaming_method(stub1)
        #
        # # server_streaming_method(stub1)
        #
        # # bidirectional_streaming_method(stub1)
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    run()
