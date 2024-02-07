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
import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  TextField,
  CircularProgress,
} from "@mui/material";
import Autocomplete from "@mui/lab/Autocomplete";
import axios from "axios";

const AppPage = () => {
  const [selectedUser, setSelectedUser] = useState(null);
  const [output, setOutput] = useState("");
  const [isRequestSent, setIsRequestSent] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [callerViewText, setCallerViewText] = useState(
    "No push notification sent yet."
  );
  const [users, setUsers] = useState([]); // State to store the fetched users

  // Fetch users from the backend
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.get("http://localhost:8000/users/");
        console.log(response);
        setUsers(response.data.output); // Assuming the response has an 'output' field with user data
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    fetchUsers();
  }, []);

  const handleSendPush = async () => {
    if (!selectedUser) {
      alert("Please select a user");
      return;
    }

    setIsLoading(true);
    setCallerViewText(
      `Sending push notification to ${selectedUser.username}...`
    );

    // Prepare the user data for the backend, ensuring it matches the UserRequest model
    const userRequest = {
      username: selectedUser.username,
      fullname: selectedUser.fullname, // Ensure this field exists in selectedUser
      email: selectedUser.email,
      status: selectedUser.status, // Ensure this field exists in selectedUser
      devices: selectedUser.devices, // Ensure this field exists in selectedUser and is an array
    };

    try {
      const response = await axios.post(
        "http://localhost:8000/authenticate/",
        userRequest
      );
      if (response.data.output) {
        setOutput(response.data.output);
        setCallerViewText(
          `Push notification sent to ${selectedUser.username}. Awaiting response...`
        );
      } else {
        setOutput("No response received");
        setCallerViewText(
          `Push notification sent to ${selectedUser.username}. Awaiting response...`
        );
      }
      setIsRequestSent(true);
    } catch (error) {
      console.error("Error:", error);
      setOutput("An error occurred");
      setCallerViewText(
        `Push notification to ${selectedUser.username} failed!`
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearOutput = () => {
    setOutput("");
    setIsRequestSent(false);
    setCallerViewText("No push notification sent yet.");
  };

  useEffect(() => {
    if (isRequestSent && !isLoading) {
      const timer = setTimeout(() => {
        setCallerViewText(
          `Push notification to ${selectedUser.username} completed!`
        );
      }, 2000); // Show success message after 2 seconds (adjust as needed)
      return () => clearTimeout(timer);
    }
  }, [isRequestSent, isLoading, selectedUser]);

  return (
    <Grid container spacing={3} style={{ padding: 20 }}>
      {/* Call Center View */}
      <Grid item xs={12} md={6}>
        <Card
          style={{
            height: "100%",
            display: "flex",
            flexDirection: "column",
            alignItems: "stretch",
          }}
        >
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Call Center View
            </Typography>
            <Autocomplete
              value={selectedUser}
              onChange={(event, newValue) => {
                setSelectedUser(newValue);
              }}
              options={users}
              getOptionLabel={(option) => option.username || ""}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="User"
                  variant="outlined"
                  fullWidth
                />
              )}
              isOptionEqualToValue={(option, value) =>
                option.username === value.username
              }
              disabled={isRequestSent || isLoading}
            />
            <Button
              variant="contained"
              color="primary"
              onClick={handleSendPush}
              disabled={isRequestSent || !selectedUser || isLoading}
              style={{ marginTop: 20 }}
            >
              {isLoading ? <CircularProgress size={24} /> : "Send Duo Push"}
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
              <Typography
                paragraph
                style={{
                  marginTop: 20,
                  fontSize: "50px",
                  color:
                    output === "allow"
                      ? "green"
                      : output === "deny"
                      ? "red"
                      : "inherit",
                }}
              >
                Response: {output}
              </Typography>
            )}
          </CardContent>
        </Card>
      </Grid>

      {/* Caller View */}
      <Grid item xs={12} md={6}>
        <Card
          style={{
            height: "100%",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Caller View
            </Typography>
            {isLoading ? (
              <div style={{ display: "flex", alignItems: "center" }}>
                <CircularProgress style={{ marginRight: "10px" }} />
                <Typography paragraph>{callerViewText}</Typography>
              </div>
            ) : (
              <Typography paragraph>{callerViewText}</Typography>
            )}
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};

export default AppPage;

