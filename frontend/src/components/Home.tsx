import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"

interface LoanAnalysisResult {
  loan_id: number
  status: "pending" | "approved" | "declined" | null
}

interface LoanApplication {
  loan_id: number
  loan_amount: number
  annual_income: number
  credit_score: number
  employment_status: string
  application_date: string
  loanAnalysisResult: LoanAnalysisResult | null
}

const Home = () => {
  const [loans, setLoans] = useState<LoanApplication[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const navigate = useNavigate()

  useEffect(() => {
    const fetchLoans = async () => {
      const token = localStorage.getItem("token")
      if (!token) {
        navigate("/login")
        return
      }

      try {
        const response = await fetch("http://localhost:8000/get_all_applications", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        if (!response.ok) {
          throw new Error("Failed to fetch loan applications")
        }

        const data = await response.json()
        setLoans(data)
      } catch (err) {
        setError("An error occurred while fetching loan applications.")
      } finally {
        setLoading(false)
      }
    }

    fetchLoans()
  }, [navigate])

  const getStatusColor = (status: string | null) => {
    switch (status) {
      case "approved":
        return "bg-green-500"
      case "pending":
        return "bg-yellow-500"
      case "declined":
        return "bg-red-500"
      default:
        return "bg-gray-500" // Default case for null or undefined
    }
  }

  const handleCreateApplication = () => {
    navigate("/create_application")
  }

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>
  }

  if (error) {
    return <div className="flex justify-center items-center h-screen text-red-500">{error}</div>
  }

  return (
    <div className="container mx-auto p-4">
      <button
        onClick={handleCreateApplication}
        className="mb-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700"
      >
        Create New Loan Application
      </button>
      <h1 className="text-2xl font-bold mb-4">Your Loan Applications</h1>
      <div className="grid gap-4">
        {loans.map((loan) => (
          <div key={loan.loan_id} className="border p-4 rounded-lg shadow-sm flex justify-between items-center">
            <div>
              <p>
                <strong>Loan ID:</strong> {loan.loan_id}
              </p>
              <p>
                <strong>Amount:</strong> ${loan.loan_amount}
              </p>
              <p>
                <strong>Date:</strong> {new Date(loan.application_date).toLocaleDateString()}
              </p>
              <p>
                <strong>Status:</strong> {loan.loanAnalysisResult?.status || "Pending"}
              </p>
            </div>
            <div className={`w-4 h-4 rounded-full ${getStatusColor(loan.loanAnalysisResult?.status ?? "pending")}`}></div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Home
