import { Injectable } from '@nestjs/common';

@Injectable()
export class RegisterCommandHandler {
    handle(registerCommand): string {
        return 'Hello World!';
    }
}
