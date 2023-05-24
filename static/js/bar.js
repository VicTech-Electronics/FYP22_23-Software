new Chart(document.getElementById("barchart"), {
	type: 'bar',
	data: {
		labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'Novermber', 'December'],
		datasets: [{
				data: transactions.revenue,
				label: 'Revenue',
				backgroundColor: "#4755AB",
				borderWidth: 1,
			}, {
				data: transactions.expenses,
				label: 'Expenses',
				backgroundColor: "#ff4f81",
				borderWidth: 1,
			},
		]
	},
	options: {
		responsive: true,
		legend: {
			position: 'top',
		},
	}
});
