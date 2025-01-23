import { Module } from '@nestjs/common';
// import { AppController } from './app.controller';
// import { RegisterController } from './presentations/controllers/RegisterController';
// import { AppService } from './app.service';
// import { RegisterCommandHandler } from './application/commandhandlers/registerCommandHandler';
import { WebsocketGateway } from './presentations/gateways/websocket.gateway'
import { CqrsModule } from '@nestjs/cqrs';
import { RegisterCommandHandler } from './application/commandhandlers/registerCommandHandler'
import { FindCidCommandHandler } from './application/commandhandlers/findCidCommandHandler'
import { RequestCommandHandler } from './application/commandhandlers/requestCommandHandler'
import { ResponseCommandHandler } from './application/commandhandlers/responseCommandHandler'
import { InMemoryPeerWriteRepository } from './infrastructure/repositories/inMemoryPeerWriteRepository'
import { InMemoryPeerReadRepository } from './infrastructure/repositories/inMemoryPeerReadRepository';
import { InMemoryUserReadRepository } from './infrastructure/repositories/inMemoryUserReadRepository';
import { InMemoryRequestWriteRepository } from './infrastructure/repositories/inMemoryRequestWriteRepository';
import { InMemoryRequestReadRepository } from './infrastructure/repositories/inMemoryRequestReadRepository';
const sharedPeers = new Map();
const sharedRequests = new Map();
const sharedUsers = [
  {
    userId: 'uid',
    accessKeys: [
      {
        accessKeyId: 'user1',
        accessSecretKey: 'secret1'
      }
    ],
    peers: [],
  }
];

@Module({
  imports: [CqrsModule.forRoot()],
  controllers: [],
  exports: [WebsocketGateway],
  providers: [WebsocketGateway, FindCidCommandHandler, RegisterCommandHandler, RequestCommandHandler, ResponseCommandHandler,
    // Repositories
    {
      provide: InMemoryRequestWriteRepository,
      useFactory: () => new InMemoryRequestWriteRepository(sharedRequests)
    },
    {
      provide: InMemoryRequestReadRepository,
      useFactory: () => new InMemoryRequestReadRepository(sharedRequests)
    },
    {
      provide: InMemoryPeerReadRepository,
      useFactory: () => new InMemoryPeerReadRepository(sharedPeers),
    },
    {
      provide: InMemoryPeerWriteRepository,
      useFactory: () => new InMemoryPeerWriteRepository(sharedPeers),
    },
    {
      provide: InMemoryUserReadRepository,
      useFactory: () => new InMemoryUserReadRepository(sharedUsers),
    },

  ]
})
export class AppModule { }
