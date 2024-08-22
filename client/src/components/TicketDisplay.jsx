import React, { useState, useEffect } from "react";

function TicketDisplay({ ticketTitle, ticketBody, embedUrl, emotion }) {
  const [showBody, setShowBody] = useState(false); // State to control the visibility of the ticket body

  // Reset showBody state whenever ticketBody changes
  useEffect(() => {
    setShowBody(false);
  }, [ticketBody]);

  const toggleBodyVisibility = () => {
    setShowBody((prevShowBody) => !prevShowBody);
  };

  return (
    <div className="ticket-display-container">
      <div className="ticket-title-container">
        <h2 className="ticket-title-label">Ticket Title:</h2>
        <p className="ticket-title-text">{ticketTitle}</p>
      </div>
      <div className="emotion-container">
        <h3 className="emotion-label">Emotion Detected:</h3>
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
          {showBody ? "Hide Ticket Content" : "Show Ticket Content"}
        </button>
      </div>
      {showBody && <p style={{ marginTop: "20px" }}>{ticketBody}</p>}
    </div>
  );
}

export default TicketDisplay;
