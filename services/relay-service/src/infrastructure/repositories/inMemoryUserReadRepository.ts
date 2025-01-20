interface User {
    userId: string,
    accessKeys: Array<any>,
    peers: string[];
}

export class InMemoryUserReadRepository {
    private readonly users: Map<string, User>;

    constructor(initialUsers: User[] = []) {
        this.users = new Map();
        initialUsers.forEach((user) => this.users.set(user.userId, user));
    }

    /**
     * Finds a user by an access key and validates the secret key.
     * @param {string} accessKeyId - The access key ID.
     * @param {string} accessSecretKey - The access secret key.
     * @returns {Promise<User | null>} - The user if valid, otherwise null.
     */
    async findByAccessKey(accessKeyId: string, accessSecretKey: string): Promise<User | null> {
        for (const user of this.users.values()) {
            const accessKey = user.accessKeys.find(
                (key) => key.accessKeyId === accessKeyId && key.accessSecretKey === accessSecretKey,
            );
            if (accessKey) {
                return user;
            }
        }
        return null;
    }

    /**
     * Finds a user by an access key ID (ignores secret key).
     * @param {string} accessKeyId - The access key ID.
     * @returns {Promise<User | null>} - The user if found, otherwise null.
     */
    async findByAccessKeyOnly(accessKeyId: string): Promise<User | null> {
        for (const user of this.users.values()) {
            if (user.accessKeys.some((key) => key.accessKeyId === accessKeyId)) {
                return user;
            }
        }
        return null;
    }

    /**
     * Returns all users stored in the repository.
     * @returns {Promise<User[]>} - An array of all user objects.
     */
    async findAll(): Promise<User[]> {
        return Array.from(this.users.values());
    }
}
