// Firebase konfiguratsiyasi
const firebaseConfig = {
    apiKey: "AIzaSyDOSnlheZfFA1d6P9a_LR441AImbIjisJE",
    authDomain: "coffe-shop-e6629.firebaseapp.com",
    projectId: "coffe-shop-e6629",
    storageBucket: "coffe-shop-e6629.firebasestorage.app",
    messagingSenderId: "1091790311107",
    appId: "1:1091790311107:web:b36087637d45c09bbc1c76",
    measurementId: "G-964MG6WLKC"
  };

// Firebase ilovasini boshlash
import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.15.0/firebase-app.js';
import { getFirestore, collection, addDoc } from 'https://www.gstatic.com/firebasejs/9.15.0/firebase-firestore.js';

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Form submit hodisasi
const contactForm = document.getElementById('contactForm');
contactForm.addEventListener('submit', async (e) => {
    e.preventDefault(); // Sahifa qayta yuklanishini oldini olish

    // Form ma'lumotlarini olish
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const subject = document.getElementById('subject').value;
    const message = document.getElementById('message').value;

    // Firestore'da saqlash
    try {
        const docRef = await addDoc(collection(db, 'messages'), {
            name: name,
            email: email,
            subject: subject,
            message: message
        });

        alert("Xabar muvaffaqiyatli yuborildi!");
        contactForm.reset(); // Formani tozalash
    } catch (error) {
        console.error("Xato yuz berdi:", error);
        alert("Xabarni yuborishda xato yuz berdi.");
    }
});
