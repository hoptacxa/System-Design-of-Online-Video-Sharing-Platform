
import { Injectable } from '@nestjs/common';

@Injectable()
export class InMemoryRequestReadRepository {
    
    constructor(private readonly requests: Map<string, any>) {
    }

    getByUuid(uuid: string) {
        return this.requests.get(uuid)
    }
}
