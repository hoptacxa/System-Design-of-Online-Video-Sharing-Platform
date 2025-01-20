import {
    SubscribeMessage,
    WebSocketGateway,
    OnGatewayInit,
    OnGatewayConnection,
    OnGatewayDisconnect,
    MessageBody,
    ConnectedSocket,
    WebSocketServer,
} from '@nestjs/websockets';
import { Logger } from '@nestjs/common';
import { Server, Socket } from 'socket.io';

@WebSocketGateway({
    cors: {
        origin: '*',
    },
})
export class WebsocketGateway implements OnGatewayInit, OnGatewayConnection, OnGatewayDisconnect {
    @WebSocketServer() server: Server;
    private readonly logger = new Logger(WebsocketGateway.name);

    afterInit(server: Server) {
        this.logger.log('WebSocket Gateway initialized at');
        server.on('connected', function(){
            console.log("a")
        })
    }
    handleConnection(@ConnectedSocket() client: Socket) {
        this.logger.log('New client connected');
        client.send(JSON.stringify({ type: '' }));
    }
    handleDisconnect(@ConnectedSocket() client: Socket) {
        this.logger.log('Client disconnected');
    }
}