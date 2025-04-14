import ReactMarkdown from "react-markdown"

export default function AnswerBox({ answer, isAnswer }) {
  return (
    <div className={`prose max-w-none bg-white p-6 rounded shadow-md mt-6 ${isAnswer ? 'text-center': 'text-left' }`}>
      <ReactMarkdown>{answer}</ReactMarkdown>
    </div>
  )
}