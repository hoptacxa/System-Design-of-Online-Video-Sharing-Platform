
import { Injectable } from '@nestjs/common';
import { RequestAggregate } from '../../../domain/aggregates/requestAggregate';
import { RequestUuid as Uuid } from '../../../domain/valueobjects/requestUuid'

@Injectable()
export class InMemoryRequestWriteRepository {
    private readonly requests: Map<string, any>;

    constructor() {
        this.requests = new Map<string, any>();
    }

    // Save a new request to the repository
    async save(request: RequestAggregate): Promise<void> {
        const uuid = request.uuid.getValue();
        if (this.requests.has(uuid)) {
            throw new Error(`Request with UUID ${uuid} already exists.`);
        }
        let {
            requesterId,
            providerId,
            payload,
            status,
        } = request;
        this.requests.set(uuid, {
            requesterId: requesterId.value,
            providerId: providerId.value,
            payload: payload.getData(),
            status: status
        })

        // console.log(this.requests)
    }

    // Find a request by UUID
    async findById(uuid: Uuid): Promise<RequestAggregate | null> {
        const request = this.requests.get(uuid.getValue());
        return request || null;
    }

    // Update an existing request
    async update(request: RequestAggregate): Promise<void> {
        const uuid = request.uuid.getValue();
        if (!this.requests.has(uuid)) {
            throw new Error(`Request with UUID ${uuid} does not exist.`);
        }
        this.requests.set(uuid, request);
    }

    // Delete a request by UUID
    async delete(uuid: Uuid): Promise<void> {
        if (!this.requests.has(uuid.getValue())) {
            throw new Error(`Request with UUID ${uuid.getValue()} does not exist.`);
        }
        this.requests.delete(uuid.getValue());
    }

    // Retrieve all requests (for debugging or testing purposes)
    async findAll(): Promise<RequestAggregate[]> {
        return Array.from(this.requests.values());
    }
}