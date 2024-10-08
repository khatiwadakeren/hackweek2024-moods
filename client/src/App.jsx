import { useState, useEffect, useRef } from "react";
import "./App.css";
import TicketDisplay from "./components/TicketDisplay";
import data01Happy from "../../seeds/01happy.json";
import data01Neutral from "../../seeds/01neutral.json";
import data01Upset from "../../seeds/01upset.json";
import data02Happy from "../../seeds/02happy.json";
import data02Neutral from "../../seeds/02neutral.json";
import data02Upset from "../../seeds/02upset.json";
import data03Happy from "../../seeds/03happy.json";
import data03Neutral from "../../seeds/03neutral.json";
import data03Upset from "../../seeds/03upset.json";
import dataHappy from "../../seeds/happy.json";
import dataNeutral from "../../seeds/neutral.json";
import dataUpset from "../../seeds/upset.json";
import Motivation from "./components/Motivation";

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
  const [response, setResponse] = useState(null); // State to store the API response
  const [ticketTitle, setTicketTitle] = useState(""); // State to store the ticket title
  const [ticketBody, setTicketBody] = useState(""); // State to store the ticket body
  const [soundUrl, setSoundUrl] = useState("");
  const audioRef = useRef(null);
  const [motivationKey, setMotivationKey] = useState(0); 

  const postTicketData = async () => {
    const url = "http://127.0.0.1:8000/api/detect-mood";

    try {
      // Stop any currently playing audio
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }

      const randomTicket = getRandomTicket();
      console.log("Ticket:", randomTicket);

      const payload = {
        ticket_body: randomTicket.ticket.comment.body,
      };

      console.log("Payload:", payload); // Ensure this logs the correct format

      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const result = await response.json();
      console.log("It worked: ", result);

      const fullSoundUrl = `http://127.0.0.1:8000${result.sound_url}`;

      // Update the state with the response, title, and body
      setResponse({
        ...result,
        ticketTitle: randomTicket.ticket.subject,
        ticketBody: randomTicket.ticket.comment.body,
      });
      setMotivationKey(prevKey => prevKey + 1);
      setSoundUrl(fullSoundUrl);

    } catch (error) {
      console.error("WHOMP: ", error);
    }
  };

  // Play the audio whenever the soundUrl changes
  useEffect(() => {
    if (soundUrl) {
      const audio = new Audio(soundUrl);
      audioRef.current = audio;
      audio.play();
    }
  }, [soundUrl]);

  return (
    <div>
      <h1 className="moody-monitor-title">Ticket Moody Monitor</h1>{" "}
      <button onClick={postTicketData}>Anyone got tickets?</button>
      {response && (
        <TicketDisplay
          ticketTitle={response.ticketTitle}
          ticketBody={response.ticketBody}
          embedUrl={response.embed_url}
          emotion={response.emotion}
        />
      )}

      {response && <Motivation key={motivationKey} emote={response.emotion} />}
    </div>
  );
}

export default App;
