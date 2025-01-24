import { io, Socket } from 'socket.io-client';
import React from 'react'
import axios from 'axios'
import './App.css'
import VideoJS from './VideoPlayer'
import videojs from 'video.js';

function App() {
  const playerRef = React.useRef(null);

  const videoJsOptions = {
    autoplay: true,
    controls: true,
    responsive: true,
    fluid: true,
    sources: [{
      src: 'https://http-0-0-0-0-3001.schnworks.com/command/get_by_name/LwekZs3Sp8g/output.m3u8',
    }]
  };

  const handlePlayerReady = (player: any) => {
    playerRef.current = player;

    // You can handle player events here, for example:
    player.on('waiting', () => {
      videojs.log('player is waiting');
    });

    player.on('dispose', () => {
      videojs.log('player will dispose');
    });
  };

  const socketServer = 'https://http-0-0-0-0-3000.schnworks.com/'
  const responderRegistration = {
    peerId: 'peer2',
    peerAddress: '/ip4/198.51.100.0/tcp/4242/p2p/QmRelay/p2p-circuit/p2p/QmRelayedPeer',
    storageCapacity: 10,
    accessKeyId: 'user1',
    accessSecretKey: 'secret1'
  }
  let wsClientResponder: Socket = io(socketServer, {
    auth: responderRegistration
  });
  // Declare a global variable to store the pullResponse
  // Define the type of the pull response
  interface PullResponse {
    [key: string]: string; // Or replace 'string' with the actual type of the response data
  }

  // Initialize the global variable with the defined type
  let globalPullResponse: PullResponse = {};
  let globalNameResolution: PullResponse = {
    name: 'QmPK1s3pNYLi9ERiq3BDxKa4XosgWwFRQUydHUtz4YgpqA'
  }

  wsClientResponder.on('find-by-cid', async (data) => {
    console.log(data);
    let { uuid, payload } = data;
    let name = payload.data.name
    name = 'name'

    let cid = globalNameResolution[name]
    if (cid) {
      wsClientResponder.emit('name-resolved', { uuid, Cid: cid });
    }
  })
  wsClientResponder.on('request', async (data) => {
    // Responder sends a response back
    let { uuid, payload } = data;
    console.log(data)
    let fileKey = payload.data.fileKey

    // Retrieve the stored pullResponse
    let Body = globalPullResponse[fileKey];

    if (typeof Body !== 'undefined') {
      wsClientResponder.emit('response', { uuid, Body });
    } else {
      try {
        let fileKey = data.payload.data.fileKey;
        console.log('responder-not-found received', fileKey, globalPullResponse);

        // Fetch the response
        let pullResponse = await axios.get(`https://http-0-0-0-0-3001.schnworks.com/command/pull/${fileKey}`);
        console.log('Pull response:', pullResponse);

        // Store pullResponse in the global variable using fileKey as the key
        globalPullResponse[fileKey] = pullResponse.data;

        console.log(`Stored pullResponse for fileKey: ${fileKey}`);
      } catch (error) {
        console.error('Error fetching pull response:', error);
      }
    }
  });

  return (
    <>
      <VideoJS options={videoJsOptions} onReady={handlePlayerReady} />
    </>
  )
}

export default App
