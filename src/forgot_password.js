const express = require("express");
const path = require("path");
const bcrypt = require("bcrypt");
const nodemailer = require("nodemailer");
const crypto = require("crypto");
const { Login } = require("./mongodb"); // Ensure this matches your export
const router = express.Router();
require("dotenv").config();

// Serve static files
router.use(express.static(path.join(__dirname, 'public')));

// Render forgot password page
router.get('/forgot-password', (req, res) => {
    res.render('fp');  
});

// POST request to handle the Forgot Password form submission
const sentTokens = new Set(); // Prevent duplicate email sends

router.post("/fp", async (req, res) => {
    const email = req.body.email;

    console.log(`Received email: ${email}`);

    if (!email) {
        return res.status(400).send("Email is required.");
    }

    try {
        const user = await Login.findOne({ email });
        if (!user) {
            return res.status(400).send("No user found with that email.");
        }

        if (sentTokens.has(email)) {
            return res.status(429).send("A reset email has already been sent. Please check your inbox.");
        }

        // Generate a unique token for password reset
        const token = generateResetToken();

        // Save the token and expiration time in the user's record
        user.resetToken = token;
        user.resetTokenExpiry = Date.now() + 3600000; // 1 hour expiry
        await user.save(); // Ensure you save the user after updating

        const resetLink = `http://localhost:3000/rp?token=${token}&email=${email}`;

        // Send the reset email
        await sendResetEmail(email, resetLink);
        sentTokens.add(email); // Mark email as sent to prevent duplicates
        res.send("Reset email sent! Please check your inbox.");
    } catch (error) {
        console.error("Error during password reset processing:", error);
        res.status(500).send("An error occurred while processing your request. Please try again later.");
    }
});

// Helper function to send reset email
async function sendResetEmail(email, resetLink) {
    let transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
            user: process.env.EMAIL_USER, // EMAIL_USER from .env
            pass: process.env.EMAIL_PASSKEY, // EMAIL_PASSKEY from .env
        },
    });

    let mailOptions = {
        from: `"BlotVision Support" <${process.env.EMAIL_USER}>`, // Better sender name
        to: email,
        subject: 'Password Reset Request',
        html: `
        <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #4c6bff;">Password Reset Request</h2>
            <p>Hello,</p>
            <p>We received a request to reset your password for your BlotVision account associated with this email address.</p>
            <p>Click the button below to reset your password. This link will expire in <strong>1 hour</strong>.</p>
            <div style="margin: 20px;">
                <a href="${resetLink}" style="background-color: #4c6bff; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a>
            </div>
            <p>If you did not request this, you can safely ignore this email.</p>
            <p style="color: #888;">Thank you,<br>BlotVision Team</p>
            <hr>
            <p style="font-size: 12px; color: #888;">
                If the button above does not work, copy and paste this link into your browser: <br>
                <a href="${resetLink}" style="color: #4c6bff;">${resetLink}</a>
            </p>
        </div>
        `
    };
    

    await transporter.sendMail(mailOptions);
}

// Generate a unique reset token
function generateResetToken() {
    return crypto.randomBytes(32).toString('hex');
}

// GET request to show the reset password form
router.get("/rp", (req, res) => {
    const { token, email } = req.query;
    if (!token || !email) {
        return res.status(400).send("Invalid token or email.");
    }
    // Render the password reset page with token and email
    res.render("rp", { token, email });
});

router.post("/rp", async (req, res) => {
    const { email, token, newPassword, confirmPassword } = req.body;

    // Log the received passwords for debugging
    console.log("New Password:", newPassword);
    console.log("Confirm Password:", confirmPassword);

    // Check if new passwords match
    if (newPassword !== confirmPassword) {
        return res.status(400).send("Passwords do not match.");
    }

    // Optional: Check password complexity
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;
    if (!passwordRegex.test(newPassword)) {
        return res.status(400).send("Password must be at least 8 characters long and include uppercase, lowercase, a number, and a special character.");
    }

    try {
        // Find the user by email
        const user = await Login.findOne({ email });
        console.log("User found:", user); // Log the user object

        // Validate the user and token
        if (!user || user.resetToken !== token || user.resetTokenExpiry < Date.now()) {
            return res.status(400).send("Invalid or expired token.");
        }

        // Hash the new password before storing it
        const hashedPassword = await bcrypt.hash(newPassword, 10);
        user.password = hashedPassword;  // Store the hashed password
        user.resetToken = undefined; // Clear the reset token
        user.resetTokenExpiry = undefined; // Clear the expiry

        // Attempt to save the user
        const updatedUser = await user.save(); // Ensure you save the changes
        console.log("User updated:", updatedUser); // Log the updated user object

        sentTokens.delete(email); // Allow new reset requests
        res.redirect("/login");
    } catch (error) {
        console.error("Error during password reset:", error);
        res.status(500).send("An error occurred while resetting your password. Please try again later.");
    }
});


module.exports = router;
