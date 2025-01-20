import { io, Socket } from 'socket.io-client';

describe('WebsocketGateway (Integration)', () => {
  let wsClient: Socket;

  beforeAll(() => {
    wsClient = io(`http://127.0.0.1:3000/`);
  });

  afterAll(() => {
    wsClient.disconnect();
  });

  it('should connect to the WebSocket server successfully', (done) => {
    wsClient.on('connect', () => {
      console.log('Client connected');
      done();
    });
  });

  it('should handle the "register" event successfully', (done) => {
    wsClient.emit('register', { peerId: 'peer1', accessKeyId: 'user1', accessSecretKey: 'secret1' });

    wsClient.on('success', (response) => {
      expect(response).toEqual(expect.objectContaining({ message: 'Peer registered successfully' }));
      done();
    });

    wsClient.on('error', (error) => {
      done(new Error(`Unexpected error: ${error.message}`));
    });
  });

  it('should handle the "request" event and forward to the correct peer', (done) => {
    wsClient.emit('request', { peerId: 'peer1', to: 'peer2', payload: { data: 'test' } });

    wsClient.on('success', (response) => {
      expect(response).toEqual(expect.objectContaining({ message: 'Request processed successfully' }));
      done();
    });

    wsClient.on('error', (error) => {
      done(new Error(`Unexpected error: ${error.message}`));
    });
  });

  it('should handle the "response" event and forward to the correct peer', (done) => {
    wsClient.emit('response', { peerId: 'peer2', to: 'peer1', payload: { data: 'response data' } });

    wsClient.on('success', (response) => {
      expect(response).toEqual(expect.objectContaining({ message: 'Response processed successfully' }));
      done();
    });

    wsClient.on('error', (error) => {
      done(new Error(`Unexpected error: ${error.message}`));
    });
  });
});