import time
from concurrent import futures
from threading import Thread

import grpc

from myapp.protos import helloworld_pb2_grpc, helloworld_pb2


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)


SERVER_ID = 1


class DemoServer(helloworld_pb2_grpc.GRPCDemoServicer):
    def SimpleMethod(self, request, context):
        print(
            "SimpleMethod called by client(%d) the message: %s"
            % (request.client_id, request.request_data)
        )
        response = helloworld_pb2.Response(
            server_id=SERVER_ID,
            response_data="Python server SimpleMethod Ok!!!!",
        )
        return response

    def ClientStreamingMethod(self, request_iterator, context):
        print("ClientStreamingMethod called by client...")
        for request in request_iterator:
            print(
                "recv from client(%d), message= %s"
                % (request.client_id, request.request_data)
            )
        response = helloworld_pb2.Response(
            server_id=SERVER_ID,
            response_data="Python server ClientStreamingMethod ok",
        )
        return response

    def ServerStreamingMethod(self, request, context):
        print(
            "ServerStreamingMethod called by client(%d), message= %s"
            % (request.client_id, request.request_data)
        )

        # create a generator
        def response_messages():
            for i in range(5):
                response = helloworld_pb2.Response(
                    server_id=SERVER_ID,
                    response_data="send by Python server, message=%d" % i,
                )
                yield response

        return response_messages()

    def BidirectionalStreamingMethod(self, request_iterator, context):
        print("BidirectionalStreamingMethod called by client...")

        # Open a sub thread to receive data
        def parse_request():
            for request in request_iterator:
                print(
                    "recv from client(%d), message= %s"
                    % (request.client_id, request.request_data)
                )

        t = Thread(target=parse_request)
        t.start()

        for i in range(5):
            yield helloworld_pb2.Response(
                server_id=SERVER_ID,
                response_data="send by Python server, message= %d" % i,
            )

        t.join()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    helloworld_pb2_grpc.add_GRPCDemoServicer_to_server(DemoServer(), server)

    server.add_insecure_port('[::]:50051')

    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
