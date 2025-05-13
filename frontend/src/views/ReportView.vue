<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import ReportService from '@/services/ReportService';
import type { GraphRequest, ChartData, ReportResponse, DBStructure } from '@/interfaces/ReportInterfaces';
import { dbCredentialsStore } from '@/store/dbCredentialsStore';
import { ChartUtils } from '@/utils/chartUtils';

const isLoading = ref(false);
const error = ref('');
const availableTables = ref<string[]>([]);
const tableColumns = ref<Record<string, string[]>>({});
const selectedTable = ref('');
const selectedColumns = ref<string[]>([]);
const generatedCharts = ref<Record<string, ChartData[]>>({});
const isLoadingStructure = ref(false);
const chartInsights = ref<Record<string, string[]>>({});
const showDetails = ref<Record<string, boolean>>({});

interface ChartRef {
  id: string;
  element: HTMLCanvasElement | null;
}
const chartRefs = ref<ChartRef[]>([]);

const getChartRef = (key: string, index: number): HTMLCanvasElement | null => {
  const id = `${key}-${index}`;
  const ref = chartRefs.value.find(r => r.id === id);
  return ref ? ref.element : null;
};

const setChartRef = (key: string, index: number, element: HTMLCanvasElement): void => {
  const id = `${key}-${index}`;
  const existingIndex = chartRefs.value.findIndex(r => r.id === id);
  if (existingIndex >= 0) {
    chartRefs.value[existingIndex].element = element;
  } else {
    chartRefs.value.push({ id, element });
  }
};

const toggleDetails = (key: string): void => {
  showDetails.value[key] = !showDetails.value[key];
};

const loadDatabaseStructure = async () => {
  if (!dbCredentialsStore.credentials) {
    error.value = 'Database credentials are missing. Please configure the database connection first.';
    return;
  }

  isLoadingStructure.value = true;
  error.value = '';

  try {
    const dbStructure = await ReportService.getDatabaseStructure() as DBStructure;
    availableTables.value = Object.keys(dbStructure);
    const columns: Record<string, string[]> = {};
    for (const [tableName, tableData] of Object.entries(dbStructure)) {
      columns[tableName] = tableData.columns.map(col => col.name);
    }
    tableColumns.value = columns;
  } catch (err: any) {
    error.value = err.message || 'Error loading database structure';
    console.error('Error loading database structure:', err);
  } finally {
    isLoadingStructure.value = false;
  }
};

onMounted(() => {
  loadDatabaseStructure();
});

const handleTableSelect = () => {
  selectedColumns.value = [];
};

const generateCharts = async () => {
  if (!selectedTable.value || selectedColumns.value.length === 0) {
    error.value = 'Please select a table and at least one column';
    return;
  }

  if (!dbCredentialsStore.credentials) {
    error.value = 'Database credentials are missing. Please configure the database connection first.';
    return;
  }

  error.value = '';
  isLoading.value = true;
  generatedCharts.value = {};
  chartInsights.value = {};
  showDetails.value = {};

  try {
    const graphRequests: GraphRequest[] = [{
      table: selectedTable.value,
      columns: selectedColumns.value
    }];

    const response = await ReportService.generateCharts(graphRequests);
    generatedCharts.value = response as Record<string, ChartData[]>;

    Object.entries(generatedCharts.value).forEach(([key, charts]) => {
      if (typeof charts === 'string') return;
      showDetails.value[key] = false;
      const allInsights: string[] = [];
      charts.forEach(chart => {
        if (chart.additional_info) {
          const parsedInsights = ChartUtils.parseAdditionalInfo(chart.additional_info);
          allInsights.push(...parsedInsights);
        }
      });
      chartInsights.value[key] = allInsights;
    });

    setTimeout(renderCharts, 100);
  } catch (err: any) {
    error.value = err.message || 'Error generating charts';
  } finally {
    isLoading.value = false;
  }
};

const renderCharts = () => {
  const processCharts = () => {
    Object.entries(generatedCharts.value).forEach(([key, charts]) => {
      if (typeof charts === 'string') return;
      const [tableName, columnName] = key.split('.');
      charts.forEach((chartData, index) => {
        const canvas = getChartRef(key, index);
        if (!canvas) return;
        ChartUtils.createChart({
          canvas,
          chartData,
          tableName,
          columnName
        });
      });
    });
  };

  requestAnimationFrame(processCharts);
};

watch(chartRefs, () => {
  if (Object.keys(generatedCharts.value).length > 0) {
    renderCharts();
  }
}, { deep: true });
</script>

<template>
  <main class="analytics-container">
    <div class="header-section">
      <h1 class="title">Analytics & Reports</h1>
      <p class="subtitle">Visualize and analyze your data with interactive charts</p>
    </div>

    <div class="selection-panel">
      <div class="selection-panel-inner">
        <h5 class="panel-title">Select Data to Visualize</h5>

        <div v-if="isLoadingStructure" class="loading-state">
          <div class="spinner">
            <div class="spinner-inner"></div>
          </div>
          <p>Loading database structure...</p>
        </div>

        <template v-else>
          <div class="form-group">
            <label for="table-select">Select Table</label>
            <select
              id="table-select"
              class="form-control"
              v-model="selectedTable"
              @change="handleTableSelect"
            >
              <option value="">-- Select a table --</option>
              <option v-for="table in availableTables" :key="table" :value="table">
                {{ table }}
              </option>
            </select>
          </div>

          <div class="form-group" v-if="selectedTable">
            <label>Select Columns to Analyze</label>
            <div class="columns-container">
              <div v-for="column in tableColumns[selectedTable]" :key="column" class="column-option">
                <input
                  class="form-check-input"
                  type="checkbox"
                  :id="`column-${column}`"
                  :value="column"
                  v-model="selectedColumns"
                >
                <label class="form-check-label" :for="`column-${column}`">
                  {{ column }}
                </label>
              </div>
            </div>
          </div>

          <div class="button-group">
            <button
              class="btn btn-primary"
              @click="generateCharts"
              :disabled="isLoading || !selectedTable || selectedColumns.length === 0"
            >
              <span v-if="isLoading" class="btn-loader"></span>
              <span v-else>Generate Charts</span>
            </button>

            <button
              class="btn btn-outline"
              @click="loadDatabaseStructure"
              :disabled="isLoadingStructure"
            >
              <span v-if="isLoadingStructure" class="btn-loader"></span>
              <span v-else>Refresh Schema</span>
            </button>
          </div>
        </template>

        <div v-if="error" class="error-message">{{ error }}</div>
      </div>
    </div>

    <div v-if="Object.keys(generatedCharts).length > 0" class="report-container">
      <div
        v-for="(charts, key) in generatedCharts"
        :key="key"
        class="report-section"
      >
        <div class="report-header">
          <h2 class="report-title">{{ key }}</h2>

          <div v-if="chartInsights[key] && chartInsights[key].length > 0" class="insights-panel">
            <div class="insights-header" @click="toggleDetails(key)">
              <h3>Key Insights</h3>
              <span class="insights-toggle" :class="{ 'expanded': showDetails[key] }">
                <i class="arrow"></i>
              </span>
            </div>

            <div v-if="showDetails[key]" class="insights-content">
              <ul>
                <li v-for="(insight, i) in chartInsights[key]" :key="i">{{ insight }}</li>
              </ul>
            </div>
          </div>
        </div>

        <template v-if="typeof charts === 'string'">
          <div class="no-data-message">{{ charts }}</div>
        </template>

        <template v-else>
          <div class="charts-grid">
            <div
              v-for="(chart, index) in charts"
              :key="`${key}-${index}`"
              class="chart-card"
            >
              <div class="chart-card-inner">
                <div class="chart-header">
                  <h4 class="chart-title">{{ chart.chart_type }}</h4>
                </div>
                <div class="chart-body">
                  <div class="canvas-container">
                    <canvas
                      :ref="(el) => {
                        if (el) {
                          setChartRef(key, index, el as HTMLCanvasElement);
                        }
                      }"
                    ></canvas>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>
  </main>
</template>

<style scoped>
.analytics-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header-section {
  margin-bottom: 2rem;
  text-align: center;
}

.title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #7b0779;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.1rem;
  color: #6c757d;
}

.selection-panel {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
  overflow: hidden;
}

.selection-panel-inner {
  padding: 1.5rem;
}

.panel-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #333;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #495057;
}

.form-control {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: border-color 0.2s;
}

.form-control:focus {
  border-color: #7b0779;
  outline: none;
  box-shadow: 0 0 0 3px rgba(123, 7, 121, 0.1);
}

.columns-container {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 0.5rem 0;
}

.column-option {
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
}

.column-option:hover {
  background-color: #f8f9fa;
}

.form-check-input {
  margin-right: 0.75rem;
  width: 1.25rem;
  height: 1.25rem;
  cursor: pointer;
}

.form-check-input:checked {
  background-color: #7b0779;
  border-color: #7b0779;
}

.form-check-label {
  cursor: pointer;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, #7b0779, #5a055e);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #9b0999, #7b0779);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(123, 7, 121, 0.2);
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-outline {
  background: transparent;
  border: 1px solid #7b0779;
  color: #7b0779;
}

.btn-outline:hover {
  background: rgba(123, 7, 121, 0.05);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.spinner {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  position: relative;
  margin-bottom: 1rem;
}

.spinner-inner {
  width: 48px;
  height: 48px;
  border: 3px solid transparent;
  border-top-color: #7b0779;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.btn-loader {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.error-message {
  margin-top: 1rem;
  padding: 1rem;
  color: #721c24;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 8px;
}

.report-container {
  margin-top: 3rem;
}

.report-section {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 2.5rem;
  overflow: hidden;
}

.report-header {
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.report-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #7b0779;
  margin: 0;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  padding: 1.5rem;
}

.chart-card {
  overflow: hidden;
}

.chart-card-inner {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chart-header {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.chart-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  color: #333;
  text-transform: capitalize;
}

.chart-body {
  flex: 1;
  padding: 1rem;
}

.canvas-container {
  height: 300px;
  position: relative;
}

.insights-panel {
  margin-top: 1.5rem;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  overflow: hidden;
}

.insights-header {
  padding: 1rem 1.5rem;
  background-color: #f8f9fa;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.insights-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.insights-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
}

.arrow {
  border: solid #7b0779;
  border-width: 0 2px 2px 0;
  display: inline-block;
  padding: 3px;
  transform: rotate(45deg);
  transition: transform 0.2s;
}

.expanded .arrow {
  transform: rotate(-135deg);
}

.insights-content {
  padding: 1rem 1.5rem;
  background-color: #fff;
}

.insights-content ul {
  margin: 0;
  padding-left: 1.5rem;
}

.insights-content li {
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.no-data-message {
  padding: 2rem;
  text-align: center;
  color: #6c757d;
}

@media (max-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }

  .button-group {
    flex-direction: column;
  }
}
</style>