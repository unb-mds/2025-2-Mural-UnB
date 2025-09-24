import { useState } from 'react';
import murallogo from './public/assets/Mural_UnB.png';
import './App.css';

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <div className="flex flex-col items-center justify-center">
        <img src={murallogo.src} className="w-85 h85 mt-20" alt="Mural logo"/>

        <h2>🚧 Ops! Ainda em Construção 🚧</h2>

        <p className="p-4">
          Mural UnB ainda está em desenvolvimento. Enquanto isso, brinque com o botão abaixo
        </p>

        <button 
          className="btn btn-outline btn-accent" 
          onClick={() => setCount((count) => count + 1)}
        >
          A conta é {count}
        </button>

        <p className="p-2">
          Para mais informações acesse{' '}
          <a 
            href="https://github.com/unb-mds/2025-2-Mural-UnB" 
            className="text-verdeMain"
            target="_blank" 
            rel="noopener noreferrer"
          >
            nossa página do Github
          </a>
        </p>
      </div>
    </>
  );
}

export default App;