
import { Injectable } from '@nestjs/common';
import { RequestAggregate } from '../../domain/aggregates/requestAggregate';
import { RequestUuid as Uuid } from '../../domain/valueobjects/requestUuid'
import { NodeId } from '../../domain/valueobjects/nodeId';
import { RequestPayload } from '../../domain/valueobjects/requestPayload';

@Injectable()
export class InMemoryRequestWriteRepository {
    // private readonly requests: Map<string, any>;

    constructor(private readonly requests: Map<string, {requesterId: string, providerId: string, payload: object, status: string}>) {
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
    }

    // Find a request by UUID
    async findById(uuid: Uuid): Promise<RequestAggregate | null> {
        const request = this.requests.get(uuid.getValue());
        return request ? new RequestAggregate(
            uuid, 
            new NodeId(request.requesterId), 
            new NodeId(request.providerId), 
            new RequestPayload(request.payload)
        ) : null
    }

    // Update an existing request
    async update(request: RequestAggregate): Promise<void> {
        const uuid = request.uuid.getValue();
        if (!this.requests.has(uuid)) {
            throw new Error(`Request with UUID ${uuid} does not exist.`);
        }
        this.requests.set(uuid, {
            requesterId: request.requesterId.value,
            providerId: request.providerId.value,
            payload: request.payload,
            status: request.status,
        });
    }

    // Delete a request by UUID
    async delete(uuid: Uuid): Promise<void> {
        if (!this.requests.has(uuid.getValue())) {
            throw new Error(`Request with UUID ${uuid.getValue()} does not exist.`);
        }
        this.requests.delete(uuid.getValue());
    }
}