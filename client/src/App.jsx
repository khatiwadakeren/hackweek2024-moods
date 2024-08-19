// import { useEffect, useState } from 'react';
import './App.css'
import data01Happy from '../../seeds/01happy.json';
import data01Neutral from '../../seeds/01neutral.json';
import data01Upset from '../../seeds/01upset.json';
import data02Happy from '../../seeds/02happy.json';
import data02Neutral from '../../seeds/02neutral.json';
import data02Upset from '../../seeds/02upset.json';
import data03Happy from '../../seeds/03happy.json';
import data03Neutral from '../../seeds/03neutral.json';
import data03Upset from '../../seeds/03upset.json';
import dataHappy from '../../seeds/happy.json';
import dataNeutral from '../../seeds/neutral.json';
import dataUpset from '../../seeds/upset.json';

const seeds = [
  data01Happy,
  data01Neutral,
  data01Upset,
  data02Happy,
  data02Neutral,
  data02Upset,
  data03Happy,
  data03Neutral,
  data03Upset,
  dataHappy,
  dataNeutral,
  dataUpset,
];

function getRandomTicket() {
  const randomIndex = Math.floor(Math.random() * seeds.length);
  return seeds[randomIndex];
}

function App() {
  const postTicketData = async () => {
    const url = '/api/detect-mood';
    
    try {
      const randomTicket = getRandomTicket();
      console.log(randomTicket)

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(randomTicket),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const result = await response.json();
      console.log('It worked: ', result);
    } catch (error) {
      console.error('WHOMP: ', error);
    }
  };

  return (
    <>
      <div>
        <h1>Moody Monitor</h1>
        <button onClick={postTicketData}>Anyone got tickets</button>
      </div>
    </>
  )
}

export default App
