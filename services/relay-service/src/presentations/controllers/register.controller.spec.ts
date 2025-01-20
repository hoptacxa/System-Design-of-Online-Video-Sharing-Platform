import { Test, TestingModule } from '@nestjs/testing';
import { RegisterController } from './RegisterController';
// import { AppController } from './app.controller';
// import { AppService } from './app.service';
import { RegisterCommandHandler } from '../../application/commandhandlers/registerCommandHandler';

describe('AppController', () => {
  let appController: RegisterController;

  beforeEach(async () => {
    const app: TestingModule = await Test.createTestingModule({
      controllers: [RegisterController],
      providers: [RegisterCommandHandler],
    }).compile();

    appController = app.get<RegisterController>(RegisterController);
  });

  describe('root', () => {
    it('should return "Hello World!"', () => {
      expect(appController.getHello()).toBe('Hello World!');
    });
  });
});
