const mongoose = require("mongoose");

// Define the Contact schema
const ContactSchema = new mongoose.Schema({
    name: { type: String, required: true },
    email: { type: String, required: true },
    subject: { type: String, required: true },
    message: { type: String, required: true },
}, { timestamps: true }); // Automatically add createdAt and updatedAt fields

const Contact = mongoose.model("Contact", ContactSchema);

module.exports = Contact;