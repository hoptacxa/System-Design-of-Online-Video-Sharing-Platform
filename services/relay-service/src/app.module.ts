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
import { InMemoryPeerWriteRepository } from './infrastructure/repositories/inMemoryPeerWriteRepository'
import { InMemoryPeerReadRepository } from './infrastructure/repositories/inMemoryPeerReadRepository';
const sharedPeers = new Map();

@Module({
  imports: [CqrsModule.forRoot()],
  controllers: [],
  exports: [WebsocketGateway],
  providers: [WebsocketGateway, RegisterCommandHandler, RequestCommandHandler, ResponseCommandHandler,
    // Repositories
    {
      provide: InMemoryPeerReadRepository,
      useFactory: () => new InMemoryPeerReadRepository(sharedPeers),
    },
    {
      provide: InMemoryPeerWriteRepository,
      useFactory: () => new InMemoryPeerWriteRepository(sharedPeers),
    },

  ]
})
export class AppModule { }
