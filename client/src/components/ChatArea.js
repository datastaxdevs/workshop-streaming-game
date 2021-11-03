import { useState } from "react"

const ChatArea = ({chatItems, sendChatItem, playerID}) => {

  const [chatText, setChatText] = useState('')

  return (<div className="chat-area">
    <div className="chat-title">In-game chat</div>
    <ul className="chat-list">
      {chatItems.map( ci => (
        <li key={ci.id} className="chat-item">
          <span
            className={`chat-player-name ${ci.playerID === playerID ? 'player-self' : 'player-other'}`}
          >
            {ci.playerName}
          </span>: {ci.text}
        </li>
      ))}
    </ul>
    <input
      type="text"
      name="chattext"
      value={chatText}
      onChange={(e) => setChatText(e.target.value)}
      onKeyDown={(e) => {
        if(e.keyCode === 13){
          sendChatItem(chatText)
          setChatText('')
        }
      } }
    />
  </div>)
}

export default ChatArea;
