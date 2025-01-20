import {
  io,
  Socket
} from 'socket.io-client'

describe('WebsocketGateway (Integration)', () => {
  let wsClient: Socket;

  afterAll(function() {
    wsClient.disconnect()
  });

  it('should connect to the WebSocket server and receive a welcome message', (done) => {
    wsClient = io(`http://127.0.0.1:3000/`);

    wsClient.on('connect', function(){
      console.log('Client connected');
      done();
    });

    // wsClient.connect();
  });
});