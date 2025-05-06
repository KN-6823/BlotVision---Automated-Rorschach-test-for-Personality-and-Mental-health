require('dotenv').config();
const express = require('express');
const session = require('express-session');
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;
const path = require('path');
const forgotPasswordRoutes = require('./forgot_password'); // Import the forgot password routes

const app = express();

// View engine setup
app.set('view engine', 'hbs');
app.set('views', path.join(__dirname, 'templates'));

// Middleware
app.use(express.static('public')); // Serve static files
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Session setup
app.use(session({
    secret: process.env.SESSION_SECRET || 'your_secret_key', // Ensure this is set in your .env
    resave: false,
    saveUninitialized: false
}));

// Initialize Passport and restore authentication state from session
app.use(passport.initialize());
app.use(passport.session());

// Passport configuration
passport.serializeUser((user, done) => {
    done(null, user);
});

passport.deserializeUser((user, done) => {
    done(null, user);
});

// Google OAuth Strategy
passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID, // Ensure this is set in your .env
    clientSecret: process.env.GOOGLE_CLIENT_SECRET, // Ensure this is set in your .env
    callbackURL: "http://localhost:3000/auth/google/callback", // Ensure this matches your Google Cloud Console
    passReqToCallback: true
},
function(request, accessToken, refreshToken, profile, done) {
    return done(null, profile);
}));

// Routes
app.use(forgotPasswordRoutes); // Mount the forgot password routes

app.get('/', (req, res) => {
    res.redirect('/login');
});

app.get('/login', (req, res) => {
    res.render('login');
});

// Google OAuth routes
app.get('/auth/google',
    passport.authenticate('google', {
        scope: ['email', 'profile'],
        prompt: 'select_account'
    })
);

app.get('/auth/google/callback',
    passport.authenticate('google', {
        successRedirect: '/dashboard',
        failureRedirect: '/login'
    })
);

app.get('/dashboard', (req, res) => {
    if (req.isAuthenticated()) {
        res.render('dashboard', { user: req.user });
    } else {
        res.redirect('/login');
    }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
