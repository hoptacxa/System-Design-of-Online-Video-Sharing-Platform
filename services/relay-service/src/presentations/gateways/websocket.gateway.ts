import { WebSocketGateway, OnGatewayInit, OnGatewayConnection, OnGatewayDisconnect, WebSocketServer, SubscribeMessage, MessageBody, ConnectedSocket } from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { Logger } from '@nestjs/common';
import { CommandBus } from '@nestjs/cqrs';
import { RegisterCommand } from '../../application/commands/registerCommand'
import { RequestCommand } from '../../application/commands/requestCommand';
import { ResponseCommand } from '../../application/commands/responseCommand';
import { v4 as uuidv4 } from 'uuid';

@WebSocketGateway({
    cors: {
        origin: '*',
    },
})
export class WebsocketGateway implements OnGatewayInit, OnGatewayConnection, OnGatewayDisconnect {
    @WebSocketServer() server: Server;
    private clients = new Map<string, Array<Socket>>();
    private readonly logger = new Logger(WebsocketGateway.name);

    constructor(private readonly commandBus: CommandBus) {}

    getClients(nodeId: string): Array<Socket> | undefined {
        return this.clients.get(nodeId);
    }
    afterInit(server: Server) {
        this.logger.log('WebSocket Gateway initialized');
    }
    // handleConnection(@ConnectedSocket() client: Socket) {
    //     this.logger.log(`New client connected: ${client.id}`);
    // }
    handleDisconnect(@ConnectedSocket() client: Socket) {
        // for (const [nodeId, storedClient] of this.clients.entries()) {
        //     if (storedClient.id === client.id) {
        //         // this.clients.delete(nodeId);
        //         this.logger.log(`Client disconnected: ${client.id} (nodeId: ${nodeId})`);
        //         break;
        //     }
        // }
    }

    async handleConnection(@ConnectedSocket() client: Socket) {
        try {
            let {
                peerId,
                accessKeyId,
                accessSecretKey,
                storageCapacity,
                peerAddress,
            } = client.handshake.auth;
            if (typeof peerId !== 'string') {
                throw new Error('PeerId must be string')
            }
            const result = await this.commandBus.execute(new RegisterCommand(peerId, accessKeyId, accessSecretKey, storageCapacity, peerAddress));
            console.log(client.handshake.auth, accessKeyId)
            if (this.clients.has(peerId)) {
                let existsClients = this.clients.get(peerId)
                existsClients.push(client)
                this.clients.set(peerId, existsClients)
            }else{
                this.clients.set(peerId, [client]);
            }
            client.emit('register-success', result);
        } catch (error) {
            this.logger.error(error.message + " in " + error.stack);
            client.emit('register-error', { message: error.message });
        }
    }

    @SubscribeMessage('request')
    async handleRequest(@MessageBody() data: { peerId: string; to: string; payload: any }, @ConnectedSocket() client: Socket) {
        try {
            let uuid: string = uuidv4();
            const result = await this.commandBus.execute(new RequestCommand(uuid, data.peerId, data.to, data.payload));
            client.emit('request-success', result);
        } catch (error) {
            console.log(error)
            this.logger.error(error)
            client.emit('request-error', { message: error.message });
        }
    }

    @SubscribeMessage('response')
    async handleResponse(@MessageBody() data: { Body: any, uuid: string }, @ConnectedSocket() client: Socket) {
        try {
            await this.commandBus.execute(new ResponseCommand(data.uuid, data.Body));
        } catch (error) {
            console.log(error)
            this.logger.error(error)
            client.emit('response-error', { message: error.message });
        }
    }
}
