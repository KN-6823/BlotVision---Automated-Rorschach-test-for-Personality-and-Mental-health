const mongoose = require("mongoose");

// Define the Login schema
const LoginSchema = new mongoose.Schema({
    name: { type: String, required: true },
    email: { type: String, required: true, unique: true },
    gender: { type: String, enum: ["Male", "Female", "Other"], required: true },
    age: { type: Number, min: 18, max: 100, required: true },
    password: { type: String, required: true },
    resetToken: { type: String },
    resetTokenExpiry: { type: Date },
    lastResetRequest: { type: Date }
});

// Model for Login schema
const Login = mongoose.model("Login-Credentials", LoginSchema, "login-credentials");

module.exports = { Login }; // Ensure you're exporting the Login model correctly
// Define the Image schema
const ImageSchema = new mongoose.Schema({
    imageData: { type: String, required: true },
    description: { type: String, required: true },
});

// Model for Image schema
const Image = mongoose.model("Image", ImageSchema, "images");

// Define the Feedback schema
const FeedbackSchema = new mongoose.Schema({
    username: { type: String, required: true },
    email: { type: String, required: true },
    feedbackSessions: [
        {
            sessionDate: { type: Date, default: Date.now },
            feedbackEntries: [
                {
                    feedback: { type: String, required: true },
                    imageIndex: { type: Number, required: true },
                    analysis: {
                        sentiment: Object,
                        dominant_emotion: Object,
                        personality_report: {
                            Personality: String,
                            Strengths: [String],
                            Weaknesses: [String],
                            Approach: String
                        }
                    }
                }
            ],
            finalReport: {
                summary_report: {
                    Final_Sentiment: String,
                    Final_Emotion: String,
                    Final_Form_Quality: String,
                    Final_Developmental_Quality: String
                }
            }
        }
    ]
});

// Model for Feedback schema
const Feedback = mongoose.model("Feedback", FeedbackSchema, "feedbacks");

mongoose.connect("mongodb://localhost:27017/BlotVision")
    .then(() => console.log("MongoDB connected"))
    .catch(err => console.error("MongoDB connection error:", err));

module.exports = { Login, Image, Feedback };
