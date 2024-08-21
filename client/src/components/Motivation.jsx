import {useState, useEffect} from 'react'
import emotions from "../../../seeds/motivationalSentences"

const Motivation = (emote) => {
    const [emotion, setEmotion] = useState("")
    // Select a random array (angry, happy, neutral)

    useEffect(() => {
        const fetchEmotion = async () => {
            try {
                console.warn(emote.emote)
                const response = await fetch('http://127.0.0.1:8000/api/emotion-check/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ emote: emote.emote }),
                });

                if (response.ok) {
                    const data = await response.json();
                    setEmotion(data.emotion);
                    console.warn(data)
                } else {
                    console.error("Failed to fetch emotion:", response.statusText);
                }
            } catch (error) {
                console.error("Error occurred while fetching emotion:", error);
            }
        };

        fetchEmotion();
    }, [])
    return (
        <div className='motivation-container'>
            {emotion}
        </div>
    )
}

export default Motivation