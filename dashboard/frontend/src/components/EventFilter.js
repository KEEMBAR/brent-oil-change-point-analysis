import React, { useEffect, useState } from 'react';
import axios from 'axios';

const EventFilter = ({ onSelect }) => {
    const [events, setEvents] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:5000/api/events')
            .then(response => setEvents(response.data))
            .catch(error => console.error('Error fetching events:', error));
    }, []);

    return (
        <div style={{ marginBottom: '1rem' }}>
            <label style={{ marginRight: '10px' }}>Filter by Event:</label>
            <select onChange={(e) => onSelect(e.target.value)}>
                <option value="">All</option>
                {events.map((event, index) => (
                    <option key={index} value={event.date}>
                        {event.title} ({event.date})
                    </option>
                ))}
            </select>
        </div>
    );
};

export default EventFilter;
