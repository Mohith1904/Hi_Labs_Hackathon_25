import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const DataVisualization = ({ data, type = 'bar' }) => {
  if (!data || data.length === 0) {
    return <div className="no-data">No data available for visualization</div>;
  }

  // Safe stringify function
  const safeStringify = (value) => {
    if (value === null || value === undefined) return '';
    if (typeof value === 'string') return value;
    if (typeof value === 'number') return value.toString();
    if (typeof value === 'boolean') return value.toString();
    if (typeof value === 'object') return JSON.stringify(value);
    return String(value);
  };

  // Transform data to ensure proper format for charts
  const chartData = data.map((item, index) => {
    // Handle different data structures
    let name, value;
    
    if (item.primary_specialty && item.provider_count) {
      // Specialty data structure
      name = safeStringify(item.primary_specialty);
      value = typeof item.provider_count === 'number' ? item.provider_count : 
              parseFloat(item.provider_count) || 0;
    } else if (item.license_state && item.provider_count) {
      // State data structure
      name = safeStringify(item.license_state);
      value = typeof item.provider_count === 'number' ? item.provider_count : 
              parseFloat(item.provider_count) || 0;
    } else {
      // Generic data structure - use first key-value pair
      const keys = Object.keys(item);
      const values = Object.values(item);
      
      name = safeStringify(keys[0] || `Item ${index + 1}`);
      value = typeof values[0] === 'number' ? values[0] : 
              typeof values[0] === 'string' ? parseFloat(values[0]) || 0 : 0;
    }
    
    return { name, value };
  }).filter(item => !isNaN(item.value) && item.value > 0); // Filter out invalid numbers and zeros

  if (chartData.length === 0) {
    return (
      <div className="no-data">
        <p>No data available for visualization</p>
        <p style={{ fontSize: '0.9rem', color: '#666', marginTop: '10px' }}>
          This could mean all values are zero or the data is still loading.
        </p>
      </div>
    );
  }

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  const renderBarChart = () => (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="value" fill="#8884d8" />
      </BarChart>
    </ResponsiveContainer>
  );

  const renderPieChart = () => (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={chartData}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          outerRadius={80}
          fill="#8884d8"
          dataKey="value"
        >
          {chartData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  );

  return (
    <div className="data-visualization">
      <h3>Data Visualization</h3>
      {type === 'pie' ? renderPieChart() : renderBarChart()}
    </div>
  );
};

export default DataVisualization;
