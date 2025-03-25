const chatContainer = document.getElementById('chat-container');
const messageForm = document.getElementById('message-form');
const messageInput = document.getElementById('message');

// Get current user
auth.onAuthStateChanged(user => {
  if (user) {
    loadMessages(user.uid);
  } else {
    // Redirect to login if not logged in
    window.location.href = '/accounts/login/';
  }
});

// Load Messages
function loadMessages(userId) {
  db.collection('messages')
    .orderBy('timestamp')
    .onSnapshot(snapshot => {
      chatContainer.innerHTML = '';
      snapshot.forEach(doc => {
        const message = doc.data();
        const messageDiv = document.createElement('div');
        messageDiv.textContent = `${message.sender}: ${message.text}`;
        chatContainer.appendChild(messageDiv);
      });
    });
}

// Send Message
messageForm.addEventListener('submit', e => {
  e.preventDefault();
  const text = messageInput.value;
  if (text.trim() !== '') {
    db.collection('messages').add({
      sender: auth.currentUser.email,
      text: text,
      timestamp: firebase.firestore.FieldValue.serverTimestamp()
    });
    messageInput.value = '';
  }
});
