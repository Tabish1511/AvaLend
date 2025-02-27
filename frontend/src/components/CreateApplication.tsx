"use client"

import { useState } from "react"
import { useNavigate } from "react-router-dom"

const CreateApplication = () => {
  const [loanAmount, setLoanAmount] = useState<number>(0)
  const [annualIncome, setAnnualIncome] = useState<number>(0)
  const [creditScore, setCreditScore] = useState<number>(0)
  const [employmentStatus, setEmploymentStatus] = useState<string>("")
  const [error, setError] = useState<string>("")
  const navigate = useNavigate()
  const apiUrl = import.meta.env.VITE_API_URL;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const token = localStorage.getItem("token")
    if (!token) {
      setError("You need to be logged in to apply for a loan.")
      return
    }

    const loanData = {
      loan_amount: loanAmount,
      annual_income: annualIncome,
      credit_score: creditScore,
      employment_status: employmentStatus,
    }

    try {
      const response = await fetch(`${apiUrl}/submit_application`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(loanData),
      })

      if (!response.ok) {
        throw new Error("Failed to submit loan application.")
      }

      // Redirect to the home page on success
      navigate("/home")
    } catch (err) {
      setError("An error occurred while submitting your application.")
    }
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Submit Loan Application</h1>

      {error && <div className="text-red-500 mb-4">{error}</div>}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block font-medium text-sm">Loan Amount</label>
          <input
            type="number"
            value={loanAmount}
            onChange={(e) => setLoanAmount(Number(e.target.value))}
            className="w-full px-4 py-2 border rounded-lg"
            required
          />
        </div>

        <div>
          <label className="block font-medium text-sm">Annual Income</label>
          <input
            type="number"
            value={annualIncome}
            onChange={(e) => setAnnualIncome(Number(e.target.value))}
            className="w-full px-4 py-2 border rounded-lg"
            required
          />
        </div>

        <div>
          <label className="block font-medium text-sm">Credit Score</label>
          <input
            type="number"
            value={creditScore}
            onChange={(e) => setCreditScore(Number(e.target.value))}
            className="w-full px-4 py-2 border rounded-lg"
            required
          />
        </div>

        <div>
          <label className="block font-medium text-sm">Employment Status</label>
          <input
            type="text"
            value={employmentStatus}
            onChange={(e) => setEmploymentStatus(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg"
            required
          />
        </div>

        <div className="flex justify-end mt-4">
          <button
            type="submit"
            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            Submit
          </button>
        </div>
      </form>
    </div>
  )
}

export default CreateApplication
