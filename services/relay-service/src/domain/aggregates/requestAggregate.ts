import { NodeId } from '../valueobjects/nodeId'
import { RequestUuid } from '../valueobjects/requestUuid';
import { RequestPayload } from '../valueobjects/requestPayload';

export enum RequestStatus {
    PENDING = 'PENDING',
    COMPLETED = 'COMPLETED',
    FAILED = 'FAILED',
}

export class RequestAggregate {
    constructor(
        public uuid: RequestUuid,
        public requesterId: NodeId,
        public providerId: NodeId,
        public payload: RequestPayload,
        public status: RequestStatus = RequestStatus.PENDING
    ) {
    }

    getStatus(): RequestStatus {
        return this.status;
    }

    updateStatus(newStatus: RequestStatus): void {
        if (newStatus === this.status) {
            throw new Error(`Request is already in status: ${newStatus}`);
        }

        if (this.status === RequestStatus.COMPLETED) {
            throw new Error('Cannot change status of a completed request.');
        }

        this.status = newStatus;
    }

    validate(): void {
        // No explicit validation needed here; VOs already validate themselves
    }
}
