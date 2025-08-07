import React, { useState } from 'react';
import EventFilter from './EventFilter';
import PriceChart from './PriceChart';
import VolatilityChart from './VolatilityChart';

const Dashboard = () => {
    const [selectedDate, setSelectedDate] = useState("");

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial' }}>
            <h1 style={{ textAlign: 'center' }}>Brent Oil Change Point Dashboard</h1>

            <div style={{
                maxWidth: '1000px',
                margin: '0 auto',
                backgroundColor: '#f9f9f9',
                padding: '20px',
                borderRadius: '10px',
                boxShadow: '0px 0px 10px rgba(0,0,0,0.1)'
            }}>
                <EventFilter onSelect={setSelectedDate} />
                <PriceChart selectedDate={selectedDate} />
                <VolatilityChart />
            </div>
        </div>
    );
};

export default Dashboard;
