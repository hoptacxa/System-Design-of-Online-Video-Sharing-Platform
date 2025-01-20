import { Controller, Get } from '@nestjs/common';
import { RegisterCommandHandler } from '../../application/commandhandlers/registerCommandHandler';

@Controller()
export class RegisterController {
  constructor(private readonly registerCommandHandler: RegisterCommandHandler) {}

  @Get()
  getHello(): string {
    return ''
  }
}
