import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
    ReferenceLine,
} from 'recharts';

const PriceChart = () => {
    const [priceData, setPriceData] = useState([]);
    const [changepoints, setChangepoints] = useState([]);

    useEffect(() => {
        // Fetch oil price data
        axios
            .get('http://localhost:5000/api/prices')
            .then((response) => setPriceData(response.data))
            .catch((error) => console.error('Error fetching prices:', error));

        // Fetch changepoints
        axios
            .get('http://localhost:5000/api/changepoints')
            .then((response) => setChangepoints(response.data))
            .catch((error) => console.error('Error fetching changepoints:', error));
    }, []);

    return (
        <div>
            <h2>Brent Oil Prices</h2>
            <ResponsiveContainer width="100%" height={400}>
                <LineChart data={priceData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="Date" tick={{ fontSize: 10 }} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line
                        type="monotone"
                        dataKey="Price"
                        stroke="#8884d8"
                        dot={false}
                    />

                    {changepoints.map((cp, index) => (
                        <ReferenceLine
                            key={index}
                            x={cp.Date}
                            stroke="red"
                            strokeDasharray="3 3"
                            label={{
                                value: 'CP',
                                position: 'top',
                                fontSize: 10,
                                fill: 'red',
                            }}
                        />
                    ))}
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default PriceChart;
