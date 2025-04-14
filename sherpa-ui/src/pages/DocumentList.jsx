import { useEffect, useState } from "react"
import axios from "axios"
import AnswerBox from "../commons/Formatter"
import { Link } from "react-router-dom"

function DocumentList() {
    const [documents, setDocuments] = useState([])
    const [selectedDoc, setSelectedDoc] = useState(null)
    const [summary, setSummary] = useState("")
    const [loading, setLoading] = useState(false)
    const [isModalOpen, setIsModalOpen] = useState(false)
    const [docSearchQuery, setDocSearchQuery] = useState("")
    const [docSearchAnswer, setDocSearchAnswer] = useState("")
    const [docSearchLoading, setDocSearchLoading] = useState(false)
    const API_URL = import.meta.env.VITE_API_URL;

    useEffect(() => {
        const fetchDocs = async () => {
            try {
                const token = localStorage.getItem("token")
                const res = await axios.get(`${API_URL}/api/summary/list`, {
                    headers: { Authorization: `Bearer ${token}` },
                })
                setDocuments(res.data)
            } catch (err) {
                console.err("Failed to fetch documents")
            }
        }
        fetchDocs()
    }, [])

    const fetchSummary = async (docId) => {
        setLoading(true)
        setSummary("")
        setSelectedDoc(docId)
        setIsModalOpen(true)
        try {
            const token = localStorage.getItem("token")
            const res = await axios.get(
                `${API_URL}/api/summary/${docId}`,
                { headers: { Authorization: `Bearer ${token}` } }
            )
            setSummary(res.data.summary)
        } catch (err) {
            setSummary("Failed to fetch summary")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-gray-50 p-6 text-black">
            <p className="text-left text-sm mt-4">
                <Link to="/search" className="text-blue-600 hover:underline">
                    {'<< Go back to Search'}
                </Link>
                <div className="text-right" onClick={() => localStorage.removeItem('token')}>
                    <Link to="/" className="text-blue-600 hover:underline">
                        {'logout'}
                    </Link>
                </div>
            </p>
            <h1 className="text-3xl font-bold text-black mb-6">Available Documents</h1>

            <div className="overflow-x-auto">
                <table className="w-full bg-white shadow-md rounded-lg overflow-hidden">
                    <thead className="bg-blue-100 text-left">
                        <tr>
                            <th className="py-3 px-4 text-gray-700">Document ID</th>
                            <th className="py-3 px-4 text-gray-700">Title</th>
                            <th className="py-3 px-4 text-gray-700">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {documents.map((doc) => (
                            <tr key={doc.doc_id} className="border-t hover:bg-blue-50">
                                <td className="py-3 px-4 text-left">{doc.doc_id}</td>
                                <td className="py-3 px-4 text-left">{doc.doc_name}</td>
                                <td className="py-3 px-4">
                                    <button
                                        onClick={() => fetchSummary(doc.doc_id)}
                                        className="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700"
                                    >
                                        View
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {documents.length === 0 && (
                            <tr>
                                <td colSpan="3" className="text-center text-gray-500 py-6">
                                    No documents found.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
            {isModalOpen && (
                <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
                    <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-2xl relative">
                        <button
                            className="absolute top-2 right-3 text-gray-500 hover:text-red-500"
                            onClick={() => setIsModalOpen(false)}
                        >
                            ✖
                        </button>
                        <h2 className="text-xl font-semibold mb-4 text-blue-700">
                            Summary for Document #{selectedDoc}
                        </h2>
                        <hr className="my-6" />
                        <h3 className="text-lg font-semibold mb-2 text-gray-700">Search within this document</h3>

                        <textarea
                            rows="3"
                            className="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-black mb-4"
                            placeholder="Ask a question about this document..."
                            value={docSearchQuery}
                            onChange={(e) => setDocSearchQuery(e.target.value)}
                        ></textarea>

                        <button
                            onClick={async () => {
                                setDocSearchAnswer("")
                                setDocSearchLoading(true)
                                try {
                                    const token = localStorage.getItem("token")
                                    const res = await axios.post(
                                        `${API_URL}/api/rag/doc-search`,
                                        {
                                            query: docSearchQuery,
                                            doc_id: selectedDoc,
                                        },
                                        {
                                            headers: {
                                                Authorization: `Bearer ${token}`,
                                            },
                                        }
                                    )
                                    setDocSearchAnswer(res.data.answer)
                                } catch (err) {
                                    setDocSearchAnswer("Failed to fetch document-specific answer.")
                                } finally {
                                    setDocSearchLoading(false)
                                }
                            }}
                            disabled={docSearchLoading || !docSearchQuery.trim()}
                            className={`w-full py-2 mt-1 rounded text-white transition-all duration-200 ${docSearchLoading || !docSearchQuery.trim()
                                ? "bg-gray-400 cursor-not-allowed"
                                : "bg-blue-600 hover:bg-blue-700"
                                }`}
                        >
                            {docSearchLoading ? "Searching..." : "Ask within Document"}
                        </button>

                        {docSearchAnswer && (
                            <div className="mt-4 bg-gray-50 border border-gray-200 p-4 rounded-md">
                                <h4 className="text-sm font-medium text-gray-600 mb-2">Answer:</h4>
                                <p className="text-gray-800 whitespace-pre-wrap"><AnswerBox isAnswer answer={docSearchAnswer} /></p>
                            </div>
                        )}
                        {loading ? (
                            <p className="text-gray-500">Loading summary...</p>
                        ) : (
                            <div className="mt-4 max-h-80 overflow-y-auto pr-2 text-gray-800 whitespace-pre-wrap">
                                <AnswerBox answer={summary} />
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    )
}

export default DocumentList
