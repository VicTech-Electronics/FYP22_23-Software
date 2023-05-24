

new Chart(document.getElementById("linechart"), {
	type: 'line',
	data: {
		labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'Novermber', 'December'],
		datasets: [{
				label: 'Urination',
				backgroundColor: window.chartColors.green,
				borderColor: window.chartColors.green,
				data: urinations,
				fill: false,
			}, {
				label: 'Defecation',
				fill: false,
				backgroundColor: window.chartColors.purple,
				borderColor: window.chartColors.purple,
				data: defecations,
			}, {
				label: 'Shower',
				fill: false,
				backgroundColor: window.chartColors.navy,
				borderColor: window.chartColors.navy,
				data: showers,
			},
		]
	},
	options: {
		responsive: true,
		// title: {
		// 	display: true,
		// 	text: 'Chart.js Line Chart'
		// },
		tooltips: {
			mode: 'index',
			intersect: false,
		},
		hover: {
			mode: 'nearest',
			intersect: true
		},
		scales: {
			xAxes: [{
				display: true,
				scaleLabel: {
					display: true,
					labelString: 'Month'
				}
			}],
			yAxes: [{
				display: true,
				scaleLabel: {
					display: true,
					labelString: 'Value'
				}
			}]
		}
	}
});
