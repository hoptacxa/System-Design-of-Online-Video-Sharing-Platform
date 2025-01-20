const { users } = require('../database');
const User = require('../../domain/entities/user');

class UserRepository {
    findUserById(userId) {
        const userData = users[userId];
        if (!userData) return null;

        return new User(userId, userData.accessSecretKey, userData.peers);
    }
}

module.exports = UserRepository;