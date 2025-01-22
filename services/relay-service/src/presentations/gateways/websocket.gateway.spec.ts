import { io, Socket } from 'socket.io-client';
import { v4 as uuid4 } from 'uuid'

const socketServer = 'http://127.0.0.1:3000/'
describe('WebsocketGateway (Integration)', () => {
  const requesterRegistration = {
    peerId: 'peer1',
    peerAddress: '/ip4/198.51.100.0/tcp/4242/p2p/QmRelay/p2p-circuit/p2p/QmRelayedPeer',
    storageCapacity: 10,
    accessKeyId: 'user1',
    accessSecretKey: 'secret1'
  }
  let wsClient: Socket;
  let peerRegistration = {
    peerId: 'peer1',
    peerAddress: '/ip4/198.51.100.0/tcp/4242/p2p/QmRelay/p2p-circuit/p2p/QmRelayedPeer',
    storageCapacity: 10,
    accessKeyId: 'user1',
    accessSecretKey: 'secret1'
  };

  beforeAll(() => {
    wsClient = io(socketServer, {
      auth: peerRegistration
    });
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
  it('should handle the "response" event but assumed someone on the network respond', (done) => {

    // Peer registration data
    let wsClientRequester = io(socketServer, {
      auth: requesterRegistration
    });

    // Simulate the requester handling the response from the responder
    wsClientRequester.once('response', (response) => {
      done();
    });

    // The requester sends a request to the responder
    setTimeout(function () {
      wsClientRequester.emit('request', { peerId: 'peer1', to: 'peer2', payload: { data: {
        fileKey: "QmPK1s3pNYLi9ERiq3BDxKa4XosgWwFRQUydHUtz4YgpqA/output.m3u8"
      } }, uuid: uuid4() });
    }, 200)
  }, 20_000);

  it('should handle the "response" event and forward to the correct peer', (done) => {
    // Peer registration data
    const responderRegistration = {
      peerId: 'peer2',
      peerAddress: '/ip4/198.51.100.0/tcp/4242/p2p/QmRelay/p2p-circuit/p2p/QmRelayedPeer',
      storageCapacity: 10,
      accessKeyId: 'user1',
      accessSecretKey: 'secret1'
    }
    let wsClientRequester = io(socketServer, {
      auth: requesterRegistration
    });
    let wsClientResponder = io(socketServer, {
      auth: responderRegistration
    });

    // Simulate the responder handling the forwarded request and emitting a "response" event
    wsClientResponder.on('request', (data) => {
      expect(data).toEqual(expect.objectContaining({
        payload: { data: 'test' }
      }));
      // Responder sends a response back
      let { uuid } = data;
      wsClientResponder.emit('response', { uuid, Body: 'Response received' });
    });

    // Simulate the requester handling the response from the responder
    wsClientRequester.once('response', (response) => {
      expect(response).toEqual(expect.objectContaining({ Body: 'Response received' }));
      wsClientRequester.disconnect()
      wsClientRequester = io(socketServer, {
        auth: requesterRegistration,
      });
      wsClientRequester.on('response', (response) => {
        expect(response).toEqual(expect.objectContaining({ Body: 'Response received' }));
        done();
      });
      wsClientRequester.emit('request', { peerId: 'peer1', to: 'peer2', payload: { data: 'test' }, uuid: uuid4() });
    });

    // Simulate an error scenario
    wsClientRequester.on('error', (error) => {
      done(new Error(`Unexpected error: ${error.message}`));
    });

    // The requester sends a request to the responder
    setTimeout(function () {
      wsClientRequester.emit('request', { peerId: 'peer1', to: 'peer2', payload: { data: 'test' }, uuid: uuid4() });
    }, 200)
  });
});