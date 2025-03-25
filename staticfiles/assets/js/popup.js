document.addEventListener('DOMContentLoaded', function () {
    const popup = document.getElementById('dating-tips-popup');
    const closeButton = document.querySelector('.close-button');
    const tipText = document.getElementById('dating-tip-text');

    const tips = [
        "Be yourself!",
        "Authenticity attracts genuine connections.",
        "Show interest in your match's hobbies and passions.",
        "Communicate openly.",
        "Be honestly from the start.",
        "Take your time to get to know each other.",
        "Respect boundaries and personal space.",
        "Plan thoughtful and creative dates.",
        "Listen more!",
        "Keep a positive attitude.",
        "smile often."
    ];

    let currentTip = 0;

    // Function to display the next tip
    function showNextTip() {
        tipText.textContent = tips[currentTip];
        currentTip = (currentTip + 1) % tips.length;
    }

    // Show pop-up after 3 seconds
    setTimeout(function () {
        popup.classList.remove('hidden');
        // Trigger CSS transition
        setTimeout(function () {
            popup.classList.add('show');
        }, 10); // Slight delay to allow CSS transition

        // Show next tip every 10 seconds
        showNextTip();
        setInterval(showNextTip, 10000);
    }, 3000); // 3-second delay before showing pop-up

    // Close pop-up when close button is clicked
    closeButton.addEventListener('click', function () {
        popup.classList.remove('show');
        // Hide pop-up after transition
        setTimeout(function () {
            popup.classList.add('hidden');
        }, 500); // Match the CSS transition duration
    });

    // Optional: Hide pop-up when clicking outside of it
    window.addEventListener('click', function (event) {
        if (event.target == popup) {
            popup.classList.remove('show');
            setTimeout(function () {
                popup.classList.add('hidden');
            }, 500);
        }
    });
});