import { WebSocketGateway, OnGatewayInit, OnGatewayConnection, OnGatewayDisconnect, WebSocketServer, SubscribeMessage, MessageBody, ConnectedSocket } from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { Logger } from '@nestjs/common';
import { CommandBus } from '@nestjs/cqrs';
import { RegisterCommand } from '../../application/commands/registerCommand'
import { RequestCommand } from '../../application/commands/requestCommand';
import { ResponseCommand } from '../../application/commands/responseCommand';
import { FindCidCommand } from '../../application/commands/findCidCommand';

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
    getAllClients() {
        return this.clients;
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
            const { peerId, accessKeyId, accessSecretKey, storageCapacity, peerAddress } = client.handshake.auth;
            if (typeof peerId !== 'string') {
                this.logger.debug(client.handshake)
                // handle reconnect
                throw new Error('PeerId must be string')
            }

            // Check if client already exists
            let existingClients = this.clients.get(peerId) || [];
            const existingClientIndex = existingClients.findIndex(c => c.id === client.id);

            if (existingClientIndex === -1) {
                // New connection
                const result = await this.commandBus.execute(new RegisterCommand(peerId, accessKeyId, accessSecretKey, storageCapacity, peerAddress));
                existingClients.push(client);
                this.clients.set(peerId, existingClients);
                client.emit('register-success', result);
                this.logger.log(`Client connected: ${client.id} (peerId: ${peerId})`);
            } else {
                // Reconnection
                this.logger.error(`Reconnection detected for client: ${client.id} (peerId: ${peerId})`);
                throw new Error(`Reconnection detected for client: ${client.id} (peerId: ${peerId})`)
            }
        } catch (error) {
            this.logger.error(`Connection error: ${error.message}`, error.stack);
            client.emit('register-error', { message: error.message });
        }
    }

    @SubscribeMessage('find-cid')
    async handleFindCid(@MessageBody() data: { peerId: string; to: string; payload: any; uuid: string }, @ConnectedSocket() client: Socket) {
        try {
            const result = await this.commandBus.execute(new FindCidCommand(data.uuid, data.peerId, data.to, data.payload));
            client.emit('find-cid-success', result);
        } catch (error) {
            console.log(error)
            this.logger.error(error)
            client.emit('find-cid-error', { message: error.message });
        }
    }

    @SubscribeMessage('request')
    async handleRequest(@MessageBody() data: { peerId: string; to: string; payload: any; uuid: string }, @ConnectedSocket() client: Socket) {
        try {
            const result = await this.commandBus.execute(new RequestCommand(data.uuid, data.peerId, data.to, data.payload));
            client.emit('request-success', result);
        } catch (error) {
            console.log(error)
            this.logger.error(error)
            client.emit('request-error', { message: error.message });
        }
    }

    @SubscribeMessage('response')
    async handleResponse(@MessageBody() data: { Body: any, uuid: string }, @ConnectedSocket() client: Socket) {
        console.log("res")
        try {
            await this.commandBus.execute(new ResponseCommand(data.uuid, data.Body));
        } catch (error) {
            console.log(error)
            this.logger.error(error)
            client.emit('response-error', { message: error.message });
        }
    }
}
