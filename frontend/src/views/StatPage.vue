<template>
    <div>
        <canvas ref="myChart"></canvas>
    </div>
</template>

<script>
import axios from 'axios';
import { Chart } from 'chart.js';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, BarController, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, BarController, CategoryScale, LinearScale);

export default {
    data() {
        return {
            chartData: {
                labels: [],
                datasets: [
                    {
                        label: 'Number of Users',
                        backgroundColor: '#42A5F5',
                        data: [],
                    },
                ],
            },
            chartInstance: null,
        };
    },
    mounted() {
        console.log('mounted called');
        this.fetchUserCounts();
        
    },
    methods: {
        async fetchUserCounts() {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/stat');
                const data = response.data;
                this.chartData.labels = Object.keys(data);
                this.chartData.datasets[0].data = Object.values(data);

                // Call renderChart after updating chartData
                this.renderChart();
            } catch (error) {
                console.error('Error fetching user counts:', error);
            }
        },
        renderChart() {
            // Check if the canvas is available before trying to create the chart
            if (this.$refs.myChart) {
                if (this.chartInstance) {
                    this.chartInstance.destroy();
                }

                this.chartInstance = new Chart(this.$refs.myChart.getContext('2d'), {
                    type: 'bar',
                    data: this.chartData,
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                display: true,
                                position: 'top',
                            },
                        },
                        scales: {
                            x: {
                                title: {
                                    display: true,
                                    text: 'Categories',
                                },
                            },
                        },
                    },
                });
            } else {
                console.error('Chart canvas element not found');
            }
        },
    },

};
</script>
