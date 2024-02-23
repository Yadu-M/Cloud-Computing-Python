import logging

import grpc
import proto_file_pb2
import proto_file_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = proto_file_pb2_grpc.MyGreeterStub(channel)
        
        # Ensure that the request message type is correct
        request = proto_file_pb2.RoverID(id="1")
        
        # Call the GetCommands RPC method and handle the response
        response = stub.GetCommands(request)
        
        # Print or handle the response according to your application's logic
        print(response)
        
if __name__ == '__main__':
    logging.basicConfig()
    run()