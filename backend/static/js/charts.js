export const COLORS = [
  '#4e79a7', '#f28e2b', '#e15759', '#76b7b2',
  '#59a14f', '#edc948', '#b07aa1', '#ff9da7',
  '#9c755f', '#bab0ac',
];

export function renderHBar(canvasId, labels, datasets) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: datasets.map((ds, i) => ({
        ...ds,
        backgroundColor: COLORS[i % COLORS.length] + 'cc',
        borderColor: COLORS[i % COLORS.length],
        borderWidth: 1,
      })),
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      plugins: { legend: { display: datasets.length > 1 } },
      scales: {
        x: { beginAtZero: true, title: { display: true, text: 'Plays' } },
        y: { ticks: { font: { size: 12 } } },
      },
    },
  });
}
