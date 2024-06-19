const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

//MongoDB connection string to use when running locally (line 15)
const MongoDBLocalConnection = "mongodb://localhost/userData"
//MongoDB connection string to use when running on docker (line 15)
const monogoDBConnection = "mongodb://mongo/userData"

// MongoDB connection
mongoose.connect(monogoDBConnection, { useNewUrlParser: true, useUnifiedTopology: true });
const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));

// Mongoose Schema and Model
const userDataSchema = new mongoose.Schema({
    email: String,
    preferences: [String]
});

const UserData = mongoose.model('UserData', userDataSchema);

// Middleware
app.use(bodyParser.json());
app.use(cors());

// Routes
app.post('/submit', (req, res) => {
    const userData = new UserData(req.body);
    res.setHeader('Access-Control-Allow-Credentials', true)
    if (req.headers.origin && ['http://localhost:3000', 'http://localhost:3001'].includes(req.headers.origin)) {
        res.setHeader('Access-Control-Allow-Origin', req.headers.origin);
    }
    userData.save()
        .then(() => {
            console.log("Data saved successfully", userData);
            res.json({ message: 'Form data saved successfully!' });
        })
        .catch(error => {
            console.log("Failed to save data", userData);
            res.status(500).json({ error: 'Error saving form data' });
        });
});

app.get('/userData', (req, res) => {
    UserData.find({})
        .then(data => {
            res.json(data);
        })
        .catch(error => {
            res.status(500).json({ error: 'Error fetching user data' });
        });
});

// Start Server
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
