import { CommandHandler, ICommandHandler } from '@nestjs/cqrs';
import { RegisterCommand } from '../commands/registerCommand';
import { InMemoryPeerReadRepository } from '../../infrastructure/repositories/inMemoryPeerReadRepository';
import { InMemoryPeerWriteRepository } from '../../infrastructure/repositories/inMemoryPeerWriteRepository';
import { NodeId } from '../../domain/valueobjects/nodeId';
import { PeerAddress } from '../../domain/valueobjects/peerAddress';
import { StorageCapacity } from '../../domain/valueobjects/storageCapacity';

@CommandHandler(RegisterCommand)
export class RegisterCommandHandler implements ICommandHandler<RegisterCommand> {
    constructor(
        private readonly peerReadRepository: InMemoryPeerReadRepository,
        private readonly peerWriteRepository: InMemoryPeerWriteRepository
    ) {}

    async execute(command: RegisterCommand): Promise<any> {
    console.log(command)
        const { peerId, accessKeyId, accessSecretKey, peerAddress, storageCapacity } = command;

        // Validate user credentials
        if (!(await this.validateUser(accessKeyId, accessSecretKey))) {
            throw new Error('Invalid credentials');
        }

        // Validate peer ownership
        if (!(await this.validatePeer(accessKeyId, peerId))) {
            throw new Error('Unauthorized peer');
        }

        // Check if peer is already registered
        const existingPeer = await this.peerReadRepository.findById(new NodeId(peerId));
        if (existingPeer) {
            throw new Error(`Peer ${peerId} is already registered`);
        }

        // Register the peer
        const nodeId = new NodeId(peerId);
        const address = new PeerAddress(peerAddress);
        const capacity = new StorageCapacity(storageCapacity);

        await this.peerWriteRepository.addPeer(
            nodeId,
            address,
            capacity,
        );

        return { message: 'Peer registered successfully' };
    }

    private async validateUser(accessKeyId: string, accessSecretKey: string): Promise<boolean> {
        // Implement actual user validation logic (e.g., check database or external service)
        // Placeholder logic:
        return accessKeyId === 'validUser' && accessSecretKey === 'validSecret';
    }

    private async validatePeer(accessKeyId: string, peerId: string): Promise<boolean> {
        // Implement peer ownership validation logic
        // Placeholder logic:
        const userPeers = await this.peerReadRepository.findByUserId(accessKeyId);
        return userPeers.some((peer) => peer.nodeId.value === peerId);
    }
}
