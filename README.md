# 🧠 BlotVision

BlotVision is an AI-driven web platform designed to automate and enhance psychological assessment using the Rorschach Inkblot Test. It streamlines test delivery, provides real-time analysis of user feedback, and generates personality reports using NLP and CNN-based models. Key features include standardized scoring, progress tracking for long-term assessment, and an intuitive interface for both users and clinicians, making mental health evaluation more accessible, consistent, and insightful.

---

## 🌟 Features

- 🔐 **User Authentication**: Signup and login functionality with secure password hashing.
- 🖼️ **Image-Based Feedback**: Users can provide insights for a series of images.
- 🧠 **Feedback Analysis**:
  - Sentiment Analysis
  - Emotion Detection
  - MBTI Personality Classification
- 📄 **Dynamic Report Generation**: Generates a downloadable personality report based on user feedback.
- 🗃️ **MongoDB Storage for User Data & Feedback**

---

## 🛠️ Tech Stack

### Backend
- **Node.js**: Server-side runtime.
- **Express.js**: Web framework for building RESTful APIs.
- **Flask**: Python-based backend for advanced ML model integration.
- **MongoDB**: NoSQL database for storing user data and feedback.

### Frontend
- **HTML/CSS**: For structuring and styling the web pages.
- **Bootstrap**: Responsive design framework.
- **JavaScript**: For dynamic interactions and API calls.

### Machine Learning
- **Transformers**: Pre-trained models for sentiment analysis, emotion detection, and MBTI classification.
- **Pandas**: For data manipulation and CSV handling.
- **Pillow**: For generating dynamic personality report images.

---

## 📈 How It Works

1. **User Flow**:
   - Users sign up or log in to access the test.
   - They provide feedback for a series of images.
   - Feedback is analyzed using ML models, and a personality report is generated.

2. **Backend Flow**:
   - Feedback is sent to the `/submit` endpoint and stored in MongoDB.
   - The Flask server processes the feedback using ML models and generates a report.

3. **Report Generation**:
   - The Flask server uses `Pillow` to create a dynamic personality report image.
   - The report is sent back to the frontend for download.

---

## 🚀 Future Enhancements

- **Admin Dashboard**: Manage users and feedback.
- **Advanced Analytics**: Provide deeper insights into user feedback.
- **Cloud Deployment**: Deploy the application on AWS/GCP.

---

## 📸 Screenshots
![image](https://github.com/user-attachments/assets/1afdc6d7-f2d3-4388-8b56-23799d0e5c29)
![image](https://github.com/user-attachments/assets/f3ce13e1-d4e5-44a4-a8c3-ac02b52e0323)

![image](https://github.com/user-attachments/assets/fe3ec0ec-7fc9-4e70-b91d-d21654e5545f)
![image](https://github.com/user-attachments/assets/e8170556-afe3-4692-a703-8a50d72c045b)
![image](https://github.com/user-attachments/assets/5fa5b1e9-9ec3-41ae-b4af-54995f6f1fd7)

---

## 📦 Installation

### Prerequisites
- **Node.js** (v14+)
- **Python** (v3.8+)
- **MongoDB** (local or cloud instance)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/blotvision.git
   cd blotvision
   ```

2. **Install Node.js Dependencies**:
   ```bash
   cd src
   npm install
   ```

3. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```
     MONGODB_URI=mongodb://localhost:27017/BlotVision
     ```

5. **Start MongoDB**:
   - Ensure MongoDB is running locally or provide a cloud connection string in `.env`.

6. **Run the Node.js Server**:
   ```bash
   cd src
   node index.js
   ```

7. **Run the Flask Server**:
   ```bash
   python app.py
   ```

8. **Access the Application**:
   - Open your browser and navigate to `http://localhost:3000`.

---
