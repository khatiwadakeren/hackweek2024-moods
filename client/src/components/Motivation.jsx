import {useState, useEffect} from 'react'
import emotions from "../../../seeds/motivationalSentences"

const Motivation = () => {
    const [emotion, setEmotion] = useState("")
    // Select a random array (angry, happy, neutral)

    useEffect(() => {

        const randomArrayIndex = Math.floor(Math.random() * emotions.length);
        console.log(randomArrayIndex)
        const selectedArray = emotions[randomArrayIndex];
        const randomElementIndex = Math.floor(Math.random() * selectedArray.length);
        const randomElement = selectedArray[randomElementIndex];
        setEmotion(randomElement)
    }, [])
    return (
        <div className='motivation-container'>
            {emotion}
        </div>
    )
}

export default Motivation