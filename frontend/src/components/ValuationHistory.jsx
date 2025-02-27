import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import axios from 'axios';
import ColorIndicator from './ColorIndicator';
const ValuationHistory = () => {
  const [data, setData] = useState([]);
  const [selectedDate, setSelectedDate] = useState('');
  const [tableData, setTableData] = useState({ columns: [], rows: [] });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/get_csv_record_data?start=0&limit=10');
        const datalist = response.data.message.map(item => ({
          csv_label: item.csv_label,
          update_date: new Date(item.update_date * 1000).toLocaleDateString()
        }));
        setData(datalist);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const handleDateChange = async (event) => {
    const csv_label = event.target.value;
    setSelectedDate(csv_label);
    const { columns, rows } = await fetchRowData(csv_label);
    setTableData({ columns, rows });
  };

  const fetchRowData = async (csv_label) => {
    const columns = ['行业', 'PB.加权', 'PB.加权.百分位', 'PE.加权', 'PE.加权.百分位', 'ROE'];
    const response = await axios.get(`/api/read_csv_data?list=${columns.join(',')}&type=1&label=${csv_label}`);
    const rows = response.data.data;
    return { columns, rows };
  };

  return (
    <div>
      <FormControl fullWidth sx={{ m: 2 }}>
        <InputLabel id="date-select-label">Select Date</InputLabel>
        <Select
          labelId="date-select-label"
          value={selectedDate}
          label="Select Date"
          onChange={handleDateChange}
        >
          {data.map((item, index) => (
            <MenuItem key={index} value={item.csv_label}>
              {item.update_date}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <TableContainer component={Paper}>
        <Typography variant="h6" sx={{ m: 2 }}>
          Valuation History
        </Typography>
        <Table>
          <TableHead>
            <TableRow>
              {tableData.columns.map((column, index) => (
                <TableCell key={index}>{column}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {tableData.rows.map((row, rowIndex) => (
              <TableRow key={rowIndex}>
                {tableData.columns.map((column, colIndex) => (
                  <TableCell key={colIndex}>
                    {row[colIndex]}
                    {colIndex === 2 && (
                      <ColorIndicator value={row[colIndex]} tipstr={`PB.加权.百分位 # ${row[colIndex]}`} />
                    )}
                    {colIndex === 4 && (
                      <ColorIndicator value={row[colIndex]} tipstr={`PE.加权.百分位 # ${row[colIndex]}`} />
                    )}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default ValuationHistory;
