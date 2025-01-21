import { io, Socket } from 'socket.io-client';
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
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
  wsClientResponder.on('request', (data) => {
    // Responder sends a response back
    let {uuid} = data;
    let val = localStorage.getItem("keyname");
    console.log(val?.length)
    wsClientResponder.emit('response', { uuid, Body: val });
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
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
