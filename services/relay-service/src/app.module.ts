import { Module } from '@nestjs/common';
// import { AppController } from './app.controller';
import { RegisterController } from './presentations/controllers/RegisterController';
// import { AppService } from './app.service';
import { RegisterCommandHandler } from './application/commandhandlers/registerCommandHandler';

@Module({
  imports: [],
  controllers: [RegisterController],
  providers: [RegisterCommandHandler],
})
export class AppModule {}
