import { initializeApp } from 'firebase/app';
import { initializeAuth, getReactNativePersistence } from 'firebase/auth';
import ReactNativeAsyncStorage from '@react-native-async-storage/async-storage';

const firebaseConfig = {
  apiKey: "AIzaSyAObPxjAFK37PO76xDA0HhbyUQnnq7C2vs",
  authDomain: "gidadb-5117c.firebaseapp.com",
  projectId: "gidadb-5117c",
  storageBucket: "gidadb-5117c.firebasestorage.app",
  messagingSenderId: "855880633193",
  appId: "1:855880633193:web:cf1b0bba16875160440bf8",
  measurementId: "G-QT33CTMLHL"
};

const app = initializeApp(firebaseConfig);

const auth = initializeAuth(app, {
  persistence: getReactNativePersistence(ReactNativeAsyncStorage)
});

export { app, auth };