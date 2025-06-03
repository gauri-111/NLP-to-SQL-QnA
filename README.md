🧠 NLP to SQL QnA using Groq + LangChain

This project converts natural language questions into SQL queries using a Large Language Model (LLM) from Groq API. It then runs the queries against a MySQL database and returns the results in human-readable format.

------------------------------------------------------------

🚀 Features

- 🔗 Integration with Groq's LLM (`gemma2-9b-it`)
- 🤖 Natural language → SQL query generation
- 🗃️ Executes queries against MySQL database (`employees`, `departments`)
- 📄 Extracts and cleans SQL query from LLM response
- 🧠 Generates human-like answers from SQL results
- ⚙️ Modular and easy to adapt for other databases or LLMs

------------------------------------------------------------

🗂️ Project Structure

nlp-to-sql-qna/
├── chatsql.py              # Main script with LLM pipeline
├── .env                    # API key and DB credentials (not tracked)
├── requirements.txt        # Python dependencies
└── README.md

------------------------------------------------------------

⚙️ How It Works

1. Load Groq API key and connect to MySQL database  
2. Convert user question to SQL using LangChain's `create_sql_query_chain`  
3. Extract clean SQL from LLM output  
4. Run SQL query using LangChain's `QuerySQLDataBaseTool`  
5. Feed result + question + query to LLM to generate a natural answer

------------------------------------------------------------

🔧 Setup Instructions

1. Clone the Repo:
   git clone https://github.com/yourusername/nlp-to-sql-qna.git  
   cd nlp-to-sql-qna

2. Create Virtual Environment:
   python -m venv venv  
   source venv/bin/activate        # On Windows: venv\Scripts\activate

3. Install Dependencies:
   pip install -r requirements.txt

4. Configure `.env` File:
   GROQ_API_KEY=your_groq_api_key

------------------------------------------------------------

🧪 Example

Input Question:
   "departmnt and name of person with maximum salary in table?"

Extracted SQL:
   SELECT departments.dept_name, employees.emp_name  
   FROM employees  
   JOIN departments ON employees.dept_id = departments.dept_id  
   JOIN salaries ON employees.emp_id = salaries.emp_id  
   ORDER BY salaries.salary DESC  
   LIMIT 1;

Final Answer:
   "Engineering department has Charlie with the highest salary."

------------------------------------------------------------

🧱 Built With

- Python
- LangChain
- Groq API
- MySQL
- Dotenv

------------------------------------------------------------

📌 Notes

- Requires MySQL running locally (`mysql+pymysql://root:@localhost/x`)  
- `employees` and `departments` tables must exist in the database  
- Uses `gemma2-9b-it` model via Groq API (temperature = 0)

------------------------------------------------------------

🔐 License

This project is licensed under the MIT License.

------------------------------------------------------------

👤 Author

Your Name  
GitHub: https://github.com/yourusername  
LinkedIn: https://linkedin.com/in/yourlinkedin
