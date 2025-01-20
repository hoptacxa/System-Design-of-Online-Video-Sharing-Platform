import { io, Socket } from 'socket.io-client';

describe('WebsocketGateway (Integration)', () => {
  let wsClient: Socket;
  let peerRegistration = {
    peerId: 'peer1',
    peerAddress: '/ip4/198.51.100.0/tcp/4242/p2p/QmRelay/p2p-circuit/p2p/QmRelayedPeer',
    storageCapacity: 10,
    accessKeyId: 'user1',
    accessSecretKey: 'secret1'
  };

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
    wsClient.emit('register', peerRegistration);
    wsClient.emit('register', {
      peerId: 'peer2',
      peerAddress: '/ip4/198.51.100.0/tcp/4242/p2p/QmRelay/p2p-circuit/p2p/QmRelayedPeer',
      storageCapacity: 10,
      accessKeyId: 'user1',
      accessSecretKey: 'secret1'
    });

    wsClient.on('success', (response) => {
      expect(response).toEqual(expect.objectContaining({ message: 'Peer registered successfully' }));
      done();
    });

    wsClient.on('error', (error) => {
      done(new Error(`Unexpected error: ${error.message}`));
    });
  });

  it('should handle the "request" event and forward to the correct peer', (done) => {
    wsClient.emit('register', peerRegistration);

    wsClient.on('request-success', (response) => {
      expect(response).toEqual(expect.objectContaining({ message: 'Request processed successfully' }));
      done();
    });
    wsClient.emit('request', { peerId: 'peer1', to: 'peer2', payload: { data: 'test' } });

    wsClient.on('error', (error) => {
      done(new Error(`Unexpected error: ${error.message}`));
    });
  });

  it('should handle the "response" event and forward to the correct peer', (done) => {
    const wsClientRequester = io(`http://127.0.0.1:3000/`); // Simulating the requester peer
    const wsClientResponder = io(`http://127.0.0.1:3000/`); // Simulating the responder peer

    // Peer registration data
    const requesterRegistration = {
      peerId: 'peer1',
      peerAddress: '/ip4/198.51.100.0/tcp/4242/p2p/QmRelay/p2p-circuit/p2p/QmRelayedPeer',
      storageCapacity: 10,
      accessKeyId: 'user1',
      accessSecretKey: 'secret1'
    }
    const responderRegistration = {
      peerId: 'peer2',
      peerAddress: '/ip4/198.51.100.0/tcp/4242/p2p/QmRelay/p2p-circuit/p2p/QmRelayedPeer',
      storageCapacity: 10,
      accessKeyId: 'user1',
      accessSecretKey: 'secret1'
    }

    // Register the requester peer
    wsClientRequester.emit('register', requesterRegistration);

    // Register the responder peer
    wsClientResponder.emit('register', responderRegistration);

    // Simulate the responder handling the forwarded request and emitting a "response" event
    wsClientResponder.on('request', (data) => {
      console.log('w')
      expect(data).toEqual(expect.objectContaining({
        payload: { data: 'test' }
      }));
      // Responder sends a response back
      let {uuid} = data;
      wsClientResponder.emit('response', { uuid, Body: 'Response received' });
      done();
    });

    // Simulate the requester handling the response from the responder
    wsClientRequester.on('response', (response) => {
      expect(response).toEqual(expect.objectContaining({ message: 'Response received' }));
      done(); // Test completed successfully
    });

    // Simulate an error scenario
    wsClientRequester.on('error', (error) => {
      done(new Error(`Unexpected error: ${error.message}`));
    });

    // The requester sends a request to the responder
    setTimeout(function() { 
      wsClientRequester.emit('request', { peerId: 'peer1', to: 'peer2', payload: { data: 'test' } });
    }, 200)
  });
});