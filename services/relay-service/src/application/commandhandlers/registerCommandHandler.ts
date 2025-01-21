import { CommandHandler, ICommandHandler } from '@nestjs/cqrs';
import { RegisterCommand } from '../commands/registerCommand';
import { InMemoryPeerReadRepository } from '../../infrastructure/repositories/inMemoryPeerReadRepository';
import { InMemoryPeerWriteRepository } from '../../infrastructure/repositories/inMemoryPeerWriteRepository';
import { InMemoryUserReadRepository } from '../../infrastructure/repositories/inMemoryUserReadRepository';
import { NodeId } from '../../domain/valueobjects/nodeId';
import { PeerAddress } from '../../domain/valueobjects/peerAddress';
import { StorageCapacity } from '../../domain/valueobjects/storageCapacity';

@CommandHandler(RegisterCommand)
export class RegisterCommandHandler implements ICommandHandler<RegisterCommand> {
    constructor(
        private readonly peerReadRepository: InMemoryPeerReadRepository,
        private readonly peerWriteRepository: InMemoryPeerWriteRepository,
        private readonly userReadRepository: InMemoryUserReadRepository,
    ) {}

    async execute(command: RegisterCommand): Promise<any> {
        const { peerId, accessKeyId, accessSecretKey, peerAddress, storageCapacity } = command;

        // Validate user credentials
        const user = await this.userReadRepository.findByAccessKey(accessKeyId, accessSecretKey);
        if (!user) {
            // throw new Error('Invalid credentials');
        }

        // Validate peer ownership
        // if (!user.peers.includes(peerId)) {
            // throw new Error('Unauthorized peer');
        // }

        // Check if peer is already registered
        const existingPeer = await this.peerReadRepository.findById(new NodeId(peerId));
        if (existingPeer) {
            // throw new Error(`Peer ${peerId} is already registered`);
        }

        // Register the peer
        const nodeId = new NodeId(peerId);
        const address = new PeerAddress(peerAddress);
        const capacity = new StorageCapacity(storageCapacity);

        await this.peerWriteRepository.addPeer(nodeId, address, capacity);

        return { message: 'Peer registered successfully' };
    }
}
