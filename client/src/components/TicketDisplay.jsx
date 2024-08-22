import React, { useState, useEffect } from "react";

function TicketDisplay({ ticketTitle, ticketBody, embedUrl, emotion }) {
  const [showBody, setShowBody] = useState(false); // State to control the visibility of the ticket body
  const [santizedBody, setSantizedBody] = useState(ticketBody);

  const wordsToSanitize = ["fuck", "angry", "mad", "furious", "irate", "enraged", "annoyed", "outraged", "livid", "resentful", "indignant", "anger", "sadness"];
  const substituteWord = "😂🤣😜";

  const replaceWords = (inputString) => {
    const regex = new RegExp(`\\b(${wordsToSanitize.join('|')})\\b`, 'gi');
    return inputString.replace(regex, substituteWord);
  };

  // Reset showBody state whenever ticketBody changes
  useEffect(() => {
    setShowBody(false);
    setSantizedBody(replaceWords(ticketBody));
  }, [ticketBody]);

  const toggleBodyVisibility = () => {
    setShowBody((prevShowBody) => !prevShowBody);
  };

  return (
    <div className="ticket-display-container">
      <div className="ticket-title-container">
        <h2 className="ticket-title-label">Title:</h2>
        <p className="ticket-title-text">{ticketTitle}</p>
      </div>
      <div className="emotion-container">
        <h3 className="emotion-label">Vibe:</h3>
        <p className="emotion-text">{emotion}</p>
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <iframe
          src={embedUrl}
          width="480"
          height="270"
          frameBorder="0"
          allowFullScreen
          title="GIF"
        ></iframe>
        <button
          style={{
            marginTop: "10px",
          }}
          onClick={toggleBodyVisibility}
        >
          {showBody ? "Hide Contents" : "Show Contents"}
        </button>
      </div>
      {showBody && <p style={{ marginTop: "20px" }}>{santizedBody}</p>}
    </div>
  );
}

export default TicketDisplay;
