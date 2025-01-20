const UserRepository = require('../../infrastructure/repositories/userRepository');
const PeerRepository = require('../../infrastructure/repositories/peerRepository');
const UserAggregate = require('../../domain/aggregates/userAggregate');
const Peer = require('../../domain/entities/peer');

class RegisterHandler {
    constructor() {
        this.userRepository = new UserRepository();
        this.peerRepository = new PeerRepository();
    }

    execute(command) {
        const { peerId, accessKeyId, accessSecretKey, socket } = command;

        // Lấy User từ repository
        const userEntity = this.userRepository.findUserById(accessKeyId);
        if (!userEntity || userEntity.secretKey !== accessKeyId) {
            return { success: false, message: 'Invalid credentials' };
        }

        // Tạo Aggregate cho User
        const userAggregate = new UserAggregate(userEntity);

        // Kiểm tra quyền sở hữu Peer
        if (!userAggregate.ownsPeer(peerId)) {
            return { success: false, message: 'Unauthorized peer' };
        }

        // Tạo thực thể Peer và thêm vào repository
        const peerEntity = new Peer(peerId, accessKeyId, socket);
        this.peerRepository.addPeer(peerEntity);

        // Thêm Peer vào Aggregate
        userAggregate.addPeer(peerEntity);

        console.log(`Peer registered: ${peerId} (User: ${accessKeyId})`);

        return { success: true, message: 'Peer registered successfully' };
    }
}

module.exports = RegisterHandler;