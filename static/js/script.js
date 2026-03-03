// Firebase imports
import { initializeApp } from "firebase/app";
import { getAuth, signInWithPopup, GoogleAuthProvider, signOut } from "firebase/auth";

// Your Firebase config
const firebaseConfig = {
    apiKey: "AIzaSyCOBhB7W5NhsiqpgH_7g4nUnrE6dwe-ueA",
    authDomain: "medfinder-782ad.firebaseapp.com",
    projectId: "medfinder-782ad",
    storageBucket: "medfinder-782ad.firebasestorage.app",
    messagingSenderId: "525471729907",
    appId: "1:525471729907:web:bf5a323d019483df0f8f86",
    measurementId: "G-RVCHLEYVDY"
  };

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// Sign in function
export function googleSignIn() {
  signInWithPopup(auth, provider)
    .then((result) => {
      const user = result.user;
      alert(`Welcome ${user.displayName}`);
      console.log(user); // Send data to backend if needed
    })
    .catch((error) => {
      console.error("Error during sign-in:", error);
    });
}

// Sign out function
export function googleSignOut() {
  signOut(auth)
    .then(() => {
      alert("Signed out successfully.");
    })
    .catch((error) => {
      console.error("Sign-out error:", error);
    });
}