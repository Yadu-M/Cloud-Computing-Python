import grpc
import proto_file_pb2
import proto_file_pb2_grpc
from concurrent import futures
import logging
import 'lab1/main.'

class MyGreeter(proto_file_pb2_grpc.MyGreeterServicer):
    def GetMap(self, request, context):
        pass
    
    def GetCommands(self, request, context):
        return proto_file_pb2.Commands(commands="your_command_here")    
    
    def GetMineSerialNum(self, request, context):
        pass

    def BotSuccees(self, request, context):
        pass

    def MinePin(self, request, context):
        pass
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    proto_file_pb2_grpc.add_MyGreeterServicer_to_server(MyGreeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
    
if __name__ == '__main__':
    logging.basicConfig()
    serve()