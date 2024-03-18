import utils, proto_file_pb2, proto_file_pb2_grpc, grpc, logging, pika


# Establishing connection with RabbitMQ server

connectionMQ = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channelMQ = connectionMQ.channel()
channelMQ.queue_declare(queue='Demine-Queue', durable=True)


def getRoverID() -> int:
    prompt = 'Enter rover id: '
    while True:
        try:
            rover_id = input(prompt)
            if ((int (rover_id) > 10) or (int (rover_id) < 1)):
                raise ValueError
            break
        except ValueError:
            prompt = 'Please rover id: '
            pass
    return rover_id


def getMapArray(mapObj) -> list[list[int]]:
    row_count = mapObj.row
    col_count = mapObj.col    
    mapArray = [[0 for _ in range(col_count)] for _ in range(row_count)]
    
    for row_idx, row in enumerate(mapObj.map):
        for col_idx, mineVal in enumerate(row.mine_val):
            mapArray[row_idx][col_idx] = mineVal
            
    return mapArray
    

def main():    
    
    with grpc.insecure_channel('localhost:50051') as channel:    
            
        stub = proto_file_pb2_grpc.MyGreeterStub(channel)

        roverId = getRoverID()  # Getting rover id from CLI
        mapObj = stub.GetMap(proto_file_pb2.Empty())  # Getting map from server
        grid = getMapArray(mapObj)  # Turning into 2d list
        commands = stub.GetCommand(proto_file_pb2.RoverID(id=roverId)).commands  # Getting commands from server    
        
        
        #---------------Traversing The Map ------------------#
        
        
        currDirection = 'SOUTH'
        currRow = 0
        currCol = 0
        MAP_ROW_SIZE = len(grid)
        MAP_COL_SIZE = len(grid[0])
        
        for command in commands:
            if command == 'L' or command == 'R':
                currDirection = utils.update_direction(curr_direction=currDirection, move=command)
            elif command == 'M':
                update = False       
                
                if currDirection == "SOUTH":
                    if currRow < (MAP_ROW_SIZE - 1):
                        currRow += 1
                        update = True
                elif currDirection == "WEST":
                    if currCol > 0:
                        currCol -= 1
                        update = True
                elif currDirection == "NORTH":
                    if currRow > 0:  
                        currRow -= 1
                        update = True
                elif currDirection == "EAST":
                    if currCol < (MAP_COL_SIZE - 1):
                        currCol += 1
                        update = True
                
                if update:            
                    if (grid[currRow][currCol]):  # If a mine exists
                        serialNum = stub.GetMineSerialNum(proto_file_pb2.MineLocation(row=currRow, col=currCol)).serialNum
                        messageToSend = f'{currRow} {currCol} {serialNum}'
                        
                        # Sending demine request
                        channelMQ.basic_publish(
                            exchange='',
                            routing_key='Demine-Queue',
                            body=messageToSend,
                            properties=pika.BasicProperties(
                                delivery_mode=pika.DeliveryMode.Persistent
                            )
                            
                        )
                        print(f'Sent mine info to deminer\nBody: "{messageToSend}"')
                        # print('Waiting for mine defuse...')
                        
                        # def ack_handler(ch, method, properties, body):
                        #     print('Mine has been defused')
                        #     grid[currRow][currCol] = 0
                        #     channelMQ.stop_consuming()
                            
                        # channelMQ.basic_consume(queue='Demine-Queue', on_message_callback=ack_handler, auto_ack=True)
                        # channelMQ.start_consuming()
                        
                
    channelMQ.close()


if __name__ == "__main__":
    logging.basicConfig()
    main()