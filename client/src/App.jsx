import { useState, useEffect, useRef } from "react";
import "./App.css";
import TicketDisplay from "./components/TicketDisplay";

import Motivation from "./components/Motivation";
import data01demo from "../../seeds/01demo.json"
import data02happy from "../../seeds/02happy.json";

const seeds = [
  data01demo,
  data02happy,
];

let currentIndex = 0;

function getRandomTicket() {
  const ticket = seeds[currentIndex];
  currentIndex = (currentIndex + 1) % seeds.length; // Reset to 0 after reaching the end
  return ticket;
}

function App() {
  const [response, setResponse] = useState(null); // State to store the API response
  const [ticketTitle, setTicketTitle] = useState(""); // State to store the ticket title
  const [ticketBody, setTicketBody] = useState(""); // State to store the ticket body
  const [soundUrl, setSoundUrl] = useState("");
  const audioRef = useRef(null);
  const [motivationKey, setMotivationKey] = useState(0); 

  const postTicketData = async () => {
    // const url = "http://127.0.0.1:8000/api/detect-mood";
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
      <h1 className="moody-monitor-title">Moody Monitor</h1>{" "}
      <button onClick={postTicketData}>Ticket Time!</button>
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
