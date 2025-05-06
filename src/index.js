const express = require("express");
const session = require("express-session");
const path = require("path");
const { Login, Image, Feedback } = require("./mongodb");
const mongoose = require("mongoose");
const forgotPasswordRouter = require("./forgot_password"); // Import the forgot password router
const bcrypt = require("bcrypt");

const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use('/css', express.static('css'));
app.use('/js', express.static('js'));
app.use('/img', express.static('img'));
app.use('/public', express.static('public'));

// Set up session
app.use(session({
    secret: "your_secret_key", // Replace with a strong secret
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false } // Set to true if using HTTPS
}));

// Handlebars setup
app.set('view engine', 'hbs');
app.set('views', path.join(__dirname, "../templates"));

// Connect to MongoDB
mongoose.connect("mongodb://localhost:27017/BlotVision", { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log("MongoDB connected"))
    .catch(err => console.error("MongoDB connection error:", err));

// Use the forgot password routes
app.use('/', forgotPasswordRouter); // Ensure this line is present

// Render home page as default
app.get('/', (req, res) => {
    res.redirect("/home");
});

// Render home page
app.get("/home", (req, res) => {
    const user = req.session.user;
    res.render("home", { user });
});

// Render login page
app.get("/login", (req, res) => {
    res.render("login");
});

// Render signup page
app.get("/signup", (req, res) => {
    res.render("signup");
});

// Render other pages
app.get("/about", (req, res) => {
    res.render("about");
});

app.get("/contact", (req, res) => {
    res.render("contact");
});

app.get("/test", (req, res) => {
    res.render("test");
});


app.post("/signup", async (req, res) => {
    try {
        const existingUser = await Login.findOne({ email: req.body.email });
        if (existingUser) {
            return res.status(400).send("User already exists with this email.");
        }

        // Hash the password before saving it
        const hashedPassword = await bcrypt.hash(req.body.password, 10);

        const user = new Login({
            name: req.body.name,
            email: req.body.email,
            password: hashedPassword,  // Save hashed password
            gender: req.body.gender,
            age: req.body.age,
        });

        await user.save();
        req.session.user = { name: user.name, email: user.email };
        res.redirect("/home");
    } catch (error) {
        console.error("Error during signup:", error);
        res.status(500).send("An error occurred during signup. Please try again.");
    }
});


app.post("/login", async (req, res) => {
    const { email, password } = req.body;

    try {
        // Find the user by email
        const user = await Login.findOne({ email });
        if (!user) {
            return res.status(400).send("Invalid email or password.");
        }

        // Compare the entered password with the stored hashed password
        const isMatch = await bcrypt.compare(password, user.password);

        // If the password doesn't match
        if (!isMatch) {
            return res.status(400).send("Invalid email or password.");
        }

        // If the password matches, log the user in
        req.session.user = { name: user.name, email: user.email };
        res.redirect("/home");
    } catch (error) {
        console.error("Login error:", error);
        res.status(500).send("An error occurred during login. Please try again.");
    }
});



// Route to submit feedback
app.post('/submit', async (req, res) => {
    try {
        console.log('Received feedback submission request');
        
        const { feedbackEntries } = req.body;
        const user = req.session.user;

        // Check if user is logged in
        if (!user) {
            console.log('User not logged in');
            return res.status(403).json({ error: "User not logged in." });
        }

        console.log('User found:', user);
        console.log('Received feedback entries:', feedbackEntries);

        // Validate feedback entries
        if (!feedbackEntries || !Array.isArray(feedbackEntries)) {
            console.log('Invalid feedback entries format:', feedbackEntries);
            return res.status(400).json({ error: "Invalid feedback data format." });
        }

        // Find or create user feedback document
        let userFeedback = await Feedback.findOne({ email: user.email });
        console.log('Existing user feedback found:', userFeedback ? 'Yes' : 'No');

        if (!userFeedback) {
            console.log('Creating new feedback document for user');
            userFeedback = new Feedback({
                username: user.name,
                email: user.email,
                feedbackSessions: []
            });
        }

        // Create new feedback session with proper structure
        const feedbackSession = {
            sessionDate: new Date(),
            feedbackEntries: feedbackEntries.map(entry => ({
                feedback: entry.feedback,
                imageIndex: entry.imageIndex,
                analysis: {
                    sentiment: entry.analysis?.Sentiment || {},
                    dominant_emotion: entry.analysis?.['Dominant Emotion'] || {},
                    personality_report: entry.analysis?.['Personality Report'] || {
                        Personality: '',
                        Strengths: [],
                        Weaknesses: [],
                        Approach: ''
                    }
                }
            }))
        };

        console.log('Created feedback session:', feedbackSession);

        // Add the new session to the user's feedback sessions
        userFeedback.feedbackSessions.push(feedbackSession);

        // Save to database
        console.log('Saving feedback to database...');
        await userFeedback.save();
        console.log('Feedback saved successfully');

        res.json({ 
            message: "Feedback submitted successfully!",
            session: feedbackSession
        });

    } catch (error) {
        console.error('Error in /submit route:', error);
        res.status(500).json({ 
            error: "Error saving feedback",
            details: error.message 
        });
    }
});

// Route to get images
app.get('/get-images', async (req, res) => {
    try {
        const images = await Image.find();
        const formattedImages = images.map(image => ({
            url: `data:image/jpeg;base64,${image.imageData}`,
            description: image.description,
        }));
        res.json(formattedImages);
    } catch (error) {
        console.error("Error fetching images:", error);
        res.status(500).send("Failed to fetch images");
    }
});

// Handle logout
app.get("/logout", (req, res) => {
    req.session.destroy((err) => {
        if (err) {
            console.error("Logout error:", err);
            return res.redirect("/home");
        }
        res.redirect("/login"); // Redirect to login page after logout
    });
});

// Start the server on port 3000
app.listen(3000, () => {
    console.log("Server running on port 3000");
});

app.use((req, res, next) => {
    res.set('Cache-Control', 'no-store');
    next();
});
