import proto_file_pb2_grpc, proto_file_pb2, utils, grpc, logging, pika, threading, sys, os
from concurrent import futures


# Rabbit MQ recieving messages
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='Defused-Mines', durable=True)
print(' [*] Waiting for mine defusal confirmations')
def callback(ch, method, properties, body: bytearray):
    print(f" [X] {body.decode()}")

channel.basic_consume(queue='Defused-Mines', on_message_callback=callback, auto_ack=True)

class MyGreeter(proto_file_pb2_grpc.MyGreeterServicer):   
    
    def GetMap(self, request, context):
        self.grid = utils.generate_map_grid()
        map_info = proto_file_pb2.MapInfo()
        
        row_size = len(self.grid)
        col_size = len(self.grid[0])
        
        map_info.row = row_size
        map_info.col = col_size
        
        self.mine_info_list = utils.generate_mines_txt(self.grid)              
        
        
        for row in self.grid:
            map_info_row = map_info.map.add()
            map_info_row.mine_val.extend(row)
                   
        return map_info

    def GetCommand(self, request, context):
        return proto_file_pb2.Commands(commands=utils.get_rover_commands(request.id))    


    def GetMineSerialNum(self, request, context):
        for mine_info in self.mine_info_list:           
            if ((mine_info[0] == request.row) and (mine_info[1] == request.col)):
                return proto_file_pb2.SerialNum(serialNum=mine_info[2])



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    proto_file_pb2_grpc.add_MyGreeterServicer_to_server(MyGreeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
    

    
if __name__ == '__main__':
    
    try:        
        logging.basicConfig()      
        threading.Thread(target=serve).start()
        channel.start_consuming()
    except:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    