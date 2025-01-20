import { WebSocketGateway, OnGatewayInit, OnGatewayConnection, OnGatewayDisconnect, WebSocketServer, SubscribeMessage, MessageBody, ConnectedSocket } from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { Logger } from '@nestjs/common';
import { CommandBus } from '@nestjs/cqrs';
import { RegisterCommand } from '../../application/commands/registerCommand'
import { RequestCommand } from '../../application/commands/requestCommand';
import { ResponseCommand } from '../../application/commands/responseCommand';

@WebSocketGateway({
    cors: {
        origin: '*',
    },
})
export class WebsocketGateway implements OnGatewayInit, OnGatewayConnection, OnGatewayDisconnect {
    @WebSocketServer() server: Server;
    private readonly logger = new Logger(WebsocketGateway.name);

    constructor(private readonly commandBus: CommandBus) {}

    afterInit(server: Server) {
        this.logger.log('WebSocket Gateway initialized');
    }
    handleConnection(@ConnectedSocket() client: Socket) {
        this.logger.log(`New client connected: ${client.id}`);
    }
    handleDisconnect(@ConnectedSocket() client: Socket) {
        this.logger.log(`Client disconnected: ${client.id}`);
    }

    @SubscribeMessage('register')
    async handleRegister(@MessageBody() data: { peerId: string; accessKeyId: string; accessSecretKey: string, storageCapacity: string, peerAddress: string }, @ConnectedSocket() client: Socket) {
        try {
            const result = await this.commandBus.execute(new RegisterCommand(data.peerId, data.accessKeyId, data.accessSecretKey, data.storageCapacity, data.peerAddress));
            client.emit('success', result);
        } catch (error) {
            client.emit('error', { message: error.message });
        }
    }

    @SubscribeMessage('request')
    async handleRequest(@MessageBody() data: { peerId: string; to: string; payload: any }, @ConnectedSocket() client: Socket) {
        try {
            const result = await this.commandBus.execute(new RequestCommand(data.peerId, data.to, data.payload));
            client.emit('success', result);
        } catch (error) {
            client.emit('error', { message: error.message });
        }
    }

    @SubscribeMessage('response')
    async handleResponse(@MessageBody() data: { peerId: string; to: string; payload: any }, @ConnectedSocket() client: Socket) {
        try {
            const result = await this.commandBus.execute(new ResponseCommand(data.peerId, data.to, data.payload));
            client.emit('success', result);
        } catch (error) {
            client.emit('error', { message: error.message });
        }
    }
}
