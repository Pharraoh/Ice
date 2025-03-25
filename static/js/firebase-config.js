// Replace with your Firebase Config
const firebaseConfig = {
  apiKey: "AIzaSyDD6NNHOhhWb9chhPTg7IGdLYFCLNBUh_g",
  authDomain: "icee-3a0d4.firebaseapp.com",
  projectId: "icee-3a0d4",
  storageBucket: "icee-3a0d4.firebasestorage.app",
  messagingSenderId: "344476593056",
  appId: "1:344476593056:web:8e615a5c96f38c9f07d2c5",
  measurementId: "G-M8QLHJC0DZ"
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.firestore();
