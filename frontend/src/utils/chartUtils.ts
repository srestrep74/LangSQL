import Chart from 'chart.js/auto';
import type { ChartData } from '@/interfaces/ReportInterfaces';
import type { ChartArea } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';

Chart.register(ChartDataLabels);
Chart.defaults.plugins.datalabels = { display: false };

interface ChartCreationOptions {
  canvas: HTMLCanvasElement;
  chartData: ChartData;
  tableName: string;
  columnName: string;
}

function getChartType(chartData: ChartData): string {
  return chartData.type || chartData.chart_type || 'bar';
}

function createGradient(ctx: CanvasRenderingContext2D, area: ChartArea, colorStart: string, colorEnd: string) {
  const gradient = ctx.createLinearGradient(0, area.bottom, 0, area.top);
  gradient.addColorStop(0, colorStart);
  gradient.addColorStop(1, colorEnd);
  return gradient;
}

function generateColors(count: number): { backgroundColor: string[], borderColor: string[] } {
  const baseColors = [
    { bg: 'rgba(54, 162, 235, 0.2)', border: 'rgba(54, 162, 235, 1)' },
    { bg: 'rgba(255, 99, 132, 0.2)', border: 'rgba(255, 99, 132, 1)' },
    { bg: 'rgba(75, 192, 192, 0.2)', border: 'rgba(75, 192, 192, 1)' },
    { bg: 'rgba(255, 159, 64, 0.2)', border: 'rgba(255, 159, 64, 1)' },
    { bg: 'rgba(153, 102, 255, 0.2)', border: 'rgba(153, 102, 255, 1)' },
    { bg: 'rgba(255, 205, 86, 0.2)', border: 'rgba(255, 205, 86, 1)' },
    { bg: 'rgba(201, 203, 207, 0.2)', border: 'rgba(201, 203, 207, 1)' },
    { bg: 'rgba(0, 204, 150, 0.2)', border: 'rgba(0, 204, 150, 1)' },
  ];

  const backgroundColors: string[] = [];
  const borderColors: string[] = [];

  for (let i = 0; i < count; i++) {
    const colorIndex = i % baseColors.length;
    backgroundColors.push(baseColors[colorIndex].bg);
    borderColors.push(baseColors[colorIndex].border);
  }

  return { backgroundColor: backgroundColors, borderColor: borderColors };
}

function enhanceDatasets(data: any, ctx: CanvasRenderingContext2D, area: ChartArea) {
  if (!data.datasets || !data.datasets.length) return data;

  const enhancedData = JSON.parse(JSON.stringify(data));
  const { backgroundColor, borderColor } = generateColors(enhancedData.datasets.length);

  enhancedData.datasets.forEach((dataset: any, index: number) => {
    const gradient = createGradient(
      ctx,
      area,
      backgroundColor[index].replace('0.2', '0.1'),
      backgroundColor[index].replace('0.2', '0.5')
    );

    dataset.backgroundColor = gradient;
    dataset.borderColor = borderColor[index];
    dataset.borderWidth = 2;

    if (dataset.data && dataset.data.length > 0) {
      dataset.tension = 0.3;
      dataset.borderRadius = 4;
    }
  });

  return enhancedData;
}

function createHistogramChart(canvas: HTMLCanvasElement, chartData: ChartData, title: string): Chart | null {
  if (!canvas) return null;

  const ctx = canvas.getContext('2d');
  if (!ctx) return null;

  const chartConfig = {
    type: 'bar',
    data: chartData.data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Frequency',
          }
        },
        x: {
          title: {
            display: true,
            text: 'Value Ranges',
          },
          ticks: {
            maxRotation: 45,
            minRotation: 45
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: title,
          font: {
            size: 16,
            weight: 'bold'
          }
        },
        tooltip: {
          callbacks: {
            title: (items: any) => `Range: ${items[0].label}`,
            label: (item: any) => `Count: ${item.raw}`
          }
        }
      }
    }
  };

  const tempArea: ChartArea = {
    top: 0,
    bottom: canvas.height,
    left: 0,
    right: canvas.width,
    width: canvas.width,
    height: canvas.height
  };

  chartConfig.data = enhanceDatasets(chartConfig.data, ctx, tempArea);

  return new Chart(canvas, chartConfig as any);
}

function createPieChart(canvas: HTMLCanvasElement, chartData: ChartData, title: string): Chart | null {
  if (!canvas) return null;

  const ctx = canvas.getContext('2d');
  if (!ctx) return null;

  const total = chartData.data.datasets[0].data.reduce((sum: number, val: number) => sum + val, 0);

  const chartConfig = {
    type: 'pie',
    data: chartData.data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: title,
          font: {
            size: 16,
            weight: 'bold'
          }
        },
        legend: {
          position: 'right',
          labels: {
            usePointStyle: true,
            padding: 15
          }
        },
        tooltip: {
          callbacks: {
            label: (context: any) => {
              const label = context.label || '';
              const value = context.raw || 0;
              const percentage = ((value / total) * 100).toFixed(1);
              return `${label}: ${value} (${percentage}%)`;
            }
          }
        }
      }
    }
  };

  const { backgroundColor, borderColor } = generateColors(chartData.data.datasets[0].data.length);
  const enhancedData = JSON.parse(JSON.stringify(chartData.data));

  enhancedData.datasets.forEach((dataset: any) => {
    dataset.backgroundColor = backgroundColor;
    dataset.borderColor = borderColor;
    dataset.borderWidth = 2;
  });

  chartConfig.data = enhancedData;

  return new Chart(canvas, chartConfig as any);
}

export function createDataTable(container: HTMLElement, chartData: ChartData, title: string): HTMLElement {
  container.innerHTML = '';

  const titleElement = document.createElement('h4');
  titleElement.textContent = title;
  titleElement.className = 'table-title';
  container.appendChild(titleElement);

  const table = document.createElement('table');
  table.className = 'data-table';

  const thead = document.createElement('thead');
  const headerRow = document.createElement('tr');

  if (chartData.data.columns) {
    const columns = chartData.data.columns as string[];

    columns.forEach((column: string) => {
      const th = document.createElement('th');
      th.textContent = column;
      headerRow.appendChild(th);
    });

    const countHeader = document.createElement('th');
    countHeader.textContent = 'Count';
    headerRow.appendChild(countHeader);

    thead.appendChild(headerRow);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    const uniqueRows = new Map<string, number>();

    if (chartData.data.rows && Array.isArray(chartData.data.rows)) {
      chartData.data.rows.forEach((row: any[]) => {
        const key = JSON.stringify(row);
        uniqueRows.set(key, (uniqueRows.get(key) || 0) + 1);
      });

      Array.from(uniqueRows.entries()).forEach(([key, count]) => {
        const row = document.createElement('tr');
        const rowData = JSON.parse(key);

        rowData.forEach((cell: any) => {
          const td = document.createElement('td');
          td.textContent = String(cell);
          row.appendChild(td);
        });

        const countCell = document.createElement('td');
        countCell.textContent = String(count);
        countCell.className = 'count-cell';
        row.appendChild(countCell);

        tbody.appendChild(row);
      });
    }

    table.appendChild(tbody);
  } else if (chartData.data.labels && chartData.data.datasets) {
    const categoryHeader = document.createElement('th');
    categoryHeader.textContent = 'Category';
    headerRow.appendChild(categoryHeader);

    const valueHeader = document.createElement('th');
    valueHeader.textContent = 'Count';
    headerRow.appendChild(valueHeader);

    thead.appendChild(headerRow);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    const labels = chartData.data.labels;
    const data = chartData.data.datasets[0].data;

    for (let i = 0; i < labels.length; i++) {
      const row = document.createElement('tr');

      const categoryCell = document.createElement('td');
      categoryCell.textContent = String(labels[i]);
      row.appendChild(categoryCell);

      const valueCell = document.createElement('td');
      valueCell.textContent = String(data[i]);
      row.appendChild(valueCell);

      tbody.appendChild(row);
    }

    table.appendChild(tbody);
  }

  container.appendChild(table);

  const style = document.createElement('style');
  style.textContent = `
    .data-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
      font-size: 0.9rem;
    }
    .data-table th, .data-table td {
      padding: 8px 12px;
      border: 1px solid #ddd;
      text-align: left;
    }
    .data-table thead {
      background-color: #f5f5f5;
    }
    .data-table th {
      font-weight: 600;
    }
    .data-table tbody tr:nth-child(even) {
      background-color: #f9f9f9;
    }
    .data-table tbody tr:hover {
      background-color: #f1f1f1;
    }
    .table-title {
      margin-top: 0;
      margin-bottom: 10px;
      font-size: 16px;
      font-weight: bold;
    }
    .count-cell {
      font-weight: 600;
      text-align: center;
      background-color: rgba(123, 7, 121, 0.05);
    }
  `;

  container.appendChild(style);

  return container;
}

export function createVisualization(options: ChartCreationOptions): Chart | HTMLElement | null {
  const { canvas, chartData, tableName, columnName } = options;

  if (!canvas) return null;

  const existingChart = Chart.getChart(canvas);
  if (existingChart) {
    existingChart.destroy();
  }

  const ctx = canvas.getContext('2d');
  if (!ctx) return null;

  const title = `${tableName}.${columnName}`;
  const chartType = getChartType(chartData);

  if (chartType === 'table') {
    const container = canvas.parentElement;
    if (!container) return null;
    canvas.style.display = 'none';
    return createDataTable(container, chartData, title);
  }

  canvas.style.display = 'block';

  if (chartType === 'pie') {
    return createPieChart(canvas, chartData, title);
  } else if (chartData.data.datasets && chartData.data.datasets[0].label &&
            chartData.data.datasets[0].label.toLowerCase().includes('histogram')) {
    return createHistogramChart(canvas, chartData, title);
  }

  const chartConfig = {
    type: chartType,
    data: chartData.data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        duration: 1000,
        easing: 'easeOutQuart'
      },
      plugins: {
        title: {
          display: true,
          text: title,
          font: {
            size: 16,
            weight: 'bold'
          },
          padding: {
            top: 10,
            bottom: 20
          }
        },
        legend: {
          position: 'top',
          labels: {
            usePointStyle: true,
            padding: 15
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.7)',
          bodyFont: {
            size: 13
          },
          titleFont: {
            size: 14,
            weight: 'bold'
          },
          padding: 10,
          cornerRadius: 6,
          displayColors: true,
          usePointStyle: true
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            padding: 8,
            font: {
              size: 11
            }
          },
          grid: {
            drawBorder: false,
            color: 'rgba(200, 200, 200, 0.15)'
          }
        },
        x: {
          ticks: {
            padding: 8,
            font: {
              size: 11
            },
            maxRotation: 45,
            minRotation: 45
          },
          grid: {
            display: false,
            drawBorder: false
          }
        }
      }
    }
  };

  const tempArea: ChartArea = {
    top: 0,
    bottom: canvas.height,
    left: 0,
    right: canvas.width,
    width: canvas.width,
    height: canvas.height
  };

  chartConfig.data = enhanceDatasets(chartConfig.data, ctx, tempArea);

  if (chartType === 'line') {
    (chartConfig as any).options.elements = {
      line: {
        tension: 0.3
      },
      point: {
        hoverRadius: 7,
        radius: 5
      }
    };
  }

  return new Chart(canvas, chartConfig as any);
}

export function parseAdditionalInfo(info: string | string[]): string[] {
  if (typeof info === 'string') {
    return info
      .split('\n')
      .filter(line => line.trim().length > 0)
      .map(line => line.trim());
  }
  return info;
}

export const ChartUtils = {
  createChart: createVisualization,
  parseAdditionalInfo,
  createDataTable,
  createHistogramChart,
  createPieChart
};