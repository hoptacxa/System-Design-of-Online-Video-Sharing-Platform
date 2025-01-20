import { Module } from '@nestjs/common';
// import { AppController } from './app.controller';
// import { RegisterController } from './presentations/controllers/RegisterController';
// import { AppService } from './app.service';
// import { RegisterCommandHandler } from './application/commandhandlers/registerCommandHandler';
import { WebsocketGateway } from './presentations/gateways/websocket.gateway'
import { WebSocketGateway } from '@nestjs/websockets';

@Module({
  imports: [],
  controllers: [],
  exports: [WebsocketGateway],
  providers: [WebsocketGateway],
})
export class AppModule {}
