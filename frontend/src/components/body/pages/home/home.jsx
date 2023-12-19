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

/* eslint-disable react/no-unescaped-entities */

import { Container, Typography, Box, Paper } from '@mui/material';

const HomePage = () => {
    return (
        <Container maxWidth="md">
            <Box my={4}>
                <Typography variant="h4" gutterBottom>
                    Duo Security Two-Factor Authentication Workflow
                </Typography>
                <Paper elevation={3} style={{ padding: '20px', marginTop: '20px' }}>
                    <Typography variant="h6" gutterBottom>
                        Overview
                    </Typography>
                    <Typography paragraph>
                        This application demonstrates the workflow of a call center employee 
                        who sends a Duo push notification to a caller to verify their identity. 
                        It's designed as a proof of concept for secure authentication in customer support scenarios.
                    </Typography>
                    <Typography variant="h6" gutterBottom>
                        How it Works
                    </Typography>
                    <Typography paragraph>
                        1. The call center employee enters the caller's email.
                    </Typography>
                    <Typography paragraph>
                        2. The script initiates a Duo Security push notification to the caller's device.
                    </Typography>
                    <Typography paragraph>
                        3. The caller receives the push notification and responds.
                    </Typography>
                    <Typography paragraph>
                        4. The script checks the response and either authenticates or denies access based on the caller's response.
                    </Typography>
                    <Typography paragraph>
                        This system enhances security by ensuring that the person on the call is the legitimate account holder, thereby preventing unauthorized access.
                    </Typography>
                </Paper>
            </Box>
        </Container>
    );
};

export default HomePage;
