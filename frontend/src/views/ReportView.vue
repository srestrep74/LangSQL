<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import ReportService from '@/services/ReportService';
import type { GraphRequest, ChartData, ReportResponse, DBStructure } from '@/interfaces/ReportInterfaces';
import { dbCredentialsStore } from '@/store/dbCredentialsStore';
import { ChartUtils } from '@/utils/chartUtils';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

const isLoading = ref(false);
const error = ref('');
const availableTables = ref<string[]>([]);
const tableColumns = ref<Record<string, string[]>>({});
const selectedTables = ref<string[]>([]);
const selectedTableColumns = ref<Record<string, string[]>>({});
const generatedCharts = ref<Record<string, ChartData[]>>({});
const isLoadingStructure = ref(false);
const chartInsights = ref<Record<string, string[]>>({});
const showDetails = ref<Record<string, boolean>>({});
const isExportingPdf = ref(false);
const exportProgress = ref(0);
const exportProgressText = ref('');

const reportContainerRef = ref<HTMLElement | null>(null);

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
      columns[tableName] = tableData.columns
        .map(col => col.name)
        .filter(colName => !colName.toLowerCase().includes('id'));
    }
    tableColumns.value = columns;

    for (const table in selectedTableColumns.value) {
      if (selectedTableColumns.value[table]) {
        selectedTableColumns.value[table] = selectedTableColumns.value[table].filter(
          colName => !colName.toLowerCase().includes('id')
        );

        if (selectedTableColumns.value[table].length === 0) {
          delete selectedTableColumns.value[table];
          selectedTables.value = selectedTables.value.filter(t => t !== table);
        }
      }
    }

    selectedTableColumns.value = { ...selectedTableColumns.value };

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

const handleTableSelect = (table: string) => {
  if (selectedTables.value.includes(table)) {
    selectedTables.value = selectedTables.value.filter(t => t !== table);
    delete selectedTableColumns.value[table];
  } else {
    selectedTables.value.push(table);
    selectedTableColumns.value[table] = [];
  }
};

const handleColumnSelect = (table: string, column: string) => {
  if (column.toLowerCase().includes('id')) {
    return;
  }

  if (!selectedTableColumns.value[table]) {
    selectedTableColumns.value[table] = [];
  }

  const columns = selectedTableColumns.value[table];
  const columnIndex = columns.indexOf(column);

  if (columnIndex === -1) {
    selectedTableColumns.value[table].push(column);
  } else {
    selectedTableColumns.value[table].splice(columnIndex, 1);

    if (selectedTableColumns.value[table].length === 0) {
      delete selectedTableColumns.value[table];
      selectedTables.value = selectedTables.value.filter(t => t !== table);
    }
  }

  selectedTableColumns.value = { ...selectedTableColumns.value };

  console.log('Current selection:', selectedTableColumns.value, 'button enabled:', hasSelectedItems.value);
};

const isColumnSelected = (table: string, column: string): boolean => {
  return selectedTableColumns.value[table]?.includes(column) || false;
};

const hasSelectedItems = computed(() => {
  return Object.keys(selectedTableColumns.value).length > 0 &&
    Object.values(selectedTableColumns.value).some(columns => columns.length > 0);
});

const generateCharts = async () => {
  if (!hasSelectedItems.value) {
    error.value = 'Please select at least one table and column';
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
    const graphRequests: GraphRequest[] = Object.entries(selectedTableColumns.value).map(([table, columns]) => ({
      table,
      columns
    }));

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

watch(selectedTableColumns, (newVal) => {
  console.log('selectedTableColumns changed:', newVal);
  console.log('hasSelectedItems:', hasSelectedItems.value);
}, { deep: true });

watch(chartRefs, () => {
  if (Object.keys(generatedCharts.value).length > 0) {
    renderCharts();
  }
}, { deep: true });

const exportToPdf = async () => {
  if (Object.keys(generatedCharts.value).length === 0) {
    error.value = 'No charts to export. Please generate some charts first.';
    return;
  }

  if (!reportContainerRef.value) {
    error.value = 'Error generating PDF: Report container not found.';
    return;
  }

  isExportingPdf.value = true;
  exportProgress.value = 0;
  exportProgressText.value = 'Preparing document...';
  error.value = '';

  try {
    Object.keys(showDetails.value).forEach(key => {
      showDetails.value[key] = true;
    });

    exportProgress.value = 5;
    exportProgressText.value = 'Rendering elements...';

    await new Promise(resolve => setTimeout(resolve, 300));

    exportProgress.value = 10;
    exportProgressText.value = 'Creating PDF document...';

    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4',
    });

    exportProgress.value = 20;
    exportProgressText.value = 'Generating cover page...';
    createCoverPage(pdf);

    let currentY = 20;

    const totalSections = Object.keys(generatedCharts.value).length;
    let processedSections = 0;

    for (const [key, charts] of Object.entries(generatedCharts.value)) {
      if (typeof charts === 'string') {
        processedSections++;
        continue;
      }

      exportProgressText.value = `Processing section: ${key}...`;
      exportProgress.value = 20 + Math.round((processedSections / totalSections) * 60);

      pdf.addPage();
      currentY = 20;

      pdf.setFontSize(18);
      pdf.setTextColor(123, 7, 121);
      pdf.text(key, 20, currentY);
      currentY += 15;

      currentY = addInsightsToPdf(pdf, key, currentY);

      const totalCharts = charts.length;
      let processedCharts = 0;

      for (const [index, chart] of charts.entries()) {
        exportProgressText.value = `Processing chart ${index + 1} of ${totalCharts} in ${key}...`;

        if (currentY > 220) {
          pdf.addPage();
          currentY = 20;
        }

        pdf.setFontSize(14);
        pdf.setTextColor(51, 51, 51);
        pdf.text(`${chart.chart_type}`, 20, currentY);
        currentY += 10;

        try {
          const canvas = getChartRef(key, index);
          if (!canvas) {
            processedCharts++;
            continue;
          }

          const imgData = canvas.toDataURL('image/png', 1.0);

          const imgProps = pdf.getImageProperties(imgData);
          const pdfWidth = pdf.internal.pageSize.getWidth() - 40;
          const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

          pdf.addImage(imgData, 'PNG', 20, currentY, pdfWidth, pdfHeight);
          currentY += pdfHeight + 20;
        } catch (err) {
          console.error(`Error converting chart ${index} of ${key}:`, err);
        }

        processedCharts++;
        const sectionProgress = processedCharts / totalCharts;
        const sectionWeight = 1 / totalSections;
        const additionalProgress = sectionProgress * sectionWeight * 60;
        exportProgress.value = 20 + Math.round((processedSections / totalSections) * 60 + additionalProgress);
      }

      processedSections++;
    }

    exportProgress.value = 85;
    exportProgressText.value = 'Generating summary and conclusions...';
    addSummaryPage(pdf);

    exportProgress.value = 95;
    exportProgressText.value = 'Saving document...';
    pdf.save('data-analysis-report.pdf');

    exportProgress.value = 100;
    exportProgressText.value = 'PDF successfully generated!';

    setTimeout(() => {
      if (isExportingPdf.value) {
        isExportingPdf.value = false;
        exportProgress.value = 0;
        exportProgressText.value = '';
      }
    }, 2000);
  } catch (err: any) {
    console.error('Error generating PDF:', err);
    error.value = `Error generating PDF: ${err.message || 'Unknown error'}`;
    exportProgressText.value = 'Error generating PDF';
  } finally {
    if (exportProgress.value < 100) {
      isExportingPdf.value = false;
      exportProgress.value = 0;
      exportProgressText.value = '';
    }
  }
};

const createCoverPage = (pdf: any) => {
  const width = pdf.internal.pageSize.getWidth();
  const height = pdf.internal.pageSize.getHeight();

  pdf.setFillColor(123, 7, 121);
  pdf.rect(0, 0, width, height, 'F');

  pdf.setFillColor(46, 204, 113);
  pdf.rect(0, height * 0.75, width, height * 0.25, 'F');

  pdf.setTextColor(255, 255, 255);
  pdf.setFontSize(30);
  pdf.setFont('helvetica', 'bold');
  const title = 'DATA ANALYSIS REPORT';
  const titleWidth = pdf.getStringUnitWidth(title) * 30 / pdf.internal.scaleFactor;
  pdf.text(title, (width - titleWidth) / 2, height * 0.4);

  pdf.setFontSize(16);
  pdf.setFont('helvetica', 'normal');
  const subtitle = 'Data Visualization and Insights';
  const subtitleWidth = pdf.getStringUnitWidth(subtitle) * 16 / pdf.internal.scaleFactor;
  pdf.text(subtitle, (width - subtitleWidth) / 2, height * 0.47);

  const date = new Date().toLocaleDateString();
  pdf.setFontSize(12);
  pdf.text(`Generated on: ${date}`, width - 60, height - 20);
};

const addInsightsToPdf = (pdf: any, key: string, startY: number): number => {
  let currentY = startY;

  if (chartInsights.value[key] && chartInsights.value[key].length > 0) {
    pdf.setFontSize(16);
    pdf.setTextColor(51, 51, 51);
    pdf.text('Key Insights:', 20, currentY);
    currentY += 10;

    pdf.setFontSize(11);
    pdf.setTextColor(80, 80, 80);

    chartInsights.value[key].forEach(insight => {
      const textLines = pdf.splitTextToSize(insight, pdf.internal.pageSize.getWidth() - 40);

      if (currentY + (textLines.length * 6) > pdf.internal.pageSize.getHeight() - 20) {
        pdf.addPage();
        currentY = 20;
      }

      pdf.circle(22, currentY - 1, 1, 'F');

      pdf.text(textLines, 25, currentY);
      currentY += (textLines.length * 6) + 4;
    });

    currentY += 10;
  }

  return currentY;
};

const addSummaryPage = (pdf: any) => {
  pdf.addPage();

  const width = pdf.internal.pageSize.getWidth();

  pdf.setFontSize(20);
  pdf.setTextColor(123, 7, 121);
  pdf.setFont('helvetica', 'bold');
  pdf.text('Summary and Conclusions', width / 2, 30, { align: 'center' });

  pdf.setDrawColor(46, 204, 113);
  pdf.setLineWidth(1);
  pdf.line(width / 4, 35, width * 3/4, 35);

  let totalCharts = 0;
  let totalInsights = 0;

  Object.entries(generatedCharts.value).forEach(([key, charts]) => {
    if (typeof charts === 'string') return;
    totalCharts += charts.length;
    totalInsights += (chartInsights.value[key]?.length || 0);
  });

  pdf.setFontSize(12);
  pdf.setTextColor(80, 80, 80);
  pdf.setFont('helvetica', 'normal');

  let y = 50;

  pdf.text(`• Total sections analyzed: ${Object.keys(generatedCharts.value).length}`, 30, y);
  y += 10;

  pdf.text(`• Total visualizations generated: ${totalCharts}`, 30, y);
  y += 10;

  pdf.text(`• Total insights identified: ${totalInsights}`, 30, y);
  y += 20;

  pdf.setFontSize(11);
  pdf.text('This report was automatically generated by analyzing the selected data.', 30, y);
  y += 7;
  pdf.text('The visualizations and insights provided are intended to help with data-driven', 30, y);
  y += 7;
  pdf.text('decision-making to improve business processes.', 30, y);

  pdf.setFontSize(10);
  pdf.setTextColor(150, 150, 150);
  pdf.text('© LangSQL Analytics Tool', width / 2, pdf.internal.pageSize.getHeight() - 20, { align: 'center' });
};
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
          <div class="tables-section">
            <h6 class="section-subtitle">Select Tables and Columns</h6>
            <div class="tables-grid">
              <div
                v-for="table in availableTables"
                :key="table"
                class="table-card"
                :class="{ 'table-selected': selectedTables.includes(table) }"
              >
                <div class="table-header" @click="handleTableSelect(table)">
                  <h4 class="table-name">{{ table }}</h4>
                  <span class="table-toggle">
                    <i class="check-icon" v-if="selectedTables.includes(table)"></i>
                  </span>
                </div>

                <div class="table-columns" v-if="selectedTables.includes(table)">
                  <div
                    v-for="column in tableColumns[table]"
                    :key="`${table}-${column}`"
                    class="column-option"
                    :class="{ 'column-selected': isColumnSelected(table, column) }"
                    @click="handleColumnSelect(table, column)"
                  >
                    <input
                      class="form-check-input"
                      type="checkbox"
                      :id="`column-${table}-${column}`"
                      :checked="isColumnSelected(table, column)"
                      @click.stop
                    >
                    <label class="form-check-label" :for="`column-${table}-${column}`">
                      {{ column }}
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="selection-summary" v-if="Object.keys(selectedTableColumns).length > 0">
            <h6>Selected Items:</h6>
            <ul class="selection-list">
              <li v-for="(columns, table) in selectedTableColumns" :key="table">
                <strong>{{ table }}</strong>: {{ columns.join(', ') }}
              </li>
            </ul>
          </div>

          <div class="button-group">
            <button
              class="btn btn-primary"
              @click="generateCharts"
              :disabled="isLoading || !hasSelectedItems"
              :class="{ 'btn-enabled': hasSelectedItems }"
            >
              <span v-if="isLoading" class="btn-loader"></span>
              <span v-else class="btn-text">Generate Charts</span>
            </button>

            <button
              class="btn btn-outline"
              @click="loadDatabaseStructure"
              :disabled="isLoadingStructure"
            >
              <span v-if="isLoadingStructure" class="btn-loader"></span>
              <span v-else class="btn-text">Refresh Schema</span>
            </button>

            <button
              v-if="Object.keys(generatedCharts).length > 0"
              class="btn btn-export"
              @click="exportToPdf"
              :disabled="isExportingPdf"
            >
              <span v-if="isExportingPdf" class="btn-loader"></span>
              <span v-else class="btn-text">
                <i class="download-icon"></i>
                Export PDF
              </span>
            </button>
          </div>

          <div v-if="!hasSelectedItems" class="selection-hint">
            Select at least one table and column to generate charts
          </div>
        </template>

        <div v-if="error" class="error-message">{{ error }}</div>
      </div>
    </div>

    <div
      v-if="Object.keys(generatedCharts).length > 0"
      class="report-container"
      ref="reportContainerRef"
    >
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

    <div v-if="isExportingPdf" class="pdf-export-overlay">
      <div class="pdf-export-modal">
        <div class="export-spinner"></div>
        <h3>Generating PDF</h3>
        <div class="progress-bar-container">
          <div class="progress-bar" :style="{ width: `${exportProgress}%` }"></div>
        </div>
        <p>{{ exportProgressText }}</p>
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

.section-subtitle {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #495057;
}

.tables-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.table-card {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s;
}

.table-selected {
  border-color: #7b0779;
  box-shadow: 0 0 0 1px rgba(123, 7, 121, 0.2);
}

.table-header {
  padding: 0.75rem 1rem;
  background-color: #f8f9fa;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  border-bottom: 1px solid #eee;
}

.table-selected .table-header {
  background-color: rgba(123, 7, 121, 0.05);
  border-bottom-color: rgba(123, 7, 121, 0.1);
}

.table-name {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.table-toggle {
  width: 18px;
  height: 18px;
  border: 2px solid #ccc;
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.table-selected .table-toggle {
  border-color: #7b0779;
  background-color: #7b0779;
}

.check-icon {
  display: inline-block;
  width: 6px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.table-columns {
  max-height: 180px;
  overflow-y: auto;
  padding: 0.5rem 0;
}

.column-option {
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
  cursor: pointer;
}

.column-option:hover {
  background-color: #f8f9fa;
}

.column-selected {
  background-color: rgba(123, 7, 121, 0.05);
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
  font-size: 0.9rem;
}

.selection-summary {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.selection-summary h6 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.selection-list {
  list-style-type: none;
  padding-left: 0;
  margin: 0;
}

.selection-list li {
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
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

.btn-text {
  color: inherit;
}

.btn-primary {
  background: linear-gradient(135deg, #7b0779, #5a055e);
  color: white !important;
}

.btn-primary .btn-text {
  color: white !important;
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
  color: white !important;
}

.btn-outline:disabled {
  color: #7b0779 !important;
  background-color: rgba(123, 7, 121, 0.05);
}

.btn-loader {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
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

.selection-hint {
  margin-top: 1rem;
  padding: 1rem;
  color: #6c757d;
  background-color: #f8f9fa;
  border-radius: 8px;
  text-align: center;
}

.btn-enabled {
  animation: pulse 2s infinite;
  box-shadow: 0 0 10px rgba(123, 7, 121, 0.3);
  color: white !important;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(123, 7, 121, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(123, 7, 121, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(123, 7, 121, 0);
  }
}

.report-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}

.btn-secondary {
  background: transparent;
  border: 1px solid #7b0779;
  color: #7b0779;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: rgba(123, 7, 121, 0.05);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(123, 7, 121, 0.1);
}

.btn-export {
  background: linear-gradient(135deg, #7b0779, #5a055e);
  color: white !important;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-export:hover {
  background: linear-gradient(135deg, #9b0999, #7b0779);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(123, 7, 121, 0.2);
}

.btn-export:active {
  transform: translateY(0);
}

.download-icon {
  display: inline-block;
  width: 16px;
  height: 16px;
  margin-right: 8px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4'/%3E%3Cpolyline points='7 10 12 15 17 10'/%3E%3Cline x1='12' y1='15' x2='12' y2='3'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
}

@media (max-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }

  .button-group {
    flex-direction: column;
  }

  .tables-grid {
    grid-template-columns: 1fr;
  }

  .btn-export {
    margin-top: 0.5rem;
  }
}

.pdf-export-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
}

.pdf-export-modal {
  background-color: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  text-align: center;
  width: 90%;
  max-width: 500px;
}

.pdf-export-modal h3 {
  color: #7b0779;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.pdf-export-modal p {
  color: #666;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.progress-bar-container {
  height: 10px;
  background-color: #f0f0f0;
  border-radius: 10px;
  overflow: hidden;
  margin: 1rem 0;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #7b0779, #2ecc71);
  border-radius: 10px;
  transition: width 0.3s ease;
}

.export-spinner {
  margin: 0 auto 1.5rem;
  width: 50px;
  height: 50px;
  border: 5px solid rgba(123, 7, 121, 0.2);
  border-top-color: #7b0779;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Make sure all button states have proper text color */
.btn-primary:hover,
.btn-primary:active,
.btn-primary:focus,
.btn-export:hover,
.btn-export:active,
.btn-export:focus {
  color: white !important;
}

.btn-primary:hover .btn-text,
.btn-primary:active .btn-text,
.btn-primary:focus .btn-text,
.btn-export:hover .btn-text,
.btn-export:active .btn-text,
.btn-export:focus .btn-text {
  color: white !important;
}

/* Ensure even disabled buttons have white text */
.btn-primary:disabled,
.btn-export:disabled {
  color: white !important;
  opacity: 0.7;
}

.btn-primary:disabled .btn-text,
.btn-export:disabled .btn-text {
  color: white !important;
}

/* Override any browser default button styles */
button.btn-primary,
button.btn-export {
  color: white !important;
}

button.btn-primary span,
button.btn-export span {
  color: white !important;
}

.btn-export .btn-text {
  color: white !important;
}

.btn-primary *,
.btn-export * {
  color: white !important;
}

.btn-outline * {
  color: #7b0779 !important;
}

.btn-outline:hover * {
  color: #7b0779 !important;
}
</style>