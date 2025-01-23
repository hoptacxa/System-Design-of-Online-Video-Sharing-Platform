import { io, Socket } from 'socket.io-client';
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import axios from 'axios'
import './App.css'

function App() {
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

  const [count, setCount] = useState(0)
  // Kích thước chuỗi cần tạo (5MB)
  const sizeInBytes = 8 * 1024 * 1024; // 5MB
  const sizeInChars = sizeInBytes / 2; // Mỗi ký tự chiếm 2 byte

  // Tạo chuỗi nhỏ để lặp lại
  const smallString = "a"; // 1 ký tự
  const repeatCount = Math.ceil(sizeInChars / smallString.length);

  // Tạo chuỗi 5MB
  const largeString = smallString.repeat(repeatCount).slice(0, sizeInChars);

  localStorage.setItem("keyname", largeString)
  // 

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        <video controls>
          <source type="application/x-mpegURL" src="https://http-0-0-0-0-3001.schnworks.com/command/get_by_name/LwekZs3Sp8g/output.m3u8" />
        </video>
      </p>
    </>
  )
}

export default App
