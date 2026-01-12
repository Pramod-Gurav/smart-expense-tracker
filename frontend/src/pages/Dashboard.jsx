import { useEffect, useState } from "react";
import { apiRequest } from "../api/client";
import { logout } from "../auth/auth";

function Dashboard() {
  const [categories, setCategories] = useState([]);
  const [expenses, setExpenses] = useState([]);

  const [amount, setAmount] = useState("");
  const [description, setDescription] = useState("");
  const [date, setDate] = useState("");
  const [categoryId, setCategoryId] = useState("");

  const [error, setError] = useState("");

  useEffect(() => {
    fetchCategories();
    fetchExpenses();
  }, []);

  async function fetchCategories() {
    try {
      const data = await apiRequest("/categories/");
      setCategories(data);
    } catch (err) {
      setError(err.message);
    }
  }

  async function fetchExpenses() {
    try {
      const data = await apiRequest("/expenses/");
      setExpenses(data);
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleAddExpense(e) {
    e.preventDefault();
    setError("");

    if (!amount || !date || !categoryId) {
      setError("Amount, date and category are required");
      return;
    }

    try {
      const newExpense = await apiRequest(
        "/expenses/",
        "POST",
        {
          amount: parseFloat(amount),
          description,
          date,
          category_id: parseInt(categoryId),
        }
      );

      setExpenses([...expenses, newExpense]);

      // reset form
      setAmount("");
      setDescription("");
      setDate("");
      setCategoryId("");
    } catch (err) {
      setError(err.message);
    }
  }

  function handleLogout() {
    logout();
    window.location.reload();
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <button onClick={handleLogout}>Logout</button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* ADD EXPENSE */}
      <h2>Add Expense</h2>

      <form onSubmit={handleAddExpense}>
        <input
          type="number"
          placeholder="Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />

        <input
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />

        <select
          value={categoryId}
          onChange={(e) => setCategoryId(e.target.value)}
        >
          <option value="">Select category</option>
          {categories.map((cat) => (
            <option key={cat.id} value={cat.id}>
              {cat.name}
            </option>
          ))}
        </select>

        <button type="submit">Add Expense</button>
      </form>

      {/* EXPENSE LIST */}
      <h2>Expenses</h2>

      <ul>
        {expenses.map((exp) => (
          <li key={exp.id}>
            ₹{exp.amount} — {exp.description} ({exp.date})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;

