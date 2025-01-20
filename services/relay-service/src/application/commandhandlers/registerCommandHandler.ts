import { Injectable } from '@nestjs/common';

@Injectable()
export class RegisterCommandHandler {
    getHello(): string {
        return 'Hello World!';
    }
}
