import { Module } from '@nestjs/common';
// import { AppController } from './app.controller';
// import { RegisterController } from './presentations/controllers/RegisterController';
// import { AppService } from './app.service';
// import { RegisterCommandHandler } from './application/commandhandlers/registerCommandHandler';
import { WebsocketGateway } from './presentations/gateways/websocket.gateway'
import { CqrsModule } from '@nestjs/cqrs';
import { RegisterCommandHandler } from './application/commandhandlers/registerCommandHandler'
import { RequestCommandHandler } from './application/commandhandlers/requestCommandHandler'
import { ResponseCommandHandler } from './application/commandhandlers/responseCommandHandler'

@Module({
  imports: [CqrsModule.forRoot()],
  controllers: [],
  exports: [WebsocketGateway],
  providers: [WebsocketGateway, RegisterCommandHandler, RequestCommandHandler, ResponseCommandHandler]
})
export class AppModule {}
