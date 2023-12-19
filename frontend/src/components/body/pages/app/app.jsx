/*
Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at https://developer.cisco.com/docs/licenses.
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
*/

import { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Grid, Button, Select, MenuItem, FormControl, InputLabel, CircularProgress } from '@mui/material';
import axios from 'axios';

const AppPage = () => {
    const [selectedUser, setSelectedUser] = useState('');
    const [output, setOutput] = useState('');
    const [isRequestSent, setIsRequestSent] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [callerViewText, setCallerViewText] = useState('No push notification sent yet.');

    const users = ['rey_diaz', 'user_2', 'user_3']; // Replace with actual user list

    const handleSendPush = async () => {
        if (!selectedUser) {
            alert("Please select a user");
            return;
        }

        setIsLoading(true);
        setCallerViewText(`Sending push notification to ${selectedUser}...`);

        try {
            const response = await axios.post('http://localhost:8000/authenticate/', { email: selectedUser });
            if (response.data.output) {
                setOutput(response.data.output);
                setCallerViewText(`Push notification sent to ${selectedUser}. Awaiting response...`);
            } else {
                setOutput('No response received');
                setCallerViewText(`Push notification sent to ${selectedUser}. Awaiting response...`);
            }
            setIsRequestSent(true);
        } catch (error) {
            console.error('Error:', error);
            setOutput('An error occurred');
            setCallerViewText(`Push notification to ${selectedUser} failed!`);
        } finally {
            setIsLoading(false);
        }
    };

    const handleClearOutput = () => {
        setOutput('');
        setIsRequestSent(false);
        setCallerViewText('No push notification sent yet.');
    };

    useEffect(() => {
        if (isRequestSent && !isLoading) {
            const timer = setTimeout(() => {
                setCallerViewText(`Push notification to ${selectedUser} completed!`);
            }, 2000); // Show success message after 2 seconds (adjust as needed)
            return () => clearTimeout(timer);
        }
    }, [isRequestSent, isLoading, selectedUser]);

    return (
        <Grid container spacing={3} style={{ padding: 20 }}>
            {/* Call Center View */}
            <Grid item xs={12} md={6}>
                <Card style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'stretch' }}>
                    <CardContent>
                        <Typography variant="h5" gutterBottom>Call Center View</Typography>
                        <FormControl fullWidth>
                            <InputLabel id="user-select-label">User</InputLabel>
                            <Select
                                labelId="user-select-label"
                                value={selectedUser}
                                label="User"
                                onChange={(e) => setSelectedUser(e.target.value)}
                                disabled={isRequestSent || isLoading}
                            >
                                {users.map((user) => (
                                    <MenuItem key={user} value={user}>{user}</MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                        <Button 
                            variant="contained" 
                            color="primary" 
                            onClick={handleSendPush} 
                            disabled={isRequestSent || !selectedUser || isLoading}
                            style={{ marginTop: 20 }}
                        >
                            {isLoading ? <CircularProgress size={24} /> : 'Send Duo Push'}
                        </Button>
                        <Button
                            variant="outlined"
                            color="primary"
                            onClick={handleClearOutput}
                            style={{ marginTop: 20, marginLeft: 10 }}
                            disabled={!output}
                        >
                            Clear Output
                        </Button>
                        {output && (
                            <Typography paragraph style={{ marginTop: 20 }}>
                                Response: {output}
                            </Typography>
                        )}
                    </CardContent>
                </Card>
            </Grid>

            {/* Caller View */}
            <Grid item xs={12} md={6}>
                <Card style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <CardContent>
                        <Typography variant="h5" gutterBottom>Caller View</Typography>
                        {isLoading ? (
                            <div style={{ display: 'flex', alignItems: 'center' }}>
                                <CircularProgress style={{ marginRight: '10px' }} />
                                <Typography paragraph>
                                    {callerViewText}
                                </Typography>
                            </div>
                        ) : (
                            <Typography paragraph>
                                {callerViewText}
                            </Typography>
                        )}
                    </CardContent>
                </Card>
            </Grid>
        </Grid>
    );
};

export default AppPage;
