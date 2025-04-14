import { useState } from "react"
import axios from "axios"
import AnswerBox from "../commons/Formatter"
import { Link } from "react-router-dom"

function Search() {
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")
  const [sources, setSources] = useState([])
  const [loading, setLoading] = useState(false)
  const [errorMsg, setErrorMsg] = useState("")
  const API_URL = import.meta.env.VITE_API_URL;

  const askQuestion = async () => {
    setLoading(true)
    setErrorMsg("")
    setAnswer("")
    setSources([])

    try {
      const res = await axios.post(
        `${API_URL}/api/rag/ask`,
        { question, tenant: "Bain" },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      )
      setAnswer(res.data.answer)
      setSources(res.data.sources)
    } catch (err) {
      setErrorMsg(err.response?.data?.detail || "Failed to get answer")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-100 to-black-100 py-10 px-4">
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-lg shadow-md">
        <div className="text-right" onClick={() => localStorage.removeItem('token')}>
          <Link to="/" className="text-blue-600 hover:underline">
            {'logout'}
          </Link>
        </div>
        <h1 className="text-3xl font-bold text-center text-black mb-6">Sherpa Search</h1>

        <textarea
          className="w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
          rows="4"
          placeholder="Ask your question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <button
          onClick={askQuestion}
          disabled={loading || !question.trim()}
          className={`mt-4 w-full text-white py-2 rounded transition-all duration-200 ${loading || !question.trim()
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-blue-600 hover:bg-blue-700"
            }`}
        >
          {loading ? "Thinking..." : "Ask Sherpa"}
        </button>
        <p className="text-right text-sm mt-4">
          <Link to="/documents" className="text-blue-600 hover:underline">
            {'See All Documents >> '}
          </Link>
        </p>
        {errorMsg && (
          <p className="mt-4 text-sm text-center text-red-600">{errorMsg}</p>
        )}

        {answer && (
          <div className="mt-10 bg-gray-50 p-6 rounded-lg border border-gray-200 text-left">
            <p className="text-gray-700 leading-relaxed whitespace-pre-wrap text-left"> <AnswerBox answer={answer} /></p>
            {sources?.length > 0 ? (
              <div className="mt-6">
                <h3 className="font-medium text-gray-600 mb-2">Sources:</h3>
                <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                  {sources.map((src, i) => (
                    <li key={i}>
                      <span className="font-semibold">{src.doc_name}</span>:{" "}
                      {src.snippet.slice(0, 120)}...
                    </li>
                  ))}
                </ul>
              </div>
            ) : (
              <p className="mt-6 text-sm text-gray-500 italic">No sources available — this answer may come from a public fallback (e.g., web).</p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default Search
