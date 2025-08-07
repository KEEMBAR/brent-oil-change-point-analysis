import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';

const VolatilityChart = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:5000/api/prices')
            .then(response => {
                const prices = response.data;
                const result = computeVolatility(prices);
                setData(result);
            })
            .catch(error => console.error('Error fetching volatility data:', error));
    }, []);

    // Calculate rolling volatility
    const computeVolatility = (prices) => {
        const windowSize = 7; // 7-day window
        const result = [];

        for (let i = windowSize; i < prices.length; i++) {
            const slice = prices.slice(i - windowSize, i);
            const returns = slice.map((d, idx, arr) => {
                if (idx === 0) return 0;
                return (arr[idx].Price - arr[idx - 1].Price) / arr[idx - 1].Price;
            }).slice(1);

            const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
            const variance = returns.reduce((sum, r) => sum + (r - mean) ** 2, 0) / returns.length;
            const volatility = Math.sqrt(variance);

            result.push({
                Date: prices[i].Date,
                Volatility: Number((volatility * 100).toFixed(3))
            });
        }

        return result;
    };

    return (
        <div>
            <h2>Volatility Over Time</h2>
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="Date" tick={{ fontSize: 10 }} />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="Volatility" stroke="#82ca9d" dot={false} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default VolatilityChart;
