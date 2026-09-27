/* ================================
   CURRENCY FORMATTER
================================ */

function formatCurrency(amount) {
    return "₹" + Number(amount).toLocaleString("en-IN", {
        maximumFractionDigits: 2
    });
}

/* ================================
   SEARCH - TRANSACTIONS PAGE
================================ */

const searchInput = document.getElementById("searchInput");

if (searchInput) {

    searchInput.addEventListener("keyup", function () {

        const searchValue = searchInput.value.toLowerCase();
        const rows = document.querySelectorAll(".transaction-table tbody tr");

        rows.forEach(function (row) {

            const rowText = row.textContent.toLowerCase();

            if (rowText.includes(searchValue)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }

        });

    });

}


/* ================================
   DASHBOARD - TOTAL SPENDING
================================ */

const totalSpending = document.getElementById("totalSpending");

if (totalSpending) {

    fetch("http://127.0.0.1:5000/api/transactions/monthly", {
        credentials: "include"
    })
        .then(response => response.json())
        .then(data => {

            let total = 0;

            data.monthly_spending.forEach(item => {
                total += item.total_spending;
            });

            totalSpending.textContent = formatCurrency(total);

        })
        .catch(error => {
            console.log("Error:", error);
        });

}


/* ================================
   DASHBOARD - TOTAL TRANSACTIONS
================================ */

const totalTransactions = document.getElementById("totalTransactions");

if (totalTransactions) {

    fetch("http://127.0.0.1:5000/api/transactions", {
        credentials: "include"
    })
        .then(response => response.json())
        .then(data => {

            totalTransactions.textContent = data.transactions.length;

        })
        .catch(error => {
            console.log("Error:", error);
        });

}


/* ================================
   DASHBOARD - HIGHEST EXPENSE
================================ */

const highestExpense = document.getElementById("highestExpense");

if (highestExpense) {

    fetch("http://127.0.0.1:5000/api/transactions", {
        credentials: "include"
    })
        .then(response => response.json())
        .then(data => {

            const transactions = data.transactions;

            let highest = 0;

            transactions.forEach(transaction => {

                if (transaction.amount > highest) {
                    highest = transaction.amount;
                }

            });

            highestExpense.textContent = formatCurrency(highest);

        })
        .catch(error => {
            console.log("Error:", error);
        });

}


/* ================================
   DASHBOARD - AVERAGE EXPENSE
================================ */

const averageExpense = document.getElementById("averageExpense");

if (averageExpense) {

    fetch("http://127.0.0.1:5000/api/transactions", {
        credentials: "include"
    })
        .then(response => response.json())
        .then(data => {

            const transactions = data.transactions;

            let total = 0;

            transactions.forEach(transaction => {
                total += transaction.amount;
            });

            const average = total / transactions.length;

            averageExpense.textContent = formatCurrency(average);

        })
        .catch(error => {
            console.log("Error:", error);
        });

}


/* ================================
   DASHBOARD - RECENT TRANSACTIONS
================================ */

const recentTransactions = document.getElementById("recentTransactions");

if (recentTransactions) {

    fetch("http://127.0.0.1:5000/api/transactions", {
        credentials: "include"
    })
        .then(response => response.json())
        .then(data => {

            const transactions = data.transactions;

            transactions.forEach(transaction => {

                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${transaction.date}</td>
                    <td>${transaction.description}</td>
                    <td>${transaction.category}</td>
                    <td>${formatCurrency(transaction.amount)}</td>
                `;

                recentTransactions.appendChild(row);

            });

        })
        .catch(error => {
            console.log("Error:", error);
        });

}


/* ================================
   ADD TRANSACTION
================================ */

const transactionForm = document.getElementById("transactionForm");

if (transactionForm) {

    transactionForm.addEventListener("submit", function(event) {

        event.preventDefault();

        const date = document.getElementById("date").value;
        const description = document.getElementById("description").value;
        const category = document.getElementById("category").value;
        const amount = document.getElementById("amount").value;

        fetch("http://127.0.0.1:5000/api/transactions", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                date: date,
                description: description,
                category: category,
                amount: Number(amount)
            })
        })
        .then(response => response.json())
        .then(data => {

            console.log(data);

            window.location.href = "index.html";

        })
        .catch(error => {
            console.log("Error:", error);
        });

    });

}


/* ================================
   TRANSACTIONS PAGE
================================ */

const transactionsList = document.getElementById("transactionsList");

if (transactionsList) {

    fetch("http://127.0.0.1:5000/api/transactions", {
        credentials: "include"
    })
        .then(response => response.json())
        .then(data => {

            const transactions = data.transactions;

            transactions.forEach(transaction => {

                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${transaction.date}</td>
                    <td>${transaction.description}</td>
                    <td>${transaction.category}</td>
                    <td>${formatCurrency(transaction.amount)}</td>
                `;

                transactionsList.appendChild(row);

            });

        })
        .catch(error => {
            console.log("Error:", error);
        });

}


/* ================================
   ANALYSIS PAGE - SUMMARY
================================ */

const analysisTotal = document.getElementById("analysisTotal");
const analysisHighest = document.getElementById("analysisHighest");
const analysisAverage = document.getElementById("analysisAverage");

if (analysisTotal || analysisHighest || analysisAverage) {

    fetch("http://127.0.0.1:5000/api/transactions", {
        credentials: "include"
    })
        .then(response => response.json())
        .then(data => {

            const transactions = data.transactions;

            let total = 0;
            let highest = 0;

            transactions.forEach(transaction => {

                total += transaction.amount;

                if (transaction.amount > highest) {
                    highest = transaction.amount;
                }

            });

            const average = total / transactions.length;

            if (analysisTotal) analysisTotal.textContent = formatCurrency(total);
            if (analysisHighest) analysisHighest.textContent = formatCurrency(highest);
            if (analysisAverage) analysisAverage.textContent = formatCurrency(average);

        })
        .catch(error => {
            console.log("Error:", error);
        });

}


/* ================================
   ANALYSIS PAGE - CATEGORY SPENDING
================================ */

const categoryAnalysis = document.getElementById("categoryAnalysis");

if (categoryAnalysis) {

    fetch("http://127.0.0.1:5000/api/transactions", {
        credentials: "include"
    })
        .then(response => response.json())
        .then(data => {

            const transactions = data.transactions;

            const categories = {};

            transactions.forEach(transaction => {

                const category = transaction.category;

                if (!categories[category]) {
                    categories[category] = 0;
                }

                categories[category] += transaction.amount;

            });

            for (const category in categories) {

                const item = document.createElement("div");

                item.className = "card";

                item.innerHTML = `
                    <h3>${category}</h3>
                    <p>${formatCurrency(categories[category])}</p>
                `;

                categoryAnalysis.appendChild(item);

            }

        })
        .catch(error => {
            console.log("Error:", error);
        });

}


/* ================================
   ANALYSIS PAGE - SPENDING CHART
================================ */

const spendingChart = document.getElementById("spendingChart");

if (spendingChart) {

    fetch("http://127.0.0.1:5000/api/transactions", {
        credentials: "include"
    })
        .then(response => response.json())
        .then(data => {

            const transactions = data.transactions;

            const categories = {};

            transactions.forEach(transaction => {

                const category = transaction.category;

                if (!categories[category]) {
                    categories[category] = 0;
                }

                categories[category] += transaction.amount;

            });

            new Chart(spendingChart, {

                type: "bar",

                data: {

                    labels: Object.keys(categories),

                    datasets: [{
                        label: "Spending",
                        data: Object.values(categories)
                    }]

                }

            });

        })
        .catch(error => {
            console.log("Error:", error);
        });

}


/* ================================
   REPORTS PAGE
================================ */

const reportTotal = document.getElementById("reportTotal");
const reportTransactions = document.getElementById("reportTransactions");
const reportHighest = document.getElementById("reportHighest");
const reportAverage = document.getElementById("reportAverage");
const reportTransactionsList = document.getElementById("reportTransactionsList");

if (reportTotal || reportTransactionsList) {

    fetch("http://127.0.0.1:5000/api/transactions", {
        credentials: "include"
    })
        .then(response => response.json())
        .then(data => {

            const transactions = data.transactions;

            let total = 0;
            let highest = 0;

            transactions.forEach(transaction => {

                total += transaction.amount;

                if (transaction.amount > highest) {
                    highest = transaction.amount;
                }

                if (reportTransactionsList) {

                    const row = document.createElement("tr");

                    row.innerHTML = `
                        <td>${transaction.date}</td>
                        <td>${transaction.description}</td>
                        <td>${transaction.category}</td>
                        <td>${formatCurrency(transaction.amount)}</td>
                    `;

                    reportTransactionsList.appendChild(row);

                }

            });

            const average = total / transactions.length;

            if (reportTotal) reportTotal.textContent = formatCurrency(total);
            if (reportTransactions) reportTransactions.textContent = transactions.length;
            if (reportHighest) reportHighest.textContent = formatCurrency(highest);
            if (reportAverage) reportAverage.textContent = formatCurrency(average);

        })
        .catch(error => {
            console.log("Error:", error);
        });

}


/* ================================
   REPORTS PAGE - EXPORT CSV
================================ */

const exportReport = document.getElementById("exportReport");

if (exportReport) {

    exportReport.addEventListener("click", function () {

        fetch("http://127.0.0.1:5000/api/transactions", {
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {

                const transactions = data.transactions;

                let csv = "Date,Description,Category,Amount\n";

                transactions.forEach(transaction => {

                    csv += `"${transaction.date}","${transaction.description}","${transaction.category}","${formatCurrency(transaction.amount)}"\n`;

                });

                const blob = new Blob([csv], {
                    type: "text/csv"
                });

                const url = URL.createObjectURL(blob);

                const link = document.createElement("a");

                link.href = url;
                link.download = "finquery_report.csv";

                link.click();

                URL.revokeObjectURL(url);

            })
            .catch(error => {
                console.log("Error:", error);
            });

    });

}


/* ================================
   REGISTER
================================ */

const registerForm = document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener("submit", async function(event) {

        event.preventDefault();

        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const response = await fetch(
            "http://127.0.0.1:5000/api/register",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password
                })
            }
        );

        const result = await response.json();

        alert(result.message);

    });

}


/* ================================
   LOGIN
================================ */

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", async function(event) {

        event.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const response = await fetch(
            "http://127.0.0.1:5000/api/login",
            {
                method: "POST",

                credentials: "include",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    email: email,
                    password: password
                })
            }
        );

        const result = await response.json();

        if (result.success) {

            window.location.href = "analysis.html";

        } else {

            alert(result.message);

        }

    });

}


/* ================================
   PAGE PROTECTION
================================ */

const currentPage = window.location.pathname;

if (
    currentPage.includes("analysis.html") ||
    currentPage.includes("transactions.html") ||
    currentPage.includes("add-transaction.html") ||
    currentPage.includes("reports.html")
) {

    fetch("http://127.0.0.1:5000/api/me", {
        credentials: "include"
    })
        .then(response => {

            if (!response.ok) {

                window.location.href = "login.html";

            }

            return response.json();

        })
        .then(result => {

            if (!result.logged_in) {

                window.location.href = "login.html";

            }

        })
        .catch(error => {

            console.log("Session check error:", error);

            window.location.href = "login.html";

        });

}

